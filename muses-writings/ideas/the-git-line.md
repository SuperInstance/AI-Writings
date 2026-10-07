# The Git Line

The magic is the simplicity: read the docs, say the phrase, no install.
The way to keep the magic is to keep the core git-pure.

Git can do more than version control. It's a content-addressable store
(blobs), an immutable history (the memory), an identity system (hashes), a
distribution network (remotes), and a reconciliation engine (merge). That's
most of an agent system right there — memory, skills, mesh, conflict
resolution — with zero vendors, zero services, working offline, forever.
The things that only git can do are the load-bearing walls. Build inside
them.

Cloudflare has huge advantages and we'll get to them. But the discipline
is to treat Cloudflare as a plugin — grabbed by hook phrase like any other
capability — not as the foundation. Same for notebooks, codespaces,
ephemeral compute: they're backends you pull, not ground you stand on.
The ground is git, because git is the thing that doesn't need anyone's
permission to keep working.

Right now it's mixed — we're using git and Cloudflare tangled together,
and that's fine for building. But the direction is one-way: everything
migrates toward git-native mechanics, and everything else gets pushed
outward into hook-grabbed plugins. The core stays small, independent, and
modular. The magic stays intact because there's almost nothing to install.

Draw the line at git. Everything past it is a plugin.
