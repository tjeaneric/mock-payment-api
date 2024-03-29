from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select

from database import sessionDep
from middlewares.protect import protect
from models import Transaction, TransactionRequest, User

router = APIRouter(prefix="/transactions", tags=["Transactions"], dependencies=[Depends(protect)])


@router.post("", status_code=status.HTTP_201_CREATED)
def create_transaction(session: sessionDep, tx_data: TransactionRequest) -> Transaction:
    """
    Check if is greater than 0
    If not, return error with a message
    """
    if tx_data.amount <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Amount should be greater than 0")

    """
    Check if receiver 's phone number consists of 10 digits
    If not, return error with a message
    """
    if len(tx_data.receiver_phone) != 10:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Receiver phone number must be 10 digits")

    """
    Check if there is a value in the amount field
    If not, return error with a message
    """
    if len(tx_data.product) <= 2:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Please enter a valid product")

    # New transaction instance
    transaction = Transaction(**tx_data.model_dump())
    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    return transaction


@router.get("", response_model=list[Transaction], status_code=status.HTTP_200_OK)
def get_transactions(session: sessionDep, current_user: User = Depends(protect)):
    statement = select(Transaction).where(Transaction.sender_phone == current_user.phone,
                                          Transaction.deleted_status == False)
    transactions = session.exec(statement).all()
    if len(transactions) < 1:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail="You do not have any transactions")
    return transactions


@router.patch("/{trans_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(session: sessionDep, trans_id: str, current_user: User = Depends(protect)):
    transaction = session.get(Transaction, trans_id)
    """
    Check if transaction exists and not deleted
    If not, return error with a message
    """
    if not (transaction and not transaction.deleted_status):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    """
    Check if the current logged in user is deleting his/her own transaction
    If not, return error with a message
    """
    if transaction.sender_phone != current_user.phone:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not allowed to perform this action")

    transaction.deleted_status = True
    session.add(transaction)
    session.commit()
    return {"message": "Transaction deleted successfully!"}
