
from fastapi import FastAPI, Request
from pydantic import BaseModel
import os
import json


app = FastAPI()

PUBLIC_STATE_PATH = os.path.join(
    os.path.dirname(__file__), '..', 'merge', 'public_state.json'
)


class PromptRequest(BaseModel):
    goal: str
    constraints: list
    context: dict


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/toggle_public")
async def toggle_public(request: Request):
    data = await request.json()
    public = data.get("public", False)
    with open(PUBLIC_STATE_PATH, "w") as f:
        json.dump({"public": public}, f)
    return {"public": public}


@app.post("/api/prompt_broker")
def prompt_broker(prompt: PromptRequest):
    # Build a pro prompt for ChatGPT↔Gemini
    prompt_text = (
        f"Goal: {prompt.goal}\n"
        f"Constraints: {prompt.constraints}\n"
        f"Context: {prompt.context}"
    )
    return {"prompt": prompt_text}
