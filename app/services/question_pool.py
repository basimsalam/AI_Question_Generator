# app/services/question_pool.py

used_questions = set()

def is_duplicate(question_text: str) -> bool:
    """Check if a question has already been used."""
    if question_text in used_questions:
        return True
    used_questions.add(question_text)
    return False

def clear_pool():
    """Reset the question pool. Can be called per session/test."""
    used_questions.clear()
