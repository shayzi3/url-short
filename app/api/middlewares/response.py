import json

from typing import Any, Mapping
from fastapi import Response, BackgroundTasks



class HTTPResponse(Response):
     media_type = "application/json"
     
     def __init__(
          self,
          content: Any,
          status_code: int = 200,
          headers: Mapping[str, str] | None = None,
          media_type: str | None = None,
          background: BackgroundTasks | None = None,
     ) -> None:
          self.content = content
          self.status_code = status_code
          
          super().__init__(content, status_code, headers, media_type, background)
          
          
     def render(self, _: Any) -> bytes:
          my_content = {
               "message": self.content,
               "status": self.status_code,
          }
          
          return json.dumps(
               my_content,
               ensure_ascii=False,
               allow_nan=False,
               indent=None,
               separators=(",", ":"),
          ).encode("utf-8")
     