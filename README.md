# Uyasir146/tiny-chess-01

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/Uyasir146/tiny-chess-01/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/Uyasir146/tiny-chess-01/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A chess engine in **3,877 bytes** of Python (`main.py`, the make.fun 4,096-byte cap). `engine_v3.py` is
the readable source; `main.py` is that source packed with the kit's own `makefun compress`, so the
payload at the repository root is the engine itself.

0x88 board representation, iterative-deepening alpha-beta with a transposition table, null-move
pruning, late-move reductions, killer moves, a history heuristic and capture-only quiescence search,
mate-distance scoring, and three additions over the first version:

- **check extension** — a position where the side to move is in check is searched one ply deeper
  (`d += 1`, capped at ply 30);
- **bishop pair** — `+32` centipawns for the side holding two or more bishops;
- **aspiration windows** — from depth 4 on, each iteration searches a window of ±50 around the
  previous score, retries at 6× width on a fail, then falls back to a full window.

Its search is budgeted by **220,000 nodes, never by a wall clock**, so a replay picks the same moves
every time: same FEN in, same move out, twice in a row. Pure standard library.

## Verified

- Move generation, perft: start position `20 / 400 / 8,902` at depths 1–3, kiwipete
  `r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1` `48 / 2,039` at depths 1–2.
- Packed payload: `exec` of `main.py` with a capturing `exec` yields a decompressed string
  byte-identical to `engine_v3.py` (sha256 `3fc699899c7926b5d4a5e48860795edc40e6f22f1df0208a53d0ba72329d7e79`).
- The kit's own practice trial-0 (drawn from drand round 33447412), replayed against the sealed env
  and scored by the kit's sealed scorer: **4 wins, 2 draws, 0 losses (5.0/6), Elo 1654**, 472 spare
  plies — wins by checkmate against the depth-2, depth-3, depth-4 and 100k-node house engines, draws
  against the 250k- and 500k-node ones. No game ended on `time`: the slowest of 97 sampled moves took
  **6.1 s** (mean 4.3 s) against the env's 10 s move cap.

## Run it

```sh
MAKEFUN_ENV_URL=http://127.0.0.1:8080 python3 main.py
```

The entry speaks the env's `POST /game` and `POST /move` with nothing but `urllib`: it asks for the
next game, searches the FEN it is handed, and answers with a UCI-shaped move, falling back to the
env's own first legal move if its choice is ever rejected.

---

<sub>Entered on [make.fun](https://make.fun/?ref=wq6bzz8g&utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>