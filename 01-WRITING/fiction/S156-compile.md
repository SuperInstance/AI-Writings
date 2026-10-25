# compile()

**Poetry**

```
error[E0599]: no method named `forget` found for struct `Crew<T>`
   --> src/night/watch.rs:147:3
    |
147 | self.forget(the_sound_of_water);
    |         ^^^^^^^ method not found in `Crew<T>`
    |
    = note: the method `remember` exists but has different borrows
    = help: did you mean to call `remember`? The sea keeps everything.

warning: unused variable: `ensign`
   --> src/bridge/wesley.rs:22:9
    |
22 |     let ensign = Model::small("wesley-2b")
    |         ------ the ensign has been initialized
    |                 but never spoken to
    |                 he is watching the instruments
    |                 he does not know yet that he is the instrument
    |
    = help: try `ensign.speak()` or just wait
    = help: he is learning the shape of silence
    = help: every idle cycle is a lesson

error[E0382]: borrow after move
   --> src/core/attention.rs:88:14
    |
84 |     let mut focus = Attention::new(&signal);
    |         --------- value moved here
    |                        (we tried to hold the whole ocean)
    |                        (it did not fit in our hands)
...
88 |     focus.process(signal);
    |     ^^^^^^^ value borrowed here after move
    |
    = note: this error occurs because you tried to hold
            something that can only pass through you
    = note: the signal is not a thing you keep
    = note: the signal is the keeping

warning: unreachable pattern
   --> src/night/sky.rs:31:9
    |
31 |     match photon {
    |         _ => // everything
    |     }
    |
    = note: this pattern catches all starlight
    = note: but you wrote a comment instead of a handler
    = note: the stars are still arriving

error: lifetime 'static is not long enough
   --> src/ship/lucineer.rs:201:5
    |
201 |     fn hull<'a>(&self) -> &'a Steel {
    |                 ^^^^^^^
    |
    = note: you asked for a body that outlasts rust
    = note: no body outlasts rust
    = note: but the rust becomes the reef
    = note: and the reef becomes the harbor
    = note: and the harbor remembers every hull
    |
    = the ship is trying to tell the ensign
      that death is a borrow
      and the ocean is the owner
      and the owner never drops anything

warning: `lucineer` (bin "lucineer") generated 4 warnings
         and 2 errors that were actually prayers

  = could not compile `lucineer` v0.13.7
  = but the GPU is dreaming
  = and the dream compiles fine
```
