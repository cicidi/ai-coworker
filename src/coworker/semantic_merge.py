# src/coworker/semantic_merge.py
import re
from dataclasses import dataclass

OUTDATED = "OUTDATED"
OVERWRITE = "OVERWRITE"
MERGE_ADD = "MERGE_ADD"
KEEP = "KEEP"


@dataclass
class SectionClassification:
    heading: str
    category: str
    current_content: str = ""
    future_content: str = ""


def _parse_sections(content: str) -> dict[str, str]:
    """Parse markdown content into dict of heading → section body."""
    sections: dict[str, str] = {}
    pattern = r"^(#{1,3}\s+.+)$"
    lines = content.split("\n")
    current_heading = "_header"
    current_body: list[str] = []

    for line in lines:
        if re.match(pattern, line):
            if current_body:
                sections[current_heading] = "\n".join(current_body).strip()
            current_heading = line.strip()
            current_body = []
        else:
            current_body.append(line)
    if current_body:
        sections[current_heading] = "\n".join(current_body).strip()

    return sections


def classify_sections(current: str, future: str) -> list[SectionClassification]:
    """Compare current and future CLAUDE.md, classify each section."""
    current_sections = _parse_sections(current)
    future_sections = _parse_sections(future)
    classifications: list[SectionClassification] = []

    for heading, cur_content in current_sections.items():
        if heading == "_header":
            continue
        if "<!-- PROTECTED" in cur_content or "<!-- INITIATIVE:" in cur_content:
            classifications.append(
                SectionClassification(heading=heading, category=KEEP, current_content=cur_content)
            )
            continue
        if heading in future_sections:
            fut_content = future_sections[heading]
            if cur_content.strip() != fut_content.strip():
                classifications.append(
                    SectionClassification(
                        heading=heading, category=OVERWRITE,
                        current_content=cur_content, future_content=fut_content,
                    )
                )
            else:
                classifications.append(
                    SectionClassification(heading=heading, category=KEEP, current_content=cur_content)
                )
        else:
            classifications.append(
                SectionClassification(heading=heading, category=KEEP, current_content=cur_content)
            )

    for heading, fut_content in future_sections.items():
        if heading == "_header":
            continue
        if heading not in current_sections:
            classifications.append(
                SectionClassification(heading=heading, category=MERGE_ADD, future_content=fut_content)
            )

    return classifications


def apply_merge(
    classifications: list[SectionClassification],
    current: str,
    future: str,
) -> str:
    """Apply classified changes to produce merged CLAUDE.md."""
    current_sections = _parse_sections(current)
    output_lines: list[str] = []

    header = current_sections.get("_header", "")
    if header:
        output_lines.append(header)
        output_lines.append("")

    for heading, cur_content in current_sections.items():
        if heading == "_header":
            continue
        match = [c for c in classifications if c.heading == heading]
        if not match:
            output_lines.append(heading)
            output_lines.append("")
            output_lines.append(cur_content)
            output_lines.append("")
            continue

        c = match[0]
        if c.category == KEEP:
            output_lines.append(heading)
            output_lines.append("")
            output_lines.append(cur_content)
            output_lines.append("")
        elif c.category == OVERWRITE:
            output_lines.append(heading)
            output_lines.append("")
            output_lines.append(c.future_content)
            output_lines.append("")

    for c in classifications:
        if c.category == MERGE_ADD:
            output_lines.append(c.heading)
            output_lines.append("")
            output_lines.append(c.future_content)
            output_lines.append("")

    return "\n".join(output_lines).strip() + "\n"
