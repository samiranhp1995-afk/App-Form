import streamlit as st
import pandas as pd

# برای ذخیره داده‌های جمع‌آوری شده
if "general_data" not in st.session_state:
    st.session_state.general_data = {}
if "documents" not in st.session_state:
    st.session_state.documents = {}
if "fats" not in st.session_state:
    st.session_state.fats = []

st.title("Fiber Project QA Checklist")

# -----------------------
# مرحله 1: اطلاعات عمومی
# -----------------------
with st.form("general_form"):
    st.subheader("General Information")
    st.session_state.general_data["Region"] = st.text_input("Region")
    st.session_state.general_data["Province"] = st.text_input("Province")
    st.session_state.general_data["City"] = st.text_input("City")
    st.session_state.general_data["Site ID / POP"] = st.text_input("Site ID / POP")
    st.session_state.general_data["Date of Visit"] = st.date_input("Date of Visit")
    st.session_state.general_data["MTMI QA-Audit Name"] = st.text_input("MTMI QA-Audit Name")
    st.session_state.general_data["Vendor/Subcontractor"] = st.text_input("Vendor/Subcontractor")
    st.session_state.general_data["MS Audit Name"] = st.text_input("MS Audit Name")
    st.session_state.general_data["Site FAT/ODC used port number"] = st.text_input("Site FAT/ODC used port number")
    st.session_state.general_data["PWR port uplink"] = st.text_input("PWR port uplink")

    submitted = st.form_submit_button("Save General Info")
    if submitted:
        st.success("✅ General information saved.")

# -----------------------
# مرحله 2: مدارک و مستندات
# -----------------------
with st.form("documents_form"):
    st.subheader("Documents Checklist (OK / Not OK)")
    st.session_state.documents["OSS or KMZ FAT location"] = st.radio("OSS or KMZ FAT location", ["OK", "Not OK"])
    st.session_state.documents["Fusion plan"] = st.radio("Fusion plan", ["OK", "Not OK"])
    st.session_state.documents["Port plan"] = st.radio("Port plan", ["OK", "Not OK"])
    st.session_state.documents["SLD diagram"] = st.radio("SLD diagram", ["OK", "Not OK"])

    submitted = st.form_submit_button("Save Documents Info")
    if submitted:
        st.success("✅ Documents information saved.")

# -----------------------
# مرحله 3: FAT ها
# -----------------------
st.subheader("FAT Section")

with st.form("fat_form", clear_on_submit=True):
    fat_number = st.text_input("FAT Number")

    st.write("Checklist (OK / Not OK)")
    fat_checklist = {
        "Master": st.radio("Master", ["OK", "Not OK"]),
        "Labeling": st.radio("Labeling", ["OK", "Not OK"]),
        "Splitter": st.radio("Splitter", ["OK", "Not OK"]),
        "Gas Clamp": st.radio("Gas Clamp", ["OK", "Not OK"]),
        "Fiber Arrangement": st.radio("Fiber Arrangement", ["OK", "Not OK"]),
        "Splitter Arrangement": st.radio("Splitter Arrangement", ["OK", "Not OK"]),
        "Cassette Priority": st.radio("Cassette Priority", ["OK", "Not OK"]),
        "FAT Box Installation": st.radio("FAT Box Installation", ["OK", "Not OK"]),
        "FAT Isolation": st.radio("FAT Isolation", ["OK", "Not OK"]),
        "Mosaic/Asphalt repairing": st.radio("Mosaic/Asphalt repairing", ["OK", "Not OK"]),
    }

    st.write("Numeric Values and Comment")
    fat_values = {
        "Core#1 PWR": st.number_input("Core#1 PWR", step=0.1),
        "Core#2 PWR": st.number_input("Core#2 PWR", step=0.1),
        "Splitter#1 PWR": st.number_input("Splitter#1 PWR", step=0.1),
        "Splitter#2 PWR": st.number_input("Splitter#2 PWR", step=0.1),
        "Comment": st.text_area("Comment"),
    }

    submitted = st.form_submit_button("➕ Add FAT")
    if submitted:
        fat_entry = {"FAT Number": fat_number}
        fat_entry.update(fat_checklist)
        fat_entry.update(fat_values)
        st.session_state.fats.append(fat_entry)
        st.success(f"✅ FAT {fat_number} added.")

# نمایش FAT های وارد شده
if st.session_state.fats:
    st.write("### FATs Added")
    st.dataframe(pd.DataFrame(st.session_state.fats))

# -----------------------
# مرحله 4: خروجی Excel
# -----------------------
if st.button("📥 Export to Excel"):
    all_data = []
    for fat in st.session_state.fats:
        row = {}
        row.update(st.session_state.general_data)
        row.update(st.session_state.documents)
        row.update(fat)
        all_data.append(row)

    df = pd.DataFrame(all_data)
    df.to_excel("fiber_checklist.xlsx", index=False)
    st.download_button("Download Excel File", data=df.to_excel(index=False), file_name="fiber_checklist.xlsx")
