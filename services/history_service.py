from sqlalchemy.orm import Session
from database import SessionLocal
from models import Chat, Message

import uuid
from datetime import datetime


# =====================================
# CREATE CHAT
# =====================================

def create_chat(username, filename):

    db: Session = SessionLocal()

    try:

        now = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        chat = Chat(

            id=str(uuid.uuid4()),

            username=username,

            filename=filename,

            created_at=now,

            updated_at=now

        )

        db.add(chat)

        db.commit()

        db.refresh(chat)

        return {

            "id": chat.id,

            "username": chat.username,

            "filename": chat.filename,

            "created_at": chat.created_at,

            "updated_at": chat.updated_at,

            "messages": []

        }

    finally:

        db.close()


# =====================================
# ADD MESSAGE
# =====================================

def add_message(
    chat_id,
    role,
    content
):

    db: Session = SessionLocal()

    try:

        message = Message(

            chat_id=chat_id,

            role=role,

            content=content,

            time=datetime.now().strftime("%H:%M:%S")

        )

        db.add(message)

        chat = db.query(Chat).filter(
            Chat.id == chat_id
        ).first()

        if chat:

            chat.updated_at = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        db.commit()

        return True

    finally:

        db.close()


# =====================================
# LOAD HISTORY
# =====================================

def load_history(username=None):

    db: Session = SessionLocal()

    try:

        query = db.query(Chat)

        if username:

            query = query.filter(
                Chat.username == username
            )

        chats = query.order_by(
            Chat.updated_at.desc()
        ).all()

        history = []

        for chat in chats:

            history.append({

                "id": chat.id,

                "username": chat.username,

                "filename": chat.filename,

                "created_at": chat.created_at,

                "updated_at": chat.updated_at,

                "messages": []

            })

        return history

    finally:

        db.close()




# =====================================
# GET SINGLE CHAT
# =====================================

def get_chat(chat_id, username=None):

    db: Session = SessionLocal()

    try:

        chat = db.query(Chat).filter(
            Chat.id == chat_id
        ).first()

        if not chat:
            return None

        if username and chat.username != username:
            return None

        messages = db.query(Message).filter(
            Message.chat_id == chat.id
        ).order_by(Message.id.asc()).all()

        return {

            "id": chat.id,

            "username": chat.username,

            "filename": chat.filename,

            "created_at": chat.created_at,

            "updated_at": chat.updated_at,

            "messages": [

                {

                    "role": message.role,

                    "content": message.content,

                    "time": message.time

                }

                for message in messages

            ]

        }

    finally:

        db.close()


# =====================================
# DELETE CHAT
# =====================================

def delete_chat(chat_id):

    db: Session = SessionLocal()

    try:

        chat = db.query(Chat).filter(
            Chat.id == chat_id
        ).first()

        if not chat:
            return False

        db.delete(chat)

        db.commit()

        return True

    finally:

        db.close()


# =====================================
# CLEAR HISTORY
# =====================================

def clear_history():

    db: Session = SessionLocal()

    try:

        db.query(Message).delete()

        db.query(Chat).delete()

        db.commit()

        return True

    finally:

        db.close()