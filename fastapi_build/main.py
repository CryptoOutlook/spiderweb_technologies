from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory='static'), name='static')

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("homepage.html", {"request": request, "title": "Form Page", "answer": None})

@app.post("/", response_class=HTMLResponse)
async def handle_form(request: Request, input1: str = Form(...), input2: str = Form(...)):
    combined = f"{input1} and {input2}"
    return templates.TemplateResponse("homepage.html", {"request": request, "title": "Form Page", "answer": combined})

# if __name__ == "__main__":
#     app.run(debug=True)
