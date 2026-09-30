"""
Stage 2 of the pipeline: splitting documents into chunks.

`split_documents` cuts each city guide at its "##" headings, so every chunk
is one section: one topic, such as a town's "Getting there" or "Where to
stay". The paragraph before a guide's first heading becomes its own
"Overview" chunk. Every chunk opens with a header naming its guide and
section, and there is no overlap between chunks.

`fallback_split` is the starter's original fixed-size chunker, kept so unit 2
has something to compare against. It still reads CHUNK_SIZE and CHUNK_OVERLAP
from config.py; `split_documents` uses neither.
"""

import re
from dataclasses import dataclass
from pathlib import Path

import config
from ingest import Document

_TITLE_LINE = re.compile(r"\A#[ \t]+(?P<title>[^\n]+)")
_SECTION_HEADING = re.compile(r"^##[ \t]+(?P<heading>[^\n]+)$", re.MULTILINE)

# The paragraph between a guide's title and its first "##" heading has no
# heading of its own. Naming it lets it stand as a section like the others.
INTRO_HEADING = "Overview"


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


@dataclass(frozen=True)
class Section:
    """One headed part of a guide, such as Halden Bay's "Getting there"."""

    guide_title: str
    heading: str
    body: str


def _split_title(document: Document) -> tuple[str, str]:
    """
    Separate a guide's "# Title" line from the text beneath it.

    Args:
        document: The guide to split.

    Returns:
        The title and the text after it. A guide with no title line is
        titled by its filename stem instead, so its sections still say
        which guide they belong to.
    """
    match = _TITLE_LINE.match(document.text)
    if match is None:
        return Path(document.source).stem, document.text
    return match.group("title").strip(), document.text[match.end():]


def parse_sections(document: Document) -> list[Section]:
    """
    Break one guide into its headed sections, in reading order.

    Text before the first "##" heading becomes an "Overview" section. A
    heading with nothing under it is dropped, because on its own it would
    be a chunk that can answer nothing.

    Args:
        document: A guide as loaded by `ingest.load_documents`.

    Returns:
        The guide's non-empty sections. A guide with no "##" headings comes
        back as a single "Overview" section.

    Raises:
        TypeError: If `document` is not a `Document`.
    """
    if not isinstance(document, Document):
        raise TypeError(
            f"expected a Document, got {type(document).__name__}"
        )

    title, remainder = _split_title(document)
    heading_matches = list(_SECTION_HEADING.finditer(remainder))

    # The intro ends where the first heading starts, and each section ends
    # where the next one starts. With no headings the only boundary is the
    # end of the text, so the whole guide becomes the intro.
    boundaries = [match.start() for match in heading_matches]
    boundaries.append(len(remainder))

    intro = remainder[:boundaries[0]].strip()
    sections = [Section(title, INTRO_HEADING, intro)]

    for match, end in zip(heading_matches, boundaries[1:], strict=True):
        heading = match.group("heading").strip()
        body = remainder[match.end():end].strip()
        sections.append(Section(title, heading, body))

    return [section for section in sections if section.body]


def _chunk_text(section: Section) -> str:
    """
    Render a section as the text that gets embedded and retrieved.

    Args:
        section: The section to render.

    Returns:
        A "Guide title: Section heading" line, a blank line, then the body.
    """
    # Most town sections never name their town, and nine "Practical notes"
    # sections are word-for-word identical. The header is the only thing
    # that tells them apart, for the embedding and for whoever reads it.
    return f"{section.guide_title}: {section.heading}\n\n{section.body}"


def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Split guides into chunks, one per headed section.

    No overlap between chunks: each section is one topic, and text borrowed
    from a neighbouring section would mix two.

    Args:
        documents: Guides as loaded by `ingest.load_documents`.

    Returns:
        Chunks in document order, numbered from 0 within each source file.

    Raises:
        TypeError: If `documents` is not a list of `Document`s.
        ValueError: If `documents` is empty.
    """
    if not isinstance(documents, list):
        raise TypeError(
            f"expected a list of Documents, got {type(documents).__name__}"
        )
    if not documents:
        raise ValueError("there are no documents to split")

    chunks: list[Chunk] = []
    for document in documents:
        for index, section in enumerate(parse_sections(document)):
            chunks.append(
                Chunk(
                    text=_chunk_text(section),
                    source=document.source,
                    index=index,
                    produced_by="chunker.py::split_documents",
                )
            )
    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
