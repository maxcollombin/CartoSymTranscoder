"""Tests for the .include directive preprocessing."""

import pytest
from pathlib import Path

from cartosym_transcoder.parser import CartoSymParser

INPUT_DIR = Path(__file__).resolve().parent.parent / "input"


def _rule_selector_name(rule) -> str | None:
    """Extract the top-level identifier name from a rule's selector/selectors.

    In the AST, a simple ``[Landuse]`` selector is stored as
    ``rule.selectors[0].conditions[0].name`` (IdentifierExpression).
    """
    if getattr(rule, 'selectors', None):
        sel = rule.selectors[0]
        if getattr(sel, 'conditions', None):
            cond = sel.conditions[0]
            if hasattr(cond, 'name'):
                return cond.name
    return rule.name


class TestIncludeDirective:
    """Tests for .include directive resolution in CSCSS files."""

    def setup_method(self):
        self.parser = CartoSymParser()

    # ── Detection & resolution ────────────────────────────────────

    def test_include_resolves_file_content(self, tmp_path):
        """An .include directive should inline the referenced file content."""
        child = tmp_path / "child.cscss"
        child.write_text("[Landuse]\n{\n   visibility: false;\n}\n")

        parent = tmp_path / "parent.cscss"
        parent.write_text(f".include 'child.cscss'\n")

        result = self.parser.parse_file(parent)
        assert result.styling_rules is not None
        assert len(result.styling_rules.rules) >= 1
        assert _rule_selector_name(result.styling_rules.rules[0]) == "Landuse"

    def test_include_preserves_local_rules(self, tmp_path):
        """Rules after .include directives should be preserved."""
        child = tmp_path / "child.cscss"
        child.write_text("[Layer1]\n{\n   visibility: false;\n}\n")

        parent = tmp_path / "parent.cscss"
        parent.write_text(
            ".include 'child.cscss'\n\n"
            "[Layer2]\n{\n   opacity: 0.5;\n}\n"
        )

        result = self.parser.parse_file(parent)
        assert result.styling_rules is not None
        rule_names = [_rule_selector_name(r) for r in result.styling_rules.rules]
        assert "Layer1" in rule_names
        assert "Layer2" in rule_names

    def test_multiple_includes(self, tmp_path):
        """Multiple .include directives should all be resolved in order."""
        a = tmp_path / "a.cscss"
        a.write_text("[LayerA]\n{\n   visibility: true;\n}\n")

        b = tmp_path / "b.cscss"
        b.write_text("[LayerB]\n{\n   visibility: false;\n}\n")

        main = tmp_path / "main.cscss"
        main.write_text(
            ".include 'a.cscss'\n"
            ".include 'b.cscss'\n"
        )

        result = self.parser.parse_file(main)
        assert result.styling_rules is not None
        rule_names = [_rule_selector_name(r) for r in result.styling_rules.rules]
        assert rule_names == ["LayerA", "LayerB"]

    # ── Relative path resolution ──────────────────────────────────

    def test_include_relative_to_parent_file(self, tmp_path):
        """Paths in .include should resolve relative to the including file."""
        subdir = tmp_path / "styles"
        subdir.mkdir()

        child = subdir / "base.cscss"
        child.write_text("[Base]\n{\n   visibility: true;\n}\n")

        parent = tmp_path / "main.cscss"
        parent.write_text(".include 'styles/base.cscss'\n")

        result = self.parser.parse_file(parent)
        assert result.styling_rules is not None
        assert _rule_selector_name(result.styling_rules.rules[0]) == "Base"

    # ── Recursive includes ────────────────────────────────────────

    def test_recursive_include(self, tmp_path):
        """A file included by another include should be resolved recursively."""
        grandchild = tmp_path / "grandchild.cscss"
        grandchild.write_text("[Deep]\n{\n   visibility: true;\n}\n")

        child = tmp_path / "child.cscss"
        child.write_text(".include 'grandchild.cscss'\n")

        parent = tmp_path / "parent.cscss"
        parent.write_text(".include 'child.cscss'\n")

        result = self.parser.parse_file(parent)
        assert result.styling_rules is not None
        assert _rule_selector_name(result.styling_rules.rules[0]) == "Deep"

    # ── Error cases ───────────────────────────────────────────────

    def test_include_file_not_found(self, tmp_path):
        """Including a nonexistent file should raise FileNotFoundError."""
        parent = tmp_path / "main.cscss"
        parent.write_text(".include 'nonexistent.cscss'\n")

        with pytest.raises(FileNotFoundError, match="nonexistent.cscss"):
            self.parser.parse_file(parent)

    def test_circular_include_raises_error(self, tmp_path):
        """Circular includes should raise ValueError."""
        a = tmp_path / "a.cscss"
        b = tmp_path / "b.cscss"

        a.write_text(".include 'b.cscss'\n")
        b.write_text(".include 'a.cscss'\n")

        with pytest.raises(ValueError, match="[Cc]ircular"):
            self.parser.parse_file(a)

    # ── Integration with real input files ─────────────────────────

    def test_include_example_file_parses(self):
        """The example input/12-include.cscss should parse without errors."""
        include_file = INPUT_DIR / "12-include.cscss"
        if not include_file.exists():
            pytest.skip("input/12-include.cscss not found")

        result = self.parser.parse_file(include_file)
        assert result.styling_rules is not None
        # Should contain rules from both included files + the local rule
        assert len(result.styling_rules.rules) >= 2

    def test_parse_string_ignores_includes(self):
        """parse_string() should not resolve includes (no file context)."""
        content = ".include 'some.cscss'\n[Layer]\n{\n   visibility: true;\n}\n"
        # parse_string has no base_dir, so .include lines should be
        # treated as unknown directives (ignored or passed through)
        result = self.parser.parse_string(content)
        assert result.styling_rules is not None
