"use strict";
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
Object.defineProperty(exports, "__esModule", { value: true });
exports.JevClient = exports.JevError = void 0;
const DEFAULT_ENDPOINT = 'https://ai-writings.pages.dev/api/jev/decide';
const DEFAULT_USER_AGENT = 'jev-client/0.1.0';
const DEFAULT_MODEL = 'jev-latest';
class JevError extends Error {
    constructor(status, body, message) {
        super(message || `JEV error ${status}`);
        this.status = status;
        this.body = body;
        this.name = 'JevError';
    }
}
exports.JevError = JevError;
class JevClient {
    constructor(opts = {}) {
        this.endpoint = opts.endpoint || DEFAULT_ENDPOINT;
        this.userAgent = opts.userAgent || DEFAULT_USER_AGENT;
        this.model = opts.model || DEFAULT_MODEL;
        this.fetchImpl = opts.fetchImpl || (typeof fetch !== 'undefined' ? fetch : (() => { throw new Error('No fetch implementation'); }));
    }
    async decide(req) {
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
        return inner;
    }
    /** Single yes/no question. */
    async noul(state, question, instructions) {
        const r = await this.decide({ state, questions: { q: { type: 'noul', question, instructions } } });
        return r.answers.q;
    }
    /** Multiple-choice question with rubric. */
    async choice(state, question, options, criteria) {
        const r = await this.decide({ state, questions: { q: { type: 'choice', question, options, criteria } } });
        return r.answers.q;
    }
    /** Score against an ordered rubric. */
    async score(state, question, levels) {
        const r = await this.decide({ state, questions: { q: { type: 'score', question, criteria: levels, scale: levels } } });
        return r.answers.q;
    }
}
exports.JevClient = JevClient;
// Default export for ergonomic imports
exports.default = JevClient;
