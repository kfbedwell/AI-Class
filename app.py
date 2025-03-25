import streamlit as st
import pandas as pd
from prophet import Prophet
from prophet.plot import plot_plotly
import plotly.graph_objects as go
import os
from groq import Groq
from dotenv import load_dotenv

# Load API key securely
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

st.set_page_config(page_title="📈 Forecast with Prophet", layout="wide")
st.title("🔮 Revenue Forecasting App using Prophet")

# File Upload
uploaded_file = st.file_uploader("📤 Upload Excel File (with Date and Revenue columns)", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        # Validate columns
        if 'Date' not in df.columns or 'Revenue' not in df.columns:
            st.error("❌ Excel file must contain 'Date' and 'Revenue' columns.")
            st.stop()

        # Clean and rename
        df = df[['Date', 'Revenue']].dropna()
        df.columns = ['ds', 'y']
        df['ds'] = pd.to_datetime(df['ds'])

        # Display raw data
        st.subheader("📊 Uploaded Data")
        st.dataframe(df)

        # Forecast Horizon
        periods = st.slider("📅 Months to Forecast", 1, 24, 6)

        # Train Prophet model
        m = Prophet()
        m.fit(df)

        future = m.make_future_dataframe(periods=periods * 30)  # approximate month as 30 days
        forecast = m.predict(future)

        # Plot forecast
        st.subheader("📈 Forecasted Revenue")
        fig = plot_plotly(m, forecast)
        st.plotly_chart(fig, use_container_width=True)

        # Show forecast table
        st.subheader("📄 Forecast Table")
        st.dataframe(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(periods * 2))

        # Optional: AI Commentary
        if GROQ_API_KEY:
            with st.expander("🤖 Generate AI Commentary"):
                client = Groq(api_key=GROQ_API_KEY)

                data_for_ai = df.to_json(orient='records')
                prompt = f"""
                You are the Head of FP&A. Analyze the following revenue data and forecast:
                1. Key trends and inflection points.
                2. Business implications and drivers.
                3. Summary for CFO using Pyramid Principle.
                4. Actionable suggestions.
                Here's the JSON data: {data_for_ai}
                """

                response = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are a financial analyst and forecasting expert."},
                        {"role": "user", "content": prompt}
                    ],
                    model="llama3-8b-8192",
                )

                commentary = response.choices[0].message.content
                st.markdown("### 📖 AI-Generated Commentary")
                st.write(commentary)
        else:
            st.warning("🔐 GROQ_API_KEY not found. AI commentary disabled.")

    except Exception as e:
        st.error(f"Something went wrong: {e}")
