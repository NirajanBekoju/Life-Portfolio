import pandas as pd 

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


life_portfolio_data = []
for sla, slus in SLA_SLU_dict.items():
    for slu in slus:
        life_portfolio_data.append([sla, slu, 0, 0, 0])



life_portfolio_df = pd.DataFrame(life_portfolio_data, columns = life_portfolio_columns)