"""
Weather Data Analysis and Visualization Module

This module provides comprehensive tools for analyzing and visualizing historical weather data.
It includes data preprocessing, statistical analysis, and various visualization techniques.

Author: RA-fi
Date: February 2026
Version: 1.0.0
"""

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from typing import Tuple, Optional

warnings.filterwarnings("ignore")

# Configuration
DATA_FILE = "EnglandWeather.csv"
FILTERED_DATA_FILE = "filtered_data.csv"
FILLED_DATA_FILE = "filled_data.csv"
FIGURE_DIR = "Figure"
MONTH_NAMES = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]
SEASON_MAP = {
    "March": "Spring", "April": "Spring", "May": "Spring",
    "June": "Summer", "July": "Summer", "August": "Summer",
    "September": "Fall", "October": "Fall", "November": "Fall",
    "December": "Winter", "January": "Winter", "February": "Winter"
}

# Configure plotting style
plt.style.use("seaborn-v0_8-darkgrid")
sns.set_palette("husl")

# Create output directory for figures
if not os.path.exists(FIGURE_DIR):
    os.makedirs(FIGURE_DIR)


def filter_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Filter and preprocess weather data with temporal feature extraction.
    
    Performs data cleaning, column selection, and feature engineering including:
    - Date/time extraction and formatting
    - Year, month, hour extraction
    - Season classification
    - Humidity percentage calculation
    
    Args:
        data (pd.DataFrame): Raw weather dataset with 'Formatted Date' column
        
    Returns:
        pd.DataFrame: Preprocessed dataframe with engineered features
        
    Raises:
        KeyError: If required columns are missing from input data
        ValueError: If date conversion fails
    """
    try:
        # Create a copy to avoid modifying original
        df = data.copy()
        
        # Convert and sort by timestamp
        df["Formatted Date"] = pd.to_datetime(df["Formatted Date"], utc=True)
        df.sort_values(by="Formatted Date", inplace=True)
        
        # Extract date and time components
        df["date"] = df["Formatted Date"].dt.date
        df["time"] = df["Formatted Date"].dt.time
        df["year"] = df["Formatted Date"].dt.year.astype(str)
        df["month"] = df["Formatted Date"].dt.month.map(
            lambda m: MONTH_NAMES[m - 1]
        )
        df["hour"] = df["Formatted Date"].dt.hour
        
        # Extract season from month
        df["season"] = df["month"].map(SEASON_MAP)
        
        # Convert humidity to percentage
        df["Humidity(%)"] = df["Humidity"] * 100
        
        # Select and reorder columns
        selected_columns = [
            "date", "time", "year", "month", "hour", "season",
            "Summary", "Precip Type", "Temperature (C)",
            "Wind Speed (km/h)", "Pressure (millibars)", "Humidity(%)"
        ]
        df_filtered = df[selected_columns].copy()
        
        # Save to CSV
        df_filtered.to_csv(FILTERED_DATA_FILE, index=False)
        print(f"✓ Data filtered and stored in {FILTERED_DATA_FILE}")
        
        return df_filtered
        
    except KeyError as e:
        print(f"✗ Error: Missing required column {e}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error filtering data: {e}")
        sys.exit(1)


def fill_missing_values(input_file: str = FILTERED_DATA_FILE,
                        output_file: str = FILLED_DATA_FILE) -> pd.DataFrame:
    """
    Fill missing values in weather data using appropriate strategies.
    
    Strategies applied:
    - Categorical: Forward fill for Precip Type
    - Numerical: Mean imputation for Temperature, Wind Speed, Pressure, Humidity
    
    Args:
        input_file (str): Path to filtered data CSV file
        output_file (str): Path to save filled data CSV file
        
    Returns:
        pd.DataFrame: Cleaned dataframe with no missing values
        
    Raises:
        FileNotFoundError: If input file does not exist
        Exception: If filling process fails
    """
    try:
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file '{input_file}' not found")
        
        # Load filtered data
        df = pd.read_csv(input_file)
        
        # Display missing value statistics
        missing_count = df.isnull().sum().sum()
        if missing_count > 0:
            print(f"ℹ Found {missing_count} missing values")
            print(f"Missing value breakdown:\n{df.isnull().sum()}\n")
        
        # Fill categorical missing values
        df["Precip Type"].fillna("rain", inplace=True)
        
        # Fill numerical missing values with mean
        numerical_columns = [
            "Temperature (C)", "Wind Speed (km/h)",
            "Pressure (millibars)", "Humidity(%)"
        ]
        
        for col in numerical_columns:
            if df[col].isnull().sum() > 0:
                mean_val = df[col].mean()
                df[col].fillna(mean_val, inplace=True)
        
        # Save cleaned data
        df.to_csv(output_file, index=False)
        print(f"✓ Missing values filled and stored in {output_file}")
        
        return df
        
    except FileNotFoundError as e:
        print(f"✗ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error filling missing values: {e}")
        sys.exit(1)


def _save_figure(filename: str, title: Optional[str] = None) -> None:
    """
    Save current matplotlib figure to FIGURE_DIR.
    
    Args:
        filename (str): Name of the output file (without directory)
        title (str, optional): Title for the plot
    """
    filepath = os.path.join(FIGURE_DIR, filename)
    plt.tight_layout()
    plt.savefig(filepath, dpi=300, bbox_inches="tight")
    print(f"✓ Figure saved: {filepath}")
    plt.close()


def _plot_distribution(data: pd.DataFrame, column: str, title: str,
                       filename: str, color: str = "steelblue") -> None:
    """
    Create and save a histogram for a given column.
    
    Args:
        data (pd.DataFrame): Input dataframe
        column (str): Column name to plot
        title (str): Plot title
        filename (str): Output filename
        color (str): Color for the histogram
    """
    plt.figure(figsize=(12, 6), dpi=150)
    sns.histplot(data=data, x=column, color=color, edgecolor="black", kde=True)
    plt.title(title, fontsize=14, fontweight="bold")
    plt.xlabel(column, fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    _save_figure(filename, title)


def _plot_categorical_distribution(data: pd.DataFrame, column: str,
                                    title: str, filename: str) -> None:
    """
    Create and save a count plot for categorical variables.
    
    Args:
        data (pd.DataFrame): Input dataframe
        column (str): Column name to plot
        title (str): Plot title
        filename (str): Output filename
    """
    plt.figure(figsize=(14, 6), dpi=150)
    ax = sns.countplot(data=data, x=column, palette="Set2", order=data[column].value_counts().index)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_xlabel(column, fontsize=12)
    ax.set_ylabel("Count", fontsize=12)
    ax.tick_params(axis="x", rotation=45)
    
    # Add value labels on bars
    for rect in ax.patches:
        ax.text(
            rect.get_x() + rect.get_width() / 2,
            rect.get_height() + 1,
            int(rect.get_height()),
            ha="center", va="bottom", fontsize=10
        )
    _save_figure(filename, title)


def _plot_relationship(data: pd.DataFrame, x: str, y: str, hue: Optional[str],
                       title: str, filename: str, plot_type: str = "scatter") -> None:
    """
    Create and save a relationship plot.
    
    Args:
        data (pd.DataFrame): Input dataframe
        x (str): X-axis column
        y (str): Y-axis column
        hue (str, optional): Column for color encoding
        title (str): Plot title
        filename (str): Output filename
        plot_type (str): Type of plot ("scatter", "line", "joint")
    """
    plt.figure(figsize=(12, 7), dpi=150)
    
    if plot_type == "joint":
        sns.jointplot(data=data, x=x, y=y, hue=hue, height=8)
    else:
        ax = plt.gca()
        if plot_type == "scatter":
            sns.scatterplot(data=data, x=x, y=y, hue=hue, ax=ax, s=50, alpha=0.6)
        elif plot_type == "line":
            sns.lineplot(data=data, x=x, y=y, hue=hue, ax=ax)
        
        ax.set_title(title, fontsize=14, fontweight="bold")
        ax.set_xlabel(x, fontsize=12)
        ax.set_ylabel(y, fontsize=12)
    
    _save_figure(filename, title)


def visualize_data(data: pd.DataFrame) -> None:
    """
    Generate comprehensive visualizations of weather data.
    
    Creates and saves multiple plots including:
    - Distribution histograms for all numerical variables
    - Categorical summaries for weather conditions
    - Relationship visualizations between variables
    - Temporal and seasonal comparisons
    
    Args:
        data (pd.DataFrame): Cleaned weather dataframe
    """
    try:
        # Load cleaned data
        if not os.path.exists(FILLED_DATA_FILE):
            print(f"✗ Error: {FILLED_DATA_FILE} not found. Run data preprocessing first.")
            return
        
        df = pd.read_csv(FILLED_DATA_FILE)
        
        print("\n" + "="*60)
        print("GENERATING VISUALIZATIONS")
        print("="*60 + "\n")
        
        # 1. Distribution plots for numerical variables
        print("Creating distribution plots...")
        _plot_distribution(df, "Humidity(%)", "Distribution of Humidity (%)",
                          "01_humidity_distribution.png", "blue")
        _plot_distribution(df, "Temperature (C)", "Distribution of Temperature (°C)",
                          "02_temperature_distribution.png", "red")
        _plot_distribution(df, "Wind Speed (km/h)", "Distribution of Wind Speed (km/h)",
                          "03_wind_speed_distribution.png", "green")
        _plot_distribution(df, "Pressure (millibars)", "Distribution of Pressure (mb)",
                          "04_pressure_distribution.png", "purple")
        
        # 2. Categorical plots
        print("Creating categorical plots...")
        _plot_categorical_distribution(df, "Precip Type",
                                       "Distribution of Precipitation Types",
                                       "05_precip_type_distribution.png")
        _plot_categorical_distribution(df, "Summary",
                                       "Distribution of Weather Conditions",
                                       "06_weather_summary_distribution.png")
        
        # 3. Relationship plots
        print("Creating relationship plots...")
        _plot_relationship(df, "Humidity(%)", "Temperature (C)", "season",
                          "Humidity vs Temperature (by Season)",
                          "07_humidity_temp_by_season.png", "scatter")
        
        _plot_relationship(df, "Humidity(%)", "Wind Speed (km/h)", "season",
                          "Humidity vs Wind Speed (by Season)",
                          "08_humidity_wind_by_season.png", "line")
        
        _plot_relationship(df, "Temperature (C)", "Pressure (millibars)", "season",
                          "Temperature vs Pressure (by Season)",
                          "09_temp_pressure_by_season.png", "scatter")
        
        # 4. Monthly comparison plots
        print("Creating monthly comparison plots...")
        plt.figure(figsize=(16, 10), dpi=150)
        g = sns.relplot(data=df, x="Humidity(%)", y="Temperature (C)",
                       hue="year", col="month", col_wrap=4, height=3)
        g.set_titles("Month: {col_name}", fontsize=12, fontweight="bold")
        _save_figure("10_monthly_humidity_temp_comparison.png")
        
        plt.figure(figsize=(16, 10), dpi=150)
        g = sns.relplot(data=df, x="Humidity(%)", y="Wind Speed (km/h)",
                       hue="year", col="month", col_wrap=4, height=3)
        g.set_titles("Month: {col_name}", fontsize=12, fontweight="bold")
        _save_figure("11_monthly_humidity_wind_comparison.png")
        
        # 5. Weather condition analysis by season
        print("Creating season-based plots...")
        plt.figure(figsize=(14, 6), dpi=150)
        sns.boxplot(data=df, x="season", y="Temperature (C)", palette="Set2")
        plt.title("Temperature Distribution by Season", fontsize=14, fontweight="bold")
        plt.xlabel("Season", fontsize=12)
        plt.ylabel("Temperature (°C)", fontsize=12)
        _save_figure("12_temperature_by_season.png")
        
        # 6. Correlation heatmap
        print("Creating correlation heatmap...")
        plt.figure(figsize=(10, 8), dpi=150)
        numerical_cols = ["Temperature (C)", "Wind Speed (km/h)",
                         "Pressure (millibars)", "Humidity(%)"]
        corr_matrix = df[numerical_cols].corr()
        sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm",
                   center=0, square=True, cbar_kws={"label": "Correlation"})
        plt.title("Correlation Matrix of Weather Variables", fontsize=14, fontweight="bold")
        _save_figure("13_correlation_heatmap.png")
        
        # 7. Interactive year-month analysis
        _plot_precipitation_by_year_month(df)
        _plot_conditions_by_year_season(df)
        
        print("\n✓ All visualizations completed successfully!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"✗ Error during visualization: {e}")
        import traceback
        traceback.print_exc()


def _plot_precipitation_by_year_month(data: pd.DataFrame) -> None:
    """
    Create precipitation distribution plot by year and month.
    
    Args:
        data (pd.DataFrame): Input dataframe
    """
    while True:
        try:
            year_input = input("Enter year to visualize precipitation (2005-2015) or 'skip': ").strip()
            if year_input.lower() == "skip":
                return
            
            year = str(int(year_input))  # Validate input
            if year not in data["year"].values:
                print(f"✗ Year {year} not found. Available years: {sorted(data['year'].unique())}")
                continue
            
            df_year = data[data["year"] == year]
            
            plt.figure(figsize=(12, 6), dpi=150)
            ax = sns.countplot(data=df_year, x="month", hue="Precip Type",
                             palette="bright", order=MONTH_NAMES)
            ax.set_title(f"Precipitation Types by Month ({year})", fontsize=14, fontweight="bold")
            ax.set_xlabel("Month", fontsize=12)
            ax.set_ylabel("Hours", fontsize=12)
            
            # Add value labels
            for rect in ax.patches:
                ax.text(rect.get_x() + rect.get_width()/2, rect.get_height() + 0.5,
                       int(rect.get_height()), ha="center", va="bottom", fontsize=9)
            
            _save_figure(f"14_precipitation_{year}.png")
            break
            
        except ValueError:
            print("✗ Invalid input. Please enter a valid year.")


def _plot_conditions_by_year_season(data: pd.DataFrame) -> None:
    """
    Create weather condition distribution plot by year and season.
    
    Args:
        data (pd.DataFrame): Input dataframe
    """
    while True:
        try:
            year_input = input("Enter year to visualize weather conditions (2005-2015) or 'skip': ").strip()
            if year_input.lower() == "skip":
                return
            
            year = str(int(year_input))  # Validate input
            if year not in data["year"].values:
                print(f"✗ Year {year} not found. Available years: {sorted(data['year'].unique())}")
                continue
            
            df_year = data[data["year"] == year]
            
            plt.figure(figsize=(14, 6), dpi=150)
            hue_order = ["Spring", "Summer", "Fall", "Winter"]
            ax = sns.countplot(data=df_year, x="Summary", hue="season",
                             hue_order=hue_order, palette="Set1")
            ax.set_title(f"Weather Conditions by Season ({year})", fontsize=14, fontweight="bold")
            ax.set_xlabel("Weather Condition", fontsize=12)
            ax.set_ylabel("Hours", fontsize=12)
            ax.tick_params(axis="x", rotation=45)
            
            # Add value labels
            for rect in ax.patches:
                ax.text(rect.get_x() + rect.get_width()/2, rect.get_height() + 0.5,
                       int(rect.get_height()), ha="center", va="bottom", fontsize=8)
            
            _save_figure(f"15_conditions_{year}.png")
            break
            
        except ValueError:
            print("✗ Invalid input. Please enter a valid year.")


def _calculate_statistics(data: pd.Series, var_name: str) -> dict:
    """
    Calculate comprehensive statistics for a numerical variable.
    
    Args:
        data (pd.Series): Numerical data series
        var_name (str): Variable name for display
        
    Returns:
        dict: Dictionary of statistical measures
    """
    stats = {
        "Variable": var_name,
        "Count": len(data),
        "Mean": data.mean(),
        "Median": data.median(),
        "Std Dev": data.std(),
        "Variance": data.var(),
        "Min": data.min(),
        "Max": data.max(),
        "Mode": data.mode()[0] if len(data.mode()) > 0 else "N/A",
        "25th Percentile": data.quantile(0.25),
        "75th Percentile": data.quantile(0.75),
    }
    return stats


def _print_statistics_table(stats: dict) -> str:
    """
    Format statistics dictionary as a readable table.
    
    Args:
        stats (dict): Statistics dictionary
        
    Returns:
        str: Formatted table string
    """
    output = f"\n{'='*70}\n"
    output += f"{'Statistic':<20} {stats['Variable']:<50}\n"
    output += f"{'='*70}\n"
    
    for key, value in stats.items():
        if key != "Variable":
            if isinstance(value, (int, float)):
                output += f"{key:<20} {value:>20.4f}\n"
            else:
                output += f"{key:<20} {value:>20}\n"
    
    output += f"{'='*70}\n"
    return output


def _calculate_correlations(data: pd.DataFrame) -> str:
    """
    Calculate and format correlation matrix.
    
    Args:
        data (pd.DataFrame): Input dataframe
        
    Returns:
        str: Formatted correlation output
    """
    numerical_cols = ["Temperature (C)", "Wind Speed (km/h)",
                     "Pressure (millibars)", "Humidity(%)"]
    
    output = "\n" + "="*70 + "\n"
    output += "CORRELATION ANALYSIS\n"
    output += "="*70 + "\n\n"
    
    correlations = []
    for i in range(len(numerical_cols)):
        for j in range(i + 1, len(numerical_cols)):
            col1, col2 = numerical_cols[i], numerical_cols[j]
            corr = data[col1].corr(data[col2])
            correlations.append((col1, col2, corr))
            output += f"{col1:<25} vs {col2:<25} : {corr:>8.4f}\n"
    
    output += "="*70 + "\n"
    return output


def _calculate_covariances(data: pd.DataFrame) -> str:
    """
    Calculate and format covariance matrix.
    
    Args:
        data (pd.DataFrame): Input dataframe
        
    Returns:
        str: Formatted covariance output
    """
    numerical_cols = ["Temperature (C)", "Wind Speed (km/h)",
                     "Pressure (millibars)", "Humidity(%)"]
    
    output = "\n" + "="*70 + "\n"
    output += "COVARIANCE ANALYSIS\n"
    output += "="*70 + "\n\n"
    
    covariances = []
    for i in range(len(numerical_cols)):
        for j in range(i + 1, len(numerical_cols)):
            col1, col2 = numerical_cols[i], numerical_cols[j]
            cov = data[col1].cov(data[col2])
            covariances.append((col1, col2, cov))
            output += f"{col1:<25} vs {col2:<25} : {cov:>12.4f}\n"
    
    output += "="*70 + "\n"
    return output


def analysis_data(data: pd.DataFrame) -> None:
    """
    Perform comprehensive statistical analysis on weather data.
    
    Generates:
    - Descriptive statistics for all numerical variables
    - Correlation analysis between variables
    - Covariance analysis
    - Statistical summary report
    
    Results are displayed in console and saved to 'analysis_report.txt'
    
    Args:
        data (pd.DataFrame): Cleaned weather dataframe
    """
    try:
        if not os.path.exists(FILLED_DATA_FILE):
            print(f"✗ Error: {FILLED_DATA_FILE} not found. Run data preprocessing first.")
            return
        
        df = pd.read_csv(FILLED_DATA_FILE)
        
        print("\n" + "="*70)
        print("WEATHER DATA ANALYSIS REPORT")
        print("="*70)
        
        # Prepare output
        output = "WEATHER DATA ANALYSIS REPORT\n"
        output += f"Generated: February 2026\n"
        output += f"Dataset: {FILLED_DATA_FILE}\n"
        output += f"Total Records: {len(df)}\n"
        
        # 1. Descriptive Statistics
        print("\n• Calculating descriptive statistics...")
        output += "\n\nDESCRIPTIVE STATISTICS\n"
        
        numerical_vars = [
            ("Temperature (C)", "Ambient Temperature"),
            ("Wind Speed (km/h)", "Wind Velocity"),
            ("Pressure (millibars)", "Atmospheric Pressure"),
            ("Humidity(%)", "Relative Humidity")
        ]
        
        for col, description in numerical_vars:
            stats = _calculate_statistics(df[col], f"{col} ({description})")
            stats_table = _print_statistics_table(stats)
            print(stats_table)
            output += stats_table
        
        # 2. Correlation Analysis
        print("• Performing correlation analysis...")
        corr_output = _calculate_correlations(df)
        print(corr_output)
        output += corr_output
        
        # 3. Covariance Analysis
        print("• Performing covariance analysis...")
        cov_output = _calculate_covariances(df)
        print(cov_output)
        output += cov_output
        
        # 4. Categorical Summary
        print("• Summarizing categorical variables...")
        output += "\n" + "="*70 + "\n"
        output += "CATEGORICAL VARIABLE SUMMARY\n"
        output += "="*70 + "\n\n"
        
        output += "Weather Conditions Distribution:\n"
        output += df["Summary"].value_counts().to_string() + "\n\n"
        
        output += "Precipitation Types Distribution:\n"
        output += df["Precip Type"].value_counts().to_string() + "\n\n"
        
        output += "Seasonal Distribution:\n"
        output += df["season"].value_counts().to_string() + "\n\n"
        
        output += "="*70 + "\n"
        
        # Save report to file
        report_file = "analysis_report.txt"
        with open(report_file, "w") as f:
            f.write(output)
        
        print(f"\n✓ Analysis completed successfully!")
        print(f"✓ Full report saved to: {report_file}")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"✗ Error during analysis: {e}")
        import traceback
        traceback.print_exc()


def display_menu() -> str:
    """
    Display the main menu and get user choice.
    
    Returns:
        str: User's menu choice
    """
    print("\n" + "="*70)
    print("WEATHER DATA ANALYSIS AND VISUALIZATION - MAIN MENU")
    print("="*70)
    print("1. Visualize Data")
    print("2. Analyze Data")
    print("3. View Data Preview")
    print("4. Exit")
    print("="*70)
    
    choice = input("Enter your choice (1-4): ").strip()
    return choice


def preview_data() -> None:
    """Display a preview of the processed data."""
    try:
        if not os.path.exists(FILLED_DATA_FILE):
            print(f"✗ Error: {FILLED_DATA_FILE} not found.")
            return
        
        df = pd.read_csv(FILLED_DATA_FILE)
        print("\n" + "="*70)
        print("DATA PREVIEW (First 10 rows)")
        print("="*70)
        print(df.head(10).to_string())
        print("\n" + "="*70)
        print(f"Total records: {len(df)}")
        print(f"Columns: {list(df.columns)}")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"✗ Error displaying data preview: {e}")


def main() -> None:
    """
    Main execution function with user-interactive menu.
    
    Orchestrates the entire workflow:
    1. Data loading and preprocessing
    2. Missing value handling
    3. User-interactive menu for visualization and analysis
    """
    try:
        print("\n" + "🌤️  " * 18)
        print("WEATHER DATA ANALYSIS AND VISUALIZATION SYSTEM")
        print("🌤️  " * 18 + "\n")
        
        # Check if data file exists
        if not os.path.exists(DATA_FILE):
            print(f"✗ Error: {DATA_FILE} not found!")
            print("Please ensure the weather data CSV file is in the current directory.")
            sys.exit(1)
        
        print("📊 Loading and preprocessing data...")
        
        # Step 1: Load and filter data
        print(f"  ✓ Loading data from {DATA_FILE}...")
        raw_data = pd.read_csv(DATA_FILE)
        print(f"  ✓ Raw data loaded: {len(raw_data)} records")
        
        print("  ✓ Filtering data...")
        df_filtered = filter_data(raw_data)
        
        # Step 2: Fill missing values
        print("  ✓ Processing missing values...")
        df_filled = fill_missing_values()
        
        print("\n✓ Data preprocessing completed successfully!\n")
        
        # Step 3: Interactive menu loop
        while True:
            choice = display_menu()
            
            if choice == "1":
                visualize_data(df_filled)
            elif choice == "2":
                analysis_data(df_filled)
            elif choice == "3":
                preview_data()
            elif choice == "4":
                print("\n👋 Thank you for using Weather Data Analysis System!")
                print("Goodbye!\n")
                break
            else:
                print("✗ Invalid choice. Please enter a number between 1 and 4.")
                continue
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Program interrupted by user.")
        print("Exiting gracefully...\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
