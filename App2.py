import streamlit as st

def clean_number(n):
    return int(n) if n == int(n) else n

st.set_page_config(page_title="CleanFoam", page_icon="💰")
st.title("CleanFoam")

# إعداد session_state
if 'workers' not in st.session_state:
    st.session_state.workers = []

# إدخال بيانات عامل جديد
st.subheader("Add New Worker")
name = st.text_input("Worker Name")
value = st.text_input("Enter the total :")
withdrawn = st.text_input("Enter the withdrawn:")

col1, col2 = st.columns(2)
add_clicked = col1.button("Add Worker")
show_clicked = col2.button("Show Table")

if add_clicked:
    if name and value and withdrawn:
        try:
            value_f = float(value)
            withdrawn_f = float(withdrawn)

            half_value = value_f / 2
            after_withdraw = half_value - withdrawn_f

            # شروط الخصم
            if half_value == 40:
                fee = 20
            elif half_value == 45:
                fee = 22.5
            elif half_value == 50:
                fee = 25
            elif half_value == 55:
                fee = 27.5
            elif value_f == 95:
                fee = 22.5
            elif int(value_f) % 10 == 5:
                fee = 32.5
            else:
                fee = 30

            final_amount = after_withdraw - fee

            # حفظ البيانات في القائمة
            st.session_state.workers.append({
                "Worker": name,
                "Total": clean_number(value_f),
                "Due": clean_number(fee),
                "Withdrawn": clean_number(withdrawn_f),
                "Remaining": clean_number(final_amount)
            })

            # مسح الحقول
            st.success(f"Worker '{name}' added successfully.")

        except ValueError:
            st.error("Please enter valid numbers.")
    else:
        st.warning("Please fill in all fields before adding.")

# عرض جدول العمال
if show_clicked and st.session_state.workers:
    st.markdown("### Workers Table")

    # تنسيق الجدول بـ HTML
    table_html = """
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            text-align: center;
            padding: 10px;
            font-weight: bold;
            border-bottom: 1px solid #ddd;
        }
    </style>
    <table>
        <tr><th>Worker</th><th>Total</th><th>Due</th><th>Withdrawn</th><th>Remaining</th></tr>
    """

    for worker in st.session_state.workers:
        table_html += f"""
        <tr>
            <td>{worker['Worker']}</td>
            <td>{worker['Total']}</td>
            <td>{worker['Due']}</td>
            <td>{worker['Withdrawn']}</td>
            <td>{worker['Remaining']}</td>
        </tr>
        """

    table_html += "</table>"
    st.markdown(table_html, unsafe_allow_html=True)

elif show_clicked:
    st.info("No workers added yet.")
