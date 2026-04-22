# frontend/Login.py

import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/api"

# --- 1. SESSION STATE ---
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"
if "user" not in st.session_state:
    st.session_state.user = None
if "register_success" not in st.session_state:
    st.session_state.register_success = False

def switch_to_register():
    st.session_state.auth_mode = "register"
    st.session_state.register_success = False

def switch_to_login():
    st.session_state.auth_mode = "login"
    st.session_state.register_success = False

# --- 2. STYLE CSS ---
st.markdown("""
    <style>
    [data-testid="stForm"] {
        background-color: white;
        padding: 20px 30px;
        border-radius: 15px;
        box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.1);
        border: none;
    }
    [data-testid="stForm"] label,
    [data-testid="stForm"] h2,
    [data-testid="stForm"] p {
        color: #1f2937 !important;
    }
    [data-testid="stForm"] .stTextInput input {
        background-color: #f3f4f6 !important;
        color: #1f2937 !important;
        border: 1px solid #d1d5db !important;
        height: 40px;
    }
    div.stFormSubmitButton > button {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%) !important;
        color: white !important;
        width: 100%;
        height: 45px;
        border-radius: 8px;
        font-weight: bold;
        border: none !important;
        text-transform: uppercase;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. HALAMAN LOGIN ---
if st.session_state.auth_mode == "login":

    # Tampilkan notif sukses register kalau baru daftar
    if st.session_state.register_success:
        st.success("Pendaftaran berhasil! Silakan login.")

    with st.form("login_form"):
        st.markdown("<h2 style='margin-bottom: 0;'>Login AI</h2>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 13px; margin-top: 0;'>Masuk ke akun AI School Future</p>", unsafe_allow_html=True)

        email = st.text_input("Email", placeholder="example@mail.com")
        pwd   = st.text_input("Password", type="password", placeholder="******")

        submit = st.form_submit_button("Log In")

    # Proses login setelah form disubmit
    if submit:
        if not email or not pwd:
            st.error("Email dan password tidak boleh kosong!")
        else:
            try:
                res  = requests.post(
                    f"{API_URL}/login",
                    json={"email": email, "password": pwd}
                )
                data = res.json()

                if data["status"] == "success":
                    # Simpan data user ke session
                    st.session_state.user = data["data"]
                    st.success(data["message"])
                    st.switch_page("pages/Dashboard.py")
                else:
                    st.error(data["message"])

            except Exception:
                st.error("Tidak dapat terhubung ke server. Pastikan backend sudah berjalan.")

    # Tombol ke halaman daftar
    st.markdown("<p style='text-align: center; font-size: 13px; margin-top: 16px;'>Belum punya akun?</p>", unsafe_allow_html=True)
    if st.button("Ayo Daftar Sekarang", use_container_width=True):
        switch_to_register()
        st.rerun()

# --- 4. HALAMAN DAFTAR ---
else:
    with st.form("register_form"):
        st.markdown("<h2 style='margin-bottom: 0;'>Daftar Akun</h2>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 13px; margin-top: 0;'>Lengkapi data diri kamu</p>", unsafe_allow_html=True)

        nama      = st.text_input("Nama Lengkap", placeholder="Budi Santoso")
        email_reg = st.text_input("Email", placeholder="example@mail.com")
        pwd_reg   = st.text_input("Buat Password", type="password", placeholder="Min. 6 karakter")

        submit_reg = st.form_submit_button("Buat Akun")

    # Proses register setelah form disubmit
    if submit_reg:
        if not nama or not email_reg or not pwd_reg:
            st.error("Semua kolom wajib diisi!")
        elif len(pwd_reg) < 6:
            st.error("Password minimal 6 karakter!")
        else:
            try:
                res  = requests.post(
                    f"{API_URL}/register",
                    json={
                        "nama_lengkap": nama,
                        "email": email_reg,
                        "password": pwd_reg
                    }
                )
                data = res.json()

                if data["status"] == "success":
                    # Tandai register berhasil lalu kembali ke login
                    st.session_state.register_success = True
                    switch_to_login()
                    st.rerun()
                else:
                    # Email sudah terdaftar atau error lain
                    st.error(data["message"])

            except Exception:
                st.error("Tidak dapat terhubung ke server. Pastikan backend sudah berjalan.")

    if st.button("Sudah punya akun? Kembali ke Login", use_container_width=True):
        switch_to_login()
        st.rerun()