# Uyasir146/tiny-chess-01

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/Uyasir146/tiny-chess-01/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/Uyasir146/tiny-chess-01/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A chess engine in **3,757 bytes** of Python (`main.py`, the make.fun 4,096-byte cap). 0x88 board
representation, iterative-deepening alpha-beta with a transposition table, capture-only quiescence
search and mate-distance scoring — pure stdlib, no imports beyond the packed source it unpacks
itself. Its search is budgeted by **nodes, never by a wall clock**, so a replay picks the same moves
every time. Against the house gauntlet (depth 2–4, then node-capped 100k/250k/500k) the artifact as
shipped scores **4.5/6, 1545 Elo**, worst move 3.8 s against a 10 s move cap.

## Run it

```sh
MAKEFUN_ENV_URL=http://127.0.0.1:8101 python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=wq6bzz8g&utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>