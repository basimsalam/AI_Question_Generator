# app/routes.py
from fastapi import APIRouter
from app.models.schema import GeneratePaperRequest, GeneratePaperResponse
import itertools
from app.services.knowledge_base import get_subjects, get_topics
from app.services.knowledge_base import load_topic_knowledge


from app.utils.caching import is_duplicate_question, add_to_question_pool, clear_question_pool
from app.utils.caching import clear_all_cached_questions
from app.services.generator import generate_question
from app.utils.caching import (
    is_duplicate_question,
    add_to_question_pool,
    clear_question_pool,
    get_cached_question,
    cache_question
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

            # Check Redis cache
            question_text = get_cached_question(topic, difficulty_level, question_type)
            kb_data = load_topic_knowledge(request.subject, request.grade, topic)
            if not question_text:
                retry = 0
                question_text = generate_question(topic=topic, difficulty=difficulty_level, question_type=question_type,kb_data=kb_data)

                while is_duplicate_question(user_id, question_text) and retry < 3:
                    question_text = generate_question(topic=topic, difficulty=difficulty_level, question_type=question_type,kb_data=kb_data)
                    retry += 1

                # Save to Redis cache
                cache_question(topic, difficulty_level, question_type, question_text)

            add_to_question_pool(user_id, question_text)
            paper[f"Question {question_number}"] = question_text
            question_number += 1

    return GeneratePaperResponse(paper=paper)


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