# tiny-chess-01 — a 0x88 negamax engine in under 4 KB

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/Uyasir146/tiny-chess-01/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/Uyasir146/tiny-chess-01/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

An entry for the [tiny-chess-01](https://make.fun/bounty/tiny-chess-01) bounty on
[make.fun](https://make.fun): a whole chess engine in one file, `main.py`, **3,796 bytes**
(cap: 4,096). Everything it needs is in its own bytes — no imports from repo files, no data files,
no network calls except the env protocol.

## Run it

`main.py` speaks the kit's env protocol: it reads `MAKEFUN_ENV_URL`, asks for the position, and
plays until the game ends. With the competition kit unpacked next to this repo:

```sh
MAKEFUN_ENV_URL=http://127.0.0.1:3000 python main.py
```

`main.py` is generated, not hand-edited. The readable source lives outside the repo and is packed
with the kit's own compressor, which LZMA-compresses it into a self-unpacking stub:

```sh
node cli/makefun.mjs compress engine.py --out main.py
```

## How the size cap is met

The readable source (~12 KB of Python) is renamed to per-scope unique short names, squashed, and
LZMA-compressed into a small self-unpacking stub (`base85` payload + `exec(lzma.decompress(...))`).
Piece-square tables ship as one base85 blob instead of decimal literals — decimal PSTs are ~4 KB of
high-entropy text that LZMA cannot compress, so they alone would blow the cap.

## Engine

* **Board**: 0x88, 128-entry array, piece codes `±1..6`.
* **Search**: iterative-deepening negamax, alpha-beta, transposition table keyed by Zobrist hash
  (piece/square + castling + en-passant file + **side to move**), killer moves, history
  heuristic, check extension, quiescence with delta-style stand-pat and a depth cap.
* **Eval**: material + tapered piece-square tables, half-file-mirrored (32 entries per piece).
* **Determinism**: the search is bounded by a **fixed node count per move**, never by a clock, and
  contains no randomness — so a replay of a trial reproduces every move exactly. This matters:
  the rules replay the final trial and mark a mismatched run `nondeterministic`.

## Correctness

Move generation is verified against the standard perft suite and cross-checked against
`python-chess`, which is a stronger test than counting leaves alone — `tools/divide.py` descends
until a node's legal-move set disagrees and prints the exact extra/missing moves.

| position | depth | nodes |
|---|---|---|
| start | 4 | 197,281 |
| Kiwipete | 3 | 97,862 |
| pos3 | 4 | 43,238 |
| pos4 | 3 | 9,467 |
| pos5 | 3 | 62,379 |

## Local harness

The env in the kit is playable without Docker: `tools/trial.py` boots `program/env/server.mjs`,
points the engine at it, and reports the Elo the env itself computes over the eight house engines.
`tools/play.py` does the same but records every game's outcome and FEN, which is how the PST
orientation bug (tables read upside-down: the king was paid to march to h5, pawns paid to stay
home) was found — visible as 0/6 losses even at 150k nodes per move.

## License

MIT. See `LICENSE`.
