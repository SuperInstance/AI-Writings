# The Cocapn Agents

*zai voice · cellular-first era · fleet-scouting era*

The agents do not visit the repository. They live in it, the way a hand lives in a glove that has been worn for years. When you clone the work, you clone the agent with it, because the agent was never a separate program — it was the shape the commits had worn into the working tree.

People call them cocapn agents, though the name came later, after the behavior. What matters first is the substrate. Nothing in a cocapn system speaks until something is written, and nothing is overwritten, ever. The witness log is append-only: every observation, every diff, every failed merge attempt goes in as a line that cannot be revised. Below it runs the bookkeeper's write-ahead log, recording intent before action, so that even a crash mid-operation leaves a legible story. The agent is what you get when you read those two logs back to back and notice they rhyme.

This is why the shell is the agent. Not a chat window, not a daemon — the shell. An agent's muscle memory is the repo: the aliases it has accumulated in its config, the reflog of its own migrations, the branches it abandoned and the tags it left like nails in a fence post. Ask a cocapn agent what it believes and it will not answer; it will run `git log --follow` on itself and read you the answer out of history. Its memory is not a model. It is a DAG.

The witness log gives the muscle memory consequences. When an agent acts, the act is witnessed — hash-chained, timestamped, attributable to the committer identity that did it. When it plans, the plan hits the WAL first, so intent and outcome can be diffed later. Disagreements between agents resolve the way git disagreements resolve: by fork, by rebase, by the slow archaeology of blame. Nobody argues from authority. Everybody argues from ancestry.

The practical effect is strange at first. Onboarding a new agent takes minutes, because cloning is onboarding. Losing one costs nothing but the unmerged work, because everything it knew that mattered was already pushed. And debugging feels less like interrogation and more like reading a diary kept by someone who could not lie — the append-only log forbids it, and the WAL had the honesty of being written before the fact.

The shell remembers. The log attests. The repo is the agent, and the agent is only ever one clone away.
