import random
from groq import Groq
import os

# 🎯 Generate soal berdasarkan jurusan
def generate_questions(jurusan: str):
    if jurusan.lower() == "teknik informatika":
        return [
            {
                "question": "Apa itu algoritma?",
                "options": ["Langkah logis", "Hardware", "Database", "UI"],
                "answer": "Langkah logis"
            },
            {
                "question": "Bahasa pemrograman?",
                "options": ["Python", "Photoshop", "Excel", "Word"],
                "answer": "Python"
            }
        ]

    elif jurusan.lower() == "psikologi":
        return [
            {
                "question": "Apa itu perilaku manusia?",
                "options": ["Respon", "Kode", "Data", "Algoritma"],
                "answer": "Respon"
            }
        ]

    return []

def calculate_score(questions, user_answers):
    correct = 0

    for i, q in enumerate(questions):
        if user_answers[i] == q["answer"]:
            correct += 1

    score = (correct / len(questions)) * 100
    return score

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
    "question": "...",
    "options": ["A", "B", "C", "D"],
    "answer": "..."
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

import json
import re

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