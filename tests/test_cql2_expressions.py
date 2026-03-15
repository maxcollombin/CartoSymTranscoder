"""Tests for CQL2 expression models (GeometryLiteral, BboxLiteral, TemporalLiteral,
SpatialPredicate, SpatialRelatePredicate, TemporalPredicate, ArrayPredicate)."""

import pytest
from pydantic import ValidationError

from cartosym_transcoder.models.expressions import (
    SpatialPredicate,
    SpatialRelatePredicate,
    TemporalPredicate,
    ArrayPredicate,
    GeometryLiteral,
    BboxLiteral,
    TemporalLiteral,
    GeometryExpression,
    TemporalExpression,
)


# ── SpatialPredicate ──────────────────────────────────────────────────────

class TestSpatialPredicate:

    def test_cql2_op(self):
        sp = SpatialPredicate(op="s_intersects", args=[])
        assert sp.op == "s_intersects"

    def test_legacy_op(self):
        sp = SpatialPredicate(op="intersects", args=[])
        assert sp.op == "intersects"

    def test_normalised_op_already_prefixed(self):
        sp = SpatialPredicate(op="s_contains", args=[])
        assert sp.normalised_op() == "s_contains"

    def test_normalised_op_legacy(self):
        sp = SpatialPredicate(op="within", args=[])
        assert sp.normalised_op() == "s_within"

    def test_all_cql2_ops_accepted(self):
        ops = [
            "s_intersects", "s_contains", "s_within", "s_touches",
            "s_crosses", "s_disjoint", "s_overlaps", "s_equals",
        ]
        for op in ops:
            sp = SpatialPredicate(op=op, args=[])
            assert sp.normalised_op() == op


# ── SpatialRelatePredicate ────────────────────────────────────────────────

class TestSpatialRelatePredicate:

    def test_valid_pattern(self):
        g1 = GeometryExpression()
        g2 = GeometryExpression()
        srp = SpatialRelatePredicate(args=[g1, g2], pattern="T*F**FFF*")
        assert srp.op == "s_relate"
        assert srp.pattern == "T*F**FFF*"

    def test_lowercase_pattern_accepted(self):
        g1 = GeometryExpression()
        g2 = GeometryExpression()
        srp = SpatialRelatePredicate(args=[g1, g2], pattern="tf*ffff**")
        assert srp.pattern == "tf*ffff**"

    def test_invalid_pattern_chars(self):
        with pytest.raises(ValidationError):
            SpatialRelatePredicate(args=[], pattern="XYZXYZXYZ")

    def test_pattern_too_short(self):
        with pytest.raises(ValidationError):
            SpatialRelatePredicate(args=[], pattern="T*F")

    def test_pattern_too_long(self):
        with pytest.raises(ValidationError):
            SpatialRelatePredicate(args=[], pattern="T*F**FFF*X")


# ── TemporalPredicate ────────────────────────────────────────────────────

class TestTemporalPredicate:

    def test_cql2_op(self):
        tp = TemporalPredicate(op="t_before", args=[])
        assert tp.op == "t_before"

    def test_legacy_op(self):
        tp = TemporalPredicate(op="before", args=[])
        assert tp.normalised_op() == "t_before"

    def test_all_15_cql2_temporal_ops(self):
        ops = [
            "t_before", "t_after", "t_meets", "t_metby",
            "t_overlaps", "t_overlappedby", "t_begins", "t_begunby",
            "t_during", "t_contains", "t_ends", "t_endedby",
            "t_equals", "t_intersects", "t_disjoint",
        ]
        for op in ops:
            tp = TemporalPredicate(op=op, args=[])
            assert tp.normalised_op() == op


# ── ArrayPredicate ────────────────────────────────────────────────────────

class TestArrayPredicate:

    def test_cql2_op(self):
        ap = ArrayPredicate(op="a_contains", args=[])
        assert ap.op == "a_contains"

    def test_legacy_op(self):
        ap = ArrayPredicate(op="acontains", args=[])
        assert ap.op == "acontains"


# ── GeometryLiteral ──────────────────────────────────────────────────────

class TestGeometryLiteral:

    def test_point(self):
        gl = GeometryLiteral(geom_type="Point", coordinates=[1.0, 2.0])
        assert gl.geom_type == "Point"
        assert gl.to_geojson() == {"type": "Point", "coordinates": [1.0, 2.0]}

    def test_polygon(self):
        coords = [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]
        gl = GeometryLiteral(geom_type="Polygon", coordinates=coords)
        geojson = gl.to_geojson()
        assert geojson["type"] == "Polygon"
        assert geojson["coordinates"] == coords

    def test_geometry_collection(self):
        gc = GeometryLiteral(
            geom_type="GeometryCollection",
            geometries=[
                GeometryLiteral(geom_type="Point", coordinates=[0, 0]),
                GeometryLiteral(geom_type="Point", coordinates=[1, 1]),
            ],
        )
        geojson = gc.to_geojson()
        assert geojson["type"] == "GeometryCollection"
        assert len(geojson["geometries"]) == 2

    def test_from_geojson_point(self):
        data = {"type": "Point", "coordinates": [3.5, 48.8]}
        gl = GeometryLiteral.from_geojson(data)
        assert gl.geom_type == "Point"
        assert gl.coordinates == [3.5, 48.8]

    def test_from_geojson_collection(self):
        data = {
            "type": "GeometryCollection",
            "geometries": [
                {"type": "Point", "coordinates": [0, 0]},
            ],
        }
        gl = GeometryLiteral.from_geojson(data)
        assert gl.geom_type == "GeometryCollection"
        assert gl.geometries is not None
        assert len(gl.geometries) == 1

    def test_roundtrip_geojson(self):
        original = {"type": "LineString", "coordinates": [[0, 0], [1, 1], [2, 0]]}
        gl = GeometryLiteral.from_geojson(original)
        assert gl.to_geojson() == original

    def test_crs_optional(self):
        gl = GeometryLiteral(
            geom_type="Point", coordinates=[0, 0], crs="EPSG:4326"
        )
        assert gl.crs == "EPSG:4326"

    def test_invalid_geom_type(self):
        with pytest.raises(ValidationError):
            GeometryLiteral(geom_type="Circle", coordinates=[0, 0])


# ── BboxLiteral ───────────────────────────────────────────────────────────

class TestBboxLiteral:

    def test_2d_bbox(self):
        bb = BboxLiteral(bbox=[0.0, 0.0, 1.0, 1.0])
        assert bb.to_cql2_json() == {"bbox": [0.0, 0.0, 1.0, 1.0]}

    def test_3d_bbox(self):
        bb = BboxLiteral(bbox=[0.0, 0.0, -10.0, 1.0, 1.0, 10.0])
        assert len(bb.bbox) == 6

    def test_too_few_values(self):
        with pytest.raises(ValidationError):
            BboxLiteral(bbox=[0.0, 0.0, 1.0])

    def test_too_many_values(self):
        with pytest.raises(ValidationError):
            BboxLiteral(bbox=[0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0])


# ── TemporalLiteral ──────────────────────────────────────────────────────

class TestTemporalLiteral:

    def test_date(self):
        tl = TemporalLiteral(temporal_type="date", value="2024-01-01")
        assert tl.to_cql2_json() == {"date": "2024-01-01"}

    def test_timestamp(self):
        tl = TemporalLiteral(temporal_type="timestamp", value="2024-01-01T12:00:00Z")
        assert tl.to_cql2_json() == {"timestamp": "2024-01-01T12:00:00Z"}

    def test_interval(self):
        tl = TemporalLiteral(
            temporal_type="interval",
            interval=["2024-01-01", "2024-12-31"],
        )
        assert tl.to_cql2_json() == {"interval": ["2024-01-01", "2024-12-31"]}

    def test_from_cql2_json_date(self):
        tl = TemporalLiteral.from_cql2_json({"date": "2020-06-15"})
        assert tl.temporal_type == "date"
        assert tl.value == "2020-06-15"

    def test_from_cql2_json_timestamp(self):
        tl = TemporalLiteral.from_cql2_json({"timestamp": "2020-06-15T08:00:00Z"})
        assert tl.temporal_type == "timestamp"

    def test_from_cql2_json_interval(self):
        tl = TemporalLiteral.from_cql2_json({"interval": ["2020-01-01", "2020-12-31"]})
        assert tl.temporal_type == "interval"
        assert tl.interval == ["2020-01-01", "2020-12-31"]

    def test_from_cql2_json_unknown(self):
        with pytest.raises(ValueError, match="Unknown temporal literal format"):
            TemporalLiteral.from_cql2_json({"foo": "bar"})

    def test_roundtrip_date(self):
        data = {"date": "2025-03-14"}
        tl = TemporalLiteral.from_cql2_json(data)
        assert tl.to_cql2_json() == data

    def test_roundtrip_interval(self):
        data = {"interval": ["2025-01-01", "2025-06-30"]}
        tl = TemporalLiteral.from_cql2_json(data)
        assert tl.to_cql2_json() == data
