from collections import defaultdict

# sessionId → list of messages
sessions = defaultdict(list)

def get_history(session_id: str):
    return sessions[session_id]

def add_message(session_id: str, role: str, content: str):
    sessions[session_id].append({
        "role": role,
        "content": content
    })
