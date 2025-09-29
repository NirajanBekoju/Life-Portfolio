import streamlit as st
from db_handler import get_unique_submission_date, get_specific_portfolio_data
from utils import plot_life_portfolio

st.set_page_config(page_title="Life Portfolio", page_icon="📈")

email = 'nirajan.bekoju@gmail.com'
submission_date_list = get_unique_submission_date(email = email)


st.markdown("## Life Portfolio Visualization")
## select the submission dates
selected_date = st.selectbox("Select submission date:", submission_date_list, index = 0)
latest_portfolio_df = get_specific_portfolio_data(email = email, date = selected_date)

if latest_portfolio_df is None or latest_portfolio_df.empty:
    st.markdown(
        "✨ **Nothing to show here yet!**\n\n"
        "It looks like you don't have any portfolio data at the moment. "
        "Once you add some investments, you'll see them here."
    )
else:
    fig = plot_life_portfolio(latest_portfolio_df)
    st.plotly_chart(fig, use_container_width=False)


