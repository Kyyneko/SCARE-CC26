## **Overview**
This project implements a transfer learning workflow using the EfficientFormer-L1 backbone pretrained on ImageNet on binary image classification

### **Data Preparation & Augmentation**

* **Dataset Setup:** The data containing 261 training images, 86 validation images, and 87 test images.


* **Data Augmentation:** The training data uses an `ImageDataGenerator` for augmentation configured with rotations (20 degrees), width/height shifts (15%), shearing (20%), zooming (20%), and horizontal flipping to improve model generalization.

### Model Architecture
The proposed architecture leverages transfer learning via a fully trainable EfficientFormerL1 backbone, initialized with pre-trained ImageNet weights. The base feature extractor is appended with a custom classification head beginning with a Global Average Pooling (GAP) layer. This is followed by a fully connected layer (128 units) utilizing L2 regularization ($\lambda = 0.01$), Batch Normalization, and a ReLU activation function. To effectively mitigate overfitting, a high dropout rate ($p = 0.6$) is applied prior to the final classification layer, which consists of a 2-unit dense layer with a softmax activation function to output the categorical probabilities.

Table below outlines the structural configuration of the proposed network

| Layer / Stage | Layer Type / Core Operation | Output Shape / Configuration |
| :--- | :--- | :--- |
| **Backbone** | EfficientFormerL1 (Pre-trained ImageNet) | Fully Trainable |
| **Pooling** | Global Average Pooling 2D | [Batch, 448] |
| **Fully Connected** | Dense (L2 Regularization $\lambda = 0.01$) | 128 Units |
| **Normalization** | Batch Normalization | [Batch, 128] |
| **Activation** | Rectified Linear Unit (ReLU) | - |
| **Regularization** | Dropout ($p = 0.6$) | - |
| **Classification** | Dense (Softmax Activation) | 2 Units (Output) |


### **Training Configuration**
| Component | Parameter / Type | Tweaks |
| :--- | :--- | :--- |
| **Optimizer** | `AdamW` | Learning Rate: 0.0005 |
| **Loss Function** | `categorical_crossentropy` | - |
| **EarlyStopping** | Callback | Monitor: Validation Loss, Patience: 50 epochs |
| **ReduceLROnPlateau** | Callback | Monitor: Validation Accuracy, Factor: 0.2, Patience: 7 epochs |
| **ThresholdCallback** | Custom Callback | Target Validation Accuracy: >= 90% |

---




## **Evaluation & Results**
The final evaluation on the test dataset yielded a test loss of **0.8986** and an overall accuracy of **87.36%**.

### **Model Export**
You can download trained models in a TensorFlow Lite format, Keras and legacy (`.h5`) formats at [Saved Models](https://drive.google.com/drive/folders/1ncadm6BNV-x9-O-LHh1DfOnQFl24J1Sr?usp=sharing)
