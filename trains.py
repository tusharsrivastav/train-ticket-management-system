import pandas as pd
import os
from passengers import open_pass_file

def display_info(number, name, trainType, runningDays):
      print("Name of train : " + name)
      print("Type of train : " + trainType)
      print("Train no. : " + number)
      print("Runs on : " + runningDays)
      print()

def update_csvFile(trains_df):
      # Correcting mistakes in CSV file
      trains_df = trains_df.dropna()
      trains_df['train_origin'] = trains_df['train_origin'].str.replace(" ", "")
      trains_df['train_destination'] = trains_df['train_destination'].str.replace(" ", "")
      trains_df['train_origin'] = [c.upper() for c in trains_df['train_origin']]
      trains_df['train_destination'] = [c.upper() for c in trains_df['train_destination']]
      trains_df['train_type'] = [c.capitalize() for c in trains_df['train_type']]

      # Creating a new column for seats available in trains
      trains_df.insert(4, 'seats_available', 10)

      # UPDATING TICKET COUNT

      # Passengers' Data
      if os.path.exists('passengers.csv'):
            pass_df = open_pass_file()
      else:
            passengers_df = pd.DataFrame({
                  "pnr_no" : '',
                  "name" : '',
                  "age" : '',
                  "gender" : '',
                  "phone_no" : '',
                  "train_name" : '',
                  "train_number" : '',
                  "train_type" : '',
                  "journey_day" : '',
                  "journey_class" : '',
                  "coach" : '',
                  "seat" : '',
                  "ticket_fare" : '',
                  "train_departure_time" : '',
                  "train_reach_time" : '',
                  "origin" : '',
                  "destination" : '',
                  }, index = [i for i in range(1)])
            passengers_df.to_csv('passengers.csv', index=False)
            pass_df = open_pass_file()

      booked_trainNames = set()
      booked_trainNamesList = []
      booked_trainDict = {}

      for train in pass_df['train_name']:
            booked_trainNamesList.append(train)
            booked_trainNames.add(train)
            
      for train in booked_trainNames:
            #print(train)
            booked_train_seatCount = 0
            for bookedTrain in booked_trainNamesList:
                  if train == bookedTrain:
                        #print(train, booked_train_seatCount, " +1")
                        booked_train_seatCount += 1
            booked_trainDict[train] = booked_train_seatCount      

      # Trains' Data
      av_trainDict = {}

      for train in trains_df['train_name']:
            av_trainDict[train] = 10


      # Updating data in dictionary
      new_dict = {}

      for train in trains_df['train_name']:
            if booked_trainDict.get(train) != None:
                  av_seats = av_trainDict[train] - booked_trainDict[train]
                  new_dict[train] = av_seats

      # Updating data in Trains' dataframe

      for train in new_dict:
            trains_df.loc[trains_df.train_name == train, "seats_available"] = new_dict[train]


      # Creating a new column for available status of trains
      trains_df.insert(4, 'available_status',
                       trains_df['seats_available'] .apply(lambda x : 'Not available' if x == 0 else 'Available'))

      return trains_df

def trains_list():
      # Opening and reading the trains' file
      trains_df = pd.read_csv('Trains_file.csv')
      trains_df = trains_df.dropna()
      
      # DISPLAYING TRAINS' INFO TO USER
      rowCount = len(trains_df)
      colCount = len(trains_df.columns)


      columnHeads = ["Name of train", "Train no.", "Type of train",
                     "Runs on", "Departure time", "Arrival time",
                     "Origin", "Destination"]

      for row in range(rowCount):
            print(row +1, end='. ')

            print(trains_df['train_name'].iloc[row])
            for i in range(len(trains_df['train_name'].iloc[row]) +4):
                  print("~", end='')
            print()
            for col in range(1, colCount):
                  col_head = trains_df.columns[col]
                  print(columnHeads[col], trains_df[col_head].iloc[row], sep=': ')
            print()
            print()

# ADDING A TRAIN
def add_train():
      trains_df = pd.read_csv('Trains_file.csv')
      
      # Defining empty lists
      name = []
      number = []
      trainType = []
      rundays = []
      depart = []
      arrival = []
      origin = []
      destination = []

      # INPUT TRAIN'S INFO
      train_name = input("Name of train: ")

      # Checking if train no. is valid and doesn't exist in the dataframe already
      rerun = True
      while(rerun == True):
            train_no = int(input("Train no.: "))
            train_noLen = len(str(train_no))
            train_noVals = trains_df['train_number'].loc[trains_df['train_number'] == train_no].values

            if train_noLen != 5:
                  print("Train no. should of 5 digits")
                  rerun = True
            else:
                  if train_no not in train_noVals:
                        rerun = False
                  else:
                        print("This train no. already exists in the database")
                        rerun = True
                  
      train_no = int(train_no)
      
      train_type = input("Type of train: ")
      train_run_days = input("Runninig days(M/T/W/F/S): ")

      # Departure and arrival time
      print("Departure time")
      depart_time_hr = int(input("Hour: "))
      depart_time_min = int(input("Minutes: "))
      depart_time = str(depart_time_hr) + ":" + str(depart_time_min)

      print("Arrival time")
      arrival_time_hr = int(input("Hour: "))
      arrival_time_min = int(input("Minutes: "))
      arrival_time = str(arrival_time_hr) + ":" + str(arrival_time_min)
      train_origin = input("Origin: ")
      train_destination = input("Destination: ")

      # Adding values to lists
      name.append(train_name)
      number.append(train_no)
      trainType.append(train_type)
      rundays.append(train_run_days.upper())
      depart.append(depart_time)
      arrival.append(arrival_time)
      origin.append(train_origin)
      destination.append(train_destination)

      # Creating a dataframe
      trains_df = pd.DataFrame({
            'train_name' : name,
            'train_number' : number,
            'train_type' : trainType,
            'train_run_days' : rundays,
            'train_departure_time' : depart,
            'train_arrival_time' : arrival,
            'train_origin' : origin,
            'train_destination' : destination      
            })

      # Creating CSV file to contain the dataframe
      trains_df.to_csv('Trains_file.csv', mode='a',
                       header = not os.path.exists('Trains_file.csv'), index=False)

      # Success message
      print("\nTrain added to the database successfully!\n")

# DELETING A TRAIN
def dlt_train():
      if not os.path.exists("Trains_file.csv"):
            print("There is no data to delete")
      else:
            # Opening train file
            trains_df = pd.read_csv("Trains_file.csv")
            
            # Input train no. of train to delete
            train_no_dlt = int(input("Train no.: "))
            
            # Deleting row where the train no. matches the input
            train_no_list = trains_df['train_number'].values

            if train_no_dlt not in train_no_list:
                  print("This train does not exist")
                  
            else:
                  trains_df.drop(trains_df[trains_df.train_number == train_no_dlt].index, inplace=True)
                  
                  # Updating the train file
                  trains_df.to_csv('Trains_file.csv', mode='w',
                                   header = True, index=False)

                  # DELETING PASSENGER'S DATA ASSOCIATED WITH DELETED TRAIN
                  if os.path.exists("passengers.csv"):
                        pass_df = pd.read_csv("passengers.csv")

                        # List of train numbers in passengers file
                        pass_tno_list = pass_df['train_number'].values

                        if train_no_dlt in pass_tno_list:
                              pass_df.drop(pass_df[pass_df.train_number == train_no_dlt].index, inplace=True)
                              
                              # Updating the passenger file
                              pass_df.to_csv('passengers.csv', mode='w',
                                             header = True, index=False)

                  # Success message
                  print("\nTrain deleted from the database successfully!\n")
            



