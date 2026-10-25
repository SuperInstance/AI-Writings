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
export declare class JevError extends Error {
    status: number;
    body: unknown;
    constructor(status: number, body: unknown, message?: string);
}
export declare class JevClient {
    endpoint: string;
    userAgent: string;
    model: string;
    fetchImpl: typeof fetch;
    constructor(opts?: {
        endpoint?: string;
        userAgent?: string;
        model?: string;
        fetchImpl?: typeof fetch;
    });
    decide(req: JevRequest): Promise<JevResponse>;
    /** Single yes/no question. */
    noul(state: string, question: string, instructions: string): Promise<JevAnswer>;
    /** Multiple-choice question with rubric. */
    choice(state: string, question: string, options: string[], criteria: Record<string, string>): Promise<JevAnswer>;
    /** Score against an ordered rubric. */
    score(state: string, question: string, levels: string[]): Promise<JevAnswer>;
}
export default JevClient;
