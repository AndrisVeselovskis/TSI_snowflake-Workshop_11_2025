import streamlit as st
import pandas as pd
import altair as alt
import snowflake.connector

st.title("🎓 Student Data Visualization (Snowflake + Streamlit)")

# ---------------------
# Snowflake credentials input
# ---------------------
st.sidebar.header("Snowflake Connection")
sf_user = st.sidebar.text_input("User")
sf_password = st.sidebar.text_input("Password", type="password")
sf_account = st.sidebar.text_input("Account")
sf_warehouse = st.sidebar.text_input("Warehouse", value="COMPUTE_WH")
sf_database = st.sidebar.text_input("Database", value="TSI_CLASSWORK_9")
sf_schema = st.sidebar.text_input("Schema", value="MY_SCHEMA")

# Connect only if all fields are filled
if sf_user and sf_password and sf_account and sf_warehouse and sf_database and sf_schema:
    try:
        conn = snowflake.connector.connect(
            user=sf_user,
            password=sf_password,
            account=sf_account,
            warehouse=sf_warehouse,
            database=sf_database,
            schema=sf_schema
        )

        query = "SELECT name, surname, id, age, faculty FROM student_data"
        df = pd.read_sql(query, conn)
        conn.close()

        st.subheader("📄 Raw Student Data")
        st.dataframe(df)

        # ---------------------
        # Age distribution
        # ---------------------
        st.subheader("📊 Age Distribution")
        age_chart = (
            alt.Chart(df)
            .mark_bar()
            .encode(
                x=alt.X("age:Q", bin=True),
                y="count()",
                tooltip=["age", "count()"]
            )
        )
        st.altair_chart(age_chart, use_container_width=True)

        # ---------------------
        # Faculty distribution
        # ---------------------
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

        st.success("✔ Visualization loaded successfully!")

    except Exception as e:
        st.error(f"❌ Connection failed: {e}")
else:
    st.info("Please enter all Snowflake credentials in the sidebar to connect.")
