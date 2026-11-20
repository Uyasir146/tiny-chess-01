# Uyasir146/tiny-chess-01

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/Uyasir146/tiny-chess-01/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/Uyasir146/tiny-chess-01/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A chess engine in **4,071 bytes** of Python — `main.py` is `engine_v7.py` packed with the kit's own
`makefun compress`, inside a 4,096-byte cap and pure standard library.

0x88 board, iterative-deepening alpha-beta with a transposition table, null-move pruning, late-move
reductions, killer moves, a history heuristic, capture-only quiescence and mate-distance scoring,
plus a check extension (`d += 1` in check, capped at ply 30), a +32 centipawn bishop pair, and
aspiration windows from depth 4 (±50, 6× on a fail, then a full window). Separate king tables for
the endgame (`KE` once fewer than 14 pieces are left, `KM` before that), and a whole-game
position history so the search never walks into a threefold repetition or a fifty-move draw.

Search is budgeted by **140,000 nodes, never a wall clock**: same FEN in, same move out.

## Verified

- perft: start `20 / 400 / 8,902`, kiwipete `48 / 2,039`.
- `main.py` is 4,071 bytes and its decompressed payload is byte-identical to `engine_v7.py`.
- Kit practice trial-0, sealed env and scorer: **5 wins, 1 draw, 0 losses (5.5/6), Elo 1809**, 535 spare plies, no timeout and a
  move-identical replay; slowest sampled move 3.3 s against a 10 s cap.
- Every request path is retried, never fatal: the engine keeps playing even if one call fails, and
  falls back to the env's own legal move list if a search ever returns nothing.

## Run it

```sh
MAKEFUN_ENV_URL=http://127.0.0.1:8080 python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=wq6bzz8g&utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>