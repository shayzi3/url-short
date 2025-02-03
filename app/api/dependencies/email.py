from typing import Annotated
from fastapi import Depends, HTTPException, status

from app.schemas import TokenPayloadModel
from app.core.security import access_security


async def account_already_verifed(
     current_user: Annotated[TokenPayloadModel, Depends(access_security)]
) -> None:
     if current_user.is_verifed is True:
          raise HTTPException(
               detail="Account already verifed!",
               status_code=status.HTTP_400_BAD_REQUEST
          )