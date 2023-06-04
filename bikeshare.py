import csv
import datetime
from datetime import date
from datetime import datetime
import time
import numpy as np
import pandas as pd

def f_calculate_file(eingabe1, eingabe2, eingabe3):
    """Calculate statistics.

        Keyword arguments:
        eingabe1 -- 1st input from user
        eingabe2 -- 2nd input from user
        eingabe3 -- 3rd input from user
        """
    if eingabe1 == "C":
        file_name = "chicago.csv"
    elif eingabe1 == "W":
        file_name = "washington.csv"
    elif eingabe1 == "NY":
        file_name = "new_york_city.csv"
    else:
        print("Error")
        return
    if eingabe1 == "C" or eingabe1 == "NY":
        df = pd.read_csv(
            file_name,
            sep=",",
            header=0,
            names=[
                "Key",
                "Start_Time",
                "End_Time",
                "Trip_Duration",
                "Start_Station",
                "End_Station",
                "User_Type",
                "Gender",
                "Birth_Year",
            ],
        )
        #Fill empty rows in Birth_Year with default value (one strategy to deal with empty values)
        df["Birth_Year"] = df["Birth_Year"].fillna(2000)
        df["Birth_Year"] = pd.to_numeric(
            df["Birth_Year"], downcast="integer", errors="coerce"
        )
    # washington.csv has less columns
    elif eingabe1 == "W":
        df = pd.read_csv(
            file_name,
            sep=",",
            header=0,
            names=[
                "Key",
                "Start_Time",
                "End_Time",
                "Trip_Duration",
                "Start_Station",
                "End_Station",
                "User_Type",
            ],
        )
    df["Start_Month"] = pd.to_datetime(df["Start_Time"]).dt.month
    df["Start_Hour"] = pd.to_datetime(df["Start_Time"]).dt.hour
    df["Weekday_Name"] = pd.to_datetime(df["Start_Time"]).dt.day_name()
    df["Start_End_Station"] = df["Start_Station"] + " * " + df["End_Station"]
    # dealing with month and day of week
    if eingabe2 == "m":
        month_number = int(f_month_converter(eingabe3))
        df = df.loc[(df["Start_Month"] == month_number)]
    elif eingabe2 == "d":
        weekday_name = f_day_converter2(eingabe3)
        df = df.loc[(df["Weekday_Name"] == weekday_name)]
    # statistics
    time_stats(df)
    station_stats(df)
    trip_duration_stats(df)
    if eingabe1 == "C" or eingabe1 == "NY":
        user_stats(df)
    elif eingabe1 == "W":
        print("User data for Washington is not calculated, as the fields do not exist.")
        print("-" * 40)
    # used for testing:
    # pd.set_option('expand_frame_repr', False)
    # print(df.head())


def time_stats(df):
    """Displays statistics on the most frequent times of travel.

            Keyword arguments:
            df -- data frame
            """
    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()
    # most frequent month
    popular_month = df["Start_Month"].mode()[0]
    print("Most Popular Start Month:", popular_month)
    # most frequent hour
    popular_hour = df["Start_Hour"].mode()[0]
    print("Most Popular Start Hour:", popular_hour)
    # most frequent day of week
    popular_weekday_name = df["Weekday_Name"].mode()[0]
    print("Most Popular Weekday Name:", popular_weekday_name)
    # duration
    print("\nThis took %s seconds." % round((time.time() - start_time), 2))
    print("-" * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.

                Keyword arguments:
                df -- data frame
                """
    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()
    # most frequent start station
    popular_start_station = df["Start_Station"].mode()[0]
    print("Most Popular Start Station:", popular_start_station)
    # most frequent end station
    popular_end_station = df["End_Station"].mode()[0]
    print("Most Popular End Station:", popular_end_station)
    # most frequent start/end station
    popular_start_end_station = df["Start_End_Station"].mode()[0]
    print("Most Popular Start End Station:", popular_start_end_station)
    # duration
    print("\nThis took %s seconds." % round((time.time() - start_time), 2))
    print("-" * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.

                    Keyword arguments:
                    df -- data frame
                    """
    print("\nCalculating Trip Duration...\n")
    start_time = time.time()
    #sum
    total_trip_duration = round(df["Trip_Duration"].sum(), 2)
    print("Total trip duration:", total_trip_duration)
    #average
    mean_trip_duration = round(df["Trip_Duration"].mean(), 2)
    print("Average trip duration:", mean_trip_duration)
    # duration
    print("\nThis took %s seconds." % round((time.time() - start_time), 2))
    print("-" * 40)


def user_stats(df):
    """Displays statistics on bikeshare users.

                        Keyword arguments:
                        df -- data frame
                        """
    print("\nCalculating User Stats...\n")
    start_time = time.time()
    # listing user types
    user_types = df["User_Type"].value_counts()
    print(user_types)
    # listing gender
    genders = df["Gender"].value_counts()
    print(genders)
    # Display earliest, most recent, and most common year of birth; Assumption: missing values set to 2000
    popular_birth_year = df["Birth_Year"].mode()[0]
    print("Most Popular Birth Year:", popular_birth_year)
    min_birth_year = df["Birth_Year"].min()
    print("Earliest Birth Year:", min_birth_year)
    max_birth_year = df["Birth_Year"].max()
    print("Most recent Birth Year:", max_birth_year)
    # duration
    print("\nThis took %s seconds." % round((time.time() - start_time), 2))
    print("-" * 40)


def f_read_file(eingabe1, eingabe2, eingabe3):
    """Listing rows from file.

            Keyword arguments:
            eingabe1 -- 1st input from user
            eingabe2 -- 2nd input from user
            eingabe3 -- 3rd input from user
            """
    if eingabe1 == "C":
        file_name = "chicago.csv"
    elif eingabe1 == "W":
        file_name = "washington.csv"
    elif eingabe1 == "NY":
        file_name = "new_york_city.csv"
    else:
        print("Error")
        return
    # cursor:
    with open(file_name, "r") as csv_file:
        csv_reader_object = csv.reader(csv_file)
        i = 1
        if eingabe2 == "m":
            month_number = f_month_converter(eingabe3)
        elif eingabe2 == "d":
            day_number = f_day_converter(eingabe3)
            formatting = "%Y-%m-%d"
        kopfzeile = next(csv_reader_object)
        print(kopfzeile)
        for row in csv_reader_object:
            if (
                eingabe2 == "n"
                or eingabe2 == "m"
                and row[1][6:7] == month_number
                or eingabe2 == "d"
                and datetime.strptime(row[1][0:10], formatting).weekday() == day_number
            ):
                print(row)
                i = i + 1

            if i > 1 and i % 5 == 1:
                print("Do you want to continue? Y = Yes, otherwise it will end")
                eingabe = input()
                if eingabe.upper() == "Y" or eingabe.upper() == "YES":
                    i = 1
                    print(kopfzeile)
                else:
                    print("end")
                    return


def f_month_converter(monthname):
    """Casting abbreviated month name to number

                Keyword arguments:
                monthname -- abbreviated month name
                """
    month_number = "0"
    if monthname == "Dummy":
        month_number = "0"
    elif monthname == "JAN":
        month_number = "1"
    elif monthname == "FEB":
        month_number = "2"
    elif monthname == "MAR":
        month_number = "3"
    elif monthname == "APR":
        month_number = "4"
    elif monthname == "MAY":
        month_number = "5"
    elif monthname == "JUN":
        month_number = "6"
    else:
        month_number = "0"
    return month_number


def f_day_converter(dayname):
    """Casting day name to number

                    Keyword arguments:
                    dayname -- abbreviated day name
                    """
    day_number = 8
    if dayname == "Dummy":
        day_number = 8
    elif dayname == "MO":
        day_number = 0
    elif dayname == "TU":
        day_number = 1
    elif dayname == "WE":
        day_number = 2
    elif dayname == "TH":
        day_number = 3
    elif dayname == "FR":
        day_number = 4
    elif dayname == "SA":
        day_number = 5
    elif dayname == "SU":
        day_number = 6
    else:
        day_number = 8
    return day_number


def f_day_converter2(dayname):
    """Casting abbreviated day name to full day name

                        Keyword arguments:
                        dayname -- abbreviated day name
                        """
    weekday_name = "false"
    if dayname == "Dummy":
        weekday_name = "false"
    elif dayname == "MO":
        weekday_name = "Monday"
    elif dayname == "TU":
        weekday_name = "Tuesday"
    elif dayname == "WE":
        weekday_name = "Wednesday"
    elif dayname == "TH":
        weekday_name = "Thursday"
    elif dayname == "FR":
        weekday_name = "Friday"
    elif dayname == "SA":
        weekday_name = "Saturday"
    elif dayname == "SU":
        weekday_name = "Sunday"
    else:
        weekday_name = "false"
    return weekday_name


def f_eingabe0():
    """0-th input from user"""
    print(
        "Would you like to see raw data or calculated statistical data? Then write R or CS. Write Exit for exit"
    )
    eingabe0 = input()
    eingabe0 = eingabe0.upper()
    if eingabe0 == "R":
        print("You have entered: " + eingabe0 + " (raw data)")
    elif eingabe0 == "CS":
        print("You have entered: " + eingabe0 + " (calculated statistical data)")
    elif eingabe0.upper() == "EXIT":
        print("Exit")
        exit()
    else:
        print("Wrong input. Try again!")
    return eingabe0


def f_eingabe1():
    """1st input from user"""
    print(
        "Would you like to see data for Chicago, New York, or Washington? Then write C, NY or W. Write Exit for exit"
    )
    eingabe1 = input()
    eingabe1 = eingabe1.upper()
    if eingabe1 == "C":
        print("You have entered: " + eingabe1 + " (Chicago)")
    elif eingabe1 == "NY":
        print("You have entered: " + eingabe1 + " (New York)")
    elif eingabe1 == "W":
        print("You have entered: " + eingabe1 + " (Washington)")
    elif eingabe1.upper() == "EXIT":
        print("Exit")
        exit()
    else:
        print("Wrong input. Try again!")
    return eingabe1


def f_eingabe2():
    """2nd input from user"""
    print(
        "Would you like to filter the data by month, day of the week or not at all? Then write m, d or n"
    )
    eingabe2 = input()
    eingabe2 = eingabe2.lower()
    if eingabe2 == "m":
        print("You have entered: " + eingabe2 + " (month).")
    elif eingabe2 == "d":
        print("You have entered: " + eingabe2 + " (day of the week).")
    elif eingabe2 == "n":
        print("You have entered: " + eingabe2 + " (not at all).")
    elif eingabe2.upper() == "EXIT":
        print("Exit")
        exit()
    else:
        print("Wrong input: Write month, day or not at all or Exit. Try again!")
    return eingabe2


def f_eingabe3a():
    """3rd input from user, variant: month"""
    print(
        "Which month do you want to see? Write JAN for January, FEB for February, MAR for March, APR for April, MAY for May, or JUN for June."
    )
    eingabe3a = input()
    eingabe3a = eingabe3a.upper()
    if eingabe3a == "JAN":
        print("You have entered: " + eingabe3a + " (January).")
    elif eingabe3a == "FEB":
        print("You have entered: " + eingabe3a + " (February).")
    elif eingabe3a == "MAR":
        print("You have entered: " + eingabe3a + " (March).")
    elif eingabe3a == "APR":
        print("You have entered: " + eingabe3a + " (April).")
    elif eingabe3a == "MAY":
        print("You have entered: " + eingabe3a + " (May).")
    elif eingabe3a == "JUN":
        print("You have entered: " + eingabe3a + " (Jun).")
    elif eingabe3a.upper() == "EXIT":
        print("Exit")
        exit()
    else:
        print("Wrong input: Write Jan, Feb, Mar, Apr, May or Jun or Exit. Try again!")
    return eingabe3a


def f_eingabe3b():
    """3rd input from user, variant: day"""
    print(
        "Which day do you want to see? Write Mo for Monday, Tu for Tuesday, We for Wednesday, Th for Thursday, Fr for Friday, Sa for Saturday, or Su for Sunday."
    )
    eingabe3b = input()
    eingabe3b = eingabe3b.upper()
    if eingabe3b == "MO":
        print("You have entered: " + eingabe3b + " (Monday).")
    elif eingabe3b == "TU":
        print("You have entered: " + eingabe3b + " (Tuesday).")
    elif eingabe3b == "WE":
        print("You have entered: " + eingabe3b + " (Wednesday).")
    elif eingabe3b == "TH":
        print("You have entered: " + eingabe3b + " (Thursday).")
    elif eingabe3b == "FR":
        print("You have entered: " + eingabe3b + " (Friday).")
    elif eingabe3b == "SA":
        print("You have entered: " + eingabe3b + " (Saturday).")
    elif eingabe3b == "SU":
        print("You have entered: " + eingabe3b + " (Sunday).")
    return eingabe3b

def main():
    i = 0
    while i == 0:
        eingabe0 = ""
        eingabe1 = ""
        eingabe2 = ""
        eingabe3a = ""
        eingabe3b = ""
        eingabe0 = f_eingabe0()
        eingabe0 = eingabe0.upper()
        if eingabe0 == "R":
            eingabe1 = f_eingabe1()
            eingabe1 = eingabe1.upper()
            eingabe2 = f_eingabe2()
            eingabe2 = eingabe2.lower()
            if eingabe2 == "n":
                f_read_file(eingabe1, "n", "dummy")
            elif eingabe2 == "m":
                eingabe3a = f_eingabe3a()
                f_read_file(eingabe1, eingabe2, eingabe3a)
            elif eingabe2 == "d":
                eingabe3b = f_eingabe3b()
                f_read_file(eingabe1, eingabe2, eingabe3b)
            else:
                print("Wrong input.")
                i = 1
        elif eingabe0 == "CS":
            eingabe1 = f_eingabe1()
            eingabe1 = eingabe1.upper()
            eingabe2 = f_eingabe2()
            eingabe2 = eingabe2.lower()
            if eingabe2 == "n":
                f_calculate_file(eingabe1, "n", "dummy")
            elif eingabe2 == "m":
                eingabe3a = f_eingabe3a()
                f_calculate_file(eingabe1, eingabe2, eingabe3a)
            elif eingabe2 == "d":
                eingabe3b = f_eingabe3b()
                f_calculate_file(eingabe1, eingabe2, eingabe3b)
        elif eingabe0 == "EXIT":
            print("Exit.")
            i = 1
        else:
            i = 0

if __name__ == "__main__":
    main()
