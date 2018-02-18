import time, datetime, calendar
import pandas as pd

# Filenames
chicago = 'chicago.csv'
new_york_city = 'new_york_city.csv'
washington = 'washington.csv'
weekdays = list(calendar.day_name)
months = list(calendar.month_name)
num_days = []
for i in range(1, 13):
    num_days.append(calendar.monthrange(2017, i)[1])

def get_city():
    '''asks the user for a city and returns the filename for
    the city's bike share data

    args:
        non.
    returns:
        (str) filename for a city's bikeshare data
    '''

    city = input('\nHello! Let\'s explore some US bikeshare data!\n'
                    'Would you like to see data for Chicago, New York,'
                    ' or Washington?\n')
    if city.title() == 'Chicago':
        city = chicago
    elif city.title() == 'New York':
        city = new_york_city
    elif city.title() == 'Washington':
        city = washington
    else:
        print("Oops...I didn't quite get that. Let's assume New York")
        city = new_york_city
    return city


def get_time_period():
    '''asks the user for a time period and returns the specified filter

    args:
        none
    returns:
        1. (str) specified time filter for bikeshare data
            none: no filter
            month: filter by month by calling only function get_month()
            day: filter by day by calling functions get_month() and get_day()
        2. (int) month for the specified time period for bikeshare display_data
        3. (int) day for the specified time period for bikeshare display_data
    '''

    time_period = input('\nWould you like to filter the data by month, day, or'
                        ' not at all? Type "none" for no time filter.\n')
    month = None
    day = None

    if time_period.lower() == 'month':
        month = get_month()
    elif time_period.lower() == 'day':
        month = get_month()
        day = get_day(month)
    elif time_period.lower() != 'none':
        print("Oops...I didn't quite get that. Let's assume 'May 1st'!")
        month = '05'
        day = '01'

    return time_period, month, day

def get_month():
    '''asks the user for a month and returns the specified month

    args:
        none
    returns:
        (str) month in the form of two-digit number in string format
    '''

    month = input('\nWhich month? January, February, March, April, May,'
                    ' or June?\n')
    if month.title() in months:
        return str(months.index(month.title())).zfill(2)
    else:
        print("Oops...I didn't quite get that. Let's assume 'May'!")
        return '05'


def get_day(month):
    '''asks the user for a day and returns the specified day

    args:
        none
    returns:
        (str) day in the form of two-digit number in string format
    '''

    err_msg = "Oops...I didn't quite get that. Let's assume '01'!"
    try:
        day = int(input('\nWhich day? Please enter an integer.\n'))
    except:
        print(err_msg)
        return '01'
    if 1 <= day <= num_days[int(month) - 1]:
        return str(day).zfill(2)
    else:
        print(err_msg)
        return '01'


def popular_month(city_file):
    '''returns the most popular month for start time for a specified city
    and time period

    args:
        (str) filename for a city's bikeshare data
    returns:
        (str) month name for the most popular month for start time

    '''

    df = pd.read_csv(city_file)
    df['Month - Start Time'] = df['Start Time'].str[5:7]
    # lists only the first item of the mode list
    # area for improvement: lists multiple popular months if tied
    popular_month_int = int(df['Month - Start Time'].mode().iloc[0])
    popular_month_str = datetime.date(2018, popular_month_int, 1).strftime('%B')
    return popular_month_str


def popular_day(city_file, month):
    '''returns the most popular day of the week (Monday, Tuesday, etc.) for a
    specificed city only if time period is unfiltered or filtered only by month

    args:
        1. (str) filename for a city's bikeshare data
        2. (str) specified month for a city's bikeshare data
            none: no filter
            month: filter by month
    returns:
        (str) name for the most popular day of the week for start time
    '''

    df = pd.read_csv(city_file)
    df['Day of Week'] = pd.to_datetime(df['Start Time']).apply(
                            lambda x: x.weekday())
    df['Month'] = pd.to_datetime(df['Start Time']).apply(
                            lambda x: x.strftime("%B"))
    if month != None:
        df = df[df['Month'] == months[int(month)]]
    popular_day_int = df['Day of Week'].mode().iloc[0]
    popular_day_str = weekdays[popular_day_int] # 0 = Monday, 6 = Saturday
    return popular_day_str


def popular_hour(city_file, month, day):
    '''returns the most popular hour of day for a specificed city and a
    predetermined time period

    args:
        1. (str) filename for a city's bikeshare data
        2. (str) selected month for a city's bikeshare data
        3. (str) selected day for a city's bikeshare data
    returns:
        (str) the most popular hour of day for start time
    '''

    df = df_filter(city_file, month, day)
    df['Hour - Start Time'] = df['Start Time'].str[-8:-6]
    popular_hour_str = str(df['Hour - Start Time'].mode().iloc[0])
    return popular_hour_str


def trip_duration(city_file, month, day):
    '''returns the total trip duration and average trip duration for
    a specificed city and a predetermined time period

    args:
        1. (str) filename for a city's bikeshare data
        2. (str) selected month for a city's bikeshare data
        3. (str) selected day for a city's bikeshare data
    returns:
        1. (int) the total trip duration for the city over the time period
        2. (float) the average trip duration for the city over the time period
    '''

    df = df_filter(city_file, month, day)
    total = df['Trip Duration'].sum()
    average = df['Trip Duration'].mean()
    return total, average


def popular_stations(city_file, month, day):
    '''returns the most popular start station and most popular end station
    for a specificed city and a predetermined time period

    args:
        1. (str) filename for a city's bikeshare data
        2. (str) selected month for a city's bikeshare data
        3. (str) selected day for a city's bikeshare data
    returns:
        1. (str) the most popular start station for
                the city over the time period
        2. (str) the most popular end station for
                the city over the time period
    '''

    df = df_filter(city_file, month, day)
    start = df['Start Station'].mode().iloc[0]
    end = df['End Station'].mode().iloc[0]
    return start, end


def popular_trip(city_file, month, day):
    '''returns the most popular trip, defined here as having the same start
    and end stations, for a specificed city and a predetermined time period

    args:
        1. (str) filename for a city's bikeshare data
        2. (str) selected month for a city's bikeshare data
        3. (str) selected day for a city's bikeshare data
    returns:
        (str) the most popular trip (from start station to end station)
        for the city over the time period
    '''

    df = df_filter(city_file, month, day)
    df['Trip'] = 'FROM: ' + df['Start Station'] + '\nTO:   ' + df['End Station']
    trip = df['Trip'].mode().iloc[0]
    return trip


def users(city_file, month, day):
    '''returns the counts of each user type ('Customer' or 'Subscriber')
    for a specificed city and a predetermined time period

    args:
        1. (str) filename for a city's bikeshare data
        2. (str) selected month for a city's bikeshare data
        3. (str) selected day for a city's bikeshare data
    returns:
        1. (int) the count of 'Customer'
        2. (int) the count of 'Subscriber'
    '''

    df = df_filter(city_file, month, day)
    cust = df['User Type'].value_counts()['Customer']
    subs = df['User Type'].value_counts()['Subscriber']
    return cust, subs


def gender(city_file, month, day):
    '''returns the counts of each gender ('Female' or 'Male')
    for a specificed city and a predetermined time period

    args:
        1. (str) filename for a city's bikeshare data
        2. (str) selected month for a city's bikeshare data
        3. (str) selected day for a city's bikeshare data
    returns:
        1. (int) the count of 'Female'
        2. (int) the count of 'Male'
    '''

    df = df_filter(city_file, month, day)
    female = df['Gender'].value_counts()['Female']
    male = df['Gender'].value_counts()['Male']
    return female, male


def birth_years(city_file, month, day):
    '''returns the earliest, most recent, and most popular birth years
    for a specificed city and a predetermined time period

    args:
        1. (str) filename for a city's bikeshare data
        2. (str) selected month for a city's bikeshare data
        3. (str) selected day for a city's bikeshare data
    returns:
        1. (int) the oldest or the earliest birth year
        2. (int) the youngest or most recent birth year
        3. (int) the mode or most popular birth year
    '''

    df = df_filter(city_file, month, day)
    oldest = int(df['Birth Year'].min())
    youngest = int(df['Birth Year'].max())
    mode = int(df['Birth Year'].mode().iloc[0])
    return oldest, youngest, mode


def display_data(city_file):
    '''displays five lines of data if the user specifies that they would
    like to and continues to ask the user whether to see five more until 'no'

    args:
        (str) filename for a city's bikeshare data
    Returns:
        none
    '''

    msg = "\n\nWould you like to view individual trip data? Type 'yes' or 'no'.\n"
    display = input(msg)
    if display == 'yes': # start the sequence of work only if user enters 'yes'
        df = df_filter(city_file, None, None)
        loc = 0
    while display == 'yes':
        print(df[loc:loc + 5])
        display = input(msg)
        loc += 5


def timer(start_time):
    '''prints the timer output in between questions

    args:
        (builtin class from time() module) time when data analysis starts
    Returns:
        none
    '''

    print("\n\nThat took %s seconds." % (time.time() - start_time))
    print("Calculating the next statistic...")


def df_filter(city_file, month, day):
    '''1. opens the csv file for a city's bikeshare data
       2. loads data into a pandas dataframe
       3. filters by the specificed date as given by two inputs (month and day)
       4. returns the filtered dataframe

    args:
        (str) filename for a city's bikeshare data
    Returns:
        (pandas dataframe) filtered dataframe
    '''

    df = pd.read_csv(city_file)
    if month != None:
        df['Month'] = pd.to_datetime(df['Start Time']).apply(
                        lambda x: x.strftime("%B"))
        df = df[df['Month'] == months[int(month)]]
    if day != None:
        df['Day'] = pd.to_datetime(df['Start Time']).apply(
                        lambda x: x.strftime("%d"))
        df = df[df['Day'] == day]
    return df


def statistics():
    '''calculates and prints out the descriptive statistics about a city
    and time period specified by the user via raw input

    args:
        none
    Returns:
        none
    '''

    # Filter by city (Chicago, New York, Washington)
    city = get_city()

    # Filter by time period (month, day, none)
    time_period, month, day = get_time_period()
    if month != None:
        month_str = datetime.date(2018, int(month), 1).strftime('%B')
    else:
        month_str = 'all months'

    print('\nCalculating the first statistic...')

    # What is the most popular month for start time?
    if time_period == 'none':
        start_time = time.time()
        print("\n\nThe most popular month for start time is...")
        print(popular_month(city))
        timer(start_time)

    # What is the most popular day of week (Monday, Tuesday...) for start time?
    if time_period == 'none' or time_period == 'month':
        start_time = time.time()
        print("\n\nThe most popular day of week for {} is...".format(month_str))
        print(popular_day(city, month))
        timer(start_time)

    if day != None: # prints out the date selected by user
        print("\n\nYou have entered {} {}.".format(month_str, int(day)))
    else: # prints out the month selected by user or all months if none
        print("\n\nYou have selected {}.".format(month_str))

    # What is the most popular hour of day for start time?
    start_time = time.time()
    print("\n\nThe most popular hour of day is...")
    print(popular_hour(city, month, day))
    timer(start_time)

    # What is the total trip duration and average trip duration?
    start_time = time.time()
    total, average = trip_duration(city, month, day)
    total = int(total)
    hours = total // 3600
    minutes = (total % 3600) // 60
    seconds = total % 60
    print("\n\nThe total trip duration for start time is...")
    print("{} seconds OR {} hours {} minutes {} seconds".format(
        total, hours, minutes, seconds))
    print("\nThe average trip duration for start time is...")
    print('%.2f seconds' % average)
    timer(start_time)

    # What is the most popular start station and most popular end station?
    start_time = time.time()
    start_station, end_station = popular_stations(city, month, day)
    print("\n\nThe most popular start station is...\n{}".format(start_station))
    print("\nThe most popular end station is...\n{}".format(end_station))
    timer(start_time)

    # What is the most popular trip?
    start_time = time.time()
    pop_trip = popular_trip(city, month, day)
    print("\n\nThe most popular trip is...\n{}".format(pop_trip))
    timer(start_time)

    # What are the counts of each user type? 'Customer' or 'Subscriber'
    start_time = time.time()
    num_cust, num_subs = users(city, month, day)
    print("\n\nThe count of customers is...\n{}".format(num_cust))
    print("\nThe count of subscribers is...\n{}".format(num_subs))
    timer(start_time)

    # What are the counts of gender?
    start_time = time.time()
    num_female, num_male = gender(city, month, day)
    print("\n\nThe count of female among subscribers is...\n{}".format(
            num_female))
    print("\nThe count of male among subscribers is...\n{}".format(
            num_male))
    timer(start_time)

    # What are the earliest, most recent, and most popular birth years?
    start_time = time.time()
    oldest, youngest, birth_years_mode = birth_years(city, month, day)
    print("\n\nThe earliest birth year among subscribers is...\n{}".format(
            oldest))
    print("\n\nThe most recent birth year among subscribers is...\n{}".format(
            youngest))
    print("\n\nThe most popular birth year among subscribers is...\n{}".format(
            birth_years_mode))
    print("\n\nThat took %s seconds." % (time.time() - start_time))

    # Display five lines of data at a time if user would like to
    display_data(city)

    # Restart?
    restart = input("\n\nWould you like to restart? Type 'yes' or 'no'.\n")
    if restart.lower() == 'yes':
        statistics()


if __name__ == "__main__":
	statistics()
