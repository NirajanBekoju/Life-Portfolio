import pandas as pd 
import random
import plotly.express as px
from db_handler import get_latest_portfolio_data
import streamlit as st

life_portfolio_columns = ['Strategic Life Areas(SLAs)', 'Strategic Life Units (SLUs)', 'Importance Level', 'Satisfaction Level', 'Average Hours Spent in Week']

SLA_SLU_dict = {
    "Relationships": [
        "Significant Other",
        "Family",
        "Friendship"
    ],
    "Body, Mind and Spirituality": [
        "Physical Health/Sports",
        "Mental Health/Mindfulness",
        "Spirituality/Faith"
    ],
    "Community and Society": [
        "Community/Citizenship",
        "Societal Engagement"
    ],
    "Job, Learning and Finances": [
        "Job/Career",
        "Education/Learning",
        "Finances"
    ],
    "Interests and Entertainment": [
        "Hobbies/Interests",
        "Online Entertainment",
        "Offline Entertainment"
    ],
    "Personal Care": [
        "Physiological Needs",
        "Activities of Daily Living"
    ]
}

def initialize_portfolio_data(email:str):
    latest_portfolio_df = get_latest_portfolio_data(email)
    if not latest_portfolio_df.empty:
        last_created_date = latest_portfolio_df['Created_Date'].iloc[0]
        latest_portfolio_df = latest_portfolio_df.drop(['Email', 'Created_Date'], axis=1)
        return latest_portfolio_df, last_created_date

    life_portfolio_data = []
    for sla, slus in SLA_SLU_dict.items():
        for slu in slus:
            life_portfolio_data.append([sla, slu, random.randint(0, 10), random.randint(0, 10), random.randint(0, 168)])

    life_portfolio_df = pd.DataFrame(life_portfolio_data, columns = life_portfolio_columns)
    return life_portfolio_df, None

def upload_portfolio_data_csv(label: str = "Upload your CSV file"):
    """
    Function to upload and read a CSV file in Streamlit.

    Parameters:
        label (str): The label shown on the upload widget.

    Returns:
        DataFrame or None: The uploaded CSV as a pandas DataFrame, or None if no file is uploaded.
    """
    uploaded_file = st.file_uploader(label, type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        if df.shape == (16, 3) and df.columns.tolist() == ['Importance Level', 'Satisfaction Level', 'Average Hours Spent in Week']:
            st.success("File uploaded successfully!")
            return df
        else:
            st.warning('CSV Validation Failed: The dataframe should contains 16 rows and 3 correct columns.')
    else:
        return None

def plot_life_portfolio(latest_portfolio_df, theme = 'dark'):
    """
    Creates and displays a Plotly scatter plot for the life portfolio data.
    
    Parameters:
        latest_portfolio_df (pd.DataFrame): DataFrame containing the latest life portfolio data.
    """


    life_portfolio_created_date = pd.to_datetime(latest_portfolio_df['Created_Date'].iloc[0])
    formatted_date = life_portfolio_created_date.strftime("%b %d, %Y")


    # Color mapping
    color_map = {
        "Relationships": "#FF6B6B",               
        "Body, Mind and Spirituality": "#4ECDC4",
        "Community and Society": "#FFD93D",       
        "Job, Learning and Finances": "#845EC2",
        "Interests and Entertainment": "#FF9671",
        "Personal Care": "#1A51E7"
    }

    # Create scatter plot
    fig = px.scatter(
        latest_portfolio_df,
        x="Satisfaction Level",
        y="Importance Level",
        size="Average Hours Spent in Week",
        color="Strategic Life Areas(SLAs)",
        hover_name="Strategic Life Units (SLUs)",
        size_max=40,
        title=f"Life Portfolio: Importance vs Satisfaction vs Time Spent <br>{formatted_date}",
        color_discrete_map=color_map,
        text="Strategic Life Units (SLUs)",
    )

    # Update traces for readability
    fig.update_traces(
        textposition="middle center",
        textfont=dict(size=12, color='white', family="Arial Black"),
        marker=dict(opacity=0.9, line=dict(width=1, color='DarkSlateGrey'))
    )

    # Add reference lines
    line_color = "white" if theme == 'dark' else "black"

    for x in [0, 5]:
        fig.add_shape(type="line", x0=x, y0=0, x1=x, y1=10, line=dict(color=line_color, width=2))
    for y in [0, 5]:
        fig.add_shape(type="line", x0=0, y0=y, x1=10, y1=y, line=dict(color=line_color, width=2))

    # Layout adjustments
    fig.update_layout(
        xaxis=dict(title="Satisfaction Level", range=[-0.9, 10.9]),
        yaxis=dict(title="Importance Level", range=[-0.9, 10.9]),
        legend_title="Strategic Life Areas",
        template="plotly_white",
        height=900,
        width = 1200,
    )

    return fig