"""Private reusable name value systems.

Each module here normalizes script-specific text and assigns deterministic
numeric values to letters or characters. They are tradition-agnostic building
blocks consumed by tradition engines and are intentionally not part of the
public API; see the design note
``.agents/docs/design/non-ascii-name-numerology.md``.

A value system module exposes a stable ``ID`` and table ``VERSION`` plus a
``values(name, ...)`` function returning a tuple of
:class:`fortune_telling_core.traditions._name_text.NameValueUnit`.
"""
