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
**SCARE Front-End** adalah antarmuka pengguna berbasis web yang dirancang untuk menjadi jembatan antara teknologi *Deep Learning* dan tenaga medis. Fokus utama dari bagian ini adalah memberikan pengalaman pengguna (UX) yang intuitif, cepat, dan reliabel dalam melakukan rujukan (*triage*) dermatologi.

Antarmuka ini memungkinkan pengguna untuk mengambil foto luka secara langsung via kamera perangkat atau mengunggah file, melakukan penyesuaian area pindaian (*cropping*), hingga mendapatkan protokol pengobatan medis yang divalidasi oleh sistem pakar berbasis AI.

---

## 🛠️ Tech Stack & UI Justification

Pemilihan teknologi difokuskan pada performa *client-side*, kemudahan integrasi API, dan estetika medis yang modern:

### 1. Core Framework: `React.js`
* **Mengapa:** Sebagai inti dari aplikasi, arsitektur berbasis komponen React memungkinkan pembuatan antarmuka yang sangat dinamis dan interaktif tanpa memuat ulang halaman (*Single Page Application*). Dipadukan dengan **Vite** sebagai *build tool* untuk memastikan kecepatan *Hot Module Replacement* (HMR) dan optimasi *build* yang maksimal.

### 2. Styling: `Tailwind CSS`
* **Mengapa:** Memungkinkan kustomisasi UI yang sangat presisi dengan sistem *utility-first*. Hal ini sangat krusial untuk membangun desain responsif yang konsisten di berbagai ukuran layar perangkat medis (tablet, ponsel, hingga desktop).

### 3. Motion & Interaction: `Framer Motion`
* **Mengapa:** Memberikan sentuhan *premium feel* melalui animasi *staggered fade-up* dan transisi antar *state* yang mulus. Animasi ini bukan sekadar estetika, melainkan berfungsi sebagai *visual cue* untuk memandu alur kerja pengguna (UX).

### 4. Image Processing: `React Easy Crop`
* **Mengapa:** Memberikan kontrol penuh kepada pengguna untuk menentukan area pindaian secara presisi. Hal ini esensial agar model AI mendapatkan input data gambar yang fokus pada area luka, meminimalisir *noise* dari latar belakang.

---

## 🏗️ Folder Structure & Architecture

Proyek ini dipisahkan ke dalam direktori `front-end/` dengan arsitektur modular yang ketat untuk memudahkan pemeliharaan dan integrasi *Full-Stack*:

```text
front-end/
├── public/               # Aset publik statis (favicon, manifest)
└── src/
    ├── assets/           # Gambar klinis, logo SCARE, dan aset visual lainnya
    ├── components/       # Komponen React yang dapat digunakan ulang (Reusable)
    │   ├── layout/       # Komponen struktural (Navbar, Footer)
    │   └── ui/           # Komponen antarmuka mikro (ScarCard, ChecklistItem)
    ├── hooks/            # Custom React Hooks untuk abstraksi logika
    ├── layouts/          # Pembungkus halaman utama (MainLayout)
    ├── pages/            # Halaman utama aplikasi:
    │   ├── Analysis/     # Modul kamera, unggah foto, dan simulasi AI
    │   ├── Home/         # Beranda edukasi (Keloid vs Hypertrophic)
    │   ├── NotFound/     # Halaman 404
    │   ├── ServerError/  # Penanganan 500 (API Down Fallback)
    │   └── Treatment/    # Dasbor hasil diagnosis & protokol pengobatan
    └── services/         # Konfigurasi Axios/Fetch untuk komunikasi ke API Back-End