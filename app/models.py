import datetime
import enum

from sqlalchemy import Column, Integer, String, DateTime, Enum, Text, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from typing import List

from .database import Base


class DocumentType(enum.Enum):
    """Enum for different types of documents a user can upload."""

    RESUME = "resume"
    JOB_DESCRIPTION = "job_description"
    OTHER = "other"


class User(Base):
    """User model representing a user in the system."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Define the 0ne to many relationship with Document
    # 'documents' will be a list of document objects associated with each user
    documents: Mapped[List["Document"]] = relationship(
        "Document",
        back_populates="owner",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, is_active={self.is_active})>"

    class Document(Base):
        """Document model for storing details about about uploaded documents. (resumes, job descriptions)"""

        __tablename__ = "documents"

        id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
        user_id: Mapped[int] = mapped_column(
            Integer, ForeignKey('users.id'), nullable=False)

        s3_key: Mapped[str] = mapped_column(String, unique=True, index=True)

        filename: Mapped[str] = mapped_column(String, nullable=False)

        document_type: Mapped[DocumentType] = mapped_column(
            Enum(DocumentType),
            nullable=False
        )

        title: Mapped[str | None] = mapped_column(String, nullable=False)

    # Optional: Store extracted text directly in DB for quick access, or rely on S3 content
    # For MVP, we'll process from S3. If this becomes a performance bottleneck,
    # we can save processed text here after initial NLP.
    # extracted_text: Mapped[str | None] = mapped_column(Text, nullable=True)

        uploaded_at: Mapped[datetime.datetime] = mapped_column(
            DateTime(timezone=True), server_default=func.now())

    # Define the many to one realtion with user
    # 'owner' will be the user object associated with each document
        owner: Mapped["User"] = relationship(
            "User",
            back_populates="documents",
            lazy="joined"
        )

    def __repr__(self):
        return (f"<Document(id={self.id}, user_id={self.user_id}, "
                f"s3_key={self.s3_key}, filename={self.filename}, "
                f"document_type={self.document_type}, title={self.title}, "
                f"uploaded_at={self.uploaded_at})>")
