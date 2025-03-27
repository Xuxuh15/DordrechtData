from dotenv import load_dotenv
import os
import requests
from dateutil import parser
from datetime import datetime, timedelta



load_dotenv()  # Load environment variables from .env file

# Define the endpoint and your API key
api_url = "https://serpapi.com/search.json"
api_key = os.getenv("SERPAPI_KEY")


# Define the search parameters
params = {
    'q': 'fc+dordrcht+matches',  # Query parameter (e.g., search term)
    'location': 'United States',  # Location to base the search on (optional)
    'api_key': api_key,  # Your API key
    'engine': 'google'  # Search engine (default is google)
}

# Send the HTTP GET request
response = requests.get(api_url, params=params)

# Check the response status code
if response.status_code == 200:
    # Parse and display the results
    data = response.json()  # The response is usually in JSON format
    # print(data)
else:
    print(f"Error: {response.status_code}")
    print(response.text)

# Gets the date from the returned data
def getDate(dateStr):
    str = dateStr.split(',')
    # Replace "yesterday" with the actual date (i.e., subtract one day from today)
    dateStr = dateStr.replace(str[0], (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"))

    # Now parse the modified string to get the datetime
    date_obj = parser.parse(dateStr)
    return date_obj

# Determines which index in list of teams belongs to the name specified
def getIndex(teams, name):
    index = -1
    for i in range(len(teams)):
        if(teams[i]['name'] == name):
            index = i; 
    return index


# Get the relevant data from response
most_recent_match = data['sports_results']['game_spotlight']
teams = most_recent_match['teams']
index_Dordrecht = getIndex(teams, 'Dordrecht')
index_opponent = 1 - index_Dordrecht
opponent = teams[index_opponent]['name']
date = getDate(most_recent_match['date']).date()
goal_summary = teams[index_Dordrecht]['goal_summary']
rankings = data['sports_results']['rankings']




