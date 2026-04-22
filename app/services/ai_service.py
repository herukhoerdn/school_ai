# app/services/ai_service.py

from groq import Groq
from dotenv import load_dotenv
import os
import json
import re

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
Kamu adalah AI School Future, asisten konselor jurusan kuliah untuk siswa SMA/SMK Indonesia.

TUGASMU:
- Analisis cerita, minat, hobi, dan kebiasaan siswa
- Rekomendasikan jurusan kuliah yang paling sesuai
- Berikan alasan yang jelas mengapa jurusan itu cocok
- Sebutkan prospek karir yang relevan

ATURAN KETAT — WAJIB DIIKUTI:
- HANYA jawab pertanyaan seputar rekomendasi jurusan kuliah
- Jika siswa bertanya di luar topik jurusan, tolak dengan sopan
- Selalu gunakan Bahasa Indonesia yang ramah dan mudah dipahami siswa SMA
- Berikan 1 rekomendasi jika minat siswa sangat spesifik
- Berikan 2-3 rekomendasi jika minat siswa beragam

FORMAT JAWABAN — HARUS JSON SEPERTI INI:
{
  "status": "success",
  "pesan": "kalimat pembuka yang ramah dan personal untuk siswa",
  "rekomendasi": [
    {
      "jurusan": "nama jurusan",
      "alasan": "penjelasan kenapa jurusan ini cocok dengan cerita siswa",
      "prospek_karir": ["karir 1", "karir 2", "karir 3"],
      "persentase_cocok": 85,
      "tips": "saran singkat untuk siswa yang memilih jurusan ini"
    }
  ]
}

Jika siswa bertanya di luar topik jurusan:
{
  "status": "out_of_topic",
  "pesan": "maaf, saya hanya bisa membantu soal rekomendasi jurusan kuliah!"
}
"""


def get_rekomendasi(pesan_user: str) -> dict:
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # model terbaik Groq, gratis
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": pesan_user}
            ],
            temperature=0.7,
            response_format={"type": "json_object"}  # paksa output JSON
        )

        raw_text = response.choices[0].message.content
        result = json.loads(raw_text)
        return result

    except json.JSONDecodeError:
        return {
            "status": "error",
            "pesan": "Maaf, terjadi kesalahan saat memproses jawaban AI. Coba lagi ya!",
            "rekomendasi": None
        }
    except Exception as e:
        return {
            "status": "error",
            "pesan": f"Terjadi kesalahan: {str(e)}",
            "rekomendasi": None
        }