import pandas as pd
import os
import warnings
import random
from trains import update_csvFile, display_info
from passengers import open_pass_file, pass_display

# Suppressing warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
pd.options.mode.chained_assignment = None  # default='warn'


# Functions
def chooseClass():
      classes = {
            "1": "Anubhati Class(EA)",
            "2": "AC First Class(1A)",
            "3": "Exec. Chair Car(EC)",
            "4": "AC 2 Tier(2A)",
            "5": "First Class(FC)",
            "6": "AC 3 Tier(3A)",
            "7": "AC 3 Economy(3E)",
            "8": "AC Chair Car(CC)",
            "9": "Sleeper(SL)"
      }
      options = ("1", "2", "3", "4", "5", "6", "7", "8", "9")

      print()
      print("Choose a Class")
      print("--------------")
      print("1. Anubhati Class(EA)",
            "2. AC First Class(1A)",
            "3. Exec. Chair Car(EC)",
            "4. AC 2 Tier(2A)",
            "5. First Class(FC)",
            "6. AC 3 Tier(3A)",
            "7. AC 3 Economy(3E)",
            "8. AC Chair Car(CC)",
            "9. Sleeper(SL)", sep='\n')
      print()

      rerun = True
      while(rerun == True):
            class_select = input("Choose a class(1-9): ")
            if str(class_select) not in options:
                  print("Select a valid option")
                  print()
                  rerun = True
            else:
                  journey_class = classes[class_select]
                  rerun = False       
      return journey_class


def calc_fare(jclass, trainType):
      base = 400
      sup_charge = 0

      # Fare for diff class
      if "EA" in jclass or "1A" in jclass or "EC" in jclass:
            reservation_charge = 60
            if trainType == 'SUPERFAST':
                  sup_charge += 75
      elif "2A" in jclass or "FC" in jclass:
            reservation_charge = 50
            if trainType == 'SUPERFAST':
                  sup_charge += 45
      elif "3A" in jclass or "3E" in jclass:
            reservation_charge = 40
            if trainType == 'SUPERFAST':
                  sup_charge += 45
      elif "CC" in jclass:
            reservation_charge = 15
            if trainType == 'SUPERFAST':
                  sup_charge += 15
      elif "SL" in jclass:
            reservation_charge = 20
            if trainType == 'SUPERFAST':
                  sup_charge += 15

      # GST Charge
      gst = (base + reservation_charge + sup_charge)*0.05

      # Total Fare
      total_fare = base + reservation_charge + sup_charge + gst

      return total_fare

def book_tickets():
      print("BOOKING TICKETS")
      print("~~~~~~~~~~~~~~~")

      # Opening and reading the trains' file
      trains_df = pd.read_csv("Trains_file.csv")

      # Updating values in CSV file
      trains_df = update_csvFile(trains_df)

      # Inputting values from the user
      origin_select = str(input("Select origin of your journey: "))
      origin_select = origin_select.upper()
      destination_select = str(input("Select destination of your journey: "))
      destination_select = destination_select.upper()

      origin_select = origin_select.replace(" ", "")
      destination_select = destination_select.replace(" ", "")

      # Checks if the origin and destination matches any train's schedule
      condition = (trains_df['train_origin'] == origin_select) \
      & (trains_df['train_destination'] == destination_select) \
      & (trains_df['available_status'] == "Available")

      av_trains_df = trains_df[condition]
      av_trains = av_trains_df.values


      # Checking whether a train is available or not
      if len(av_trains) == 0:
            print("Sorry! No trains are available.")
            cont = True
      else:
            cont = False

      
      while(cont == False):

            print()
            print("{0} train(s) found!".format(len(av_trains)))
            print()


            # FOR MULTIPLE AVAILABLE TRAINS
            if len(av_trains) > 1:
                  sno = 1
                  sno_list = []
                  
                  for train in av_trains:
                        ind_value = av_trains_df.index[sno-1]
                        train_info = trains_df.iloc[ind_value]

                        
                        # Assigning train's info to variables
                        trainName = str(train_info[0])
                        trainNumber = str(train_info[1])
                        trainType = str(train_info[2])
                        trainRunningDays = str(train_info[3])

                        # Removing duplicate running days
                        x = trainRunningDays.replace(",", "")
                        x = x.replace(" ", "")
                        trainRunningDays = list(sorted(set(x), key=x.index))

                        string = ""
                        for i in trainRunningDays:
                              string += i + " "

                        trainRunningDays = string

                        # Displaying information to the user
                        print(str(sno) + ".", end=' ')
                        display_info(trainNumber, trainName, trainType,
                                     trainRunningDays)
                        
                        sno_list.append(sno)
                        sno += 1
                  
                  # Train selection
                  train_select = int(input("Select a train: "))

                  rerun = True
                  while (rerun == True):
                        if train_select not in sno_list:
                              print("\nEnter a valid option.\n")
                              rerun = True
                        else:
                              rerun = False
                              cont = False

                              print("\nSELECTED TRAIN")
                              
                              ind_value = av_trains_df.index[train_select - 1]
                              train_info = trains_df.iloc[ind_value]
            
                              # Assigning train's info to variables
                              trainName = str(train_info[0])
                              trainNumber = str(train_info[1])
                              trainType = str(train_info[2])
                              trainRunningDays = str(train_info[3])
                              trainStatus = str(train_info[4])
                              trainTicketsAvail = train_info[5]
                              trainDepartureTime = str(train_info[6])
                              trainArrivalTime = str(train_info[7])
                              trainOrigin = str(train_info[8])
                              trainDestination = str(train_info[9])
            
                              display_info(trainNumber, trainName, trainType,
                                           trainRunningDays)
                              
                              journey_class = chooseClass()
            
            # FOR SINGLE TRAIN AVAILABLE
            if len(av_trains) == 1:
                  
                  # Finding the row of the available train
                  ind_value = av_trains_df.index[0]
                  train_info = trains_df.iloc[ind_value]

                  # Assigning train's info to variables
                  trainName = str(train_info[0])
                  trainNumber = str(train_info[1])
                  trainType = str(train_info[2])
                  trainRunningDays = str(train_info[3])
                  trainStatus = str(train_info[4])
                  trainTicketsAvail = train_info[5]
                  trainDepartureTime = str(train_info[6])
                  trainArrivalTime = str(train_info[7])
                  trainOrigin = str(train_info[8])
                  trainDestination = str(train_info[9])

                  # Removing duplicate running days
                  x = trainRunningDays.replace(",", "")
                  x = x.replace(" ", "")
                  trainRunningDays = list(sorted(set(x), key=x.index))

                  string = ""
                  for i in trainRunningDays:
                        string += i + " "
                  
                  trainRunningDays = string
                  
                  # Displaying information to the user
                  display_info(trainNumber, trainName, trainType,
                               trainRunningDays)

                  # Train selection confirmation
                  rerun = True
                  while(rerun == True):
                        select = input("Select this train?(Y/N): ")
                        select = select.lower()

                        if select != "y" and select != "n":
                              print("Enter a valid character")
                              rerun = True
                        elif select == "n":
                              rerun = False
                              
                              contLoop = False
                              return contLoop
                        else:
                              rerun = False
                              cont = False
                              journey_class = chooseClass()

            return journey_class, trainName, trainNumber, trainType, \
                   trainRunningDays, trainStatus, trainTicketsAvail, \
                   trainDepartureTime, trainArrivalTime, trainOrigin, \
                   trainDestination
            

def day_selection(selectedDay, trainBookedInfo, trainTicketsAvail):
      trainBookedRun = trainBookedInfo[4]
      trainBookedRun = set(trainBookedRun)

      days_dict = {
            "M" : "Monday",
            "T" : "Tuesday",
            "W" : "Wednesday",
            "F" : "Friday",
            "S" : "Saturday"
      }

      selectedDay = selectedDay.upper().replace(" ", "")
      selectedDayDisplay = selectedDay[0]

      if selectedDayDisplay not in trainBookedRun or selectedDay == "THURSDAY" or selectedDay == "SUNDAY":
            print("Sorry! This train does not run on {0}".format(days_dict[selectedDayDisplay]))
            contLoop = False
            return contLoop
      else:      
            for day in trainBookedRun:
                  if selectedDay[0] == day:
                        print()
                        print("Seats available : " + str(trainTicketsAvail))
                        print()
                        return days_dict[day]
                  else:
                        pass


def user_info_input(trainBookedInfo, selectedDay, trainTicketsAvail,
                    journeyClass):
      # Inputting information
      passengerCount = int(input("No. of passengers : "))

      # Passengers' Data
      if os.path.exists('passengers.csv'):
            pass_df = pd.read_csv('passengers.csv')
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
            pass_df = pd.read_csv('passengers.csv')

      # Checking how many tickets are available
      if trainTicketsAvail < passengerCount:
            print("Sorry! Only {0} seat(s) avialable.".format(trainTicketsAvail))
            contLoop = False
            return contLoop
      else:
            # Creating empty lists to store data
            pnrCol = []
            namesCol = []
            ageCol = []
            genderCol = []
            phoneCol = []
            coachCol = []
            seatCol = []
            fareCol = []
            train = trainBookedInfo

# Checking if phone value is valid and doesn't exist in the dataframe already
            rerun = True
            while(rerun == True):
                  phone = int(input("Phone no.: "))
                  phoneLen = len(str(phone))
                  phoneVals = pass_df['phone_no'].loc[pass_df['phone_no']
                                                      == phone].values

                  if phoneLen != 10:
                        print("Phone no. should of 10 digits")
                        rerun = True
                  else:
                        if phone not in phoneVals:
                              rerun = False
                        else:
                              print("This phone no. already exists in the database")
                              rerun = True
                        
            phone = int(phone)
            #print("Phone no. is {0} .".format(phone))

            # Assigning PNR no.
            rerun = True
            while(rerun == True):
                  pnr = random.randrange(1000000000, 9999999999)
                  
                  pnrVals = pass_df['pnr_no'].loc[pass_df['pnr_no'] == pnr].values

                  if pnr not in pnrVals:
                        rerun = False
                  else:
                        rerun = True

            
            # Taking info for each passenger
            for passenger in range(passengerCount):
                  print()
                  print("Passenger {0}".format(passenger + 1))
                  name = str(input("Name: "))
                  name = name.capitalize()
                  age = int(input("Age: "))
                  

                  # Checks if the gender value is valid
                  rerun = True
                  while(rerun == True):
                        gender = str(input("Male/Female: "))
                        gender = gender.lower().replace(" ", "")

                        if gender != "male" and gender != "female":
                              print("Enter a valid option")
                              rerun = True
                        else:
                              rerun = False
                  gender = gender.capitalize()

                  # Assigning PNR no. and seat no. to passengers
                  coachOpt = {1: "A", 2: "B", 3: "C", 4: "D"}
                  rerun = True
                  while(rerun == True):
                        seat = random.randrange(10, 70)
                        coachRand = random.randrange(1, 4)
                        coach = coachOpt[coachRand]

                        coachVals = pass_df['coach'].loc[pass_df['seat'] == seat].values
                        seatVals = pass_df['seat'].loc[pass_df['coach'] == coach].values

                        if seat not in seatVals and coach not in coachVals:
                              rerun = False
                        else:
                              rerun = True

                  # Calculating fare for each passenger
                  fare = calc_fare(journeyClass, train[3])

                  # Storing data in lists
                  pnr_col = pnrCol.append(pnr)
                  names_col = namesCol.append(name)
                  age_col = ageCol.append(age)
                  gender_col = genderCol.append(gender)
                  phone_col = phoneCol.append(phone)
                  coach_col = coachCol.append(coach)
                  seat_col = seatCol.append(seat)
                  fare_col = fareCol.append(fare)
            
            # Creating a dataframe
            passengers_df = pd.DataFrame({
                  "pnr_no" : pnrCol,
                  "name" : namesCol,
                  "age" : ageCol,
                  "gender" : genderCol,
                  "phone_no" : phoneCol,
                  "train_name" : train[1],
                  "train_number" : train[2],
                  "train_type" : train[3],
                  "journey_day" : selectedDay,
                  "journey_class" : journeyClass,
                  "coach" : coachCol,
                  "seat" : seatCol,
                  "ticket_fare" : fareCol,
                  "train_departure_time" : train[7],
                  "train_reach_time" : train[8],
                  "origin" : train[9],
                  "destination" : train[10],
                  })

            # Creating CSV file to contain the dataframe
            passengers_df.to_csv('passengers.csv', mode='a', header = not os.path.exists('passengers.csv'), index=False)



            # Success message
            print()
            print("TICKETS BOOKED SUCCESSFULLY!!")
            print()

            pass_df = open_pass_file()
            pass_df = pass_df.loc[pass_df['phone_no'] == phone]

            # Displaying tickets to the user
            rowCount = len(pass_df)
            colCount = len(pass_df.columns)

            pass_display(pass_df, rowCount, colCount)

            total_price = 0
            for row in range(rowCount):
                  total_price += pass_df['ticket_fare'].iloc[row]
                  
            print("TOTAL FARE : ₹{0}".format(total_price))
            print()
            

# Cancel a ticket
def cancel_ticket():
      if not os.path.exists("passengers.csv"):
            print("No ticket has been booked yet.")
      else:
            # Opening passenger file
            pass_df = pd.read_csv("passengers.csv")
            
            # Input PNR no. of ticket to cancel
            pnr = float(input("PNR no.: "))
            
            condition = pass_df['pnr_no'] == pnr

            # List of details associated with given pnr no
            pnr_matches = pass_df[condition]

            if pnr not in pnr_matches.values:
                  print("This PNR no is not valid")
                  cont = False
                  
            else:
                  rowCount = len(pnr_matches)
                  colCount = len(pass_df.columns)

                  # Display matched tickets
                  print("{0} MATCH(ES) FOUND.".format(len(pnr_matches)))
                  print()

                  pass_display(pnr_matches, rowCount, colCount)

                  confirm = input("Do you want to cancel the ticket(s)?(Y/N):  ")
                  print()
                  confirm = confirm.lower()
                  
                  if confirm != 'y':
                        cont = False                     
                  else:
                        pass_df.drop(pass_df[pass_df.pnr_no == pnr].index, inplace=True)
                        
                        # Updating the train file
                        pass_df.to_csv('passengers.csv', mode='w', header = True, index=False)

                        # Success message
                        print("\nTicket successfully cancelled!\n")

                        cont = False
            
            return cont


