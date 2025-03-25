# 📈 AI Revenue Forecasting App with Prophet

This interactive Streamlit app allows users to upload an Excel file with `Date` and `Revenue` columns, generate revenue forecasts using Facebook's **Prophet** algorithm, and optionally receive **AI-generated FP&A commentary** powered by Groq's LLM.

---

## 🚀 Features

- ✅ Upload Excel file (.xlsx) with Date & Revenue columns
- 🔍 Automatically parses and cleans data
- 🔮 Forecasts revenue using Prophet
- 📊 Interactive Plotly charts
- 📋 Forecast results in tabular format
- 🤖 AI-generated FP&A commentary (optional with Groq API key)

---

## 📁 File Format Requirements

Your Excel file must include the following columns:

| Column  | Description                      |
|---------|----------------------------------|
| `Date`  | The date of the revenue record   |
| `Revenue` | The numeric revenue amount       |

---

## 🖥️ How to Run This App Locally

### 1. Clone the repository

```bash
git clone https://github.com/your-username/forecasting-app.git
cd forecasting-app
