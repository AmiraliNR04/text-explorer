- [x] Day 3: single-pass analyzer
## Single-pass design

`Analyzer` reads the input once and computes all stats simultaneously.
A 10GB file is read only once, not four times. It's also lazy — nothing
is read until `analyze()` is called.

- [x] Day 3: single-pass analyzer
## Single-pass design

`Analyzer` reads the input once and computes all stats simultaneously.
A 10GB file is read only once, not four times. It's also lazy — nothing
is read until `analyze()` is called.

- [x] Day 4: @timed decorator

## Timing

`@timed` decorator logs the runtime of any function. It uses `try/finally`,
so it logs **even if the function raises an error** — which is exactly when
you need that information most.