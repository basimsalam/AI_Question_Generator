# app/routes.py
from datetime import datetime
from fastapi import APIRouter
from app.models.schema import GeneratePaperRequest, GeneratePaperResponse
from app.utils.response import success_response, error_response

import itertools
from app.services.knowledge_base import get_subjects, get_topics
from app.services.knowledge_base import load_topic_knowledge
from app.utils.document_generator import save_question_paper_as_pdf, save_question_paper_as_word
from fastapi.responses import FileResponse
from app.utils.caching import is_duplicate_question, add_to_question_pool, clear_question_pool
from app.utils.caching import clear_all_cached_questions
from app.services.generator import generate_question
from app.utils.caching import (
    is_duplicate_question,
    add_to_question_pool,
    clear_question_pool
)



router = APIRouter()


@router.get("/")
def read_root():
    return {"message": "Welcome to the AI Question Paper Generator API"}

@router.post("/generate-paper", response_model=GeneratePaperResponse)
def generate_paper(request: GeneratePaperRequest):
    user_id = "demo_user"
    paper = {}
    clear_question_pool(user_id)

    topic_cycle = itertools.cycle(request.topics)
    type_cycle = itertools.cycle(request.question_types)
    question_number = 1

    for difficulty_level, count in request.difficulty_distribution.items():
        for _ in range(count):
            topic = next(topic_cycle)
            question_type = next(type_cycle)
            knowledge = load_topic_knowledge(request.subject, request.grade, topic)

            question_text = generate_question(topic=topic, difficulty=difficulty_level, question_type=question_type,kb_data=knowledge)

            retry = 0
            while is_duplicate_question(user_id, question_text) and retry < 3:
                question_text = generate_question(topic=topic, difficulty=difficulty_level, question_type=question_type)
                retry += 1

            add_to_question_pool(user_id, question_text)
            paper[f"Question {question_number}"] = question_text
            question_number += 1

    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    word_file = save_question_paper_as_word(paper, f"question_paper_{timestamp}.docx")
    pdf_file = save_question_paper_as_pdf(paper, f"question_paper_{timestamp}.pdf")

    
    return success_response(
    body={
        "paper": paper,
        "download_links": {
            "pdf": f"/download/pdf/{timestamp}",
            "word": f"/download/word/{timestamp}"
        }
    },
    message="Question paper generated successfully"
)
    



@router.get("/subjects")
def fetch_subjects():
    return {"subjects": get_subjects()}


@router.get("/topics")
def fetch_topics(subject: str, grade: str):
    return {"topics": get_topics(subject, grade)}



@router.get("/clear-cache")
def clear_cache_endpoint():
    clear_all_cached_questions()
    return {"message": "All cached questions cleared."}


@router.get("/download/pdf/{timestamp}")
def download_pdf(timestamp: str):
    path = f"generated_papers/question_paper_{timestamp}.pdf"
    return FileResponse(path, media_type='application/pdf', filename=f"question_paper_{timestamp}.pdf")


@router.get("/download/word/{timestamp}")
def download_word(timestamp: str):
    path = f"generated_papers/question_paper_{timestamp}.docx"
    return FileResponse(path, media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document', filename=f"question_paper_{timestamp}.docx")
