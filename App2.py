import streamlit as st
import pandas as pd

def clean_number(n):
    return int(n) if n == int(n) else n

st.set_page_config(page_title="CleanFoam", page_icon="✅")
st.title("CleanFoam")

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
st.subheader("Add Worker")
name = st.text_input("Worker Name", st.session_state.name_input)
value = st.text_input("Enter the total :", st.session_state.value_input)
withdrawn = st.text_input("Enter the withdrawn:", st.session_state.withdrawn_input)
due_optional = st.text_input("Enter custom Due (optional):", st.session_state.due_input)
is_cf = st.checkbox("CF")

if st.button("OK"):
    if name and value:
        try:
            value_f = float(value)
            withdrawn_f = float(withdrawn) if withdrawn else 0
            due_custom = float(due_optional) if due_optional else None

            if is_cf:
                st.session_state.workers.append({
                    "Worker": name,
                    "Total": clean_number(value_f),
                    "Due": "",
                    "Withdrawn": "",
                    "Remaining": ""
                })
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

# Display Table and Summary
if st.session_state.workers:
    df = pd.DataFrame(st.session_state.workers)
    st.markdown("### Workers Table")
    st.dataframe(df, use_container_width=True)

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

    # Delete worker
    st.markdown("### Delete")
    worker_names = [w['Worker'] for w in st.session_state.workers]
    selected_worker = st.selectbox("Select worker to delete", worker_names)

    if st.button("Delete"):
        st.session_state.workers = [w for w in st.session_state.workers if w['Worker'] != selected_worker]
        st.success(f"Worker '{selected_worker}' has been deleted.")
        st.rerun()

else:
    st.info("No workers added yet.")
