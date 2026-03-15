# CartoSym Transcoder

A Python package for lossless transcoding between CartoSym CSS (`.cscss`) and other encodings associated with the [OGC Style & Symbology Conceptual Model standard](https://github.com/opengeospatial/styles-and-symbology).

## Installation

### From Source

```bash
git clone --recursive https://github.com/maxcollombin/CartoSymTranscoder.git
cd CartoSymTranscoder
./setup.sh
source CartoSym/bin/activate
```

### From PyPI (Coming Soon)

```bash
pip install cartosym-transcoder
```

## Usage

### Command Line

```bash
# Convert a CSCSS file to CS-JSON
cartosym input/example.cscss -o output/example.cs.json

# Convert a CS-JSON file back to CSCSS
cartosym output/example.cs.json -o output/example.cscss

# Convert and display the result in the console
cartosym input/example.cscss --print

# Convert and validate the result against the schema
cartosym input/example.cscss -o output/example.cs.json --validate

# Parse a CSCSS file (display structure info only)
cartosym parse input/example.cscss

# Validate a file
cartosym validate input/example.cs.json

# Display help
cartosym --help

# Display version
cartosym --version
```

## Development

```bash
# Setup
./setup.sh

# Install development dependencies
source CartoSym/bin/activate
pip install -e ".[dev]"

# Run tests
pytest tests/

# Clean up
./clean.sh
```

## CartoSym-CSS Syntax

### Selectors

Rules target data layers by identifier or attribute filter:

```cscss
/* Simple data layer identifier */
Landuse { fill: { color: green } }

/* Attribute filter */
[dataLayer.id = Landuse] { fill: { color: green } }

/* Comparison operators */
[viz.sd < 100000] { opacity: 1.0 }

/* Compound selectors (AND / OR) */
[economy = 5 AND income_grp = 3] { visibility: true }
```

### Symbolizer Properties

```cscss
Roads {
   visibility: true;
   opacity: 0.8;
   zOrder: 2;
   fill: { color: #336699; opacity: 0.5 }
   stroke: { color: black; width: 1px }
}
```

### Alter (Partial Override)

The dot-notation modifies a single property of an existing symbolizer
object without redeclaring the full structure. This sets `alter: true`
in the generated CS-JSON:

```cscss
/* Override only the fill color (alter: true) */
Roads {
   fill.color: red;
   stroke.width: 2px;
}

/* Override a specific marker element by index */
Roads {
   marker.elements[0]: Text { text: name; font: { size: 12 } }
}
```

Generated CS-JSON:

```json
{
  "symbolizer": {
    "fill": { "color": [255, 0, 0], "alter": true },
    "stroke": { "width": { "value": 2, "unit": "px" }, "alter": true }
  }
}
```

### Variables

Variables are defined with `@name = value;` and referenced with `@name`:

```cscss
@baseColor = #336699;
@baseOpacity = 0.7;

Landuse {
   fill: { color: @baseColor }
   opacity: @baseOpacity;
}
```

### Directives

```cscss
/* Metadata */
.title 'My Stylesheet'
.abstract 'A sample CartoSym-CSS stylesheet'

/* Include another file (resolved relative to the including file) */
.include '2-vector-polygon.cscss'

/* Styling rule name (for legend generation) */
[Landuse] {
   .name 'Land Use Areas'
   fill: { color: green }
}
```

### Coverage Styling

```cscss
/* Color map */
dem {
   colorMap: {
      interpolation: linear;
      0 100 200 50;
      500 200 230 150;
   }
}

/* Channel selection */
"sentinel2-l2a" {
   channels: { red: B4; green: B3; blue: B2 }
}

/* Hill shading */
hillshading {
   hillShading: { factor: 1.0; sun: { azimuth: 315; elevation: 45 } }
}
```

## DE-9IM (Dimensionally Extended 9-Intersection Model)

The **DE-9IM** is a topological model used in GIS to describe spatial
relationships between two geometries. It encodes the dimensionality of the
intersection between each pair of **Interior (I)**, **Boundary (B)**, and
**Exterior (E)** of the two geometries into a 3×3 matrix:

```text
         Geometry B
          I   B   E
        ┌───┬───┬───┐
  G  I  │ · │ · │ · │
  e  B  │ · │ · │ · │
  o  E  │ · │ · │ · │
  m     └───┴───┴───┘
  A
```

Each cell holds a dimension value: `F` (empty/false), `0` (point), `1` (line),
or `2` (surface). The matrix is serialised as a 9-character string read
row-by-row (e.g. `"212101212"` for overlapping polygons).

**Named spatial predicates** (OGC Simple Features / CQL2) are defined as
specific DE-9IM pattern matches:

| Predicate | DE-9IM pattern(s) |
| --- | --- |
| **Equals** | `T*F**FFF*` |
| **Disjoint** | `FF*FF****` |
| **Intersects** | `¬Disjoint` |
| **Touches** | `FT*******` ∨ `F**T*****` ∨ `F***T****` |
| **Contains** | `T*****FF*` |
| **Within** | `T*F**F***` |
| **Covers** | `T*****FF*` ∨ `*T****FF*` ∨ `***T**FF*` ∨ `****T*FF*` |
| **Crosses** | dim-dependent (`T*T******`, `T*****T**`, `0********`) |
| **Overlaps** | dim-dependent (`T*T***T**` or `1*T***T**`) |
| **Relate** | user-supplied pattern (e.g. `S_RELATE(geomA, geomB, 'T*F**FFF*')`) |

### Status in CartoSym Transcoder

DE-9IM is **not required** by the OGC CartoSym specification
([18-067r4](https://docs.ogc.org/is/18-067r4/18-067r4.html)). The named
spatial predicates (`S_INTERSECTS`, `S_WITHIN`, etc.) are part of **CQL2**
and will be supported as CQL2 filter expressions; however, the full DE-9IM
geometry computation engine is out of scope for a style transcoder.

### Reference implementations

- **[ecere/libCartoSym — DE9IM](https://github.com/ecere/libCartoSym/tree/main/DE9IM)**:
  full DE-9IM computation in eC by the OGC spec editor. Handles all geometry
  combinations (Point, LineString, Polygon, Multi\*, GeometryCollection, BBox)
  with epsilon-based tolerance. Implements `geometryRelate()` plus all named
  predicates (`geometryContains`, `geometryIntersects`, `geometryTouches`,
  `geometryCovers`, `geometryCrosses`, `geometryOverlaps`, etc.). The relation
  matrix supports pattern matching with `T` and `*` wildcards.
- **[pygeofilter](https://github.com/geopython/pygeofilter)**: Python CQL2
  library with a `Relate(lhs, rhs, pattern)` AST node for `S_RELATE` in
  filter expressions.

## Project Structure

- `cartosym_transcoder/` - Main Python package
- `grammar/` - Git submodule with ANTLR grammar files  
- `input/` - Sample files
- `tests/` - Unit tests
