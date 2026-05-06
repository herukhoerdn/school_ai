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
        res  = requests.get(f"{API_URL}/chat/riwayat/{user_id}")
        data = res.json()
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
    except Exception:
        pass
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

</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if "chat_history" not in st.session_state:
    riwayat_db = load_riwayat_dari_db()
    if riwayat_db:
        st.session_state.chat_history = {
            "Percakapan Utama": riwayat_db
        }
    else:
        st.session_state.chat_history = {
            "Percakapan Utama": [
                {"role": "assistant", "content": f"Halo {nama_user}! Ceritakan minat, hobi, atau kesukaanmu — nanti saya bantu rekomendasikan jurusan kuliah yang paling cocok untukmu 😊"}
            ]
        }

if "current_chat" not in st.session_state:
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

    cols_prof = st.columns([1, 4])
    with cols_prof[0]:
        st.write("👤")
    with cols_prof[1]:
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

with tab1:
    st.title(f"💬 {st.session_state.current_chat}")
st.subheader("🎯 Tryout Jurusan")

col1, col2 = st.columns(2)

with col1:
    jurusan = st.selectbox(
        "Pilih jurusan yang kamu minati",
        ["Teknik Informatika", "Psikologi", "Manajemen", "Kedokteran"]
    )

with col2:
    kampus = st.multiselect(
        "Pilih 2-3 kampus tujuan",
        ["UI", "ITB", "UGM", "BINUS", "UNPAD"]
    )

# =========================
# BUTTON MULAI TRYOUT
# =========================

if not st.session_state.tryout_started:
    if st.button("🚀 Mulai Tryout", key="start_tryout"):

        if len(kampus) < 2:
            st.warning("Pilih minimal 2 kampus tujuan.")

        else:
            with st.spinner("Mengambil soal tryout..."):

                res = requests.post(
                    f"{API_URL}/tryout/start",
                    json={
                        "jurusan": jurusan,
                        "kampus": kampus
                    }
                )

                if res.status_code == 200:
                    data = res.json()

                    if data.get("status") == "success":
                        st.session_state.tryout_started = True
                        st.session_state.tryout_questions = data["questions"]
                        st.session_state.selected_kampus = kampus
                        st.rerun()

                else:
                    st.error(f"Gagal mengambil soal: {res.text}")


# =========================
# TAMPILKAN SOAL TRYOUT
# =========================

if st.session_state.tryout_started:
    st.markdown("## 📝 Soal Tryout")

    with st.form("submit_tryout_form"):

        user_answers = []

        for i, q in enumerate(st.session_state.tryout_questions):
            st.markdown(f"### {i+1}. {q['question']}")

            answer = st.radio(
                "Pilih jawaban",
                q["options"],
                key=f"q_{i}"
            )

            # Ambil huruf depan: A / B / C / D
            selected_letter = answer[0]
            user_answers.append(selected_letter)

        submit = st.form_submit_button("📊 Submit Jawaban")


    # =========================
    # SUBMIT JAWABAN TRYOUT
    # =========================

    if submit:
        with st.spinner("Menghitung hasil..."):

            payload = {
                "user_answers": user_answers,
                "questions": st.session_state.tryout_questions,
                "kampus": st.session_state.selected_kampus
            }

            res = requests.post(
                f"{API_URL}/tryout/submit",
                json=payload
            )

            if res.status_code == 200:
                data = res.json()

                if data.get("status") == "success":
                    st.success(f"🎯 Skor kamu: {data['score']}%")

                    st.markdown("## Peluang Masuk Kampus")

                    for p in data["peluang"]:
                        st.write(f"🎓 {p['kampus']}")
                        st.progress(p["peluang"] / 100)
                        st.caption(f"{p['peluang']}% peluang masuk")

                    if st.button("🔄 Coba Lagi", key="reset_tryout"):
                        st.session_state.tryout_started = False
                        st.session_state.tryout_questions = []
                        st.session_state.selected_kampus = []
                        st.rerun()

                else:
                    st.error("Gagal menghitung hasil tryout.")

            else:
                st.error(f"Server Error: {res.text}")

    st.markdown("---")

    # =========================
    # FORM TES MINAT & BAKAT
    # =========================
    with st.container():
        st.subheader("🧠 Analisis Minat & Bakat")
        st.caption("Isi kuisioner berikut untuk mengetahui jurusan yang cocok untukmu.")

        with st.form(key=f"assessment_form_{user_id}"):
            col1, col2 = st.columns(2)

            with col1:
                minat = st.multiselect(
                    "Apa minat kamu?",
                    ["Teknologi", "Bisnis", "Seni", "Kesehatan", "Sosial", "Pendidikan"]
                )

                hobi = st.multiselect(
                    "Apa hobi kamu?",
                    ["Coding", "Membaca", "Menggambar", "Menulis", "Main Game", "Berorganisasi"]
                )

            with col2:
                pelajaran = st.multiselect(
                    "Pelajaran favorit?",
                    ["Matematika", "Informatika", "Bahasa", "Biologi", "Ekonomi", "Sejarah"]
                )

                deskripsi = st.text_area("Ceritakan tentang dirimu (opsional)")

            submit = st.form_submit_button("🔍 Analisis Sekarang")

        if submit:
            if not minat and not hobi and not pelajaran and not deskripsi:
                st.warning("Minimal isi salah satu.")
            else:
                with st.spinner("AI sedang menganalisis..."):
                    answers = minat + hobi + pelajaran + [deskripsi]

                    res = requests.post(
                        f"{API_URL}/assessment",
                        json={"answers": answers}
                    )

                    data = res.json()

                    if data.get("status") == "success":
                        st.success("Hasil Analisis")

                        for i, r in enumerate(data["data"], 1):
                            st.markdown(f"### {i}. {r['jurusan']}")
                            st.progress(r["persentase"] / 100)
                            st.write(f"**Persentase cocok:** {r['persentase']}%")
                            st.write(f"**Alasan:** {r['alasan']}")
                            st.write(f"**Prospek:** {', '.join(r['prospek'])}")
                            st.write(f"**Tips:** {r['tips']}")
                            st.markdown("---")

    st.markdown("---")

    # =========================
    # RIWAYAT ASSESSMENT
    # =========================
    with st.container():
        st.subheader("📊 Riwayat Assessment")

        if st.button("🔄 Refresh Riwayat", key="refresh_riwayat"):
            st.rerun()

        riwayat = load_riwayat_assessment(user_id)

        if not riwayat:
            st.info("Belum ada riwayat assessment.")
        else:
            for item in riwayat:
                with st.expander(f"📄 Assessment #{item['id']}"):
                    st.write("**Jawaban User:**")
                    for a in item["answers"]:
                        st.write(f"- {a}")

                    st.write("**Hasil AI:**")
                    for r in item["result"]:
                        st.write(f"**{r['jurusan']}** ({r['persentase']}%)")
                        st.progress(r["persentase"] / 100)

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f'<div class="stat-card">📑<br><b>{len(st.session_state.chat_history)}</b><br>Total Chat</div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="stat-card">🔥<br><b>Aktif</b><br>Status</div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="stat-card">💬<br><b>{len(messages)}</b><br>Pesan</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- AREA CHAT ---
chat_container = st.container()
with chat_container:
    st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)
    for msg in messages:
        div_class    = "chat-user" if msg["role"] == "user" else "chat-ai"
        bubble_class = "user-bubble" if msg["role"] == "user" else "ai-bubble"
        st.markdown(f'''
            <div class="chat-row {div_class}">
                <div class="bubble {bubble_class}">{msg["content"]}</div>
            </div>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.is_loading:
    st.markdown("🤖 *AI sedang menganalisis...*")

# --- INPUT & KIRIM KE BACKEND ---
user_input = st.chat_input("Ceritakan minat dan hobimu di sini...")

if user_input and not st.session_state.is_loading:
    messages.append({"role": "user", "content": user_input})
    st.session_state.chat_history[st.session_state.current_chat] = messages
    st.session_state.is_loading = True
    st.rerun()

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
        requests.post(
            f"{API_URL}/chat/simpan",
            json={
                "user_id"   : user_id,
                "pesan_user": messages[-2]["content"],
                "respons_ai": response
            }
        )
    except Exception:
        pass

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