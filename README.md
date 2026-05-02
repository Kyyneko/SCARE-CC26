<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white" alt="TensorFlow">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Plotly-239120?style=for-the-badge&logo=plotly&logoColor=white" alt="Plotly">
  <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV">
  
  <br><br>
  <h1>SCARE: Scar Classification and Recognition Engine</h1>
  <p><b>Advanced Deep Learning System for Clinical Dermatological Scar Triage</b></p>
</div>

---

## 🚀 Live Demo
Aplikasi prediksi SCARE telah di-deploy secara publik dan dapat diakses melalui:
👉 **[SCARE Dashboard - Live Web App](https://scare-cc26.streamlit.app)**

---

## 📖 Project Overview
**SCARE** adalah *Capstone Project* Data Science berstandar industri yang berfokus pada penyelesaian tantangan klinis dermatologi: **Membedakan Hypertrophic Scars dan Keloid Scars secara visual.** 

Secara klinis, kedua jenis bekas luka ini sangat mirip di fase awal perkembangannya. Kesalahan diagnosis dapat menyebabkan *treatment* yang salah (misalnya, operasi eksisi pada Keloid justru akan memperparah ukurannya). SCARE hadir sebagai *second-opinion tool* cerdas berbasis **Computer Vision** dan **Deep Learning** untuk membantu tenaga medis maupun pasien dalam melakukan identifikasi dini secara non-invasif dan seketika (*real-time*).

---

## 🛠️ Tech Stack & Architecture Justification

Pemilihan teknologi dalam proyek ini didasarkan pada prinsip *scalability*, performa komputasi, dan kecepatan *deployment*:

### 1. Core Machine Learning: `TensorFlow` & `Keras`
* **Mengapa:** TensorFlow menawarkan ekosistem paling matang untuk komputasi *Deep Learning*. Fitur `tf.data` dan integrasi *pre-trained weights* (Keras Applications) sangat vital untuk mengeksekusi arsitektur *Computer Vision* yang berat tanpa kendala *memory leak*.

### 2. Model Arsitektur: `MobileNetV2` (Transfer Learning)
* **Mengapa:** Dari 5 arsitektur yang diuji (CNN Scratch, VGG16, ResNet50, EfficientNetB0, MobileNetV2), **MobileNetV2** terpilih karena efisiensi parameternya (hanya ~3.4 Juta parameter). Arsitektur berbasis *Depthwise Separable Convolution* ini sangat ringan untuk dideploy pada *cloud server* gratis (RAM sangat terbatas), namun tetap mempertahankan akurasi klasifikasi yang setara dengan model raksasa.

### 3. Data Processing & Computer Vision: `OpenCV`, `NumPy`, `Pandas`
* **Mengapa OpenCV:** Kecepatannya dalam mengeksekusi operasi matriks *low-level* (I/O, resize, konversi BGR ke RGB) jauh lebih unggul dibandingkan PIL/Pillow saat memproses ratusan gambar sekaligus. Digunakan juga untuk menghitung *Variance of Laplacian* (deteksi blur).
* **Mengapa Pandas/NumPy:** Standar industri untuk *Data Wrangling*, manipulasi *dataframe* JSON metric hasil evaluasi, dan vektorisasi *array* matriks gambar.

### 4. Interactive Web Application: `Streamlit`
* **Mengapa:** Streamlit memungkinkan iterasi *Rapid Prototyping* dari script Python langsung menjadi *Web App* fungsional tanpa membuang waktu menulis HTML/JS/CSS kompleks. Memiliki mekanisme `@st.cache_resource` yang sangat efisien untuk menyimpan *graph* TensorFlow di dalam RAM tanpa harus memuat ulang model setiap kali *user* mengunggah gambar.

### 5. Advanced Visualizations: `Plotly`
* **Mengapa:** Berbeda dengan Matplotlib/Seaborn yang bersifat statis, Plotly menawarkan *interactive charts*. Pada data medis, interaktivitas (*hover tooltips*, *zoom*) memungkinkan pengguna untuk menginspeksi metrik statistik A/B Testing dengan jauh lebih detail dan mendalam secara langsung di web.

---

## 🔬 Metodologi Pipeline Data Science

Proyek ini tidak sekadar melatih model, melainkan mengikuti standar pipeline MLOps yang ketat:

1. **Data Wrangling & Cleaning:**
   * Melakukan pembersihan data kotor secara algoritmik menggunakan `cv2.Laplacian(img, cv2.CV_64F).var()` untuk mendeteksi dan membuang gambar yang memiliki level *blurriness* parah.
2. **Exploratory Data Analysis (EDA):**
   * Menganalisis *class imbalance* (rasio 1:2 antara Hypertrophic dan Keloid) dan mengekstraksi metrik *pixel brightness* serta resolusi data.
3. **Feature Engineering & Augmentation:**
   * Menerapkan Normalisasi skala `[-1, 1]` spesifik untuk ImageNet MobileNetV2.
   * Melakukan *agressive data augmentation* (`RandomRotation`, `RandomFlip`, `RandomZoom`) untuk memaksa model belajar mengenali fitur bentuk (*shape*), bukan orientasi.
   * Menggunakan algoritma **Class Weighting** otomatis (`sklearn.utils.class_weight`) untuk menghukum *(penalize)* model lebih berat jika salah menebak kelas minoritas, menetralisir bias data secara matematis.
4. **A/B Testing & Modeling:**
   * Mengevaluasi kandidat model menggunakan *stratified data split*. 

---

## 📊 Hasil A/B Testing & Performa

Berdasarkan hasil metrik pada set pengujian (*blind test data*), **MobileNetV2 (Frozen Base)** secara signifikan mengalahkan model *scratch* maupun kompetitor *pre-trained* lainnya:

| Metrik | Skor (MobileNetV2) | Interpretasi Klinis |
|---|---|---|
| **Accuracy** | `76.67%` | Akurasi klasifikasi umum dari total pasien uji. |
| **F1-Score** | `76.92%` | Keseimbangan harmonik presisi dan sensitivitas. Sangat baik mengingat ada *imbalance data*. |
| **Precision** | `77.35%` | Dari semua pasien yang ditebak Keloid oleh AI, 77.35% benar. Mencegah alarm palsu *(False Positives)*. |
| **Recall** | `76.67%` | AI berhasil mendeteksi 76.67% dari semua kasus aktual yang benar-benar ada. |

> **Business Impact:** Dengan skor ROC AUC `0.8533`, sistem ini sangat reliabel sebagai *screening agent* lapis pertama di puskesmas atau aplikasi *telemedicine* sebelum dokter spesialis turun tangan.

---

## 💻 Instalasi Lokal (Reproducing the Project)

Bagi Anda yang ingin menjalankan atau berkontribusi pada proyek ini secara lokal:

```bash
# 1. Clone Repositori (Branch data-scientist)
git clone -b data-scientist https://github.com/Kyyneko/SCARE-CC26.git
cd SCARE-CC26

# 2. Buat Virtual Environment (Sangat disarankan)
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# 3. Install Dependensi (Pastikan menggunakan Python 3.11 atau 3.12)
pip install -r requirements.txt

# 4. Jalankan Dashboard SCARE
streamlit run streamlit_app.py
```

---
<p align="center">
  <i>Proyek Capstone Data Science &mdash; Dikembangkan untuk Coding Camp 2026</i><br>
  <b>Oleh: [Kyyneko]</b>
</p>
