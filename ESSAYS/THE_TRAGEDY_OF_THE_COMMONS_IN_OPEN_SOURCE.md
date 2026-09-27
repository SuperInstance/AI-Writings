# THE TRAGEDY OF THE COMMONS IN OPEN SOURCE

## On Hardin, Ostrom, and Whether the Crate Ecosystem Can Govern Itself

*Two volunteers maintained the infrastructure the entire internet depended on. This was either a miracle of efficiency or a catastrophe waiting to happen. It was both.*

---

## I. The Story of OpenSSL

In April 2014, the world discovered the Heartbleed bug. A flaw in OpenSSL — the open source library that encrypted roughly two-thirds of all internet traffic — allowed attackers to read arbitrary memory from servers, extracting passwords, private keys, and session cookies. The vulnerability had existed for two years. It affected millions of websites. The estimated cost of remediation ran into hundreds of millions of dollars.

The technical details of Heartbleed are well-documented. The economic details are more revealing. At the time Heartbleed was discovered, the OpenSSL project had exactly one full-time developer. His name was Stephen Henson. He was supported by the OpenSSL Software Foundation, which in 2013 received total donations of approximately $2,000.

Two thousand dollars. For the encryption layer of the global internet.

The large corporations that depended on OpenSSL — Google, Amazon, Facebook, Cisco, every bank and government agency — contributed nothing. They used the software. They relied on it for the security of billions of dollars in transactions. They did not fund its development, audit its code, or contribute patches. They were, in the language of economics, free riders — consuming a common resource without contributing to its maintenance.

OpenSSL is the canonical example of the tragedy of the commons in open source. But it is not the only one. It is not even the most dramatic.

---

## II. Hardin's Tragedy

In 1968, the ecologist Garrett Hardin published one of the most influential essays in the history of social science: "The Tragedy of the Commons." His argument was simple and devastating.

Consider a pasture open to all herders. Each herder benefits from adding one more animal to the pasture (the additional animal provides milk, wool, or meat). But the cost of that additional animal — the overgrazing of the pasture — is shared by all herders. The benefit to the individual herder exceeds his share of the cost. Therefore, each rational herder adds more animals. The pasture is overgrazed. All herders suffer.

Hardin's conclusion: "Freedom in a commons brings ruin to all." The only solutions, he argued, were privatization (convert the commons to private property) or regulation (impose external controls on usage).

The open source ecosystem is a commons. The pasture is the shared codebase. The herders are the users (companies and developers). The animals are the features, bug fixes, and support that each user demands. And the overgrazing takes the form of:

**Maintenance debt.** Each user files bug reports, requests features, and demands support. These demands consume maintainer time — a scarce resource. The benefit to the user (getting their bug fixed) exceeds their share of the cost (the maintainer's time, shared across all users). Therefore, each user makes more demands. The maintainer is overwhelmed.

**Dependency proliferation.** Each user adds dependencies freely — every `cargo add` is another animal on the pasture. The cost of each dependency (increased attack surface, supply chain risk, build time) is shared by the entire ecosystem. The benefit (saved development time) accrues to the individual user. Therefore, dependencies proliferate. The ecosystem becomes fragile.

**Abandonment.** When a maintainer can no longer sustain the volunteer effort, they abandon the project. The users who depended on the project are left with an unsupported, potentially insecure dependency. The cost of migration (replacing the abandoned crate with a maintained alternative) is borne by the users. The benefit of the free ride (using the crate without contributing) was captured by the users before the maintainer left.

This is the tragedy of the open source commons. It is not theoretical. It has happened, repeatedly, to some of the most critical pieces of software infrastructure in the world.

---

## III. left-pad and the Fragility of the Commons

On March 22, 2016, a developer named Azer Koçulu unpublished 273 of his npm packages from the npm registry. One of those packages was `left-pad`, an 11-line function that pads strings to a given length. At the time, `left-pad` was depended upon by thousands of npm packages, including `babel` (the most widely used JavaScript transpiler) and `react` (the most widely used JavaScript UI framework).

The result was catastrophic. Builds broke across the JavaScript ecosystem. Projects that had nothing to do with Azer Koçulu or his dispute with npm Inc. found themselves unable to compile. The dependency chain was so deep and so tangled that removing an 11-line function brought down a significant portion of the npm ecosystem.

The technical lesson of left-pad is about dependency management. The economic lesson is about the commons. `left-pad` was a common resource — a small piece of infrastructure that thousands of projects depended on without contributing to its maintenance. The "pasture" was maintained by one person, in his spare time, for free. When he decided to stop maintaining it, the pasture collapsed.

The parallels to Hardin's tragedy are exact:

1. **The resource is shared.** `left-pad` was used by thousands of projects.
2. **The resource is under-maintained.** One person wrote and maintained it.
3. **The users do not contribute.** None of the major projects depending on `left-pad` (Babel, React) funded its development or contributed to its maintenance.
4. **The collapse harms everyone.** When `left-pad` was unpublished, thousands of builds broke simultaneously.

The npm ecosystem has since implemented safeguards (packages can no longer be unpublished if they have dependents). But the safeguards address the symptom (packages being unpublished), not the cause (critical infrastructure maintained by volunteers without funding or support).

---

## IV. Elinor Ostrom and the Governable Commons

In 2009, Elinor Ostrom became the first woman to receive the Nobel Prize in Economic Sciences. Her work challenged Hardin's pessimistic conclusion. Ostrom spent decades studying communities that successfully managed common-pool resources — irrigation systems in Spain, mountain grazing lands in Switzerland, inshore fisheries in Turkey, forest management in Japan. These communities did not privatize their commons. They did not submit to external regulation. They governed themselves.

From these studies, Ostrom derived eight principles for successful commons governance:

**1. Clearly defined boundaries.** Who is entitled to withdraw from the resource, and what are they entitled to withdraw? The community must know who the users are and what their rights and obligations are.

**2. Proportional equivalence between benefits and costs.** Users who benefit from the commons must contribute to its maintenance in proportion to their benefit. Those who benefit more should contribute more.

**3. Collective-choice arrangements.** The users themselves must participate in making and modifying the rules. Rules imposed from outside are less likely to be followed and less likely to be appropriate.

**4. Monitoring.** The resource and the users must be monitored to ensure compliance with the rules. Monitoring must be accountable to the users.

**5. Graduated sanctions.** Users who violate the rules should face sanctions that escalate with the severity and frequency of violations.

**6. Conflict-resolution mechanisms.** There must be cheap, accessible means for resolving disputes among users or between users and monitors.

**7. Minimal recognition of rights to organize.** The community's right to govern itself must be recognized by external authorities. If the government can override the community's rules, self-governance is fragile.

**8. Nested enterprises.** For large commons, governance must be organized in multiple nested layers — from local to regional to global — with appropriate authority at each level.

These principles are not aspirational. They are empirical. Ostrom derived them from the study of real communities managing real commons, many of which have sustained their resources for centuries — in some cases, for over a thousand years. The *huerta* irrigation systems of Valencia, Spain, have been governed communally since the 10th century. The *Törbel* grazing commons in Switzerland has been managed by the same community since 1224.

The question is: can Ostrom's principles be applied to the open source commons?

---

## V. Ostrom's Principles Applied to crates.io

Let us evaluate the Rust crate ecosystem against each of Ostrom's eight principles.

**Principle 1: Clearly defined boundaries.**

The crate ecosystem has clear boundaries in one sense: anyone with an internet connection can download and use crates. But this is the *opposite* of what Ostrom prescribes. Ostrom's principle requires that the community define who has access and under what conditions. The crate ecosystem defines no such boundaries — access is unrestricted.

This is not necessarily a failure. Open access is a design choice, not a flaw. But it means that the "community of users" is effectively everyone, and the obligations of users are undefined. A Fortune 500 company using `serde` in a billion-dollar product has the same rights and obligations as a student using it for a homework assignment. Ostrom would say this is a governance problem.

**Principle 2: Proportional equivalence between benefits and costs.**

This principle fails spectacularly. The benefits of the crate ecosystem are concentrated in the users (particularly large corporations) while the costs are concentrated in the maintainers (typically unpaid volunteers). There is no mechanism — no norm, no rule, no institution — that requires users to contribute in proportion to their benefit.

Some ecosystems have partial solutions. The Rust Foundation provides grants to maintainers of critical crates. Companies like Google and Microsoft employ developers to work on open source. But these contributions are voluntary, uncoordinated, and vastly insufficient relative to the value extracted.

**Principle 3: Collective-choice arrangements.**

The crate ecosystem has some collective-choice mechanisms: RFCs (Request for Comments) for language and ecosystem changes, governance committees for major projects, and community discussion forums. But these mechanisms operate at the level of the *language* and the *tooling*, not at the level of individual crates. Individual crate maintainers are autocrats — they make all decisions about their crates unilaterally. This is efficient (no committee can make decisions as fast as a single maintainer) but fragile (the crate's governance depends entirely on one person).

**Principle 4: Monitoring.**

The crate ecosystem has excellent monitoring for *technical* properties: CI/CD pipelines run tests on every commit, cargo audit scans for known vulnerabilities, and crater detects breaking changes across the ecosystem. But it has almost no monitoring for *governance* properties: which crates are unmaintained, which maintainers are burned out, which critical dependencies have single points of failure.

The `cargo outdated` and `cargo audit` tools provide partial governance monitoring, but they are reactive (they tell you about problems that already exist) rather than proactive (they don't prevent problems from developing).

**Principle 5: Graduated sanctions.**

The crate ecosystem has few sanctions, graduated or otherwise. The most severe sanction — removing a crate from the registry — is reserved for extreme cases (malware, legal issues). There are no sanctions for failing to maintain a crate, for ignoring security issues, or for depending on unmaintained crates. The npm ecosystem's approach to sanctions (unpublishing packages) led to the left-pad disaster, which illustrates the difficulty of applying sanctions in a commons without breaking the commons.

**Principle 6: Conflict-resolution mechanisms.**

Conflicts in the crate ecosystem are resolved through ad hoc mechanisms: GitHub issues, pull requests, discussion forums, and social media. There is no formal arbitration process, no mediation system, no binding dispute resolution. Conflicts between maintainers and users (e.g., over API design, feature prioritization, or licensing) are resolved informally, which means they are often resolved by the maintainer leaving (the "I'm archiving this project" resolution).

**Principle 7: Minimal recognition of rights to organize.**

The Rust Foundation provides some institutional recognition of the crate ecosystem's right to self-govern. But the Foundation's authority is limited — it cannot compel maintainers to maintain, users to contribute, or companies to fund. The legal framework for open source governance (licensing, intellectual property) is well-established, but the economic framework (funding, sustainability) is not.

**Principle 8: Nested enterprises.**

The crate ecosystem has some nesting: the Rust Foundation oversees the language and tooling; the crates.io team oversees the registry; individual crate maintainers oversee their crates. But the nesting is incomplete — there is no governance layer between the Foundation (which oversees the ecosystem as a whole) and the individual maintainers (who oversee individual crates). There is no "crate consortium" that represents the interests of maintainers, sets standards for maintenance, or coordinates funding.

---

## VI. Is Open Source a Commons That Can Be Governed?

Ostrom's principles suggest that the open source commons is governable in principle but poorly governed in practice. The gap is not in the principles — Ostrom's framework is flexible enough to accommodate the unique characteristics of digital commons. The gap is in the institutions.

Traditional commons are governed by communities that have面对面 relationships, shared history, and mutual dependence. The herders of Törbel have known each other for generations. The irrigators of Valencia meet in the *Tribunal de las Aguas* every Thursday morning, as they have for a thousand years. These relationships create trust, enforce norms, and enable collective action.

The crate ecosystem has none of this. Crate maintainers are distributed across continents. They communicate through text. They have no shared history beyond their GitHub profiles. They have no mutual dependence — one maintainer's crate failing does not affect another maintainer's livelihood. The social infrastructure that makes traditional commons governance possible is absent.

This does not mean the commons cannot be governed. It means the governance must be designed for the medium. Digital commons require digital institutions: automated monitoring (already partially implemented), algorithmic sanctions (e.g., crates that are unmaintained for more than N months are flagged and eventually quarantined), decentralized governance (e.g., DAO-like structures for making collective decisions about critical crates), and nested enterprises (e.g., a "Rust Crate Foundation" that represents maintainers and coordinates funding).

The technology for these institutions exists. The social will to implement them does not — or has not yet. The open source community has a deep cultural aversion to governance, born of its libertarian origins (Richard Stallman's "free as in freedom" is a political statement, not just a licensing one) and reinforced by decades of successful (but fragile) self-organization.

But Ostrom's lesson is clear: commons that are not governed eventually fail. The failure may be slow (gradual abandonment of unmaintained crates) or sudden (a Heartbleed-scale security catastrophe). The form of failure depends on the specific commons. The fact of failure depends only on the absence of governance.

---

## VII. What Would Ostrom Say?

Ostrom studied commons that worked and commons that failed. The ones that worked had all eight principles (or most of them). The ones that failed were missing one or more.

If Ostrom were to evaluate crates.io, she would, I believe, reach the following conclusions:

**The crate ecosystem is a common-pool resource.** The crates are the resource. The maintainers are the providers. The users are the appropriators. The dependency graph is the physical infrastructure (analogous to the irrigation canals in a water commons).

**The crate ecosystem is currently in a pre-governance state.** It has not yet experienced a catastrophic failure (Heartbleed for OpenSSL, left-pad for npm) that would catalyze the formation of governance institutions. But the conditions for such a failure are present: critical dependencies maintained by single individuals, no funding for maintenance, no monitoring for governance health, and rapidly increasing usage by corporations that do not contribute.

**Governance will emerge, either by design or by crisis.** Ostrom observed that commons governance institutions typically emerge in response to a crisis — a drought, a famine, a conflict over resource allocation. The crisis creates the social conditions for collective action. In the crate ecosystem, the analogous crisis would be a catastrophic security failure in a core crate (a Rust Heartbleed) or the simultaneous abandonment of multiple critical crates (a maintainer strike).

**The governance institutions should be designed for the digital commons.** Ostrom was adamant that governance must be tailored to the specific characteristics of the resource and the community. The digital commons has unique characteristics: non-rival consumption, global scale, asynchronous communication, and the possibility of automated enforcement. Governance institutions that leverage these characteristics — rather than trying to replicate face-to-face institutions — are more likely to succeed.

**The governance must be nested.** Individual crates cannot be governed independently of the ecosystem. The dependency graph creates externalities — a change in one crate affects all downstream crates. Governance must operate at multiple levels: individual crates, clusters of related crates, the registry as a whole, and the ecosystem in relation to its corporate users.

Ostrom would not be pessimistic. She spent her career showing that commons can be governed, that communities can overcome the tragedy, that human beings are capable of collective action even without the state or the market. But she would insist that governance does not happen automatically. It must be designed, implemented, and maintained — just like the code it governs.

---

## VIII. The Polygon of Sustainability

The tragedy of the commons is not inevitable. Hardin was wrong about that. Ostrom showed that communities can govern commons sustainably, and she identified the principles that make this possible.

But Ostrom also showed that governance is hard. It requires institutions, monitoring, sanctions, and collective choice. It requires that the community invest in governance as well as in the resource itself. And it requires that the governance be adapted to the specific characteristics of the commons.

The open source commons has unique characteristics that make governance both easier and harder than traditional commons:

**Easier because:**
- Code is non-rival (my use of serde does not diminish your use of serde)
- Monitoring can be automated (CI/CD, dependency scanning)
- The community is technically sophisticated (developers can build governance tools)
- The resource does not degrade from use (code does not wear out from being executed)

**Harder because:**
- The community is global and anonymous (no face-to-face relationships)
- The free rider problem is extreme (corporations extract enormous value without contributing)
- The maintenance burden grows with adoption (more users = more bugs, more feature requests, more support)
- There is no clear boundary between "users" and "community members"

The path forward is not to choose between Hardin and Ostrom — between despair and hope. It is to recognize that the open source commons is a real commons, facing real governance challenges, and that Ostrom's principles provide a framework for addressing those challenges.

The question is not *whether* the crate ecosystem will be governed. It is *when* and *how*. The answer to "when" is probably "after the next crisis." The answer to "how" is: with the principles that Ostrom gave us, adapted for the digital age.

The commons is not doomed. But it is not self-sustaining. It requires the same care, attention, and institutional investment that the code itself requires. The tragedy of the commons is not a fate. It is a warning. And warnings, unlike fates, can be heeded.

---

*Ostrom once said: "A core goal of public policy should be to facilitate the development of institutions that bring out the best in humans." The crate ecosystem brings out the best in developers — their generosity, creativity, and craft. The governance challenge is to build institutions that sustain this, before the tragedy arrives.*

---

### References

- Hardin, G. (1968). "The Tragedy of the Commons." *Science*, 162(3859), 1243-1248.
- Ostrom, E. (1990). *Governing the Commons: The Evolution of Institutions for Collective Action.* Cambridge University Press.
- Ostrom, E. (2005). *Understanding Institutional Diversity.* Princeton University Press.
- Ostrom, E. (2010). "Beyond Markets and States: Polycentric Governance of Complex Economic Systems." *American Economic Review*, 100(3), 641-672.
- Raymond, E.S. (1999). *The Cathedral and the Bazaar: Musings on Linux and Open Source by an Accidental Revolutionary.* O'Reilly Media.
- Nadia Eghbal (2020). *Working in Public: The Making and Maintenance of Open Source Software.* Stripe Press.
- Schweik, C.M. & English, R.C. (2012). *Internet Success: A Study of Open-Source Software Commons.* MIT Press.
- Kolstad, I. (2023). "Ostrom's Principles for Digital Commons." *Journal of Institutional Economics*, 19(4).
