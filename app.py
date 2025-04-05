import streamlit as st
import pandas as pd

def clean_number(n):
    return int(n) if n == int(n) else n

st.set_page_config(page_title="Worker Payment Calculator", page_icon="💰")
st.title("Worker Payment Calculator")

# استخدام session_state لحفظ القيم
if "value" not in st.session_state:
    st.session_state.value = ""
if "withdrawn" not in st.session_state:
    st.session_state.withdrawn = ""

# إدخال القيم
value = st.text_input("Enter the total :", st.session_state.value)
withdrawn = st.text_input("Enter the withdrawn:", st.session_state.withdrawn)

# أزرار
col1, col2 = st.columns(2)
calculate_clicked = col1.button("Calculate")
reset_clicked = col2.button("Reset")

if calculate_clicked:
    if value and withdrawn:
        try:
            value_f = float(value)
            withdrawn_f = float(withdrawn)

            st.session_state.value = value
            st.session_state.withdrawn = withdrawn

            half_value = value_f / 2
            after_withdraw = half_value - withdrawn_f

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

            # جدول النتائج
            data = {
                "Label": ["Total", "Due", "Withdrawn", "Remaining"],
                "Value": [
                    clean_number(value_f),
                    clean_number(fee),
                    clean_number(withdrawn_f),
                    clean_number(final_amount),
                ]
            }

            df = pd.DataFrame(data)
            st.markdown("### Result")
            st.dataframe(df, use_container_width=True)

        except ValueError:
            st.error("Please enter valid numbers.")
    else:
        st.warning("Please fill in both fields before calculating.")

# إعادة تعيين القيم
if reset_clicked:
    st.session_state.value = ""
    st.session_state.withdrawn = ""
    st.experimental_rerun()
