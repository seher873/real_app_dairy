import streamlit as st
from fpdf import FPDF
from database import DairyDB
import os

DB = DairyDB("dairy.db")

st.title("🐼 Malik Dairy App")

st.header("Add Milk Entry")
with st.form("entry_form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Customer Name")
        contact = st.text_input("Contact")
        shift = st.selectbox("Shift", ["Morning", "Evening"])
    with col2:
        mound = st.number_input("Mound", 0.0, step=0.1)
        kg = st.number_input("Kg", 0.0, step=0.1)

    submitted = st.form_submit_button("Add Entry")
    if submitted:
        total = round((mound + kg) * 1, 2)  # Assuming fixed rate of 1 since rate is removed
        DB.add_entry(name, contact, shift, mound, kg, total)
        st.success("Entry added successfully")

st.header("All Entries")
entries = DB.get_all_entries()
if entries:
    st.dataframe(
        [{
            "Name": e[1], "Contact": e[2], "Shift": e[3], "Mound": e[4], "Kg": e[5],
            "Total": e[6]
        } for e in entries]
    )

    morning_total = sum(e[6] or 0 for e in entries if e[3] == "Morning")
    evening_total = sum(e[6] or 0 for e in entries if e[3] == "Evening")
    grand_total = morning_total + evening_total

    st.subheader("Total Summary")
    st.write(f"🌅 Morning Total: {morning_total} PKR")
    st.write(f"🌙 Evening Total: {evening_total} PKR")
    st.write(f"🮾 Grand Total: {grand_total} PKR")

    if st.button("📨 Print PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, "Malik Dairy", ln=1, align="C")
        pdf.set_font("Arial", "", 14)
        pdf.cell(200, 10, "Milk Obaid", ln=1, align="C")

        pdf.set_font("Arial", "", 10)
        pdf.ln(10)
        pdf.cell(200, 10, "All Entries:", ln=1)

        for e in entries:
            pdf.cell(200, 10, f"Name: {e[1]} | Contact: {e[2]} | Shift: {e[3]} | Mound: {e[4]} | Kg: {e[5]} | Total: {e[6]}", ln=1)

        pdf.ln(5)
        pdf.set_font("Arial", "B", 11)
        pdf.cell(200, 10, f"Morning Total: {morning_total} PKR", ln=1)
        pdf.cell(200, 10, f"Evening Total: {evening_total} PKR", ln=1)
        pdf.cell(200, 10, f"Grand Total: {grand_total} PKR", ln=1)

        filename = "dairy_report.pdf"
        pdf.output(filename)
        with open(filename, "rb") as f:
            st.download_button("📄 Download PDF", f, file_name=filename)

if st.button("🗑️ Delete All Entries"):
    DB.delete_all_entries()
    st.warning("All entries deleted.")