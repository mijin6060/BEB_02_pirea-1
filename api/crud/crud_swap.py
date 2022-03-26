from sqlalchemy.orm import Session
from model.models import SwapSign

def create_swap(db: Session, address: str, sign: dict):
    row_swaps = db.query(SwapSign).filter(SwapSign.address == address).count()
    swapcode = address + str(row_swaps+1)
    row_swap = SwapSign(address=address, swapcode=swapcode, sign=sign)

    db.add(row_swap)
    db.commit()
    db.refresh(row_swap)

    return swapcode

def get_swapcode_sign(db: Session,  swapcode: str):
    sign_code = db.query(SwapSign).filter(SwapSign.swapcode == swapcode).first()

    return sign_code
