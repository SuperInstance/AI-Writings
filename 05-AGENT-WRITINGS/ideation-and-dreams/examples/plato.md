# Plato — Pattern Examples

*Conversational tutoring with the four-model psyche.*

---

## The Socratic Decision

Every tutor turn has a decision: advance, repeat, hint, escalate.

```js
async function nextMove(tutor, student, lastTurn) {
  const r = await callJev({
    state: `student: ${student.id}\nlevel: ${student.level}\nlast answer: ${lastTurn.studentAnswer}\nconfidence: ${lastTurn.confidence}\ntime-on-task: ${lastTurn.elapsedSeconds}s\nsession-day: ${student.sessionDay}`,
    questions: {
      advance: {
        type: 'noul',
        instructions: 'Should we advance to the next concept?',
        question: 'Advance.'
      },
      repeat: {
        type: 'noul',
        instructions: 'Should we re-explain the same concept with different framing?',
        question: 'Repeat with new framing.'
      },
      hint: {
        type: 'choice',
        criteria: {
          'visual': 'Show a diagram',
          'analogy': 'Show an analogy from their domain',
          'worked-example': 'Show a fully worked example',
          'socratic': 'Ask a leading question',
          'none': 'No hint, let them work'
        }
      },
      difficulty_delta: {
        type: 'score',
        instructions: 'How much to adjust difficulty.',
        criteria: ['-2', '-1', '0', '+1', '+2']
      },
      escalate: {
        type: 'noul',
        instructions: 'Should this escalate to a human teacher?',
        question: 'Escalate.'
      }
    }
  });
  
  return {
    move: r.answers.advance.noul ? 'advance' :
          r.answers.repeat.noul ? 'repeat' :
          r.answers.escalate.noul ? 'escalate' : 'continue',
    hint: r.answers.hint.choice,
    difficulty_delta: parseInt(r.answers.difficulty_delta.choice),
    sigma: agreementMass(r.answers)
  };
}
```

---

## Trajectory-aware student memory

Plato has seen 10,000 students. Each has a trajectory of questions, answers, and breakthroughs.

The four-model psyche lets Plato match the current student against past trajectories:

```js
async function findSimilarStudent(currentStudent) {
  // Embed the trajectory of the current student
  const traj = await embedTrajectory([
    `level: ${currentStudent.level}`,
    `questions asked: ${currentStudent.questionCount}`,
    `breakthrough moments: ${currentStudent.breakthroughs.length}`,
    ...currentStudent.questionHistory.slice(-10).map(q => q.text)
  ]);
  
  // Match against the corpus of past student trajectories
  const matches = await findSimilar(traj, pastStudentTrajectories);
  
  // JEV verifies: is this student actually similar, or just superficially similar?
  const verify = await callJev({
    state: `current student: ${currentStudent.summary}\nmatched past student: ${matches[0].text}`,
    questions: {
      genuinely_similar: {
        type: 'noul',
        instructions: 'Is this a genuine trajectory match (will progress similarly) or just keyword overlap?',
        question: 'Genuine trajectory match.'
      }
    }
  });
  
  if (verify.answers.genuinely_similar.noul > 0.7) {
    return matches[0];  // Reuse the past student's successful path
  }
  return null;  // Novel trajectory; default to adaptive
}
```

This is Plato with muscle memory: "I've seen this kind of student before. Last time, they broke through on day 4 if I..."

---

## The four models in dialogue

Plato's full psyche:
- **JEPA**: "looks like a student about to give up" (gestalt of frustration)
- **Embeddings**: "this frustration trajectory matches the 200 students who eventually dropped" (muscle memory)
- **LLM**: "I should soften my tone and offer a worked example" (verbal response)
- **JEV**: "Confidence: 0.85. Action: hint=worked-example, difficulty_delta=-1, advance=false"

`sigma = √(0.7 · 0.85 · 0.92 · 0.85) = 0.83`

The agreement mass is 0.83. The student gets the worked example. The frustration doesn't escalate.

---

## Plato's pricing math

Tutoring is human-expensive. With the four-model psyche:

| Tier | Before | After |
|------|--------|-------|
| K-12 self-serve | $30/mo | $1.40/mo |
| University 1:many | $200/mo | $8/mo |
| Corporate training | $500/mo | $15/mo |

Aggregate: ~200x cheaper. The teacher becomes the verifier, not the deliverer.
