from pathlib import Path
import re
from ingestion.parsers.base import BaseParser, ParsedDocument


class MarkdownParser(BaseParser):
    supported_extensions = [".md", ".markdown", ".txt"]

    def parse(self, path: Path) -> ParsedDocument:
        raw = path.read_text(encoding="utf-8", errors="replace")
        sections = []
        current_section = {"title": "Introduction", "text": ""}

        for line in raw.splitlines():
            heading = re.match(r"^(#{1,3})\s+(.+)", line)
            if heading:
                if current_section["text"].strip():
                    sections.append(current_section)
                current_section = {"title": heading.group(2).strip(), "text": ""}
            else:
                current_section["text"] += line + "\n"

        if current_section["text"].strip():
            sections.append(current_section)

        # Strip markdown syntax for plain content
        clean = re.sub(r"[#*`_>\[\]!]", "", raw)
        clean = re.sub(r"\n{3,}", "\n\n", clean).strip()

        return ParsedDocument(
            file_name=path.name,
            file_type=path.suffix.lstrip(".") or "txt",
            title=path.stem.replace("_", " ").replace("-", " "),
            content=clean,
            sections=sections,
            metadata={"total_sections": len(sections), "source_path": str(path)},
        )
