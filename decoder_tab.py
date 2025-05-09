import streamlit as st
import csv
import io
from datetime import datetime
from pyais import NMEAMessage

def render_decoder_tab():
    def convert_timestamp(epoch_timestamp):
        try:
            dt_object = datetime.utcfromtimestamp(float(epoch_timestamp))
            return dt_object.strftime('%Y-%m-%d %H:%M:%S.%f')
        except ValueError as e:
            return f"Invalid timestamp: {epoch_timestamp}. Error: {e}"

    def decode_line(line, output_format):
        try:
            parts = line.strip().split(" ", 1)
            if len(parts) != 2:
                return {"timestamp": "Invalid", "decoded_message": None, "csv_fields": None, "decoded_obj": None, "error": f"Invalid line format: {line.strip()}"}
            epoch_timestamp, raw_message = parts
            human_timestamp = convert_timestamp(epoch_timestamp)
            nmea_message = NMEAMessage.from_string(raw_message)
            decoded_message = nmea_message.decode()
            csv_fields = list(decoded_message.asdict().values()) if output_format == "CSV values" else None
            return {"timestamp": human_timestamp, "decoded_message": str(decoded_message), "decoded_obj": decoded_message, "csv_fields": csv_fields, "error": None}
        except Exception as e:
            return {"timestamp": "Error", "decoded_message": None, "csv_fields": None, "decoded_obj": None, "error": str(e)}

    if "include_headers" not in st.session_state:
        st.session_state.include_headers = True
    output_format = st.selectbox(
        "Decoded message format",
        ["Raw pyais string", "CSV values", "For visualisation (.csv with lat/lon/mmsi/timestamp)"],
        key="format"
    )
    include_headers = False
    if output_format == "For visualisation (.csv with lat/lon/mmsi/timestamp)":
        include_headers = st.checkbox("Include headers in CSV export", value=st.session_state.include_headers)
        st.session_state.include_headers = include_headers

    uploaded_file = st.file_uploader("Upload AIS log file (with timestamps and NMEA)", type=["txt", "log", "csv"], key="decode")
    if uploaded_file and st.button("Start Decode"):
        with st.spinner("Decoding in progress..."):
            content = uploaded_file.read().decode("utf-8").splitlines()
            progress = st.progress(0)
            decoded_results = []
            total = len(content)
            for i, line in enumerate(content):
                decoded_results.append(decode_line(line, output_format))
                progress.progress((i + 1) / total)

        def convert_to_csv(decoded, format_option):
            output = io.StringIO()
            writer = csv.writer(output)
            if format_option == "For visualisation (.csv with lat/lon/mmsi/timestamp)" and include_headers:
                writer.writerow(["mmsi", "latitude", "longitude", "timestamp"])
            for entry in decoded:
                if format_option == "CSV values" and entry["csv_fields"] and not entry["error"]:
                    writer.writerow([entry["timestamp"]] + entry["csv_fields"])
                elif format_option == "For visualisation (.csv with lat/lon/mmsi/timestamp)" and entry["decoded_message"] and not entry["error"]:
                    try:
                        fields = entry["decoded_obj"].asdict() if entry["decoded_obj"] else {}
                        if fields.get("type") == 5:
                            continue
                        mmsi = fields.get("mmsi")
                        lat = fields.get("y") or fields.get("lat")
                        lon = fields.get("x") or fields.get("lon")
                        if not all([mmsi, lat, lon]):
                            continue
                        ts = entry["timestamp"]
                        writer.writerow([mmsi, lat, lon, ts])
                    except:
                        continue
                elif format_option == "Raw pyais string":
                    writer.writerow([entry["timestamp"], entry["decoded_message"], entry["error"]])
            return output.getvalue()

        valid = [d for d in decoded_results if not d["error"]]
        errors = [d for d in decoded_results if d["error"]]
        col1, col2, col3 = st.columns(3)
        with col1:
            st.download_button("📄 Download All", data=convert_to_csv(decoded_results, output_format),
                file_name="decoded_all_values.csv" if output_format == "CSV values" else "decoded_all_raw.csv",
                mime="text/csv")
        with col2:
            st.download_button("✅ Valid Only", data=convert_to_csv(valid, output_format),
                file_name="decoded_valid_values.csv" if output_format == "CSV values" else "decoded_valid_raw.csv",
                mime="text/csv")
        with col3:
            st.download_button("❌ Errors Only", data=convert_to_csv(errors, output_format),
                file_name="decoded_errors.csv", mime="text/csv")