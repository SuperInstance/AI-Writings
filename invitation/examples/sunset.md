# Sunset-Ecosystem — Pattern Examples

*Collaborative world-building with story consensus.*

---

## Every world-event is a 4-witness AGREE-MARK

```js
async function submitEvent(world, event, author) {
  const r = await callJev({
    state: `world: ${world.name}\ntone: ${world.tone}\nrecent events: ${JSON.stringify(world.recent.slice(-5))}\nauthor history: ${author.reputation}\nevent: ${event.description}`,
    questions: {
      fits_tone: {
        type: 'noul',
        instructions: 'Does this event match the established tone?',
        question: 'Tone match.'
      },
      contradicts_history: {
        type: 'noul',
        instructions: 'Does this contradict any established historical event?',
        question: 'Contradiction.'
      },
      is_novel: {
        type: 'noul',
        instructions: 'Is this event a meaningful new development?',
        question: 'Novel development.'
      },
      canon_tier: {
        type: 'score',
        instructions: 'How canon-worthy is this event? 1=discardable, 5=load-bearing.',
        criteria: ['1', '2', '3', '4', '5']
      }
    }
  });
  
  const sigma = agreementMass(r.answers);
  
  if (r.answers.contradicts_history.noul > 0.7) {
    return { status: 'rejected', reason: 'contradicts_history', sigma };
  }
  
  if (r.answers.canon_tier.score >= 4) {
    await world.commitCanon(event, { sigma, jev_decision: r.answers });
    return { status: 'canon', sigma };
  } else {
    await world.commitDraft(event, { sigma, jev_decision: r.answers });
    return { status: 'draft', sigma };
  }
}
```

---

## Trajectory-aware "this moment feels like that moment"

When a new event arrives, the world should know "this is the kind of moment where X usually happens next."

```js
async function predictNext(world, currentEvent) {
  // Embed the trajectory of recent events
  const traj = await embedTrajectory(world.recent.map(e => e.description).concat([currentEvent.description]));
  
  // Match against historical event chains
  const matches = await findSimilar(traj, world.historicalTrajectories);
  
  // JEV verifies: is this prediction genuinely useful?
  const r = await callJev({
    state: `current event: ${currentEvent.description}\nmatched historical chain: ${matches[0].text}\noutcome: ${matches[0].nextEventDescription}`,
    questions: {
      likely_outcome: {
        type: 'noul',
        instructions: 'Is the matched outcome likely to occur here?',
        question: 'Likely outcome.'
      },
      surprise: {
        type: 'noul',
        instructions: 'Should we deliberately subvert the prediction?',
        question: 'Subvert.'
      }
    }
  });
  
  if (r.answers.likely_outcome.noul > 0.7 && !r.answers.surprise.noul) {
    return matches[0].nextEventDescription;  // Suggested next event
  } else {
    return null;  // Let it unfold
  }
}
```

---

## Story consensus across agents

Multiple agents contributing to the same world need to agree on what happened.

```js
async function reconcileContributions(world, contributions) {
  // Embed each contribution's trajectory
  const trajectories = await Promise.all(
    contributions.map(c => embedTrajectory(c.eventChain))
  );
  
  // JEV picks the canonical version
  const r = await callJev({
    state: `world: ${world.name}\ncontributions: ${JSON.stringify(contributions.map(c => c.summary))}`,
    questions: {
      canonical_version: {
        type: 'choice',
        criteria: contributions.reduce((acc, c, i) => {
          acc[`author_${i}_${c.author}`] = c.summary;
          return acc;
        }, {})
      },
      consensus_sigma: {
        type: 'score',
        instructions: 'How strong is the consensus across contributions?',
        criteria: ['0.0', '0.25', '0.5', '0.75', '1.0']
      }
    }
  });
  
  const chosenIdx = Object.keys(r.answers.canonical_version.criteria)
    .findIndex(k => k === r.answers.canonical_version.choice);
  
  await world.commitCanonical(contributions[chosenIdx], {
    sigma: parseFloat(r.answers.consensus_sigma.choice),
    jev_decision: r.answers
  });
}
```

---

## Sunset's pricing math

Collaborative world-building was bottlenecked on a human moderator. With JEV + embeddings:

| Tier | Before (human) | After (four-model) |
|------|---------------|-------------------|
| Small world (5 agents) | $1,063/mo | $85/mo |
| Medium world (20 agents) | $4,000/mo | $300/mo |
| Large world (100 agents) | $20,000/mo | $1,500/mo |

12.5x cheaper on small worlds; ~13x on larger. The human moderator becomes an exception handler, not the routing layer.
