from typing import Optional

import uvicorn
from eth_account.messages import encode_defunct
from fastapi import FastAPI
from uuid import UUID
from uuid import uuid4
from pydantic import BaseModel
from web3.auto import w3
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


phrase: UUID = uuid4()


class Auth(BaseModel):
    signed_message: str
    description: Optional[str] = None


@app.post("/auth")
async def authentication(body: Auth):
    message = encode_defunct(text=f'{phrase}')
    public_key = w3.eth.account.recover_message(message, signature=body.signed_message)
    return {"public_key": public_key}


@app.get("/uuid")
async def root():
    return {"uuid": phrase}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)