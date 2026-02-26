import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings("ignore")

# Load the data
data = pd.read_csv("EnglandWeather.csv")
df = pd.DataFrame(data)


def filter_data(df):
    """
    Filters the data to include only the necessary columns and formats the data for analysis.
    """
    df["Formatted Date"] = pd.to_datetime(df["Formatted Date"], utc=True)
    df.sort_values(by="Formatted Date", inplace=True)
    df["date"] = [d.date() for d in df["Formatted Date"]]
    df["time"] = [d.time() for d in df["Formatted Date"]]
    correct_date = pd.to_datetime(df["date"], format="%Y-%m-%d").dt.strftime("%m-%d-%Y")
    df1 = pd.DataFrame(correct_date)
    df["date"] = df1["date"].astype("datetime64[ns]")
    df.sort_values(by="Formatted Date", inplace=True)
    df2 = df[
        [
            "date",
            "time",
            "Summary",
            "Precip Type",
            "Temperature (C)",
            "Wind Speed (km/h)",
            "Pressure (millibars)",
            "Humidity",
        ]
    ]

    df3 = df2["date"].dt.year
    df2["year"] = df3.astype("string")
    df4 = df2["date"].dt.month

    month = []
    for i in df4:
        if i == 1:
            month.append("January")
        if i == 2:
            month.append("February")
        if i == 3:
            month.append("March")
        if i == 4:
            month.append("April")
        if i == 5:
            month.append("May")
        if i == 6:
            month.append("June")
        if i == 7:
            month.append("July")
        if i == 8:
            month.append("August")
        if i == 9:
            month.append("September")
        if i == 10:
            month.append("October")
        if i == 11:
            month.append("November")
        if i == 12:
            month.append("December")

    df5 = pd.DataFrame(month)
    df2["month"] = df5

    df100 = pd.DataFrame(data)
    df100["Formatted Date"] = pd.to_datetime(df100["Formatted Date"], utc=True)
    df2["hour"] = df100["Formatted Date"].apply(lambda x: x.hour)

    df6 = df2["month"]
    df6 = df2["month"]

    season = []
    for i in df6:
        if i == "March" or i == "April" or i == "May":
            season.append("Spring")
        if i == "June" or i == "July" or i == "August":
            season.append("Summer")
        if i == "September" or i == "October" or i == "November":
            season.append("Fall")
        if i == "December" or i == "January" or i == "February":
            season.append("Winter")

    df7 = pd.DataFrame(season)
    df2["season"] = df7
    df2["Humidity(%)"] = df2["Humidity"] * 100
    df2 = df2[
        [
            "date",
            "time",
            "year",
            "month",
            "hour",
            "season",
            "Summary",
            "Precip Type",
            "Temperature (C)",
            "Wind Speed (km/h)",
            "Pressure (millibars)",
            "Humidity(%)",
        ]
    ]
    df2.to_csv("filtered_data.csv", index=True)
    print("Data filtered and stored in filtered_data.csv")


def fill_missing_values(df):
    """
    Fills missing values in the data.
    """
    f_data = pd.read_csv("filtered_data.csv")
    df2 = pd.DataFrame(f_data)
    null_data = df2[df2.isnull().any(axis=1)]
    null_data["date"].unique()
    df2["Precip Type"].fillna("rain", inplace=True)
    df2["Temperature (C)"].fillna(df2["Temperature (C)"].mean(), inplace=True)
    df2["Wind Speed (km/h)"].fillna(df2["Wind Speed (km/h)"].mean(), inplace=True)
    df2["Pressure (millibars)"].fillna(df2["Pressure (millibars)"].mean(), inplace=True)
    df2["Humidity(%)"].fillna(df2["Humidity(%)"].mean(), inplace=True)
    df2.to_csv("filled_data.csv", index=True)
    print("Missing values filled and stored in filled_data.csv")


def visualize_data(df):
    """
    Visualizes the data using various plots.
    """

    f_data = pd.read_csv("filled_data.csv")
    df2 = pd.DataFrame(f_data)

    plt.figure(figsize=(12, 6), dpi=150)
    sns.histplot(data=df2, x="Humidity(%)", color="blue", ec="black")
    plt.title("Histogram of Humidity", fontsize=10)
    plt.show()

    plt.figure(figsize=(12, 6))
    sns.histplot(data=df2, x="Temperature (C)", color="blue", ec="black")
    plt.title("Histogram of Temperature", fontsize=10)
    plt.show()

    plt.figure(figsize=(12, 6))
    y = sns.histplot(
        data=df2,
        x="Precip Type",
        color="blue",
        ec="black",
        element="bars",
        bins=20,
        stat="count",
        legend=False,
    )
    y.set(xlabel="type of precipitation")
    y.bar_label(y.containers[0])
    plt.title("Histogram of type of precipitatione", fontsize=10)
    plt.show()

    plt.figure(figsize=(12, 6))

    y = sns.histplot(
        data=df2,
        x="Summary",
        color="blue",
        ec="black",
        element="bars",
        bins=20,
        stat="count",
        legend=False,
    )

    y.set(xlabel="Summary")
    y.bar_label(y.containers[0])
    plt.xticks(rotation=90)
    plt.title("Histogram of Summary", fontsize=10)
    plt.show()

    plt.figure(figsize=(12, 6))
    sns.histplot(data=df2, x="Wind Speed (km/h)", color="blue", ec="black")
    plt.title("Histogram of Wind Speed", fontsize=10)
    plt.show()

    plt.figure(figsize=(12, 6))
    y = sns.histplot(
        data=df2,
        x="Pressure (millibars)",
        color="blue",
        ec="black",
        element="bars",
        bins=20,
        stat="count",
        legend=False,
    )
    y.set(xlabel="Pressure (millibars)")
    y.bar_label(y.containers[0])
    plt.xticks(rotation=90)
    plt.title("Histogram of Pressure", fontsize=10)
    plt.show()

    plt.figure(figsize=(12, 6))
    sns.jointplot(data=df2, x="Humidity(%)", y="Temperature (C)", hue="season")

    plt.show()

    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df2, x="Humidity(%)", y="Temperature (C)", hue="season")
    plt.title("Humidity VS Temperature", fontsize=10)
    plt.show()

    plt.figure(figsize=(12, 6))

    sns.relplot(
        data=df2,
        x="Humidity(%)",
        y="Wind Speed (km/h)",
        hue="year",
        col="month",
        col_wrap=4,
    )
    plt.title("Comparison of Humidity and Wind Speed by date ", fontsize=10)
    plt.show()

    plt.figure(figsize=(12, 6))

    sns.relplot(
        data=df2,
        x="Humidity(%)",
        y="Temperature (C)",
        hue="year",
        col="month",
        col_wrap=4,
    )
    plt.title("Comparison of Humidity and Temperature by date ", fontsize=10)
    plt.show()

    plt.figure(figsize=(12, 6))

    sns.relplot(
        data=df2,
        x="Humidity(%)",
        y="Pressure (millibars)",
        hue="year",
        col="month",
        col_wrap=4,
    )
    plt.title("Comparison of Humidity and Pressure by date ", fontsize=10)
    plt.show()

    plt.figure(figsize=(12, 6))

    sns.relplot(
        data=df2,
        x="Humidity(%)",
        y="Temperature (C)",
        hue="Summary",
        col="month",
        col_wrap=4,
    )
    plt.title(
        "Comparison of Humidity and Temperature by date and condition ", fontsize=10
    )
    plt.show()

    plt.figure(figsize=(12, 6))

    sns.relplot(
        data=df2,
        x="Humidity(%)",
        y="Wind Speed (km/h)",
        hue="Summary",
        col="month",
        col_wrap=3,
    )
    plt.title(
        "Comparison of Humidity and Wind Speed by date and condition ", fontsize=10
    )
    plt.show()

    # Visualizing the rain in 2015 and 2016
    input_year = input("Enter the year to visualize the data: (2005-2015) ")
    input_year = str(input_year)
    df21 = df2[df2["year"] == input_year]
    df21
    hue_order = ["snow", "rain"]
    plt.figure(figsize=(10, 7))
    countplot1 = countplot = sns.countplot(
        data=df21,
        x="month",
        hue="Precip Type",
        hue_order=hue_order,
        color="blue",
        palette="bright",
    )
    countplot1.set_title(f"Hours of snow or rain in {input_year} ")
    for rect in countplot1.patches:
        countplot1.text(
            rect.get_x() + rect.get_width() / 2,
            rect.get_height() + 0.75,
            rect.get_height(),
            horizontalalignment="center",
            fontsize=11,
        )
    plt.show()

    # visualizing the special weather conditions in 2015 and 2016
    input_year = input("Enter the year to visualize the data: (2005-2015) ")
    input_year = str(input_year)
    df51 = df2[df2["year"] == input_year]
    df51
    hue_order = ["Spring", "Summer", "Fall", "Winter"]
    plt.figure(figsize=(10, 7))
    countplot51 = sns.countplot(
        data=df51,
        x="Summary",
        hue="season",
        hue_order=hue_order,
        color="blue",
        palette="bright",
    )
    countplot51.set_title(
        f"The number of hours of the day that had special weather conditions in {input_year}"
    )
    plt.xticks(rotation=90)
    for rect in countplot51.patches:
        countplot51.text(
            rect.get_x() + rect.get_width() / 2,
            rect.get_height() + 0.75,
            rect.get_height(),
            horizontalalignment="center",
            fontsize=11,
        )
    plt.show()


def analysis_data(df):
    """
    Analyzes the data and provides insights.
    """
    f_data = pd.read_csv("filled_data.csv")
    df2 = pd.DataFrame(f_data)
    print("Data Analysis :: \n")
    print("Summary of Temperature :: ")
    print(df2["Temperature (C)"].describe())
    print("Summary of Wind Speed :: ")
    print(df2["Wind Speed (km/h)"].describe())
    print("Summary of Pressure :: ")
    print(df2["Pressure (millibars)"].describe())
    print("Summary of Humidity :: ")
    print(df2["Humidity(%)"].describe())
    print("Mean Temperature :: ")
    print(df2["Temperature (C)"].mean())
    print("Median Temperature :: ")
    print(df2["Temperature (C)"].median())
    print("Mode Temperature :: ")
    print(df2["Temperature (C)"].mode())
    print("Standard Deviation of Temperature :: ")
    print(df2["Temperature (C)"].std())
    print("Variance of Temperature :: ")
    print(df2["Temperature (C)"].var())
    print("Mean Wind Speed :: ")
    print(df2["Wind Speed (km/h)"].mean())
    print("Median Wind Speed :: ")
    print(df2["Wind Speed (km/h)"].median())
    print("Mode Wind Speed :: ")
    print(df2["Wind Speed (km/h)"].mode())
    print("Standard Deviation of Wind Speed :: ")
    print(df2["Wind Speed (km/h)"].std())
    print("Variance of Wind Speed :: ")
    print(df2["Wind Speed (km/h)"].var())
    print("Mean Pressure :: ")
    print(df2["Pressure (millibars)"].mean())
    print("Median Pressure :: ")
    print(df2["Pressure (millibars)"].median())
    print("Mode Pressure :: ")
    print(df2["Pressure (millibars)"].mode())
    print("Standard Deviation of Pressure :: ")
    print(df2["Pressure (millibars)"].std())
    print("Variance of Pressure :: ")
    print(df2["Pressure (millibars)"].var())
    print("Mean Humidity :: ")
    print(df2["Humidity(%)"].mean())
    print("Median Humidity :: ")
    print(df2["Humidity(%)"].median())
    print("Mode Humidity :: ")
    print(df2["Humidity(%)"].mode())
    print("Standard Deviation of Humidity :: ")
    print(df2["Humidity(%)"].std())
    print("Variance of Humidity :: ")
    print(df2["Humidity(%)"].var())
    print("Correlation between Temperature and Humidity :: ")
    print(df2["Temperature (C)"].corr(df2["Humidity(%)"]))
    print("Correlation between Temperature and Wind Speed :: ")
    print(df2["Temperature (C)"].corr(df2["Wind Speed (km/h)"]))
    print("Correlation between Temperature and Pressure :: ")
    print(df2["Temperature (C)"].corr(df2["Pressure (millibars)"]))
    print("Correlation between Wind Speed and Pressure :: ")
    print(df2["Wind Speed (km/h)"].corr(df2["Pressure (millibars)"]))
    print("Correlation between Wind Speed and Humidity :: ")
    print(df2["Wind Speed (km/h)"].corr(df2["Humidity(%)"]))
    print("Correlation between Pressure and Humidity :: ")
    print(df2["Pressure (millibars)"].corr(df2["Humidity(%)"]))
    print("Covariance between Temperature and Humidity :: ")
    print(df2["Temperature (C)"].cov(df2["Humidity(%)"]))
    print("Covariance between Temperature and Wind Speed :: ")
    print(df2["Temperature (C)"].cov(df2["Wind Speed (km/h)"]))

    print("Covariance between Temperature and Pressure :: ")
    print(df2["Temperature (C)"].cov(df2["Pressure (millibars)"]))
    print("Covariance between Wind Speed and Pressure :: ")
    print(df2["Wind Speed (km/h)"].cov(df2["Pressure (millibars)"]))
    print("Covariance between Wind Speed and Humidity :: ")
    print(df2["Wind Speed (km/h)"].cov(df2["Humidity(%)"]))
    print("Covariance between Pressure and Humidity :: ")
    print(df2["Pressure (millibars)"].cov(df2["Humidity(%)"]))
    print("Covariance between Temperature and Humidity :: ")
    print(df2["Temperature (C)"].cov(df2["Humidity(%)"]))
    print("Covariance between Temperature and Wind Speed :: ")
    print(df2["Temperature (C)"].cov(df2["Wind Speed (km/h)"]))
    print("Covariance between Temperature and Pressure :: ")
    print(df2["Temperature (C)"].cov(df2["Pressure (millibars)"]))
    print("\n \n \n")


if __name__ == "__main__":
    """
    Main execution block. Prompts the user to input a list of cities and a date, fetches weather data for those cities,
    processes and stores the data, visualizes the data, and provides analysis.
    """
    filter_data(df)
    fill_missing_values(df)
    while True:
        print("Data Analysis and Visualization of Weather Data in England :: ")
        print("1. Visualize Data")
        print("2. Analyze Data")
        print("3. Exit")
        choice = input("Enter your choice: ")
        choice = int(choice)
        if choice == 1:
            visualize_data(df)
        elif choice == 2:
            analysis_data(df)
        elif choice == 3:
            break
        else:
            print("Invalid choice. Please try again.")
            continue
