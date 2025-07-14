import httpx
import time

API_URL = "http://127.0.0.1:8000/generate-paper"

test_payload = {
    "subject": "Math",
    "grade": "10",
    "topics": ["Quadratic Equations", "Linear Equations", "Circles"],
    "difficulty_distribution": {
        "Easy": 3,
        "Medium": 5,
        "Hard": 2
    }
}

def benchmark_paper_generation():
    start_time = time.time()

    with httpx.Client(timeout=60.0) as client:
        response = client.post(API_URL, json=test_payload)
    
    end_time = time.time()
    elapsed = end_time - start_time

    print(f"Status Code: {response.status_code}")
    print(f"Time Taken: {elapsed:.2f} seconds")
    print(f"Number of Questions: {len(response.json()['paper'])}")

    # Optional: Print one sample question
    print("\nSample Question:\n", response.json()['paper'][0]['question_text'])

if __name__ == "__main__":
    benchmark_paper_generation()
