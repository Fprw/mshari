import streamlit as st
import pandas as pd

def clean_number(n):
    return int(n) if n == int(n) else n

st.set_page_config(page_title="CleanFoam", page_icon="✅")
st.title("CleanFoam")

# Initialize session state
if 'workers' not in st.session_state:
    st.session_state.workers = []
if 'name_input' not in st.session_state:
    st.session_state.name_input = ""
if 'value_input' not in st.session_state:
    st.session_state.value_input = ""
if 'withdrawn_input' not in st.session_state:
    st.session_state.withdrawn_input = ""

# Input fields
st.subheader("Add New Worker")
name = st.text_input("Worker Name", st.session_state.name_input, key="name_input_key")
value = st.text_input("Enter the total :", st.session_state.value_input, key="value_input_key")
withdrawn = st.text_input("Enter the withdrawn:", st.session_state.withdrawn_input, key="withdrawn_input_key")

# OK Button
if st.button("OK"):
    if name and value and withdrawn:
        try:
            value_f = float(value)
            withdrawn_f = float(withdrawn)

            half_value = value_f / 2
            after_withdraw = half_value - withdrawn_f

            # Updated fee logic with new conditions
            if half_value == 40:
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

            # Add to workers
            st.session_state.workers.append({
                "Worker": name,
                "Total": clean_number(value_f),
                "Due": clean_number(fee),
                "Withdrawn": clean_number(withdrawn_f),
                "Remaining": clean_number(final_amount)
            })

            # Clear input fields
            st.session_state.name_input = ""
            st.session_state.value_input = ""
            st.session_state.withdrawn_input = ""

            # Manually clear visible inputs
            st.experimental_set_query_params()  # optional to reset URL state
            st.rerun()

        except ValueError:
            st.error("Please enter valid numbers.")
    else:
        st.warning("Please fill in all fields before pressing OK.")

# Display table
if st.session_state.workers:
    st.markdown("### Workers Table")
    df = pd.DataFrame(st.session_state.workers)
    st.dataframe(df, use_container_width=True)

    total_sum = sum([w['Total'] for w in st.session_state.workers])
    st.markdown(f"### Total of All Workers: **{clean_number(total_sum)}**")
else:
    st.info("No workers added yet.")
