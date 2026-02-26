# from fastapi import APIRouter
# from pydantic import BaseModel
# from app.services.rag_service import generate_answer

# router = APIRouter()

# class ChatRequest(BaseModel):
#     question: str

# @router.post("/chat")
# def chat(request: ChatRequest):
#     answer = generate_answer(request.question)
#     return {"answer": answer}

from fastapi import APIRouter
from app.models.chat_models import ChatRequest, ChatResponse, KBReference, Guardrail
from app.services.session_service import get_history, add_message
from app.services.rag_service import generate_answer
from app.services.classifier_service import classify_issue
from app.services.guardrail_service import check_guardrail

router = APIRouter()

@router.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    # 1️⃣ Guardrail
    blocked, reason = check_guardrail(request.message)

    if blocked:
        return ChatResponse(
            answer="Request blocked due to policy violation.",
            kbReferences=[],
            confidence=0.0,
            tier="N/A",
            severity="N/A",
            needsEscalation=True,
            guardrail=Guardrail(blocked=True, reason=reason)
        )

    # 2️⃣ Load session history
    history = get_history(request.sessionId)

    # 3️⃣ Generate answer
    answer, kb_refs_raw, confidence = generate_answer(
        request.message,
        history
    )

    if not answer:
        answer = "The information is not available in the provided documents."

    # 4️⃣ Classify
    tier, severity = classify_issue(request.message)

    needs_escalation = True if severity == "HIGH" else False

    # 5️⃣ Save session
    add_message(request.sessionId, "user", request.message)
    add_message(request.sessionId, "assistant", answer)

    # 6️⃣ Format KB refs
    kb_refs = [
        KBReference(id=ref["id"], title=ref["title"])
        for ref in kb_refs_raw
    ]

    return ChatResponse(
        answer=answer,
        kbReferences=kb_refs,
        confidence=confidence,
        tier=tier,
        severity=severity,
        needsEscalation=needs_escalation,
        guardrail=Guardrail(blocked=False, reason=None)
    )
