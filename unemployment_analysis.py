# ============================================================
# Unemployment Analysis with Python
# CodeAlpha Data Science Internship - Task 2
# Author: Syed Muhammad Jawad
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# STEP 1: LOAD THE DATA
# ============================================================
df = pd.read_csv(r'C:\Users\kazmi\OneDrive\Documents\CodeAlpha_UnemploymentAnalysis\Unemployment in India.csv')

# Clean column names (remove extra spaces)
df.columns = df.columns.str.strip()

print("=== DATASET OVERVIEW ===")
print(f"Shape: {df.shape}")
print(f"\nFirst 5 rows:\n{df.head()}")
print(f"\nColumn Names: {list(df.columns)}")
print(f"\nData Types:\n{df.dtypes}")

# ============================================================
# STEP 2: DATA CLEANING
# ============================================================
# Convert Date column to datetime format
df['Date'] = pd.to_datetime(df['Date'].str.strip(), format='%d-%m-%Y')

# Check for missing values
print(f"\n=== MISSING VALUES ===")
print(df.isnull().sum())

# Drop rows with missing values
df.dropna(inplace=True)

# Rename columns for easier use
df.rename(columns={
    'Estimated Unemployment Rate (%)': 'Unemployment_Rate',
    'Estimated Employed': 'Employed',
    'Estimated Labour Participation Rate (%)': 'Labour_Participation_Rate'
}, inplace=True)

print(f"\nDataset after cleaning: {df.shape} rows")

# ============================================================
# STEP 3: BASIC STATISTICS
# ============================================================
print("\n=== BASIC STATISTICS ===")
print(df[['Unemployment_Rate', 'Employed', 'Labour_Participation_Rate']].describe())

# ============================================================
# STEP 4: VISUALIZATIONS
# ============================================================

sns.set_style("whitegrid")
fig, axes = plt.subplots(2, 2, figsize=(18, 14))
fig.suptitle('Unemployment Analysis in India\nCodeAlpha Data Science Internship — Syed Muhammad Jawad',
             fontsize=14, fontweight='bold', y=0.98)

# --- PLOT 1: Average Unemployment Rate Over Time ---
monthly_avg = df.groupby('Date')['Unemployment_Rate'].mean().reset_index()

axes[0, 0].plot(monthly_avg['Date'], monthly_avg['Unemployment_Rate'],
                color='steelblue', linewidth=2, marker='o', markersize=3)
axes[0, 0].axvline(pd.to_datetime('2020-03-01'), color='red',
                   linestyle='--', linewidth=1.5, label='COVID-19 Start (Mar 2020)')
axes[0, 0].set_title('Average Unemployment Rate Over Time', fontweight='bold')
axes[0, 0].set_xlabel('Date')
axes[0, 0].set_ylabel('Unemployment Rate (%)')
axes[0, 0].legend()
axes[0, 0].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
axes[0, 0].tick_params(axis='x', rotation=45)

# --- PLOT 2: COVID-19 Impact — Before vs During ---
pre_covid = df[df['Date'] < '2020-03-01']['Unemployment_Rate'].mean()
during_covid = df[df['Date'] >= '2020-03-01']['Unemployment_Rate'].mean()

bars = axes[0, 1].bar(['Pre-COVID\n(Before Mar 2020)', 'During COVID\n(Mar 2020 onwards)'],
                       [pre_covid, during_covid],
                       color=['green', 'crimson'], width=0.5, edgecolor='black')
axes[0, 1].set_title('COVID-19 Impact on Unemployment Rate', fontweight='bold')
axes[0, 1].set_ylabel('Average Unemployment Rate (%)')
for bar, val in zip(bars, [pre_covid, during_covid]):
    axes[0, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
                    f'{val:.2f}%', ha='center', fontweight='bold', fontsize=11)

# --- PLOT 3: Top 10 Regions by Unemployment Rate ---
top_regions = df.groupby('Region')['Unemployment_Rate'].mean().sort_values(ascending=False).head(10)

axes[1, 0].barh(top_regions.index, top_regions.values,
                color='steelblue', edgecolor='black')
axes[1, 0].set_title('Top 10 Regions by Average Unemployment Rate', fontweight='bold')
axes[1, 0].set_xlabel('Average Unemployment Rate (%)')
axes[1, 0].invert_yaxis()
axes[1, 0].margins(x=0.05)

# --- PLOT 4: Rural vs Urban Unemployment ---
area_avg = df.groupby('Area')['Unemployment_Rate'].mean()

axes[1, 1].pie(area_avg.values, labels=area_avg.index,
               autopct='%1.1f%%', colors=['#66b3ff', '#ff9999'],
               startangle=90, wedgeprops={'edgecolor': 'black'})
axes[1, 1].set_title('Rural vs Urban Unemployment Distribution', fontweight='bold')

plt.tight_layout(rect=[0, 0, 1, 0.95], h_pad=4, w_pad=3)
plt.savefig('unemployment_analysis.png', dpi=150, bbox_inches='tight')
plt.show()
print("\n✅ Chart saved as 'unemployment_analysis.png'")

# ============================================================
# STEP 5: KEY INSIGHTS
# ============================================================
print("\n=== KEY INSIGHTS ===")
print(f"1. Overall average unemployment rate: {df['Unemployment_Rate'].mean():.2f}%")
print(f"2. Pre-COVID average unemployment rate: {pre_covid:.2f}%")
print(f"3. During-COVID average unemployment rate: {during_covid:.2f}%")
print(f"4. COVID-19 increased unemployment by: {during_covid - pre_covid:.2f}%")
print(f"5. Highest unemployment region: {df.groupby('Region')['Unemployment_Rate'].mean().idxmax()}")
print(f"6. Lowest unemployment region: {df.groupby('Region')['Unemployment_Rate'].mean().idxmin()}")
print(f"7. Peak unemployment month: {monthly_avg.loc[monthly_avg['Unemployment_Rate'].idxmax(), 'Date'].strftime('%B %Y')}")
print(f"   Peak rate: {monthly_avg['Unemployment_Rate'].max():.2f}%")