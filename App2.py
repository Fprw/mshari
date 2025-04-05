import streamlit as st
import pandas as pd
from fpdf import FPDF
import base64

def clean_number(n):
    return int(n) if n == int(n) else n

st.set_page_config(page_title="Workers Payment Calculator", page_icon="✅")
st.title("Workers Payment Calculator")

# Session state init
if 'workers' not in st.session_state:
    st.session_state.workers = []
if 'name_input' not in st.session_state:
    st.session_state.name_input = ""
if 'value_input' not in st.session_state:
    st.session_state.value_input = ""
if 'withdrawn_input' not in st.session_state:
    st.session_state.withdrawn_input = ""
if 'due_input' not in st.session_state:
    st.session_state.due_input = ""

# Input fields
st.subheader("Add New Worker")
name = st.text_input("Worker Name", st.session_state.name_input)
value = st.text_input("Enter the total :", st.session_state.value_input)
withdrawn = st.text_input("Enter the withdrawn:", st.session_state.withdrawn_input)
due_optional = st.text_input("Enter custom Due (optional):", st.session_state.due_input)

if st.button("OK"):
    if name and value:
        try:
            value_f = float(value)
            withdrawn_f = float(withdrawn) if withdrawn else 0
            due_custom = float(due_optional) if due_optional else None

            half_value = value_f / 2
            after_withdraw = half_value - withdrawn_f

            # Fee (Due) Logic
            if due_custom is not None:
                fee = due_custom
            elif half_value == 40:
                fee = 20
            elif half_value == 45:
                fee = 22.5
            elif half_value == 50:
                fee = 25
            elif half_value == 52.5:
                fee = 27.5
            elif half_value == 55:
                fee = 25
            elif value_f == 95:
                fee = 22.5
            elif int(value_f) % 10 == 5:
                fee = 32.5
            else:
                fee = 30

            final_amount = after_withdraw - fee

            # Save worker
            st.session_state.workers.append({
                "Worker": name,
                "Total": clean_number(value_f),
                "Due": clean_number(fee),
                "Withdrawn": clean_number(withdrawn_f),
                "Remaining": clean_number(final_amount)
            })

            # Clear inputs
            st.session_state.name_input = ""
            st.session_state.value_input = ""
            st.session_state.withdrawn_input = ""
            st.session_state.due_input = ""

            st.rerun()

        except ValueError:
            st.error("Please enter valid numbers.")
    else:
        st.warning("Please fill in at least name and total.")

# Display Table
if st.session_state.workers:
    df = pd.DataFrame(st.session_state.workers)
    st.markdown("### Workers Table")
    st.dataframe(df, use_container_width=True)

    # Summary calculations
    total_sum = sum([w['Total'] for w in st.session_state.workers])
    for_workera = sum([w['Withdrawn'] + w['Remaining'] for w in st.session_state.workers])
    for_cleanfoam = total_sum - for_workera

    st.markdown(f"### Total of All Workers: **{clean_number(total_sum)}**")
    st.markdown(f"**For workera:** {clean_number(for_workera)}")
    st.markdown(f"**For CleanFoam:** {clean_number(for_cleanfoam)}")

    # PDF export button
    def generate_pdf(dataframe):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Workers Payment Report", ln=True, align="C")

        pdf.set_font("Arial", style="B", size=12)
        headers = ["Worker", "Total", "Due", "Withdrawn", "Remaining"]
        col_widths = [40, 30, 30, 30, 30]
        for i, header in enumerate(headers):
            pdf.cell(col_widths[i], 10, header, border=1, align='C')
        pdf.ln()

        pdf.set_font("Arial", size=12)
        for _, row in dataframe.iterrows():
            pdf.cell(col_widths[0], 10, str(row["Worker"]), border=1, align='C')
            pdf.cell(col_widths[1], 10, str(row["Total"]), border=1, align='C')
            pdf.cell(col_widths[2], 10, str(row["Due"]), border=1, align='C')
            pdf.cell(col_widths[3], 10, str(row["Withdrawn"]), border=1, align='C')
            pdf.cell(col_widths[4], 10, str(row["Remaining"]), border=1, align='C')
            pdf.ln()

        return pdf.output(dest='S').encode('latin-1')

    pdf_bytes = generate_pdf(df)
    b64 = base64.b64encode(pdf_bytes).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="workers_report.pdf">📄 Download PDF Report</a>'
    st.markdown(href, unsafe_allow_html=True)
else:
    st.info("No workers added yet.")
