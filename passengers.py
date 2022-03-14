import pandas as pd
import os

def open_pass_file():
      pass_df = pd.read_csv('passengers.csv')

      # Correcting null values & negative values
      pass_df = pass_df.dropna()
      pass_df[['age', 'phone_no', 'train_number', 'seat', 'pnr_no', 'ticket_fare']] = pass_df[['age', 'phone_no', 'train_number', 'seat', 'pnr_no', 'ticket_fare']].astype('int64').apply(lambda x : abs(x))

      return pass_df
      
def passengers_list():
      # Opening and reading passengers' file
      if os.path.exists('passengers.csv'):
            pass_df = open_pass_file()
            
            # DISPLAYING PASSENGERS' INFO TO USER
            rowCount = len(pass_df)
            colCount = len(pass_df.columns)
            
            print("PASSENGERS' LIST")
            print("----------------")
            print()

            pass_display(pass_df, rowCount, colCount)
            
      else:
            print("No user data yet.")


def pass_display(pass_df, rowCount, colCount):
      columnHeads = ["PNR no.", "Name of passenger", "Age", "Sex", "Phone no.", "Train Name", "Train no.", "Type of train", "Day of Journey", "Journey Class", "Coach", "Seat no.", "Ticket Fare", "Departure time", "Reachs destination on", "Origin", "Destination"]

      for row in range(rowCount):
            print(row +1, end='. ')
            seat_no = str(pass_df['coach'].iloc[row]) + str(pass_df['seat'].iloc[row])
            fare = "₹" + str(pass_df['ticket_fare'].iloc[row])

            for col in range(15):
                  col_head = pass_df.columns[col]

                  if col != 10 and col != 11 and col != 12:
                        print(columnHeads[col], pass_df[col_head].iloc[row], sep=': ')
                  elif col == 10:
                        print("Seat no.", seat_no, sep=': ')
                  elif col == 12:
                        print("Ticket Fare", fare, sep=': ')

            print()
