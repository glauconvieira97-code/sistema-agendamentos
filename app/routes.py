from fastapi import APIRouter, Request, Form, Depends, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import SessionLocal
from app.models import Usuario, Agendamento

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


# ==============================
# 🔹 Função para obter sessão do banco
# ==============================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==============================
# 🔹 Função auxiliar para verificar login
# ==============================
def verificar_login(request: Request):
    return request.session.get("usuario_id") is not None


# ==============================
# 🏠 PÁGINA INICIAL
# ==============================
@router.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ==============================
# 👤 USUÁRIOS
# ==============================

# Cadastrar novo usuário
@router.post("/cadastrar")
async def cadastrar_usuario(
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db)
):
    novo_usuario = Usuario(nome=nome, email=email, senha=senha)
    db.add(novo_usuario)
    db.commit()
    return RedirectResponse(url="/", status_code=303)


# Listar usuários
@router.get("/usuarios", response_class=HTMLResponse)
def listar_usuarios(request: Request, db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()
    return templates.TemplateResponse("usuarios.html", {"request": request, "usuarios": usuarios})


# Formulário para editar usuário
@router.get("/editar/{usuario_id}", response_class=HTMLResponse)
def editar_usuario_form(usuario_id: int, request: Request, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    return templates.TemplateResponse("editar.html", {"request": request, "usuario": usuario})


# Salvar edição de usuário
@router.post("/editar/{usuario_id}")
def salvar_edicao(
    usuario_id: int,
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario:
        usuario.nome = nome
        usuario.email = email
        usuario.senha = senha
        db.commit()
    return RedirectResponse("/usuarios", status_code=303)


# Excluir usuário
@router.get("/deletar/{usuario_id}")
def deletar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario:
        db.delete(usuario)
        db.commit()
    return RedirectResponse("/usuarios", status_code=303)


# ==============================
# 📅 AGENDAMENTOS
# ==============================

# Exibir formulário de agendamento
@router.get("/agendar", response_class=HTMLResponse)
def form_agendamento(request: Request, db: Session = Depends(get_db)):
    if not verificar_login(request):
        return RedirectResponse("/login", status_code=303)

    usuarios = db.query(Usuario).all()
    return templates.TemplateResponse("agendar.html", {
        "request": request,
        "usuarios": usuarios,
        "usuario_nome": request.session.get("usuario_nome")
    })


# Criar agendamento
@router.post("/agendar")
def criar_agendamento(
    request: Request,
    titulo: str = Form(...),
    data_hora: str = Form(...),
    usuario_id: int = Form(...),
    db: Session = Depends(get_db)
):
    if not verificar_login(request):
        return RedirectResponse("/login", status_code=303)

    data_hora_obj = datetime.fromisoformat(data_hora)
    agendamento = Agendamento(
        titulo=titulo,
        data_hora=data_hora_obj,
        usuario_id=usuario_id
    )
    db.add(agendamento)
    db.commit()
    return RedirectResponse("/agendamentos", status_code=303)


# Listar agendamentos
@router.get("/agendamentos", response_class=HTMLResponse)
def listar_agendamentos(request: Request, db: Session = Depends(get_db)):
    if not verificar_login(request):
        return RedirectResponse("/login", status_code=303)

    agendamentos = db.query(Agendamento).all()
    return templates.TemplateResponse("agendamentos.html", {
        "request": request,
        "agendamentos": agendamentos,
        "usuario_nome": request.session.get("usuario_nome")
    })


# Editar agendamento (formulário)
@router.get("/editar_agendamento/{agendamento_id}", response_class=HTMLResponse)
def editar_agendamento_form(agendamento_id: int, request: Request, db: Session = Depends(get_db)):
    if not verificar_login(request):
        return RedirectResponse("/login", status_code=303)

    agendamento = db.query(Agendamento).filter(Agendamento.id == agendamento_id).first()
    usuarios = db.query(Usuario).all()
    return templates.TemplateResponse("editar_agendamento.html", {
        "request": request,
        "agendamento": agendamento,
        "usuarios": usuarios,
        "usuario_nome": request.session.get("usuario_nome")
    })


# Salvar agendamento editado
@router.post("/editar_agendamento/{agendamento_id}")
def salvar_agendamento_editado(
    agendamento_id: int,
    titulo: str = Form(...),
    data_hora: str = Form(...),
    usuario_id: int = Form(...),
    db: Session = Depends(get_db)
):
    agendamento = db.query(Agendamento).filter(Agendamento.id == agendamento_id).first()
    if agendamento:
        agendamento.titulo = titulo
        agendamento.data_hora = datetime.fromisoformat(data_hora)
        agendamento.usuario_id = usuario_id
        db.commit()
    return RedirectResponse("/agendamentos", status_code=303)


# Excluir agendamento
@router.get("/deletar_agendamento/{agendamento_id}")
def deletar_agendamento(agendamento_id: int, db: Session = Depends(get_db)):
    agendamento = db.query(Agendamento).filter(Agendamento.id == agendamento_id).first()
    if agendamento:
        db.delete(agendamento)
        db.commit()
    return RedirectResponse("/agendamentos", status_code=303)


# ==============================
# 🔐 LOGIN E LOGOUT
# ==============================

@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
def login(
    request: Request,
    response: Response,
    email: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()

    if usuario and usuario.senha == senha:
        request.session["usuario_id"] = usuario.id
        request.session["usuario_nome"] = usuario.nome
        return RedirectResponse("/agendamentos", status_code=303)

    return templates.TemplateResponse("login.html", {
        "request": request,
        "erro": "E-mail ou senha incorretos"
    })


@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=303)
