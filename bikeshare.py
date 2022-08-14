import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
  'new york city': 'new_york_city.csv',
  'washington': 'washington.csv' }

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
  city = input('Would you like to see data for Chicago, New York, or Washington?\n').lower()
  
  while True:        
    if city in CITY_DATA:
      city = CITY_DATA[city]            
      break;
    print("That's not available option")
    print('Select from "Chicago", "New york city", "Washington"')
    city = input('Would you like to see data for Chicago, New York, or Washington?\n').lower()

  # get user input for filter
  filter = input('Would you like to filter the data by month, day, or not at all (none / both)?\n').lower()
  
  while True:
    if filter in ['month', 'day', 'none', 'both']: break
    print("That's not available option")
    print('Select from "Month", "Day", "None", "Both"')
    filter = input('Would you like to filter the data by month, day, or not at all (none / both)?\n').lower()

  month = None
  day = None

  if filter == 'month' or filter == 'both':
    # get user input for month 
    while True:
      month = input('Which month - January, February, March, April, May, or June?\n').lower()
      if month in ['all', 'january', 'february', 'march', 'april', 'may' ,'june']: break
      print("That's not available option")
      print('Select from "January", "February", "March", "April", "May", "June"')

  if filter == 'day' or filter == 'both':
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
      day = input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n').lower()
      if day in ['all', 'monday', 'tuesday', 'wednesday','thursday', 'friday', 'saturday', 'sunday']: break
      print("That's not available option")
      print('Select from "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"')

  print('-'*40) ## divider
  return city, month, day

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
  df = pd.read_csv(city)

  # convert the Start Time column to datetime
  df['Start Time'] = pd.to_datetime(df['Start Time'])
  
  # extract month and day of week from Start Time to create new columns
  df['month'] = df['Start Time'].dt.month
  df['hour'] = df['Start Time'].dt.hour
  df['day_of_week'] = df['Start Time'].dt.dayofweek
  df['day'] = df['Start Time'].dt.day_name()

  if month != 'all' and month is not None:
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    month = months.index(month) + 1

    # filter by month to create the new dataframe
    df = df[df['month']==month]

  if day != 'all' and day is not None: 
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = days.index(day)

    # filter by day of week to create the new dataframe
    df = df[df['day_of_week']==day]

  return df

def time_stats(df):
  """Displays statistics on the most frequent times of travel."""

  print('\nCalculating The Most Frequent Times of Travel...\n')
  start_time = time.time()

  # display the most common month
  popular_month = df['month'].mode()[0]
  print('Most Popular Start Month: ', popular_month)

  # display the most common day of week
  popular_day = df['day'].mode()[0]
  print('Most Popular Start Day: ', popular_day)
  
  # display the most common start hour
  popular_hour = df['hour'].mode()[0]
  print('Most Popular Start Hour: ', popular_hour)
  
  print("\nThis took %s seconds." % round(time.time() - start_time, 3))
  print('-'*40)

def station_stats(df):
  """Displays statistics on the most popular stations and trip."""

  print('\nCalculating The Most Popular Stations and Trip...\n')
  start_time = time.time()

  # display most commonly used start station
  print('Most Popular Start Station: ', df['Start Station'].mode()[0])

  # display most commonly used end station
  print('Most Popular End Station: ', df['End Station'].mode()[0])

  # display most frequent combination of start station and end station trip
  
  df['trip'] = 'From: [' + df['Start Station'] + '] To: [' + df['End Station'] + ']'
  
  print('Most Popular Trip: ', df['trip'].mode()[0])

  print("\nThis took %s seconds." % round(time.time() - start_time, 3))
  print('-'*40)

def trip_duration_stats(df):
  """Displays statistics on the total and average trip duration."""
  
  print('\nCalculating Trip Duration...\n')
  start_time = time.time()
  
  # display total travel time
  
  print('Total Travel Time: ', np.sum(df['Trip Duration']))
  
  # display mean travel time
  print('Average Travel Time: (Rounded)', round(np.mean(df['Trip Duration']), 3) )
  
  print("\nThis took %s seconds." % round(time.time() - start_time, 3))
  print('-'*40)


def user_stats(df):
  """Displays statistics on bikeshare users."""
  
  print('\nCalculating User Stats...\n')
  start_time = time.time()
  
  # Display counts of user types
  print('Counts of User type: ')
  print(df['User Type'].value_counts())
  print('-' * 10)
  
  print('Counts of User gender: ')
  if 'Gender' not in df.columns:
    print('this data does not have Gender data')
  else:
    # Display counts of gender
    print(df['Gender'].value_counts())
  
  # Display earliest, most recent, and most common year of birth
  print('-' * 10)
  
  print('Distribution of User Birth year: ')
  
  if 'Birth Year' not in df.columns:
    print('this data does not have Birth data')
  else:
    # Display earliest, most recent, most common year of birth 
    print('Most Earliest birth year: ')
    print(int(df['Birth Year'].sort_values(ascending=True).iloc[0]))
    
    print('Most Recent birth year: ')
    print(int(df['Birth Year'].sort_values(ascending=False).iloc[0]))
    
    print('Most Common birth year: ')
    print(int(df['Birth Year'].mode()[0]))

  print("\nThis took %s seconds." % round(time.time() - start_time, 3))
  print('-'*40)

def main():
  while True:
    city, month, day = get_filters()
    
    df = load_data(city, month, day)
    
    # backup for print
    df_b = pd.read_csv(city)
      
    time_stats(df)
    station_stats(df)
    trip_duration_stats(df)
    user_stats(df)

    idx = 0
    
    # get user input for view data
    
    view = input('\nWould you like to view individual trip data? Type "Yes" or "No"\n').lower()  
      
    while True:
      if view == 'yes':
        print(df_b.iloc[idx:idx+5, ].to_string())
        idx = idx + 5    
      
      if view == 'no':
        break
      
      if view not in ['yes', 'no']:
        print("That's not available option")
        print('Select from "Yes", "No"')
      view = input('\nWould you like to view individual trip data? Type "Yes" or "No"\n').lower()
          
    restart = input('\nWould you like to restart? Enter yes or no.\n')
    if restart.lower() != 'yes': break


if __name__ == "__main__":
  main()
