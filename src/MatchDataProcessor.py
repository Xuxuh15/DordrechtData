import argparse
import pandas as pd
import config as cf



FILE_PATH = "../matchData.csv"
output_file_name = "processedMatchData"


# Defines a new ArgumentParser
argument_parser = argparse.ArgumentParser(prog= "Match Data Processor",
                                          description = "Formats and processes match data into a .csv file",
                                          epilog = "")

# The command line arguments this program takes
argument_parser.add_argument('-filePath', type=str, default = FILE_PATH, help="The path to the input file e.g. <fileName>.csv")
argument_parser.add_argument('-outputName', type=str, default = output_file_name, help = "What you want the output file to be named")
argument_parser.add_argument('-header_index', type=str, default = 9, help = "The index of the header (Note that csv files start on index 0)")
argument_parser.add_argument('-week', type=int, default = 0, help = "The competition week number")
argument_parser.add_argument('-opponent', type=str, default = "", help = "The opponent (make sure to add quotation marks) e.g. e.g. 'Ajax' ")


args = argument_parser.parse_args()

file_path = args.filePath
output_file_name = args.outputName + '.csv'
index_header = args.header_index
week_no = args.week
opponent = args.opponent

column_names =  ['Player Name', 'Period Name', 'Period Number', 'Total Duration', 'Total Distance', 'HSRD > 20', 'HSRD > 25', 'HSRD > 30',
                 'HSRE > 20', 'HSRE > 25', 'HSRE > 30','Maximum Velocity','Acceleration Efforts > 2','Deceleration Efforts > 2','Acceleration Efforts > 3', 'Deceleration Efforts > 3', 
                 'Acceleration Efforts > 4','Deceleration Efforts > 4', 'Playerload 3D', 'Explosive Efforts', 'EMD', 'HMPE', 'HMLD', 'Half']


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
start_time = param_list[1]
unix_start_time = param_list[2]
durtaion = param_list[3]
num_players = param_list[4]
num_periods = param_list[5]
num_params = param_list[6]



# Read the csv file and store data into a data frame
raw_data = pd.read_csv(file_path, header = index_header)


# Converts a Hour:Minute:Second time string into value in minutes
def convert_to_minutes(time_str):
    # Split the time string into hours, minutes, and seconds
    hours, minutes, seconds = map(int, time_str.split(':'))
    
    # Convert hours to minutes and add minutes and seconds converted to minutes
    total_minutes = round(hours * 60 + minutes + seconds / 60)
   
    return total_minutes

# Determines which half a minute is categorized in [1,2]
def calculate_half(minute):
    if(int(minute) <= 45):
        return 1; 
    else:
        return 2; 

# Filter data by period. We only want periods that are numbers
data = raw_data[(raw_data['Period Name'].str.len() <= 3) | (raw_data['Period Name'].str.len() <= 3 )].copy()

# Rename the columns
data.columns = column_names

data['Total Duration'] = data['Total Duration'].apply(convert_to_minutes)
data[['Total Distance','HSRD > 20', 'HSRD > 25', 'HSRD > 30','HSRE > 20', 'HSRE > 25', 'HSRE > 30', 'Maximum Velocity', 'Playerload 3D', 'EMD','HMPE', 'HMLD']] = data[['Total Distance','HSRD > 20', 'HSRD > 25', 'HSRD > 30',
        'HSRE > 20', 'HSRE > 25', 'HSRE > 30','Maximum Velocity', 'Playerload 3D', 'EMD', 'HMPE', 'HMLD']].map(lambda x: int(round(x)))
data[['Half']] = data[['Period Name']].map(calculate_half)
data.sort_values(by = ['Player Name', 'Half'], axis = 0, inplace = True)

#Inserts the followings columns:
# Team column
data.insert(0, 'Team', cf.TEAM, allow_duplicates=False)

# Inserts Week Number column
data.insert(2, 'Week Number', week_no, allow_duplicates=False)

# Date Column
data.insert(3, 'Date', date0,allow_duplicates=False)

# Match Type Column
data.insert(4, 'Match Type', cf.MatchType.COMPETITION.value, allow_duplicates=False)

# GPS System Column
data.insert(5, 'GPS System', cf.GPSVERSION.CATAPULT.value, allow_duplicates=False)

# Opponent Column
data.insert(6, 'Opponent', opponent, allow_duplicates=False)

# Save the processsed data into a .csv file of name specified by the command line argument outputName
data.to_csv(output_file_name, index=False)

print(data)




 
 

 