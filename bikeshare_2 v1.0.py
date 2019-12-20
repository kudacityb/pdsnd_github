import time
import pandas as pd
import numpy as np
#Define which cities can be entered as well as files that are included
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
month='blank'
day='blank'
#get filter is function for inputs
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    cities = list(CITY_DATA.keys())

    city = input('Please enter the city (chicago, new york city, washington): ')
    while not(city.lower() in cities):
        city = input('Please enter the city (chicago, new york city, washington): ')
    city = city.lower()       
    # get user input for month (all, january, february, ... , june)
    month = input('Please enter the month (all, january, february, march, april, may, june, july, august, september, october, november, december) :')   
    while not(month.lower() in ["all","january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]):
        month = input('Please enter the month (all, january, february, march, april, may, june, july, august, september, october, november, december) :')    
    month = month.lower()  
        
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Please enter the (all, monday, tuesday, wednesday, thursday, friday, saturday, sunday): ')
    while not(day.lower() in ["all","monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]):
        day = input('Please enter the (all, monday, tuesday, wednesday, thursday, friday, saturday, sunday): ')  
    day = day.lower()

    print('-'*40)
    return city, month, day

#load data is function to upload data and filter based on user input
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time']=pd.to_datetime(df['Start Time'])
     
    if month != 'all':
        df['MonthName']=df['Start Time'].dt.strftime('%B')    
        dfun = df
        month = month.capitalize()
        df = df[df['MonthName']==month]
    
    if day != 'all':
        weekDays = {"monday":0,"tuesday":1, "wednesday":2, "thursday":3, "friday":4, "saturday":5, "sunday":6}
        daynum = weekDays[day]
        df['DayOfWeek']=df['Start Time'].dt.weekday
        df = df[df['DayOfWeek']==daynum]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df['MonthName'] = df['Start Time'].dt.strftime('%B')       
    mHistogram = df['Start Time'].dt.strftime('%B').unique()
    mMostColumn = df[df['MonthName']==mHistogram[0]]
    if mHistogram.shape[0]==1:
        print('Data was filtered on month therefore data for comparison of months are not available')
    else: 
        print(mHistogram[0],' is the most common month which occurs ', mMostColumn.count()[1], ' times')


    # display the most common day of week
    df['DayOfWeek']= df['Start Time'].dt.weekday
    dHistogram = df['DayOfWeek'].unique()
    dMostColumn = df[df['DayOfWeek']==dHistogram[0]]
    weekDaysList = ("monday","tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")
    if dHistogram.shape[0]==1:
        print('Data was filtered on day therefore data for comparison of days of week are not available')
    else: 
        print(weekDaysList[dHistogram[0]],' is the most common day which occurs ', dMostColumn.count()[1], ' times')

    # display the most common start hour
    hHistogram = df['Start Time'].dt.strftime('%H').unique()
    df['Hour'] = df['Start Time'].dt.strftime('%H')
    hMostColumn = df[df['Hour']==hHistogram[0]]
    print(hHistogram[0],':00 is the most common hour of rental which occurs ', hMostColumn.count()[1], ' times')
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    ssHistogram = df['Start Station'].unique()
    ssMostColumn = df[df['Start Station']==ssHistogram[0]]
    print(ssHistogram[0],'is the most common start station of rentals which occurs ', ssMostColumn.count()[1], ' times')



    # display most commonly used end station
    esHistogram = df['End Station'].unique()
    esMostColumn = df[df['End Station']==esHistogram[0]]
    print(esHistogram[0],'is the most common end station of rentals which occurs ', esMostColumn.count()[1], ' times')



    # display most frequent combination of start station and end station trip
    df['Route'] = df['Start Station'] + ' to ' + df['End Station']
    rHistogram = df['Route'].unique()
    rMostColumn = df[df['Route']==rHistogram[0]]
    print(rHistogram[0],'is the most common route of rentals which occurs ', rMostColumn.count()[1], ' times')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    totaltime = sum(df['Trip Duration'])
    print(totaltime/60, 'minutes were spent renting the bikes')


    # display mean travel time
    averagetime = df['Trip Duration'].mean()
    print(averagetime/60,'minutes was the average rental time')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    utHistogram = df['User Type'].value_counts(dropna=False)
    print('User Type     Frequency of Type \n',utHistogram,'\n')


    # Display counts of gender
    if 'Gender' in df.columns:
        gHistogram = df['Gender'].value_counts(dropna=False)
        print('Gender         Frequency of Gender \n',gHistogram,'\n')
    else:
        print('Gender information not available in dataset')


    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliestBirthYear = df['Birth Year'].min()
        recentBirthYear = df['Birth Year'].max()
        commonBirthYear = df['Birth Year'].unique()[0]
        print('The oldest customer was born in ',np.trunc(earliestBirthYear))
        print('The youngest customer was born in ',np.trunc(recentBirthYear))
        print('THe most common birth year is ',np.trunc(commonBirthYear))
    else:
        print('Birth Year information not in data')
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        rawdata = input('\nWould you like to see 5 lines of raw data? yes or no.\n').lower()
        while rawdata != 'yes' and rawdata != 'no':
            rawdata = input('\nWould you like to see 5 lines of raw data? yes or no.\n').lower()
        if rawdata == 'yes':
            pd.set_option('display.max_columns', None) 
            print(df[:5])

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
