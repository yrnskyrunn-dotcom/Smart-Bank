from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .database import Base
import enum

class AccountType(str, enum.Enum):
    checking = "checking"
    savings = "savings"

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped = mapped_column(DateTime(timezone=True), server_default=func.now())

    accounts = relationship("Account", back_populates="owner")

class Account(Base):
    __tablename__ = "accounts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), default="Main")
    type: Mapped[AccountType] = mapped_column(Enum(AccountType), default=AccountType.checking)
    balance: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped = mapped_column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="accounts")
    outgoing = relationship("Transaction", back_populates="from_account", foreign_keys="Transaction.from_account_id")
    incoming = relationship("Transaction", back_populates="to_account", foreign_keys="Transaction.to_account_id")

class Transaction(Base):
    __tablename__ = "transactions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    from_account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), nullable=True)
    to_account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), nullable=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str] = mapped_column(String(255), default="")
    idempotency_key: Mapped[str] = mapped_column(String(64), nullable=True, index=True)
    created_at: Mapped = mapped_column(DateTime(timezone=True), server_default=func.now())

    from_account = relationship("Account", foreign_keys=[from_account_id], back_populates="outgoing")
    to_account = relationship("Account", foreign_keys=[to_account_id], back_populates="incoming")
