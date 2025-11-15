import streamlit as st
import pandas as pd
import snowflake.connector
import altair as alt

st.title("🎓 Student Data Visualization")
st.write("Interactive charts from Snowflake table `student_data`")

# --- Snowflake connection ---
conn = snowflake.connector.connect(
    user=st.secrets["snowflake"]["user"],
    password=st.secrets["snowflake"]["password"],
    account=st.secrets["snowflake"]["account"],
    warehouse="COMPUTE_WH",
    database="TSI_CLASSWORK_9",
    schema="MY_SCHEMA"
)

query = "SELECT name, surname, id, age, faculty FROM student_data"
df = pd.read_sql(query, conn)

st.subheader("📄 Raw Data")
st.dataframe(df)

# --- Age distribution ---
st.subheader("📊 Age Distribution")

age_chart = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x="age:Q",
        y="count()",
        tooltip=["age", "count()"]
    )
)
st.altair_chart(age_chart, use_container_width=True)

# --- Faculty distribution ---
st.subheader("🏫 Students per Faculty")

faculty_chart = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x="faculty:N",
        y="count()",
        tooltip=["faculty", "count()"]
    )
)
st.altair_chart(faculty_chart, use_container_width=True)

st.success("Visualization loaded successfully 🎉")
