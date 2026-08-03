from fastapi import FastAPI, UploadFile, File, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from starlette.middleware.sessions import SessionMiddleware
from database import Base, engine
import models
import os
import shutil
import uuid

# =====================================
# SERVICES
# =====================================

from services.pdf_service import extract_text
from services.chunk_service import chunk_text
from services.embedding_service import create_embeddings

from services.vector_db import (
    store_embeddings,
    delete_collection
)

from services.retrieval_service import retrieve_chunks
from services.llm_services import ask_llm

from services.history_service import (
    create_chat,
    add_message,
    load_history,
    get_chat,
    delete_chat
)

from services.auth_service import (
    register_user,
    login_user
)

# =====================================
# FASTAPI APP
# =====================================

app = FastAPI(title="MedTrace AI")
Base.metadata.create_all(bind=engine)

app.add_middleware(
    SessionMiddleware,
    secret_key="clinibuddy-secret-key"
)

print("=" * 50)
print("RUNNING MAIN.PY FROM:", __file__)
print("=" * 50)

# =====================================
# STATIC + TEMPLATE
# =====================================

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(directory="templates")

# =====================================
# STORAGE
# =====================================

UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

# =====================================
# MODELS
# =====================================

class Question(BaseModel):
    question: str
    chat_id: str


class User(BaseModel):
    username: str
    password: str

# =====================================
# LOGIN PAGE
# =====================================

@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):

    if "username" in request.session:
        return RedirectResponse("/app")
    
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "request": request
        }
    )


# =====================================
# MAIN APPLICATION
# =====================================

@app.get("/app", response_class=HTMLResponse)
def app_page(request: Request):

    if "username" not in request.session:
        return RedirectResponse("/")
    
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "username": request.session["username"]
       }
    )

# =====================================
# REGISTER
# =====================================
@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={"request": request}
    )
@app.post("/register")
def register(data: User):

    print("========== REGISTER HIT ==========")
    print("Username:", data.username)
    print("Password:", data.password)

    success = register_user(data.username, data.password)

    print("Success:", success)

    if not success:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    return {"success": True}
# =====================================
# LOGIN
# =====================================

@app.post("/login")
def login(request: Request, data: User):

    success = login_user(
        data.username,
        data.password
    )

    if not success:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    request.session["username"] = data.username

    return {
        "success": True
    }

# =====================================
# LOGOUT
# =====================================

@app.get("/logout")
def logout(request: Request):

    request.session.clear()

    return RedirectResponse(
        url="/"
    )

# =====================================
# UPLOAD REPORT
# =====================================

# =====================================
# UPLOAD REPORT
# =====================================

@app.post("/upload")
def upload(
    request: Request,
    file: UploadFile = File(...)
):

    # -----------------------------
    # Login Required
    # -----------------------------
    if "username" not in request.session:

        raise HTTPException(
            status_code=401,
            detail="Please login first"
        )

    try:

        # -----------------------------
        # Validate PDF
        # -----------------------------
        if not file.filename.lower().endswith(".pdf"):

            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed"
            )

        # -----------------------------
        # Save PDF
        # -----------------------------
        unique_name = f"{uuid.uuid4()}_{file.filename}"

        file_path = os.path.join(
            UPLOAD_FOLDER,
            unique_name
        )

        with open(file_path, "wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        print("Saved:", file.filename)

        # -----------------------------
        # Extract Text
        # -----------------------------
        pages = extract_text(file_path)

        if not pages:

            raise HTTPException(
                status_code=400,
                detail="Unable to extract text from PDF"
            )

        # -----------------------------
        # Chunk Text
        # -----------------------------
        chunks = chunk_text(pages)

        # -----------------------------
        # Create Embeddings
        # -----------------------------
        embeddings = create_embeddings(chunks)

        # -----------------------------
        # Create Chat
        # -----------------------------
        chat = create_chat(
            request.session["username"],
            file.filename
      )

        chat_id = chat["id"]

        # -----------------------------
        # Store Embeddings
        # -----------------------------
        store_embeddings(
            chat_id,
            chunks,
            embeddings
        )

        print("Stored vectors:", chat_id)

        return {

            "success": True,

            "filename": file.filename,

            "pages": len(pages),

            "chunks": len(chunks),

            "chat_id": chat_id

        }

    except HTTPException:

        raise

    except Exception as e:

        print("UPLOAD ERROR:", e)

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )


# =====================================
# ASK AI
# =====================================

# =====================================
# ASK AI
# =====================================

@app.post("/ask")
def ask_question(
    request: Request,
    data: Question
):

    # -----------------------------
    # Login Required
    # -----------------------------
    if "username" not in request.session:

        raise HTTPException(
            status_code=401,
            detail="Please login first"
        )

    # -----------------------------
    # Empty Question
    # -----------------------------
    if not data.question.strip():

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    # -----------------------------
    # Check Chat
    # -----------------------------
    chat = get_chat(data.chat_id)

    if not chat:

        raise HTTPException(
            status_code=404,
            detail="Chat not found"
        )

    # -----------------------------
    # Save User Question
    # -----------------------------
    add_message(
        data.chat_id,
        "user",
        data.question
    )

    try:

        # -----------------------------
        # Retrieve Relevant Chunks
        # -----------------------------
        retrieved = retrieve_chunks(
            data.chat_id,
            data.question
        )

        context = retrieved["context"]
        pages = retrieved["pages"]

        # -----------------------------
        # No Context Found
        # -----------------------------
        if not context.strip():

            answer = (
                "I couldn't find relevant information "
                "in the uploaded medical report."
            )

        else:

            # -----------------------------
            # Ask LLM
            # -----------------------------
            answer = ask_llm(
                data.question,
                context
            )

            '''if pages:

                page_text = ", ".join(
                    f"Page {page}"
                    for page in pages
                )

                answer += f"\n\n📄 Source: {page_text}"
                '''
        # -----------------------------
        # Save AI Response
        # -----------------------------
        add_message(
            data.chat_id,
            "assistant",
            answer
        )

        return {

            "question": data.question,

            "answer": answer

        }

    except Exception as e:

        print("ASK ERROR:", e)

        answer = "Sorry, I was unable to process your question."

        add_message(
            data.chat_id,
            "assistant",
            answer
        )

        return {

            "question": data.question,

            "answer": answer

        }


# =====================================
# HISTORY
# =====================================
# =====================================
# HISTORY
# =====================================

@app.get("/history")
def history(request: Request):

    if "username" not in request.session:

        raise HTTPException(
            status_code=401,
            detail="Please login first"
        )

    return {

        "chats": load_history(
            request.session["username"] 
        )

    }


# =====================================
# OPEN CHAT
# =====================================

@app.get("/history/{chat_id}")
def open_chat(
    request: Request,
    chat_id: str
):

    if "username" not in request.session:

        raise HTTPException(
            status_code=401,
            detail="Please login first"
        )

    chat = get_chat(chat_id,
                    request.session["username"]
    )

    if not chat:

        raise HTTPException(
            status_code=404,
            detail="Chat not found"
        )

    return chat


# =====================================
# DELETE CHAT
# =====================================

@app.delete("/history/{chat_id}")
def remove_chat(
    request: Request,
    chat_id: str
):

    if "username" not in request.session:

        raise HTTPException(
            status_code=401,
            detail="Please login first"
        )
    
    
    chat = get_chat(
        chat_id,
        request.session["username"]
   )


    if not chat:

        raise HTTPException(
        status_code=404,
        detail="Chat not found"
        )


    delete_chat(chat_id)

    delete_collection(chat_id)


    return {

        "success": True,

        "message": "Chat deleted"

   }


# =====================================
# HEALTH
# =====================================

@app.get("/health")
def health():

    return {

        "status": "running",

        "application": "MedTrace AI"

    }


# =====================================
# EXPORT CHAT
# =====================================

@app.get("/export/{chat_id}/{file_type}")
def export_chat(
    request: Request,
    chat_id: str,
    file_type: str
):

    if "username" not in request.session:

        raise HTTPException(
            status_code=401,
            detail="Please login first"
        )

    chat = get_chat(chat_id,
                    request.session["username"]
    )

    if not chat:

        raise HTTPException(
            status_code=404,
            detail="Chat not found"
        )

    os.makedirs(
        "exports",
        exist_ok=True
    )

    # ---------------- TXT ----------------

    if file_type.lower() == "txt":

        filepath = os.path.join(

            "exports",

            f"{chat_id}.txt"

        )

        with open(
            filepath,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                f"Medical Report: {chat['filename']}\n\n"
            )

            for msg in chat["messages"]:

                f.write(
                    f"{msg['role'].upper()}:\n"
                )

                f.write(
                    f"{msg['content']}\n\n"
                )

        return FileResponse(

            path=filepath,

            filename="ChatHistory.txt",

            media_type="text/plain"

        )

    # ---------------- PDF ----------------

    elif file_type.lower() == "pdf":

        filepath = os.path.join(

            "exports",

            f"{chat_id}.pdf"

        )

        doc = SimpleDocTemplate(filepath)

        styles = getSampleStyleSheet()

        story = []

        story.append(

            Paragraph(

                "<b>CliniBuddy AI Chat Export</b>",

                styles["Title"]

            )

        )

        story.append(

            Paragraph(

                f"<b>Medical Report:</b> {chat['filename']}",

                styles["Heading2"]

            )

        )

        for msg in chat["messages"]:

            story.append(

                Paragraph(

                    f"<b>{msg['role'].capitalize()}:</b> {msg['content']}",

                    styles["BodyText"]

                )

            )

        doc.build(story)

        return FileResponse(

            path=filepath,

            filename="ChatHistory.pdf",

            media_type="application/pdf"

        )

    raise HTTPException(

        status_code=400,

        detail="Supported formats: pdf, txt"

    )


# =====================================
# DEBUG ROUTES
# =====================================

print("\n========== REGISTERED ROUTES ==========")

for route in app.routes:

    print(route.path)

print("=======================================\n")