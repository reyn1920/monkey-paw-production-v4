from sqlmodel import Session
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markdown import markdown as md_to_html
from ..store.db import Asset, Draft, engine
import datetime, json

BASE = Path(__file__).resolve().parents[2]
ART_DIR = BASE / "artifacts" / "staging"
TPL_DIR = BASE / "templates"
AVATAR_DIR = BASE / "avatars"

env = Environment(
    loader=FileSystemLoader(str(TPL_DIR)),
    autoescape=select_autoescape(['html', 'xml'])
)

def load_avatar(name: str) -> dict:
    p = AVATAR_DIR / f"{name}.json"
    if not p.exists():
        return {"name":"default","tone":"neutral","pacing":"medium","reading_level":"8","call_to_action":"none"}
    import json
    return json.loads(p.read_text())

def save_asset(draft_id: int, kind: str, content: str) -> str:
    ART_DIR.mkdir(parents=True, exist_ok=True)
    path = ART_DIR / f"{kind}_{draft_id}.txt"
    path.write_text(content)
    with Session(engine) as s:
        a = Asset(draft_id=draft_id, kind=kind, path=str(path), created_at=datetime.datetime.utcnow())
        s.add(a); s.commit()
    return str(path)

def render_template(draft: Draft, template_name: str) -> str:
    tpl = env.get_template(template_name)
    avatar = load_avatar(draft.avatar)
    return tpl.render(content=draft.content, avatar=avatar, draft_id=draft.id)

def render_markdown_to_site(markdown_text: str, output_dir: Path) -> str:
    output_dir.mkdir(parents=True, exist_ok=True)
    html = md_to_html(markdown_text)
    p = output_dir / "index.html"
    p.write_text(html)
    return str(p)
