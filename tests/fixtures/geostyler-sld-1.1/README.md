# Vendored GeoStyler SLD 1.1 test corpus

A verbatim copy of the SLD 1.1 test data from
[`geostyler/geostyler-sld-parser`](https://github.com/geostyler/geostyler-sld-parser),
`data/slds/1.1/`, used by `tests/test_sld_se_geostyler.py` to exercise the
`cartosym_transcoder.codecs.sld_se` reader/writer against third-party SLD/SE
1.1.0 documents (not just this project's own hand-written fixtures in
`input/sld/`).

## Provenance

- Source: <https://github.com/geostyler/geostyler-sld-parser>
- Path: `data/slds/1.1/`
- Commit: `48f761c812d5d04df44cfa09f3969b5c78778131`
- Retrieved: 2026-08-28
- Licence: BSD-2-Clause (see the upstream repository's `LICENSE`)

Files are copied unmodified. They are SE 1.1.0 (`se:` namespace,
`se:SvgParameter`).

## How the tests use them

`tests/test_sld_se_geostyler.py` splits the corpus into two explicit lists:

- **in scope** — files fully within this codec's vector + Part-1-raster
  scope. Each must `read` → `write` → validate against the vendored OGC XSD
  → `read` again to a Pydantic-model fixed point.
- **out of scope** — files using constructs this codec deliberately does
  not map (non-`circle` marks, graphic fills/strokes, `ogc:Function`
  filters, `se:MinScaleDenominator`, `se:LinePlacement`, contrast
  enhancement, …). Each must raise `NotImplementedError` (a *clean*
  rejection — never another exception type).

Moving a file between categories is a deliberate act: the test will fail
loudly if a change silently shifts one.
