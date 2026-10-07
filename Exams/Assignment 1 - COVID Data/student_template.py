import sys

"""
Create a program which will provide answers to the questions posed in the assignment description.
We've provided a function which will parse the NYT covid database file (named "us-counties.csv"); 
however, its correct implementation will be up to you. DO NOT MODIFY THIS FUNCTION.
Your code needs to be successful as well as sufficiently commented/documented to receive full credit.
"""


def parse_nyt_data(file_path=''):
    """
    Parse the NYT covid database and return a list of tuples. Each tuple describes one entry in the source data set.
    Date: the day on which the record was taken in YYYY-MM-DD format
    County: the county name within the State
    State: the US state for the entry
    Cases: the cumulative number of COVID-19 cases reported in that locality
    Deaths: the cumulative number of COVID-19 death in the locality

    :param file_path: Path to data file
    :return: A List of tuples containing (date,county, state, fips, cases, deaths) information

    ____________________ DO NOT MODIFY THIS FUNCTION ___________________
    """
    # data point list
    data=[]

    # open the NYT file path
    try:
        fin = open(file_path)
    except FileNotFoundError:
        print('File ', file_path, ' not found. Exiting!')
        sys.exit(-1)

    # get rid of the headers
    fin.readline()

    # while not done parsing file
    done = False

    # loop and read file
    while not done:
        line = fin.readline()

        if line == '':
            done = True
            continue

        # format is date,county,state,fips,cases,deaths
        (date,county, state, fips, cases, deaths) = line.rstrip().split(",")

        # clean up the data to remove empty entries
        if cases=='':
            cases=0
        if deaths=='':
            deaths=0

        # convert elements into ints
        try:
            entry = (date,county,state, fips, int(cases), int(deaths))
        except ValueError:
            print('Invalid parse of ', entry)

        # place entries as tuple into list
        data.append(entry)


    return data

### YOUR CODE HERE ###
data = parse_nyt_data("../../data/covid/us-counties.csv") 

#Separate Harrisonburg and Rockingham into sublists by having all data containing keywords appended
HBurg = [] #Initialize list by setting variable equal to empty brackets, function below will "fill"
Rock = [] #Initialize list by setting variable equal to empty brackets, function below will "fill"

for line in data: #data is a list of values, data is in 'lines'
    if "Harrisonburg city" in line[1] and "Virginia" in line[2] and not "West Virginia" in line[2]: 
        # ^ line sorts out all County data based on the name of county and the name of state. 
        # ^ Given multiple states have "Virginia" in name, "not "West Virginia"" was added for certainty
        HBurg.append(line) #places entire line in sublist if contain keyword
    if "Rockingham" in line[1] and "Virginia" in line[2] and not "West Virginia" in line[2]: #See above notes
        Rock.append(line) #See above notes

#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
#Question 1: When was the first positive COVID case in Harrisonburg?
#When was the first positive case in Rockingham County? (2 questions)
#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------

for line in HBurg: #Sets parameter that python is to read the list on a line by line bases
    if line[4] > 0: # row 5 ("4" in python) contains # cases, sets conditional of "if there is a number in this row greater than 0, do the following:"
        print("Harrisonburg Initial Infection Date (IID): ", line[0]) # row 1 ("0" in python) contains date, based on prior line, prints the date based on the # of cases
        break #Stops the function once the above criteria is completed
#-------------------------------------------------------------------------------------------------------------------------
for line in Rock:  #Sets parameter that python is to read the list on a line by line bases
    if line[4] > 0: # row 5 ("4" in python) contains # cases, sets conditional of "if there is a number in this row greater than 0, do the following:"
        print("Rockingham Initial Infection Date (IID): ", line[0]) # row 1 ("0" in python) contains date, based on prior line, prints the date based on the # of cases
        break #Stops the function once the above criteria is completed

#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
# Question 2: On what date was the greatest number of new cases reported in Harrisonburg? 
# What date in Rockingham County? (2 questions)
#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------

max_H = 0 #set arbitrary
max_H_date = "" #Set arbitrary
for i in range(1, len(HBurg)): #iterates through list HBurg
    new = HBurg[i][4] - HBurg[i-1][4] #subtracts last lines # of cases from current line's
    if new > max_H: # if conditional asks "if the new is greater than the current max, do the following:"
        max_H = new # replaces the current max_H with the "new" if the above condtional is true
        max_H_date = HBurg[i][0] #returns the date from current line (represented by "i")
print("Most new cases in Harrisonburg on:" , max_H_date) #Once the list is iterated through, prints the line and the date retrieved by the conditional  
print("Number of new cases: " , max_H) #Prints the line, and the final maximum number of cases generated by the conditional
#------------------------------------------------------------------------------------------------------
max_R = 0 #set arbitrary
max_R_date = ""#Set arbitrary
for i in range(1, len(Rock)): #iterates through list Rock
    new = Rock[i][4] - Rock[i-1][4] #subtracts last lines # of cases from current line's
    if new > max_R: # if conditional asks "if the new is greater than the current max, do the following:"
        max_R = new # replaces the current max_H with the "new" if the above condtional is true
        max_R_date = Rock[i][0] #returns the date from current line (represented by "i")
print("Most new cases in Rockingham on:" , max_R_date)    #Once the list is iterated through, prints the line and the date retrieved by the conditional
print("Number of new cases: " , max_R) #Prints the line, and the final maximum number of cases generated by the conditional

#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
#Question 3: What was the worst seven-day period in Harrisonburg city for new COVID cases? 
#What period in Rockingham County? 
#These are the seven-day periods when the number of new cases was maximal. (2 questions)
#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------

max_H7 = 0 #set arbitrary initials
max_H7_i = ""#set arbitrary initials
max_H7_f = ""#set arbitrary initials
for i in range(7, len(HBurg)): #feeds 7 lines from list at a time to match 7 day
    sum_new = 0 #set arbitrary initials

    for j in range(i-6, i+1): #i is endpoint, these values for the range will set i as the endpoint and include the 6 values prior
        new = HBurg[j][4] - HBurg[j-1][4] #Similar code for Q2, use "j" because "i" is already in use
        sum_new += new #Increases sum_new by "new" from every iteration

    if sum_new > max_H7: #Conditional, "if x is greater than y, do z"
        max_H7 = sum_new #If above conditional is true, replaces current max with sum_new
        max_H7_i = HBurg[i-6][0] #Returns the date from column 1 of the row 6 lines prior
        max_H7_f = HBurg[i][0] #Returns the date from column 1 of the current line
print("Most new cases were observed in Harrisonburg between " , max_H7_i ," and " , max_H7_f) #Outputs the dates in legible range for ease of understanding
print("Number of new cases: ", max_H7) #Outputs the number of new cases over the given span of time
#------------------------------------------------------------------------------------------------------
max_R7 = 0 #set arbitrary initials
max_R7_i = ""#set arbitrary initials
max_R7_f = ""#set arbitrary initials
for i in range(7, len(Rock)): #feeds 7 lines from list at a time to match 7 day
    sum_new = 0 #set arbitrary initials

    for j in range(i-6, i+1): #i is endpoint, these values for the range will set i as the endpoint and include the 6 values prior
        new = Rock[j][4] - Rock[j-1][4] #Similar code for Q2, use "j" because "i" is already in use
        sum_new += new #Increases sum_new by "new" from every iteration

    if sum_new > max_R7: #Conditional, "if x is greater than y, do z"
        max_R7 = sum_new #If above conditional is true, replaces current max with sum_new
        max_R7_i = Rock[i-6][0] #Returns the date from column 1 of the row 6 lines prior
        max_R7_f = Rock[i][0] #Returns the date from column 1 of the current line
print("Most new cases in Rockingham were observed between " , max_R7_i ," and " , max_R7_f) #Outputs the dates in legible range for ease of understanding
print("Number of new cases: ", max_R7)#Outputs the number of new cases over the given span of time