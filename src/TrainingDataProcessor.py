import argparse
import datetime
import pandas as pd
import config as cf



FILE_PATH = "../TrainingData1.csv"
DEFAULT_OUTPUT_NAME = 'ProcessedTrainingData'



# Defines a new ArgumentParser
argument_parser = argparse.ArgumentParser(prog= "Training Data Processor",
                                          description = "Formats and processes training data into a .csv file",
                                          epilog = "")

# The command line arguments this program takes
argument_parser.add_argument('-filePath', type=str, default = FILE_PATH, help="The path to the input file e.g. <fileName>.csv")
argument_parser.add_argument('-outputName', type=str, default = DEFAULT_OUTPUT_NAME, help = "What you want the output file to be named")
argument_parser.add_argument('-header_index', type=str, default = 9, help = "The index of the header (Note that csv files start on index 0)")
argument_parser.add_argument('-week', type=int, default = 0, help = "The training week number")



args = argument_parser.parse_args()

file_path = args.filePath
output_file_name = args.outputName + '.csv'
index_header = args.header_index
week_no = args.week

# All the columns in the output file
column_names =  ['Training Number','Training Type','Match Minutes','RPE','Week Number',	'Date',	'WeekNum','Week Type', 'Phase',
                'Player Name','Position','Availability', 'Data Source','Session Type','Day Code','Match','Competition',
                'Role', 'Duration', 'Total Distance', 'HSRD > 20', 
                 'HSRD > 25', 'HSRD > 30','HSRE > 20', 'HSRE > 25', 'HSRE > 30','Maximum Velocity','Acceleration Efforts > 2',
                 'Deceleration Efforts > 2','Acceleration Efforts > 3', 'Deceleration Efforts > 3', 
                 'Acceleration Efforts > 4','Deceleration Efforts > 4', 'Total Player Load', 'Explosive Efforts', 'EMD', 'HMPE', 'HMLD', 'RPE*Duration']


# Meta data from the .csv file
date0 = None
start_time = None
num_players = None 
duration = None
unix_start_time = None
num_params = None
num_periods = None
param_list = []


# Read the meta data to store later
with open(file_path, "r") as file:
    for _ in range(7):  # Read the first 3 lines
        param_list.append(file.readline())

date0 = param_list[0].split(',')[1].strip()
print(date0)
start_time = param_list[1]
unix_start_time = param_list[2]
durtaion = param_list[3]
num_players = param_list[4]
num_periods = param_list[5]
num_params = param_list[6]

output_file_name = "processedTrainingData" + datetime.datetime.now().strftime("%d-%m-%y") + ".csv"




# Read the csv file and store data into a data frame
raw_data = pd.read_csv(file_path, header=index_header)





# Converts a Hour:Minute:Second time string into value in minutes
def convert_to_minutes(time_str):
    # Split the time string into hours, minutes, and seconds
    hours, minutes, seconds = map(int, time_str.split(':'))
    
    # Convert hours to minutes and add minutes and seconds converted to minutes
    total_minutes = round(hours * 60 + minutes + seconds / 60)
   
    return total_minutes


# Get rid of any extra white space
raw_data.columns = raw_data.columns.str.strip()

# Filter data by period. We only want periods that are numbers
data = raw_data[(raw_data['Period Name'] == 'Session')].copy()



# Clean and format the file
data.drop(labels=['Period Name','Period Number'], axis=1,inplace=True)
data.dropna(axis=1, how='all',inplace=True)

# This section specifies the output file format. Default values used where applicable
data.insert(0,'Training Number', 1)
data.insert(1, 'Training Type', None)
data.insert(2, 'Match Minutes', None)
data.insert(3, 'RPE', 1)
data.insert(4, 'Week Number', None)
data.insert(5, 'Date', date0)
data.insert(6, 'WeekNum', None)
data.insert(7, 'Week Type', None)
data.insert(8, 'Phase', None)

data.insert(10, 'Position', None)
data.insert(11, 'Availability', None)
data.insert(12, 'Session Type', None)
data.insert(13, 'Day Code', None)
data.insert(14, 'Match', None)
data.insert(15, 'Competiton', None)
data.insert(16, 'Role', None)
data.insert(17, 'Data Source', cf.GPSVERSION.CATAPULT.value,)
data['RPE*Duration'] = None


# Rename the columns
data.columns = column_names


data['Duration'] = data['Duration'].apply(convert_to_minutes)
data[['Total Distance','HSRD > 20', 'HSRD > 25', 'HSRD > 30','HSRE > 20', 'HSRE > 25', 'HSRE > 30', 'Maximum Velocity', 'Total Player Load', 'EMD','HMPE', 'HMLD']] = data[['Total Distance','HSRD > 20', 'HSRD > 25', 'HSRD > 30',
        'HSRE > 20', 'HSRE > 25', 'HSRE > 30','Maximum Velocity', 'Total Player Load', 'EMD', 'HMPE', 'HMLD']].map(lambda x: int(round(x)))

data['RPE*Duration'] = data["RPE"].combine(data["Duration"].astype(int), lambda x, y: x * y)
data.sort_values(by = ['Player Name'], axis = 0, inplace = True)

# Save the processsed data into a .csv file of name specified by the command line argument outputName
data.to_csv(output_file_name, index=False)

print(data)




 
 

 