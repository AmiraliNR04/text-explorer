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


- [x] Day 5: context managers (@contextmanager + class-based)

## Context managers

Two patterns, same job:

1. `@contextmanager` (`timed_block`) — for simple timing wrappers.
2. Class-based (`AnalysisSession`) — when state must survive after `with`
   (e.g., `session.stats`, `session.success`, `session.duration`).

Both use `try/finally` under the hood, so cleanup runs **even on error**.