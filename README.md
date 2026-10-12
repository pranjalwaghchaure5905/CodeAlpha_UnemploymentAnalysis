# Unemployment Analysis with Python

## CodeAlpha Data Science Internship – Task 2

### Project Overview
This project analyzes unemployment trends in India using Python and data visualization libraries. It explores unemployment rates across regions, monthly patterns, and changes during the COVID-19 period.

### Objectives
- Analyze unemployment data in India.
- Clean missing and duplicate data.
- Calculate summary statistics.
- Compare average unemployment rates across regions.
- Visualize monthly unemployment trends.
- Compare unemployment rates before and during the COVID-19 period.
- Explore month-wise average unemployment rates.

### Technologies Used
- Python
- Pandas
- Matplotlib
- Seaborn
- Visual Studio Code

### Dataset
The project uses `Unemployment in India.csv`, containing regional unemployment rates, estimated employment, labour participation rates, dates, and area information.

### Key Findings
- Overall average unemployment rate in the analyzed dataset: approximately 11.79%.
- Tripura has the highest regional average in this dataset: 28.35%.
- Meghalaya has the lowest regional average in this dataset: 4.80%.
- Average unemployment was 9.51% before the defined COVID-19 period and 17.77% during it.
- April has the highest month-wise average in this dataset: 23.64%.

These are descriptive findings from the available dataset and do not independently establish causation or recurring seasonal effects.

### Project Structure
```text
CodeAlpha_UnemploymentAnalysis/
├── dataset/
│   ├── Unemployment in India.csv
│   └── Unemployment_Rate_upto_11_2020.csv
├── outputs/
│   ├── rate_distribution.png
│   ├── regional_unemployment.png
│   ├── monthly_trend.png
│   ├── covid_comparison.png
│   ├── seasonal_analysis.png
│   └── cleaned_unemployment_data.csv
├── unemployment_analysis.py
└── README.md
```

### How to Run
1. Install Python.
2. Install the required libraries:
   `pip install pandas matplotlib seaborn`
3. Run the script:
   `python unemployment_analysis.py`

### Conclusion
This project demonstrates how Python can be used to clean, analyze, and visualize unemployment data. The visualizations help identify regional differences and patterns within the available dataset.