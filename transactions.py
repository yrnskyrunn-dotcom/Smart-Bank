from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..database import get_db
from .. import models, schemas
from ..auth import get_current_user

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("/transfer", response_model=schemas.TransactionOut)
def transfer(payload: schemas.TransferIn, db: Session = Depends(get_db), user=Depends(get_current_user), x_idempotency_key: str | None = Header(default=None)):
    if payload.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be > 0")
    if payload.from_account_id == payload.to_account_id:
        raise HTTPException(status_code=400, detail="Cannot transfer to the same account")

    from_acct = db.get(models.Account, payload.from_account_id)
    to_acct = db.get(models.Account, payload.to_account_id)
    if not from_acct or not to_acct:
        raise HTTPException(status_code=404, detail="Account not found")
    if from_acct.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed to move funds from this account")

    # idempotency check
    if x_idempotency_key:
        existing = db.execute(select(models.Transaction).where(models.Transaction.idempotency_key == x_idempotency_key)).scalar_one_or_none()
        if existing:
            return existing

    if from_acct.balance < payload.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    # Atomic transfer
    from_acct.balance -= payload.amount
    to_acct.balance += payload.amount
    tx = models.Transaction(from_account_id=from_acct.id, to_account_id=to_acct.id, amount=payload.amount, description=payload.description, idempotency_key=x_idempotency_key)
    db.add(tx)
    db.add(from_acct)
    db.add(to_acct)
    db.commit()
    db.refresh(tx)
    return tx

@router.get("/", response_model=list[schemas.TransactionOut])
def history(db: Session = Depends(get_db), user=Depends(get_current_user)):
    accounts = db.query(models.Account.id).filter(models.Account.user_id == user.id).all()
    acct_ids = [a[0] for a in accounts]
    if not acct_ids:
        return []
    txs = db.query(models.Transaction).filter(
        (models.Transaction.from_account_id.in_(acct_ids)) | (models.Transaction.to_account_id.in_(acct_ids))
    ).order_by(models.Transaction.created_at.desc()).all()
    return txs
