import streamlit as st
import pandas as pd

def clean_number(n):
    return int(n) if n == int(n) else n

st.set_page_config(page_title="CleanFoam", page_icon="✅")
st.title("CleanFoam")

# إعداد session_state
if 'workers' not in st.session_state:
    st.session_state.workers = []

if 'added_names' not in st.session_state:
    st.session_state.added_names = []

if 'name' not in st.session_state:
    st.session_state.name = ""
if 'value' not in st.session_state:
    st.session_state.value = ""
if 'withdrawn' not in st.session_state:
    st.session_state.withdrawn = ""

# عرض أسماء العمال المضافة
if st.session_state.added_names:
    st.markdown("### Added Workers:")
    names_html = "<div style='display:flex; flex-wrap:wrap;'>"
    for worker_name in st.session_state.added_names:
        names_html += f"""
        <div style='background-color:#d4edda; color:#155724; border-radius:5px;
                    padding:6px 12px; margin:5px; font-weight:bold; display:inline-block;'>
            ✓ {worker_name}
        </div>
        """
    names_html += "</div>"
    st.markdown(names_html, unsafe_allow_html=True)

# إدخال بيانات عامل جديد
st.subheader("Add New Worker")
st.session_state.name = st.text_input("Worker Name", st.session_state.name)
st.session_state.value = st.text_input("Enter the total :", st.session_state.value)
st.session_state.withdrawn = st.text_input("Enter the withdrawn:", st.session_state.withdrawn)

col1, col2, col3 = st.columns(3)
ok_clicked = col1.button("OK")
add_next_clicked = col2.button("Add Worker")
done_clicked = col3.button("Done")

# OK يقوم بالحساب وتسجيل العامل
if ok_clicked:
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

            # إضافة الاسم إلى القائمة الظاهرة
            st.session_state.added_names.append(st.session_state.name)

        except ValueError:
            st.error("Please enter valid numbers.")
    else:
        st.warning("Please fill in all fields before pressing OK.")

# Add Worker يقوم فقط بتصفية الحقول
if add_next_clicked:
    st.session_state.name = ""
    st.session_state.value = ""
    st.session_state.withdrawn = ""

# عند الضغط على Done نعرض الجدول
if done_clicked:
    if st.session_state.workers:
        st.markdown("### Workers Table")
        df = pd.DataFrame(st.session_state.workers)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No workers added yet.")
