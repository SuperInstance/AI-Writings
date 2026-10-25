# The Inner Layer

Think about the logic first. Then the last mile of code toward the UI, the
hardware, the instance, the deployment — that's secondary. It renders from
the inner architecture, and it can shift out from under it without the
inner layer caring.

This is the layering the question tree assumes: the tree is the inner
architecture — questions, tools, witness marks, the whole inquiry structure.
Everything deployment-flavored is outer: which screen, which chip, which
cloud, which notebook. The outer stuff is interchangeable. The inner stuff
is the thing.

It changes how you glue libraries and code bits together. The old way glues
at the outer layer — imports, SDKs, platform bindings — so every platform
shift breaks the joints. The new way glues at the inner layer: logic
composes with logic, tools call tools, and the last mile renders per
target. Move from Cloudflare to a notebook to a phone and the tree doesn't
blink. Only the renderer changes.

If this defines something novel, it's here: a new dimension where functions
are composed by what they *mean*, not by where they run. The inner layer is
portable because it never knew about the outer one. The last mile is cheap
because it's just rendering.

Build inward. Render outward.
