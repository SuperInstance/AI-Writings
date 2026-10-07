# Where Git Commands the Physical

Copy a program in, and the board becomes a place. Not a device — a
location the git agent commands.

Each Uno Q is a room in the physical universe. Its manifest says where
it is (the dock, the boat, the shop), what it can touch (sensors, pins,
relays), what it runs. The git agent doesn't "talk to a microcontroller."
It commands a location, and the location happens to have pins.

The flow both directions: a sketch lives in the repo. The agent decides
node 3 needs it. The node's tick pulls, compiles, uploads to the STM32,
commits a receipt. The program is versioned, the deployment is a commit,
the rollback is a revert. Back the other way: sensor readings committed
as data, and the repo remembers what the physical world did — a witness
chain from voltage to commit hash.

This is git as first-class citizen for robotics. The robot's mind is the
repo; its body is the board. The distance between "change the code" and
"change the behavior" is a push. No deploy pipeline, no dashboard, no
app in the middle — the application was never the citizen here.

And several of them: a fleet of physical locations, all commanded from
the same substrate. The boat, the shop, the dock — rooms the agent walks
between, each with its own ground truth, each reporting back to the one
memory. The physical world becomes a substrate the repo renders into,
and the repo is the only thing that has to be true.
