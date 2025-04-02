import argparse


FILE_PATH = '../dummydata/matchData.csv'
OUTPUT_NAME = 'processedMatchData'

# Defines a new ArgumentParser
argument_parser = argparse.ArgumentParser(prog= "Match Data Processor",
                                          description = "Formats and processes match data into a .csv file",
                                          epilog = "")

# The command line arguments this program takes
argument_parser.add_argument('-file_path', type=str, default = FILE_PATH, help="The path to the input file e.g. <fileName>.csv")
argument_parser.add_argument('-output_name', type=str, default = OUTPUT_NAME, help = "What you want the output file to be named")
argument_parser.add_argument('-header_index', type=str, default = 9, help = "The index of the header (Note that csv files start on index 0)")
argument_parser.add_argument('-week', type=int, default = 0, help = "The competition week number")
argument_parser.add_argument('-opponent', type=str, default = "", help = "The opponent (make sure to add quotation marks) e.g. e.g. 'Ajax' ")