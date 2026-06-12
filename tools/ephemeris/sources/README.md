# Built-In Ephemeris Sources

`src/fortune_telling_core/astronomy/ephemeris/builtin_series.py` is generated
from the files in this directory by:

```sh
python tools/ephemeris/generate_builtin_series.py --download-missing
```

To verify that the committed generated module still matches these source files:

```sh
python tools/ephemeris/generate_builtin_series.py --check --download-missing
```

The VSOP87D files are a local cache under `.cache/ephemeris/vsop87d/`, not
repository-managed source files and not part of `tools/`. They are public
IMCCE/Bureau des Longitudes coefficient files from
`https://ftp.imcce.fr/pub/ephem/planets/vsop87/`.

To populate or refresh that cache directly:

```sh
python tools/ephemeris/download_vsop87d.py
```

Downloads are verified against `MANIFEST.sha256`; the manifest keeps stable
`vsop87d/...` source identifiers even though the cache lives under `.cache/`.
The generator retains terms where `abs(A) >= 1e-7`.

`meeus_tables.py` contains structured Moon and Pluto periodic tables
transcribed from Meeus, *Astronomical Algorithms*, 2nd ed., chapters 47 and 37.
