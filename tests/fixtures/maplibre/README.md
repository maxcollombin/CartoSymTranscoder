# Vendored MapLibre style corpus

MapLibre GL style documents used by `tests/test_maplibre_corpus.py` to
exercise the `cartosym_transcoder.codecs.maplibre` reader/writer against
real, spec-valid styles rather than hand-written ones.

Everything here comes from **official MapLibre repositories** (not
third-party parsers). File contents are **unmodified**; the only local
change is layout (flat upstream → the sub-directories below).

## Layout

| dir | what | how the tests use it |
|---|---|---|
| `atomic/` | one styling construct per file (fill / line / circle / symbol / background), lifted from MapLibre GL JS render tests | reader unit tests (per PR of `codecs/maplibre`) |
| `integration/` | a complete published style | end-to-end reader → model → writer round-trip |
| `style-spec/` | small valid styles from the style-spec conformance suite (metadata / references / root properties) | reader must not choke on non-layer style keys |

Until the codec lands, `test_maplibre_corpus.py` only asserts each file is
(a) valid JSON and (b) valid against the official MapLibre style
specification (see `tests/_maplibre_spec.py`), and that the stub
reader/writer raise `NotImplementedError` cleanly.

## Provenance

### `atomic/`

- Source: <https://github.com/maplibre/maplibre-gl-js>
- Path: `test/integration/render/tests/<case>/<variant>/style.json`
- Commit: `8bec9e4105dca0b9e1daef6a4cca5d94b17f56ff`
- Retrieved: 2026-08-30
- Licence: BSD-3-Clause (see the upstream repository's `LICENSE.txt`)

Mapping of local name → upstream case:

| local | upstream `<case>/<variant>` |
|---|---|
| `fill-color-literal.json` | `fill-color/literal` |
| `fill-opacity-default.json` | `fill-opacity/default` |
| `fill-outline-color-default.json` | `fill-outline-color/default` |
| `fill-outline-color-literal.json` | `fill-outline-color/literal` |
| `fill-pattern-literal.json` | `fill-pattern/literal` |
| `line-color-literal.json` | `line-color/literal` |
| `line-simple.json` | `line-opacity/default` |
| `line-opacity-literal.json` | `line-opacity/literal` |
| `line-width-function.json` | `line-width/function` |
| `circle-color-literal.json` | `circle-color/literal` |
| `circle-radius-literal.json` | `circle-radius/literal` |
| `circle-stroke-width-default.json` | `circle-stroke-width/default` |
| `circle-stroke-literal.json` | `circle-stroke-color/literal` |
| `background-color-literal.json` | `background-color/literal` |
| `text-field-literal.json` | `text-field/literal` |
| `icon-image-literal.json` | `icon-image/literal` |

The upstream files carry a `metadata.test` block (render-harness sizing);
it is free-form `metadata` per the style spec and is left in place.

### `integration/demotiles.json`

- Source: <https://github.com/maplibre/demotiles> (`gh-pages` branch)
- Path: `style.json` — the official "MapLibre World" demo style
- Commit: `601ae60796ceceda2cbd2ed3d2ea92d17a84be4b`
- Retrieved: 2026-08-30
- Licence: BSD-3-Clause

### `style-spec/`

- Source: <https://github.com/maplibre/maplibre-style-spec>
- Path: `test/integration/style-spec/tests/<name>.input.json` (only the
  ones whose `<name>.output.json` is `[]`, i.e. valid)
- Commit: `92767d8725d824c470d57c4f9ba8c06e2ae317ed`
- Retrieved: 2026-08-30
- Licence: ISC / BSD-3-Clause (the spec derives from Mapbox's
  `mapbox-gl-js` style spec)

## Related vendored files

- `tests/schemas/maplibre-style-spec/v8.json` — the MapLibre style
  reference (same repo/commit as `style-spec/` above). It is MapLibre's
  bespoke schema format, **not** JSON Schema; validation goes through the
  official `@maplibre/maplibre-gl-style-spec` CLI (`gl-style-validate`),
  invoked from `tests/_maplibre_spec.py`. The vendored copy is kept for
  reference and offline inspection.
