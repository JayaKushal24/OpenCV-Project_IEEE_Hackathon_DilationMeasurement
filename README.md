# 📏 Dilation Measurement using OpenCV & Kivy

**Project Name:** Project_IEEE_Hackathon_Cervical Dilation Measurement  

## 📌 Overview
### 🔴 **Current Problem with Existing Methods**
Traditional cervical dilation measurement methods often rely on **manual inspection** by healthcare professionals, which can be **subjective, inconsistent, and prone to errors**. Existing imaging techniques using **ultrasound or conventional cameras** may lack precision in detecting the exact dilation, especially in **low-light or obstructed conditions**. Additionally, these methods often require **expensive equipment**, making them less accessible in resource-limited settings.

### 🟢 **Why This Proposed Idea is Better**
This project introduces an **automated, real-time, and non-invasive approach** using **millimeter wave endoscope cameras, OpenCV, and Kivy**. The system:  
✅ **Improves Accuracy** – Uses computer vision for precise radius and area detection.  
✅ **Eliminates Subjectivity** – Provides quantitative, repeatable measurements.  
✅ **Enhances Real-Time Monitoring** – Continuously tracks changes in dilation.  
✅ **Cost-Effective & Scalable** – Works with widely available endoscope cameras.  
✅ **Reduces Manual Errors** – Automates data collection and logging.  

This innovative system enhances the **efficiency, accuracy, and accessibility** of cervical dilation measurement, making it a promising solution for **clinical and remote healthcare applications**.

### 🔹 Key Features
✅ **Live Video Processing** using OpenCV  
✅ **Real-time Circle Detection** with adjustable edge detection thresholds  
✅ **Radius & Area Calculation in cm²** based on a **calibration factor**  
✅ **Kivy GUI Integration** with sliders for tuning detection parameters  
✅ **Data Logging to CSV** for analysis  
✅ **Detection & Highlighting of Relevant Areas** in the video feed  

---

## 🛠 Implementation Details

### 📸 **Circle Detection Process**
1️⃣ Captures live video using **OpenCV** from **endoscope cameras**.  
2️⃣ Applies **Gaussian Blur** & converts to **grayscale**.  
3️⃣ Uses **Canny Edge Detection** with user-controlled threshold values.  
4️⃣ Detects **circular contours** using `cv2.findContours()` & `cv2.minEnclosingCircle()`.  
5️⃣ Converts detected radius from pixels to **centimeters** using a **conversion factor**.  
6️⃣ **Calculates the area** of detected regions using `π * r²`.  
7️⃣ **Highlights and marks the detected areas** on the live video feed.  
8️⃣ Displays detected radius and area on-screen (toggle ON/OFF).  
9️⃣ Logs the detected radius and area into a **CSV file** for further study.  

### 📡 **Conversion Factor**
- The conversion factor translates pixels to real-world measurements. 
- Current factor: `0.0167 cm/pixel` (adjustable based on calibration).

---

## 🎛 GUI Features (Kivy UI)
### **Sliders for Dynamic Control**
🎚 **Threshold 1** - Controls lower edge detection sensitivity  
🎚 **Threshold 2** - Controls upper edge detection sensitivity  

### **Buttons**
🔘 **"Radius" Button** - Toggles radius display & logs data to CSV  

---

## 📂 Data Logging (CSV Output)
- Each detected radius (in cm) and area (in cm²) is stored along with the **timestamp (HH:MM format)**.
- Data is saved to `output.csv` for later analysis.

Example Entry:
```
Time, Radius (cm), Area (cm²)
14:30, 3.45, 37.39
14:31, 3.50, 38.47
```

---

## 🚀 Getting Started
### 🔹 **Installation Requirements**
Ensure you have the required dependencies installed:
```sh
pip install opencv-python numpy kivy
```

### 🔹 **Run the Application**
```sh
python main.py
```

---

## 📧 Contact
For any queries, reach out to **Yandarapu Jaya Kushal** at [yandarapu.jaya2022@vitstudent.ac.in](mailto:yandarapu.jaya2022@vitstudent.ac.in)

🚀 **Developed for IEEE Hackathon**
