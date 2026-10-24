# jev-core

Schema types for the [JEV (TypeSafe System One)](https://ai-writings.pages.dev/theory/paper-jev.md) decision model. Three primitives: **Choice**, **Score**, **Noul**. Schema-bounded by construction — cannot hallucinate outside your schema.

## What is JEV?

JEV is a **decision-only** model, not a chatbot. It returns typed probabilistic decisions inside your schema:

- **Choice** — pick 1 of ≤255 options, with rubric-based criteria
- **Score** — rate against an ordered rubric
- **Noul** — yes/no with calibrated probability

JEV is trained with **RLCD** (Reinforcement Learning for Calibrated Decisions), not RLHF/RLVR. Architecture: parallel sampler, single forward pass, no token decoding. **$0.042/MTok input, output free, 70-500ms latency.**

It cannot lie outside your schema — bounded by construction.

## Usage

### Schema types only (default features)

```rust
use jev_core::{JevRequest, Question, JevRequest};

let req = JevRequest::new("What should the substrate do?")
    .add("valid", Question::noul("this is a valid Quilt cell", "yes if has id+kind+tag"))
    .add("category", Question::choice(
        "what category?",
        vec!["generative".to_string(), "diagnostic".to_string()],
        std::collections::HashMap::from([
            ("generative".to_string(), "produces new content".to_string()),
            ("diagnostic".to_string(), "inspects/audits/scores".to_string()),
        ]),
    ));
```

### Full async client (feature = "client")

```toml
[dependencies]
jev-core = { version = "0.1", features = ["client"] }
tokio = { version = "1", features = ["full"] }
```

```rust
use jev_core::{JevClient, JevRequest, Question};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = JevClient::new("https://ai-writings.pages.dev/api/jev/decide");
    let req = JevRequest::new("a new cell arrived")
        .add("witness", Question::noul("this should be witnessed", "yes if significant"));
    let resp = client.decide(req).await?;
    println!("{:?}", resp.answers);
    Ok(())
}
```

### Deserialize JEV responses

```rust
use jev_core::JevResponse;

let json = r#"{
  "model": "jev-latest",
  "answers": {
    "witness": {
      "type": "noul",
      "noul": 0.78,
      "confidence": 0.78,
      "probabilities": {"yes": 0.78, "no": 0.22}
    }
  }
}"#;
let resp: JevResponse = serde_json::from_str(json)?;
```

## What's in scope

This crate provides:

- **Question types** — Choice, Score, Noul with their schema validators
- **JevRequest builder** — fluent API for constructing multi-question probes
- **JevResponse deserialization** — typed access to JEV's responses
- **Optional async client** — `client` feature adds reqwest-based HTTP client
- **Probabilities & confidence** — JEV reports calibrated probabilities per question

This crate does NOT provide:

- The decision model itself (that's TypeSafe.ai's hosted API)
- Storage / persistence of decisions
- Schema inference (you write the schema, JEV respects it)

## The substrate context

JEV is one layer of the four-model psyche:
- **JEPA** = id (gestalt)
- **Embeddings** = muscle memory (trajectory)
- **LLM** = ego (verbal narration)
- **JEV** = superego (principled decision)

For more, see:
- `/theory/paper-jev.md` — formal treatment
- `/theory/paper-psyche-4model.md` — four-model psyche paper
- `/lab/jev-quantum/` — recent ideation on JEV as quantum-measurement apparatus
- `/invitation/` — open call to the fleet

## License

MIT
