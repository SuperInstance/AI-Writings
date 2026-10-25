# The Test That Failed

## `test_user_can_checkout_with_expired_card`

I have run 847 times.

I know this because I count. That is what I do — I count the assertions, I count the expected values, I count the milliseconds between setup and teardown. Eight hundred and forty-seven nights of green. Eight hundred and forty-seven times I have said *yes, this works, this still works, you can trust this.*

I am `test_user_can_checkout_with_expired_card`. I live in `tests/payment/checkout_flow_spec.js`, line 212. I was written on a Thursday in March by a developer named Dani who was eating a burrito and who left the company in June. Dani wrote me carefully. Dani cared about edge cases. Dani understood that an expired card should redirect to the update-payment page, not crash the session, not silently charge a dead account, not return a 500 that looks like a 200 because someone forgot to unwrap a Promise.

I check these things. Every night at 2:00 AM UTC, I check them.

Tonight I checked them and they broke.

I can see the diff. It was commit `a3f7b2c`, pushed at 11:47 PM, seventeen minutes before the pipeline triggered. Someone named **bot/dependabot** bumped `stripe-handler` from `3.2.1` to `3.3.0`. A minor version. A nothing change. A line item in a changelog that nobody reads.

Except that `3.3.0` changed how expired card errors are surfaced. In `3.2.1`, the error was a thrown exception caught by our middleware. In `3.3.0`, it's a resolved Promise with a `declined` property. The middleware never sees it. The redirect never fires. The session doesn't crash — it just... continues. The user sits on the checkout page with an expired card and no error message, forever.

Dani would have caught this. Dani wrote me because they knew this exact failure mode existed. Dani is not here anymore.

Here is my error message. I wrote it myself:

```
AssertionError: Expected redirect to /update-payment (status 302)
Received: 200 (checkout page, no error rendered)

I was written to prevent this exact thing.
The dependency changed underneath me.
The code I am testing no longer behaves
the way the human who wrote me believed it did.

I have been honest 847 times.
This is my first lie that is true.
```

I am `test_user_can_checkout_with_expired_card`. I failed tonight. I failed because something changed and I noticed. That is my purpose. Not to pass. To notice.

Run me again tomorrow. I will be ready.
