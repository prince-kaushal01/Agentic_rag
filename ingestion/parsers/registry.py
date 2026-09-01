from pathlib import Path
from ingestion.parsers.base import BaseParser, ParsedDocument
from ingestion.parsers.pdf_parser import PDFParser
from ingestion.parsers.docx_parser import DOCXParser
from ingestion.parsers.markdown_parser import MarkdownParser
from ingestion.parsers.csv_parser import CSVParser
from ingestion.parsers.excel_parser import ExcelParser

_PARSERS: list[BaseParser] = [
    PDFParser(),
    DOCXParser(),
    MarkdownParser(),
    CSVParser(),
    ExcelParser(),
]


def parse_file(path: Path) -> ParsedDocument:
    """Auto-detect parser by file extension and return a ParsedDocument."""
    path = Path(path)
    for parser in _PARSERS:
        if parser.can_parse(path):
            return parser.parse(path)
    raise ValueError(f"No parser available for file type: {path.suffix!r}")


def supported_extensions() -> list[str]:
    exts = []
    for p in _PARSERS:
        exts.extend(p.supported_extensions)
    return exts
