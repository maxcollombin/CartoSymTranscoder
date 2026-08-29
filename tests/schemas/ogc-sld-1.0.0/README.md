# Vendored OGC SLD 1.0.0 XML Schemas

A **local, self-contained copy** of the OGC schema graph needed to
XML-Schema-validate SLD 1.0.0 *style documents* produced (and consumed) by
`cartosym_transcoder.codecs.sld` in its SLD 1.0.0 dialect. Used only by the
test suite (`tests/_xsd.py`, `tests/test_sld10_corpus.py`) — not imported at
runtime, not part of the distributed package.

## Provenance

- Source: <http://schemas.opengis.net/> (the canonical OGC schema repository)
- Retrieved: 2026-08-29
- Entry point: `sld/1.0.0/StyledLayerDescriptor.xsd`, which pulls in
  transitively: Filter Encoding 1.0.0 (`filter/1.0.0/`), GML 2.1.2
  (`gml/2.1.2/`), and the two W3C schemas `xlink.xsd` / `xml.xsd`.
- Fetched with `xmlschema.download_schemas(...)`, which mirrors every remote
  `schemaLocation` under `http/<host>/<path>` and leaves the schema text
  otherwise untouched. Load the tree by pointing an XSD parser at
  `StyledLayerDescriptor.xsd` in this directory — the `http/` mirror is
  resolved automatically by relative path, no network access required.

## Local modifications

None. Unlike the SLD 1.1.0 graph, the SLD 1.0.0
`StyledLayerDescriptor.xsd` does not include the WMS operation schemas
(`DescribeLayer` / `GetMap` / `sld_capabilities`), so nothing had to be
trimmed — the 9 files here are exactly what the entry point references.

## GML 2.1.2 note

Like GML 3.1.1 in the SLD 1.1.0 graph, GML 2.1.2 is not perfectly
XSD-1.0-valid. `tests/_xsd.py` therefore builds this schema with
`validation='lax'` too. SLD style documents emitted by this codec use no
GML content; the GML subgraph is only pulled in to satisfy imports.

## Licence

OGC schemas are published by the Open Geospatial Consortium under terms that
permit redistribution (see the `<copyright>` annotation inside each `.xsd`
and <https://www.ogc.org/legal/>). The two W3C schemas are under the W3C
Software and Document licence.
