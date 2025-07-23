import pandas as pd
import matplotlib.pyplot as plt
import base64
import streamlit as st
from datetime import datetime

# Load the spreadsheet
df = pd.read_excel("Velocity_Data.xlsx")

# Clean and convert dates
df['Start Date'] = pd.to_datetime(df['Start Date'], errors='coerce')
df['End Date'] = pd.to_datetime(df['End Date'], errors='coerce')

# Hardcoded sprint names from visuals
sprint_name_mapping = {
    "Data Sprint 7": "Data Sprint 7 – 6/4–6/18",
    "Data Sprint 8": "Data Sprint 8 – 6/18–7/2",
    "Data Sprint 9": "Data Sprint 9 – 7/2–7/16",
    "Eng-Platform Sprint 7": "Eng-Platform Sprint 7 – 6/4–6/18",
    "Eng-Platform Sprint 8": "Eng-Platform Sprint 8 – 6/18–7/2",
    "Eng-Platform Sprint 9": "Eng-Platform Sprint 9 – 7/2–7/16",
    "Eng-Prod Sprint 8": "Eng-Prod Sprint 8 – 6/18–7/7",
    "Eng-Prod Sprint 9": "Eng-Prod Sprint 9 – 7/8–7/15",
    "Eng-AIOps Sprint 7": "Eng-AIOps Sprint 7 – 6/4–6/18",
    "Eng-AIOps Sprint 8": "Eng-AIOps Sprint 8 – 6/18–7/2",
    "Eng-AIOps Sprint 9": "Eng-AIOps Sprint 9 – 7/2–7/16",
    "Design Sprint 7": "Design Sprint 7 – 6/4–6/18",
    "Design Sprint 8": "Design Sprint 8 – 6/18–7/2",
    "Design Sprint 9": "Design Sprint 9 – 7/2–7/16",
}

df["Sprint Display"] = df["Sprint Name"].map(sprint_name_mapping)
df = df.sort_values(by=["Team Name", "Start Date"])

# Streamlit UI
st.set_page_config(page_title="Team Average Velocity Dashboard", layout="wide")
st.image("Clarvos_Logo2025_FullColor.png", width=200)
st.title("Team Average Velocity Dashboard")
st.markdown("Compare Story Points *Committed vs Completed* across teams and sprints.")

# Plot by team
teams = df["Team Name"].unique()
for team in teams:
    team_df = df[df["Team Name"] == team]

    fig, ax = plt.subplots(figsize=(10, 4))
    index = range(len(team_df))
    bar_width = 0.35

    ax.bar(index, team_df["Story Points Committed"], bar_width, label="Committed")
    ax.bar(
        [i + bar_width for i in index],
        team_df["Story Points Completed"],
        bar_width,
        label="Completed",
    )

    ax.set_xlabel("Sprint")
    ax.set_ylabel("Story Points")
    ax.set_title(f"{team} Velocity")
    ax.set_xticks([i + bar_width / 2 for i in index])
    ax.set_xticklabels(team_df["Sprint Display"], rotation=45, ha="right")
    ax.legend()

    st.pyplot(fig)

# Table
st.markdown("### 📊 Full Velocity Table")
st.dataframe(df[["Team Name", "Sprint Display", "Story Points Committed", "Story Points Completed"]])

# CSV Download
csv = df.to_csv(index=False)
b64 = base64.b64encode(csv.encode()).decode()
st.markdown(
    f"⬇️ [Download full data as CSV](data:file/csv;base64,{b64})",
    unsafe_allow_html=True,
)

