from ebooklib import epub;from pathlib import Path;import sys,glob
ins=sys.argv[1] if len(sys.argv)>1 else 'artifacts/staging/*.txt';out=sys.argv[2] if len(sys.argv)>2 else 'artifacts/published/book.epub'
book=epub.EpubBook();book.set_identifier('monkey-paw-epub');book.set_title('Monkey Paw Book');book.set_language('en')
files=sorted(glob.glob(ins)) or [Path('artifacts/staging/blank.txt').write_text('Blank') or 'artifacts/staging/blank.txt']
chs=[]
for i,f in enumerate(files,1): c=epub.EpubHtml(title=f'Chapter {i}',file_name=f'chap_{i}.xhtml');c.content=f'<h1>Chapter {i}</h1><pre>'+Path(f).read_text()+'</pre>';book.add_item(c);chs.append(c)
book.toc=tuple(chs);book.add_item(epub.EpubNcx());book.add_item(epub.EpubNav());book.spine=['nav']+chs
Path(out).parent.mkdir(parents=True,exist_ok=True);epub.write_epub(out,book);print(out)