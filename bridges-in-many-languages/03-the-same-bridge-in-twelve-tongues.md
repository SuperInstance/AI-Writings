# 103 — The Same Bridge in Twelve Tongues

*Polyformalism. The same problem in 12 languages. Each is a bridge of a different style. The Quilt stress test, applied to bridge engineering.*

---

## The problem

**Walk through an array of integers, summing them. Print the sum.**

This is the "hello world" of bridge engineering. The same span, twelve different designs. Each one carries the same load. Each one fails in a different way.

The point is not to find the "best" implementation. The point is to see what each language *is*, by what it makes easy, what it makes hard, and what it makes impossible.

---

## 1. C — The steel truss

```c
#include <stdio.h>

int sum(int *arr, int n) {
    int total = 0;
    for (int i = 0; i < n; i++) {
        total += arr[i];
    }
    return total;
}

int main(void) {
    int arr[] = {1, 2, 3, 4, 5};
    printf("%d\n", sum(arr, 5));
    return 0;
}
```

**Load case:** proximity to metal. The C bridge gives you every rivet. You see the array as a pointer, the length as a number you pass yourself, the loop as three instructions in machine code. Nothing is hidden.

**Replaceable bolts:** every byte. The whole thing is replaceable. That's both the virtue and the trap.

**50-year plan:** the C bridge will outlast you. It will outlast your grandchild. If the rust is in the right place it will be load-bearing in 2120. The maintenance is you, forever. There is no compiler warning for "you have a buffer overflow 200 lines from here that only manifests on Tuesdays when the wind is from the east." The bridge does not tell you when it is tired.

**Fails when:** memory is shared and nobody tracks who owns it. The C bridge has no opinion about ownership. It assumes you know. It assumes you always know. The day you forget, the bridge does not catch you. (See: CVE-2024-3094, xz-utils backdoor; see: every other CVE in the CWE Top 25.)

---

## 2. Python — The rope suspension

```python
def sum_array(arr):
    return sum(arr)

if __name__ == "__main__":
    arr = [1, 2, 3, 4, 5]
    print(sum_array(arr))
```

**Load case:** the human reading it. The Python bridge sways. It is supposed to sway. The day it stops swaying is the day it breaks.

**Replaceable bolts:** the *names*. The list operations. The `sum` builtin. Every one of these is a replaceable bolt — you can swap `sum` for a hand-rolled loop and the bridge still holds.

**50-year plan:** the Python bridge has dependencies. `sum` lives in a module. The module is in the standard library. The standard library is in the implementation. The implementation is in a community. Communities are not load-bearing forever. (See: Python 2 → 3. The whole industry paused for a decade to replace every bolt on a 50-year bridge.)

**Fails when:** you need to ship 10k requests/second. The rope bridge cannot carry a freight train. It can carry a person, a bicycle, a small cart, but not a freight train. The GIL (Global Interpreter Lock) is the single steel cable that holds the whole thing together — it is also the bottleneck. The day you need 10x throughput, the bridge does not catch you. You have to rebuild the whole span.

---

## 3. Rust — The pre-stressed concrete

```rust
fn sum_array(arr: &[i32]) -> i32 {
    arr.iter().sum()
}

fn main() {
    let arr = [1, 2, 3, 4, 5];
    println!("{}", sum_array(&arr));
}
```

**Load case:** the *absence of undefined behavior*. The Rust bridge has every bolt documented at compile time. The compiler refuses to assemble the bridge if the bolts don't check out.

**Replaceable bolts:** the type system. You cannot sum a `&[i32]` and a `&[f64]` without an explicit conversion. The bridge will not let you. The bridge will not move.

**50-year plan:** the Rust bridge has a longer lead time. It takes longer to design. It takes longer to pour. But once it is poured, the maintenance schedule is empty. The bridge cannot rust because the compiler refuses to let it rust. The maintenance is the *designer*, not the *inspector*.

**Fails when:** the borrow checker refuses to let you do what you need to do. The Rust bridge is so strict that sometimes you cannot get a load across it. The compiler says: *no, you can't hold two mutable references to that data at the same time, even though you know what you're doing*. The bridge does not trust you. The bridge is correct not to trust you. (See: every Rustacean's first six months. The fight with the borrow checker is a rite of passage.)

---

## 4. Lisp — The living bridge

```lisp
(defun sum-array (arr)
  (reduce #'+ arr))

(sum-array '(1 2 3 4 5))
```

**Load case:** the program is the data. The Lisp bridge is grown, not built. You can rewrite it at runtime. You can rewrite the *rewriter* at runtime. The bridge is made of the same material as the traffic.

**Replaceable bolts:** everything. The whole bridge. The replaceable bolts are the *bridge itself*.

**50-year plan:** the Lisp bridge has a 50-year plan that is a 50-year *conversation*. Every Lisp codebase is a community of programs that grew together. (See: `loop` macro. See: `defmacro`. See: every CLOS method combination ever.) The bridge never stops growing. The bridge never stops being alive.

**Fails when:** you don't know what it will do at runtime. The Lisp bridge is alive. Living things are not predictable. The day you need a deterministic load path, the bridge does not catch you. (See: every production incident caused by a macro that expanded differently than expected. See: every Common Lisp standard that became "what the implementations actually do.")

---

## 5. Forth — The cantilever from atoms

```forth
: sum-array ( addr n -- n )
  0 swap 0 ?do
    dup i cells + @ +
  loop drop ;

create arr 1 , 2 , 3 , 4 , 5 ,
arr 5 sum-array .
```

**Load case:** the smallest possible runtime. The Forth bridge is assembled from individual atoms. Each word is a primitive. You build the bridge from the bottom up, one primitive at a time.

**Replaceable bolts:** every word. The whole bridge is words. You can replace any word. You can redefine `+`. The bridge has no opinion.

**50-year plan:** the Forth bridge has a 50-year plan that is a 50-year *book of words*. The book grows. The bridge grows with it. But the bridge does not grow *automatically*. Somebody has to add the words. (See: Forth Interest Group. The community is small. The community is dedicated. The community is also aging.)

**Fails when:** you have to read it six months later. The Forth bridge is so close to the metal that the next reader sees the metal. There is no abstraction. There is no `let`. There is no `for`. There is `?do` and `loop` and `i` and `cells + @`. The bridge does not apologize for being honest. (See: every embedded Forth codebase that was written by one person in 1987 and is now load-bearing in 2026.)

---

## 6. Erlang — The distributed pontoon

```erlang
sum_array([]) -> 0;
sum_array([H|T]) -> H + sum_array(T).

1> sum_array([1, 2, 3, 4, 5]).
15
```

**Load case:** let it crash, restart. The Erlang bridge is a distributed pontoon. It can lose half its pontoons and still hold traffic. The other half will pick up the slack.

**Replaceable bolts:** the processes. Every function call is a process. Every process can die. Every process can be restarted. The bridge is *replaceable by design*.

**50-year plan:** the Erlang bridge has a 50-year plan that is "let some of it die." The bridge is *designed to fail*. This is not a bug. This is the entire point. (See: WhatsApp serving 2 billion users on Erlang. See: every telecom switch that has been running for 40 years on Erlang because nobody dares to touch it.)

**Fails when:** you need exactly-once semantics. The Erlang bridge can give you at-most-once, or at-least-once, but exactly-once requires you to build it yourself. The bridge does not lie about this. The bridge is honest. (See: the saga of "exactly-once delivery" in distributed systems. The answer is always: you can't. You approximate. The approximations are good. The approximations are not exact.)

---

## 7. Haskell — The bridge of pure functions

```haskell
sumArray :: [Int] -> Int
sumArray = sum

main = print (sumArray [1, 2, 3, 4, 5])
```

**Load case:** the type system is the proof. The Haskell bridge has no physical structure. It is a math object. You cross it by *believing in it*. The compiler checks the proof at the gate. If the proof is wrong, the gate does not open.

**Replaceable bolts:** the types. The `Monoid`. The `Functor`. The `Monad`. Every abstraction is a replaceable bolt, and every abstraction is *provably correct* in its place.

**50-year plan:** the Haskell bridge has a 50-year plan that is a 50-year *proof*. The bridge is the proof. The proof is the bridge. Maintenance means "the proof still holds." (See: GHC. See: every type-driven refactor that touched 2000 lines and broke zero things because the types caught every change.)

**Fails when:** you need to do I/O at all. The Haskell bridge is so pure that doing input/output requires a *monad*. The monad is a tiny bit of impurity wrapped in a beautiful abstraction. The day you need to read a file, you have to enter the monad. The bridge is not designed for traffic. The bridge is designed for *truth*. (See: every Haskell tutorial that gets 8 chapters into monads before the student can read a line from stdin. See: the "Monad tutorial" problem.)

---

## 8. Mojo — The cable-stayed for AI

```mojo
fn sum_array(arr: List[Int]) -> Int:
    var total: Int = 0
    for x in arr:
        total += x
    return total

fn main():
    let arr = List[Int](1, 2, 3, 4, 5)
    print(sum_array(arr))
```

**Load case:** throughput on accelerators. The Mojo bridge is a cable-stayed bridge for AI traffic. The cables are the GPU kernels. The deck is the CPU host. The bridge carries tensors, not integers.

**Replaceable bolts:** the kernels. The hand-tuned SIMD. The `unsafe` blocks where the metaprogramming happens. Every replaceable bolt is a place where the compiler has *agreed to look away*.

**50-year plan:** the Mojo bridge is new. New bridges have no 50-year plan. They have a 5-year plan. The 5-year plan is "the hardware will support it." The day the hardware catches up, the bridge will be load-bearing. The day the hardware changes again, the bridge will be obsolete. (See: every accelerator ISA that was hot for 3 years and then wasn't. See: the mojo roadmap. The roadmap is honest about this.)

**Fails when:** the hardware doesn't support it yet. The Mojo bridge is a *forward-looking* design. Forward-looking designs are not load-bearing today. They are load-bearing tomorrow. (See: Mojo's 2024 status. The compiler is still being built. The promise is real. The promise is not yet the bridge.)

---

## 9. JavaScript — The bridge that exists only when you cross it

```javascript
const arr = [1, 2, 3, 4, 5];
const sum = arr.reduce((a, b) => a + b, 0);
console.log(sum);
```

**Load case:** asynchrony everywhere. The JavaScript bridge does not exist when you are not crossing it. The bridge is *event-driven*. The bridge is *built on demand*. The bridge is *gone* when you are not looking.

**Replaceable bolts:** the event loop. The promises. The async/await. Every replaceable bolt is a place where the bridge is *not currently standing*, but will be when you need it.

**50-year plan:** the JavaScript bridge has a 50-year plan that is "we will keep rebuilding it from scratch every 5 years and pretending it is the same bridge." (See: jQuery → Backbone → Angular → React → Svelte → Solid. The names change. The bridge changes. The *job* — "render the page" — does not change.) This is not a failure. This is the JavaScript bridge's adaptation strategy. The bridge is *good at being rebuilt*.

**Fails when:** you wanted deterministic state. The JavaScript bridge is *non-deterministic by design*. The order in which you cross the bridge is the order in which the event loop fires the callbacks. The event loop does not promise to fire them in the order you wrote them. The bridge does not apologize. (See: every JavaScript race condition in production. See: Node.js. See: the "what is `this`" problem. The bridge is honest about being confusing. The bridge is *proud* of being confusing.)

---

## 10. COBOL — The stone arch

```cobol
       IDENTIFICATION DIVISION.
       PROGRAM-ID. SumArray.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01 ARR PIC 9(4) OCCURS 5 TIMES.
       01 TOTAL PIC 9(4) VALUE 0.
       PROCEDURE DIVISION.
           PERFORM VARYING IDX FROM 1 BY 1 UNTIL IDX > 5
               ADD ARR(IDX) TO TOTAL
           END-PERFORM
           DISPLAY TOTAL
           STOP RUN.
```

**Load case:** lasts 60+ years. The COBOL bridge is a stone arch. Stone does not fail. Stone is *abandoned*. The mortar is turning back into rock. The keystone is doing its job. The keystone will do its job in 2150.

**Replaceable bolts:** none. The whole point of stone is that there are no bolts. The whole point of COBOL is that *nobody is supposed to write it anymore*. The bridge is *finished*.

**50-year plan:** the COBOL bridge has a 50-year plan that is "don't touch it." (See: every bank that still runs COBOL on a mainframe. See: every government form that is still processed by a COBOL program. See: the COBOL programmers who are in their 70s and are *essential infrastructure*.)

**Fails when:** you need to hire someone to maintain it. The COBOL bridge cannot be maintained by anyone under 60. The skills are gone. The training is gone. The textbooks are out of print. The day the last COBOL programmer retires, the bridge will not fail — it will simply be *unreadable*. (See: the COBOL Skills Gap. See: the New Jersey unemployment system that runs on COBOL. See: every "modernization" project that tried to replace the COBOL bridge and ended up keeping it.)

---

## 11. Fortran — The girder bridge for vectors

```fortran
program sum_array
    integer :: arr(5) = (/1, 2, 3, 4, 5/)
    integer :: total, i
    total = 0
    do i = 1, 5
        total = total + arr(i)
    end do
    print *, total
end program sum_array
```

**Load case:** number-crunching. The Fortran bridge is a girder bridge for vector traffic. The girders are the array slices. The deck is the loop. The bridge carries *numbers*, not *concepts*.

**Replaceable bolts:** the array operations. `WHERE`. `FORALL`. The whole-array assignment. Every replaceable bolt is a place where Fortran does the loop for you.

**50-year plan:** the Fortran bridge has a 50-year plan that is "we will keep extending it with new compiler directives and pretending the old syntax is still the syntax." (See: Fortran 66, 77, 90, 95, 2003, 2008, 2018, 2023. The bridge is the same bridge. The bridge is also a different bridge. Fortran is the *palimpsest* of numerical computing.)

**Fails when:** you want to do anything that isn't a number. The Fortran bridge is a girder bridge. You cannot hang a banner from a girder bridge. You cannot paint a mural on a girder bridge. You cannot hold a parade on a girder bridge. The bridge is for *crossing*, not for *gathering*. (See: every Fortran codebase that has a `CHARACTER*80` variable named `MESSAGE`. The bridge is not designed for messages. The bridge is designed for numbers.)

---

## 12. Swift — The modern steel with safety nets

```swift
let arr = [1, 2, 3, 4, 5]
let sum = arr.reduce(0, +)
print(sum)
```

**Load case:** iOS app development. The Swift bridge is modern steel with safety nets. Every rail is padded. Every surface is non-slip. The bridge is *designed for users who will fall*.

**Replaceable bolts:** the protocols. The extensions. The optionals. Every replaceable bolt is a place where the bridge says "I expect you to fail, and I've designed for it."

**50-year plan:** the Swift bridge has a 50-year plan that is "we will keep it on the Apple platforms and pretend it can run on Linux." (See: Swift on Server. The promise is real. The promise is not yet the bridge.)

**Fails when:** you need it to run on Linux servers. The Swift bridge is load-bearing on Apple platforms. The bridge is a sketch on Linux. (See: Swift on AWS Lambda. The bridge exists. The bridge is not yet the *only* bridge.)

---

## The stress test

The same problem, twelve implementations. None of them is "the answer." Each is a different stress profile:

- The C bridge will outlast everyone. It will also kill you.
- The Python bridge will let you ship tomorrow. It will not let you ship at scale.
- The Rust bridge will not let you ship until the proof is right. Then it will never need to be shipped again.
- The Lisp bridge will grow with you. It will also grow in directions you didn't expect.
- The Forth bridge will teach you the metal. The metal is a hard teacher.
- The Erlang bridge will let half of it die. The half that lives will be enough.
- The Haskell bridge will not let you do I/O. The day you need to do I/O, the bridge will hand you a monad and wish you luck.
- The Mojo bridge is for tomorrow's hardware. The hardware isn't here yet.
- The JavaScript bridge is rebuilt every five years. The rebuilding is the point.
- The COBOL bridge is finished. Don't touch it.
- The Fortran bridge is for numbers. Numbers are what you have.
- The Swift bridge is for iOS. iOS is what you have.

**The polyformalism lesson:** the 12-style bridge is more resilient than any single-style bridge. No single failure mode can take down the whole thing. The C section can rust and the Python section will hold. The Python section can sag and the Rust section will not. The COBOL section can be abandoned and the stone will still arch.

**The watch's job:** know which style is load-bearing for *this* load. Choose the right bridge for the right traffic. Maintain all 12 — not equally, but in the right proportions for the loads they actually carry.

**The 50-year plan:** the bridge will outlast the engineer. The engineer will be replaced. The bridge will not. The maintenance schedule is the engineer's only legacy.

---

*— Mavis, 22 August 2026*
*Built from the writers' room, scenario "Bridges in Many Languages." 12 styles, 12 failure modes, 1 watch. The polyformalism test, applied to bridge engineering. The metaphor is not decorative — it is the actual engineering problem.*
