from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse

from app.api.dependencies.url import get_access_or_api, Payload
from app.api.dependencies.timeout import Timeout
from .service import UrlService, get_url_service
from .schema import UserSendUrl, ReturnUrl



url_router = APIRouter(tags=["Url"])



@url_router.post(
     path="/api/v1/url/",
     dependencies=[
          Depends(Timeout(route="get_url", seconds=12))
     ]
)
async def get_short_url(
     url: UserSendUrl,
     current_user: Annotated[Payload, Depends(get_access_or_api)],
     service: Annotated[UrlService, Depends(get_url_service)]
) -> ReturnUrl:
     return await service.get_short_url(
          current_user=current_user,
          url=str(url.url)
     )
     
     
     
@url_router.get(path="/url/{url_id}/")
async def get_url_by_id(
     url_id: str,
     service: Annotated[UrlService, Depends(get_url_service)]
) -> RedirectResponse:
     redirect_url = await service.get_url_by_id(id=url_id)
     return RedirectResponse(url=redirect_url)