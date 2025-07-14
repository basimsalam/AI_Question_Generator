import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-70b-8192"  # or use a smaller version if needed


def generate_question(topic: str, difficulty: str, question_type:str ,kb_data: dict = None,template: str = None):
    objectives = "\n".join(kb_data.get("learning_objectives", [])) if kb_data else ""
    key_facts = "\n".join(kb_data.get("key_facts", [])) if kb_data else ""
    prompt = f"""
    Generate a clean, exam-ready {question_type.lower()} question only — no explanations, no intro.

    Subject: Auto
    Grade: 10
    Topic: {topic}
    Difficulty: {difficulty}
    
    Learning Objectives:
    {objectives}

    Key Facts:
    {key_facts}

    Only return the actual question in the specified type. Do not include metadata, marks, or formatting unless needed for clarity.

    Examples:
    - MCQ: What is the function of the lungs? A) Digestion B) Respiration C) Circulation D) Protection
    - Short Answer: Define osmosis with one example.
    - Long Answer: Explain the nitrogen cycle in detail with labeled diagram.
    """

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You generate school-level exam questions for teachers."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(GROQ_URL, headers=headers, json=payload)
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"].strip()
        return content
    except Exception as e:
        return f"Error generating question: {str(e)}"
