# cleanfoam_app.py
import streamlit as st
import pandas as pd
import os
import json

# إعداد الصفحة
st.set_page_config(page_title="CleanFoam", page_icon="✅")

# دالة تنظيف الأرقام
def clean_number(n):
    return int(n) if n == int(n) else n

# الدالة الخاصة بواجهة المستخدم
def user_interface():
    st.title("CleanFoam - User Panel")

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
    if 'manual_date_input' not in st.session_state:
        st.session_state.manual_date_input = ""

    st.subheader("Today's Date")
    manual_date = st.text_input("Date", st.session_state.manual_date_input)
    st.session_state.manual_date_input = manual_date

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
                st.session_state.name_input = ""
                st.session_state.value_input = ""
                st.session_state.withdrawn_input = ""
                st.session_state.due_input = ""
                st.rerun()

            except ValueError:
                st.error("Please enter valid numbers.")
        else:
            st.warning("Please fill in at least date, name, and total.")

    if st.session_state.workers:
        display_df = pd.DataFrame(st.session_state.workers)
        date_row = pd.DataFrame([{
            "Worker": f"Date: {manual_date}",
            "Total": "",
            "Due": "",
            "Withdrawn": "",
            "Remaining": "",
            "Received": ""
        }])
        df_with_date = pd.concat([date_row, display_df], ignore_index=True)

        def highlight_negative_rows(row):
            color = '#ffcccc' if isinstance(row["Remaining"], (int, float)) and row["Remaining"] < 0 else ''
            return ['background-color: {}'.format(color)] * len(row)

        styled_df = df_with_date.style.apply(highlight_negative_rows, axis=1)
        st.markdown("### Table")
        st.dataframe(styled_df, use_container_width=True)

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

        if st.button("إرسال"):
            folder = "submissions"
            os.makedirs(folder, exist_ok=True)
            filepath = os.path.join(folder, f"{manual_date}.json")
            with open(filepath, "w") as f:
                json.dump(st.session_state.workers, f, indent=2)
            st.success(f"تم الإرسال باسم {manual_date}")
    else:
        st.info("No workers added yet.")

# واجهة المشرف
def admin_interface():
    st.title("CleanFoam - Admin Panel")
    folder = "submissions"
    os.makedirs(folder, exist_ok=True)
    files = [f for f in os.listdir(folder) if f.endswith(".json")]

    if not files:
        st.info("لا توجد بيانات مرسلة بعد.")
    else:
        selected_file = st.selectbox("اختر التاريخ", files)
        filepath = os.path.join(folder, selected_file)

        with open(filepath, "r") as f:
            data = json.load(f)

        df = pd.DataFrame(data)
        st.markdown(f"### البيانات من: **{selected_file.replace('.json', '')}**")

        for i in range(len(df)):
            received_key = f"received_{i}"
            df.at[i, "Received"] = st.checkbox(
                f"Received: {df.at[i, 'Worker']}", value=df.at[i]["Received"], key=received_key
            )

        if st.button("حفظ"):
            with open(filepath, "w") as f:
                json.dump(df.to_dict(orient="records"), f, indent=2)
            st.success("تم الحفظ بنجاح.")

        st.dataframe(df, use_container_width=True)

# تسجيل الدخول
def login():
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        if username == "M" and password == "12345":
            st.session_state.role = "user"
        elif username == "Admin" and password == "CF3010":
            st.session_state.role = "admin"
        else:
            st.sidebar.error("Invalid credentials")

# تحكم بتسجيل الدخول
if 'role' not in st.session_state:
    login()
else:
    if st.session_state.role == "user":
        user_interface()
    elif st.session_state.role == "admin":
        admin_interface()
