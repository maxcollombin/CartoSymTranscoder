# GeoServer SLD corpus

24 real-world GeoServer sample styles, vendored verbatim from
`geostyler/geostyler-sld-parser` (see `UPSTREAM` for the exact pin and
licence).

## What this corpus is

Every file is **SLD 1.0.0**:

- `CssParameter` (not SE 1.1.0 `SvgParameter`)
- default `sld` namespace, no `se:` namespace
- `<ogc:Filter>` / `<ogc:PropertyName>` for selection
- `PointPlacement` / `AnchorPoint` / `Displacement` spelled the 1.0 way

This is the version GeoServer emits and reads by default — distinct from
the SLD 1.1.0 / SE 1.1.0 that the in-repo `sld_se` codec targets.

## GeoServer-specific extensions present

| file | extension |
|---|---|
| `default_generic.sld` | `<VendorOption name="ruleEvaluation">`; `<ogc:Function name="geometry\|dimension\|isCoverage">` |
| `pattern_polygon.sld` | `<VendorOption name="graphic-margin">` |
| `poly_landmarks.sld` | `<VendorOption name="group">`, `<VendorOption name="autoWrap">` |
| `tiger_roads.sld` | `<VendorOption name="group">` |

The other 20 files are plain SLD 1.0.0 with no vendor extension — useful
for exercising the 1.0.0 XML dialect on its own.

## Refreshing

Re-pull `data/slds/geoserver/` from the upstream repo at a newer commit,
update `UPSTREAM`, review the diff.
