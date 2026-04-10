#!/usr/bin/env python3
"""
Kombiniert ein Manuskript zu einem EPUB.

Verwendung:
    python3 build-epub.py                        # -> Manuskript.epub (alle Bücher)
    python3 build-epub.py -b "Buch 1"            # -> nur Buch 1
    python3 build-epub.py -o mein_buch.epub      # -> eigener Dateiname
    python3 build-epub.py -t "Mein Roman"        # -> eigener Titel
    python3 build-epub.py -a "Max Mustermann"    # -> Autor setzen
    python3 build-epub.py -l de                   # -> Sprache (Standard: de)

Abhängigkeit:
    pip install ebooklib
"""

import argparse
import os
import re
import glob
import html

from ebooklib import epub

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MANUSKRIPT_DIR = os.path.join(SCRIPT_DIR, "03 - Manuskript")
LEXIKON_FILE = os.path.join(MANUSKRIPT_DIR, "Lexikon.md")

STYLESHEET = """
body {
    font-family: Georgia, "Times New Roman", serif;
    line-height: 1.6;
    margin: 1em;
}
h1 {
    text-align: center;
    margin-top: 3em;
    margin-bottom: 1em;
    page-break-before: always;
}
h2 {
    text-align: center;
    margin-top: 2em;
    margin-bottom: 0.5em;
}
p {
    text-indent: 1.5em;
    margin: 0.2em 0;
}
p.first {
    text-indent: 0;
}
.scene-separator {
    text-align: center;
    margin: 1.5em 0;
    text-indent: 0;
}
.title-page {
    text-align: center;
    margin-top: 30%;
}
.title-page h1 {
    font-size: 2em;
    page-break-before: auto;
}
.title-page p {
    font-size: 1.2em;
    text-indent: 0;
}
blockquote {
    font-style: italic;
    margin-left: 2em;
    margin-right: 1em;
}
"""


def strip_frontmatter(text: str) -> str:
    m = re.match(r"^---\s*\n.*?\n---\s*\n", text, re.DOTALL)
    if m:
        text = text[m.end():]
    return text


def strip_footer_meta(text: str) -> str:
    text = re.sub(r"\n---\s*\n(\*[^\n]*\*\s*\n?)+\s*$", "", text)
    return text


def get_chapter_title(chapter_dir: str) -> str:
    kapitel_file = os.path.join(chapter_dir, "_Kapitel.md")
    if not os.path.exists(kapitel_file):
        return os.path.basename(chapter_dir)
    with open(kapitel_file, "r", encoding="utf-8") as f:
        content = f.read()
    m = re.search(r"^# (.+)$", content, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return os.path.basename(chapter_dir)


def get_scene_files(chapter_dir: str) -> list[str]:
    chapter_name = os.path.basename(chapter_dir)
    pattern = os.path.join(chapter_dir, f"{chapter_name}-S*.md")
    return sorted(glob.glob(pattern))


def extract_scene_text(filepath: str) -> str:
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    text = strip_frontmatter(text)
    text = strip_footer_meta(text)
    text = re.sub(r"^# .+\n+", "", text)
    return text.strip()


def get_chapter_dirs(base_dir: str) -> list[str]:
    dirs = []
    for entry in sorted(os.listdir(base_dir)):
        full = os.path.join(base_dir, entry)
        if os.path.isdir(full) and re.match(r"K\d+", entry):
            dirs.append(full)
    return dirs


def get_book_dirs() -> list[str]:
    book_dirs = []
    for entry in sorted(os.listdir(MANUSKRIPT_DIR)):
        full = os.path.join(MANUSKRIPT_DIR, entry)
        if os.path.isdir(full) and entry.startswith("Buch"):
            book_dirs.append(full)
    if not book_dirs:
        chapter_dirs = get_chapter_dirs(MANUSKRIPT_DIR)
        if chapter_dirs:
            book_dirs = [MANUSKRIPT_DIR]
    return book_dirs


def md_to_html(text: str) -> str:
    """Konvertiert einfaches Markdown (kursiv, fett) zu HTML."""
    text = html.escape(text)
    # Fett: **text** oder __text__
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"__(.+?)__", r"<strong>\1</strong>", text)
    # Kursiv: *text* oder _text_
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"(?<!_)_(?!_)(.+?)(?<!_)_(?!_)", r"<em>\1</em>", text)
    return text


def prose_to_html(text: str) -> str:
    """Konvertiert Prosatext in HTML-Absätze."""
    paragraphs = re.split(r"\n\n+", text)
    parts = []
    first = True
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        css_class = ' class="first"' if first else ""
        parts.append(f"<p{css_class}>{md_to_html(p)}</p>")
        first = False
    return "\n".join(parts)


def lexikon_to_html(text: str) -> str:
    """Konvertiert Lexikon-Markdown in HTML."""
    paragraphs = re.split(r"\n\n+", text)
    parts = []
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        if p == "* * *":
            parts.append('<p class="scene-separator">* * *</p>')
            continue
        m = re.match(r"^##\s+(.+)$", p)
        if m:
            parts.append(f"<h2>{html.escape(m.group(1))}</h2>")
            continue
        if p.startswith(">"):
            lines = p.split("\n")
            quote_lines = []
            for line in lines:
                line = re.sub(r"^>\s*", "", line).strip().strip("*")
                if line:
                    quote_lines.append(f"<p>{html.escape(line)}</p>")
            parts.append(f"<blockquote>{''.join(quote_lines)}</blockquote>")
            continue
        parts.append(f"<p>{md_to_html(p)}</p>")
    return "\n".join(parts)


def build_epub(output_path: str, title: str, author: str, language: str,
               book_filter: str | None = None):
    book = epub.EpubBook()

    book.set_identifier("ashworth-manuscript")
    book.set_title(title)
    book.set_language(language)
    if author:
        book.add_author(author)

    # Stylesheet
    style = epub.EpubItem(
        uid="style",
        file_name="style/default.css",
        media_type="text/css",
        content=STYLESHEET.encode("utf-8"),
    )
    book.add_item(style)

    # Titelseite
    title_html = f"""<div class="title-page">
<h1>{html.escape(title)}</h1>
<p>{html.escape(author)}</p>
</div>"""
    title_page = epub.EpubHtml(title="Titel", file_name="title.xhtml", lang=language)
    title_page.content = title_html
    title_page.add_item(style)
    book.add_item(title_page)

    spine = ["nav", title_page]
    toc = []
    chapters_epub = []

    book_dirs = get_book_dirs()
    if not book_dirs:
        print("Keine Kapitel gefunden!")
        return

    if book_filter:
        book_dirs = [d for d in book_dirs if os.path.basename(d) == book_filter]
        if not book_dirs:
            print(f"Buch '{book_filter}' nicht gefunden!")
            return

    multi_book = len(book_dirs) > 1 or (len(book_dirs) == 1 and book_dirs[0] != MANUSKRIPT_DIR)
    chapter_idx = 0

    for book_dir in book_dirs:
        book_name = os.path.basename(book_dir)
        book_toc_items = []

        if multi_book and book_dir != MANUSKRIPT_DIR:
            print(f"\n{book_name}:")

        chapter_dirs = get_chapter_dirs(book_dir)
        for chapter_dir in chapter_dirs:
            chapter_title = get_chapter_title(chapter_dir)
            scene_files = get_scene_files(chapter_dir)

            if not scene_files:
                continue

            chapter_idx += 1
            file_name = f"chapter_{chapter_idx:03d}.xhtml"

            # Kapitel-HTML zusammenbauen
            body_parts = [f"<h1>{html.escape(chapter_title)}</h1>"]
            for i, scene_file in enumerate(scene_files):
                if i > 0:
                    body_parts.append('<p class="scene-separator">* * *</p>')
                prose = extract_scene_text(scene_file)
                if prose:
                    body_parts.append(prose_to_html(prose))

            epub_chapter = epub.EpubHtml(
                title=chapter_title,
                file_name=file_name,
                lang=language,
            )
            epub_chapter.content = "\n".join(body_parts)
            epub_chapter.add_item(style)
            book.add_item(epub_chapter)
            spine.append(epub_chapter)
            chapters_epub.append(epub_chapter)
            book_toc_items.append(epub_chapter)

            print(f"  {chapter_title}: {len(scene_files)} Szenen")

        if multi_book and book_dir != MANUSKRIPT_DIR:
            toc.append((epub.Section(book_name), book_toc_items))
        else:
            toc.extend(book_toc_items)

    # Lexikon am Ende
    if os.path.exists(LEXIKON_FILE):
        with open(LEXIKON_FILE, "r", encoding="utf-8") as f:
            lex_text = f.read()
        lex_text = strip_frontmatter(lex_text)
        m = re.match(r"^# (.+)\n+", lex_text)
        if m:
            lex_title = m.group(1).strip()
            lex_text = lex_text[m.end():]
        else:
            lex_title = "Lexikon"

        lex_chapter = epub.EpubHtml(
            title=lex_title,
            file_name="lexikon.xhtml",
            lang=language,
        )
        lex_chapter.content = f"<h1>{html.escape(lex_title)}</h1>\n{lexikon_to_html(lex_text)}"
        lex_chapter.add_item(style)
        book.add_item(lex_chapter)
        spine.append(lex_chapter)
        toc.append(lex_chapter)
        print(f"  {lex_title}")

    book.toc = toc
    book.spine = spine

    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    epub.write_epub(output_path, book)
    print(f"\nEPUB erstellt: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manuskript zu EPUB")
    parser.add_argument("-o", "--output", default="Manuskript.epub",
                        help="Ausgabedatei (Standard: Manuskript.epub)")
    parser.add_argument("-t", "--title", default="MANUSKRIPT",
                        help="Titel auf der Titelseite")
    parser.add_argument("-a", "--author", default="",
                        help="Autor auf der Titelseite")
    parser.add_argument("-b", "--book", default=None,
                        help="Nur ein bestimmtes Buch bauen (z.B. 'Buch 1')")
    parser.add_argument("-l", "--language", default="de",
                        help="Sprache (Standard: de)")
    args = parser.parse_args()

    output = args.output
    if not os.path.isabs(output):
        output = os.path.join(SCRIPT_DIR, output)

    build_epub(output, args.title, args.author, args.language, args.book)
