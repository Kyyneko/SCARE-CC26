<div align="center">
  <img src="https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black" alt="React">
  <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind">
  <img src="https://img.shields.io/badge/Framer_Motion-0055FF?style=for-the-badge&logo=framer&logoColor=white" alt="Framer Motion">
  <img src="https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white" alt="Vite">
  <img src="https://img.shields.io/badge/React_Router-CA4245?style=for-the-badge&logo=react-router&logoColor=white" alt="React Router">
  
  <br><br>
  <h1>SCARE: Front-End UI Architecture</h1>
  <p><b>Interactive Clinical Interface for Advanced Scar Classification Engine</b></p>
</div>

---

## 📖 Project Overview
**SCARE Front-End** adalah antarmuka pengguna berbasis web yang dirancang untuk menjadi jembatan antara teknologi *Deep Learning* dan tenaga medis. Fokus utama dari *repository* ini adalah memberikan pengalaman pengguna (UX) yang intuitif, cepat, dan reliabel dalam melakukan triage dermatologi.

Antarmuka ini memungkinkan pengguna untuk mengambil foto luka secara langsung via kamera perangkat atau mengunggah file, melakukan penyesuaian area pindaian (*cropping*), hingga mendapatkan protokol pengobatan medis yang divalidasi oleh sistem pakar berbasis AI.

---

## 🛠️ Tech Stack & UI Justification

Pemilihan teknologi difokuskan pada performa *client-side*, kemudahan integrasi API, dan estetika medis yang modern:

### 1. Framework: `React.js` (Vite)
* **Mengapa:** Menggunakan arsitektur berbasis komponen untuk memastikan skalabilitas kode. **Vite** dipilih sebagai *build tool* karena kecepatan *Hot Module Replacement* (HMR) yang jauh lebih unggul dibanding CRA, mempercepat siklus pengembangan.

### 2. Styling: `Tailwind CSS`
* **Mengapa:** Memungkinkan kustomisasi UI yang sangat presisi dengan sistem *utility-first*. Hal ini sangat krusial untuk membangun desain responsif yang konsisten di berbagai ukuran layar perangkat medis (tablet, ponsel, hingga desktop).

### 3. Motion & Interaction: `Framer Motion`
* **Mengapa:** Memberikan sentuhan *premium feel* melalui animasi *staggered fade-up* dan transisi antar *state* yang mulus. Animasi ini bukan sekadar estetika, melainkan berfungsi sebagai *visual cue* untuk memandu alur kerja pengguna (UX).

### 4. Image Processing: `React Easy Crop`
* **Mengapa:** Memberikan kontrol penuh kepada pengguna untuk menentukan area pindaian secara presisi (1:1 aspect ratio). Hal ini krusial agar model AI mendapatkan input data gambar yang fokus pada area luka, meminimalisir *noise* latar belakang.

---

## 🏗️ Folder Structure & Architecture

Proyek ini menggunakan struktur modular yang terorganisir di dalam direktori `front-end/` untuk memudahkan kolaborasi:

```text
front-end/
├── public/               # Aset publik statis
└── src/
    ├── assets/           # Aset visual dan logo SCARE
    ├── components/       # Komponen atomik dan molekular
    │   ├── layout/       # Footer.jsx, Navbar.jsx
    │   └── ui/           # ScarCard.jsx, ChecklistItem.jsx, ScrollToTop.jsx
    ├── hooks/            # Custom React Hooks
    ├── layouts/          # MainLayout.jsx (Pembungkus utama)
    ├── pages/            # Halaman utama aplikasi:
    │   ├── Analysis/     # Modul kamera dan pemrosesan gambar
    │   ├── Home/         # Beranda edukasi
    │   ├── NotFound/     # Penanganan halaman tidak ditemukan
    │   ├── ServerError/  # Fallback kegagalan sistem
    │   └── Treatment/    # Hasil diagnosis dan protokol medis
    ├── services/         # Integrasi API dan logika eksternal
    └── App.jsx           # Sentralisasi rute aplikasi

---

## 🔬 Key UX Features

1.  **Smart Camera Interface**: Integrasi kamera *environment-facing* dengan penanganan izin akses yang aman.
2.  **State-Driven Transitions**: Penggunaan `AnimatePresence` untuk transisi mulus antara tahap *Upload* -> *Crop* -> *Processing* -> *Result*.
3.  **Medical-Grade Visualization**: Tagging otomatis (Aggressive vs Stabilized growth) berdasarkan hasil klasifikasi untuk membantu keputusan klinis.
4.  **Error Boundary & Fallback**: Sistem proteksi yang mencegah aplikasi *crash* jika pengguna mencoba mengakses halaman hasil tanpa data analisis.

---

## 💻 Instalasi Lokal (Running the Project)

Untuk menjalankan *Front-End* SCARE di lingkungan pengembangan Anda:

```bash
# 1. Clone Repositori (Branch full-stack)
git clone -b full-stack [https://github.com/Kyyneko/SCARE-CC26.git](https://github.com/Kyyneko/SCARE-CC26.git)
cd SCARE-CC26

# 2. Install Dependensi (Pastikan Node.js sudah terinstal)
npm install

# 3. Jalankan Aplikasi dalam Mode Development
npm run dev

# 4. Akses Aplikasi
# Buka http://localhost:5173 di browser Anda