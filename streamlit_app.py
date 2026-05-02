"""
Streamlit Dashboard — Klasifikasi Hypertrophic vs Keloid Scars
"""

import streamlit as st
import json, os
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
from PIL import Image
import cv2

# -- Config --
st.set_page_config(page_title="SCARE Dashboard", page_icon="", layout="wide")

BASE_DIR = Path(r"d:\Coding Camp 2026\Data-scientist")
OUTPUT_DIR = BASE_DIR / "output"
PLOTS_DIR = OUTPUT_DIR / "plots"
METRICS_DIR = OUTPUT_DIR / "metrics"
MODELS_DIR = OUTPUT_DIR / "models"
CLEAN_DIR = BASE_DIR / "dataset" / "Dataset_Bersih"
CLASS_NAMES = ["Hypertrophic", "Keloid"]
IMG_SIZE = 224
VALID_EXT = (".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif")

def list_images(folder):
    if not folder.exists(): return []
    return [f for f in folder.iterdir() if f.is_file() and f.suffix.lower() in VALID_EXT]

def load_json(name):
    path = METRICS_DIR / name
    if path.exists():
        with open(str(path), encoding="utf-8") as f:
            return json.load(f)
    return None

# -- Custom CSS --
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

html, body, p, span, div, h1, h2, h3, h4, h5, h6, li, td, th, label, input, textarea, button {
    font-family: 'Inter', sans-serif;
}

/* Animated gradient title */
.main-title {
    font-size: 2.8rem;
    font-weight: 900;
    background: linear-gradient(135deg, #60a5fa, #a78bfa, #f472b6, #60a5fa);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradient-shift 4s ease infinite;
    margin-bottom: 0;
    letter-spacing: -1px;
}
@keyframes gradient-shift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.sub-title {
    font-size: 1.05rem;
    color: #94a3b8;
    margin-top: 6px;
    font-weight: 400;
    letter-spacing: 0.3px;
}

/* Glassmorphism stat cards */
.stat-card {
    background: rgba(30, 41, 59, 0.7);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(71, 85, 105, 0.5);
    border-radius: 16px;
    padding: 22px 16px;
    text-align: center;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}
.stat-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 16px 16px 0 0;
}
.stat-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
    border-color: rgba(148, 163, 184, 0.3);
}
.stat-card h2 {
    font-size: 2.2rem;
    font-weight: 900;
    color: #f1f5f9;
    margin: 0;
    letter-spacing: -0.5px;
}
.stat-card p {
    font-size: 0.78rem;
    color: #94a3b8;
    margin: 6px 0 0 0;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 600;
}

.card-hyper::before { background: linear-gradient(90deg, #ef4444, #f87171); }
.card-keloid::before { background: linear-gradient(90deg, #3b82f6, #60a5fa); }
.card-total::before { background: linear-gradient(90deg, #8b5cf6, #a78bfa); }
.card-best::before { background: linear-gradient(90deg, #10b981, #34d399); }

/* Section headers with accent */
.section-header {
    font-size: 1.25rem;
    font-weight: 700;
    color: #e2e8f0;
    margin: 36px 0 14px 0;
    padding-bottom: 10px;
    border-bottom: 2px solid transparent;
    border-image: linear-gradient(90deg, #3b82f6, #8b5cf6, transparent) 1;
}

/* Insight box with glow */
.insight-box {
    background: rgba(30, 58, 95, 0.6);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(59, 130, 246, 0.4);
    border-radius: 12px;
    padding: 18px 20px;
    font-size: 0.9rem;
    color: #bfdbfe;
    line-height: 1.7;
    box-shadow: 0 4px 20px rgba(59, 130, 246, 0.1);
}

/* Winner box with glow */
.winner-box {
    background: linear-gradient(135deg, rgba(6, 78, 59, 0.8), rgba(6, 95, 70, 0.8));
    backdrop-filter: blur(12px);
    border: 1px solid rgba(16, 185, 129, 0.5);
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    box-shadow: 0 8px 32px rgba(16, 185, 129, 0.15);
    transition: all 0.3s ease;
}
.winner-box:hover {
    box-shadow: 0 12px 48px rgba(16, 185, 129, 0.25);
    transform: translateY(-2px);
}
.winner-box h3 {
    color: #6ee7b7;
    margin: 0;
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-weight: 700;
}
.winner-box h1 {
    color: #34d399;
    margin: 8px 0;
    font-size: 2rem;
    font-weight: 900;
    letter-spacing: -0.5px;
}
.winner-box p {
    color: #a7f3d0 !important;
    font-size: 0.9rem;
}

/* Pipeline steps */
.pipeline-step {
    background: rgba(30, 41, 59, 0.5);
    border: 1px solid #334155;
    border-radius: 10px;
    padding: 12px 16px;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 12px;
    transition: all 0.2s ease;
}
.pipeline-step:hover {
    background: rgba(51, 65, 85, 0.7);
    border-color: #60a5fa;
    transform: translateX(4px);
}
.pipeline-num {
    background: linear-gradient(135deg, #3b82f6, #8b5cf6);
    color: #fff;
    width: 28px; height: 28px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 0.8rem;
    flex-shrink: 0;
}
.pipeline-text {
    color: #cbd5e1;
    font-size: 0.88rem;
    font-weight: 500;
}

/* Sidebar */
div[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
    border-right: 1px solid #1e293b;
}
div[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}

/* Smooth scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0f172a; }
::-webkit-scrollbar-thumb { background: #334155; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #475569; }
</style>
""", unsafe_allow_html=True)

# -- Sidebar --
st.sidebar.markdown("### SCARE")
st.sidebar.markdown("---")
page = st.sidebar.radio("", [
    "Overview", "Exploratory Data Analysis", "Model Performance",
    "A/B Testing", "Prediksi", "Insight & Kesimpulan"
], label_visibility="collapsed")

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="font-size:0.75rem; color:#94a3b8; line-height:1.6;">
<b>Capstone Project</b><br>
Scar Classification and Recognition Engine<br>
Deep Learning - TensorFlow
</div>
""", unsafe_allow_html=True)


# ============================
# PAGE: OVERVIEW
# ============================
if page == "Overview":
    st.markdown('<p class="main-title">SCARE</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Scar Classification and Recognition Engine — Deep Learning untuk Diagnosis Bekas Luka Kulit</p>', unsafe_allow_html=True)
    st.markdown("---")

    hyper_count = len(list_images(CLEAN_DIR / "hypertrophic scars" / "sukses_diproses"))
    keloid_count = len(list_images(CLEAN_DIR / "keloid scars" / "sukses_diproses"))
    best = load_json("best_model.json")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="stat-card card-total"><h2>{hyper_count + keloid_count}</h2><p>Total Gambar Bersih</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="stat-card card-hyper"><h2>{hyper_count}</h2><p>Hypertrophic Scars</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="stat-card card-keloid"><h2>{keloid_count}</h2><p>Keloid Scars</p></div>', unsafe_allow_html=True)
    with c4:
        acc = f"{best['accuracy']:.1%}" if best else "N/A"
        st.markdown(f'<div class="stat-card card-best"><h2>{acc}</h2><p>Best Model Accuracy</p></div>', unsafe_allow_html=True)

    st.markdown("")

    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown('<p class="section-header">Tentang Proyek</p>', unsafe_allow_html=True)
        st.markdown("""
        Hypertrophic scars dan keloid scars sering sulit dibedakan secara visual oleh tenaga medis.
        Proyek ini membangun model **deep learning** yang dapat mengklasifikasikan kedua jenis bekas
        luka dari gambar dermatologi.

        **Pendekatan:**
        - Membandingkan 3 arsitektur: CNN Scratch, MobileNetV2 (Frozen), MobileNetV2 (Fine-Tuned)
        - Data augmentation + class weights untuk mengatasi class imbalance
        - Transfer learning dari ImageNet pre-trained weights
        - Preprocessing khusus MobileNetV2 (normalisasi [-1, 1])
        """)

    with col2:
        st.markdown('<p class="section-header">Pipeline</p>', unsafe_allow_html=True)
        steps = [
            "Data Wrangling & Cleaning",
            "Exploratory Data Analysis",
            "Data Preparation & Augmentation",
            "Model Training (3 Arsitektur)",
            "Evaluasi & A/B Testing",
            "Dashboard & Deployment"
        ]
        for i, step in enumerate(steps, 1):
            st.markdown(f"""
            <div class="pipeline-step">
                <div class="pipeline-num">{i}</div>
                <div class="pipeline-text">{step}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<p class="section-header">Sampel Gambar Dataset</p>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.caption("**Hypertrophic Scars**")
        imgs = list_images(CLEAN_DIR / "hypertrophic scars" / "sukses_diproses")
        if imgs:
            cols = st.columns(4)
            for i, c in enumerate(cols):
                if i < len(imgs):
                    c.image(str(imgs[i]), use_container_width=True)
    with col2:
        st.caption("**Keloid Scars**")
        imgs = list_images(CLEAN_DIR / "keloid scars" / "sukses_diproses")
        if imgs:
            cols = st.columns(4)
            for i, c in enumerate(cols):
                if i < len(imgs):
                    c.image(str(imgs[i]), use_container_width=True)


# ============================
# PAGE: EDA
# ============================
elif page == "Exploratory Data Analysis":
    st.markdown('<p class="main-title">Exploratory Data Analysis</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Analisis mendalam terhadap distribusi dan karakteristik dataset</p>', unsafe_allow_html=True)
    st.markdown("---")

    hyper_c = len(list_images(CLEAN_DIR / "hypertrophic scars" / "sukses_diproses"))
    keloid_c = len(list_images(CLEAN_DIR / "keloid scars" / "sukses_diproses"))

    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure(data=[go.Bar(
            x=CLASS_NAMES, y=[hyper_c, keloid_c],
            marker_color=["#ef4444", "#3b82f6"],
            text=[hyper_c, keloid_c], textposition='outside',
            textfont=dict(size=16, color="#e2e8f0"),
            hovertemplate='%{x}: %{y} gambar<extra></extra>'
        )])
        fig.update_layout(
            title=dict(text="Distribusi Jumlah Gambar per Kelas", font=dict(size=16)),
            xaxis_title="Kelas", yaxis_title="Jumlah Gambar",
            yaxis=dict(range=[0, max(hyper_c, keloid_c) * 1.2], gridcolor="#334155"),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#e2e8f0", size=13), height=420,
            margin=dict(t=50, b=40)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption(f"**Gambar 1.** Distribusi jumlah gambar per kelas. Keloid ({keloid_c}) hampir 2x lipat Hypertrophic ({hyper_c}), menunjukkan class imbalance yang perlu ditangani.")

    with col2:
        fig = go.Figure(data=[go.Pie(
            labels=CLASS_NAMES, values=[hyper_c, keloid_c],
            hole=0.5, marker_colors=["#ef4444", "#3b82f6"],
            textinfo='label+percent', textfont_size=14,
            hovertemplate='%{label}: %{value} gambar (%{percent})<extra></extra>'
        )])
        fig.update_layout(
            title=dict(text="Proporsi Kelas dalam Dataset", font=dict(size=16)),
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)", font=dict(family="Inter", color="#e2e8f0", size=13),
            height=420, margin=dict(t=50, b=40),
            annotations=[dict(text=f'N={hyper_c+keloid_c}', x=0.5, y=0.5, font_size=16, font_color='#94a3b8', showarrow=False)]
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption(f"**Gambar 2.** Proporsi kelas dalam dataset. Hypertrophic hanya {hyper_c/(hyper_c+keloid_c)*100:.1f}% dari total dataset.")

    st.markdown('<p class="section-header">Analisis Detail</p>', unsafe_allow_html=True)

    fig_num = 3
    captions = {
        "eda_file_size_dist.png": "Distribusi ukuran file gambar per kelas. Keloid memiliki rata-rata ukuran file lebih besar (16.8 KB vs 13.8 KB), mengindikasikan kompleksitas tekstur yang lebih tinggi.",
        "eda_pixel_intensity.png": "Distribusi intensitas pixel RGB per kelas. Kedua kelas menunjukkan distribusi yang saling overlap, membuktikan bahwa klasifikasi manual berdasarkan warna saja tidak cukup."
    }
    for plot_name in ["eda_file_size_dist.png", "eda_pixel_intensity.png"]:
        path = PLOTS_DIR / plot_name
        if path.exists():
            st.image(str(path), use_container_width=True)
            st.caption(f"**Gambar {fig_num}.** {captions[plot_name]}")
            fig_num += 1

    ratio = keloid_c / max(hyper_c, 1)
    st.markdown(f"""
    <div class="insight-box">
    <b>Analisis Class Imbalance:</b><br>
    Rasio Hypertrophic : Keloid = 1 : {ratio:.2f}<br>
    Penanganan: Class weights (Hypertrophic diberi bobot lebih tinggi) + Data Augmentation pada training set.<br>
    Tanpa penanganan, model cenderung bias ke kelas mayoritas (Keloid).
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="section-header">Data Dictionary</p>', unsafe_allow_html=True)
    st.markdown("""
    | Fitur | Tipe Data | Deskripsi |
    |---|---|---|
    | `image` | `numpy.ndarray` | Matriks gambar RGB yang telah di-resize menjadi 224x224 pixels. Rentang nilai pixel disesuaikan melalui *preprocessing*. |
    | `label` | `int` | Target variabel (0 = Hypertrophic Scars, 1 = Keloid Scars). |
    | `file_size` | `float` | Ukuran file gambar dalam Kilobytes (KB). |
    | `sharpness` | `float` | Tingkat ketajaman gambar, dihitung menggunakan *Variance of Laplacian*. |
    | `brightness` | `float` | Rata-rata intensitas pixel gambar dalam grayscale (0-255). |
    """)

    st.markdown('<p class="section-header">Feature Engineering & Preprocessing</p>', unsafe_allow_html=True)
    st.markdown("""
    Untuk meningkatkan kualitas representasi data yang masuk ke model, dilakukan beberapa teknik *Feature Engineering* dan *Preprocessing*:
    
    1. **MobileNetV2 Preprocessing (`preprocess_input`)**: 
       * Mengubah rentang intensitas pixel awal dari `[0, 255]` menjadi `[-1, 1]`. Normalisasi ini merupakan standar bawaan pre-trained weights MobileNetV2 dan **krusial** untuk mencapai akurasi optimal.
    2. **Data Augmentation**: 
       * Membuat fitur sintesis dari data yang ada untuk memperkaya variasi *training*.
       * Teknik: *Random Rotation* (15 derajat), *Random Zoom* (10%), *Random Flip* (Horizontal & Vertikal), dan *Random Brightness* (10%).
       * Tujuan: Menghindari *overfitting* dan membuat model kebal terhadap perbedaan orientasi/kualitas foto pasien.
    3. **Class Weighting**: 
       * Menghitung dan memberikan bobot *penalty* yang lebih besar pada misklasifikasi kelas minoritas (Hypertrophic) agar model tidak bias menebak kelas Keloid.
    """)


# ============================
# PAGE: MODEL PERFORMANCE
# ============================
elif page == "Model Performance":
    st.markdown('<p class="main-title">Performa Model</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Perbandingan arsitektur deep learning</p>', unsafe_allow_html=True)
    st.markdown("---")

    results = load_json("model_results.json")
    best = load_json("best_model.json")

    if results:
        if best:
            st.markdown(f"""
            <div class="winner-box">
                <h3>MODEL TERBAIK</h3>
                <h1>{best['name']}</h1>
                <p style="color:#065f46; margin:0;">Accuracy: {best['accuracy']:.4f} | F1-Score: {best['f1_score']:.4f} | Precision: {best['precision']:.4f} | Recall: {best['recall']:.4f}</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("")

        df = pd.DataFrame(results).T[["accuracy","f1_score","precision","recall"]].round(4)
        df.columns = ["Accuracy", "F1-Score", "Precision", "Recall"]

        def highlight_best(s):
            is_max = s == s.max()
            return ['background-color: #065f46; color: #ffffff; font-weight: 700' if v else '' for v in is_max]

        st.dataframe(df.style.apply(highlight_best, axis=0), use_container_width=True)

        metric_colors = {"Accuracy": "#3b82f6", "F1-Score": "#8b5cf6", "Precision": "#06b6d4", "Recall": "#10b981"}
        fig = go.Figure()
        for metric in df.columns:
            fig.add_trace(go.Bar(
                name=metric, x=df.index.tolist(), y=df[metric].tolist(),
                marker_color=metric_colors[metric],
                text=[f"{v:.2%}" for v in df[metric]], textposition='outside',
                textfont=dict(size=10, color="#94a3b8"),
                hovertemplate=f'{metric}: ' + '%{y:.4f}<extra>%{x}</extra>'
            ))
        fig.update_layout(
            barmode='group',
            title=dict(text="Perbandingan Metrik Evaluasi per Arsitektur", font=dict(size=16)),
            xaxis_title="Arsitektur Model", yaxis_title="Skor",
            yaxis=dict(range=[0, 1.1], gridcolor="#334155", dtick=0.1),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#e2e8f0", size=13), height=480,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
            margin=dict(t=80, b=40)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption("**Gambar 5.** Perbandingan 4 metrik evaluasi (Accuracy, F1-Score, Precision, Recall) untuk setiap arsitektur. MobileNetV2 dengan transfer learning (frozen base) menunjukkan performa tertinggi di semua metrik.")

        st.markdown('<p class="section-header">Confusion Matrix & ROC Curve</p>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            path = PLOTS_DIR / "viz_confusion_matrix.png"
            if path.exists():
                st.image(str(path), use_container_width=True)
                st.caption("**Gambar 6.** Confusion Matrix model terbaik (MobileNetV2). Hypertrophic: 21/30 benar (70%), Keloid: 48/60 benar (80%).")
        with c2:
            path = PLOTS_DIR / "viz_roc_curve.png"
            if path.exists():
                st.image(str(path), use_container_width=True)
                st.caption("**Gambar 7.** ROC Curve dengan AUC = 0.8533. Kurva di atas diagonal menunjukkan diskriminasi baik.")

        path = PLOTS_DIR / "viz_training_history.png"
        if path.exists():
            st.markdown('<p class="section-header">Training History</p>', unsafe_allow_html=True)
            _, center, _ = st.columns([1, 6, 1])
            with center:
                st.image(str(path), use_container_width=True)
                st.caption("**Gambar 8.** Kurva training accuracy dan loss. MobileNetV2 konvergensi paling cepat dan stabil dibanding CNN Scratch.")
    else:
        st.warning("Jalankan pipeline terlebih dahulu untuk generate hasil model.")


# ============================
# PAGE: A/B TESTING
# ============================
elif page == "A/B Testing":
    st.markdown('<p class="main-title">A/B Testing</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Perbandingan statistik antar arsitektur model</p>', unsafe_allow_html=True)
    st.markdown("---")

    ab_data = load_json("ab_testing.json")
    if ab_data:
        df_ab = pd.DataFrame(ab_data)

        def color_winner(val):
            if val == "Ya":
                return 'color: #34d399; font-weight: 600'
            return ''

        st.dataframe(
            df_ab.style.applymap(color_winner, subset=["Significant"]),
            use_container_width=True,
            hide_index=True
        )
        st.caption("**Tabel 1.** Hasil A/B Testing antar model. Semua perbandingan menunjukkan perbedaan yang signifikan (Ya), mengkonfirmasi keunggulan MobileNetV2.")

        st.markdown('<p class="section-header">Visualisasi Perbandingan</p>', unsafe_allow_html=True)
        results = load_json("model_results.json")
        if results:
            models = list(results.keys())
            fig = make_subplots(rows=1, cols=2, subplot_titles=["Accuracy","F1-Score"],
                               horizontal_spacing=0.12)
            bar_colors = ["#3b82f6","#ef4444","#10b981","#f59e0b","#8b5cf6"][:len(models)]

            acc_vals = [results[m]["accuracy"] for m in models]
            f1_vals = [results[m]["f1_score"] for m in models]

            fig.add_trace(go.Bar(
                x=models, y=acc_vals, marker_color=bar_colors,
                text=[f"{v:.2%}" for v in acc_vals], textposition='outside',
                textfont=dict(size=11, color="#94a3b8"),
                hovertemplate='%{x}: %{y:.4f}<extra>Accuracy</extra>',
                showlegend=False
            ), row=1, col=1)
            fig.add_trace(go.Bar(
                x=models, y=f1_vals, marker_color=bar_colors,
                text=[f"{v:.2%}" for v in f1_vals], textposition='outside',
                textfont=dict(size=11, color="#94a3b8"),
                hovertemplate='%{x}: %{y:.4f}<extra>F1-Score</extra>',
                showlegend=False
            ), row=1, col=2)
            fig.update_yaxes(range=[0, 1.1], gridcolor="#334155", dtick=0.1, title_text="Skor")
            fig.update_xaxes(title_text="Model")
            fig.update_layout(
                height=450, plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter", color="#e2e8f0", size=13),
                margin=dict(t=60, b=40)
            )
            st.plotly_chart(fig, use_container_width=True)
            st.caption("**Gambar 9.** Perbandingan Accuracy dan F1-Score antar model. MobileNetV2 (frozen) menunjukkan skor tertinggi pada kedua metrik.")

        best = load_json("best_model.json")
        if best:
            st.markdown(f"""
            <div class="winner-box">
                <h3>KESIMPULAN A/B TESTING</h3>
                <h1>{best['name']}</h1>
                <p style="color:#065f46; margin:0;">Mengungguli semua model lain secara signifikan dengan F1-Score = {best['f1_score']:.4f}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("Jalankan pipeline terlebih dahulu.")


# ============================
# PAGE: PREDIKSI
# ============================
elif page == "Prediksi":
    st.markdown('<p class="main-title">Prediksi Gambar</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Upload gambar bekas luka untuk klasifikasi otomatis</p>', unsafe_allow_html=True)
    st.markdown("---")

    uploaded = st.file_uploader("Pilih gambar bekas luka", type=["jpg","jpeg","png","bmp"])

    if uploaded:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown('<p class="section-header">Input</p>', unsafe_allow_html=True)
            st.image(uploaded, caption="Gambar yang diupload", use_container_width=True)

        with col2:
            st.markdown('<p class="section-header">Hasil Prediksi</p>', unsafe_allow_html=True)
            best = load_json("best_model.json")
            if best:
                model_path = MODELS_DIR / f"{best['name']}.keras"
                if model_path.exists():
                    try:
                        import tensorflow as tf
                        from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

                        @st.cache_resource
                        def load_model(path):
                            return tf.keras.models.load_model(str(path))

                        model = load_model(model_path)

                        uploaded.seek(0)
                        file_bytes = np.asarray(bytearray(uploaded.read()), dtype=np.uint8)
                        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
                        img_input = preprocess_input(img.astype(np.float32))
                        img_input = np.expand_dims(img_input, axis=0)

                        pred = model.predict(img_input, verbose=0)[0][0]
                        cls = 1 if pred >= 0.5 else 0
                        conf = pred if cls == 1 else 1 - pred

                        color = "#ef4444" if cls == 0 else "#3b82f6"
                        st.markdown(f"""
                        <div style="background:{color}10; border:2px solid {color}; border-radius:12px; padding:24px; text-align:center;">
                            <p style="color:{color}; font-size:0.85rem; font-weight:600; margin:0; text-transform:uppercase; letter-spacing:1px;">Klasifikasi</p>
                            <h1 style="color:{color}; margin:4px 0; font-size:2rem;">{CLASS_NAMES[cls]}</h1>
                            <p style="color:#94a3b8; margin:0;">Confidence: <b>{conf:.1%}</b></p>
                        </div>
                        """, unsafe_allow_html=True)

                        st.markdown("")
                        st.progress(float(conf))

                        if cls == 0:
                            st.info("**Hypertrophic Scar** -- Bekas luka yang tumbuh dalam batas luka asli, cenderung membaik seiring waktu.")
                        else:
                            st.info("**Keloid Scar** -- Bekas luka yang tumbuh melampaui batas luka asli, tidak membaik sendiri tanpa penanganan.")
                    except Exception as e:
                        st.error(f"Error saat prediksi: {e}")
                else:
                    st.warning(f"File model tidak ditemukan: {model_path}")
            else:
                st.warning("Jalankan pipeline terlebih dahulu.")


# ============================
# PAGE: INSIGHT
# ============================
elif page == "Insight & Kesimpulan":
    st.markdown('<p class="main-title">Insight & Kesimpulan</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Jawaban pertanyaan bisnis dan rekomendasi pengembangan</p>', unsafe_allow_html=True)
    st.markdown("---")

    best = load_json("best_model.json")
    results = load_json("model_results.json")
    questions = load_json("business_questions.json")

    if questions and best and results:
        st.markdown('<p class="section-header">Jawaban Pertanyaan Bisnis</p>', unsafe_allow_html=True)

        n_models = len(results)
        answers = [
            f"**Belum tercapai.** Model terbaik ({best['name']}) mencapai akurasi {best['accuracy']:.1%} dan AUC 0.8533, masih di bawah target akurasi 85%. Namun AUC > 0.85 menunjukkan kemampuan diskriminasi yang baik. Faktor: dataset kecil (596 gambar), class imbalance (1:2).",
            f"**{best['name']}** dengan transfer learning dari ImageNet — Accuracy: {best['accuracy']:.4f}, F1-Score: {best['f1_score']:.4f}. Mengungguli {n_models - 1} model lainnya secara signifikan berdasarkan A/B Testing.",
            "Model memanfaatkan fitur **tekstur, warna, dan bentuk** bekas luka. Analisis EDA: Hypertrophic lebih tajam (sharpness 593.8 vs 413.2) dan brightness lebih tinggi (100.9 vs 94.1). Distribusi RGB saling overlap, sehingga deep learning diperlukan.",
            "**Ya.** Kombinasi data augmentation (rotasi, flip, zoom) + class weights + **preprocessing yang tepat** (normalisasi [-1,1] via preprocess_input) meningkatkan akurasi ~10% dibanding normalisasi standar [0,1].",
            f"Model dapat digunakan sebagai **alat bantu screening awal** (AUC 0.8533, recall seimbang 70-80%). Namun **bukan pengganti** dokter spesialis. Diperlukan validasi klinis."
        ]
        for i, (q, a) in enumerate(zip(questions, answers)):
            with st.expander(q):
                st.markdown(a)

    st.markdown('<p class="section-header">Temuan Teknis</p>', unsafe_allow_html=True)
    st.markdown("""
    1. **Preprocessing krusial**: `preprocess_input` yang sesuai arsitektur ([-1,1] untuk MobileNetV2) meningkatkan akurasi ~10%
    2. **Transfer learning > Fine-tuning** pada dataset kecil: Base layer frozen lebih efektif
    3. **CNN dari scratch tidak cukup**: Pre-trained features dari ImageNet esensial untuk medical imaging
    """)

    st.markdown('<p class="section-header">Kesimpulan Utama</p>', unsafe_allow_html=True)
    if best:
        st.markdown(f"""
        1. **Model terbaik: {best['name']}** dengan akurasi {best['accuracy']:.1%} dan F1-Score {best['f1_score']:.4f}
        2. **Transfer learning** dari ImageNet terbukti paling efektif untuk dataset medis kecil
        3. **Preprocessing yang tepat** dan **class weights** berperan krusial dalam performa model
        4. Akurasi belum mencapai target 85% — limitasi utama adalah ukuran dataset (596 gambar)
        5. Model siap sebagai **alat bantu screening** dengan supervisi tenaga medis
        """)

    st.markdown('<p class="section-header">Rekomendasi Pengembangan</p>', unsafe_allow_html=True)
    st.markdown("""
    | No | Rekomendasi | Dampak |
    |---|---|---|
    | 1 | Perbanyak dataset (1000+ gambar per kelas) | Meningkatkan akurasi signifikan |
    | 2 | Arsitektur terbaru (EfficientNetV2, ConvNeXt) | Akurasi lebih tinggi |
    | 3 | Grad-CAM untuk interpretabilitas | Kepercayaan dokter meningkat |
    | 4 | Cross-validation (k-fold) | Evaluasi lebih robust |
    | 5 | Validasi klinis dengan dermatolog | Siap deployment medis |
    """)
