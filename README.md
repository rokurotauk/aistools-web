# AIS Web App

A multi-tab Streamlit app for decoding, validating, visualising, and managing AIS (Automatic Identification System) messages.

---

## 🔧 Features

### 🧭 Decode AIS Messages
- Upload timestamped AIS logs
- Choose output format (raw string, CSV fields, or visualisation-friendly)
- Export decoded messages (all, valid only, or errors only)

### ✅ AIS Checksum Validator
- Upload AIS logs (with or without timestamps)
- Validates NMEA checksums
- Displays only invalid messages
- Exports invalid messages with timestamps

### 🗺️ AIS Map Visualisation
- Upload decoded AIS CSVs
- View vessel positions or heatmaps
- Optional trails, POIs, shapefiles

### ✉️ Encode AIS Messages *(coming soon)*  
### ⏯️ AIS Replay *(coming soon)*  
### 📈 AIS Jump Detector *(coming soon)*  
### 🔍 AIS MMSI Extractor *(coming soon)*  

---

## 🚀 How to Run

Install dependencies:
```bash
pip install -r requirements.txt
```

Launch app:
```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
app.py                     # Main entry point
decoder_tab.py             # Decoder functionality
checksum_tab.py            # Checksum validator logic
visualisation_tab.py       # Mapping logic
encoder_tab.py             # Placeholder
replay_tab.py              # Placeholder
jump_detector_tab.py       # Placeholder
mmsi_extractor_tab.py      # Placeholder
requirements.txt           # Python dependencies
README.md                  # This file
```