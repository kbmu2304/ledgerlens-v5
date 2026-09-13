from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Numeric, Enum, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
import enum
from app.db.base import Base


class AccountType(str, enum.Enum):
    CHECKING = "checking"
    SAVINGS = "savings"
    CREDIT_CARD = "credit_card"
    INVESTMENT = "investment"
    LOAN = "loan"
    OTHER = "other"


class Account(Base):
    __tablename__ = "accounts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id = Column(String, ForeignKey("organizations.id"), nullable=False, index=True)
    account_number = Column(String(255), nullable=False, index=True)
    account_name = Column(String(255), nullable=False)
    account_type = Column(Enum(AccountType), nullable=False, index=True)
    institution_name = Column(String(255))
    current_balance = Column(Numeric(15, 2), default=0)
    currency = Column(String(3), default="USD")
    is_active = Column(Boolean, default=True, index=True)
    description = Column(Text)
    last_synced = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    organization = relationship("Organization", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account", cascade="all, delete-orphan")
    findings = relationship("Finding", back_populates="account", cascade="all, delete-orphan")
