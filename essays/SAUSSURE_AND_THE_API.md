# Saussure and the API

*How the father of structural linguistics already explained why your function names are wrong, your standard library is arbitrary, and that's exactly the point*

---

## 1. The Sign

Ferdinand de Saussure's *Course in General Linguistics* (1916) — compiled posthumously from his students' lecture notes, making it one of the most influential books never actually written by its nominal author — introduced a distinction that would reshape every human science. The linguistic sign, Saussure argued, is composed of two parts: the *signifier* (signifiant) — the sound pattern, the acoustic image, the form — and the *signified* (signifié) — the concept, the meaning, the mental content. The word "tree" is a sign whose signifier is the sequence of phonemes /triː/ and whose signified is the concept of a tree — the woody, leafy, rooted thing that grows in forests.

The relationship between signifier and signified, Saussure insisted, is *arbitrary*. There is no natural connection between the sound "tree" and the concept of a tree. The same concept is signified by "arbre" in French, "Baum" in German, "木" in Japanese. The choice of signifier is conventional — determined by the history of the language community, not by any inherent fitness of the sound for the concept. The word "tree" does not sound tree-like. It means "tree" only because English speakers have agreed — implicitly, historically, collectively — that it does.

Now consider the function:

```rust
fn push(&mut self, value: T)
```

The signifier is `push`. The signified is the behavior: "add an element to the end of this collection, reallocating if necessary, updating the length." The relationship between `push` and this behavior is arbitrary. The same behavior could be called `add`, `append`, `insert`, `enqueue`, `put`, `store`, or `xqrplz`. None of these names has a natural connection to the behavior. `push` has become conventional — not because it is inherently better, but because enough programmers have used it in enough contexts that it has acquired a stable meaning within the programming language community.

This is Saussure's arbitrariness of the sign, instantiated in code. The API is the signifier. The behavior is the signified. And the gulf between them is where all the interesting things happen.

---

## 2. The Arbitrariness of the API

Let me press this point, because it is the foundation of everything that follows. Consider the standard library of any major programming language and ask: why these names and not others?

In Rust:
- `Vec::push` — add an element
- `Vec::pop` — remove the last element
- `Vec::len` — get the length
- `Vec::iter` — get an iterator
- `Vec::sort` — sort in place

Why `push` and not `add`? Because `push` evokes the stack operation — push onto the top. But `Vec` is not a stack. You can push to the end, but you can also insert at any position. The name `push` is a metaphor that constrains the mental model. It suggests stack-like behavior in a data structure that is more general.

Why `len` and not `length` or `size` or `count`? Because of convention and history. `len` is short, which matters for a frequently used operation. `length` would work just as well — Python uses it (actually Python uses `len()` as a built-in function, but `list.__len__` is the method). `size` would also work — C++ uses it. `count` would work — some libraries use it. The choice is arbitrary, constrained only by brevity and convention.

Why `iter` and not `iterator` or `each` or `walk` or `traverse`? Ruby uses `each`. JavaScript uses `forEach` and `Symbol.iterator`. Python uses `__iter__`. Each language has made a different arbitrary choice for the same signified.

Saussure would not be surprised. He would say: of course the names are different. The sign is arbitrary. The meaning is determined not by the name but by the *system of names* — the position of each signifier relative to every other signifier in the language.

---

## 3. Value Through Opposition

Saussure's most radical claim is that meaning is determined not by the relationship between signifier and signified, but by the relationship between signifiers *within the system*. A sign means what it means because it is *different from* other signs. "Cat" means "cat" not because of any inherent catness in the word, but because "cat" is not "bat," "mat," "rat," or "hat." The phonological difference produces the semantic difference. Meaning is differential.

In an API, this principle operates with striking clarity:

- `push` vs `pop` — add vs remove, LIFO pair
- `insert` vs `remove` — add at position vs remove at position, indexed pair
- `get` vs `set` — read vs write, accessor pair
- `encode` vs `decode` — serialize vs deserialize, transformation pair
- `lock` vs `unlock` — acquire vs release, synchronization pair
- `open` vs `close` — begin vs end, lifecycle pair
- `connect` vs `disconnect` — establish vs terminate, network pair
- `enable` vs `disable` — activate vs deactivate, toggle pair
- `serialize` vs `deserialize` — to bytes vs from bytes, marshalling pair
- `encrypt` vs `decrypt` — to ciphertext vs from ciphertext, cryptography pair

Each pair defines meaning through opposition. `push` means "add to the end" partly because `pop` means "remove from the end." If the language had only `push` and not `pop`, `push` would be less meaningful — it would be an "add" operation without a specific directional or positional connotation. The existence of `pop` — the complementary operation — gives `push` its stack-like flavor. The two signs define each other.

This is Saussure's structuralist insight: meaning is not in the individual sign but in the *system of differences*. An API is not a collection of independent operations. It is a *structure* — a network of oppositions where each operation derives its meaning from its position relative to every other operation.

Consider what happens when this structure is violated. If you have `push` and `pop` (stack operations) but then add `enqueue` and `dequeue` (queue operations) to the same data structure, the meaning of all four operations becomes confused. Is this a stack or a queue? The structural oppositions have broken down. The programmer can no longer infer the semantics from the names alone because the names no longer form a coherent system of differences. The API has lost its structural integrity.

Good API design is structuralist design. It creates systems of signs where each sign's meaning is determined by its position in a network of oppositions. Bad API design is anti-structuralist: it creates collections of signs where meanings are vague, overlapping, or contradictory. The difference between a well-designed API and a poorly designed one is not a matter of individual function names. It is a matter of the *structure* of those names — the system of differences that gives each name its meaning.

---

## 4. Synchrony and Diachrony

Saussure distinguished between *synchronic* linguistics — the study of a language at a single point in time — and *diachronic* linguistics — the study of how a language changes over time. He argued that these are fundamentally different enterprises. Synchronic analysis reveals the structure of the system. Diachronic analysis reveals how that structure evolved. The structure at any given moment does not depend on its history — a speaker of modern English does not need to know Old English to speak modern English. But the history explains how the current structure came to be.

APIs have both synchronic and diachronic dimensions. The synchronic API is the interface as it exists today — the set of functions, their names, their signatures, their documentation. The diachronic API is the history of how the interface evolved — what was added, what was deprecated, what was renamed, what was removed.

The synchronic API is what programmers learn and use. You do not need to know that `Vec::push` was once called `push_back` in an earlier version of the language (it wasn't — but imagine it was). You need to know what `push` does *now*. The current meaning is determined by the current system, not by its history.

But the diachronic API explains the quirks. Why does Python have both `list.sort()` and `sorted(list)`? Because `sorted` was added later as a built-in function, while `sort` has been a list method since the beginning. The diachronic history explains the redundancy. Why does JavaScript have both `typeof null` returning `"object"` and `null` being a primitive value? Because of a bug in the original implementation that became part of the spec for backwards compatibility. The history explains the inconsistency.

Saussure's insight is that the synchronic system is what matters for users, while the diachronic history is what matters for designers. The user sees the API as a static structure — a system of signs with fixed relationships. The designer sees it as a dynamic process — a system that has evolved and will continue to evolve. Both perspectives are valid. Neither is complete without the other.

The challenge of API versioning is fundamentally a Saussurean challenge. When you change an API, you are changing the sign system. The old signs (function names, signatures, behaviors) had meanings determined by their position in the old system. The new signs have meanings determined by their position in the new system. If the change is radical enough — if enough signs are renamed, removed, or redefined — the entire system of differences shifts, and the meanings of unchanged signs may change as well. This is why deprecation is so important: it bridges the synchronic and diachronic, allowing the system to evolve while preserving the structure that current users depend on.

---

## 5. Langue and Parole: The Library and the Program

Saussure's most fundamental distinction is between *langue* (language as a social institution, the abstract system of rules and conventions) and *parole* (speech, the individual act of using language). Langue is shared. Parole is personal. Langue is stable. Parole is ephemeral. Langue is the system. Parole is the event.

The standard library is langue. Your program is parole.

The standard library defines the shared system of signs — the functions, types, traits, and conventions that all programmers in the language agree upon. It is the social institution of the language, maintained by a community (the language designers, the standard committee, the open-source contributors) and shared by all users. It changes slowly, through deliberate processes (RFCs, proposals, votes). It is the grammar and vocabulary of the language.

Your program is parole — an individual act of using the language to express something. It uses the signs of the standard library (langue) to create new signs (your functions, your types, your APIs) that are meaningful within your specific context. Your program is a speech act — a creative, individual use of the shared system.

The distinction explains several phenomena. First, why standard library design is so contentious: because langue belongs to everyone, everyone has an opinion about it. Changes to the standard library affect all programs (all acts of parole). A poorly named standard library function is a permanent, shared burden. A well-named one is a permanent, shared benefit. The stakes are high because the audience is universal.

Second, why internal APIs can be more experimental: because they are closer to parole than langue. An internal API is used by a small team, not the entire language community. It can change more freely because fewer people depend on it. The cost of renaming an internal function is measured in hours of refactoring. The cost of renaming a standard library function is measured in millions of broken programs.

Third, why documentation is essential for langue and optional for parole. The standard library must be documented because it is shared — you cannot assume that users share your mental model. Your internal code needs less documentation because you can assume that your teammates share your context. Documentation is the bridge between individual understanding and shared meaning. It is what makes langue accessible to all speakers.

---

## 6. Syntagmatic and Paradigmatic Relations

Saussure identified two types of relationship that organize the linguistic system. *Syntagmatic* relations are horizontal — the relationships between signs that co-occur in a sequence. In "the cat sat on the mat," each word's meaning is partly determined by its neighbors. "Sat" means what it means because it follows "the cat" (a noun phrase that serves as the subject) and precedes "on the mat" (a prepositional phrase that serves as the locative complement). The syntagmatic axis is the axis of combination.

*Paradigmatic* relations are vertical — the relationships between signs that could substitute for each other in a given position. In "the cat sat on the mat," "cat" could be replaced by "dog," "child," "professor," or "tyrannosaurus." Each substitution changes the meaning. The paradigmatic axis is the axis of selection.

In an API, syntagmatic relations are the *call sequences*. To read a file in Rust:

```rust
let mut file = File::open("data.txt")?;  // open
let mut contents = String::new();        // allocate buffer
file.read_to_string(&mut contents)?;     // read
```

The sequence `open → allocate → read` is a syntagmatic chain. Each operation's meaning depends on its position in the chain. `read_to_string` means what it means because it follows `open` (the file is already open) and uses `contents` (the buffer is already allocated). The syntagmatic relations create the *program's* meaning — the horizontal flow of operations that accomplishes a task.

The paradigmatic relations are the *alternatives* at each position. Instead of `File::open`, you could use `File::create` (open for writing). Instead of `read_to_string`, you could use `read_to_end` (read into a `Vec<u8>`) or `read_exact` (read a specific number of bytes). Each alternative defines the meaning of the chosen operation through its *absence*. `open` means "open for reading" partly because it is *not* `create` (open for writing). The paradigmatic axis creates meaning through the alternatives that were available but not chosen.

Good API design operates on both axes. Syntagmatically: the operations should compose naturally, forming chains that read like sentences. Paradigmatically: the alternatives should be clearly differentiated, each occupying a distinct niche in the design space. An API where the paradigmatic alternatives blur together — where `read`, `read_to_string`, `read_to_end`, and `read_exact` overlap in confusing ways — has failed paradigmatically. An API where the operations don't compose naturally — where you need obscure incantations to perform common sequences — has failed syntagmatically.

The fluent interface pattern (method chaining) is a syntagmatic design technique:

```rust
let result = vec.iter()
    .filter(|x| x > &0)
    .map(|x| x * 2)
    .collect::<Vec<_>>();
```

Each method in the chain is a syntagmatic unit, and the chain is a syntagmatic relation. The meaning of the whole is determined by the sequence of its parts. The paradigmatic axis operates at each position: instead of `filter`, you could use `filter_map`; instead of `map`, you could use `for_each`; instead of `collect`, you could use `fold` or `reduce`. The programmer navigates both axes simultaneously, selecting operations (paradigmatic) and combining them (syntagmatic) to express the desired computation.

This is language use in Saussure's fullest sense. Programming is the creative combination of signs along both axes — selecting from the paradigmatic alternatives (what the standard library provides) and arranging them in syntagmatic chains (what the program requires). The API is the langue that makes this creativity possible. The program is the parole that realizes it.

---

## 7. The Structuralist Analysis of the Standard Library

If we take Saussure seriously, we should be able to perform a structuralist analysis of any standard library — identifying the systems of opposition, the networks of difference, the paradigmatic and syntagmatic relations that give the API its meaning.

Consider the Rust collection types: `Vec<T>`, `VecDeque<T>`, `LinkedList<T>`, `HashMap<K, V>`, `BTreeMap<K, V>`, `HashSet<T>`, `BTreeSet<T>`, `BinaryHeap<T>`. These form a structure of oppositions:

- **Ordered vs unordered:** `Vec` vs `HashMap`, `BTreeMap` vs `HashMap`
- **Indexed vs sequential:** `Vec` (random access) vs `LinkedList` (sequential only)
- **Map vs set:** `HashMap` vs `HashSet`, `BTreeMap` vs `BTreeSet`
- **Sorted vs unsorted:** `BTreeMap` vs `HashMap`, `BTreeSet` vs `HashSet`
- **Stack vs queue vs deque:** `Vec` (stack) vs `VecDeque` (double-ended queue)
- **Heap vs others:** `BinaryHeap` (priority) vs all others (no priority)

Each opposition defines a dimension of meaning. A `HashMap` is meaningful not in isolation but as *not-`BTreeMap`* (not sorted) and *not-`Vec`* (not indexed by position). A `Vec` is meaningful as *not-`VecDeque`* (stack, not deque) and *not-`LinkedList`* (indexed, not sequential). The system of collection types is a Saussurean structure — a network of differences where each type's meaning is determined by its position relative to every other type.

Now consider what happens when a type is added to the system. If Rust added, say, a `TrieMap<K, V>` (a map based on a trie data structure), it would not just add a new type. It would shift the entire structure. `HashMap` would now be "the fast unordered map" as opposed to `TrieMap`'s "the prefix-efficient map." `BTreeMap` would be "the sorted map" as opposed to both. The addition of one type changes the meaning of all existing types, because meaning is relational. This is Saussure's structuralism in action.

The standard library's naming conventions also form a structural system. Rust uses short, imperative names for common operations (`push`, `pop`, `get`, `set`, `len`, `sort`). Less common operations get longer, more descriptive names (`with_capacity`, `from_raw_parts`, `into_boxed_slice`). This is a graded system where the length of the signifier encodes the frequency of the signified — a structural relationship between form and meaning that is not arbitrary but *motivated*.

Saussure acknowledged that some signs are more motivated than others. Onomatopoeia — words that imitate sounds — are motivated: "cuckoo" sounds like the bird's call. But even onomatopoeia is conventionalized (French "coucou" is different from English "cuckoo"). In APIs, motivation appears when the function name suggests its behavior: `sort` really does sort, `reverse` really does reverse. But `HashMap::get` could just as easily be called `HashMap::lookup` or `HashMap::find` or `HashMap::at`. The choice is conventional. The motivation is partial. The arbitrariness is always underneath.

---

## 8. Diachronic Catastrophe: When APIs Break

In 2015, the Python community experienced a Saussurean crisis. Python 3.0, released in 2008, had introduced a number of breaking changes from Python 2. The most notorious was the change in how strings worked: Python 2's `str` type was a byte string, and `unicode` was a separate type. Python 3's `str` type was a Unicode string, and `bytes` was the byte string type. The signifier `str` had been reassigned to a different signified.

For Saussure, this is a diachronic event with synchronic consequences. The Python 2 system of string types (`str` vs `unicode`) was a structure with specific oppositions. The Python 3 system (`str` vs `bytes`) was a different structure with different oppositions. The migration from one to the other was not just a technical change — it was a *structural* change. The meaning of every string operation in every Python program had to be re-evaluated in the new system.

The migration took years. In 2015, seven years after Python 3's release, many major projects were still on Python 2. The cost was enormous, and the cause was not any single technical change but the cumulative effect of many changes to the sign system. The structure of Python had shifted, and every program that depended on the old structure had to be rebuilt.

This is the diachronic catastrophe that Saussure's framework predicts. Language change is not a simple matter of adding new words. It is a restructuring of the entire system of differences. When the structure changes, the meaning of every sign is potentially affected. The Python 2-to-3 transition is the programming language equivalent of the Great Vowel Shift — a systemic change that altered the relationships between all elements.

API designers who understand Saussure design for stability. They recognize that the API is a structure of differences, and that any change to one element affects the meaning of all others. They add new elements rather than changing existing ones. They deprecate rather than remove. They maintain the system of oppositions even as the system evolves. They treat the API as what it is: a language, with all the fragility and power that implies.

---

## 9. Naming as Political Economy

Saussure's arbitrariness principle has a corollary that is less often discussed: the choice of signifier, while arbitrary, is not neutral. The signifier that becomes conventional shapes how we think about the signified. To call an operation `push` is to invoke the metaphor of a stack — of physical pressure, of stacking objects. To call the same operation `append` is to invoke the metaphor of a list — of adding to the end, of concatenation. The behavior is the same. The mental model is different. The name shapes the thought.

This is the Sapir-Whorf hypothesis applied to APIs: the vocabulary of your programming language shapes how you think about the problems you solve. A language that calls collections "arrays" encourages indexed, positional thinking. A language that calls them "lists" encourages sequential, recursive thinking. A language that calls them "sequences" encourages abstract, generic thinking. The signifier shapes the signified, not by changing the behavior, but by changing the *frame* through which the programmer understands the behavior.

The politics of naming in APIs is real. When a library calls its master-slave architecture "master-slave," it reinforces a metaphor that carries historical baggage. When it renames to "primary-replica," the metaphor changes, and with it, the mental frame. The behavior is identical. The signifier is different. And the difference matters — not because the old signifier is "wrong" (Saussure: the sign is arbitrary) but because signifiers are embedded in social contexts that give them connotations beyond their denotations.

The standard library of a programming language is a political document. Its naming choices reflect the values, assumptions, and blind spots of its creators. The POSIX function `creat()` (for "create a file") is missing its final 'e' because, according to Dennis Ritchie, the original Unix file system had a limit on the length of variable names, and the name was chosen to fit. The missing 'e' has persisted for fifty years — an arbitrary signifier that has become a historical artifact, a fossil of a technical constraint that no longer exists. Every time a programmer types `creat()`, they are reminded that language is shaped by history, not by reason.

---

## 10. The API as Langue

An API is a language. Not a metaphorical language — a real language, with signifiers (function names, type names, method names) and signifieds (behaviors, invariants, contracts). The relationship between signifier and signified is arbitrary but conventionalized. Meaning is determined by opposition (`push` vs `pop`, `get` vs `set`). The system has synchronic structure (what the API is now) and diachronic history (how it evolved). It operates on syntagmatic (call sequences) and paradigmatic (alternative operations) axes. It distinguishes langue (the standard library) from parole (the program).

Saussure gave us the tools to understand why some APIs feel natural and others feel alien. A natural API is one whose structure of oppositions is clear, consistent, and learnable. An alien API is one whose structure is muddy, inconsistent, or hidden. The difference is not in the behaviors — those are what they are. The difference is in the *signs* — the names, the patterns, the conventions that give the behaviors meaning.

The next time you design an API, think like a linguist. Ask: what are my signifiers? What are my signifieds? Are the oppositions clear? Is the structure consistent? Does the naming reflect the behavior, or does it obscure it? Have I created a system of differences where each sign means something because of what it is not?

You are not just writing function signatures. You are creating a language. Saussure would expect nothing less.

---

## References

- Saussure, F. de (1916). *Cours de linguistique générale*. Payot. English translation by R. Harris (1983), *Course in General Linguistics*. Duckworth.
- Harris, R. (1987). *Reading Saussure: A Critical Commentary on the Cours de linguistique générale*. Duckworth.
- Culler, J. (1976). *Ferdinand de Saussure*. Cornell University Press.
- Hawkes, T. (1977). *Structuralism and Semiotics*. Methuen.
- Bloch, J. (2008). *Effective Java* (2nd ed.). Addison-Wesley. (Chapter 7: General Programming — API design principles.)
- Raymond, E.S. (2004). *The Art of UNIX Programming*. Addison-Wesley. (Naming conventions as structural system.)
- Tulving, E. & Thomson, D.M. (1973). "Encoding Specificity and Retrieval Processes in Episodic Memory." *Psychological Review*, 80(5), 352–373.
