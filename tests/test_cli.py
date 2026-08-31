"""CLI behaviour: exit codes, streams, quiet mode, diagnostics."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = ROOT / "examples"


def run(*argv: str, **kw) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "pycartosym.cli", *argv],
        cwd=ROOT,
        capture_output=True,
        text=True,
        **kw,
    )


class TestExitCodes:
    def test_no_args_prints_help_and_exits_usage(self):
        r = run()
        assert r.returncode == 1

    def test_missing_input_file_is_not_found(self):
        r = run("does-not-exist.cscss", "--print")
        assert r.returncode == 2
        assert "file not found" in r.stderr

    def test_syntax_error_is_input_invalid(self, tmp_path: Path):
        bad = tmp_path / "bad.cscss"
        bad.write_text("Fill {\n  color: ;\n}\n", encoding="utf-8")
        r = run("validate", str(bad))
        assert r.returncode == 3
        assert "syntax error" in r.stderr
        # position + caret
        assert f"{bad}:2:" in r.stderr
        assert "^" in r.stderr

    def test_unknown_conversion_is_unsupported(self, tmp_path: Path):
        src = tmp_path / "x.weird"
        src.write_text("{}", encoding="utf-8")
        r = run(str(src), "--print")
        assert r.returncode == 4

    def test_transcode_gap_is_its_own_code(self):
        r = run(str(EXAMPLES / "0-basic.cscss"), "--to-format", "maplibre", "--print")
        assert r.returncode == 5


class TestStreamsAndQuiet:
    def test_success_note_on_stdout_by_default(self, tmp_path: Path):
        out = tmp_path / "out.cs.json"
        r = run(str(EXAMPLES / "0-basic.cscss"), "-o", str(out))
        assert r.returncode == 0
        assert out.exists()
        assert r.stdout.strip().startswith("ok:")

    def test_quiet_silences_success_note(self, tmp_path: Path):
        out = tmp_path / "out.cs.json"
        r = run(str(EXAMPLES / "0-basic.cscss"), "-o", str(out), "-q")
        assert r.returncode == 0
        assert r.stdout == ""

    def test_errors_go_to_stderr(self):
        r = run("nope.cscss", "--print")
        assert r.stdout == ""
        assert "error:" in r.stderr


class TestConversion:
    def test_print_defaults_to_the_other_text_encoding(self):
        r = run(str(EXAMPLES / "0-basic.cscss"), "--print")
        assert r.returncode == 0
        assert '"stylingRules"' in r.stdout

    def test_output_needs_force_to_overwrite(self, tmp_path: Path):
        out = tmp_path / "out.cs.json"
        out.write_text("x", encoding="utf-8")
        r = run(str(EXAMPLES / "0-basic.cscss"), "-o", str(out))
        assert r.returncode == 1
        assert "--force" in r.stderr

    @pytest.mark.parametrize("no_color", ["1", None])
    def test_no_color_env_strips_ansi(self, no_color: str | None):
        env = {"PATH": __import__("os").environ["PATH"]}
        if no_color is not None:
            env["NO_COLOR"] = no_color
        r = run("nope.cscss", "--print", env=env)
        assert "\033[" not in r.stderr
