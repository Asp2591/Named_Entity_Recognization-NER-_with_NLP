from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
import spacy
from spacy import displacy
from fastapi.staticfiles import StaticFiles

app = FastAPI()

nlp = spacy.load('en_core_web_sm')
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "entities": None})

@app.post("/entity", response_class=HTMLResponse)
async def entity(request: Request, file: UploadFile = File(None), text: str = Form(None)):
    readable_file = ""

    if file and file.filename:  # Ensure a file was actually uploaded
        content = await file.read()
        readable_file = content.decode('utf-8', errors='ignore')
    elif text and text.strip():
        readable_file = text.strip()

    if readable_file:
        doc = nlp(readable_file)
        html = displacy.render(doc, style="ent", page=False)
        return templates.TemplateResponse("index.html", {"request": request, "entities": html})

    return templates.TemplateResponse("index.html", {"request": request, "entities": "<p style='color:red;'>Please provide either a file or text input!</p>"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)