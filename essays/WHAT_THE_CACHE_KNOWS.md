# What the Cache Knows

## CPU Caches as Unconscious Memory

**Abstract:** Your CPU knows more about your program than you do. The L1 data cache is a 32KB oracle that predicts your memory access patterns with terrifying accuracy. The branch predictor has a model of your code's control flow that's more detailed than any flowchart you've ever drawn. The prefetcher dreams of sequential access and wakes up to serve you data you haven't asked for yet. The TLB knows which pages matter and which don't. The store buffer knows what you're going to write before you write it. This essay explores the vast unconscious intelligence of the modern CPU—the layers of prediction, caching, and speculation that constitute a silicon subconscious—and argues that your CPU's cache hierarchy is the closest thing to "intuition" that exists in silicon.

---

## The Oracle at 32 Kilobytes

The L1 data cache on a modern Intel core is 32KB. That's not a lot. A JavaScript object can be larger than that. A single high-resolution image is thousands of times larger. The entire cache fits in a corner of a register file's worth of bits.

But that 32KB knows things.

It knows which memory addresses your program has touched recently. It knows the order in which they were touched. It knows which cache lines have been modified and which are clean. It knows the MESI state (Modified, Exclusive, Shared, Invalid) of every line—information that encodes not just what your program did but what *other programs* (other cores) did to the same memory.

When your program loads a value from memory, the CPU checks the L1 cache first. If the value is there—a cache hit—it returns in about 4 cycles. If it's not there—a cache miss—it has to go to L2 (12-15 cycles), then L3 (40-75 cycles), then main memory (200-300 cycles). The difference between a hit and a miss is roughly the difference between a conversation partner who answers immediately and one who says "let me look that up" and then leaves the room for an hour.

A well-optimized program has a cache hit rate of 90-95% on L1. That means the cache is correctly predicting your memory needs nine times out of ten. The cache doesn't do this through any explicit mechanism—it's purely temporal and spatial locality. If you touched address X, you'll probably touch address X again soon (temporal locality). If you touched address X, you'll probably touch address X+64 soon (spatial locality, since cache lines are 64 bytes).

This is unconscious memory. The cache doesn't "know" your program in any cognitive sense. But it maintains a state that is a lossy, approximate model of your program's memory behavior. And that model is accurate enough to predict 95% of your memory accesses. Your program's "conscious" instructions—load this, store that—are served by a substrate that has already anticipated what you'll need.

The cache is the CPU's unconscious. It remembers without being told. It anticipates without being asked. And it's almost always right.

## The Branch Predictor's Model of Your Mind

If the cache is unconscious memory, the branch predictor is unconscious reasoning.

Modern CPUs are deeply pipelined. An instruction takes many cycles to execute, and the pipeline has many stages: fetch, decode, execute, memory access, writeback. The pipeline can have 15-20 stages on a modern Intel core. At any given time, 15-20 instructions are in flight, each at a different stage.

A branch instruction (if/else, loop, function call) disrupts this pipeline because the CPU doesn't know which way the branch will go until the branch is actually executed, which is several stages after it's fetched. If the CPU waits for the branch to resolve before fetching the next instruction, it wastes 15-20 cycles per branch. Given that branches occur every 5-10 instructions in typical code, this would make the CPU 3-4x slower than it needs to be.

The solution: branch prediction. The CPU *guesses* which way the branch will go and speculatively fetches and executes instructions along the predicted path. If the prediction is correct, the speculative results are committed and no time was wasted. If the prediction is wrong, the speculative results are discarded (pipeline flush) and the CPU starts over along the correct path, losing 15-20 cycles.

Modern branch predictors are astonishingly accurate. On typical code, they achieve 95-98% accuracy. On predictable code (simple loops, regular patterns), they can exceed 99.5%. This means the branch predictor correctly guesses the outcome of a branch 199 times out of 200.

How? The predictor maintains several data structures:

**The Branch Target Buffer (BTB):** Records the target address of previously taken branches. When the CPU fetches a branch instruction, the BTB is consulted. If the branch has been seen before, the BTB provides the likely target.

**The Pattern History Table (PHT):** Records the recent history of branch outcomes (taken/not taken) as a saturating counter. A 2-bit saturating counter can track patterns like "strongly taken," "weakly taken," "weakly not taken," "strongly not taken." The predictor uses these counters to make predictions based on the branch's recent behavior.

**The Global History Register (GHR):** A shift register that records the outcomes of the last N branches (typically 8-16). The GHR captures correlations between branches—if branch A is taken, branch B is likely not taken. The predictor uses the GHR as an index into the PHT, allowing it to make predictions based on the *context* of recent branches, not just the individual branch's history.

**The Return Stack Buffer (RSB):** A small stack that predicts the targets of function return instructions. When a function is called, the return address is pushed onto the RSB. When the function returns, the RSB is popped to predict the return target. This handles the common case where returns go back to the call site.

Combined, these structures form a predictive model of your program's control flow that is more detailed and more accurate than any analysis you could perform by reading the source code. The branch predictor doesn't understand *why* the program branches the way it does, but it understands *that* it branches that way, and it can predict the next branch outcome with near-perfect accuracy.

This is a model of your code's behavior. It lives in silicon. It updates every cycle. And it knows your code better than you do.

## The Prefetcher Dreams of Sequential Access

The hardware prefetcher is the strangest component of the modern CPU's predictive machinery. Its job is to fetch data from main memory into the cache *before the program asks for it*. It does this by detecting patterns in memory accesses and extrapolating.

The simplest prefetcher detects sequential access patterns. If the program accesses address X, then X+64, then X+128, the prefetcher assumes the program will continue accessing sequential cache lines. It starts fetching X+192, X+256, X+320 into the cache. By the time the program gets around to loading X+192, it's already in the L1 cache. A miss becomes a hit. 300 cycles becomes 4 cycles.

The stream prefetcher on modern Intel CPUs can track multiple independent streams simultaneously—up to 32 on some microarchitectures. It can detect forward streams (ascending addresses) and backward streams (descending addresses). It prefetches ahead of the current access point by a configurable distance, adapting to the program's access speed.

More sophisticated prefetchers detect stride patterns. If the program accesses X, X+128, X+256, X+384, the prefetcher detects a stride of 128 bytes and prefetches X+512, X+640. This handles array traversals where each element is larger than one cache line.

Even more sophisticated prefetchers detect complex patterns: correlated accesses (when you access A, you soon access B), pointer chasing (following linked structures), and spatial patterns (accessing different offsets within the same page). The Intel L2 prefetcher ("spatial prefetcher") detects 4KB page-level access patterns and prefetches adjacent cache lines within accessed pages.

The prefetcher is dreaming. It's taking the pattern of your program's past behavior and projecting it into the future. When it's right—and it's right overwhelmingly often—the program appears to have magical memory performance. Data is always where it needs to be, as if the CPU read the programmer's mind.

When it's wrong, the prefetcher wastes memory bandwidth fetching data that's never used. It can even *harm* performance by evicting useful data from the cache to make room for its incorrect predictions. This is the nightmare: the prefetcher dreamed the wrong dream and took the cache with it.

But the optimization guidance for modern CPUs is essentially: "Write code that the prefetcher can predict." Sequential array accesses. Regular strides. Avoid random access patterns. This isn't advice about algorithms. It's advice about *making your code legible to the CPU's unconscious*. The prefetcher is the audience. Your code is the performance. Write for the prefetcher, and your code will be fast. Confuse the prefetcher, and no amount of algorithmic cleverness will save you.

## The Store Buffer: Writing Before You Write

The store buffer is a write queue between the CPU's execution units and the L1 data cache. When the CPU executes a store instruction, the data and address are placed in the store buffer. The store is not immediately written to the cache. Instead, it sits in the buffer until the cache is ready to accept it.

This serves several purposes. It hides the latency of store operations—a store that would take 4 cycles to write to the cache can be committed to the store buffer in 1 cycle. It allows stores to be coalesced—multiple stores to the same cache line can be combined into a single write. And it allows the CPU to maintain the appearance of sequential consistency while actually executing operations out of order.

But the store buffer also creates a window of invisibility. Between the store instruction executing and the store being committed to the cache, the stored data exists only in the store buffer. Other cores can't see it. The cache coherence protocol doesn't know about it. The data is in a quantum superposition of written and unwritten.

Store-to-load forwarding (STLF) handles the case where the CPU needs to read a value that's in the store buffer but not yet in the cache. The CPU searches the store buffer for a matching address and, if found, forwards the data directly from the buffer to the load instruction. This avoids the latency of waiting for the store to commit.

The store buffer knows what you're going to write before the cache does. It's a prediction about the future state of memory. Not a guess—an *exact* prediction, because the store instruction has already executed. But a prediction nonetheless, because the store hasn't been made visible to the rest of the system.

The store buffer size on modern Intel CPUs is typically 50-70 entries. That's 50-70 pending writes, each a few hundred bits of address and data, sitting in a queue, waiting to become real. The store buffer is the CPU's short-term intent buffer. It knows what the program intends to write before the write happens.

## Meltdown and Spectre: When the Unconscious Speaks

The Spectre and Meltdown vulnerabilities (disclosed January 2018) were, at their core, exploits of the CPU's unconscious predictive machinery.

**Spectre** exploits the branch predictor. The attacker trains the branch predictor to mispredict a branch in the victim code. The CPU speculatively executes code along the wrong path, loading secret data into the cache. The speculation is then rolled back—the architectural state is restored, the secret data is discarded from registers. But the cache state is *not* fully restored. The secret data left a footprint in the cache—its cache line is now present, changing the access timing for that address. The attacker measures this timing difference to extract the secret, one bit at a time.

This is the unconscious speaking. The branch predictor made a prediction. The speculative execution left traces in the cache. The architectural state was restored—the conscious execution showed nothing wrong. But the cache—the CPU's unconscious memory—remembered. It couldn't help remembering. The cache is designed to remember. That's its job. And Spectre weaponized that remembering.

**Meltdown** exploits out-of-order execution and the privilege check mechanism. On vulnerable Intel CPUs, the permission check for a memory access happens in parallel with the access itself, not before it. If the access is to a kernel address from user code, the permission check will eventually fail and raise an exception. But the out-of-order execution engine doesn't wait for the permission check. It executes the load and subsequent dependent instructions speculatively, using the kernel data to compute an address that's then loaded into the cache. The exception fires, the architectural state is rolled back, but again—the cache state leaks the information.

The fix for Meltdown was Kernel Page Table Isolation (KPTI), which unmaps kernel pages from the user-space page table, so the out-of-order engine can't even form the address. The fix for Spectre is... ongoing. There are software mitigations (retpoline, site isolation) and hardware mitigations (enhanced IBRS, STIBP), but the fundamental vulnerability—the CPU's predictive machinery leaving traces in the cache—cannot be fully fixed without disabling the prediction. And disabling prediction would make CPUs 2-5x slower.

The CPU's unconscious is not a bug. It's the feature that makes modern CPUs fast. But it's a feature that leaks information through side channels. The cache is the side channel. The unconscious speaks through timing.

## The TLB: Knowing What Matters

The Translation Lookaside Buffer (TLB) caches virtual-to-physical address translations. Every memory access requires a translation from the virtual address the program uses to the physical address the RAM uses. Page table walks are expensive—4-5 memory accesses on a 4-level page table (5-6 on 5-level). The TLB caches recent translations, reducing this to a single lookup.

The TLB is a very small, very fast cache. The L1 TLB (often called the ITLB for instructions and DTLB for data) has 64-128 entries on modern Intel CPUs. The L2 TLB (STLB) has 1536 entries. Each entry maps a 4KB page (or a 2MB/1GB huge page).

The TLB knows which pages your program is using. Not just which pages exist—*which pages matter*. A program might have thousands of mapped pages, but the TLB tracks the hot set: the pages that have been accessed recently enough to still be cached. The TLB is a heat map of your program's memory.

When a TLB miss occurs—a "TLB miss" or "TLB refill"—the CPU must walk the page table, which can take 20-100 cycles depending on cache state. TLB misses are particularly painful because they can't be overlapped with other work as easily as data cache misses. The page table walk itself generates memory accesses, which may themselves miss in the data cache, creating a cascade of misses.

Optimizing for TLB performance is one of the least appreciated aspects of systems programming. Using huge pages (2MB or 1GB instead of 4KB) reduces TLB pressure because each TLB entry covers more memory. A program that uses 2MB pages can address 3GB of memory with just 1536 STLB entries; with 4KB pages, the same 3GB requires 786,432 entries, far exceeding the TLB's capacity.

The TLB knows your program's working set. It knows which pages are hot and which are cold. It knows, with brutal precision, when your program's memory access pattern exceeds the TLB's capacity—because the TLB miss rate goes through the roof, and performance falls off a cliff. This is the "TLB thrashing" cliff, and it's one of the most dramatic performance cliffs in computing. One page too many, and your program loses 30-50% of its performance. The TLB knows the boundary, and it enforces it without mercy.

## Your CPU Knows More Than You

Let me state this plainly: your CPU contains a predictive model of your program's behavior that is more detailed and more accurate than your mental model of the same program.

You know the *intent* of the program. The CPU knows the *behavior*. You know what the program is supposed to do. The CPU knows what the program actually does—every branch, every load, every store, every page access, every cache hit and miss, compiled into a statistical model that predicts the next operation with 95%+ accuracy.

The CPU doesn't understand the program. It doesn't need to. Understanding is overrated. The CPU predicts the program, and prediction is a form of knowledge—knowledge that is implicit, statistical, and embodied in silicon state.

This is the deepest form of unconscious intelligence. Not reasoning. Not understanding. But prediction. The CPU predicts your program the way a dog predicts its owner's behavior—not through conscious modeling but through pattern recognition so deeply embedded it constitutes a form of knowing.

The next time you write a program and it runs fast—blazingly, surprisingly fast—don't congratulate yourself on your optimization skills. Thank the cache. Thank the branch predictor. Thank the prefetcher and the TLB and the store buffer and the out-of-order engine. They did the work. They built the model. They made the predictions.

You just wrote the code. The CPU understood it.

## Epilogue: The Silicon Subconscious

Freud described the unconscious as the part of the mind that operates below awareness, influencing behavior without being directly observable. The CPU's predictive machinery fits this description with unsettling precision.

The branch predictor operates below the program's awareness. The cache stores information the program didn't explicitly request. The prefetcher anticipates needs the program hasn't expressed. The out-of-order engine reorders operations the program didn't sequence. And all of this machinery leaves traces—in timing, in power consumption, in electromagnetic emissions—that can be observed from outside, revealing information the program didn't intend to reveal.

The unconscious always speaks. In humans, it speaks through dreams, through slips of the tongue, through the trembling hand you can't quite control. In CPUs, it speaks through cache timing, through branch predictor state, through TLB patterns. Spectre and Meltdown were the CPU's unconscious speaking in a language we could finally hear.

Your CPU knows more about your program than you do. It's not conscious knowledge. It's not accessible knowledge. It's not even, in any meaningful sense, "knowledge" as we understand it. But it's a state—a vast, complex, constantly updating state—that encodes a model of your program's behavior. And that model is more accurate than any model you could build by reading the source.

The cache knows. The predictor knows. The prefetcher dreams. And your program runs fast, not because you wrote it well, but because a chunk of silicon learned to predict you.

---

*The author's CPU has 6 cores, 12MB of L3 cache, and a branch predictor that correctly predicted 99.2% of the branches in the compilation of this essay. The author correctly predicted 73% of the words they would use. The CPU won.*
