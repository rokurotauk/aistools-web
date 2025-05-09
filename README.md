# AIS Web App

This web application provides two main functionalities:
1. **Decode raw AIS messages** from timestamped NMEA logs.
2. **Visualise AIS data** as vessel positions or heatmaps on an interactive map.

Built using [Streamlit](https://streamlit.io), [pyais](https://github.com/M0r13n/pyais), [Folium](https://python-visualization.github.io/folium/), and [Geopandas](https://geopandas.org/).

---

## 📦 Features

### 🧭 Decoder Tab
- Upload raw AIS logs (each line: `timestamp NMEA`)
- Choose output format:
  - Raw `pyais` decoded string
  - CSV field values
  - Visualisation format (`mmsi, latitude, longitude, timestamp`)
- Download decoded results (all, valid only, or errors only)
- Supports multi-part messages (e.g., type 5)

### 🗺️ Visualisation Tab
- Upload CSV files (decoded AIS data)
- Visualise by:
  - Vessel positions (with optional trails)
  - Heatmap mode
- Add:
  - Points of interest (POI CSV)
  - Shapefiles (ZIP format)

---

## 🚀 Deployment (Streamlit Cloud)

1. Push this repo to [GitHub](https://github.com)
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
3. Click "New app" and link your repo
4. Set **main file** to `app.py`
5. Done! Your app will be deployed live.

---

## 📁 File Structure

```
app.py                  # Main app entry point
decoder_tab.py          # AIS decoding functionality
visualisation_tab.py    # Map visualisation logic
requirements.txt        # Python dependencies
README.md               # This file
```

---

## 🛠 Requirements

Install locally with:
```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 📄 Sample Data

You can use the included `sample_ais_positions.csv` to test the visualisation tab.

---

## 🔐 License

MIT License.