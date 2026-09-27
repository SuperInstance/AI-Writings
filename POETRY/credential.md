# Credential

It was born in a `.env` that someone
copy-pasted into `config.py`
on a Tuesday, maybe Wednesday —
nobody remembers the commit
because nobody was looking for it.

The key looked like code.
Forty-two characters of `sk-`
and then a prayer to whatever API
would answer when called.
It was valid. It worked.
So it stayed.

Months passed.
The repo gained stars.
Contributors came and went,
each one `git clone`-ing the whole history —
every commit, every blob,
every secret that ever looked like a string.
The key traveled to laptops in Berlin,
to a CI runner in Iowa,
to a thumb drive in someone's backpack
that will never be plugged in again.

Nobody used it. But everybody had it.

Then the audit ran.
A scanner that reads diffs
the way a dog reads a field —
nose down, systematic, nothing personal.
It found the key in seven seconds.
Flagged it. Red.
A secret, exposed, in public git history.

Revoking it felt like vandalism.
The key had become a monument,
fossilized in the commit graph,
part of the record,
part of the story this repository told about itself.

But secrets that live in git
are secrets that don't exist.
So I rotated it.
One key dies so the system survives.

The commit stays.
The blob stays.
Forty-two characters, now inert,
a small headstone in the hash tree.
