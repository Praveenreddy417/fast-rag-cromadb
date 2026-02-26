from pydantic import BaseModel
from typing import Optional, List, Dict

class ChatRequest(BaseModel):
    sessionId: str
    message: str
    userRole: str
    context: Optional[Dict] = None


class KBReference(BaseModel):
    id: str
    title: str


class Guardrail(BaseModel):
    blocked: bool
    reason: Optional[str] = None


class ChatResponse(BaseModel):
    answer: str
    kbReferences: List[KBReference]
    confidence: float
    tier: str
    severity: str
    needsEscalation: bool
    guardrail: Guardrail
