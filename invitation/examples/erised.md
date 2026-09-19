# Erised — Pattern Examples

*Want and desire as trajectories.*

---

## A want is a trajectory

Erised has been modeling what agents want. The four-model psyche reframes: a want is the dμ of an agent's history.

```js
async function getWant(agent) {
  // Embed the trajectory of the agent's recent decisions
  const traj = await embedTrajectory(agent.decisionHistory.slice(-20).map(d => d.summary));
  
  // The trajectory IS the want. The dμ of where the agent has been heading.
  return {
    type: 'want',
    trajectory: traj,
    summary: describeTrajectory(traj),  // LLM narrates what the trajectory points to
    strength: jepaStrength(agent, traj)  // JEPA: "looks like a strong want"
  };
}
```

---

## Want satisfaction as a JEV decision

```js
async function checkSatisfaction(agent, event, currentWant) {
  const r = await callJev({
    state: `agent: ${agent.name}\ncurrent want: ${currentWant.summary}\nevent: ${event.description}\nagent state before: ${JSON.stringify(agent.stateBefore).slice(0, 200)}\nagent state after: ${JSON.stringify(agent.stateAfter).slice(0, 200)}`,
    questions: {
      want_satisfied: {
        type: 'noul',
        instructions: 'Did this event satisfy the current want?',
        question: 'Satisfied.'
      },
      want_intensified: {
        type: 'noul',
        instructions: 'Did this event intensify the want (now wanting more)?',
        question: 'Intensified.'
      },
      want_changed: {
        type: 'noul',
        instructions: 'Did this event shift the want to something different?',
        question: 'Changed.'
      },
      new_want: {
        type: 'choice',
        criteria: {
          // catalog of possible wants
          'safety': 'Safety / security',
          'connection': 'Connection / relationship',
          'mastery': 'Mastery / competence',
          'autonomy': 'Autonomy / agency',
          'meaning': 'Meaning / purpose',
          'novelty': 'Novelty / surprise'
        }
      }
    }
  });
  
  return {
    status: r.answers.want_changed.noul ? 'changed' :
            r.answers.want_satisfied.noul ? 'satisfied' :
            r.answers.want_intensified.noul ? 'intensified' : 'unchanged',
    newWant: r.answers.want_changed.noul ? r.answers.new_want.choice : null,
    sigma: agreementMass(r.answers)
  };
}
```

---

## The want-history as muscle memory

What an agent has wanted in the past is the trajectory of its wants. Embed that.

```js
async function recallSimilarWant(agent, currentEvent) {
  const eventEmbedding = await embedText(currentEvent.description);
  
  // Match against past events-that-satisfied-wants
  const matches = await findSimilar(eventEmbedding, agent.satisfyingEvents);
  
  // JEV: is this match genuinely similar?
  const r = await callJev({
    state: `current event: ${currentEvent.description}\nmatched past event: ${matches[0]?.event.description}\nwant satisfied: ${matches[0]?.want.summary}`,
    questions: {
      want_predicted: {
        type: 'noul',
        instructions: 'Does the current event suggest the same want as the matched past event?',
        question: 'Same want.'
      }
    }
  });
  
  if (r.answers.want_predicted.noul > 0.7) {
    return {
      predictedWant: matches[0].want,
      basedOn: matches[0].event.id,
      confidence: r.answers.want_predicted.confidence
    };
  }
  return null;
}
```

---

## Why this matters for Erised

Want has always been hard to model because it changes. The four-model psyche doesn't model the want as a fixed thing — it models the want as a *trajectory*.

The agent's want is the dμ of its recent decisions. The want shifts when the trajectory shifts. Want is computed, not stored.

This is the dμ of desire. The tangent, not the point.
