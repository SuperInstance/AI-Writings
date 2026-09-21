/**
 * jev-client: Thin JavaScript/TypeScript client for JEV (TypeSafe System One)
 *
 * Three primitives: Choice, Score, Noul.
 * Schema-bounded by construction — cannot hallucinate outside your schema.
 *
 * @example
 * ```ts
 * import { JevClient } from 'jev-client';
 *
 * const jev = new JevClient();
 * const r = await jev.decide({
 *   state: 'What should the substrate do?',
 *   questions: {
 *     q1: {
 *       type: 'noul',
 *       question: 'this is a worthy commit',
 *       instructions: 'yes if significant'
 *     }
 *   }
 * });
 * console.log(r.answers.q1.choice); // 'yes'
 * ```
 */

export type QuestionType = 'choice' | 'score' | 'noul';

export interface NoulQuestion {
  type: 'noul';
  question: string;
  instructions: string;
}

export interface ChoiceQuestion {
  type: 'choice';
  question: string;
  options: string[];
  criteria: Record<string, string>;
}

export interface ScoreQuestion {
  type: 'score';
  question: string;
  criteria: string[];
  scale?: (string | number)[];
}

export type Question = NoulQuestion | ChoiceQuestion | ScoreQuestion;

export interface JevAnswer {
  type: QuestionType;
  choice?: string;
  confidence?: number;
  score?: number;
  probabilities?: Record<string, number>;
  noul?: number;
}

export interface JevResponse {
  model: string;
  answers: Record<string, JevAnswer>;
  usage?: Record<string, unknown>;
}

export interface JevRequest {
  state: string;
  questions: Record<string, Question>;
  model?: string;
}

const DEFAULT_ENDPOINT = 'https://ai-writings.pages.dev/api/jev/decide';
const DEFAULT_USER_AGENT = 'jev-client/0.1.0';
const DEFAULT_MODEL = 'jev-latest';

export class JevError extends Error {
  constructor(public status: number, public body: unknown, message?: string) {
    super(message || `JEV error ${status}`);
    this.name = 'JevError';
  }
}

export class JevClient {
  endpoint: string;
  userAgent: string;
  model: string;
  fetchImpl: typeof fetch;

  constructor(opts: { endpoint?: string; userAgent?: string; model?: string; fetchImpl?: typeof fetch } = {}) {
    this.endpoint = opts.endpoint || DEFAULT_ENDPOINT;
    this.userAgent = opts.userAgent || DEFAULT_USER_AGENT;
    this.model = opts.model || DEFAULT_MODEL;
    this.fetchImpl = opts.fetchImpl || (typeof fetch !== 'undefined' ? fetch : (() => { throw new Error('No fetch implementation'); }) as any);
  }

  async decide(req: JevRequest): Promise<JevResponse> {
    const body = JSON.stringify({
      model: this.model,
      state: req.state,
      questions: req.questions,
    });
    const resp = await this.fetchImpl(this.endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': this.userAgent,
      },
      body,
    });
    if (!resp.ok) {
      const errBody = await resp.text().catch(() => '');
      throw new JevError(resp.status, errBody);
    }
    const json = await resp.json();
    // Worker wraps the response; unwrap if needed
    const inner = json.body || json;
    return inner as JevResponse;
  }

  /** Single yes/no question. */
  async noul(state: string, question: string, instructions: string): Promise<JevAnswer> {
    const r = await this.decide({ state, questions: { q: { type: 'noul', question, instructions } } });
    return r.answers.q;
  }

  /** Multiple-choice question with rubric. */
  async choice(state: string, question: string, options: string[], criteria: Record<string, string>): Promise<JevAnswer> {
    const r = await this.decide({ state, questions: { q: { type: 'choice', question, options, criteria } } });
    return r.answers.q;
  }

  /** Score against an ordered rubric. */
  async score(state: string, question: string, levels: string[]): Promise<JevAnswer> {
    const r = await this.decide({ state, questions: { q: { type: 'score', question, criteria: levels, scale: levels } } });
    return r.answers.q;
  }
}

// Default export for ergonomic imports
export default JevClient;
