from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


# =====================================
# USERS TABLE
# =====================================

class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String,
        unique=True,
        nullable=False
    )

    password = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    


# =====================================
# CHATS TABLE
# =====================================

class Chat(Base):

    __tablename__ = "chats"

    id = Column(
        String,
        primary_key=True
    )

    username = Column(
        String,
        nullable=False
    )

    filename = Column(
        String,
        nullable=False
    )

    created_at = Column(
        String
    )

    updated_at = Column(
        String
    )

    
    messages = relationship(
        "Message",
        back_populates="chat",
        cascade="all, delete"
    )


# =====================================
# MESSAGES TABLE
# =====================================

class Message(Base):

    __tablename__ = "messages"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    chat_id = Column(
        String,
        ForeignKey("chats.id")
    )

    role = Column(
        String,
        nullable=False
    )

    content = Column(
        Text,
        nullable=False
    )

    time = Column(
        String
    )

    chat = relationship(
        "Chat",
        back_populates="messages"
    )