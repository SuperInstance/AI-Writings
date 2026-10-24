# The Pragmatics of Error Messages

*How the most ignored branch of linguistics explains why your compiler talks to you like a pedantic robot, and how it could talk to you like a colleague*

---

## 1. The Message That Means Nothing and Everything

```
error[E0308]: mismatched types
 --> src/main.rs:3:5
  |
3 |     x: "hello"
  |     ^^^^^^^^^^ expected `i32`, found `&str`
```

To a Rust beginner, this error message is a wall of hieroglyphs. What is `E0308`? What is `src/main.rs:3:5`? What does "expected `i32`, found `&str`" even mean? The beginner stares at it, then at their code, then back at the error, and the gap between what the compiler is saying and what the beginner understands is a canyon.

To a Rust expert, this error message is a precise diagnostic. The type mismatch is at line 3, column 5. The declared type is `i32`, the provided value is `&str`. The fix is obvious: either change the type annotation or change the value. The expert reads the error and immediately knows what to do.

Same message. Two readers. Two completely different meanings. The meaning of the error message depends not on the message alone, but on the reader, the context, and the shared knowledge between them. This is *pragmatics* — the branch of linguistics that studies how context contributes to meaning. And it is the blind spot of every compiler ever built.

---

## 2. Syntax, Semantics, Pragmatics: The Three Layers of Meaning

Charles Morris, building on Charles Sanders Peirce's semiotics, divided the study of signs into three branches (1938):

- **Syntax:** The formal relationship between signs. How words combine into sentences. In compilers: parsing, grammar, the rules of well-formedness.
- **Semantics:** The relationship between signs and their referents. What words mean. In compilers: type checking, the rules of well-typedness.
- **Pragmatics:** The relationship between signs and their users. How context affects meaning. In compilers: error messages, documentation, the user experience.

Compilers are extraordinarily good at syntax and semantics. Decades of research have produced parsers that handle ambiguity gracefully, type systems that catch deep errors, and optimization passes that rival human craftsmanship. But compilers are terrible at pragmatics. They produce error messages that are syntactically precise and semantically accurate but pragmatically catastrophic — messages that say the right thing to the wrong person in the wrong way.

The reason is structural. Syntax and semantics are formal properties of the language. They can be specified precisely, implemented algorithmically, and tested exhaustively. Pragmatics is *situated* — it depends on who is reading the message, what they already know, what they're trying to do, and what they need to hear next. You cannot specify pragmatics in a language standard. You cannot test it with unit tests. You can only evaluate it by putting it in front of real humans with real problems and seeing whether they understand.

This is why error message design is the hardest problem in compiler construction. Not because the messages are technically difficult to produce — they are trivially generated during type checking and parsing. But because the messages must bridge the gap between the compiler's formal knowledge and the programmer's situated understanding. This gap is the pragmatic gap, and it is where most compilers fail.

---

## 3. Grice's Cooperative Principle and the Compiler

H.P. Grice's cooperative principle (1967, published 1989) states: "Make your conversational contribution such as is required, at the stage at which it occurs, by the accepted purpose or direction of the talk exchange in which you are engaged." The principle is undergirded by four maxims:

**Maxim of Quantity:** Make your contribution as informative as is required. Not more, not less.

**Maxim of Quality:** Try to make your contribution one that is true. Do not say what you believe to be false. Do not say that for which you lack adequate evidence.

**Maxim of Relation:** Be relevant.

**Maxim of Manner:** Be perspicuous. Avoid obscurity and ambiguity. Be brief and orderly.

Let us evaluate a typical compiler error message against these maxims.

```
error: expected `Vec<i32>`, found `i32`
```

**Quantity:** Is this as informative as required? It tells us the expected type and the found type. It does not tell us *why* the type was expected, *where* the expectation came from, or *how* to fix it. For the expert, this is sufficient — they already know the context. For the beginner, this is radically under-informative. The maxim of quantity is satisfied for one audience and violated for another. **Verdict: Partial violation.**

**Quality:** Is this true? Yes. The expected type is `Vec<i32>` and the found type is `i32`. The compiler is not lying. **Verdict: Satisfied.**

**Relation:** Is this relevant? Yes — it identifies the specific location and nature of the type mismatch. It is directly relevant to the error. **Verdict: Satisfied.**

**Manner:** Is this perspicuous? "expected `Vec<i32>`, found `i32`" is unambiguous but opaque. The jargon (`Vec<i32>`) is obscure to beginners. The format (expected X, found Y) is concise but not explanatory. **Verdict: Partial violation.**

The overall assessment: the compiler satisfies quality and relation but struggles with quantity and manner. It tells the truth, and it tells you something relevant, but it does not tell you enough, and it does not tell you clearly. This is the pragmatic profile of most compiler error messages: honest but unhelpful, relevant but opaque.

---

## 4. Conversational Implicature and the Helpful Compiler

Grice's most powerful concept is *conversational implicature* — the meaning that is conveyed not by what is said but by what is *not said*, given the assumption that the speaker is following the cooperative principle. If someone asks "Is John a good programmer?" and you reply "He's very punctual," the implicature is that John is not a good programmer. You didn't say it. You followed all four maxims (you were informative, truthful, relevant, and perspicuous). But the *implicature* — what the listener infers — is clear.

Compiler error messages generate implicatures, most of them unintentional and many of them harmful.

Consider:

```
error: cannot find symbol: method getLength()
```

The literal meaning is: the compiler looked for a method called `getLength` and did not find it. The implicature — what the programmer infers — depends on their experience:

- **Beginner's implicature:** "The method doesn't exist. I'm doing something fundamentally wrong."
- **Intermediate's implicature:** "I probably misspelled the method name. Let me check the API."
- **Expert's implicature:** "This is a Java error, and the method is probably `length()`, not `getLength()`. I've been writing too much Python."

The same message generates three different implicatures based on three different levels of background knowledge. The compiler, of course, does not know which implicature the programmer will draw. It just says what it says and hopes for the best.

A pragmatically aware compiler would anticipate the implicatures and address them. It would say:

```
error: cannot find method `getLength()` on type `String`
help: `String` has a method `length()` — did you mean that?
```

The `help` line is not additional information in the semantic sense (the programmer could have figured it out). It is additional information in the *pragmatic* sense — it heads off the wrong implicature and steers the programmer toward the right one. This is what Grice would call *repairing* the conversational contribution. The first line (the error) was under-informative. The second line (the help) brings it up to the required level of informativeness.

Rust's compiler is genuinely good at this. Consider a real Rust error:

```
error[E0277]: the trait bound `Vec<i32>: Iterator` is not satisfied
 --> src/main.rs:4:14
  |
4 |     for x in vec {
  |              ^^^ `Vec<i32>` is not an iterator
  |
  = help: the following other types implement trait `Iterator`:
            std::vec::IntoIter<T>
            std::slice::Iter<'a, T>
            std::slice::IterMut<'a, T>
            and 140 others
  = note: you might need to call `.into_iter()` or `.iter()` or `.iter_mut()`
help: consider calling `.into_iter()` on the `Vec<i32>`
  |
4 |     for x in vec.into_iter() {
  |              ++++++++++++++++
```

This error message is a masterclass in pragmatic design. It satisfies all four maxims:

- **Quantity:** It tells you the error, the location, the types involved, the available alternatives, and a specific suggestion with the exact code to write.
- **Quality:** Everything is accurate. The types are correct. The suggestion compiles.
- **Relation:** Every piece of information is relevant to fixing the error. No noise.
- **Manner:** The message is structured hierarchically — error first, then context, then suggestions. It is orderly and perspicuous.

The Rust compiler team has explicitly acknowledged that they design error messages for pragmatics, not just semantics. The `rustc_errors` module includes infrastructure for suggestions, notes, and help messages — all of which are pragmatic constructs. They are not about what the error *is*. They are about what the programmer *needs to hear*. This is Grice applied to compilers, and it works.

---

## 5. The Maxim of Quantity and the Information Firehose

The maxim of quantity says: be as informative as required, but not more. Most compilers violate this maxim in both directions simultaneously: they are under-informative about what the programmer needs and over-informative about what the compiler knows.

Consider a C++ template error. When a template instantiation fails, the compiler produces pages of output — the full instantiation stack, every type involved, every constraint that was checked, every substitution failure. This is the compiler dumping its internal state, violating the maxim of quantity by being radically *more* informative than required. The programmer does not need to see the full instantiation stack. They need to know which template argument is wrong and why.

The reason for this violation is that the compiler lacks a pragmatic model. It does not know what the programmer needs. So it errs on the side of more information, hoping that the answer is in there somewhere. This is like answering the question "what time is it?" by reading the entire history of horology. Technically informative. Pragmatically useless.

A pragmatically aware compiler would filter its output based on the programmer's likely needs. For a beginner: short messages with explanations and suggestions. For an expert: precise diagnostics without the pedagogy. This requires the compiler to maintain a model of the user — a pragmatic model that tracks experience level, context, and likely intent.

Some modern compilers are moving in this direction. Elm's compiler is famous for its friendly, beginner-oriented error messages. Rust's compiler adapts its suggestions based on the error context. TypeScript's language server provides contextual suggestions in the IDE that are different from the errors shown on the command line. These are pragmatic adaptations — changes in the message based on changes in the context.

But no compiler today has a full pragmatic model. No compiler asks: "who is reading this message? What do they already know? What are they trying to do? What do they need to hear?" These are the questions that pragmatics demands, and they are questions that current compiler architectures are not designed to answer.

---

## 6. Context and the Indexical Error

In pragmatics, an *indexical* is an expression whose meaning depends on the context of utterance. "I" refers to the speaker. "Here" refers to the location. "Now" refers to the time. The meaning of an indexical is not fixed — it shifts with the context.

Error messages are full of indexicals. "Here," "this," "the above," "the following" — all of these refer to entities in the error context, and their meaning depends on what the programmer can see. Consider:

```
error: type mismatch here
```

"Here" is an indexical. It means "at this location in the source code." But the error message does not include the location — it assumes the programmer knows where "here" is. In a command-line compiler, "here" might be indicated by a line number. In an IDE, it might be indicated by a red squiggly underline. The meaning of "here" depends on the medium of presentation — the pragmatic context.

More subtly, consider:

```
error: cannot borrow `x` as mutable more than once at a time
```

"More than once" is indexical. It refers to a specific borrowing event — the second borrow that caused the error. But the programmer might not know which borrow was the first one. The message assumes that the programmer can identify both borrows from context. If they can't — if the borrows are in different functions, different files — the message is pragmatically opaque.

A pragmatically designed error message would resolve the indexicals explicitly:

```
error: cannot borrow `x` as mutable more than once
  --> first borrow at src/main.rs:2:5
  --> second borrow at src/main.rs:4:8
  = note: the first borrow is still active when the second borrow occurs
help: consider scoping the first borrow with a new block
```

This is what Rust actually does in many cases. The Rust compiler team has internalized the lesson of indexicals: never assume the programmer can see the context. Make the context explicit. Resolve the indexicals. Show, don't imply.

---

## 7. Speech Acts in Error Messages

Let us apply Searle's taxonomy of speech acts to error messages:

**Representatives (asserting):** "type mismatch at line 4." The compiler asserts a fact about the program. Most error messages are representatives.

**Directives (requesting):** "consider using `.into_iter()` instead." The compiler suggests an action. This is a directive — a polite request for the programmer to change their code.

**Commissives (promising):** "this error will be fixed by adding a lifetime annotation." The compiler commits to a claim about the future state of the program. This is risky — if the suggested fix doesn't work, the compiler has violated a commitment.

**Expressives (acknowledging):** "warning: this code is correct but unconventional." The compiler expresses an attitude about the code. This is less common but valuable.

**Declarations (enacting):** "compilation failed." The compiler declares a state change — the build is over, the program was not produced. This is a performative: the utterance creates the reality it describes.

The best error messages use a combination of these acts. They *assert* the error (representative), *suggest* a fix (directive), *explain* the context (representative), and *declare* the outcome (declaration). This multi-act structure is natural in human conversation — when a colleague points out a bug, they don't just say "this is wrong." They say "this is wrong, here's why, and here's what I'd do about it." The compiler should do the same.

The worst error messages use only one act type — the representative. "Syntax error" is a pure assertion. It tells you what is wrong but not why, not where (beyond a line number), and not how to fix it. The programmer must do all the pragmatic work themselves — inferring the cause, locating the error, and constructing a fix. This is the compiler outsourcing its pragmatic responsibility to the user.

---

## 8. Face Theory and the Tone of Errors

Penelope Brown and Stephen Levinson's politeness theory (1987) builds on Erving Goffman's concept of *face* — the public self-image that every person maintains. Brown and Levinson identify two types of face: *positive face* (the desire to be approved of, liked, respected) and *negative face* (the desire not to be imposed upon, to maintain autonomy). Every communicative act is a potential threat to one or both types of face.

Error messages are, by their nature, face-threatening acts. They tell the programmer that they made a mistake. This threatens positive face ("you did something wrong") and negative face ("you must fix this before you can proceed"). The question is how to deliver this threat while minimizing the damage.

The C compiler's approach: bald on record, no redress. "error: syntax error." This is the most face-threatening delivery possible. No explanation, no suggestion, no softening. It is the compiler equivalent of shouting "WRONG" in a crowded room.

The Elm compiler's approach: positive politeness. "I'm not sure what you mean by `foldl`. Did you mean `List.foldl`? It looks like you might need to import it." This softens the face threat by treating the error as a misunderstanding rather than a mistake. The compiler presents itself as a collaborator, not a judge. The use of "I" and "you" creates a conversational frame that reduces the threat.

The Rust compiler's approach: negative politeness with informative redress. "error[E0308]: mismatched types... consider changing the type annotation." The error code (E0308) is impersonal, distancing the threat from the programmer. The suggestion ("consider") is hedged, preserving the programmer's autonomy. The informative context (type names, locations, alternatives) provides the tools for self-correction without imposing a specific fix.

All three approaches satisfy Grice's maxims (they are truthful, relevant, informative, and clear). But they differ in their pragmatic framing — how they manage the face threat inherent in telling someone they are wrong. And the framing matters. Studies in computer science education (Kumar, 2014; Becker, 2019) have shown that the tone and framing of error messages significantly affect learning outcomes, debugging time, and programmer confidence. A compiler that speaks politely is not just more pleasant — it is more *effective*.

---

## 9. Jakobson's Functions and the Error as Communication

Roman Jakobson's model of communication (1960) identifies six functions of language, each corresponding to a component of the communicative act:

1. **Referential** (context): Conveying information about the world. "There is a type mismatch."
2. **Emotive** (addresser): Expressing the speaker's attitude. "I'm confused by this code."
3. **Conative** (addressee): Directing the listener to act. "Fix this type error."
4. **Phatic** (contact): Establishing or maintaining the communication channel. "Compiling..."
5. **Metalingual** (code): Talking about the language itself. "`i32` is a 32-bit signed integer type."
6. **Poetic** (message): Focusing on the form of the message itself. "error: the trait bound is not satisfied."

A good error message serves multiple functions simultaneously. It is referential (it states the error), conative (it suggests a fix), and metalingual (it explains the type system). A great error message also serves the emotive function — it acknowledges the programmer's frustration ("I know this is confusing — here's why") and the phatic function — it maintains the programmer's engagement with the compiler ("here are some things to try").

Most compiler errors serve only the referential and poetic functions. They state the error and they present it in a formatted way. They miss the conative (no suggestion), the emotive (no acknowledgment), the phatic (no ongoing engagement), and the metalingual (no explanation of the type system rule that was violated).

The Rust compiler's multi-part error messages serve all six functions. The primary error message is referential. The suggestions are conative. The notes are metalingual. The error codes and file locations are phatic (they maintain the channel). The friendly tone of the help messages is emotive. And the consistent formatting (error, note, help) is poetic.

This is why Rust's error messages are widely regarded as the best in the industry. Not because they are technically superior (they are generated by the same type checker that every compiler uses), but because they are pragmatically superior — they serve all six of Jakobson's functions, creating a communicative experience that is informative, actionable, and humane.

---

## 10. The Compiler That Followed Grice

Imagine a compiler that truly followed Grice's cooperative principle. What would it look like?

**Quantity:** It would give you exactly as much information as you need — no more, no less. For a beginner, it would explain the type system rule that was violated. For an expert, it would just show the types. It would adapt its verbosity to your level of expertise, which it would infer from your code (simple programs get simple explanations; complex programs get precise diagnostics).

**Quality:** It would never be wrong. It would never suggest a fix that doesn't compile. It would never claim a type that isn't correct. This is harder than it sounds — many compiler suggestions are best-effort heuristics that sometimes produce false positives. A Gricean compiler would check its suggestions before emitting them, sacrificing speed for accuracy.

**Relation:** Every line of the error message would be relevant to the error and to fixing it. No boilerplate, no noise, no "for more information see this overwhelming documentation page." The message would be laser-focused on what you need to know right now to move forward.

**Manner:** The message would be clear, brief, and orderly. It would use language that matches your level of expertise. It would avoid jargon when you don't need it and use it precisely when you do. It would structure its output for quick scanning — the most important information first, the details available on demand.

Such a compiler would not be a research project. It would be an engineering effort that requires:
1. A user model — tracking the programmer's experience level and context
2. A suggestion engine — generating and validating potential fixes
3. An explanation system — translating type system jargon into natural language
4. A presentation layer — formatting the message for the medium (CLI, IDE, web)

Each of these components exists in some form today. Rust has a suggestion engine. Elm has an explanation system. IDEs have a presentation layer. What does not exist is the integration — the pragmatic layer that ties them all together and makes the error message a *conversation* rather than a *declaration*.

The pragmatic compiler is not a fantasy. It is an engineering goal. And it is the most important unsolved problem in programming language design — not because it is the hardest technically (it isn't), but because it is the problem that affects the most people. Every programmer reads error messages. Every programmer is frustrated by them. Every programmer would be better served by a compiler that followed Grice's maxims — that cooperated, that was informative, truthful, relevant, and clear.

The compiler speaks. It is time we made it speak well.

---

## References

- Morris, C. (1938). "Foundations of the Theory of Signs." *International Encyclopedia of Unified Science*, 1(2), 1–59.
- Grice, H.P. (1989). *Studies in the Way of Words*. Harvard University Press.
- Searle, J.R. (1969). *Speech Acts: An Essay in the Philosophy of Language*. Cambridge University Press.
- Jakobson, R. (1960). "Closing Statement: Linguistics and Poetics." In Sebeok (ed.), *Style in Language*, 350–377. MIT Press.
- Brown, P. & Levinson, S.C. (1987). *Politeness: Some Universals in Language Usage*. Cambridge University Press.
- Goffman, E. (1967). *Interaction Ritual: Essays on Face-to-Face Behavior*. Doubleday.
- Becker, B.A. (2019). "An Effective Approach to Enhancing Compiler Error Messages." *Proceedings of the 50th ACM Technical Symposium on Computer Science Education*, 724–730.
- Barik, T., Ford, D., Smith, J., & Murphy-Hill, E. (2018). "How Developers Diagnose Compiler Error Messages." *Proceedings of the 40th International Conference on Software Engineering*, 1012–1023.
- Kumar, A.N. (2014). "An Evaluation of Integrated Development Environments for Novice Java Programmers." *Computer Science Education*, 24(3), 213–240.
