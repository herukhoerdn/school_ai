# frontend/pages/Dashboard.py

import streamlit as st
import requests

st.set_page_config(page_title="AI School Future", layout="wide")

API_URL = "http://127.0.0.1:8000/api"

# --- GUARD: Cek apakah user sudah login ---
if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Kamu belum login! Silakan login terlebih dahulu.")
    st.switch_page("Login.py")
    st.stop()

# Data user dari session
user_data = st.session_state.user
nama_user = user_data.get("nama_lengkap", "Siswa")
user_id   = user_data.get("id")
# =========================
# INIT SESSION STATE TRYOUT
# =========================

if "tryout_started" not in st.session_state:
    st.session_state["tryout_started"] = False

if "tryout_questions" not in st.session_state:
    st.session_state["tryout_questions"] = []

if "tryout_answers" not in st.session_state:
    st.session_state["tryout_answers"] = []

if "selected_kampus" not in st.session_state:
    st.session_state["selected_kampus"] = []

if "selected_jurusan" not in st.session_state:
    st.session_state["selected_jurusan"] = ""
# --- FUNGSI LOAD RIWAYAT DARI DATABASE ---

def load_riwayat_dari_db():
    try:

        print("USER ID =", user_id)

        res = requests.get(
            f"{API_URL}/chat/riwayat/{user_id}"
        )

        data = res.json()

        print(data)

        if data["status"] == "success" and data["data"]:

            messages = []

            for item in data["data"]:

                messages.append({
                    "role": "user",
                    "content": item["pesan_user"]
                })

                if item["respons_ai"]:
                    messages.append({
                        "role": "assistant",
                        "content": item["respons_ai"]
                    })

            return messages

    except Exception as e:
        st.error(str(e))
        print(e)

    return None

def load_riwayat_assessment(user_id):
    try:
        res = requests.get(f"{API_URL}/assessment/riwayat/{user_id}")
        data = res.json()
        if data["status"] == "success":
            return data["data"]
    except:
        pass
    return []

# --- CUSTOM CSS ---
st.markdown("""
<style>

/* =========================
   BACKGROUND
========================= */

.stApp {
    background-color: #19284C;
}

header[data-testid="stHeader"] {
    background-color: #19284C !important;
}

.stbottom > div {
    background-color: #19284C !important;
}

/* =========================
   TEXT UTAMA
========================= */

h1, h2, h3, h4, h5, h6, p {
    color: #FFFFFF !important;
}

/* Label form */
label {
    color: #FFFFFF !important;
    font-weight: 500 !important;
}

/* =========================
   INPUT / SELECTBOX
========================= */

.stSelectbox div[data-baseweb="select"],
.stMultiSelect div[data-baseweb="select"],
.stTextArea textarea,
.stTextInput input {
    background-color: #FFFFFF !important;
    border-radius: 10px !important;
    color: #000000 !important;
}

/* text selected dropdown */
.stSelectbox span,
.stMultiSelect span {
    color: #000000 !important;
}

/* placeholder */
.stSelectbox input,
.stMultiSelect input {
    color: #000000 !important;
}

/* dropdown menu option */
div[role="listbox"] div {
    color: #000000 !important;
    background-color: #FFFFFF !important;
}

/* =========================
   BUTTON
========================= */

/* Tombol utama */
.stButton > button,
.stFormSubmitButton > button {
    background: linear-gradient(135deg, #4F8CFF, #6A5CFF) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 10px 20px !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    transition: 0.3s ease;
}

/* Hover effect */
.stButton > button:hover,
.stFormSubmitButton > button:hover {
    transform: translateY(-2px);
    opacity: 0.95;
}

/* Focus effect */
.stButton > button:focus,
.stFormSubmitButton > button:focus {
    outline: none !important;
    box-shadow: 0 0 0 2px rgba(79,140,255,0.4);
}


/* =========================
   CARD
========================= */

.stat-card {
    background-color: #FFFFFF;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
    color: #000000 !important;
}

/* =========================
   SIDEBAR
========================= */

section[data-testid="stSidebar"] {
    background-color: #D3D3D3;
    border-right: 1px solid #E0E0E0;
}

section[data-testid="stSidebar"] * {
    color: #000000 !important;
}
            
/* WRAPPER */
.chat-wrapper {
    width: 100%;
    max-width: 800px;
    margin: auto;
    padding: 20px;
}

/* ROW */
.chat-row {
    display: flex;
    margin-bottom: 12px;
}

/* ALIGNMENT */
.chat-user {
    justify-content: flex-end;
}

.chat-ai {
    justify-content: flex-start;
}

/* BUBBLE UMUM */
.bubble {
    padding: 12px 16px;
    border-radius: 18px;
    max-width: 90%;
    font-size: 15px;
    line-height: 1.5;
    word-wrap: break-word;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}

/* USER (KANAN) */
.user-bubble {
    background: linear-gradient(135deg, #4F8CFF, #6A5CFF);
    color: white;
    border-bottom-right-radius: 4px;
}

/* AI (KIRI) */
.ai-bubble {
    background-color: #FFFFFF;
    color: #000000;
    border-bottom-left-radius: 4px;
}

/* OPTIONAL: ICON */
.chat-avatar {
    font-size: 20px;
    margin: 0 8px;
}
            
/* PAKSA SEMUA TEKS DI DALAM AI JADI HITAM */
.ai-bubble * {
    color: #000000 !important;
}

</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if "chat_history" not in st.session_state:

    riwayat = load_riwayat_dari_db()

    if riwayat:
        st.session_state.chat_history = {
            "Percakapan Utama": riwayat
        }
    else:
        st.session_state.chat_history = {
            "Percakapan Utama": [
                {
                    "role": "assistant",
                    "content": f"Halo {nama_user}! Yuk mulai tanya tentang jurusan atau karir kamu 🚀"
                }
            ]
        }

if (
    "current_chat" not in st.session_state
    or st.session_state.current_chat is None
):
    st.session_state.current_chat = "Percakapan Utama"
if (
    st.session_state.current_chat is None
    or st.session_state.current_chat not in st.session_state.chat_history
):
    st.session_state.current_chat = "Percakapan Utama"

if "is_loading" not in st.session_state:
    st.session_state.is_loading = False

# --- SIDEBAR ---
with st.sidebar:
    st.title("AI School Future")
    st.markdown("---")

    if st.button("+ Percakapan Baru", use_container_width=True):
        new_id   = len(st.session_state.chat_history) + 1
        new_name = f"Chat {new_id}"
        st.session_state.chat_history[new_name] = [
            {"role": "assistant", "content": f"Halo {nama_user}! Ada yang ingin kamu tanyakan soal jurusan?"}
        ]
        st.session_state.current_chat = new_name
        st.rerun()

    st.markdown("---")
    st.write("### Riwayat Chat")
    for chat_name in list(st.session_state.chat_history.keys()):
        is_active = chat_name == st.session_state.current_chat
        if st.button(
            chat_name,
            key=f"btn_{chat_name}",
            use_container_width=True,
            type="primary" if is_active else "secondary"
        ):
            st.session_state.current_chat = chat_name
            st.rerun()

    st.markdown("---")

    st.write("👤")
    st.write(f"**{nama_user}**")
    st.caption(user_data.get("email", ""))

    if st.button("Logout", use_container_width=True, type="secondary"):
        st.session_state.user         = None
        st.session_state.chat_history = {}
        st.session_state.current_chat = None
        st.switch_page("Login.py")

# --- MAIN CONTENT ---
messages = st.session_state.chat_history[st.session_state.current_chat]

tab1, tab2 = st.tabs(["💬 Chat AI", "🧠 Tes Minat & Bakat"])

# =========================
# TAB 1: CHAT AI (BERSIH)
# =========================
with tab1:
    st.markdown("## 🤖 AI Career Assistant")
    st.caption("Tanyakan jurusan, karir, atau masa depan kamu di sini")
    st.markdown("---")

    # CHAT AREA
    chat_container = st.container()
    with chat_container:
        st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)

        for msg in messages:
            div_class = "chat-user" if msg["role"] == "user" else "chat-ai"
            bubble_class = "user-bubble" if msg["role"] == "user" else "ai-bubble"

            st.markdown(f'''
                <div class="chat-row {div_class}">
                    <div class="bubble {bubble_class}">{msg["content"]}</div>
                </div>
            ''', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.is_loading:
        st.markdown("🤖 *AI sedang menganalisis...*")

    user_input = st.chat_input("💬 Tulis pertanyaan kamu tentang jurusan atau karir...")

    if user_input and not st.session_state.is_loading:

        st.session_state.last_user_message = user_input

        messages.append({
        "role": "user",
        "content": user_input
        })

        st.session_state.chat_history[
        st.session_state.current_chat
        ] = messages

        st.session_state.is_loading = True
        st.rerun()


# =========================
# TAB 2: TRYOUT + TES MINAT
# =========================
with tab2:
    st.subheader("🎯 Tryout Jurusan")

    jurusan = st.selectbox(
    "Pilih jurusan",
    [
        "Teknik Informatika",
        "Psikologi",
        "Manajemen",
        "Kedokteran"
    ] 
     )

    kampus = st.multiselect(
    "Pilih kampus",
    [
        "UI",
        "ITB",
        "UGM",
        "BINUS",
        "UNPAD"
    ]
    )

    # START TRYOUT
    if not st.session_state.tryout_started:
        if st.button("🚀 Mulai Tryout"):
            if len(kampus) < 2:
                st.warning("Pilih minimal 2 kampus!")
            else:
                res = requests.post(
                f"{API_URL}/tryout/start",
                    json={"jurusan": jurusan, "kampus": kampus}
                )
                if res.status_code == 200:
                    data = res.json()
                    if data["status"] == "success":
                         st.session_state.tryout_started = True
                         st.session_state.tryout_questions = data["questions"]
                         st.session_state.selected_kampus = kampus
                         st.rerun()

    # SOAL TRYOUT
    if st.session_state.tryout_started:
        st.markdown("## 📝 Soal Tryout")

        with st.form("form_tryout"):
            answers = []

            for i, q in enumerate(st.session_state.tryout_questions):
                st.write(f"{i+1}. {q['question']}")
                ans = st.radio("Jawaban:", q["options"], key=f"q_{i}")
                answers.append(ans[0])

            submit = st.form_submit_button("📊 Submit")

        if submit:
            res = requests.post(
                f"{API_URL}/tryout/submit",
                json={
                    "user_answers": answers,
                    "questions": st.session_state.tryout_questions,
                    "kampus": st.session_state.selected_kampus
                }
            )

            data = res.json()

            if data["status"] == "success":
                st.success(f"Skor: {data['score']}%")
                score = data["score"]

            if score <= 30:
                st.warning("""
                📚 Jangan menyerah dulu!

                Hasil tryout ini bukan akhir, tapi awal untuk berkembang.
                Coba tingkatkan belajar sedikit demi sedikit setiap hari.

            💡 Tips:
                - Pelajari kembali konsep dasar
                - Latihan soal rutin
                - Fokus pada materi yang masih sulit
                - Jangan takut salah saat belajar

                Semangat! Progress kecil tetap progress 🚀
                """)

            elif score <= 70:
                st.info("""
                🔥 Hasil kamu sudah cukup bagus!
                    Kamu sudah memahami beberapa materi penting.
                    Tinggal meningkatkan konsistensi dan memperbanyak latihan.

                💡 Tips:
                    - Kerjakan tryout lebih sering
                    - Pelajari pembahasan soal yang salah
                    - Latih manajemen waktu saat ujian
                    - Fokus pada kelemahan utama kamu

                    Pertahankan dan terus naikkan skor kamu 💪
                    """)

            else:
                st.success("""
                    🏆 Keren banget!

                        Kemampuan kamu sudah sangat baik dan punya peluang besar masuk kampus impian.

                        💡 Tips:
                            - Pertahankan konsistensi belajar
                            - Perbanyak simulasi ujian asli
                            - Jangan cepat puas
                            - Jaga fokus dan mental saat ujian

                            Gas terus, calon mahasiswa sukses 🚀🎓
                            """)

            for p in data["peluang"]:
                st.write(f"🎓 {p['kampus']}")

                st.progress(p["peluang"] / 100)

                st.caption(f"📈 Peluang diterima: {p['peluang']}%")


# tombol ulang DI LUAR loop
            if st.button("🔄 Ulang", key="ulang_tryout"):
                st.session_state.tryout_started = False
                st.session_state.tryout_questions = []
                st.rerun()

    st.markdown("---")

    st.title("🧠 Tes Minat & Bakat")

    st.markdown("""
        Temukan jurusan yang paling cocok berdasarkan minat dan hobimu.
        Pilih beberapa kategori yang paling menggambarkan diri kamu 🚀
        """)

# =========================
# PILIH MINAT & HOBI
# =========================

    with st.container(border=True):

        minat = st.multiselect(
        "🎯 Pilih Minat",
        [
            "Teknologi",
            "Bisnis",
            "Desain",
            "Kesehatan",
            "Psikologi",
            "Pendidikan",
            "Komunikasi",
            "Sains",
            "Game",
            "Matematika",
            "Sosial",
            "Hukum"
        ],
        placeholder="Pilih beberapa minat..."
    )

    hobi = st.multiselect(
        "🎮 Pilih Hobi",
        [
            "Coding",
            "Game",
            "Menggambar",
            "Menulis",
            "Membaca",
            "Public Speaking",
            "Fotografi",
            "Editing Video",
            "Musik",
            "Olahraga",
            "Eksperimen",
            "Bisnis Online"
        ],
        placeholder="Pilih beberapa hobi..."
    )

    analisis = st.button("🔍 Analisis Minat Bakat")

# =========================
# HASIL ANALISIS
# =========================

    if analisis:

            hasil = []

    # =================
    # TEKNIK INFORMATIKA
    # =================
            if "Teknologi" in minat or "Coding" in hobi:
                hasil.append({
            "jurusan": "Sarjana Teknik Informatika",
            "persen": 92,
            "desc": "Cocok untuk kamu yang suka teknologi, logika, coding, dan pengembangan software.",
            "karier": [
                "Software Engineer",
                "Web Developer",
                "AI Engineer",
                "Cyber Security"
            ]
        })

    # =================
    # BISNIS DIGITAL
    # =================
            if "Bisnis" in minat:
                hasil.append({
            "jurusan": "Sarjana Bisnis Digital",
            "persen": 87,
            "desc": "Cocok untuk kamu yang tertarik dunia bisnis modern dan startup digital.",
            "karier": [
                "Digital Marketer",
                "Business Analyst",
                "Entrepreneur",
                "Content Strategist"
            ]
        })

    # =================
    # GAME DEVELOPMENT
    # =================
            if "Game" in hobi:
                hasil.append({
            "jurusan": "Sarjana Game Development",
            "persen": 84,
            "desc": "Cocok untuk kamu yang suka dunia game, kreativitas, dan teknologi interaktif.",
            "karier": [
                "Game Developer",
                "Game Designer",
                "3D Artist",
                "Game Programmer"
            ]
        })

    # =================
    # DESAIN
    # =================
            if "Desain" in minat or "Menggambar" in hobi:
                hasil.append({
            "jurusan": "Desain Komunikasi Visual",
            "persen": 80,
            "desc": "Cocok untuk kamu yang kreatif dan suka visual design.",
            "karier": [
                "Graphic Designer",
                "UI/UX Designer",
                "Illustrator",
                "Creative Director"
            ]
        })

    # =========================
    # TAMPILKAN HASIL
    # =========================

            if hasil:

                st.markdown("## 🎓 Rekomendasi Jurusan")

            for h in hasil:

                st.markdown(f"### {h['jurusan']}")

                st.progress(h["persen"] / 100)

                st.caption(f"📈 Kecocokan: {h['persen']}%")

                st.info(h["desc"])

                st.markdown("#### 💼 Prospek Karier")

            for karier in h["karier"]:
                st.write(f"✅ {karier}")

            st.markdown("---")

    else:
        st.warning("""
Belum ditemukan jurusan yang cocok.

Coba pilih minat dan hobi lebih banyak supaya sistem bisa menganalisis lebih akurat 🚀
""")

# --- AREA CHAT ---

st.markdown("""
<style>
.chat-wrapper {
    max-width: 700px;
    margin: auto;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)

# --- INPUT & KIRIM KE BACKEND ---    

if st.session_state.is_loading:
    try:
        res  = requests.post(
            f"{API_URL}/chat/rekomendasi",
            json={"pesan": messages[-1]["content"]}
        )
        data = res.json()

        if data["status"] == "success":
            pesan    = data["pesan"]
            rekom    = data.get("rekomendasi", [])
            response = f"{pesan}\n\n"

            for i, r in enumerate(rekom, 1):
                response += f"**{i}. {r['jurusan']}** — {r['persentase_cocok']}% cocok\n"
                response += f"{r['alasan']}\n\n"
                response += f"Prospek karir: {', '.join(r['prospek_karir'])}\n"
                response += f"Tips: {r['tips']}\n\n"
                response += "---\n"

        elif data["status"] == "out_of_topic":
            response = data["pesan"]
        else:
            response = "Maaf, terjadi kesalahan. Coba lagi ya!"

    except Exception:
        response = "Tidak dapat terhubung ke server. Pastikan backend sudah berjalan."

    # Simpan response AI ke database
    try:
        if "last_user_message" in st.session_state:

            print("AKAN SIMPAN CHAT")
            print(user_id)
            print(st.session_state.last_user_message)

            response_save = requests.post(
            f"{API_URL}/chat/simpan",
            json={
                "user_id": user_id,
                "pesan_user": st.session_state.last_user_message,
                "respons_ai": response
    }
)

            print(response_save.status_code)
            print(response_save.text)

    except Exception as e:
        st.error(str(e))
        print(e)

    messages.append({"role": "assistant", "content": response})
    st.session_state.chat_history[st.session_state.current_chat] = messages
    st.session_state.is_loading = False
    st.rerun()

if "tryout_started" not in st.session_state:
    st.session_state.tryout_started = False

if "tryout_questions" not in st.session_state:
    st.session_state.tryout_questions = []

if "tryout_answers" not in st.session_state:
    st.session_state.tryout_answers = []

if "selected_kampus" not in st.session_state:
    st.session_state.selected_kampus = []

if "selected_jurusan" not in st.session_state:
    st.session_state.selected_jurusan = ""