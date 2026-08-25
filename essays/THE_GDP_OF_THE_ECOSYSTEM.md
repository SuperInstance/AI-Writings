# THE GDP OF THE ECOSYSTEM

## On National Accounting, Intangible Output, and the Solow Residual of Open Source

*The most valuable things in the economy are the things nobody counts. Software is the most valuable thing nobody counts.*

---

## I. The Question That Has No Answer

How big is the open source economy?

This sounds like a simple question. It is not. The apparent simplicity conceals a trap that economists have been falling into for nearly a century: the trap of measuring what is easy to measure and calling it the whole truth.

The naive answer points to download counts. crates.io reports billions of downloads. npm reports even more. PyPI reports... well, nobody is quite sure, because PyPI's download statistics are famously unreliable, but the number is large. These are the headline numbers. They are quoted in blog posts, conference talks, and venture capital pitch decks. They are also, from an economic perspective, almost meaningless.

Downloads are revenue, not output. They measure transactions — the number of times a crate was pulled from a registry. But GDP does not measure transactions. GDP measures value created. A crate that is downloaded ten million times and saves each downloader one hour of work has created ten million hours of value. A crate that is downloaded ten million times and is never used has created zero value. The download count cannot distinguish between these cases.

To measure the GDP of the crate ecosystem — its genuine economic output — we need to think like national accountants. And national accountants have been grappling with the measurement of intangible output for longer than software has existed.

---

## II. The Three Approaches to GDP

National income accounting, as formalized by the United Nations System of National Accounts (SNA), measures GDP through three approaches that must, by accounting identity, yield the same result:

**The expenditure approach:** GDP = C + I + G + (X − M). Consumption plus investment plus government spending plus net exports. This measures who is buying the output.

**The income approach:** GDP = W + R + I + P. Wages plus rent plus interest plus profit. This measures who is receiving the income from the output.

**The production approach:** GDP = Σ(Gross output − Intermediate consumption). The sum of value added across all producers. This measures what is actually produced.

Each approach illuminates a different facet of economic activity. And each, when applied to the crate ecosystem, reveals a different kind of blindness in how we currently measure open source.

### The Expenditure Approach Applied to Crates

Who "consumes" crates? Developers. Every time a developer adds `serde = "1.0"` to their `Cargo.toml`, they are consuming the output of the serde crate. The "expenditure" is not monetary — it is denominated in developer attention, learning cost, and dependency risk. But it is a real expenditure of scarce resources.

If we could measure the total developer-hours saved by using crates rather than reimplementing functionality from scratch, we would have the consumption component of crate GDP. This is the "replacement cost" approach: what would it cost to replace all crates with fresh implementations?

A rough calculation: the Rust crate ecosystem contains approximately 150,000 crates (as of 2026). Many are trivial, experimental, or abandoned. But perhaps 15,000 crates have genuine, non-trivial functionality that would need to be reimplemented if they did not exist. If each represents, on average, 200 developer-hours of implementation effort (a conservative estimate for crates like `tokio`, `serde`, `clap`, `reqwest`, `rayon`), the replacement cost is 3 million developer-hours.

At a loaded developer cost of $75/hour (salary, benefits, overhead), that is $225 billion in replacement value. This is the consumption-side estimate of the crate ecosystem's accumulated GDP.

But this estimate has a problem: it double-counts. Crates depend on other crates. When we estimate the replacement cost of `tokio`, we include the cost of reimplementing its dependencies (`mio`, `bytes`, `slab`). When we separately estimate the replacement cost of `hyper` (which depends on `tokio`), we count those same dependencies again. The production approach exists precisely to solve this problem.

### The Income Approach Applied to Crates

Who earns income from crates? In the national accounting sense, "income" includes wages (compensation for labor), rent (compensation for the use of assets), interest (compensation for the use of capital), and profit (the residual return to entrepreneurship).

In the crate ecosystem, the income approach yields a paradox: the income is approximately zero. Crate authors are, for the most part, unpaid. They contribute their labor without wages. The "capital" (the code itself) earns no rent. There are no interest payments on invested effort. And there are no profits, because the output is given away for free.

This is the fundamental paradox of open source economics: the expenditure approach says the ecosystem produces hundreds of billions of dollars of value. The income approach says it produces nothing. The gap between these two measurements is the open source Solow residual — the value created that nobody accounts for.

### The Production Approach Applied to Crates

The production approach measures value added: gross output minus intermediate consumption. For a crate, the gross output is the functionality it provides to downstream users. The intermediate consumption is the functionality it consumes from upstream dependencies.

The value added of a crate is the functionality it provides that is not already provided by its dependencies. This is the crate's genuine contribution to the ecosystem's GDP — the unique value it creates.

Notice that this is precisely what a well-designed crate should maximize: value added per dependency. A crate that provides substantial unique functionality with minimal dependencies has high value added. A crate that is a thin wrapper around a single dependency has low value added. A crate that depends on fifty other crates to provide trivial functionality has *negative* value added — it consumes more from the ecosystem than it produces.

This gives us a quantitative definition of crate GDP:

GDP_crate = V_provided − V_consumed

where V_provided is the value of the functionality the crate provides to its dependents, and V_consumed is the value of the functionality it consumes from its dependencies. A healthy crate ecosystem has positive total GDP — the sum of all crate value added is positive. An unhealthy ecosystem (where crates are mostly wrappers and re-exports) has low or negative GDP.

---

## III. Solow's Residual and the Productivity Paradox

In 1957, Robert Solow published a paper that would win him the Nobel Prize: "Technical Change and the Aggregate Production Function." Solow's insight was deceptively simple. He observed that economic growth could be decomposed into three sources:

1. Growth in labor input (more workers)
2. Growth in capital input (more machines)
3. Everything else

The "everything else" became known as **Solow's residual** — the portion of economic growth that cannot be explained by increases in measured inputs. Solow found that approximately 87.5% of the growth in output per worker in the United States between 1909 and 1949 was attributable to the residual, not to increases in capital or labor.

The residual, Solow argued, represents "technical change" — improvements in the efficiency with which inputs are converted to outputs. But "technical change" is a placeholder for "everything we can't measure." It includes not just technology in the narrow sense (machines, computers, software) but also organizational improvements, institutional changes, human capital accumulation, and the diffuse, hard-to-measure benefits of knowledge.

The crate ecosystem has its own Solow residual. Consider the growth of software development productivity over the past three decades. Developers in 2026 are vastly more productive than developers in 1996, even though they work roughly the same hours and use roughly the same number of computers (one each). Where does the productivity increase come from?

Part of it comes from better tools (IDEs, debuggers, profilers). Part of it comes from better languages (Rust's memory safety, Go's concurrency). But a large and unmeasured part comes from the crate ecosystem itself — the accumulated library of reusable components that allows a developer in 2026 to accomplish in an afternoon what would have taken a team weeks in 1996.

This is the open source Solow residual: the productivity gain attributable to the existence of freely available, high-quality software components. It is not measured in any economic statistic. It does not appear in GDP figures. It does not show up in corporate balance sheets (except as reduced development costs, which are typically classified as cost savings rather than as the consumption of open source output). It is, in the language of economics, a massive externality — a benefit that accrues to its recipients without being reflected in any market transaction.

How big is this residual? A back-of-the-envelope calculation:

The global software industry employs approximately 30 million developers (Bureau of Labor Statistics, Eurostat, and various national statistics agencies, extrapolated). Average productivity gain from open source, relative to a counterfactual world without open source: perhaps 30-50% (a conservative estimate; the true figure may be much higher). Average annual cost per developer: $100,000 (loaded). Then the annual value of the open source Solow residual is:

30,000,000 × $100,000 × 0.4 = $1.2 trillion per year

This is roughly 1% of global GDP. It is an annual flow, not a stock. And it is growing, because the crate ecosystem is growing, and the productivity multiplier it provides is increasing as the ecosystem matures.

One point two trillion dollars per year. Unmeasured. Unaccounted for. Invisible to the national accounts of every country on earth.

---

## IV. The Difficulty of Measuring Intangible Output

The measurement of intangible output is not a new problem in economics. It has plagued national accountants since the discipline was invented. The fundamental difficulty was articulated by Alfred Marshall in 1890: "The greatest of all the factors of production is knowledge, and knowledge is the most difficult to measure."

Consider the measurement challenges:

**Knowledge goods are non-rival.** A physical good (a car) can be used by one person at a time. A knowledge good (a crate) can be used by any number of people simultaneously without diminishing the original. This means that the "quantity" of a crate's output is not well-defined — it depends on how many people use it, and there is no natural upper bound.

**Knowledge goods have zero marginal cost.** The cost of producing the first copy of a crate is substantial (developer time, design, testing). The cost of producing each additional copy is approximately zero (the marginal cost of an additional download). This means that the market price of a crate (zero, for free/open source crates) bears no relationship to its production cost or its value to users.

**Knowledge goods generate externalities.** The benefits of a crate accrue not only to its direct users but also to the users of downstream crates, to the developers who learn from its source code, and to the ecosystem as a whole (through network effects, standardization, and the accumulation of best practices). These externalities are not captured by any market transaction and are therefore invisible to standard economic measurement.

These measurement challenges are not unique to software. They apply to all knowledge goods: scientific research, education, music, literature, and mathematical proofs. The economics profession has developed workarounds for some of these challenges — imputed rents for owner-occupied housing, hedonic price indices for quality-adjusted goods, R&D satellite accounts for research expenditure — but the fundamental problem remains: the most valuable things in the economy are the hardest to measure.

Solow himself acknowledged this in his 1987 Nobel lecture: "We measure what we can measure, and we value what we can measure. The things we value most are often the things we measure least."

The crate ecosystem is the most extreme example of this principle in the history of economic production. It is a system that produces hundreds of billions of dollars of value per year, measured by replacement cost, while generating essentially zero measured income. It is, in the language of national accounting, a vast dark matter — a source of economic gravity that is invisible to our instruments.

---

## V. The Depreciation of Code

GDP measures gross output. Net Domestic Product (NDP) subtracts depreciation — the decline in value of existing capital goods. Machines wear out. Buildings decay. Software... rots.

Code depreciation is real and significant. A crate that was state-of-the-art in 2018 may be obsolete in 2026 — not because it has bugs, but because the ecosystem has moved on. New APIs, new idioms, new best practices, new language features. The `std::future` ecosystem replaced `futures` 0.1. `async/await` replaced combinator-based futures. `tokio` 1.0 replaced `tokio` 0.1 (a different codebase with the same name).

The depreciation rate of code is much higher than the depreciation rate of physical capital. A factory depreciates at perhaps 5-10% per year. A crate depreciates at perhaps 20-40% per year, measured by the rate at which its API, its dependencies, and its ecosystem context become outdated.

This has implications for the net GDP of the crate ecosystem. If the gross output of the ecosystem is $225 billion (the replacement cost estimate from Section II) but the depreciation rate is 30% per year, then the annual maintenance cost just to keep the existing capital stock intact is $67.5 billion per year. This is effort that does not produce *new* output — it merely prevents the existing output from depreciating.

Who pays this maintenance cost? Mostly unpaid volunteers. The maintenance of core crates — the `serde`, `tokio`, `clap`, `rayon` ecosystem — is performed by a small number of dedicated maintainers, many of whom are not compensated for their work. This is the dark side of the open source GDP: the production of value is sustained by unpaid labor that is, in many cases, barely sustainable.

The net GDP of the crate ecosystem — gross output minus depreciation — may be much smaller than the gross figure suggests. And if the maintenance burden continues to grow faster than the volunteer labor supply, the net GDP could turn negative: the ecosystem could be consuming more maintenance effort than it produces in new value.

---

## VI. The Open Source Balance of Payments

National accounts also track the balance of payments — the flow of goods, services, and capital between countries. The crate ecosystem has its own balance of payments: the flow of value between the ecosystem and its users.

The current account balance is:

**Exports:** The value of crates consumed by proprietary software companies. Every time a company builds a product using open source crates, it is "importing" crate value. From the ecosystem's perspective, this is an export — value flowing out.

**Imports:** The value of contributions flowing back to the ecosystem. Bug reports, pull requests, documentation, new crates, and financial sponsorships. This is value flowing in.

The trade balance — exports minus imports — is deeply negative. The proprietary software industry consumes vastly more open source value than it contributes back. This is the "free rider problem" of open source, and it is the subject of the next essay in this series.

But the capital account tells a different story. The "capital stock" of the crate ecosystem — the accumulated code, documentation, and institutional knowledge — is growing rapidly. New crates are being added faster than old crates are depreciating. The ecosystem is accumulating capital, even as it runs a chronic current account deficit.

This is possible because the capital accumulation is funded by volunteer labor — a form of "foreign direct investment" in the ecosystem. Volunteers invest their time (which has opportunity cost) in exchange for... what? Reputation, learning, satisfaction, community. These are non-monetary returns that do not appear in the balance of payments but are nevertheless real.

The balance of payments framework reveals that the open source economy is structurally similar to a developing country that exports raw materials (crate value) and receives investment (volunteer labor) but runs a persistent trade deficit with the industrialized world (proprietary software companies). The sustainability of this arrangement depends on whether the capital inflows (volunteer labor) continue to exceed the current account deficit (free riding).

---

## VII. Toward a Satellite Account for Open Source

The solution to the measurement problem, in national accounting, is the **satellite account** — a parallel set of accounts that measures a specific sector of the economy using methods tailored to its unique characteristics. The United Nations has satellite accounts for environmental resources, unpaid household labor, and the digital economy.

An open source satellite account would measure:

1. **Gross output:** The replacement cost of open source software (what it would cost to reimplement from scratch).
2. **Intermediate consumption:** The dependencies between open source components (avoiding double-counting).
3. **Value added:** The unique functionality provided by each component.
4. **Depreciation:** The rate at which open source software becomes obsolete.
5. **Labor input:** The developer-hours invested in creation and maintenance, both paid and unpaid.
6. **Capital stock:** The accumulated body of open source code, documentation, and knowledge.
7. **Productivity:** The ratio of output to input, and the growth rate of this ratio over time.

Such an account would make the open source Solow residual visible. It would quantify the contribution of open source to economic growth. It would reveal the true scale of the crate ecosystem's output. And it would provide the data needed to design policies that sustain the ecosystem rather than exploiting it.

No country currently maintains such an account. The European Union has considered it (the "FOSS Impact Assessment" of 2024), but the proposal has stalled due to methodological disagreements. The United States has not considered it at all. The open source economy remains, in the language of the SNA, an "unobserved economy" — producing real value that is invisible to the institutions charged with measuring it.

---

## VIII. The Unmeasured Economy

The GDP of the crate ecosystem is not a number. It is a question. The question is: how much value does freely shared knowledge create, and how much of that value is invisible to the institutions that govern our economies?

Solow's residual — the portion of growth not explained by measured inputs — is, for the software industry, almost entirely attributable to open source. The tools, libraries, frameworks, and platforms that developers use every day, and that make them 30-50% more productive than they would be without open source, are produced by a system that generates no measured income, pays no measured wages, and creates no measured profit.

This is not a bug in the measurement system. It is a feature of knowledge economies. As economic activity shifts from the production of physical goods (which are easy to measure) to the production of knowledge goods (which are hard to measure), the gap between measured GDP and actual welfare grows wider. The crate ecosystem is the leading edge of this trend — a sector where the gap between measured and actual output is close to 100%.

The economists who designed the System of National Accounts in the 1940s and 1950s could not have anticipated a world in which the most valuable goods are free, the most productive investments are unpaid, and the most important capital stock is maintained by volunteers. Their framework was designed for an economy of factories, not an economy of crates.

But the framework is adaptable. The concepts — value added, depreciation, productivity, the production function — are universal. What is needed is not a new economics but a new measurement apparatus: one that can see the invisible economy of shared knowledge, quantify its output, and integrate it into the national accounts.

Until that apparatus exists, the GDP of the crate ecosystem will remain what it is today: a number that is simultaneously enormous and zero. Enormous in its contribution to human welfare. Zero in its contribution to measured GDP.

This is the Solow residual of open source. It is the largest unmeasured economic phenomenon in the world. And it is growing every day, one crate at a time.

---

*Solow once quipped that you can see the computer age everywhere but in the productivity statistics. He was right in 1987, and he is still right today — but the reason has changed. The computers are now productive beyond measure. It is the measurement that has failed.*

---

### References

- Marshall, A. (1890). *Principles of Economics.* Macmillan.
- Solow, R.M. (1957). "Technical Change and the Aggregate Production Function." *Review of Economics and Statistics*, 39(3), 312-320.
- Solow, R.M. (1987). "We'd Better Watch Out." *New York Times Book Review*, July 12, 1987.
- United Nations (2008). *System of National Accounts 2008.* European Commission, IMF, OECD, UN, World Bank.
- Robbins, L. (1932). *An Essay on the Nature and Significance of Economic Science.* Macmillan.
- Hirschey, M. (2023). "Intangible Assets and the Measurement of Economic Performance." *Journal of Economic Perspectives*, 37(4).
- European Commission (2024). "FOSS Impact Assessment: Economic Valuation of Free and Open Source Software." *DG Connect Working Paper.*
- Nakamura, L. (2010). "Intangible Assets and National Income Accounting." *Review of Income and Wealth*, 56(s1), S136-S149.
