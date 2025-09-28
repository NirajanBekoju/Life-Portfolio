import streamlit as st
import pandas as pd 
import db_handler
from utils import initialize_portfolio_data
st.set_page_config(page_title="Life Portfolio", layout="wide")

# Ensure table exists
db_handler.create_table()


email = 'nirajan.bekoju@gmail.com'
life_portfolio_df, last_created_date = initialize_portfolio_data(email)




st.title('Life Portfolio')
st.markdown('Fill in Importance Level, Satisfaction level, Average Hours spent in each SLUs per week')

st.markdown(f'**Last Submission Date : {last_created_date}**')

# Calculate dynamic height
row_height = 35
table_height = row_height * len(life_portfolio_df) + 50  # extra for header
## editable table
edited_life_portfolio_df = st.data_editor(
    life_portfolio_df, 
    num_rows='fixed',
    width="stretch",
    height=table_height,
    hide_index=True,
    column_config={
        "Importance Level": st.column_config.NumberColumn(
            "Importance Level", 
            help="Importance Level (0 to 10)",
            min_value=0, 
            max_value=10, 
            step=1, 
            format="%.0f"),
        "Satisfaction Level": st.column_config.NumberColumn(
            "Satisfaction Level", 
            help="Satisfaction Level (0 to 10)",
            min_value=0, 
            max_value=10, 
            step=1, 
            format="%.0f"),
        "Average Hours Spent in Week": st.column_config.NumberColumn(
            "Average Hours Spent in Week", 
            help="Average Hours (0 to 168)",
            min_value=0, 
            max_value=168, 
            step=1, 
            format="%.0f"),
    },
    disabled=['Strategic Life Areas(SLAs)', 'Strategic Life Units (SLUs)'],
)

confirm_save = st.checkbox("I confirm I want to save this table")
## save button
if confirm_save:
    if st.button('Save'):
        success = db_handler.save_dataframe(edited_life_portfolio_df, email)
        if success:
            st.success('Your table has been saved successfully')
        else:
            st.warning('Not Successful!')
    

