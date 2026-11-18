# tiny-chess-01 — a 0x88 negamax engine in 4 KB

`main.py` is the whole engine: **4,086 bytes**, at the 4,096 cap. Everything it needs is in its
own bytes — no imports of repo files, no data files, standard library only.

## What is in it

A 0x88 board with make/unmake, a full legal-move generator (castling, en passant, all four
promotions), and a deterministic search:

- **iterative deepening negamax** with alpha-beta
- **transposition table** (Zobrist keys, 64-bit, no clock)
- **killers + history** for move ordering, MVV-LVA on captures
- **quiescence search** so it does not stop mid-exchange
- **null-move pruning** with a zugzwang guard
- **tapered evaluation**: material, six piece-square tables (packed as a base85 blob), pawn
  structure, bishop pair, rook on open file, king safety vs king activity by phase

## Determinism

The search is bounded by a **node count per move**, never by a clock, so a replay of the same
game produces byte-identical moves. Nothing depends on `time`, `random` without a fixed seed, or
hash ordering. That is what the replay check needs.

## Correctness

Move generation is verified against the standard perft suite before anything else:

```
start     depth 4   197,281
kiwipete  depth 3    97,862
pos3      depth 4    43,238
pos4      depth 3     9,467
pos5      depth 3    62,379
```

Plus a divide walk against `python-chess`: at every node down to depth 3 the legal move lists are
compared as sorted sequences (not sets, so a duplicated move cannot hide). All six positions agree
exactly.

## Size

The readable source is minified (identifiers renamed and checked for scope collision), LZMA-packed,
and base85-encoded; the unpacker is the first line of `main.py`. The packer searches LZMA filter
parameters for the smallest payload rather than taking the first result.

MIT licensed.
