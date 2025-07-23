import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ----- Page Configuration -----
st.set_page_config(
    page_title="Clarvos | Team Average Velocity Dashboard",
    layout="wide"
)

# ----- Logo and Header -----
logo_path = "Clarvos_Logo2025_FullColor.png"
if os.path.exists(logo_path):
    st.image(logo_path, width=250)
st.title("📊 Team Average Velocity Dashboard")

# ----- File Upload or Default -----
uploaded_file = st.file_uploader("Upload your Sprint Velocity Excel file", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
else:
    default_file = "Sprint_Velocity_Per_Team.xlsx"
    if os.path.exists(default_file):
        df = pd.read_excel(default_file)
    else:
        st.error("No file uploaded and no default file found.")
        st.stop()

# ----- Sprint Name Mapping -----
SPRINT_NAME_MAP = {
    "Sprint 5": "Design Sprint 5: 5/7 - 5/21",
    "Sprint 6": "Design Sprint 6: 5/21 - 6/4",
    "Sprint 7": "Design Sprint 7: 6/4 - 6/18",
    "Sprint 8": "Design Sprint 8: 6/18 - 7/2",
    "Sprint 9": "Design Sprint 9: 7/2 - 7/16",
    "ML Ops Sprint": "Eng-ML Ops Sprint 7: 7/2 - 7/16",
    "Eng Sprint 6": "Eng-AIOps Sprint 6: 5/21 - 6/4",
    "Platform Sprint 5": "Eng-Platform Sprint 5: 5/7 - 5/21",
    "Platform Sprint 8": "Eng-Platform Sprint 8: 6/18 - 7/2",
    "Product Sprint 5": "Eng-Prod Sprint 5: 5/7 - 5/21"
}
df["Sprint"] = df["Sprint"].replace(SPRINT_NAME_MAP)

# ----- Compute Velocity Averages -----
avg_velocity_df = df.groupby("Team").agg(
    Avg_Velocity=("Velocity", "mean"),
    Sprint_Count=("Sprint", "count")
).reset_index().sort_values(by="Avg_Velocity", ascending=False)

# ----- Chart: Average Velocity per Team -----
st.subheader("📈 Average Velocity per Team")
fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.barplot(data=avg_velocity_df, x="Team", y="Avg_Velocity", palette="viridis", ax=ax1)
ax1.axhline(1.0, color="gray", linestyle="--", label="Target = 1.0")
ax1.set_ylabel("Average Velocity (Completed / Committed)")
ax1.set_ylim(0, max(avg_velocity_df["Avg_Velocity"].max() + 0.2, 1.5))
ax1.legend()
st.pyplot(fig1)

# ----- Chart: Sprint Count per Team -----
st.subheader("📊 Sprint Participation Volume")
fig2, ax2 = plt.subplots(figsize=(10, 4))
sns.barplot(data=avg_velocity_df, x="Team", y="Sprint_Count", palette="mako", ax=ax2)
ax2.set_ylabel("Sprint Count")
st.pyplot(fig2)

# ----- Chart: Velocity Distribution -----
st.subheader("📉 Velocity Distribution Across Teams and Sprints")
fig3, ax3 = plt.subplots(figsize=(10, 5))
sns.stripplot(data=df, x="Team", y="Velocity", hue="Sprint", jitter=True, dodge=True, alpha=0.8)
ax3.axhline(1.0, color="gray", linestyle="--", linewidth=1)
ax3.set_ylabel("Velocity")
ax3.set_title("Velocity by Team per Sprint")
st.pyplot(fig3)
