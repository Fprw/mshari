import streamlit as st

def clean_number(n):
    return int(n) if n == int(n) else n

st.set_page_config(page_title="Worker Payment Calculator", page_icon="💰")
st.title("Worker Payment Calculator")

value = st.text_input("Enter the total :")
withdrawn = st.text_input("Enter the withdrawn:")

if st.button("Calculate"):
    if value and withdrawn:
        try:
            value = float(value)
            withdrawn = float(withdrawn)

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

            # بناء الجدول بـ HTML لتنسيق النص في الوسط وجعله عريض
            table_html = f"""
            <style>
                table {{
                    width: 100%;
                    border-collapse: collapse;
                }}
                th, td {{
                    text-align: center;
                    padding: 10px;
                    font-weight: bold;
                    border-bottom: 1px solid #ddd;
                }}
            </style>
            <table>
                <tr><th>Label</th><th>Value</th></tr>
                <tr><td>Total</td><td>{clean_number(value)}</td></tr>
                <tr><td>Due</td><td>{clean_number(fee)}</td></tr>
                <tr><td>Withdrawn</td><td>{clean_number(withdrawn)}</td></tr>
                <tr><td>Remaining</td><td>{clean_number(final_amount)}</td></tr>
            </table>
            """

            st.markdown("### Result")
            st.markdown(table_html, unsafe_allow_html=True)

        except ValueError:
            st.error("Please enter valid numbers.")
    else:
        st.warning("Please fill in both fields before calculating.")
