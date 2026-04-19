from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
import os

from database import SessionLocal, engine, Base
from models import User, Analise
from auth import hash_password, verify_password
from interpretador import interpretar

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )

@app.post("/login")
def login(request: Request, email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.password):
        return RedirectResponse("/", status_code=302)

    response = RedirectResponse("/dashboard", status_code=302)
    response.set_cookie(key="user_id", value=str(user.id))
    return response

@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={}
    )

@app.post("/register")
def register(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = User(email=email, password=hash_password(password))
    db.add(user)
    db.commit()
    return RedirectResponse("/", status_code=302)

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={}
    )

@app.post("/calcular", response_class=HTMLResponse)
def calcular(request: Request,
             p: float = Form(...),
             argila: float = Form(...),
             ca: float = Form(...),
             mg: float = Form(...),
             k: float = Form(...),
             ctc: float = Form(...),
             db: Session = Depends(get_db)):

    dados = {"p": p, "argila": argila, "ca": ca, "mg": mg, "k": k, "ctc": ctc}
    resultado = interpretar(dados)

    analise = Analise(**dados, resultado=resultado)
    db.add(analise)
    db.commit()

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"resultado": resultado}
    )
