import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# 🔹 STEP 1: AI call
def analyze_answers_ai(answers: list[str]):
    prompt = f"""
Kamu adalah AI career counselor.

User menjawab:
{answers}

Tugas kamu:
- Berikan TOP 3 rekomendasi jurusan kuliah
- Berikan persentase kecocokan (0-100)
- Berikan alasan
- Berikan prospek karir
- Berikan tips

WAJIB output JSON valid TANPA teks tambahan:
[
  {{
    "jurusan": "...",
    "persentase": 90,
    "alasan": "...",
    "prospek": ["...", "..."],
    "tips": "..."
  }}
]
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content


# 🔹 STEP 2: PARSE JSON (INI YANG KAMU TANYA)
def analyze_and_parse(answers):
    raw = analyze_answers_ai(answers)

    # 🔥 ambil hanya bagian JSON
    start = raw.find("[")
    end   = raw.rfind("]") + 1
    json_str = raw[start:end]

    try:
        return json.loads(json_str)
    except Exception as e:
        print("ERROR PARSE:", raw)
        return []