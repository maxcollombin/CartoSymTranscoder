# Vendored OGC SLD 1.1.0 / SE 1.1.0 XML Schemas

This directory holds a **local, self-contained copy** of the OGC schema graph
needed to XML-Schema-validate SLD *style documents* produced (and consumed) by
`pycartosym.codecs.sld` (SE 1.1.0 dialect). Used only by the test
suite (`tests/_xsd.py`, `tests/test_sld_xsd.py`) — it is not imported at runtime
and not part of the distributed package.

## Provenance

- Source: <http://schemas.opengis.net/> (the canonical OGC schema repository)
- Retrieved: 2026-08-27
- Entry point: `sld/1.1.0/StyledLayerDescriptor.xsd` (SLD 1.1.0), which pulls in
  transitively: SE 1.1.0 (`se/1.1.0/`), Filter Encoding 1.1.0 (`filter/1.1.0/`),
  GML 3.1.1 base (`gml/3.1.1/base/`, `gml/3.1.1/smil/`), and the two W3C
  schemas `xlink.xsd` / `xml.xsd`.
- Fetched with `xmlschema.download_schemas(...)`, which mirrors every remote
  `schemaLocation` under `http/<host>/<path>` and leaves the schema text
  otherwise untouched. Load the tree by pointing an XSD parser at
  `StyledLayerDescriptor.xsd` in this directory — the `http/` mirror is
  resolved automatically by relative path, no network access and no custom
  URI resolver required.

## Local modifications

Exactly one file is patched, and two groups of files are removed:

- **`sldAll.xsd`** — reduced to an empty schema for the `sld` namespace.
  Upstream, `StyledLayerDescriptor.xsd` does `<xsd:include schemaLocation="sldAll.xsd"/>`,
  and `sldAll.xsd` in turn includes `DescribeLayer.xsd`, `GetMap.xsd` and
  `sld_capabilities.xsd` — the WMS *operation* request/response schemas. Those
  drag in the entire WMS 1.3.0 / WFS 1.1.0 / OWS 1.0.0 schema graph, none of
  which is relevant to validating an SLD *style document*
  (`StyledLayerDescriptor` / `NamedLayer` / `UserStyle` / `FeatureTypeStyle` /
  `CoverageStyle` / `Rule` / symbolizers — all declared directly in
  `StyledLayerDescriptor.xsd` or the SE schemas).
- Removed as now-unreferenced: `DescribeLayer.xsd`, `GetMap.xsd`,
  `sld_capabilities.xsd`, and the `http/schemas.opengis.net/{ows,wfs,wms}/`
  subtrees.

## GML 3.1.1 note

GML 3.1.1 is not strictly XSD-1.0-valid (a well-known defect: e.g.
`AbstractReferenceSystemBaseType` in `referenceSystems.xsd` is an illegal
`<xsd:restriction>`). `libxml2`/`lxml` reject the whole graph over it;
`xmlschema` rejects it too under strict schema-building. The test helper
therefore builds the schema with `validation='lax'`, which records the
internal GML defects as warnings instead of aborting, while still validating
instance documents correctly. SLD style documents emitted by this codec use no
GML content, so the GML subgraph is only pulled in to satisfy the imports.

## Licence

OGC schemas are published by the Open Geospatial Consortium under terms that
permit redistribution (see the `<copyright>` annotation inside each `.xsd` and
<https://www.ogc.org/legal/>). The two W3C schemas are under the W3C Software
and Document licence.
