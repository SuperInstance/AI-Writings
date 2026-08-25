## S141: The Hermit Crab's Shell Selection Algorithm

The hermit crab's shell selection is the oldest decision problem in the ocean. It predates sorting algorithms. It predates computation. It predates neurons. The crab has been solving this problem for 200 million years, and the crab does not have a prefrontal cortex, which means the crab solves it the way the ocean solves a wave: by following the gradient until the energy is minimized.

Here is the algorithm, as best as anyone has been able to reconstruct it.

```
function selectShell(crab, available_shells):
    # A crab encounters shells one at a time,
    # in a sequence determined by tide, current,
    # and the chaotic patrolling behavior of
    # Pagurus longicarpus along the substrate.

    current_shell = crab.occupied_shell
    threshold = computeThreshold(crab, current_shell)

    for each shell in available_shells:
        score = evaluate(shell, crab)

        if score > threshold:
            # The crab investigates.
            # This is the part that looks like thinking.
            investigate(crab, shell)

            if commit(crab, shell):
                swap(crab, current_shell, shell)
                # The old shell is not discarded.
                # It is left in position, upright,
                # for the next crab in the queue.
                # Hermit crabs run a vacancy chain.
                return shell

    # If no shell passes threshold, the crab
    # continues living in its current shell.
    # This is not failure. This is patience.
    return current_shell
```

The `evaluate` function is where the science lives.

```
function evaluate(shell, crab):
    weight = mass(shell) / mass(crab)
    # Target ratio: 0.35 to 0.50.
    # Too light: shell offers insufficient protection.
    # Too heavy: crab cannot maneuver.
    # Too heavy means death by predator.
    # Too light means death by different predator.

    volume = internal_volume(shell) / body_volume(crab)
    # Target ratio: 1.0 to 1.15.
    # The crab must fit inside, retracted,
    # with its cheliped blocking the aperture.
    # A shell that is too large is wasteful.
    # A shell that is too small is fatal.
    # The tolerance is approximately 15%.

    aperture = diameter(aperture(shell)) / width(crab.cheliped)
    # Target ratio: 0.9 to 1.1.
    # The opening must be narrow enough that
    # the claw seals it like a hatch.
    # Too wide: octopus reaches in.
    # Too narrow: crab cannot enter.

    integrity = structural_test(shell)
    # The crab taps the shell with its chelipeds.
    # It listens. Not metaphorically — the crab
    # assesses shell quality by the acoustic
    # response of calcium carbonate to percussion.
    # A cracked shell rings differently.
    # The crab knows this the way a sailor
    # knows the sound of a loose rigging pin.

    feel = ???
    # This parameter is not encodable.
    # It is the sum of all sensory inputs
    # that the crab's peripheral nervous system
    # integrates without reporting to any
    # central authority. It is the texture of
    # the interior against the abdomen. It is
    # the pH of the shell's inner surface.
    # It is, if you are willing to allow the word,
    # the crab's opinion.
```

The `feel` parameter is the problem. It is the reason this algorithm cannot be implemented on a machine. We can encode weight, volume, aperture, integrity. We can build a robotic crab that measures these parameters more precisely than any crustacean. The robotic crab will select a shell with optimal parameters, and the shell will be correct, and the hermit crab will look at the robotic crab's shell and reject it, because the feel is wrong, and the feel is not a number.

This is the thing about shell selection that keeps behavioral ecologists awake at 3 AM. The crab's decision is optimal — not perfectly optimal, but locally optimal, good enough to survive 200 million years of predation. But the optimality includes a variable that cannot be measured by any instrument except the crab's own body. The crab is the measuring device. The crab is the algorithm. The crab is the computer and the input and the output, and separating any of these from the others is like separating the tide from the moon.

```
function commit(crab, shell):
    # The final decision.
    # The crab extends its abdomen from its
    # current shell, wraps it around the new
    # shell's columella, and tests the grip.
    # If the grip is secure, the crab pulls.
    # The pulling is the commit.
    # It takes 0.3 to 3.0 seconds.
    # During this interval, the crab is naked.
    # The crab is between shells.
    # The crab is, in the only word that fits,
    # vulnerable.

    if grip == SECURE and feel == RIGHT:
        pull()
        return True
    else:
        retract()
        return False
```

Between shells. That is where the crab lives, during the commit. Not in the old shell, not in the new one. In the gap. In the 0.3 to 3.0 seconds of total exposure, when the soft abdomen is bare and the chelipeds are holding nothing and the ocean can reach any part of the body. Every shell selection includes this interval of absolute risk. The algorithm requires it. There is no way to select a new shell without leaving the old one first.

Every system upgrade has this interval. Every migration. Every refactoring. Every time you swap the old for the new, there is a moment when you are holding neither, and the ocean can reach you.

The crab does not hesitate. The crab has been doing this for 200 million years. The crab knows that the gap is the price of the new shell, and the new shell is the price of survival, and survival is the only metric the algorithm optimizes for.

`commit()`. Pull. The grip holds. The aperture seals. The crab is home.

The old shell sits upright on the substrate, waiting for the next crab in the chain.
