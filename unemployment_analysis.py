import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Project folders
DATA_FOLDER = "dataset"
OUTPUT_FOLDER = "outputs"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Load the main dataset
file_path = os.path.join(DATA_FOLDER, "Unemployment in India.csv")
df = pd.read_csv(file_path)

print("=" * 60)
print("       UNEMPLOYMENT ANALYSIS IN INDIA")
print("=" * 60)

# Clean column names
df.columns = df.columns.str.strip()

# Display basic information
print("\nDataset Shape:", df.shape)
print("\nColumn Names:")
print(df.columns.tolist())

print("\nFirst 5 Rows:")
print(df.head())

print("\nMissing Values Before Cleaning:")
print(df.isnull().sum())

# Clean text columns
for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].str.strip()

# Convert date column if available
if " Date" in df.columns:
    df.rename(columns={" Date": "Date"}, inplace=True)

if "Date" in df.columns:
    df["Date"] = pd.to_datetime(
        df["Date"], dayfirst=True, errors="coerce"
    )

# Remove completely empty rows and duplicates
df.dropna(how="all", inplace=True)
df.drop_duplicates(inplace=True)

# Convert numeric columns
for col in ["Estimated Unemployment Rate (%)",
            "Estimated Employed",
            "Estimated Labour Participation Rate (%)"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

print("\nMissing Values After Cleaning:")
print(df.isnull().sum())

# Identify important columns
rate_col = "Estimated Unemployment Rate (%)"
region_col = "Region"

if rate_col not in df.columns:
    raise ValueError(
        f"Expected column '{rate_col}' not found. "
        f"Available columns: {df.columns.tolist()}"
    )

# Summary statistics
print("\nUnemployment Rate Summary:")
print(df[rate_col].describe())

# 1. Unemployment rate distribution
plt.figure(figsize=(9, 5))
sns.histplot(df[rate_col].dropna(), bins=20, kde=True)
plt.title("Distribution of Unemployment Rates in India")
plt.xlabel("Unemployment Rate (%)")
plt.ylabel("Number of Observations")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_FOLDER, "rate_distribution.png"))
plt.close()

# 2. Average unemployment rate by region
if region_col in df.columns:
    region_avg = (
        df.groupby(region_col)[rate_col]
        .mean()
        .sort_values(ascending=False)
    )

    print("\nAverage Unemployment Rate by Region:")
    print(region_avg.round(2))

    plt.figure(figsize=(12, 7))
    region_avg.sort_values().plot(kind="barh")
    plt.title("Average Unemployment Rate by Region")
    plt.xlabel("Average Unemployment Rate (%)")
    plt.ylabel("Region")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_FOLDER, "regional_unemployment.png"))
    plt.close()

# 3. Monthly trend
if "Date" in df.columns:
    dated_df = df.dropna(subset=["Date", rate_col]).copy()
    dated_df["Month"] = dated_df["Date"].dt.to_period("M").dt.to_timestamp()

    monthly_avg = dated_df.groupby("Month")[rate_col].mean()

    plt.figure(figsize=(12, 5))
    plt.plot(monthly_avg.index, monthly_avg.values, marker="o")
    plt.title("Monthly Unemployment Rate Trend in India")
    plt.xlabel("Month")
    plt.ylabel("Average Unemployment Rate (%)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_FOLDER, "monthly_trend.png"))
    plt.close()

    # 4. COVID-19 comparison
    dated_df["Period"] = dated_df["Date"].apply(
        lambda date: "Before COVID-19"
        if date < pd.Timestamp("2020-03-01")
        else "COVID-19 Period"
    )

    covid_avg = dated_df.groupby("Period")[rate_col].mean()

    print("\nCOVID-19 Period Comparison:")
    print(covid_avg.round(2))

    plt.figure(figsize=(7, 5))
    covid_avg.plot(kind="bar")
    plt.title("Average Unemployment: Before vs COVID-19")
    plt.xlabel("Period")
    plt.ylabel("Average Unemployment Rate (%)")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_FOLDER, "covid_comparison.png"))
    plt.close()

# Save cleaned data
df.to_csv(os.path.join(OUTPUT_FOLDER, "cleaned_unemployment_data.csv"),
          index=False)




# 5. Month-wise unemployment analysis
if "Date" in df.columns:
    seasonal_df = df.dropna(subset=["Date", rate_col]).copy()

    seasonal_df["Month_Name"] = seasonal_df["Date"].dt.month_name()
    seasonal_df["Month_Number"] = seasonal_df["Date"].dt.month

    month_avg = (
        seasonal_df.groupby(["Month_Number", "Month_Name"])[rate_col]
        .mean()
        .reset_index()
        .sort_values("Month_Number")
    )

    print("\nMonth-wise Average Unemployment Rate:")
    print(month_avg[["Month_Name", rate_col]].round(2).to_string(index=False))

    plt.figure(figsize=(11, 5))
    sns.barplot(data=month_avg, x="Month_Name", y=rate_col)
    plt.title("Month-wise Average Unemployment Rate in India")
    plt.xlabel("Month")
    plt.ylabel("Average Unemployment Rate (%)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_FOLDER, "seasonal_analysis.png"))
    plt.close()

    highest_month = month_avg.loc[month_avg[rate_col].idxmax()]
    lowest_month = month_avg.loc[month_avg[rate_col].idxmin()]

    print(f"\nHighest average: {highest_month['Month_Name']} "
          f"({highest_month[rate_col]:.2f}%)")
    print(f"Lowest average: {lowest_month['Month_Name']} "
          f"({lowest_month[rate_col]:.2f}%)")

    print(
        "\nNote: Month-wise differences indicate patterns in this dataset. "
        "They do not prove a recurring seasonal effect."
    )

print("\nAnalysis completed successfully!")
print("Check the 'outputs' folder for graphs and cleaned data.")
