#!/usr/bin/env python3
"""
Kombiniert ein Manuskript zu einem PDF im Standard-Manuskript-Format.

Verwendung:
    python3 build-pdf.py                        # -> Manuskript.pdf (alle Bücher)
    python3 build-pdf.py -b "Buch 1"            # -> nur Buch 1
    python3 build-pdf.py -o mein_buch.pdf       # -> eigener Dateiname
    python3 build-pdf.py -t "Mein Roman"        # -> eigener Titel auf Titelseite
"""

import argparse
import os
import platform
import re
import glob
from fpdf import FPDF

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MANUSKRIPT_DIR = os.path.join(SCRIPT_DIR, "03 - Manuskript")
RESSOURCEN_DIR = os.path.join(SCRIPT_DIR, "08 - Ressourcen")

# Serienweite Defaults
DEFAULT_AUTHOR = "C. J. Whitmore"
DEFAULT_SERIES = "Die Ashworth Drei"

# Cover-Dateien pro Buch (Schlüssel = Ordnername unter 03 - Manuskript/)
COVER_FILES = {
    "Buch 1": "ashworth-book1.png",
    "Buch 2": "ashworth-book2.png",
    "Buch 3": "buck3.png",
    "Buch 4": "buch4.png",
    "Buch 5": "buch5.png",
}

# --- Manuskript-Format-Einstellungen ---
FONT_NAME = "CourierNew"
FONT_SIZE = 12

if platform.system() == "Darwin":
    FONT_DIR = "/System/Library/Fonts/Supplemental/"
    FONT_REGULAR = "Courier New.ttf"
    FONT_BOLD = "Courier New Bold.ttf"
    FONT_ITALIC = "Courier New Italic.ttf"
else:
    FONT_DIR = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts")
    FONT_REGULAR = "cour.ttf"
    FONT_BOLD = "courbd.ttf"
    FONT_ITALIC = "couri.ttf"

LINE_HEIGHT = 10  # ~doppelter Zeilenabstand bei 12pt
MARGIN_TOP = 25
MARGIN_BOTTOM = 25
MARGIN_LEFT = 30
MARGIN_RIGHT = 25
PAGE_WIDTH = 210  # A4
PAGE_HEIGHT = 297

SCENE_SEPARATOR = "* * *"
LEXIKON_FILE = os.path.join(MANUSKRIPT_DIR, "Lexikon.md")


def strip_frontmatter(text: str) -> str:
    """Entfernt YAML-Frontmatter (--- ... ---) am Anfang."""
    m = re.match(r"^---\s*\n.*?\n---\s*\n", text, re.DOTALL)
    if m:
        text = text[m.end():]
    return text


def strip_footer_meta(text: str) -> str:
    """Entfernt Fußzeilen-Metadaten (--- gefolgt von *kursiven* Zeilen am Ende)."""
    text = re.sub(r"\n---\s*\n(\*[^\n]*\*\s*\n?)+\s*$", "", text)
    return text


def get_chapter_title(chapter_dir: str) -> str:
    """Liest Kapiteltitel aus _Kapitel.md."""
    kapitel_file = os.path.join(chapter_dir, "_Kapitel.md")
    if not os.path.exists(kapitel_file):
        return os.path.basename(chapter_dir)
    with open(kapitel_file, "r", encoding="utf-8") as f:
        content = f.read()
    m = re.search(r"^# (.+)$", content, re.MULTILINE)
    if m:
        title = m.group(1).strip()
        title = re.sub(r"^Kapitel\s+\d+\s*[—–-]\s*", "", title)
        return title
    return os.path.basename(chapter_dir)


def get_scene_files(chapter_dir: str) -> list[str]:
    """Findet Szenen-Dateien sortiert nach Nummer (K01-S01, K01-S02, ...)."""
    chapter_name = os.path.basename(chapter_dir)
    pattern = os.path.join(chapter_dir, f"{chapter_name}-S*.md")
    files = sorted(glob.glob(pattern))
    return files


def extract_scene_text(filepath: str) -> str:
    """Extrahiert den reinen Prosatext einer Szene."""
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    text = strip_frontmatter(text)
    text = strip_footer_meta(text)
    text = re.sub(r"^# .+\n+", "", text)
    text = re.sub(r"^\* \* \*\s*\n*", "", text)
    return text.strip()


def get_chapter_dirs(base_dir: str) -> list[str]:
    """Findet Kapitelordner sortiert (K01, K02, ...)."""
    dirs = []
    for entry in sorted(os.listdir(base_dir)):
        full = os.path.join(base_dir, entry)
        if os.path.isdir(full) and re.match(r"K\d+", entry):
            dirs.append(full)
    return dirs


def get_book_dirs() -> list[str]:
    """Findet Buchordner unter Manuskript/ (z.B. 'Buch 1', 'Buch 2').
    Falls keine Buchordner existieren, wird Manuskript/ selbst als einziges Buch behandelt."""
    book_dirs = []
    for entry in sorted(os.listdir(MANUSKRIPT_DIR)):
        full = os.path.join(MANUSKRIPT_DIR, entry)
        if os.path.isdir(full) and entry.startswith("Buch"):
            book_dirs.append(full)

    # Fallback: Kapitel direkt unter Manuskript/ (Einzelwerk ohne Buchordner)
    if not book_dirs:
        chapter_dirs = get_chapter_dirs(MANUSKRIPT_DIR)
        if chapter_dirs:
            book_dirs = [MANUSKRIPT_DIR]

    return book_dirs


class ManuscriptPDF(FPDF):
    def __init__(self, title: str):
        super().__init__("P", "mm", "A4")
        self.set_auto_page_break(auto=True, margin=MARGIN_BOTTOM)
        self.set_margins(MARGIN_LEFT, MARGIN_TOP, MARGIN_RIGHT)
        self.add_font(FONT_NAME, "", os.path.join(FONT_DIR, FONT_REGULAR))
        self.add_font(FONT_NAME, "B", os.path.join(FONT_DIR, FONT_BOLD))
        self.add_font(FONT_NAME, "I", os.path.join(FONT_DIR, FONT_ITALIC))
        self.chapter_count = 0
        self.total_title = title

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font(FONT_NAME, "", 10)
        self.set_y(10)
        text_width = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT
        self.cell(text_width / 2, 5, self.total_title, align="L")
        self.cell(text_width / 2, 5, str(self.page_no()), align="R")
        self.ln(10)

    def footer(self):
        pass

    def title_page(self, title: str, author: str):
        self.add_page()
        self.set_font(FONT_NAME, "B", 24)
        self.ln(80)
        self.cell(0, 20, title, align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font(FONT_NAME, "", 14)
        self.ln(10)
        self.cell(0, 10, author, align="C", new_x="LMARGIN", new_y="NEXT")

    def book_heading(self, title: str):
        """Trennseite für ein Buch in einer Serie."""
        self.add_page()
        self.ln(50)
        self.set_font(FONT_NAME, "B", 18)
        self.cell(0, LINE_HEIGHT, title, align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font(FONT_NAME, "", FONT_SIZE)

    def chapter_heading(self, title: str):
        self.add_page()
        self.chapter_count += 1
        self.ln(30)
        self.set_font(FONT_NAME, "B", 14)
        self.cell(0, LINE_HEIGHT, title, align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(25)
        self.set_font(FONT_NAME, "", FONT_SIZE)

    def scene_separator(self):
        self.ln(LINE_HEIGHT)
        self.set_font(FONT_NAME, "", FONT_SIZE)
        self.cell(0, LINE_HEIGHT, SCENE_SEPARATOR, align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(LINE_HEIGHT)

    @staticmethod
    def _md_to_fpdf(text: str) -> str:
        """Konvertiert *kursiv* und _kursiv_ (Markdown) zu __kursiv__ (fpdf2-Marker)."""
        text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"__\1__", text)
        text = re.sub(r"(?<!_)_(?!_)(.+?)(?<!_)_(?!_)", r"__\1__", text)
        return text

    def write_prose(self, text: str):
        self.set_font(FONT_NAME, "", FONT_SIZE)
        text_width = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT
        for paragraph in re.split(r"\n\n+", text):
            paragraph = paragraph.strip()
            if not paragraph:
                continue
            self.cell(10)
            self.multi_cell(
                text_width - 10,
                LINE_HEIGHT,
                self._md_to_fpdf(paragraph),
                markdown=True,
                new_x="LMARGIN",
                new_y="NEXT",
            )
            self.ln(LINE_HEIGHT * 0.5)

    def write_lexikon(self, text: str):
        """Schreibt das Lexikon mit Überschriften, Blockzitaten (kursiv) und Prosa."""
        self.set_font(FONT_NAME, "", FONT_SIZE)
        text_width = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT
        for paragraph in re.split(r"\n\n+", text):
            paragraph = paragraph.strip()
            if not paragraph:
                continue
            if paragraph == "* * *":
                self.scene_separator()
                continue
            m = re.match(r"^##\s+(.+)$", paragraph)
            if m:
                self.ln(LINE_HEIGHT)
                self.set_font(FONT_NAME, "B", FONT_SIZE)
                self.multi_cell(text_width, LINE_HEIGHT, m.group(1),
                                new_x="LMARGIN", new_y="NEXT")
                self.ln(LINE_HEIGHT * 0.5)
                self.set_font(FONT_NAME, "", FONT_SIZE)
                continue
            if paragraph.startswith(">"):
                self.set_font(FONT_NAME, "I", FONT_SIZE)
                lines = paragraph.split("\n")
                for line in lines:
                    line = re.sub(r"^>\s*", "", line)
                    line = line.strip().strip("*")
                    if not line:
                        continue
                    self.cell(15)
                    self.multi_cell(text_width - 15, LINE_HEIGHT, line,
                                    new_x="LMARGIN", new_y="NEXT")
                self.ln(LINE_HEIGHT * 0.3)
                self.set_font(FONT_NAME, "", FONT_SIZE)
                continue
            self.cell(10)
            self.multi_cell(text_width - 10, LINE_HEIGHT, paragraph,
                            new_x="LMARGIN", new_y="NEXT")
            self.ln(LINE_HEIGHT * 0.5)


def find_cover_image(book_filter: str | None) -> str | None:
    """Findet das Cover-Bild für ein bestimmtes Buch."""
    if book_filter and book_filter in COVER_FILES:
        path = os.path.join(RESSOURCEN_DIR, COVER_FILES[book_filter])
        if os.path.exists(path):
            return path
    for name, filename in COVER_FILES.items():
        if book_filter and name != book_filter:
            continue
        path = os.path.join(RESSOURCEN_DIR, filename)
        if os.path.exists(path):
            return path
    return None


def build_pdf(output_path: str, title: str, author: str, book_filter: str | None = None):
    pdf = ManuscriptPDF(title)

    # Cover-Bild als erste Seite
    cover_path = find_cover_image(book_filter)
    if cover_path:
        pdf.add_page()
        # Cover zentriert auf der Seite, Seitenverhältnis beibehalten
        img_width = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT
        img_height = img_width * 1.5  # ~6:9 Verhältnis
        y_offset = (PAGE_HEIGHT - img_height) / 2
        pdf.image(cover_path, x=MARGIN_LEFT, y=y_offset, w=img_width)
        print(f"Cover: {os.path.basename(cover_path)}")

    pdf.title_page(title, author)

    book_dirs = get_book_dirs()
    if not book_dirs:
        print("Keine Kapitel gefunden!")
        return

    # Filter auf bestimmtes Buch
    if book_filter:
        book_dirs = [d for d in book_dirs if os.path.basename(d) == book_filter]
        if not book_dirs:
            print(f"Buch '{book_filter}' nicht gefunden!")
            return

    multi_book = len(book_dirs) > 1 or (len(book_dirs) == 1 and book_dirs[0] != MANUSKRIPT_DIR)

    for book_dir in book_dirs:
        book_name = os.path.basename(book_dir)

        if multi_book and book_dir != MANUSKRIPT_DIR:
            pdf.book_heading(book_name)
            print(f"\n{book_name}:")

        chapter_dirs = get_chapter_dirs(book_dir)
        for chapter_dir in chapter_dirs:
            chapter_title = get_chapter_title(chapter_dir)
            scene_files = get_scene_files(chapter_dir)

            if not scene_files:
                continue

            pdf.chapter_heading(chapter_title)

            for i, scene_file in enumerate(scene_files):
                if i > 0:
                    pdf.scene_separator()
                prose = extract_scene_text(scene_file)
                if prose:
                    pdf.write_prose(prose)

            print(f"  {chapter_title}: {len(scene_files)} Szenen")

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
        pdf.chapter_heading(lex_title)
        pdf.write_lexikon(lex_text)
        print(f"  {lex_title}")

    pdf.output(output_path)
    print(f"\nPDF erstellt: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manuskript zu PDF")
    parser.add_argument("-o", "--output", default=None,
                        help="Ausgabedatei (Standard: aus Titel abgeleitet)")
    parser.add_argument("-t", "--title", default=DEFAULT_SERIES,
                        help="Titel auf der Titelseite")
    parser.add_argument("-a", "--author", default=DEFAULT_AUTHOR,
                        help="Autor auf der Titelseite")
    parser.add_argument("-b", "--book", default=None,
                        help="Nur ein bestimmtes Buch bauen (z.B. 'Buch 1')")
    args = parser.parse_args()

    output = args.output
    if output is None:
        safe_title = args.title
        for old, new in [("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss"),
                         ("Ä", "Ae"), ("Ö", "Oe"), ("Ü", "Ue")]:
            safe_title = safe_title.replace(old, new)
        safe_title = re.sub(r"[^\w\s-]", "", safe_title).strip()
        safe_title = re.sub(r"[\s]+", "-", safe_title)
        output = f"{safe_title}.pdf"
    if not os.path.isabs(output):
        output = os.path.join(SCRIPT_DIR, output)

    build_pdf(output, args.title, args.author, args.book)
