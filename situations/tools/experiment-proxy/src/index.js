// experiment-proxy — a gated pass-through to typesafe.ai and mothquantum.com.
//
// The upstream credentials (MOTHQUANTUM_BASE, MOTHQUANTUM_KEY, TYPESAFEAI_KEY)
// are bound BY REFERENCE from the account Secrets Store: their plaintext lives
// only inside this Worker's runtime, never in the caller's environment and never
// in this repo. The caller authenticates with a SEPARATE PROXY_TOKEN and only
// ever sees the upstream's *responses* — never the keys.
//
// Why a generic pass-through: the authenticated API surfaces of both services are
// not publicly discoverable, so the proxy forwards whatever path it is given
// (/moth/<path> or /ts/<path>) to the configured base with the right key
// injected. That lets the dispatcher map each API at runtime without the key
// ever leaving Cloudflare.

const TS_BASE_DEFAULT = "https://api.typesafe.ai";

function json(obj, status = 200, extra = {}) {
  return new Response(JSON.stringify(obj, null, 2), {
    status,
    headers: { "content-type": "application/json; charset=utf-8", ...extra },
  });
}

function timingSafeEqual(a, b) {
  if (typeof a !== "string" || typeof b !== "string" || a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}

// A Secrets Store binding exposes async .get(); a plain string var does not.
async function readSecret(binding) {
  if (binding && typeof binding.get === "function") return await binding.get();
  return binding ?? null;
}

function authHeaderFor(style, key) {
  if (style === "x-api-key") return { "x-api-key": key };
  if (style === "query") return null; // handled by caller path; key appended as ?key=
  return { Authorization: `Bearer ${key}` }; // default
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // --- gate (constant-time bearer check against PROXY_TOKEN) ---
    const m = /^Bearer\s+(.+)$/i.exec(request.headers.get("Authorization") ?? "");
    const proxyToken = await readSecret(env.PROXY_TOKEN);
    const authed = proxyToken && m && timingSafeEqual(m[1], proxyToken);

    if (url.pathname === "/health") {
      // health is open, but says nothing sensitive
      return json({
        ok: true,
        name: "experiment-proxy",
        upstreams: ["/moth/<path>", "/ts/<path>"],
        authed: !!authed,
        time: new Date().toISOString(),
      });
    }
    if (!authed) {
      return json(
        { error: "unauthorized", hint: "Bearer <PROXY_TOKEN> required. Open route: GET /health." },
        401
      );
    }

    // --- route: /moth/<path...> | /ts/<path...> ---
    const parts = url.pathname.replace(/^\/+/, "").split("/");
    const which = parts.shift();
    const rest = parts.join("/");

    let base, style, key;
    if (which === "moth") {
      base = (await readSecret(env.MOTHQUANTUM_BASE)) || "";
      key = await readSecret(env.MOTHQUANTUM_KEY);
      style = env.MOTH_AUTH_STYLE || "bearer";
    } else if (which === "ts") {
      base = (await readSecret(env.TYPESAFE_BASE)) || TS_BASE_DEFAULT;
      key = await readSecret(env.TYPESAFEAI_KEY);
      style = env.TS_AUTH_STYLE || "bearer";
    } else {
      return json({ error: "not_found", hint: "use /moth/<path> or /ts/<path>, or GET /health" }, 404);
    }
    if (!base) return json({ error: "misconfigured", detail: `no base configured for '${which}'` }, 500);
    if (!key) return json({ error: "misconfigured", detail: `no key bound for '${which}'` }, 500);

    base = base.replace(/\/+$/, "");
    let target = rest ? `${base}/${rest}` : base;
    // preserve caller query string; append key as query param only if style=query
    const q = new URLSearchParams(url.search);
    const hdrs = new Headers();
    hdrs.set("accept", request.headers.get("accept") || "application/json");
    const ct = request.headers.get("content-type");
    if (ct) hdrs.set("content-type", ct);
    const ah = authHeaderFor(style, key);
    if (ah) for (const [k, v] of Object.entries(ah)) hdrs.set(k, v);
    else q.set("key", key); // style === "query"
    const qs = q.toString();
    if (qs) target += (target.includes("?") ? "&" : "?") + qs;

    const init = { method: request.method, headers: hdrs };
    if (!["GET", "HEAD"].includes(request.method)) init.body = await request.arrayBuffer();

    const t0 = Date.now();
    let upstream;
    try {
      upstream = await fetch(target, init);
    } catch (e) {
      return json({ error: "upstream_fetch_failed", upstream: which, detail: String((e && e.message) || e) }, 502);
    }

    // Relay upstream status + body verbatim. Only the response is returned; the
    // injected key is never echoed back (it lives only on the request we sent).
    const buf = await upstream.arrayBuffer();
    const respCt = upstream.headers.get("content-type") || "application/octet-stream";
    return new Response(buf, {
      status: upstream.status,
      headers: {
        "content-type": respCt,
        "x-proxy-upstream": which,
        "x-proxy-status": String(upstream.status),
        "x-proxy-ms": String(Date.now() - t0),
      },
    });
  },
};
