import streamlit as st
import pandas as pd
import base64

def clean_number(n):
    return int(n) if n == int(n) else n

st.set_page_config(page_title="CleanFoam", page_icon="✅")
st.title("CleanFoam")

# Session state init
if 'workers' not in st.session_state:
    st.session_state.workers = []
if 'received_status' not in st.session_state:
    st.session_state.received_status = {}
if 'name_input' not in st.session_state:
    st.session_state.name_input = ""
if 'value_input' not in st.session_state:
    st.session_state.value_input = ""
if 'withdrawn_input' not in st.session_state:
    st.session_state.withdrawn_input = ""
if 'due_input' not in st.session_state:
    st.session_state.due_input = ""
if 'manual_date_input' not in st.session_state:
    st.session_state.manual_date_input = ""

# إدخال التاريخ
st.subheader("Today's Date")
manual_date = st.text_input("Date", st.session_state.manual_date_input)
st.session_state.manual_date_input = manual_date

# إضافة عامل
st.subheader("Add Worker")
name = st.text_input("Name", st.session_state.name_input)
value = st.text_input("Enter the total :", st.session_state.value_input)
withdrawn = st.text_input("Enter the withdrawn:", st.session_state.withdrawn_input)
due_optional = st.text_input("Enter custom Due (optional):", st.session_state.due_input)
is_cf = st.checkbox("CF")

if st.button("OK"):
    if manual_date and name and value:
        try:
            value_f = float(value)
            withdrawn_f = float(withdrawn) if withdrawn else 0
            due_custom = float(due_optional) if due_optional else None

            if is_cf:
                data = {
                    "Worker": name,
                    "Total": clean_number(value_f),
                    "Due": "",
                    "Withdrawn": "",
                    "Remaining": "",
                    "Received": False
                }
            else:
                half_value = value_f / 2
                after_withdraw = half_value - withdrawn_f

                if due_custom is not None:
                    fee = due_custom
                elif half_value == 40:
                    fee = 20
                elif half_value == 45:
                    fee = 20
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

                data = {
                    "Worker": name,
                    "Total": clean_number(value_f),
                    "Due": clean_number(fee),
                    "Withdrawn": clean_number(withdrawn_f),
                    "Remaining": clean_number(final_amount),
                    "Received": False
                }

            st.session_state.workers.append(data)
            st.session_state.received_status[name] = False

            # Clear inputs
            st.session_state.name_input = ""
            st.session_state.value_input = ""
            st.session_state.withdrawn_input = ""
            st.session_state.due_input = ""

            st.rerun()

        except ValueError:
            st.error("Please enter valid numbers.")
    else:
        st.warning("Please fill in at least date, name, and total.")

# عرض الجدول
if st.session_state.workers:
    st.markdown(f"### Workers Table — Date: **{manual_date}**")

    display_df = pd.DataFrame(st.session_state.workers)

    # التحكم في Received لكل عامل
    for i, worker in enumerate(display_df["Worker"]):
        received_key = f"received_{i}"
        if received_key not in st.session_state:
            st.session_state[received_key] = display_df.at[i, "Received"]

        st.session_state[received_key] = st.checkbox(
            f"Received: {worker}", value=st.session_state[received_key]
        )
        display_df.at[i, "Received"] = st.session_state[received_key]

    # تلوين الصفوف اللي فيها Remaining سالب
    def highlight_negative(val):
        return 'background-color: #ffcccc' if val < 0 else ''

    styled_df = display_df.style.applymap(highlight_negative, subset=["Remaining"])

    st.dataframe(styled_df, use_container_width=True)

    # حساب المجموع
    total_sum = sum([w['Total'] for w in st.session_state.workers if isinstance(w['Total'], (int, float))])
    for_workera = sum([
        (w['Withdrawn'] if isinstance(w['Withdrawn'], (int, float)) else 0) +
        (w['Remaining'] if isinstance(w['Remaining'], (int, float)) else 0)
        for w in st.session_state.workers
    ])
    for_cleanfoam = total_sum - for_workera

    st.markdown(f"### Total: **{clean_number(total_sum)}**")
    st.markdown(f"**For workera:** {clean_number(for_workera)}")
    st.markdown(f"**For CleanFoam:** {clean_number(for_cleanfoam)}")

    # حذف عامل
    st.markdown("### Delete")
    worker_names = [w['Worker'] for w in st.session_state.workers]
    selected_worker = st.selectbox("Select worker to delete", worker_names)

    if st.button("Delete"):
        st.session_state.workers = [w for w in st.session_state.workers if w['Worker'] != selected_worker]
        st.success(f"Worker '{selected_worker}' has been deleted.")
        st.rerun()

    # إرسال: حفظ الجدول كملف CSV
    st.markdown("### إرسال البيانات")
    if st.button("إرسال"):
        export_df = pd.DataFrame(st.session_state.workers)
        csv = export_df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="cleanfoam_{manual_date}.csv">Download CSV for Notion</a>'
        st.markdown(href, unsafe_allow_html=True)
else:
    st.info("No workers added yet.")
