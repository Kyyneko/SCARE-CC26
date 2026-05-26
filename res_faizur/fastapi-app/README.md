# Scar Image Classification API

A FastAPI service designed to run local, real-time inference on a TensorFlow Lite (TFLite) image classification model, distinguishing between target categories: **Hypertrophic** and **Keloid** scars.

---

## API Capabilities and Design

* **Dual-Class Classification:** Specifically maps images of scars to `"Hypertrophic"` or `"Keloid"` outputs.
* **TFLite Engine Integration:** Powered by a fast, optimized `tflite-runtime` interpreter, offering rapid responses without the memory footprint of full TensorFlow.
* **Auto-Pre-processing:** Automatically maps input upload files (images), dynamic sizes to match the pre-defined target input shape configured inside your TFLite model, and maps pixel arrays to `[0.0, 1.0]` floating-point values.
* **Cross-Origin Access (CORS):** Pre-equipped with liberal CORS access middlewares so JavaScript frontends can connect without encountering security blocks.

---

## API Endpoints Reference

### 1. Root / Service Health Status
Checks if the underlying web application service is running and whether the custom `.tflite` model was successfully imported into the runtime memory buffer.

* **Method:** `GET`
* **Path:** `/`
* **Response Signature (`application/json`):**
  ```json
  {
    "status": "active",
    "message": "Scar Classification API is running.",
    "model_loaded": true,
    "instructions": "Send a POST request with an image file to /predict/."
  }
  ```

---

### 2. File Inference & Scar Categorization
Submit raw file records directly to have the system parse, pre-process, calculate predictions, and return classifications.

* **Method:** `POST`
* **Path:** `/predict/`
* **Content-Type:** `multipart/form-data`
* **Payload Parameters:**
  
  | Field Name | Type | Source | Definition |
  | :--- | :--- | :--- | :--- |
  | `file` | `Binary (File upload)` | Form Data | The scar image to classify (`JPEG`, `PNG`, etc.) |

* **Response Signature (`application/json`):**
  ```json
  {
    "prediction": "Keloid",
    "confidence": 0.8941295742988586,
    "all_scores": {
      "Hypertrophic": 0.10587042570114136,
      "Keloid": 0.8941295742988586
    }
  }
  ```

* **Possible Non-200 Status Codes:**
  * `400 Bad Request` - Provided file type is not a valid image format.
  * `503 Service Unavailable` - Model binary is missing from the server root directory layout.
  * `500 Internal Server Error` - Underlying numpy matrix operations or math processing failed.
  
  
---
