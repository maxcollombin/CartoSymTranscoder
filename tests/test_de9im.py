"""Tests for cartosym_transcoder.models.de9im — DE-9IM lookup table and utilities."""

import pytest

from cartosym_transcoder.models.de9im import (
    DE9IM_PREDICATES,
    CQL2_SPATIAL_PREDICATES,
    match_pattern,
    is_valid_de9im,
    predicate_matches,
    get_patterns,
)


# ── is_valid_de9im ────────────────────────────────────────────────────────

class TestIsValidDE9IM:
    """Validate that well-formed DE-9IM matrices are recognised."""

    @pytest.mark.parametrize("matrix", [
        "212101212",
        "FF2FF1212",
        "0FFFFFFF2",
        "F0FFFF012",
        "FFFFFFFFF",
        "000000000",
        "222222222",
    ])
    def test_valid(self, matrix: str):
        assert is_valid_de9im(matrix) is True

    @pytest.mark.parametrize("matrix,reason", [
        ("T*F**FFF*", "pattern chars not allowed in matrix"),
        ("short", "too short"),
        ("0123456789", "too long"),
        ("21210121X", "invalid char X"),
        ("", "empty"),
    ])
    def test_invalid(self, matrix: str, reason: str):
        assert is_valid_de9im(matrix) is False, reason


# ── match_pattern ─────────────────────────────────────────────────────────

class TestMatchPattern:
    """Test single-pattern matching (Python port of DE9IM::match)."""

    def test_exact_match(self):
        assert match_pattern("212101212", "212101212") is True

    def test_wildcard_star(self):
        assert match_pattern("212101212", "*********") is True

    def test_T_matches_non_F(self):
        assert match_pattern("212101212", "T*T***T**") is True

    def test_T_rejects_F(self):
        assert match_pattern("FF2FF1212", "T********") is False

    def test_disjoint_pattern(self):
        assert match_pattern("FF2FF1212", "FF*FF****") is True

    def test_contains_pattern(self):
        assert match_pattern("212FF1FF2", "T*****FF*") is True

    def test_equals_pattern(self):
        assert match_pattern("0FFFFFFF2", "T*F**FFF*") is True

    def test_within_pattern(self):
        assert match_pattern("0FF0FFF02", "T*F**F***") is True

    def test_case_insensitive(self):
        assert match_pattern("ff2ff1212", "FF*FF****") is True

    def test_wrong_lengths(self):
        with pytest.raises(ValueError, match="exactly 9 characters"):
            match_pattern("212", "T*T***T**")
        with pytest.raises(ValueError, match="exactly 9 characters"):
            match_pattern("212101212", "T*T")


# ── predicate_matches ─────────────────────────────────────────────────────

class TestPredicateMatches:
    """Test named-predicate lookup and matching."""

    def test_disjoint(self):
        assert predicate_matches("FF2FF1212", "disjoint") is True

    def test_not_disjoint(self):
        assert predicate_matches("212101212", "disjoint") is False

    def test_intersects_positive(self):
        """intersects is ¬disjoint."""
        assert predicate_matches("212101212", "intersects") is True

    def test_intersects_negative(self):
        assert predicate_matches("FF2FF1212", "intersects") is False

    def test_contains(self):
        assert predicate_matches("212FF1FF2", "contains") is True

    def test_within(self):
        assert predicate_matches("0FF0FFF02", "within") is True

    def test_equals(self):
        assert predicate_matches("0FFFFFFF2", "equals") is True

    def test_touches_variant1(self):
        """FT******* — boundary intersection."""
        assert predicate_matches("FT0000000", "touches") is True

    def test_touches_variant2(self):
        """F**T***** — interior-boundary."""
        assert predicate_matches("F00T00000", "touches") is True

    def test_overlaps(self):
        assert predicate_matches("212101212", "overlaps") is True

    def test_cql2_prefix_stripped(self):
        """s_ prefix is stripped before lookup."""
        assert predicate_matches("212101212", "s_overlaps") is True
        assert predicate_matches("FF2FF1212", "s_disjoint") is True

    def test_unknown_predicate(self):
        with pytest.raises(ValueError, match="Unknown spatial predicate"):
            predicate_matches("212101212", "not_a_predicate")


# ── get_patterns ──────────────────────────────────────────────────────────

class TestGetPatterns:
    """Test pattern retrieval by predicate name."""

    def test_single_pattern(self):
        assert get_patterns("contains") == ["T*****FF*"]

    def test_multi_pattern(self):
        patterns = get_patterns("touches")
        assert len(patterns) == 3
        assert "FT*******" in patterns

    def test_cql2_prefix(self):
        assert get_patterns("s_contains") == ["T*****FF*"]

    def test_empty_for_intersects(self):
        """intersects has no patterns (it's ¬disjoint)."""
        assert get_patterns("intersects") == []

    def test_unknown_raises(self):
        with pytest.raises(ValueError):
            get_patterns("bogus")


# ── Table integrity ───────────────────────────────────────────────────────

class TestTableIntegrity:
    """Verify the lookup tables are consistent."""

    def test_all_patterns_are_9_chars(self):
        for pred, patterns in DE9IM_PREDICATES.items():
            for p in patterns:
                assert len(p) == 9, f"{pred}: pattern {p!r} is {len(p)} chars"

    def test_all_pattern_chars_valid(self):
        valid = set("012TF*tf")
        for pred, patterns in DE9IM_PREDICATES.items():
            for p in patterns:
                for ch in p:
                    assert ch in valid, f"{pred}: invalid char {ch!r} in {p!r}"

    def test_cql2_map_covers_all_predicates(self):
        """Every DE9IM predicate has a matching s_ CQL2 name."""
        for pred in DE9IM_PREDICATES:
            assert f"s_{pred}" in CQL2_SPATIAL_PREDICATES

    def test_cql2_map_values_exist(self):
        """Every CQL2 mapping points to a known predicate."""
        for cql2_name, pred_name in CQL2_SPATIAL_PREDICATES.items():
            assert pred_name in DE9IM_PREDICATES
