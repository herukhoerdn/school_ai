# app/utils/seed_jurusan.py

from app.config.database import SessionLocal
from app.models.jurusan import Jurusan

DATA_JURUSAN = [
    {
        "nama": "Teknik Informatika",
        "fakultas": "Fakultas Teknik",
        "jenjang": "S1",
        "deskripsi": "Mempelajari algoritma, pemrograman, dan pengembangan sistem komputer.",
        "kata_kunci": ["coding", "programming", "komputer", "teknologi", "game", "aplikasi", "software", "internet"],
        "prospek_karir": ["Software Engineer", "Data Scientist", "Mobile Developer", "DevOps Engineer"],
        "mapel_relevan": ["Matematika", "TIK", "Fisika"],
        "passing_grade": 650.0
    },
    {
        "nama": "Desain Komunikasi Visual",
        "fakultas": "Fakultas Seni dan Desain",
        "jenjang": "S1",
        "deskripsi": "Mempelajari desain grafis, ilustrasi, dan komunikasi visual.",
        "kata_kunci": ["desain", "gambar", "visual", "seni", "kreatif", "ilustrasi", "fotografi", "warna"],
        "prospek_karir": ["UI/UX Designer", "Graphic Designer", "Art Director", "Illustrator"],
        "mapel_relevan": ["Seni Budaya", "TIK", "Bahasa Indonesia"],
        "passing_grade": 580.0
    },
    {
        "nama": "Manajemen Bisnis",
        "fakultas": "Fakultas Ekonomi",
        "jenjang": "S1",
        "deskripsi": "Mempelajari pengelolaan bisnis, strategi, dan kewirausahaan.",
        "kata_kunci": ["bisnis", "jualan", "dagang", "wirausaha", "uang", "marketing", "organisasi", "pemimpin"],
        "prospek_karir": ["Business Analyst", "Marketing Manager", "Entrepreneur", "Konsultan Bisnis"],
        "mapel_relevan": ["Ekonomi", "Matematika", "Bahasa Indonesia"],
        "passing_grade": 570.0
    },
    {
        "nama": "Ilmu Komunikasi",
        "fakultas": "Fakultas Ilmu Sosial",
        "jenjang": "S1",
        "deskripsi": "Mempelajari media, jurnalistik, hubungan masyarakat, dan komunikasi massa.",
        "kata_kunci": ["media", "sosial", "konten", "nulis", "ngomong", "presenter", "jurnalis", "youtuber", "podcast"],
        "prospek_karir": ["Jurnalis", "Content Creator", "Public Relations", "Broadcaster"],
        "mapel_relevan": ["Bahasa Indonesia", "Bahasa Inggris", "Sosiologi"],
        "passing_grade": 560.0
    },
    {
        "nama": "Psikologi",
        "fakultas": "Fakultas Psikologi",
        "jenjang": "S1",
        "deskripsi": "Mempelajari perilaku manusia, kesehatan mental, dan konseling.",
        "kata_kunci": ["bantu orang", "empati", "konseling", "mental", "perilaku", "sosial", "curhat", "pendengar"],
        "prospek_karir": ["Psikolog", "HRD", "Konselor", "Researcher"],
        "mapel_relevan": ["Biologi", "Sosiologi", "Bahasa Indonesia"],
        "passing_grade": 600.0
    },
    {
        "nama": "Teknik Elektro",
        "fakultas": "Fakultas Teknik",
        "jenjang": "S1",
        "deskripsi": "Mempelajari sistem kelistrikan, elektronika, dan otomasi.",
        "kata_kunci": ["listrik", "elektronik", "robot", "rangkaian", "teknik", "mesin", "hardware", "arduino"],
        "prospek_karir": ["Electrical Engineer", "Robotics Engineer", "PLC Programmer", "IoT Developer"],
        "mapel_relevan": ["Fisika", "Matematika", "TIK"],
        "passing_grade": 630.0
    },
    {
        "nama": "Kedokteran",
        "fakultas": "Fakultas Kedokteran",
        "jenjang": "S1",
        "deskripsi": "Mempelajari ilmu kesehatan, anatomi, dan pengobatan.",
        "kata_kunci": ["kesehatan", "dokter", "medis", "biologi", "bantu orang", "rumah sakit", "sains"],
        "prospek_karir": ["Dokter Umum", "Dokter Spesialis", "Peneliti Medis"],
        "mapel_relevan": ["Biologi", "Kimia", "Fisika"],
        "passing_grade": 750.0
    },
    {
        "nama": "Olahraga / Ilmu Keolahragaan",
        "fakultas": "Fakultas Ilmu Keolahragaan",
        "jenjang": "S1",
        "deskripsi": "Mempelajari ilmu olahraga, pelatihan fisik, dan kesehatan jasmani.",
        "kata_kunci": ["olahraga", "atletik", "sepak bola", "basket", "renang", "gym", "fisik", "aktif"],
        "prospek_karir": ["Pelatih Olahraga", "Atlet Profesional", "Fisioterapis", "Sports Analyst"],
        "mapel_relevan": ["PJOK", "Biologi", "IPA"],
        "passing_grade": 520.0
    },
]


def seed():
    db = SessionLocal()
    try:
        # Cek apakah data sudah ada
        existing = db.query(Jurusan).count()
        if existing > 0:
            print(f"[SEED] Data jurusan sudah ada ({existing} jurusan). Skip.")
            return

        for data in DATA_JURUSAN:
            jurusan = Jurusan(**data)
            db.add(jurusan)

        db.commit()
        print(f"[SEED] Berhasil menambahkan {len(DATA_JURUSAN)} jurusan ke database.")
    except Exception as e:
        db.rollback()
        print(f"[SEED] Gagal: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed()