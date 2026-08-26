"""
Abstract base class for format codecs.

Each codec provides a reader (format → Style) and a writer (Style → format).
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, List, Union

from ..models.styles import Style


class CodecReader(ABC):
    """Abstract reader: converts a specific format into a Style model."""

    @abstractmethod
    def read(self, source: Union[str, Path]) -> Style:
        """Read *source* (file path or string content) and return a Style model.

        Parameters
        ----------
        source : str | Path
            Either a filesystem path to the input file, or the raw string
            content in the source format.

        Returns
        -------
        Style
            Validated Pydantic Style model.
        """
        ...


class CodecWriter(ABC):
    """Abstract writer: converts a Style model into a specific format."""

    @abstractmethod
    def write(self, style: Style) -> Any:
        """Serialise *style* into the target format.

        Parameters
        ----------
        style : Style
            Pydantic Style model to serialise.

        Returns
        -------
        str | dict
            The serialised output (string for text formats, dict for JSON).
        """
        ...


class Codec:
    """Container that pairs a reader and a writer for a given format.

    Attributes
    ----------
    format_name : str
        Human-readable name of the format (e.g. ``"CartoSym-CSS"``).
    extensions : list[str]
        File extensions handled by this codec, **with leading dot**
        (e.g. ``[".cscss"]``).
    reader : CodecReader | None
        Reader instance, or *None* if the format is write-only.
    writer : CodecWriter | None
        Writer instance, or *None* if the format is read-only.
    """

    def __init__(
        self,
        format_name: str,
        extensions: List[str],
        reader: CodecReader = None,
        writer: CodecWriter = None,
    ):
        self.format_name = format_name
        self.extensions = extensions
        self.reader = reader
        self.writer = writer

    def read(self, source: Union[str, Path]) -> Style:
        """Delegate to the reader."""
        if self.reader is None:
            raise NotImplementedError(
                f"Reading is not supported for format '{self.format_name}'"
            )
        return self.reader.read(source)

    def write(self, style: Style) -> Any:
        """Delegate to the writer."""
        if self.writer is None:
            raise NotImplementedError(
                f"Writing is not supported for format '{self.format_name}'"
            )
        return self.writer.write(style)

    def __repr__(self) -> str:
        r = "R" if self.reader else "-"
        w = "W" if self.writer else "-"
        return f"<Codec '{self.format_name}' [{r}{w}] {self.extensions}>"
