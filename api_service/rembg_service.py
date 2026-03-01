from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

from rembg import new_session, remove
from rembg.sessions.base import BaseSession


@dataclass(frozen=True)
class RemoveParams:
    alpha_matting: bool = False


class RembgService:
    def __init__(self, default_model: str) -> None:
        self._default_model = default_model
        self._sessions: Dict[str, BaseSession] = {}

    def get_session(self, model: Optional[str] = None) -> BaseSession:
        model_name = model or self._default_model
        session = self._sessions.get(model_name)
        if session is None:
            session = new_session(model_name)
            self._sessions[model_name] = session
        return session

    def remove_background(self, image_bytes: bytes, *, model: Optional[str], params: RemoveParams) -> bytes:
        session = self.get_session(model)
        return remove(image_bytes, session=session, alpha_matting=params.alpha_matting)

