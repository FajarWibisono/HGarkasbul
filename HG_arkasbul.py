import streamlit as st
import pandas as pd
import json
from datetime import datetime
import re
import os

# Konfigurasi halaman
st.set_page_config(page_title="SSC Worksheet", layout="wide")

# File untuk menyimpan data
DATA_FILE = "ssc_data.json"

# Fungsi untuk memuat data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# Fungsi untuk menyimpan data
def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Fungsi validasi email
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Fungsi untuk export ke Excel
def export_to_excel(data):
    if not data:
        return None
    
    rows = []
    for entry in data:
        base_row = {
            'Nama': entry['nama'],
            'Tanggal Pengisian': entry['tanggal'],
            'Email': entry['email']
        }
        
        # STOP
        for i in range(3):
            row = base_row.copy()
            row['Kategori'] = 'STOP'
            row['No'] = i + 1
            row['Aktivitas/Perilaku'] = entry['stop'][i]['aktivitas']
            row['Parameter/Waktu'] = entry['stop'][i]['parameter']
            rows.append(row)
        
        # START
        for i in range(3):
            row = base_row.copy()
            row['Kategori'] = 'START'
            row['No'] = i + 1
            row['Aktivitas/Perilaku'] = entry['start'][i]['aktivitas']
            row['Parameter/Waktu'] = entry['start'][i]['parameter']
            rows.append(row)
        
        # CONTINUE
        for i in range(3):
            row = base_row.copy()
            row['Kategori'] = 'CONTINUE'
            row['No'] = i + 1
            row['Aktivitas/Perilaku'] = entry['continue'][i]['aktivitas']
            row['Parameter/Waktu'] = entry['continue'][i]['parameter']
            rows.append(row)
    
    df = pd.DataFrame(rows)
    df = df[['Nama', 'Tanggal Pengisian', 'Email', 'Kategori', 'No', 'Aktivitas/Perilaku', 'Parameter/Waktu']]
    return df

# Sidebar untuk mode admin
st.sidebar.title("🔐 Mode Admin")
admin_password = st.sidebar.text_input("Password Admin", type="password")
is_admin = admin_password == "admin123"

if is_admin:
    st.sidebar.success("✅ Login Admin Berhasil")
    st.sidebar.markdown("---")

# Main App
st.title("📋 STOP, START, CONTINUE Worksheet")
st.markdown("**www.humanisgroup.co.id**")
st.markdown("---")

# Mode Admin
if is_admin:
    st.sidebar.subheader("📊 Admin Panel")
    
    data = load_data()
    st.sidebar.metric("Total Submissions", len(data))
    
    if st.sidebar.button("🗑️ Delete All Data", type="secondary"):
        if st.sidebar.checkbox("Konfirmasi hapus semua data"):
            save_data([])
            st.sidebar.success("Semua data telah dihapus!")
            st.rerun()
    
    if st.sidebar.button("📥 Export to Excel"):
        df = export_to_excel(data)
        if df is not None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"SSC_Data_{timestamp}.xlsx"
            df.to_excel(filename, index=False)
            
            with open(filename, "rb") as file:
                st.sidebar.download_button(
                    label="⬇️ Download Excel",
                    data=file,
                    file_name=filename,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        else:
            st.sidebar.warning("Tidak ada data untuk di-export")
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("📋 Data Submissions")
    
    if data:
        for idx, entry in enumerate(data):
            with st.sidebar.expander(f"{entry['nama']} - {entry['tanggal']}"):
                st.write(f"**Email:** {entry['email']}")
                if st.button(f"🗑️ Hapus", key=f"del_{idx}"):
                    data.pop(idx)
                    save_data(data)
                    st.rerun()

# Petunjuk Pengisian
st.header("📖 PETUNJUK PENGISIAN")
st.info("""
**STOP-START-CONTINUE** adalah metode yang digunakan untuk mengevaluasi dan mengubah perilaku. Prinsipnya adalah untuk berhenti melakukan perilaku yang tidak diinginkan (STOP), memulai perilaku baru yang diinginkan (START), dan melanjutkan perilaku yang sudah pernah dilakukan namun belum konsisten atau belum menjadi bagian dari kebiasaan diri (CONTINUE).

**Langkah-langkah dalam metode ini adalah:**
1. Identifikasi perilaku yang ingin diubah.
2. Pertimbangkan apa yang akan dilakukan untuk menghentikan (STOP) perilaku tersebut.
3. Pertimbangkan apa yang akan dilakukan untuk memulai (START) perilaku yang diinginkan.
4. Pertimbangkan apa yang akan dilakukan untuk melanjutkan (CONTINUE) perilaku yang sudah dilakukan dengan baik.
5. Pilihlah hal atau aktivitas yang **Relevan, Realistik, Recognizable, dan Real Time** (dapat segera dilakukan)
6. Tuliskanlah dalam kalimat yang **operasional, jangan normatif**.
7. Implementasikan rencana perubahan perilaku dan evaluasi hasilnya.
""")

# Tips dan Trick
st.header("💡 TIPS DAN TRICK")
st.success("""
**7 tips dan trik untuk menuliskan aktivitas atau perilaku dalam metode STOP-START-CONTINUE:**

1. **Fokus pada satu atau dua perubahan perilaku saja.**

2. **Jelas dan spesifik** dalam menentukan perilaku yang akan diubah. Misalnya, bukan hanya menyatakan "ingin makan lebih sehat", tapi juga menentukan jenis makanan yang akan ditinggalkan dan jenis makanan yang akan dikonsumsi.

3. **Buat rencana tindakan yang realistis dan dapat dilakukan.** Misalnya, jangan menetapkan tujuan untuk berolahraga selama 2 jam setiap hari jika Anda tahu itu tidak mungkin dilakukan.

4. **Tentukan dukungan yang dibutuhkan** untuk mencapai tujuan. Misalnya, jika ingin berolahraga lebih sering, pastikan untuk membuat jadwal yang dapat diikuti dan temukan teman yang akan berolahraga bersama.

5. **Catat dan evaluasi perubahan yang dilakukan.** Ini akan membantu Anda untuk melihat perkembangan dan mengevaluasi apakah rencana tindakan yang Anda buat efektif atau perlu diubah.

6. **Jangan ragu untuk mengubah rencana jika diperlukan.** Jika sesuatu tidak bekerja seperti yang diharapkan, cobalah untuk menemukan solusi yang berbeda.

7. **Ingat untuk menghormati dan melanjutkan perilaku yang sudah dilakukan dengan baik.** Hal ini akan memberikan dorongan positif dan membantu Anda untuk tetap fokus pada perubahan yang ingin dicapai.
""")

st.markdown("---")

# Form Input
st.header("📝 FORMULIR PENGISIAN")

with st.form("ssc_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        nama = st.text_input("Nama *", placeholder="Masukkan nama lengkap Anda")
    
    with col2:
        tanggal = st.date_input("Tanggal Pengisian *", value=datetime.now())
    
    email = st.text_input("Email *", placeholder="contoh@email.com")
    
    st.markdown("---")
    
    # STOP Section
    st.subheader("🛑 STOP - Perilaku yang Ingin Dihentikan")
    st.caption("Maksimal 3 inisiatif")
    
    stop_data = []
    for i in range(3):
        st.markdown(f"**Inisiatif STOP #{i+1}**")
        col1, col2 = st.columns([2, 1])
        with col1:
            stop_aktivitas = st.text_area(
                f"Aktivitas/Perilaku",
                key=f"stop_aktivitas_{i}",
                placeholder="Tuliskan aktivitas/perilaku yang ingin dihentikan",
                height=80
            )
        with col2:
            stop_parameter = st.text_area(
                f"Parameter/Waktu",
                key=f"stop_parameter_{i}",
                placeholder="Kapan/berapa lama",
                height=80
            )
        stop_data.append({"aktivitas": stop_aktivitas, "parameter": stop_parameter})
    
    st.markdown("---")
    
    # START Section
    st.subheader("▶️ START - Perilaku Baru yang Ingin Dimulai")
    st.caption("Maksimal 3 inisiatif")
    
    start_data = []
    for i in range(3):
        st.markdown(f"**Inisiatif START #{i+1}**")
        col1, col2 = st.columns([2, 1])
        with col1:
            start_aktivitas = st.text_area(
                f"Aktivitas/Perilaku",
                key=f"start_aktivitas_{i}",
                placeholder="Tuliskan aktivitas/perilaku baru yang ingin dimulai",
                height=80
            )
        with col2:
            start_parameter = st.text_area(
                f"Parameter/Waktu",
                key=f"start_parameter_{i}",
                placeholder="Kapan/berapa lama",
                height=80
            )
        start_data.append({"aktivitas": start_aktivitas, "parameter": start_parameter})
    
    st.markdown("---")
    
    # CONTINUE Section
    st.subheader("✅ CONTINUE - Perilaku yang Ingin Dilanjutkan")
    st.caption("Maksimal 3 inisiatif")
    
    continue_data = []
    for i in range(3):
        st.markdown(f"**Inisiatif CONTINUE #{i+1}**")
        col1, col2 = st.columns([2, 1])
        with col1:
            continue_aktivitas = st.text_area(
                f"Aktivitas/Perilaku",
                key=f"continue_aktivitas_{i}",
                placeholder="Tuliskan aktivitas/perilaku yang ingin dilanjutkan",
                height=80
            )
        with col2:
            continue_parameter = st.text_area(
                f"Parameter/Waktu",
                key=f"continue_parameter_{i}",
                placeholder="Kapan/berapa lama",
                height=80
            )
        continue_data.append({"aktivitas": continue_aktivitas, "parameter": continue_parameter})
    
    st.markdown("---")
    
    submitted = st.form_submit_button("✅ Submit", type="primary", use_container_width=True)
    
    if submitted:
        # Validasi
        if not nama:
            st.error("❌ Nama harus diisi!")
        elif not email:
            st.error("❌ Email harus diisi!")
        elif not validate_email(email):
            st.error("❌ Format email tidak valid!")
        else:
            # Simpan data
            new_entry = {
                "nama": nama,
                "tanggal": tanggal.strftime("%Y-%m-%d"),
                "email": email,
                "stop": stop_data,
                "start": start_data,
                "continue": continue_data,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            data = load_data()
            data.append(new_entry)
            save_data(data)
            
            st.success("✅ Data berhasil disimpan!")
            st.balloons()
            
            # Reset form dengan rerun
            st.info("Refresh halaman untuk mengisi form baru.")

# Footer
st.markdown("---")
st.markdown("*Powered by Humanis Group | www.humanisgroup.co.id*")