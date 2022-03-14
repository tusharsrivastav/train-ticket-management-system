from trains import trains_list, add_train, dlt_train
from passengers import passengers_list
import book
from search import pass_search, train_search


def train_file():
      print("TRAIN FILE")
      print("----------")
      print("1. Add a train")
      print("2. Delete a train")
      print("3. Display all trains")
      print()

      sub_opt = int(input("Select any one option: "))
      print()

      if sub_opt == 1:
            add_train()
      elif sub_opt == 2:
            dlt_train()
      elif sub_opt == 3:
            trains_list()
      else:
            print()
            print("Select a valid option")
            print()
            report()


def report():
      print("REPORT")
      print("------")
      print("1. Train Report")
      print("2. Passenger Report")
      print()

      sub_opt = int(input("Select any one option: "))
      print()

      if sub_opt == 1:
            train_report()
      elif sub_opt == 2:
            pass_report()
      else:
            print()
            print("Select a valid option")
            print()
            report()

def train_report():
      print("TRAIN REPORT")
      print("------------")
      print("1. Search for a train")
      print("2. Display all the trains")
      print()

      sub_opt = int(input("Select any one option: "))
      print()

      if sub_opt == 1:
            train_search()
      elif sub_opt == 2:
            trains_list()
      else:
            print()
            print("Select a valid option")
            print()
            train_report()

def pass_report():
      print("PASSENGER REPORT")
      print("------------")
      print("1. Search for a passenger")
      print("2. Display all passengers")
      print()

      pass_sub_opt = int(input("Select any one option: "))
      print()

      if pass_sub_opt == 1:
            pass_search()
      elif pass_sub_opt == 2:
            passengers_list()
      else:
            print()
            print("Select a valid option")
            print()
            pass_report()

def menu():
      cont = True
      while(cont == True):
            print("WELCOME USER!!")
            print("-------------")
            print()
            print("1. Train file")
            print("2. Book a ticket")
            print("3. Cancel a ticket")
            print("4. Report")
            print("5. Quit")

            print()
            opt = int(input("Select any one option : "))
            print()

            if opt == 1:
                  train_file()

            elif opt == 2:
                  # Selecting train and class
                  trainBookedInfo = book.book_tickets()
                  #print(trainBookedInfo)

                  # Continue
                  cont = trainBookedInfo
                  if cont == False or cont == None:
                        cont = True
                        rerun = True
                        while(rerun == True):
                              print()
                              select = input("Do you want to go to main menu?(Y/N): ")
                              print()
                              select = select.lower()

                              if select != "y" and select != "n":
                                    print("Enter a valid character")
                                    rerun = True
                              elif select == "n":
                                    rerun = False
                                    contLoop = False
                              else:
                                    menu()
                        if contLoop == False:
                              break

                  print()

                  # Selecting day of journey
                  selectedDay = input("Select the day of journey : ")
                  trainTicketsAvail = trainBookedInfo[6]

                  selectedDay = book.day_selection(selectedDay, trainBookedInfo,
                                                   trainTicketsAvail)
                  #print("Day : " + str(selectedDay))
                  cont = selectedDay

                  if cont == False:
                        cont = True
                        rerun = True
                        while(rerun == True):
                              print()
                              select = input("Do you want to go to main menu?(Y/N): ")
                              print()
                              select = select.lower()

                              if select != "y" and select != "n":
                                    print("Enter a valid character")
                                    rerun = True
                              elif select == "n":
                                    rerun = False
                                    contLoop = False
                              else:
                                    menu()
                        if contLoop == False:
                              break

                  print()

                  # Inputting user information
                  journeyClass = trainBookedInfo[0]
                  userInfo = book.user_info_input(trainBookedInfo, selectedDay,
                                                  trainTicketsAvail, journeyClass)
                  cont = userInfo

                  if cont == False:
                        break

                  # Success message
                  flag = False
                  while (flag == False):
                        print()
                        c = input("Do you want to go to main menu?(Y/N): ")
                        print()

                        if c.lower() == "y":
                              menu()
                        elif c.lower() == "n":
                              flag = False
                              break
                        else:
                              print("Enter a valid option")
                              print()
                              flag = False

            elif opt == 3:
                  cont = book.cancel_ticket()
                  while (cont == False):
                        print()
                        c = input("Do you want to go to main menu?(Y/N): ")
                        print()

                        if c.lower() == "y":
                              menu()
                        elif c.lower() == "n":
                              flag = False
                              break
                        else:
                              print("Enter a valid option")
                              print()
                              flag = False

            elif opt == 4:
                  report()

            elif opt == 5:
                  print("Program ends")
                  break

            print()
            print()

menu()
