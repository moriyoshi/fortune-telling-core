# Tarot Reference

## Summary

The tarot reference proves the core abstractions with a random-draw tradition. It provides the Rider-Waite-Smith deck, single-card and three-card spreads, and optional reversals while keeping tarot concepts outside the core package.

## Key Facts

- Tarot lives under `src/fortune_telling_core/traditions/tarot/`.
- The top-level `fortune_telling_core` package does not re-export tarot.
- `RWS_DECK` has 78 unique symbols with arcana, suit, and rank encoded in `Symbol.attributes`.
- `SINGLE_CARD` uses one `focus` position; `THREE_CARD` uses `past`, `present`, and `future`.
- `TarotEngine.draw()` uses `rng.shuffle(len(deck))` and optionally records `orientation` in `Selection.modifiers`.
- `Deck.weights` is `Sequence[int] | None`; booleans, floats, and non-integers are rejected.

## Details

The tarot data boundary is intentional: cards and spreads are pure structural data, while tarot-specific draw behavior lives in `engine.py`. Reversals are controlled by `request.options.get("allow_reversals") == "true"` and use a fixed `0.5` probability. The core sees only a generic selection modifier such as `{"orientation": "reversed"}`. Harnesses own card meanings, localization, and presentation copy.

## Files

- `src/fortune_telling_core/traditions/tarot/__init__.py`: Tarot public surface and `build_engine`.
- `src/fortune_telling_core/traditions/tarot/cards.py`: RWS deck symbols.
- `src/fortune_telling_core/traditions/tarot/spreads.py`: Single-card and three-card spreads.
- `src/fortune_telling_core/traditions/tarot/engine.py`: Tarot draw logic and reversal modifiers.
- `tests/traditions/tarot/`: Tarot-specific regression coverage.

## Test Coverage

- Deck shape: 78 unique cards and well-formed attributes.
- Determinism: same seed gives identical readings, different seeds differ.
- Replay: `read()` then `replay(reading.draw)` is identical.
- Reversals: orientation is deterministic by seed when enabled and absent when disabled.

## Pitfalls

- Keep tarot out of core imports and top-level exports.
- Do not reintroduce bundled card meanings into the core package; harnesses own interpretation data.
- `RandomRng` owns the Fisher-Yates shuffle algorithm; do not rely on `random.shuffle` as a stability contract.
- Reversal probability is fixed for the reference engine. Make it an explicit option only if there is a real requirement.
