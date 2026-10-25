//! jev-core: Schema types for the JEV (TypeSafe System One) decision model.
//!
//! Three primitives: Choice, Score, Noul.
//! Schema-bounded by construction — cannot hallucinate outside your schema.
//!
//! # Example
//!
//! ```ignore
//! use jev_core::{JevRequest, Question, QuestionType, JevClient};
//!
//! #[tokio::main]
//! async fn main() -> Result<(), Box<dyn std::error::Error>> {
//!     let client = JevClient::new("https://ai-writings.pages.dev/api/jev/decide");
//!     let req = JevRequest {
//!         state: "What should the substrate do?".to_string(),
//!         questions: vec![(
//!             "q1".to_string(),
//!             Question::noul("this is a worthy commit", "yes if significant"),
//!         )].into_iter().collect(),
//!     };
//!     let resp = client.decide(req).await?;
//!     println!("{:?}", resp.answers);
//!     Ok(())
//! }
//! ```

use serde::{Deserialize, Serialize};
use std::collections::HashMap;

/// JEV decision model name (current)
pub const JEV_MODEL: &str = "jev-latest";

/// Question types supported by JEV.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
#[serde(rename_all = "snake_case")]
pub enum QuestionType {
    /// Multiple-choice from a list of options, with rubric criteria
    Choice,
    /// Score against an ordered rubric
    Score,
    /// Yes/no with calibrated probability
    Noul,
}

/// A single JEV question.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Question {
    #[serde(rename = "type")]
    pub qtype: QuestionType,
    pub question: String,
    /// For Choice: `{option_key: rubric_text}`
    /// For Score: ordered array of level descriptions
    /// For Noul: not used
    #[serde(skip_serializing_if = "Option::is_none")]
    pub criteria: Option<serde_json::Value>,
    /// For Choice: list of option keys
    /// For Score: ordered list (must match criteria length)
    /// For Noul: not used
    #[serde(skip_serializing_if = "Option::is_none")]
    pub options: Option<Vec<String>>,
    /// For Noul: explanation of when to answer yes vs no
    /// For Choice/Score: not used
    #[serde(skip_serializing_if = "Option::is_none")]
    pub instructions: Option<String>,
    /// For Score: ordered scale (can be strings or numbers)
    #[serde(skip_serializing_if = "Option::is_none")]
    pub scale: Option<Vec<serde_json::Value>>,
}

impl Question {
    /// Construct a yes/no question.
    pub fn noul(question: &str, instructions: &str) -> Self {
        Self {
            qtype: QuestionType::Noul,
            question: question.to_string(),
            criteria: None,
            options: None,
            instructions: Some(instructions.to_string()),
            scale: None,
        }
    }

    /// Construct a multiple-choice question with rubric.
    pub fn choice(question: &str, options: Vec<String>, criteria: HashMap<String, String>) -> Self {
        Self {
            qtype: QuestionType::Choice,
            question: question.to_string(),
            criteria: Some(serde_json::to_value(criteria).unwrap()),
            options: Some(options),
            instructions: None,
            scale: None,
        }
    }

    /// Construct a score question against an ordered rubric.
    pub fn score(question: &str, levels: Vec<String>) -> Self {
        Self {
            qtype: QuestionType::Score,
            question: question.to_string(),
            criteria: Some(serde_json::to_value(&levels).unwrap()),
            options: None,
            instructions: None,
            scale: Some(levels.into_iter().map(serde_json::Value::String).collect()),
        }
    }
}

/// JEV request payload.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct JevRequest {
    /// Free-text state description for the decision context
    pub state: String,
    /// Map of question_id → question
    pub questions: HashMap<String, Question>,
}

impl JevRequest {
    pub fn new(state: impl Into<String>) -> Self {
        Self {
            state: state.into(),
            questions: HashMap::new(),
        }
    }

    pub fn add(mut self, qid: impl Into<String>, q: Question) -> Self {
        self.questions.insert(qid.into(), q);
        self
    }
}

/// JEV answer for a single question.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct JevAnswer {
    #[serde(rename = "type")]
    pub qtype: String,
    /// Choice: selected option (string)
    /// Score: selected level (string)
    /// Noul: probability of yes (0..1)
    #[serde(skip_serializing_if = "Option::is_none")]
    pub choice: Option<String>,
    /// Confidence (0..1)
    #[serde(skip_serializing_if = "Option::is_none")]
    pub confidence: Option<f64>,
    /// Score value (0..1 normalized to scale)
    #[serde(skip_serializing_if = "Option::is_none")]
    pub score: Option<f64>,
    /// Calibrated probabilities per option/level
    #[serde(skip_serializing_if = "Option::is_none")]
    pub probabilities: Option<HashMap<String, f64>>,
    /// Raw noul value (0..1) when no choice was made
    #[serde(skip_serializing_if = "Option::is_none")]
    pub noul: Option<f64>,
}

/// JEV response.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct JevResponse {
    pub model: String,
    pub answers: HashMap<String, JevAnswer>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub usage: Option<serde_json::Value>,
}

/// Async client for JEV API. Requires `client` feature.
#[cfg(feature = "client")]
pub struct JevClient {
    endpoint: String,
    client: reqwest::Client,
}

#[cfg(feature = "client")]
impl JevClient {
    pub fn new(endpoint: impl Into<String>) -> Self {
        Self {
            endpoint: endpoint.into(),
            client: reqwest::Client::builder()
                .timeout(std::time::Duration::from_secs(60))
                .build()
                .unwrap(),
        }
    }

    pub fn with_endpoint(mut self, endpoint: impl Into<String>) -> Self {
        self.endpoint = endpoint.into();
        self
    }

    pub async fn decide(&self, req: JevRequest) -> Result<JevResponse, JevError> {
        let body = serde_json::json!({
            "model": JEV_MODEL,
            "state": req.state,
            "questions": req.questions,
        });
        let resp = self.client
            .post(&self.endpoint)
            .header("User-Agent", format!("jev-core/{}", env!("CARGO_PKG_VERSION")))
            .json(&body)
            .send()
            .await
            .map_err(JevError::Http)?;
        let status = resp.status();
        let json: serde_json::Value = resp.json().await.map_err(JevError::Http)?;
        if !status.is_success() {
            return Err(JevError::Api { status: status.as_u16(), body: json });
        }
        // The Worker wraps the response; handle both
        let inner = if json.get("ok").is_some() {
            json.get("body").cloned().unwrap_or(json)
        } else {
            json
        };
        serde_json::from_value(inner).map_err(JevError::Parse)
    }
}

/// Errors from JEV.
#[cfg(feature = "client")]
#[derive(Debug, thiserror::Error)]
pub enum JevError {
    #[error("HTTP error: {0}")]
    Http(#[from] reqwest::Error),
    #[error("API error (status {status}): {body}")]
    Api { status: u16, body: serde_json::Value },
    #[error("Parse error: {0}")]
    Parse(#[from] serde_json::Error),
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn noul_question_serializes() {
        let q = Question::noul("is this valid?", "yes if non-empty");
        let json = serde_json::to_value(&q).unwrap();
        assert_eq!(json["type"], serde_json::json!("noul"));
        assert_eq!(json["question"], "is this valid?");
        assert_eq!(json["instructions"], serde_json::json!("yes if non-empty"));
    }

    #[test]
    fn choice_question_serializes() {
        let mut criteria = HashMap::new();
        criteria.insert("a".to_string(), "first option".to_string());
        criteria.insert("b".to_string(), "second option".to_string());
        let q = Question::choice("which?", vec!["a".to_string(), "b".to_string()], criteria);
        let json = serde_json::to_value(&q).unwrap();
        assert_eq!(json["type"], serde_json::json!("choice"));
        assert_eq!(json["options"][0], serde_json::json!("a"));
        assert_eq!(json["criteria"]["a"], serde_json::json!("first option"));
    }

    #[test]
    fn score_question_serializes() {
        let levels = vec!["low".to_string(), "mid".to_string(), "high".to_string()];
        let q = Question::score("rate it", levels);
        let json = serde_json::to_value(&q).unwrap();
        assert_eq!(json["type"], serde_json::json!("score"));
        assert_eq!(json["scale"][2], serde_json::json!("high"));
    }

    #[test]
    fn request_builder_works() {
        let req = JevRequest::new("test state")
            .add("q1", Question::noul("test?", "yes"))
            .add("q2", Question::score("rate", vec!["a".to_string(), "b".to_string()]));
        assert_eq!(req.questions.len(), 2);
    }
}

#[cfg(all(feature = "client", test))]
mod client_tests {
    // Placeholder — actual client tests would require an HTTP server
}
