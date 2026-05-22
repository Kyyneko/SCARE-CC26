require("dotenv").config(); // Muat variabel dari file .env sebelum apapun

const express = require("express");
const cors = require("cors");
const multer = require("multer");
const sequelize = require("./config/database");
const Prediction = require("./models/Prediction");
const { classifyScar } = require("./services/predictService");

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware wajib
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Sinkronisasi Database
sequelize.sync({ force: false }) // force: false memastikan data tidak terhapus setiap server restart
  .then(() => console.log("Database SQLite berhasil disinkronisasi."))
  .catch((err) => console.error("Gagal sinkronisasi database:", err));

// Konfigurasi Multer untuk upload file gambar (In-Memory Buffer)
const storage = multer.memoryStorage();
const upload = multer({
  storage: storage,
  limits: { fileSize: 10 * 1024 * 1024 }, // Batas ukuran file 10MB
  fileFilter: (req, file, cb) => {
    if (file.mimetype.startsWith("image/")) {
      cb(null, true);
    } else {
      cb(new Error("Hanya file gambar (JPG, JPEG, PNG) yang diperbolehkan!"), false);
    }
  },
});

// ==========================================
// ENDPOINT RESTful API
// ==========================================

// 1. POST /api/predict - Melakukan klasifikasi AI & simpan metadata ke database
app.post("/api/predict", upload.single("image"), async (req, res, next) => {
  try {
    const { sessionId } = req.body;

    // Proteksi: validasi input file
    if (!req.file) {
      return res.status(400).json({
        status: "fail",
        message: "Silakan unggah gambar luka terlebih dahulu.",
      });
    }

    // Proteksi: validasi session ID
    if (!sessionId) {
      return res.status(400).json({
        status: "fail",
        message: "Parameter sessionId wajib disertakan.",
      });
    }

    console.log(`[POST /api/predict] Memproses gambar untuk sessionId: ${sessionId}`);

    // Proses klasifikasi menggunakan Service AI
    const result = await classifyScar(req.file.buffer);

    // Simpan metadata analisis ke database (TIDAK menyimpan file gambar untuk menjaga privasi)
    const prediction = await Prediction.create({
      sessionId: sessionId,
      label: result.label,
      accuracy: result.accuracy,
    });

    // Kembalikan respons RESTful yang rapi
    return res.status(201).json({
      status: "success",
      message: "Model classified successfully",
      data: {
        id: prediction.id,
        label: prediction.label,
        accuracy: prediction.accuracy,
        createdAt: prediction.createdAt,
      },
    });
  } catch (error) {
    next(error); // Lempar error ke middleware global agar tidak crash
  }
});

// 2. GET /api/predictions - Mengambil riwayat analisis (bisa disaring per sessionId)
app.get("/api/predictions", async (req, res, next) => {
  try {
    const { sessionId } = req.query;
    let predictions;

    if (sessionId) {
      // Mengambil riwayat hanya untuk session aktif pengguna saat ini
      predictions = await Prediction.findAll({
        where: { sessionId },
        order: [["createdAt", "DESC"]],
      });
    } else {
      // Mengambil seluruh riwayat anonim (misal untuk statistik global)
      predictions = await Prediction.findAll({
        order: [["createdAt", "DESC"]],
      });
    }

    return res.status(200).json({
      status: "success",
      results: predictions.length,
      data: predictions,
    });
  } catch (error) {
    next(error);
  }
});

// 3. DELETE /api/predictions - Menghapus semua riwayat sesi aktif (fitur privasi user)
app.delete("/api/predictions", async (req, res, next) => {
  try {
    const { sessionId } = req.query;

    if (!sessionId) {
      return res.status(400).json({
        status: "fail",
        message: "Parameter sessionId wajib disertakan untuk menghapus riwayat.",
      });
    }

    console.log(`[DELETE /api/predictions] Menghapus riwayat untuk sessionId: ${sessionId}`);

    // Menghapus data riwayat sesi aktif dari database
    const deletedCount = await Prediction.destroy({
      where: { sessionId },
    });

    return res.status(200).json({
      status: "success",
      message: `Berhasil menghapus ${deletedCount} riwayat sesi dari database.`,
    });
  } catch (error) {
    next(error);
  }
});

// Endpoint default info
app.get("/", (req, res) => {
  res.status(200).json({
    name: "SCARE Advanced Scar Classification Engine API",
    status: "running",
  });
});

// ==========================================
// GLOBAL ERROR HANDLING MIDDLEWARE (Crash Protection)
// ==========================================
app.use((err, req, res, next) => {
  console.error("Terjadi error pada API SCARE:", err.message);

  const statusCode = err.name === "MulterError" ? 400 : 500;
  
  res.status(statusCode).json({
    status: "error",
    message: err.message || "Terjadi kesalahan internal pada server SCARE.",
  });
});

// Menjalankan server Express
if (process.env.NODE_ENV !== "test") {
  app.listen(PORT, () => {
    console.log(`Server Express SCARE berjalan di http://localhost:${PORT}`);
  });
}

module.exports = app;
