from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..auth import get_current_user

router = APIRouter(prefix="/accounts", tags=["accounts"])

@router.post("/", response_model=schemas.AccountOut)
def create_account(payload: schemas.AccountCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    acct = models.Account(user_id=user.id, name=payload.name, type=models.AccountType(payload.type))
    db.add(acct)
    db.commit()
    db.refresh(acct)
    return acct

@router.get("/", response_model=list[schemas.AccountOut])
def list_accounts(db: Session = Depends(get_db), user=Depends(get_current_user)):
    accts = db.query(models.Account).filter(models.Account.user_id == user.id).all()
    return accts
