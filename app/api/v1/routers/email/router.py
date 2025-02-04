from typing import Annotated
from fastapi import APIRouter, BackgroundTasks, Depends, Response, Security

from app.api.dependencies.email import account_already_verifed
from app.core.security import access_security
from app.schemas import ResponseModel, TokenPayloadModel
from .service import EmailService, get_email_service
from .schema import Code



email_router = APIRouter(prefix="/api/v1/email", tags=["Email"], dependencies=[Depends(account_already_verifed)])


@email_router.post("/send")
async def send_email(
     current_user: Annotated[TokenPayloadModel, Security(access_security)],
     service: Annotated[EmailService, Depends(get_email_service)],
     background_tasks: BackgroundTasks,
) -> ResponseModel:
     return await service.send_email(
          current_user=current_user,
          bg_task=background_tasks
     )
     
     
     
@email_router.post("/check")
async def check_email(
     code: Code,
     current_user: Annotated[TokenPayloadModel, Security(access_security)],
     service: Annotated[EmailService, Depends(get_email_service)],
     response: Response
) -> ResponseModel:
     status_verify, answer_model = await service.check_email(
          code=code.code,
          current_user=current_user
     )
     if status_verify is True:
          new_token = await access_security.create_token(
               **current_user.verifed_is_true
          )
          response.set_cookie(
               key="access_token",
               value=new_token,
               secure=True
          )
     return answer_model
     