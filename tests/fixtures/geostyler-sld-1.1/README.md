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
  not map. Each must raise `NotImplementedError` (a *clean* rejection —
  never another exception type).

Moving a file between categories is a deliberate act: the test will fail
loudly if a change silently shifts one.

## Out-of-scope breakdown (28 files)

The scope boundary, mapped against this corpus:

| SE/SLD construct rejected | files | assessment |
|---|---|---|
| `se:Mark/se:WellKnownName` other than `circle` (`square`, `triangle`, `star`, `cross`, `x`, `shape://slash`, `ttf://` glyph) | 8 | extensible — real future scope |
| `se:GraphicFill` / `se:GraphicStroke` (hatch / pattern fills & strokes) | 6 | GeoServer vendor extension / CartoSym Part 2 |
| `se:MinScaleDenominator` / `se:MaxScaleDenominator` | 4 | **real 1:1 mapping to `viz.sd`, not yet implemented** |
| `se:LabelPlacement/se:LinePlacement` | 3 | unfinished design work |
| `ogc:Function` inside `ogc:Filter` | 2 | no Filter Encoding 1.1 mapping without `ogc:Function` support |
| `ogc:Function` inside `se:Label` (`round`, …) | 1 | property-driven label text, out of scope |
| `se:RasterSymbolizer/se:ContrastEnhancement` | 1 | "not supported by SLD/SE" per OGC Annex B |
| `se:ExternalGraphic/se:InlineContent` (base64) | 1 | no `se:OnlineResource` |
| bare `se:RasterSymbolizer` (only `se:Opacity`) | 1 | niche, no fix planned |
| colour = `se:Categorize` function result | 1 | property-driven colour, out of scope |

Only the `ScaleDenominator` and non-`circle`-mark rows (~12 files) are
"could reasonably be added"; the rest are deliberate Part-2 / vendor
scope calls.

**Source validity**: 6 of the 52 files are not themselves valid against
the pure OGC SE 1.1.0 XSD (empty `<se:Filter/>`, `ogc:Function` where the
schema wants `ogc:PropertyName`, a disallowed `type` attribute). Two of
those (`empty_filter`, `function_nested`) are in-scope — the codec
normalises them into valid SLD on write.
