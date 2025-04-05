import streamlit as st
import pandas as pd

def clean_number(n):
    return int(n) if n == int(n) else n

st.set_page_config(page_title="Workers Payment Calculator", page_icon="✅")
st.title("Workers Payment Calculator")

# Initialize session state
if 'workers' not in st.session_state:
    st.session_state.workers = []

# Input fields (بدون key في النصوص)
st.subheader("Add New Worker")
name = st.text_input("Worker Name")
value = st.text_input("Enter the total :")
withdrawn = st.text_input("Enter the withdrawn:")

# OK Button
if st.button("OK"):
    if name and value and withdrawn:
        try:
            value_f = float(value)
            withdrawn_f = float(withdrawn)

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

            # Add worker to list
            st.session_state.workers.append({
                "Worker": name,
                "Total": clean_number(value_f),
                "Due": clean_number(fee),
                "Withdrawn": clean_number(withdrawn_f),
                "Remaining": clean_number(final_amount)
            })

            # Refresh page to clear inputs
            st.experimental_rerun()

        except ValueError:
            st.error("Please enter valid numbers.")
    else:
        st.warning("Please fill in all fields before pressing OK.")

# Show current workers table
if st.session_state.workers:
    st.markdown("### Workers Table")
    df = pd.DataFrame(st.session_state.workers)
    st.dataframe(df, use_container_width=True)

    # Show total of all "Total" values
    total_sum = sum([w['Total'] for w in st.session_state.workers])
    st.markdown(f"### Total of All Workers: **{clean_number(total_sum)}**")
else:
    st.info("No workers added yet.")
