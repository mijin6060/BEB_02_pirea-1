from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel
from crud.crud_swap import *
from crud.crud_abi import *
from database.db import get_db
from sqlalchemy.orm import Session
from web3 import Web3
import os, json

router = APIRouter(
    prefix="/api/v0.1/swap"
)


class Data(BaseModel):
    order: str
    address: str

@router.post("/create", tags=["swap"])
async def get_swap_recent(info: Request, db: Session =Depends(get_db)):
    req_info = await info.json()
    print(req_info['order'])

    swap_code = create_swap(db, str(req_info['address']), req_info['order'], req_info["haveForm"], req_info["wantForm"])

    return swap_code

@router.get("/get", tags=["swap"]) 
async def get_swap_code(swapcode: str, db: Session=Depends(get_db)):
    async def get_swap_url(db: Session, contractAddress: str = "", tokenId: int = 0): 

        abi = await get_create_abi(db, cont_address=contractAddress)
        print("Abi!!!", abi)
        dictret = dict(abi.__dict__)
        print("Abi!!", dictret)

        abi_json_load = json.loads(dictret['abijson'])
        w3 = Web3(Web3.HTTPProvider(SECRET_FILE_WEB3['RINKEBY_END_POINT']))

        cont_address_checksum = w3.toChecksumAddress(contractAddress)
        
        contract_obj = w3.eth.contract(address=cont_address_checksum, abi=abi_json_load)
        print(cont_address_checksum)

        if (tokenId >= 1):
            tokenURI = contract_obj.functions.tokenURI(1).call()
            return tokenURI
        db.close()

    signcode = get_swapcode_sign(db, swapcode=swapcode)
    signcode_dict = dict(signcode.__dict__)
    
    if signcode_dict["wantForm"]["type"] == "ERC721" :
        want_token_url = await get_swap_url(db, contractAddress=signcode_dict["wantForm"]["tokenAddress"], tokenId=int(signcode_dict["wantForm"]["tokenId"]))
        print(want_token_url)
        signcode_dict["want_token_url"] = want_token_url

    
    if signcode_dict["haveForm"]["type"] == "ERC721" :
        have_token_url = await get_swap_url(db, contractAddress=signcode_dict["haveForm"]["tokenAddress"], tokenId= int(signcode_dict["haveForm"]["tokenId"]))
        signcode_dict["have_token_url"] = have_token_url

    return signcode_dict

@router.get("/get/all", tags=["swap"])
async def get_swap_all(db: Session=Depends(get_db), more: int = 1):
    sign_all = get_swapcode_recent_all(db, more)
    return sign_all

@router.get("/get/tokenid/url", tags=["swap"])
async def get_swap(db: Session=Depends(get_db), contractAddress: str = "", tokenId: int = 0): 
    abi = await get_create_abi(db, cont_address=contractAddress)
    dictret = dict(abi.__dict__)

    abi_json_load = json.loads(dictret['abijson'])
    w3 = Web3(Web3.HTTPProvider(SECRET_FILE_WEB3['RINKEBY_END_POINT']))

    cont_address_checksum = w3.toChecksumAddress(contractAddress)
    
    contract_obj = w3.eth.contract(address=cont_address_checksum, abi=abi_json_load)
    print(cont_address_checksum)

    if (tokenId >= 1):
        tokenURI = contract_obj.functions.tokenURI(1).call()
        return tokenURI


