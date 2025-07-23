import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(page_title="Team Velocity Dashboard", layout="wide")
st.title("🚀 Team Sprint Velocity Dashboard")

# Load data: use uploaded file if provided, otherwise load default
uploaded_file = st.file_uploader("📤 Upload your Sprint Velocity Excel file", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    st.success("✅ File uploaded successfully!")
else:
    default_file = "Sprint_Velocity_Per_Team.xlsx"
    if os.path.exists(default_file):
        st.info("📎 No upload detected. Using default sample file.")
        df = pd.read_excel(default_file)
    else:
        st.error("❌ No file uploaded and no default file found. Please upload a valid .xlsx file.")
        st.stop()

# Show raw data
st.subheader("📄 Raw Velocity Data")
st.dataframe(df)

# Compute average velocity
avg_velocity_df = df.groupby("Team").agg(
    Avg_Velocity=("Velocity", "mean"),
    Sprint_Count=("Sprint", "count")
).reset_index().sort_values(by="Avg_Velocity", ascending=False)

# Plot bar chart
st.subheader("📊 Average Velocity per Team (Last 3 Sprints)")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=avg_velocity_df, x="Team", y="Avg_Velocity", palette="coolwarm", ax=ax)
ax.axhline(1.0, color="gray", linestyle="--", label="Target Velocity = 1.0")
ax.set_ylabel("Avg Velocity (Completed / Committed)")
ax.set_title("Team Average Velocity")
ax.set_ylim(0, max(avg_velocity_df["Avg_Velocity"].max() + 0.2, 1.5))
ax.legend()
st.pyplot(fig)

# Show summary table
st.dataframe(avg_velocity_df.style.format({"Avg_Velocity": "{:.2f}"}))

# Download buttons
csv_summary = avg_velocity_df.to_csv(index=False).encode("utf-8")
csv_raw = df.to_csv(index=False).encode("utf-8")

st.download_button("📥 Download Summary CSV", data=csv_summary, file_name="average_velocity_summary.csv", mime="text/csv")
st.download_button("📥 Download Raw Data CSV", data=csv_raw, file_name="raw_velocity_data.csv", mime="text/csv")
