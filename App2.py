import streamlit as st
import pandas as pd

def clean_number(n):
    return int(n) if n == int(n) else n

st.set_page_config(page_title="CleanFoam", page_icon="✅")
st.title("CleanFoam")

# إعداد session_state
if 'workers' not in st.session_state:
    st.session_state.workers = []

if 'last_added' not in st.session_state:
    st.session_state.last_added = ""

if 'name' not in st.session_state:
    st.session_state.name = ""
if 'value' not in st.session_state:
    st.session_state.value = ""
if 'withdrawn' not in st.session_state:
    st.session_state.withdrawn = ""

# إدخال بيانات عامل جديد
st.subheader("Add New Worker")
st.session_state.name = st.text_input("Worker Name", st.session_state.name)
st.session_state.value = st.text_input("Enter the total :", st.session_state.value)
st.session_state.withdrawn = st.text_input("Enter the withdrawn:", st.session_state.withdrawn)

col1, col2 = st.columns(2)
add_clicked = col1.button("Add Worker")
done_clicked = col2.button("Done")

if add_clicked:
    if st.session_state.name and st.session_state.value and st.session_state.withdrawn:
        try:
            value_f = float(st.session_state.value)
            withdrawn_f = float(st.session_state.withdrawn)

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

            # حفظ البيانات
            st.session_state.workers.append({
                "Worker": st.session_state.name,
                "Total": clean_number(value_f),
                "Due": clean_number(fee),
                "Withdrawn": clean_number(withdrawn_f),
                "Remaining": clean_number(final_amount)
            })

            # حفظ اسم آخر عامل
            st.session_state.last_added = st.session_state.name

            # تفريغ الحقول تلقائيًا
            st.session_state.name = ""
            st.session_state.value = ""
            st.session_state.withdrawn = ""

        except ValueError:
            st.error("Please enter valid numbers.")
    else:
        st.warning("Please fill in all fields before adding.")

# عرض اسم آخر عامل تم تسجيله مع علامة صح
if st.session_state.last_added:
    st.success(f"✓ Worker '{st.session_state.last_added}' added successfully.")

# عند الضغط على Done نعرض الجدول
if done_clicked:
    if st.session_state.workers:
        st.markdown("### Workers Table")

        df = pd.DataFrame(st.session_state.workers)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No workers added yet.")
