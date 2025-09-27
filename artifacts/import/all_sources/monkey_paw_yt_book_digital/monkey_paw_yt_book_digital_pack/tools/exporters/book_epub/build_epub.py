from ebooklib import epub
from pathlib import Path
import sys, glob

def build_epub(inputs_glob: str, out_file: str):
    book = epub.EpubBook()
    book.set_identifier("monkey-paw-epub")
    book.set_title("Monkey Paw Book")
    book.set_language("en")

    chapter_files = sorted(glob.glob(inputs_glob))
    if not chapter_files:
        c = Path("artifacts/staging/blank.txt")
        c.parent.mkdir(parents=True, exist_ok=True)
        c.write_text("Blank chapter — add drafts to artifacts/staging")
        chapter_files = [str(c)]

    chapters = []
    for i, path in enumerate(chapter_files, 1):
        c = epub.EpubHtml(title=f"Chapter {i}", file_name=f"chap_{i}.xhtml", lang="en")
        c.content = f"<h1>Chapter {i}</h1><pre>{Path(path).read_text()}</pre>"
        book.add_item(c)
        chapters.append(c)

    book.toc = tuple(chapters)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ['nav'] + chapters

    Path(out_file).parent.mkdir(parents=True, exist_ok=True)
    epub.write_epub(out_file, book)

if __name__ == "__main__":
    ins = sys.argv[1] if len(sys.argv)>1 else "artifacts/staging/*.txt"
    out = sys.argv[2] if len(sys.argv)>2 else "artifacts/published/book.epub"
    build_epub(ins, out)
    print(f"Wrote {out}")
