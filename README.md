# SCARE (Scar Classification and Recognition Engine)

**SCARE** adalah proyek *Capstone Data Science* yang berfokus pada pengembangan model *Deep Learning* untuk membedakan dua jenis bekas luka kulit klinis: **Hypertrophic Scars** dan **Keloid Scars**. Proyek ini bertujuan untuk membangun sistem cerdas yang dapat mengklasifikasikan jenis *scar* berdasarkan input visual dari kamera atau gambar.

---

## 🎯 Objektif Proyek
1. Mengatasi kesulitan membedakan Hypertrophic dan Keloid secara visual.
2. Melakukan evaluasi (A/B Testing) terhadap beberapa arsitektur *Deep Learning*.
3. Mengemas hasil dan *insight* terbaik ke dalam *Interactive Web Dashboard* berbasis Streamlit yang mudah digunakan.

## 📊 Dataset & Preprocessing
*   **Total Data Bersih:** 596 Gambar (setelah proses *cleaning* & deteksi *blur*).
*   **Imbalance Handling:** *Data Augmentation* agresif dan algoritma *Class Weights* untuk memprioritaskan kelas minoritas (Hypertrophic).
*   **Feature Engineering:** Model menggunakan normalisasi khusus `[-1, 1]` via fungsi `preprocess_input` dari MobileNetV2.

## 🧠 Evaluasi Model (A/B Testing)
Proyek ini membandingkan 5 arsitektur (termasuk transfer learning & pelatihan *from scratch*). Berdasarkan eksperimen, pemenangnya adalah:

**🥇 MobileNetV2 (Transfer Learning - Frozen Base)**
*   **Accuracy:** `76.67%`
*   **F1-Score:** `76.92%`
*   **Precision:** `77.35%`
*   **Recall:** `76.67%`
*   **AUC ROC:** `0.8533`

> Model MobileNetV2 secara statistik mengungguli arsitektur lain, menawarkan keseimbangan sempurna antara konvergensi *loss* yang stabil dan komputasi yang ringan.

## 🛠️ Tech Stack
*   **Bahasa Pemrograman:** Python 3.x
*   **Machine Learning Framework:** TensorFlow / Keras
*   **Data Analysis & Vision:** Pandas, NumPy, OpenCV, Pillow
*   **Visualisasi Data:** Plotly
*   **Web Dashboard:** Streamlit (dengan custom CSS Premium UI & Glassmorphism)

## 💻 Instalasi & Menjalankan Proyek Secara Lokal

1. **Clone repository ini** dan pastikan berada di branch `data-scientist`:
   ```bash
   git clone -b data-scientist https://github.com/Kyyneko/SCARE-CC26.git
   cd SCARE-CC26
   ```

2. **Install semua dependensi** (Disarankan menggunakan virtual environment `venv` atau `conda`):
   ```bash
   pip install -r requirements.txt
   ```

3. **Jalankan Dashboard Streamlit**:
   ```bash
   streamlit run streamlit_app.py
   ```

4. **Akses Dashboard** melalui browser di `http://localhost:8501`.

## 📁 Struktur Proyek Utama
```text
📦SCARE-CC26
 ┣ 📂dataset          # Raw dataset & scripts gathering
 ┣ 📂output
 ┃ ┣ 📂metrics        # Hasil evaluasi model (JSON)
 ┃ ┣ 📂models         # File model tersimpan (.keras)
 ┃ ┗ 📂plots          # Hasil export visualisasi EDA & evaluasi
 ┣ 📜capstone_full.ipynb  # Notebook utama eksekusi End-to-End
 ┣ 📜data_dictionary.md   # Kamus fitur dataset
 ┣ 📜requirements.txt     # Library dependencies untuk deployment
 ┗ 📜streamlit_app.py     # Source code Web Dashboard
```

---
*Proyek ini dirancang sebagai submisi untuk Coding Camp 2026 - Data Scientist Path.*
