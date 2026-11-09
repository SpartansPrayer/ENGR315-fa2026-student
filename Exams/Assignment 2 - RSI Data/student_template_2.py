"""
CULMINATING ASSIGNMENT 2: RSI

Create a program which will provide answers to the tasks posed in the assignment description.

For this assignment, you will start from scratch with this blank template.
It is your reponsibility to include all necessary program components in this file.
Your code needs to be successful as well as sufficiently commented/documented to receive full credit.

The relevant data file is named "all_participant_data_rsi.csv" and is located in data > drop-jump.

All file paths need to be relative and execute from this file's directory;
the Visual Studio Code setting "Python > Terminal: Execute in File Dir" 
must be enabled in File > Preferences > Settings.

See Canvas for additional requirements.
"""
#Imports:
import sys
import numpy as np
from scipy.stats import ttest_rel, stats, norm, chisquare
import pandas as pd
import matplotlib.pyplot as plt


def parse_rsi_data(file_path):

    """
        Parse the RSI database and return a list of tuples. Each tuple describes one entry in the source data set.
        Trial: the trial the data is associated with
        force_plate_rsi: rsi data collected w/ force plate
        accelerometer_rsi: rsi collected w/ accelerometer
        percent_error: percent error of collected dats
    
        :param file_path: Path to data file
        :return: A List of tuples containing (trial, force_plate_rsi, accelerometer_rsi, percent_error) information
    
    """
    try:                            #attempts to continually perform the following:
        fin = open(file_path)       #attributes variable "fin" to the function open(file_path), compacts and simplifies code
    except FileNotFoundError:       #flags if the program cannot find the file
        print('File ', file_path, ' not found. Exiting!') #prints error message
        sys.exit(-1)                    #terminates program
    import csv

    data = [] #Initiates list as empty, to be filled
    fin.readline() #opens file and reads a line
   
    done = False # while not done parsing file
    
    while not done: # loop and read file
        line = fin.readline()
   
        if line == '':  #if the line has no entry,  stops reading the file and moves on to the nxt instructions
            done = True #the conditional sets the done variable to true,
            continue    #stops reading the file and moves on to the next instructions
   
        # format is trial,force_plate_rsi,accelerometer_rsi,percent_error
        (trial,force_plate_rsi,accelerometer_rsi,percent_error) = line.rstrip().split(",") #splits the lines apart at the columns and attributes them based on location to an element variable
   
           # clean up the data to remove empty entries
        if force_plate_rsi=='':    #blank entry -> change to 0 so math functions dont get messed up
            force_plate_rsi=0
        if accelerometer_rsi=='':  #blank entry -> change to 0 so math functions dont get messed up
            accelerometer_rsi=0
        if percent_error=='':      #blank entry -> change to 0 so math functions dont get messed up
            percent_error=0

        # convert elements into floats as needed and attributes to a tuple
        try:
            entry = (trial, float(force_plate_rsi), float(accelerometer_rsi), float(percent_error))
        except ValueError:                    #flags if theres an error with the values for whatever reason 
            print('Invalid parse of ', entry) #and prints an error message containing the relevant line
     
        data.append(entry) # place entries as tuple into list
    
    return data #Returns the filled "data" list

data = parse_rsi_data("../../data/drop-jump/all_participant_data_rsi.csv") #Tells the "parse_rsi_data" function the relative file path of the file it should use
alpha = 0.05 #significance level
forceplate=[] #Initiates list as empty, to be filled
accelero=[]   #Initiates list as empty, to be filled
Fpart=[]      #Initiates list as empty, to be filled

for line in data:
    forceplate.append(line[1]) #appends the second element/float to the forceplate list
    accelero.append(line[2])   #appends the third element/float to the forceplate list
    if "F_trial" in line[0]:   #conditional, searches the 1st element for the specified info
        Fpart.append(line)     #appends the line to the Fpart list if the conditional is true
platearray = np.array(forceplate) #converts list into an array
accelarray = np.array(accelero)   #converts list into an array

#Task 1: For the new dataset of RSI values (all_participant_data_rsi.csv), 
#conduct a paired t-test comparing all the force plate and accelerometer RSI values. 
#Clearly report the t-value, p-value, null and alternative hypotheses, 
#and decide whether the null hypothesis can be rejected or not. 
#In your report: What can we conclude about the two measurement methods?

#Source for t-test code: https://www.youtube.com/watch?v=4_2G9wu3wVY

t_stat, p_value = ttest_rel(platearray, accelarray, alternative="two-sided" ) #Function, conducts t-test on related samples, inputs are the 2 "samples" and the definition of the null hypothesis, returns the t-stat and p-value
print('Question 1: Force plate and accelerometer paired t-test:') #prints
print("t-value; ", t_stat) #prints
if p_value >= alpha: #conditional, if the p-value is greater than alpha, the null hypothesis (the means are equal) is true, otherewise the alternative hypothesis is retained
    print("P value (", p_value, ") is greater than alpha (", alpha, ")") #prints
    print("Retain the null hypothesis: There is NO significant difference between force plate readings and accelerometer readings") #prints
    print("Reject the alternate hypothesis: There IS significant difference between force plate readings and accelerometer readings") #prints
else:
    print("P value (", p_value, ") is less than alpha (", alpha, ")") #prints
    print("Reject the null hypothesis: There is NO significant difference between force plate readings and accelerometer readings") #prints
    print("Retain the alternate hypothesis: There IS significant difference between force plate readings and accelerometer readings") #prints
       

#Task 2: For the RSI values gathered using an accelerometer, fit a normal distribution 
#and conduct a Chi2 Goodness of Fit Test. Clearly print out the chi2 stat, p-value, 
#and an indication of whether it is a good fit or not. 
#Plot a histogram of the accelerometer data with the normal distribution curve overlaid. 
#In your report: what factors in the data cause this to be a good fit or not?

#Source for fit: https://www.youtube.com/watch?v=IUcvPo2WCB8
#Source Chi: https://www.youtube.com/watch?v=Fv-U-pZ4HbI  , \ENGR315-fa2026-student\Module 5 - Data Fitting\0 - Lecture Examples\chi-square-gof-categorical.py

print('\nQuestion 2: Histogram, fitting a normal distribution, and performing a Chi2 goodness of fit test on the accelerometer readings:') #prints

[mean_fit, std_fit] = norm.fit(accelero) #fits the accelero list to a normal distribution and returns the mean and standard deviation from this

# bin the examples
bins = np.linspace(-2, 2, 9)  # 9 edges from -2 to 2 make 8 bins

# Trick from StackExchange to add infinite on each end (10 bins in total)
# https://stackoverflow.com/questions/11633874/numpy-use-bins-with-infinite-range
bins = np.r_[-np.inf, bins, np.inf]

# place observations into bins, returns observed values based on the histogram of the dataset
observed_counts, observed_edges = np.histogram(accelero, bins=bins, density=False)

#expected counts come from the probability of each bin under the distribution
expected_mu = 0
expected_std = 1

#the CDF difference between bin edges gives the probability of a value within the bins
expected_prob = np.diff(norm.cdf(bins, loc=expected_mu, scale=expected_std))

#Expected frequency for each bin
expected_counts = expected_prob * len(accelero)

#Conduct chi2 goodness of fit test
#ddof=2: the datasets were standardized with their own mean and standard deviation (2 estimated parameters)
(chi_stat, p_val_chi) = chisquare(f_obs=observed_counts, f_exp=expected_counts, ddof=2) #returns the chi statistic and the p-value from the goodness of fit test

print("Mean: ", mean_fit)
print("Standard Deviation: ", std_fit)

print("Chi2 Stat: ", chi_stat) #prints
print("P value chi2: ", p_val_chi) #prints
if p_val_chi >= alpha: #Null Hypothesis, normal distribution is good fit, if p-value is greater than alpha, the null is retained, otherwise it is rejected
    print("P value is greater than alpha (",alpha,"): Good Fit") #prints
else: #if the conditional statement is not true, execute the following
    print("P value is less than alpha (",alpha,"): Poor Fit") #prints

#Code for Histogram at bottom of program



#Task 3: From the force plate and accelerometer-based RSI data for all participants, 
# create and print() a dataframe containing only the trials from Participant ‘F’. 
# Calculate the 95% confidence intervals for Participant F’s RSI for both the 
# force plate and accelerometer measurements. 
# In your report: What can we conclude about the two measurement methods from these?

#DataFrame Source: https://www.youtube.com/watch?v=5pGfRjnLaNI


#Creates the dataframe using pandas, DataFrame function reads the list, 
# splits the elements in each line, and attributes them to the respective header
df = pd.DataFrame(Fpart, columns=["trial","force_plate_rsi","accelerometer_rsi","percent_error"])

print("\nQuestion 3: Data Frame and 95 percent confidence interval for participant F") #print
print("DataFrame of Participant F Trials:") #print
print(df) #print

#mean and std for force plate data of participant F:
m_fp = df['force_plate_rsi'].mean() #reads all datapoints under the associated header and finds the mean
std_fp = df['force_plate_rsi'].std(ddof=1) #reads all datapoints under the associated header and finds the standard deviation, ddof=1 is a default and tells the function to treat the population as infinite

#95% of data lies within (+/-) 2 standard deviations from mean, 
# min and max of range are therefore the mean +/- 2 standard deviations
print("\nForce Plate 95% Confidence interval range: ")
print("Mean:",m_fp,"\nStandard Deviation: ", std_fp)
print("Min:", m_fp - (2*std_fp), "\nMax:", m_fp + (2*std_fp)) 

#mean and std for accelerometer data of participant F:
m_ac = df['accelerometer_rsi'].mean() #reads all datapoints under the associated header and finds the mean
std_ac = df['accelerometer_rsi'].std(ddof=1) #reads all datapoints under the associated header and finds the standard deviation, ddof=1 is a default and tells the function to treat the population as infinite

#95% of data lies within (+/-) 2 standard deviations from mean, 
# min and max of range are therefore the mean +/- 2 standard deviations
print("\nAccelerometer 95% Confidence interval range: ")
print("Mean:",m_ac,"\nStandard Deviation: ", std_ac)
print("Min:", m_ac - (2*std_ac), "\nMax:", m_ac + (2*std_ac)) 



#Histogram code from question 2:
plt.hist(accelero, bins=(len(accelero)-1), density=False) #plots the histogram
x = np.linspace(np.min(accelero), np.max(accelero)) #returns an even spacing of numbers based on the maximum and minimum of the accelero list
plt.plot(x, norm.pdf(x, mean_fit, std_fit)) #Draws plot with the data from the accelero list as the x-axis and the probability distribution as the y-axis
plt.xlabel("Accelerometer Force Readings") #makes plot generate with respective axis label
plt.ylabel('Probability Density') #makes plot generate with respective axis label
plt.show() #Causes the plot to show