import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )


class Bets(Base):
    __tablename__ = "bets"

    name: Mapped[str] = mapped_column(nullable=False)
    coefficient: Mapped[Decimal] = mapped_column(nullable=False)
    bet_at: Mapped[datetime] = mapped_column(default=func.now())
    money_amount: Mapped[float] = mapped_column(nullable=False)
    result: Mapped[int] = mapped_column(nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    event_id: Mapped[uuid.UUID] = mapped_column(nullable=False)

    user: Mapped["Users"] = relationship("Users", back_populates="bets")


class Users(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[bytes] = mapped_column(nullable=False)
    balance: Mapped[float] = mapped_column(default=0, nullable=False)

    bets: Mapped[list["Bets"]] = relationship(
        "Bets", back_populates="user", cascade="all, delete-orphan"
    )
