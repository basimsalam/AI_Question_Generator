from pydantic import BaseModel
from typing import List, Dict, Optional,Literal


# # 🎯 Question schema
# class Question(BaseModel):
#     question_text: str
#     topic: str
#     subject: str
#     difficulty: str  # "Easy", "Medium", "Hard"
#     type: str  # "MCQ", "Descriptive", "Fill in the Blank", etc.


# 📥 Request schema to generate a paper
class GeneratePaperRequest(BaseModel):
    subject: str
    grade: str
    topics: List[str]
    difficulty_distribution: Dict[str, int]  # e.g., {"Easy": 3, "Medium": 5, "Hard": 2}
    question_types: List[Literal["MCQ", "Short Answer", "Long Answer"]]


# 📤 Response schema for generated paper
class GeneratePaperResponse(BaseModel):
    paper: dict
