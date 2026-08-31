# Vendored CartoSym-JSON Part 2 (Shapes) schema

A **local copy** of the JSON Schema for Part 2 of the OGC Cartographic
Symbology conceptual model — *"Model extension for graphical shapes and
transformations"* (Shape Graphics: `Circle`, `Ellipse`, `Rectangle`,
`Arc`, `Path`, shape outlines, 2D/3D transforms, gradient/pattern fills).

Used as the **authoritative reference** for the shape of the Part 2
concepts the codecs map onto (`models/symbolizers.py` — `ShapeOutline`,
`ClosedShape`, `CircleGraphic`; the MapLibre `circle` mapping). It is
**not currently wired into runtime validation**: the package's runtime
schema is the Part 1 `src/pycartosym/schemas/CartoSym-JSON.schema.json`.

## Provenance

- Source: <https://github.com/opengeospatial/cartographic-symbology>,
  path `2-shapes/schemas/CartoSym-JSON-2-shapes.schema.json`
- Upstream commit: `3123eb769f7293d6f6948d555e622b6ec8489877` (2024-06-03)
- Retrieved: 2026-08-30, byte-for-byte (no edits)

## Note — this is a *delta overlay*, not a standalone schema

The file is an overlay on Part 1: its `$defs` opens with an `allOf`
`$ref` to `../1-core/schema/CartoSym-JSON.schema.json` and several
entries redefine a Part 1 `$def` as `{ "allOf": [ {"$ref":
"#/$defs/<name>"}, … ] }` (a self-reference that only resolves once the
two `$defs` maps are merged). It therefore cannot be handed to a
validator as-is — treat it as documentation of the Part 2 additions,
cross-referenced against Part 1.

### The `Circle` chain (what the codecs rely on)

```
abstractGraphic : { alter, position: unitPoint, opacity: zeroToOne }
abstractShape  --|> abstractGraphic : { outline: shapeOutline }
closedShape    --|> abstractShape   : { fill: fill }
circle         --|> closedShape     : { type: "Circle", center: unitPoint, radius: unitValue }
```

`shapeOutline` is **not** a Part 1 `stroke`:
`{ alter, thickness: unitValue, opacity: zeroToOne, color }`.
