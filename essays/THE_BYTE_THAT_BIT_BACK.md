# The Byte That Bit Back

## A History of Security Vulnerabilities Told Through Individual Bytes

**Abstract:** Every catastrophic security failure begins with something small. An off-by-one error. A null byte where there shouldn't be one. A sign bit that should have been zero. A single byte, in the wrong place, at the wrong time, with the wrong semantics, and the entire edifice comes crashing down. This essay traces the history of computer insecurity through the stories of individual bytes—the bits that flipped, the signs that were wrong, the bounds that weren't checked—and argues that every byte in a running program is a loaded gun. Most of the time it points at nothing. But sometimes, in the right (wrong) hands, it points at root.

---

## The Off-by-One That Owned the Internet

CVE-2001-0149. WU-FTPD, the Washington University FTP server. The version of FTP server that was running on, by some estimates, 60% of the internet's FTP servers in the late 1990s and early 2000s.

The bug was in the handling of the `SITE EXEC` command, which allowed remote execution of commands—a feature that should never have existed but did because the 1990s were a lawless hellscape. The specific issue was a buffer overflow in the command parsing, but the interesting part is the *mechanism*: an off-by-one error.

An off-by-one error is the simplest possible mistake. You allocate `N` bytes. You write `N+1` bytes. The last byte goes one past the end of the buffer. In C, this is undefined behavior. In practice, on the stack layouts of the late 1990s, that one extra byte overwrote the least significant byte of the saved frame pointer on the stack.

One byte. Eight bits. 256 possible values. And with those 256 values, an attacker could redirect the function's return address by up to 255 bytes in either direction. Given that the buffer itself was on the stack, an attacker could fill it with shellcode and then use the one-byte overwrite to point the return address *into that shellcode*.

The exploit was publicly released in 2000. Within weeks, thousands of FTP servers were compromised. The real damage came from the fact that FTP servers often ran as root (because the 1990s were a lawless hellscape, I cannot emphasize this enough), so remote code execution meant immediate root access. One byte. Root. The entire internet.

The fix was one line: change `<=` to `<`. One character. The difference between "less than or equal to" and "less than." The difference between a secure server and a compromised one. The difference between a good day and the worst day of a system administrator's life.

This is the byte that bit back. Not a sophisticated vulnerability. Not a zero-day discovered by a nation-state research team. A `<=` that should have been `<`. A single byte of overwrite. And root.

## The Null Byte That Broke Everything

PHP, circa forever. The language that keeps giving (vulnerabilities, that is).

In C, strings are null-terminated. A null byte (`0x00`) marks the end of a string. PHP, being implemented in C, inherits this convention. But PHP's higher-level string representation uses explicit lengths, not null termination. A PHP string can contain null bytes.

This mismatch—C uses null termination, PHP uses length—created a class of vulnerabilities known as "null byte injection." The canonical example: PHP's `include()` statement, used to include and execute files. If a PHP program takes user input and passes it to `include()` with some suffix appended:

```php
include($_GET['page'] . '.php');
```

The intention is clear: only `.php` files can be included. The attacker sends `page=../../etc/passwd%00`. The `%00` is a URL-encoded null byte. PHP's string is `../../etc/passwd\0.php`. But when this string is passed to the C-level `fopen()` call, C sees the null byte as the end of the string. It opens `../../etc/passwd`. The `.php` suffix is invisible to C.

One null byte. The entire access control model of a PHP application—assuming the file ends in `.php`—evaporated. This bug pattern affected not just `include()` but `fopen()`, `file_get_contents()`, `copy()`, `rename()`, and virtually every PHP function that operates on filenames. For years. Across thousands of applications.

The byte was `0x00`. Eight zero bits. The absence of a signal. And in that absence, entire security models collapsed. The null byte didn't do anything. That's exactly why it was dangerous. It made the C runtime *stop reading*. It created a boundary that the higher-level language didn't believe in. The null byte is the serpent in the garden of string handling—it whispers "this is the end," and the C runtime believes it, even though the PHP runtime knows it isn't.

PHP eventually fixed this by checking for null bytes in filename arguments and rejecting them. The fix took years. The null byte had been biting back since the beginning.

## The Sign Bit That Crashed a Rocket

Ariane 5. Flight 501. June 4, 1996. Thirty-seven seconds after launch, the rocket veered off course and disintegrated. The cause: an unhandled exception in the inertial guidance system.

The exception was an integer overflow. A 64-bit floating-point value representing the rocket's velocity was being converted to a 16-bit signed integer. The value was larger than 32767, the maximum value of a 16-bit signed integer. The conversion failed. The Ada runtime raised an exception. The exception was not caught. The guidance system crashed. The backup guidance system—which was running the same software—crashed in the same way. The rocket had no guidance. It tried to correct for a phantom trajectory deviation that resulted from garbage data produced by the crash. The correction was extreme. The rocket broke apart.

Cost: $370 million. Cause: one sign bit.

Well, not exactly one sign bit. The 16-bit signed integer has a sign bit. The 64-bit float value that was being converted didn't fit in the range [-32768, 32767]. The most significant bit—the sign bit of the 16-bit representation—was being used to represent magnitude, not sign. The value wasn't negative. It was just too positive.

But the narrative is cleaner if I blame the sign bit, and the narrative isn't entirely wrong. The decision to use a *signed* 16-bit integer for a velocity value was a design choice that halved the representable range. An unsigned 16-bit integer would have handled values up to 65535, potentially avoiding the overflow. The sign bit—the one bit dedicated to representing negativity—was the bit that wasn't available for representing the rocket's actual velocity.

Why was the code converting to a 16-bit integer at all? Because the code was reused from Ariane 4. On Ariane 4, the velocity values were smaller. On Ariane 5, which was faster and had a different trajectory, the values were larger. The code was never revalidated for the new flight profile because, reportedly, the engineers assumed the code was correct—after all, it had worked on Ariane 4.

The sign bit assumed values would fit in a signed 16-bit range. The rocket disagreed. The rocket won.

One bit. The sign bit. The assumption that a velocity would be small enough to fit in 15 bits of magnitude. An assumption that cost $370 million and destroyed a decade of engineering work. The sign bit bit back.

## The Integer Overflow That Gave Root

CVE-2009-1895. Linux kernel, versions before 2.6.30. The `pipe_buffer` structure had a signed integer used to represent the buffer count. The `pipe` system call created a pipe with a certain number of buffers, and the count was stored as an `int`.

The vulnerability: the kernel didn't properly validate the buffer count before using it for memory allocation. A specially crafted sequence of operations could cause the count to become negative (interpreted as a very large unsigned value when used as a size), leading to a smaller-than-expected allocation followed by out-of-bounds writes.

The exploit was elegant. The attacker creates a pipe, writes data to fill the buffers, then manipulates the buffer count via a race condition or a series of operations that causes the count to wrap around to a negative value. The kernel allocates a tiny buffer. The attacker writes data into it. The data spills into adjacent kernel memory. Including function pointers. Which the attacker can overwrite with addresses pointing to shellcode.

Result: kernel-level code execution. Ring 0. Complete system compromise from a user account.

The fix: use unsigned integers for counts and sizes, and validate them properly. This is a lesson that has been learned approximately ten thousand times and will need to be learned ten thousand more, because integers in C are a footgun that never runs out of ammo.

The sign bit—bit 31 of a 32-bit integer—was the trigger. When the count went negative, the sign bit flipped. And with that flip, the semantic meaning of the integer changed from "a small positive number of buffers" to "a very large unsigned allocation size." One bit. Two interpretations. Complete system compromise.

## The Space That Wasn't There

CVE-2014-0160. Heartbleed. The OpenSSL vulnerability that allowed remote attackers to read arbitrary memory from servers using vulnerable versions of OpenSSL.

The bug was in the TLS heartbeat extension. The client sends a heartbeat request containing a payload and a payload length. The server responds with the same payload. The implementation:

```c
// Simplified
memcpy(buffer, request_payload, request_length);
```

The server trusted the client's stated payload length. If the client said "my payload is 64KB" but only sent 1 byte, the server would copy 64KB from its own memory—starting from the request payload location—into the response. The extra bytes came from the server's process memory. They could contain anything: private keys, session tokens, passwords, other users' data.

The fix was two lines: check that the stated payload length doesn't exceed the actual received data length. Two lines. The vulnerability existed for *two years* before discovery. During that time, an estimated 17% of the internet's HTTPS servers were vulnerable. Including banks. Including government services. Including the infrastructure of the internet itself.

The byte that bit back here wasn't a specific byte value. It was the *absence* of bytes. The client claimed N bytes existed. Only M bytes existed (M < N). The server copied the M real bytes plus (N - M) bytes of whatever happened to be adjacent in memory. The gap between claimed length and actual length—measured in bytes—was the weapon.

Every byte in that gap was a byte that shouldn't have been read. Every byte in that gap was potentially someone's password, someone's credit card number, someone's private key. And the server just handed them over, because nobody checked whether the length was real.

## The Bit That Killed DNS

CVE-2015-5477. BIND 9, the most widely used DNS server on the internet. A single-byte error in the handling of DNS response packets could cause the server to crash.

The specific issue was in `lib/dns/rdata.c`. When parsing certain DNS responses, BIND failed to properly validate that a buffer had enough space before writing. The result was an assertion failure—a deliberate crash rather than silent corruption, because BIND's developers had the good sense to prefer crashing over being owned.

But crashing is still bad. DNS is the phone book of the internet. If DNS goes down, everything goes down. A remote attacker could send a specially crafted DNS response to a vulnerable BIND server and crash it. Repeatedly. A denial-of-service attack against the internet's directory service.

The byte that did it? A length field in a DNS response packet. The attacker set it to a value that was one byte larger than the buffer allocated for it. One byte of overflow triggered the assertion. One byte of overflow crashed the DNS server. One byte of overflow took down the internet's naming system.

## Every Byte Is a Loaded Gun

I want to make a point that I think is underappreciated: in a C program, every byte is a loaded gun.

Not most bytes. Not some bytes. *Every* byte. Every byte in a running C program has the potential, if read or written at the wrong time with the wrong value, to cause a security vulnerability. The only reason most programs work is that most bytes point at nothing most of the time.

Consider what a single byte can do:
- A null byte can terminate a C string prematurely, bypassing length checks
- A `0xFF` byte can be interpreted as -1 in a signed context, causing infinite loops or buffer underflows
- A byte with value 0x80 can flip a sign bit, turning a positive number negative
- A single-byte overwrite can modify a return address, a function pointer, or a length field
- A single byte read beyond a buffer can leak sensitive information
- A single byte of underallocation can create a one-byte overflow that's enough for a stack pivot

The entire discipline of computer security is, at its core, the discipline of managing bytes. Buffer overflows are about writing bytes where they shouldn't go. Information leaks are about reading bytes that shouldn't be read. Integer overflows are about bytes being interpreted with the wrong semantics. Format string vulnerabilities are about bytes being treated as format specifiers. Injection attacks are about bytes being interpreted as code instead of data.

And the programming language that dominates systems software—C—gives you no help whatsoever. C trusts you to manage every byte correctly. C assumes you know what you're doing. C assumes that every byte you write is a byte you meant to write, in the place you meant to write it, with the value you meant to write.

In a program of any non-trivial size, this assumption is always wrong. Always. There has never been a non-trivial C program without a byte-level error. The question is not whether the errors exist. The question is whether the errors are exploitable.

Most of the time, they're not. Most of the time, the off-by-one writes into padding. Most of the time, the sign bit confusion produces a wrong but harmless result. Most of the time, the null byte just causes a string to be truncated. Most of the time, the gun points at nothing.

But "most of the time" is not "all of the time." And in the gap between "most" and "all," entire industries have been born. Vulnerability research. Penetration testing. Static analysis. Dynamic analysis. Fuzzing. Bug bounties. All of these exist because "most of the time" is not good enough.

## The Lesson (There Is No Lesson)

I'd love to tell you there's a lesson here. "Always validate your inputs." "Use unsigned integers for sizes." "Check your bounds." "Use a memory-safe language."

These are all true. And they're all insufficient.

The WU-FTPD developers thought they'd validated their inputs. They just missed one `<=` that should have been `<`. The Ariane 5 engineers thought they'd checked their ranges. The ranges just changed between rocket versions. The OpenSSL developers thought they'd handled the heartbeat correctly. They just forgot one length check. The BIND developers thought their parser was robust. They just missed one case.

Every byte is a loaded gun, and no amount of careful handling changes the fact that guns go off. The best you can do is minimize the number of guns, point them in safe directions, and check frequently to see if any have fired.

Memory-safe languages help—they eliminate entire categories of byte-level errors. Rust helps—it eliminates data races and enforces ownership semantics. Static analysis helps—it catches patterns that humans miss. Formal verification helps—it proves properties about programs.

But none of these eliminate all byte-level errors. The gun is always there. The bullet is always chambered. And every now and then, a single byte—eight bits, one `<=` that should have been `<`, one sign bit that should have been zero, one null byte that shouldn't have been there—pulls the trigger.

---

*The author has written approximately 200,000 bytes of C code in their career. They have introduced approximately 2,000 byte-level errors. Most were caught. Some were not. The ones that were not are still out there, in running systems, pointing at nothing. For now.*
