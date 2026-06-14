# Unihan Stroke-Count Source

`src/fortune_telling_core/traditions/_name_values/data/unihan_total_strokes.txt`
is generated from the Unicode Unihan database by:

```sh
python tools/unihan/generate_total_strokes.py --download-missing
```

To verify that the committed table still matches the source archive:

```sh
python tools/unihan/generate_total_strokes.py --check --download-missing
```

The Unihan archive is a local cache under `.cache/unihan/`, not a
repository-managed source file and not part of `tools/`. It is the public
`Unihan.zip` from `https://www.unicode.org/Public/15.0.0/ucd/`, published by
Unicode, Inc. under the Unicode License v3
(`https://www.unicode.org/license.txt`), which permits redistribution of data
files.

To populate or refresh that cache directly:

```sh
python tools/unihan/download_unihan.py
```

Downloads are verified against `MANIFEST.sha256`; the manifest keeps a stable
`unihan/...` source identifier even though the cache lives under `.cache/`.

The generator extracts the `kTotalStrokes` property from the archive member
`Unihan_IRGSources.txt`. Per Unicode UAX #38 a `kTotalStrokes` entry may list
two space-separated values; the first (the count for the most customary form)
is the one bundled. These are representative-glyph totals, **not** the Kangxi or
school-specific counts that a particular `seimei handan` or `xingmingxue` school
may require — the `cjk_name_strokes` engine records that caveat in provenance
when this source is used.
