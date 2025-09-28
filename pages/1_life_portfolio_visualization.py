import streamlit as st
from db_handler import get_latest_data
from utils import plot_life_portfolio

st.set_page_config(page_title="Life Portfolio", page_icon="📈")

email = 'nirajan.bekoju@gmail.com'


st.markdown("## Life Portfolio Visualization")
## get latest life portfolio data and plot them

latest_portfolio_df = get_latest_data(email)
if latest_portfolio_df is None or latest_portfolio_df.empty:
    st.markdown(
        "✨ **Nothing to show here yet!**\n\n"
        "It looks like you don't have any portfolio data at the moment. "
        "Once you add some investments, you'll see them here."
    )
else:
    fig = plot_life_portfolio(latest_portfolio_df)
    st.plotly_chart(fig, use_container_width=False)


