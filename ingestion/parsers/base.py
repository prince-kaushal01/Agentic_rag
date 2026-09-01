from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ParsedDocument:
    """Raw output from any parser — handed to the chunker."""
    file_name: str
    file_type: str
    title: str
    content: str                        # full extracted text
    pages: list[dict] = field(default_factory=list)   # [{page: 1, text: "..."}]
    sections: list[dict] = field(default_factory=list) # [{title: "...", text: "..."}]
    metadata: dict = field(default_factory=dict)


class BaseParser:
    supported_extensions: list[str] = []

    def can_parse(self, path: Path) -> bool:
        return path.suffix.lower() in self.supported_extensions

    def parse(self, path: Path) -> ParsedDocument:
        raise NotImplementedError
