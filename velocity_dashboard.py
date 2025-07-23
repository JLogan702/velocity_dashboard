import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns

# Load Excel data
excel_file = "Velocity_Data.xlsx"
df = pd.read_excel(excel_file)

# Clean and sort
df = df.dropna(subset=["Team", "Sprint", "Committed", "Completed"])
df["Sprint"] = df["Sprint"].astype(str)
df["Velocity"] = df["Completed"] / df["Committed"]
df.sort_values(by=["Team", "Sprint"], inplace=True)

# App layout
st.set_page_config(page_title="Team Average Velocity Dashboard", layout="wide")

# Logo and Title
st.image("Clarvos_Logo2025_FullColor.png", width=200)
st.title("Team Average Velocity Dashboard")

# Select team
teams = df["Team"].unique()
selected_team = st.selectbox("Select a team", teams)

# Filter data
team_df = df[df["Team"] == selected_team]

# Line chart - Velocity over Sprints
st.subheader(f"Velocity Trend - {selected_team}")
fig1, ax1 = plt.subplots(figsize=(10, 4))
sns.lineplot(data=team_df, x="Sprint", y="Velocity", marker="o", ax=ax1)
ax1.set_ylim(0, 2)
ax1.axhline(1.0, ls="--", c="gray", label="Target Velocity")
ax1.set_ylabel("Velocity (Completed / Committed)")
ax1.set_xlabel("Sprint")
ax1.set_title("Velocity Over Time")
ax1.legend()
st.pyplot(fig1)

# Bar chart - Committed vs Completed
st.subheader(f"Committed vs Completed - {selected_team}")
fig2, ax2 = plt.subplots(figsize=(10, 4))
width = 0.35
x = range(len(team_df))
ax2.bar(x, team_df["Committed"], width, label="Committed", color="#5B8DEF")
ax2.bar([i + width for i in x], team_df["Completed"], width, label="Completed", color="#6DD3CE")
ax2.set_xticks([i + width / 2 for i in x])
ax2.set_xticklabels(team_df["Sprint"], rotation=45)
ax2.set_ylabel("Story Points")
ax2.set_title("Committed vs Completed Story Points")
ax2.legend()
st.pyplot(fig2)

# Data Table
st.subheader(f"Sprint Summary - {selected_team}")
st.dataframe(team_df[["Sprint", "Committed", "Completed", "Velocity"]].reset_index(drop=True))

