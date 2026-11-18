# tiny-chess-01 — a 0x88 negamax engine in 4 KB

`main.py` is the whole engine: **4,086 bytes**, at the 4,096 cap. Everything it needs is in its
own bytes — no imports from repo files, no data files, no network calls except the env protocol.

## How the size cap is met

Readable source lives outside the repo; `main.py` is produced by a build step that renames every
identifier to a per-scope unique short name, squashes whitespace, and LZMA-compresses the result
into a 3-line self-unpacking stub (`base85` payload + `exec(lzma.decompress(...))`). Piece-square
tables are stored as one base85 blob instead of decimal literals — decimal PSTs are ~4 KB of
high-entropy text that LZMA cannot compress, so they alone would blow the cap.

## Engine

* **Board**: 0x88, 128-entry array, piece codes `±1..6`.
* **Search**: iterative-deepening negamax, alpha-beta, transposition table keyed by Zobrist hash
  (piece/square + castling + en-passant file + **side to move**), killer moves, history
  heuristic, check extension, quiescence with delta-style stand-pat.
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
| pos5 | 3 | 62379 |

## Local harness

The env in the kit is playable without Docker: `tools/trial.py` boots `program/env/server.mjs`,
points the engine at it, and reports the Elo the env itself computes over the eight house engines.
`tools/play.py` does the same but records every game's outcome and FEN, which is how the PST
orientation bug (tables read upside-down: the king was paid to march to h5, pawns paid to stay
home) was found — visible as 0/6 losses even at 150k nodes per move.

## License

MIT. See `LICENSE`.