import streamlit as st

def clean_number(n):
    return int(n) if n == int(n) else n

st.set_page_config(page_title="Worker Payment Calculator", page_icon="💰")
st.title("Worker Payment Calculator")

value = st.number_input("Enter the total :", step=1.0, format="%.2f")
withdrawn = st.number_input("Enter the withdrawn:", step=1.0, format="%.2f")

if st.button("Calculate"):
    half_value = value / 2
    after_withdraw = half_value - withdrawn

    if half_value == 40:
        fee = 20
    elif half_value == 45:
        fee = 22.5
    elif half_value == 50:
        fee = 25
    elif half_value == 55:
        fee = 27.5
    elif value == 95:
        fee = 22.5
    elif int(value) % 10 == 5:
        fee = 32.5
    else:
        fee = 30

    final_amount = after_withdraw - fee

    st.markdown("### Result")
    st.write(f"**Total :** {clean_number(value)}")
    st.write(f"**Due :** {clean_number(fee)}")
    st.write(f"**Withdrawn :** {clean_number(withdrawn)}")
    st.write(f"**Remaining :** {clean_number(final_amount)}")
