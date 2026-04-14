from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from scipy import stats

st.set_page_config(
    page_title="Assignment 4 - Bitcoin Response Analysis",
    layout="wide",
)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "gold" / "crypto_sentiment_daily_extended.csv"


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_FILE)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    numeric_cols = [
        "btc_close",
        "btc_volume",
        "btc_daily_return",
        "fear_greed_value",
        "holiday_flag",
        "positive_return",
        "is_weekend",
        "non_working_day_flag",
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def safe_group(df: pd.DataFrame, flag_col: str, value_col: str, flag_value: int) -> pd.Series:
    return df.loc[df[flag_col] == flag_value, value_col].dropna()


st.title("Assignment 4: Bitcoin + Fear & Greed Statistical Analysis App")

st.markdown(
    """
This app extends the Assignment 3 Gold dataset by adding a **holiday calendar** joined on **date**.
The goal is to explore whether Bitcoin returns and response patterns differ across working and non-working days,
and whether the **Fear & Greed Index** is associated with market returns.
"""
)

try:
    df = load_data()
except FileNotFoundError:
    st.error(
        "Final dataset not found. First run:\n\n"
        "`python transform/prepare_assignment4_data.py`\n\n"
        "Expected file:\n"
        "`data/gold/crypto_sentiment_daily_extended.csv`"
    )
    st.stop()

if df.empty:
    st.warning("The dataset is empty.")
    st.stop()

st.header("1. Project Overview / Data Story")
st.write(
    """
- **Original Assignment 3 dataset:** Bitcoin market data from Binance + Fear & Greed sentiment data
- **New external source added:** Holiday calendar dataset
- **Join key:** `date`
- **Main question:** Are Bitcoin return patterns different on working vs non-working days, and how is sentiment related to returns?
"""
)

st.header("2. Data Preview")
st.subheader("Sample of Final Dataset")
st.dataframe(df.head(), use_container_width=True)

st.subheader("Summary Statistics")
st.dataframe(df.describe(include="all"), use_container_width=True)

st.subheader("Important Variables")
st.markdown(
    """
- `btc_daily_return`: daily Bitcoin return  
- `fear_greed_value`: sentiment score  
- `holiday_flag`: 1 if holiday, 0 otherwise  
- `positive_return`: 1 if return > 0, 0 otherwise  
- `non_working_day_flag`: 1 if weekend or holiday, 0 otherwise  
"""
)

st.header("3. Visual Storytelling")

min_date = df["date"].min()
max_date = df["date"].max()

selected_dates = st.slider(
    "Select date range",
    min_value=min_date.to_pydatetime(),
    max_value=max_date.to_pydatetime(),
    value=(min_date.to_pydatetime(), max_date.to_pydatetime()),
)


filtered_df = df[
    (df["date"] >= pd.Timestamp(selected_dates[0])) &
    (df["date"] <= pd.Timestamp(selected_dates[1]))
].copy()

if "non_working_day_flag" not in filtered_df.columns:
    filtered_df["non_working_day_flag"] = (
        (filtered_df["is_weekend"].fillna(0).astype(int) == 1) |
        (filtered_df["holiday_flag"].fillna(0).astype(int) == 1)
    ).astype(int)
col1, col2 = st.columns(2)

with col1:
    st.subheader("BTC Daily Return Over Time")
    fig1, ax1 = plt.subplots(figsize=(8, 4))
    ax1.plot(filtered_df["date"], filtered_df["btc_daily_return"])
    ax1.set_xlabel("Date")
    ax1.set_ylabel("BTC Daily Return")
    ax1.set_title("Time Series of Bitcoin Daily Return")
    plt.xticks(rotation=45)
    st.pyplot(fig1)

with col2:
    st.subheader("Fear & Greed Value Over Time")
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    ax2.plot(filtered_df["date"], filtered_df["fear_greed_value"])
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Fear & Greed Value")
    ax2.set_title("Time Series of Fear & Greed Sentiment")
    plt.xticks(rotation=45)
    st.pyplot(fig2)

col3, col4 = st.columns(2)

with col3:
    st.subheader("BTC Return by Working vs Non-Working Day")
    g_working = safe_group(filtered_df, "non_working_day_flag", "btc_daily_return", 0)
    g_non_working = safe_group(filtered_df, "non_working_day_flag", "btc_daily_return", 1)

    fig3, ax3 = plt.subplots(figsize=(8, 4))
    plot_data = []
    labels = []

    if len(g_working) > 0:
        plot_data.append(g_working)
        labels.append("Working Day")
    if len(g_non_working) > 0:
        plot_data.append(g_non_working)
        labels.append("Non-Working Day")

    if plot_data:
        ax3.boxplot(plot_data, labels=labels)
        ax3.set_ylabel("BTC Daily Return")
        ax3.set_title("Grouped Return Distribution")
        st.pyplot(fig3)
    else:
        st.info("Not enough data to draw grouped boxplot.")

with col4:
    st.subheader("Fear & Greed vs BTC Daily Return")
    scatter_df = filtered_df[["fear_greed_value", "btc_daily_return"]].dropna()

    if len(scatter_df) > 1:
        fig4, ax4 = plt.subplots(figsize=(8, 4))
        ax4.scatter(scatter_df["fear_greed_value"], scatter_df["btc_daily_return"])
        ax4.set_xlabel("Fear & Greed Value")
        ax4.set_ylabel("BTC Daily Return")
        ax4.set_title("Correlation Scatterplot")
        st.pyplot(fig4)
    else:
        st.info("Not enough data for scatterplot.")

st.subheader("Positive Return Counts by Non-Working Day")
count_table = pd.crosstab(filtered_df["positive_return"], filtered_df["non_working_day_flag"])

if not count_table.empty:
    fig5, ax5 = plt.subplots(figsize=(7, 4))
    count_table.T.plot(kind="bar", ax=ax5)
    ax5.set_xlabel("Non-Working Day Flag")
    ax5.set_ylabel("Count")
    ax5.set_title("Categorical Count Plot")
    ax5.legend(title="Positive Return")
    st.pyplot(fig5)
else:
    st.info("Not enough categorical data for count chart.")

st.header("4. Hypothesis Testing")

test_option = st.selectbox(
    "Choose an analysis",
    [
        "One-sample t-test: mean BTC return vs 0",
        "Two-sample t-test: working vs non-working day returns",
        "Chi-square: positive_return vs non_working_day_flag",
        "Variance comparison: working vs non-working day returns",
        "Correlation: fear_greed_value vs btc_daily_return",
    ],
)

if test_option == "One-sample t-test: mean BTC return vs 0":
    sample = filtered_df["btc_daily_return"].dropna()

    st.markdown("**Null hypothesis (H0):** Mean BTC daily return = 0")
    st.markdown("**Alternative hypothesis (H1):** Mean BTC daily return ≠ 0")

    if len(sample) < 2:
        st.warning("Not enough data for one-sample t-test.")
    else:
        t_stat, p_val = stats.ttest_1samp(sample, 0)
        st.write(f"**t-statistic:** {t_stat:.4f}")
        st.write(f"**p-value:** {p_val:.4f}")
        st.write("**Why this test fits:** It compares one continuous sample against a benchmark value of 0.")
        st.write("**Interpretation:** A small p-value suggests the average daily return is statistically different from zero.")
        st.write("**Limitation:** With a small date range, results may not generalize well.")

elif test_option == "Two-sample t-test: working vs non-working day returns":
    g1 = safe_group(filtered_df, "non_working_day_flag", "btc_daily_return", 0)
    g2 = safe_group(filtered_df, "non_working_day_flag", "btc_daily_return", 1)

    st.markdown("**Null hypothesis (H0):** Mean return is the same for working and non-working days")
    st.markdown("**Alternative hypothesis (H1):** Mean return is different between the two groups")

    if len(g1) < 2 or len(g2) < 2:
        st.warning("Not enough data in one or both groups for two-sample t-test.")
    else:
        t_stat, p_val = stats.ttest_ind(g1, g2, equal_var=False)
        st.write(f"**t-statistic:** {t_stat:.4f}")
        st.write(f"**p-value:** {p_val:.4f}")
        st.write("**Why this test fits:** It compares a continuous variable across two independent groups.")
        st.write("**Interpretation:** A small p-value suggests average returns differ across the two day types.")
        st.write("**Limitation:** Crypto markets trade 24/7, so holiday effects may be weak.")

elif test_option == "Chi-square: positive_return vs non_working_day_flag":
    contingency = pd.crosstab(filtered_df["positive_return"], filtered_df["non_working_day_flag"])

    st.markdown("**Null hypothesis (H0):** Positive return is independent of non-working day status")
    st.markdown("**Alternative hypothesis (H1):** Positive return is associated with non-working day status")

    if contingency.shape[0] < 2 or contingency.shape[1] < 2:
        st.warning("Not enough category variation for chi-square test.")
    else:
        chi2, p_val, dof, expected = stats.chi2_contingency(contingency)
        st.write("**Contingency Table:**")
        st.dataframe(contingency, use_container_width=True)
        st.write(f"**Chi-square statistic:** {chi2:.4f}")
        st.write(f"**p-value:** {p_val:.4f}")
        st.write("**Why this test fits:** Both variables are categorical.")
        st.write("**Interpretation:** A small p-value suggests that positive-return frequency may differ by day type.")
        st.write("**Limitation:** Small expected counts can weaken reliability.")

elif test_option == "Variance comparison: working vs non-working day returns":
    g1 = safe_group(filtered_df, "non_working_day_flag", "btc_daily_return", 0)
    g2 = safe_group(filtered_df, "non_working_day_flag", "btc_daily_return", 1)

    st.markdown("**Question:** Is return variability different between working and non-working days?")

    if len(g1) < 2 or len(g2) < 2 or g2.var(ddof=1) == 0:
        st.warning("Not enough data for variance comparison.")
    else:
        f_stat = g1.var(ddof=1) / g2.var(ddof=1)
        st.write(f"**F-statistic:** {f_stat:.4f}")
        st.write("**Why this test fits:** It compares the spread or volatility of returns across two groups.")
        st.write("**Interpretation:** Values far from 1 suggest group variability may differ.")
        st.write("**Limitation:** This is sensitive to outliers and non-normality.")

elif test_option == "Correlation: fear_greed_value vs btc_daily_return":
    subset = filtered_df[["fear_greed_value", "btc_daily_return"]].dropna()

    st.markdown("**Null hypothesis (H0):** No linear relationship between Fear & Greed and BTC daily return")
    st.markdown("**Alternative hypothesis (H1):** A linear relationship exists")

    if len(subset) < 3:
        st.warning("Not enough data for correlation analysis.")
    else:
        corr, p_val = stats.pearsonr(subset["fear_greed_value"], subset["btc_daily_return"])
        st.write(f"**Correlation coefficient:** {corr:.4f}")
        st.write(f"**p-value:** {p_val:.4f}")
        st.write("**Why this test fits:** Both variables are quantitative.")
        st.write("**Interpretation:** Correlation near 1 or -1 indicates a stronger linear relationship.")
        st.write("**Limitation:** Correlation does not imply causation.")

st.header("5. Reflection / Limitations")
st.markdown(
    """
- The analysis uses a short dataset, so statistical power is limited.  
- Holiday effects may be weak because Bitcoin trades continuously.  
- Statistical significance does not automatically imply practical importance.  
- Join quality depends on clean and matching date formats.  
- Outliers in returns can affect t-tests, variance comparison, and correlation.  
"""
)