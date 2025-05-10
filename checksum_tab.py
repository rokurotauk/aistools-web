import streamlit as st
import pandas as pd
import csv
import io
import re

def calculate_nmea_checksum(nmea_str):
    if nmea_str.startswith(('!', '$')):
        nmea_str = nmea_str[1:]
    data_to_check = nmea_str.split('*')[0]
    checksum = 0
    for char in data_to_check:
        checksum ^= ord(char)
    return f"{checksum:02X}"

def extract_nmea(line: str) -> str:
    if "!AI" not in line or "*" not in line:
        return None
    try:
        start = line.index("!AI")
        end = line.index("*", start)
        sentence = line[start:end+3]  # include * and 2 hex chars
        if len(sentence.split("*")[1]) == 2:
            return sentence
    except ValueError:
        return None
    return None

def validate_checksum_debug(line: str):
    if '*' not in line:
        return "MISSING *", "", "", ""
    try:
        sentence, provided_checksum = line.rsplit('*', 1)
        calculated = calculate_nmea_checksum(sentence)
        return ("VALID" if calculated.upper() == provided_checksum.upper() else "INVALID",
                calculated, provided_checksum, sentence)
    except Exception:
        return "ERROR", "", "", ""

def render_checksum_tab():
    st.title('✅ AIS Checksum Validator')
    uploaded_file = st.file_uploader("Upload AIS NMEA log (with or without timestamps)", type=["txt", "log", "csv"], key="checksum")

    if uploaded_file:
        lines = uploaded_file.read().decode("utf-8").splitlines()
        results = []
        valid_count = 0
        invalid_count = 0

        with st.spinner("Validating checksums..."):
            for idx, raw_line in enumerate(lines, start=1):
                line = raw_line.strip()

                nmea = extract_nmea(line)
                if not nmea:
                    results.append([str(idx), "NOT FOUND", raw_line.strip(), "", "", ""])
                    invalid_count += 1
                    continue

                status, calculated, expected, body = validate_checksum_debug(nmea)
                if status == "VALID":
                    valid_count += 1
                else:
                    invalid_count += 1
                results.append([str(idx), status, raw_line.strip(), nmea, calculated, expected])

        st.success(f"✅ {valid_count} valid, ❌ {invalid_count} invalid out of {len(lines)} lines")

        df = pd.DataFrame([[str(v) for v in row] for row in results], columns=[
            "Line #", "Status", "Original Line", "Extracted NMEA", "Calculated Checksum", "Expected Checksum"
        ])

        if invalid_count > 0:
            st.warning(f"❌ {invalid_count} invalid messages found:")
            st.dataframe(df[df['Status'] != 'VALID'], use_container_width=True)
            csv_output = df[df['Status'] != 'VALID'].to_csv(index=False)
            st.download_button('⬇️ Download Invalid Messages', data=csv_output, file_name='invalid_messages.csv', mime='text/csv')
        else:
            st.success('✅ All messages are valid!')