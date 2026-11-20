"""
CULMINATING ASSIGNMENT 3: Musical Note Detection

Create a program which detects the note being played from the given audio file based on its frequency.
It is up to you to employ an appropriate methodology to process the audio signal and detect the note.
The relevant data file is named "Guitar-note-1.wav" and is located in data > musical-notes.
In the same directory, we also provide a reference for the corresponding frequencies of each note.

Your code needs to be successful as well as sufficiently commented/documented to receive full credit.
We have provided a possible method for converting the .wav file to usable data below.
All file paths need to be relative and execute from this file's directory;
the Visual Studio Code setting "Python > Terminal: Execute in File Dir" 
must be enabled in File > Preferences > Settings.

See Canvas for additional requirements.
"""
from numpy.fft import rfft, rfftfreq
import sys
import scipy
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt

#Task 1: Create a plot of the audio signal over time for its entire duration.
#For all graphs, include appropriate labels, titles, and legends. Include 
#this plot as generated for Guitar-note-1 in your report.

#Task 2: Develop a signal processing methodology appropriate for this problem. 
#Create another plot(s) showing only a few periods of interest (relevant to the
#waveform of the musical note being played) of the original signal as well as 
#your processed signal. For all graphs, include appropriate labels, titles, and 
#legends. You may supplement this with more than one plot if you believe that is 
#appropriate. Include this plot(s) as generated for Guitar-note-1 in your report.

#Task 3: Employ an appropriate signal detection methodology to identify the note 
#being played (i.e., 'A1', 'A#1', 'B1', 'C1', ... 'F7', 'F#7', G7, 'G#7', etc.) 
#based on the signal's main frequency; each note corresponds to a specific 
#frequency, such as 'C3', which is 131 Hz. A supplementary file 
#note-frequencies-reference.csv for each note and its corresponding frequency has 
#been added to the repository for you to reference. Your code must be able to 
#accurately determine the note for any of the given audio files without alteration. 
#Apply your code to all five recordings and include in your report a table showing 
#the file name, detected frequency (Hz), and corresponding musical note for each 
#recording.

def parse_note(file_path=''):
    
    """
        Parse the note frequency reference and return a list of tuples. Each tuple describes one entry in the source data set.
        Note/Name: Name of note with respect to the Frequency
        Frequency/Hz: Frequency of a respective note
    
        :param file_path: Path to data file
        :return: A List of tuples containing (Note, Frequency) information
    
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
        (Note, Frequency) = line.rstrip().split(",") #splits the lines apart at the columns and attributes them based on location to an element variable
   
           # clean up the data to remove abnormal entries
        if Frequency=='Hz':    # Because line 2 of the reference contains a string in position [1] which messes with the line read, converts the string input from 
            Frequency = 0      #this line into a manageable integer/float
            
        # convert elements into floats as needed and attributes to a tuple
        try:
            entry = (Note, float(Frequency)) 
        except ValueError:                    #flags if theres an error with the values for whatever reason 
            print('Invalid parse of ', entry) #and prints an error message containing the relevant line
     
        data.append(entry) # place entries as tuple into list
    
    return data #Returns the filled "data" list

data = parse_note("../../data/musical-notes/note-frequencies-reference.csv") #Feeds relative path of the csv file into the parse_note function, the output is attributed to the variable "data"

Freq = [] #Initiate empty list
for line in data:           #iterates through data and appends each line to the empty "Freq" list
    Freq.append(line)       #This makes it easier to keep track of the csv reference data

num_wavs = 5 #Set number of wav files to read


for i in range(1,num_wavs+1): #iterates through a list ranging from 1 to the value of num_wavs (because python reads the end of a range as -1 of that value)
    # Read WAV file (replace "None")
    samplerate, data = wavfile.read('../../data/musical-notes/Guitar-note-'+str(i)+'.wav') #takes the i value from the iteration and uses it to run a changing relative file path limited by the range, function outputs the samplerate and data within a wavfile
    duration = len(data)/samplerate #divides the amount of data collected by the rate it is collected
    time = np.arange(0, duration, 1/samplerate) #function creates an evely spaced array where the start is 0, the stop is the duration of the signal, and the step is the inveerse sample rate
       
    FFT = rfft(data) #function computes the one-dimensional n-point discrete Fourier Transform of a real-valued array by means of a Fast Fourier Transform
    N = len(FFT) #assigns the length of the FFT computation to a variable
    n = np.arange(N) #Creates an evenly spaced list ranging from 0 to N
    T = N/samplerate #Finds the time at a specific point by using the length of the FFT to invert the sample rate
    freq = n/T #finds the frequency by dividing finding how many bins there are within the time length of the audio file

    freq_bins = rfftfreq(len(data), 1/samplerate) #Return the Discrete Fourier Transform sample frequencies where the length of data is the window size and the inverse of the sample rate is the sample spacing

    # Find dominant frequency
    magnitude = np.abs(FFT) #magnitude is based on the absolute value of the FFT
    dominant_idx = np.argmax(magnitude[1:]) #Sets the "dominant" or significant x values as the local maxes
    dominant_freq = freq_bins[dominant_idx] #finds the dominant frequency by relating the key x values to the DFT sample frequencies
    
    dominant_note = None    #Initiate variable as empty
    likely_freq = 0         #Initiate variable as empty
    dominant_note = None    #Initiate variable as empty
    upperband = 0           #Initiate variable as empty
    lowerband=0             #Initiate variable as empty
    for j in range(2, len(Freq)): #iterates through a list where j is any value beween 2 (due the second row being a second header line) and the length of the Freq list
        new_Hz = Freq[j][1] #sets the new_Hz variable as equal to the frequency value in the second colum of the list based on the line number j
        if dominant_freq < new_Hz+(new_Hz*0.01) and dominant_freq > new_Hz-(new_Hz*0.01) : #conditional that requires the calculated frequency value to be within 1% of the frequency value from the reference file for accuracy without requiring absolute precision
            likely_freq = new_Hz #sets the frequency from the reference that meets the condtional as the likely frequency of the respective audio file
            dominant_note = str(Freq[j][0]) #if the conditional is true: reads the first column of the current line of th reference and returns the value as a string 
            upperband = new_Hz+(new_Hz*0.01) #if the conditional is true: sets the upper band (for use in a bandpass filter) as the reference frequency + 1%
            lowerband = new_Hz-(new_Hz*0.01) #if the conditional is true: sets the lower band (for use in a bandpass filter) as the reference frequency - 1%

    #Following function applies a bandpass filter (combined upper and lower pass filters) to the data
    def bandpass(data: np.ndarray, edges: list[float], samplerate: float, poles: int = 5):
        sos = scipy.signal.butter(poles, edges, 'bandpass', fs=samplerate, output='sos')
        filtered_data = scipy.signal.sosfiltfilt(sos, data)
        return filtered_data

    filtered = bandpass(data, [lowerband, upperband], samplerate) #Feeds data, the data edges, and the samplerate into the filter function

    print("(Deliverable 3) \nFor Guitar-note-"+str(i)+'.wav:') #Prints the deliverable and the name of the audio files
    print(f"Calculated frequency: {dominant_freq:.2f} Hz")      #prints the calculated frequency 
    print(f"Likely Frequency (<1% difference): {likely_freq:.2f} Hz") #prints the frequency value that aligns with the calculated resort
    print("Note likely played is: ", dominant_note) #Prints the name of the note
    """
    #Prints the plot of the raw untouched data from the wavfile
    plt.plot(time, data, label="Raw Signal")                        
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Plot of Guitar-note-'+str(i)+'.wav (Deliverable 1)')
    plt.legend(loc='upper right')
    plt.show()
    """

    #outputs the plots of the unfilted and filtered data over a set time, shows how age ratings matter and apply   
    plt.plot(time, data, time, filtered, label="Unfiltered"+"Filtered") ###!!!####
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Plot of Guitar-note-'+str(i)+'.wav (Deliverable 2)')
    plt.xlim(1, 2)
    plt.legend(loc='upper right')
    plt.show()

    #outputs the plots of the FFT
    plt.plot(freq, FFT, label="Transformed Signal")
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('FFT Amplitude')
    plt.xlim(0, 5000)
    plt.title('Fast Fourier Transformation of Guitar-note-'+str(i)+'.wav (Deliverable 3)')
    plt.legend(loc='upper right')
    plt.show()
    