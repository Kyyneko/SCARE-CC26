# Data Dictionary — SCARE (Scar Classification and Recognition Engine)

## Dataset Overview
| Field | Value |
|---|---|
| **Nama Proyek** | SCARE (Scar Classification and Recognition Engine) |
| **Tipe Dataset** | Image Classification (Binary) |
| **Domain** | Dermatologi / Medis |
| **Sumber** | Dataset publik gambar dermatologi |
| **Ukuran Total** | 607 gambar (mentah), 596 gambar (bersih) |

## Kelas

| Label | Nama Kelas | Deskripsi | Jumlah (Mentah) | Jumlah (Bersih) |
|---|---|---|---|---|
| 0 | **Hypertrophic Scars** | Bekas luka hipertrofik — tumbuh dalam batas luka asli, cenderung membaik seiring waktu | 207 | 201 |
| 1 | **Keloid Scars** | Bekas luka keloid — tumbuh melampaui batas luka asli, tidak membaik sendiri | 400 | 395 |

## Preprocessing

| Tahap | Detail |
|---|---|
| **Deteksi Blur** | Laplacian variance threshold = 10.0 |
| **Resize** | 224×224 piksel dengan padding (tanpa distorsi) |
| **Normalisasi** | Piksel di-scale ke range `[-1, 1]` menggunakan `preprocess_input` bawaan MobileNetV2 |
| **Augmentasi** | Rotation ±15°, flip Horizontal/Vertikal, zoom ±10%, brightness ±10% |

## Split Data

| Set | Proporsi | Stratified |
|---|---|---|
| Training | 70% | Ya |
| Validation | 15% | Ya |
| Test | 15% | Ya |

## Fitur Input

| Fitur | Tipe | Shape | Range | Deskripsi |
|---|---|---|---|---|
| **Image** | float32 | (224, 224, 3) | `[-1, 1]` | Gambar RGB yang dinormalisasi untuk MobileNetV2 |
| **file_size** | float | - | > 0 | Ukuran file gambar dalam Kilobytes (KB) |
| **sharpness** | float | - | > 0 | Tingkat ketajaman gambar (*Variance of Laplacian*) |
| **brightness**| float | - | [0, 255] | Rata-rata intensitas piksel gambar (*Grayscale*) |

## Target Output

| Field | Tipe | Values | Deskripsi |
|---|---|---|---|
| **label** | int | 0 atau 1 | 0=Hypertrophic, 1=Keloid |
| **probability** | float | [0, 1] | Probabilitas kelas Keloid |

## Penanganan Imbalance

| Metode | Detail |
|---|---|
| **Class Weights** | Dihitung otomatis dengan `sklearn.utils.class_weight.compute_class_weight('balanced')` |
| **Data Augmentation** | Diterapkan hanya pada data training |
