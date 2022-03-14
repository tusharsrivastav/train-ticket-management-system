import pandas as pd
from trains import update_csvFile, display_info
from book import display_info
from passengers import open_pass_file, pass_display

# PASSENGER SEARCH
def pass_search():
      pass_df = open_pass_file()

      # Input PNR no to search
      pnr_search = int(input("Enter your PNR no.: "))
      print()

      condition = pass_df['pnr_no'] == pnr_search

      # List of details associated with given pnr no
      pnr_matches = pass_df[condition]

      rowCount = len(pnr_matches.values)
      colCount = len(pass_df.columns)

      # Display results
      print("{0} MATCH(ES) FOUND.".format(len(pnr_matches)))
      print()

      pass_display(pnr_matches, rowCount, colCount)
      

# TRAIN SEARCH
def train_search():
      # Opening and reading the trains' file
      trains_df = pd.read_csv("Trains_file.csv")

      # Updating values in CSV file
      trains_df = update_csvFile(trains_df)

      # Input train no to search
      train_no_search = int(input("Enter train no.: "))
      print()

      train_no_list = trains_df['train_number'].values

      if train_no_search not in train_no_list:
            print("This train does not exist")
      else:
            condition = trains_df['train_number'] == train_no_search

            train_matched = trains_df[condition]
            ind_value = train_matched.index[0]
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

            # Display results
            print("{0} MATCH(ES) FOUND.".format(len(train_matched)))
            print()
            display_info(trainNumber, trainName, trainType, trainRunningDays)
