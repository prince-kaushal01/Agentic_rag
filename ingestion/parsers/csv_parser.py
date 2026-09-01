from pathlib import Path
import csv
from ingestion.parsers.base import BaseParser, ParsedDocument


class CSVParser(BaseParser):
    supported_extensions = [".csv"]

    def parse(self, path: Path) -> ParsedDocument:
        rows = []
        headers = []

        with open(path, encoding="utf-8", errors="replace", newline="") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames or []
            for row in reader:
                rows.append(row)

        # Convert to readable text blocks — each row becomes a sentence
        text_parts = [f"Columns: {', '.join(headers)}\n"]
        for i, row in enumerate(rows, 1):
            line = " | ".join(f"{k}: {v}" for k, v in row.items() if v)
            text_parts.append(f"Row {i}: {line}")

        return ParsedDocument(
            file_name=path.name,
            file_type="csv",
            title=path.stem.replace("_", " ").replace("-", " "),
            content="\n".join(text_parts),
            metadata={
                "total_rows": len(rows),
                "columns": headers,
                "source_path": str(path),
            },
        )
