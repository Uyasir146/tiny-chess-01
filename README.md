# tiny-chess-01 — a 0x88 negamax engine in under 4 KB

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/Uyasir146/tiny-chess-01/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/Uyasir146/tiny-chess-01/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

An entry for the [tiny-chess-01](https://make.fun/bounty/tiny-chess-01) bounty on
[make.fun](https://make.fun): one file, `main.py`, **3,796 bytes** (cap 4,096). It imports nothing
from the repo, reads no data files and makes no network calls except the env protocol.

## Run it

`main.py` reads `MAKEFUN_ENV_URL` and plays until the game ends. With the kit unpacked next to it:

```sh
MAKEFUN_ENV_URL=http://127.0.0.1:3000 python main.py
```

`main.py` is generated, not hand-edited: the readable source lives outside the repo and is packed
by the kit's compressor, `node cli/makefun.mjs compress engine.py --out main.py`, which
LZMA-compresses it into a self-unpacking stub (`base85` payload + `exec(lzma.decompress(...))`).
Piece-square tables ship as one base85 blob — decimal PSTs are ~4 KB of high-entropy text LZMA
cannot compress, so they alone would blow the cap.

## Engine

* **Board**: 0x88, 128-entry array, piece codes `±1..6`.
* **Search**: iterative-deepening negamax, alpha-beta, a transposition table keyed by Zobrist hash
  (piece/square + castling + en-passant file + **side to move**), killers, history heuristic,
  check extension, quiescence with stand-pat and a depth cap.
* **Eval**: material + tapered piece-square tables, half-file-mirrored.
* **Determinism**: bounded by a **fixed node count per move**, never a clock, with no randomness —
  a replayed trial reproduces every move, which the rules require (a mismatch is `nondeterministic`).

## Correctness

Move generation is verified on the perft suite and cross-checked against `python-chess` — a stronger
test than counting leaves. `tools/divide.py` descends until a node's legal-move set disagrees and
prints the exact extra or missing moves. Start d4 = 197,281; Kiwipete d3 = 97,862; pos3 d4 = 43,238;
pos4 d3 = 9,467; pos5 d3 = 62,379. The local harness (`tools/trial.py`) boots the kit's own env in
Node, so Elo is measured without Docker — which is how the PST orientation bug (tables read
upside-down: the king was paid to march to h5, pawns paid to stay home) showed up as 0/6 losses.

## License

MIT. See `LICENSE`.
