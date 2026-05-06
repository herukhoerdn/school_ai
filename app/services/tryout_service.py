import random
from groq import Groq
import os
import json
import re


# 🎯 Generate soal berdasarkan jurusan
def generate_questions(jurusan: str):
    if jurusan.lower() == "teknik informatika":
        return [
            {
                "question": "Apa itu algoritma?",
                "options": ["A. Langkah logis", "B. Hardware", "C. Database", "D. UI"],
                "correct_answer": "A"
            },
            {
                "question": "Bahasa pemrograman?",
                "options": ["A. Python", "B. Photoshop", "C. Excel", "D. Word"],
                "correct_answer": "A"
            }
        ]

    elif jurusan.lower() == "psikologi":
        return [
            {
                "question": "Apa itu perilaku manusia?",
                "options": ["A. Respon", "B. Kode", "C. Data", "D. Algoritma"],
                "correct_answer": "A"
            }
        ]

    return []

def calculate_score(user_answers, questions):
    total_questions = len(questions)

    if total_questions == 0:
        return 0

    correct_count = 0

    for i in range(total_questions):
        if i < len(user_answers):
            if user_answers[i] == questions[i].correct_answer:
                correct_count += 1

    score = (correct_count / total_questions) * 100

    return round(score, 2)

def predict_chance(score, kampus_list):
    hasil = []

    for kampus in kampus_list:
        if score >= 85:
            chance = random.randint(80, 95)
        elif score >= 70:
            chance = random.randint(60, 80)
        else:
            chance = random.randint(30, 60)

        hasil.append({
            "kampus": kampus,
            "peluang": chance
        })

    return hasil

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_questions_ai(jurusan, level="medium"):
    prompt = f"""
Buatkan 5 soal pilihan ganda untuk jurusan {jurusan} dengan tingkat kesulitan {level}.

Format JSON:
[
  {{
    "question": "Apa yang dimaksud algoritma?",
    "options": [
      "A. Sebuah prosedur sistematis",
      "B. Sebuah perangkat keras",
      "C. Sebuah database",
      "D. Sebuah jaringan komputer"
    ],
    "correct_answer": "A"
  }}
]
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    text = response.choices[0].message.content

    return parse_json(text)
def parse_json(text):
    try:
        match = re.search(r"\[.*\]", text, re.DOTALL)
        return json.loads(match.group())
    except:
        print("ERROR PARSE:", text)
        return []
    
def get_level_from_score(score):
    if score >= 85:
        return "hard"
    elif score >= 60:
        return "medium"
    else:
        return "easy"
    
def generate_adaptive_questions(jurusan, prev_score=None):
    if prev_score is None:
        level = "medium"
    else:
        level = get_level_from_score(prev_score)

    return generate_questions_ai(jurusan, level)