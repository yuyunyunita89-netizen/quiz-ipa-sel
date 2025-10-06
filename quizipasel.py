import streamlit as st
from dataclasses import dataclass
from typing import List
import difflib

# ---------- Data Model ----------
@dataclass
class LKPEntry:
    no: int
    soal: str
    jawaban: str
    analisis: str

def sample_lkp_entries() -> List[LKPEntry]:
    return [
        LKPEntry(
            no=1,
            soal="Sebutkan fungsi inti sel!",
            jawaban="Mengatur aktivitas sel dan menyimpan DNA.",
            analisis="Mudah: mengingat inti sel. Sulit: membedakan DNA dengan inti."
        ),
        LKPEntry(
            no=2,
            soal="Apa fungsi mitokondria?",
            jawaban="Menghasilkan energi (ATP) dari respirasi seluler.",
            analisis="Mudah: mengingat julukan power house. Sulit: menjelaskan proses kimia."
        ),
        LKPEntry(
            no=3,
            soal="Apa perbedaan utama sel hewan dan sel tumbuhan?",
            jawaban="Sel tumbuhan memiliki dinding sel dan kloroplas; sel hewan tidak.",
            analisis="Mudah: menyebut organel khas. Sulit: menjelaskan fungsi kloroplas."
        )
    ]

def is_similar(user_answer: str, correct_answer: str, threshold=0.6) -> bool:
    ratio = difflib.SequenceMatcher(None, user_answer.lower(), correct_answer.lower()).ratio()
    return ratio > threshold

# ---------- UI Streamlit ----------
st.set_page_config(page_title="Kuis IPA: Sel", layout="centered")
st.title("🔬 Kuis IPA - Sel-sel Tubuh Manusia")

tab1, tab2 = st.tabs(["📝 Kuis Interaktif", "📄 Lembar Kerja (LKP)"])

entries = sample_lkp_entries()

# --- Tab Kuis Interaktif ---
with tab1:
    st.subheader("Jawab pertanyaan berikut:")
    score = 0
    jawaban_user = {}
    
    with st.form("kuis_form"):
        for e in entries:
            user_input = st.text_area(f"Soal {e.no}: {e.soal}", key=f"q_{e.no}")
            jawaban_user[e.no] = user_input
        submitted = st.form_submit_button("Kirim Jawaban")
    
    if submitted:
        st.subheader("📊 Hasil Kuis")
        for e in entries:
            user = jawaban_user[e.no]
            correct = is_similar(user, e.jawaban)
            if correct:
                st.success(f"Soal {e.no}: Jawaban Benar")
                score += 1
            else:
                st.error(f"Soal {e.no}: Jawaban Kurang Tepat")
            with st.expander("Lihat Kunci Jawaban"):
                st.markdown(f"**{e.jawaban}**")
        
        st.markdown("---")
        st.subheader("🎯 Skor Akhir")
        st.markdown(f"**Nilai: {score}/{len(entries)}** ({(score/len(entries))*100:.0f}%)")
        if score == len(entries):
            st.success("💯 Hebat! Semua jawaban benar.")
        elif score >= len(entries) // 2:
            st.info("👍 Bagus, tapi masih bisa ditingkatkan.")
        else:
            st.warning("📚 Masih perlu belajar lagi. Semangat!")

# --- Tab LKP ---
with tab2:
    st.subheader("📄 Lembar Kerja Praktik (LKP)")
    for e in entries:
        with st.expander(f"Soal {e.no}"):
            st.markdown(f"**Soal**: {e.soal}")
            st.markdown(f"**Jawaban**: {e.jawaban}")
            st.markdown(f"**Analisis**: {e.analisis}")
