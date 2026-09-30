"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
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

    intro_end = (
        heading_matches[0].start() if heading_matches else len(remainder)
    )
    sections = [Section(title, INTRO_HEADING, remainder[:intro_end].strip())]

    section_ends = [match.start() for match in heading_matches[1:]]
    section_ends.append(len(remainder))
    for match, end in zip(heading_matches, section_ends, strict=True):
        heading = match.group("heading").strip()
        body = remainder[match.end():end].strip()
        sections.append(Section(title, heading, body))

    return [section for section in sections if section.body]


def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Split documents into chunks. ⚠️ REPLACE THE BODY OF THIS IN MILESTONE 3.

    Right now it just calls the fallback. That is the plain, generic behaviour
    the brief is talking about.

    When you write your own strategy, set `produced_by` to
    "chunker.py::split_documents" so your README's Sample Chunks section names
    the right function. `app.py chunks` prints that string for you.

    Things worth thinking about before you write any code:
      - Are your documents short posts or long guides?
      - Is the useful information in one sentence, or spread over a paragraph?
      - Would splitting on paragraph breaks keep more thoughts intact than
        splitting on a character count?
    """
    return fallback_split(documents)


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
