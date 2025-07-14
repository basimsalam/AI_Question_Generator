import json
from pathlib import Path

KB_PATH = Path("data/sample_kb.json")


def load_knowledge_base():
    with open(KB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_subjects():
    kb = load_knowledge_base()
    return list(kb.keys())


def get_topics(subject: str, grade: str):
    kb = load_knowledge_base()
    topics = []

    if subject in kb and grade in kb[subject]:
        for unit in kb[subject][grade].values():
            topics.extend(unit.get("topics", []))
    return topics


def load_topic_knowledge(subject: str, grade: str, topic: str):
    kb = load_knowledge_base()
    try:
        units = kb.get(subject, {}).get(grade, {})
        for unit in units.values():
            for t in unit.get("topics", []):
                if isinstance(t, dict) and t.get("name") == topic:
                    return t
                elif isinstance(t, str) and t == topic:
                    return {}  # Topic found but no detailed metadata
    except Exception as e:
        print(f"Error retrieving topic knowledge: {e}")
    return {}
