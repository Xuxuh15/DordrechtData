from MatchDataProcessor import data
from loadsheets import connect_to_sheets
from matchDataParser import argument_parser
import config


def main():

    service = None
    try:
       service = connect_to_sheets()
    except Exception as e:
        print(e)



     # Call the Sheets API
    sheet = service.spreadsheets()

    values = []

    # Go through the datafame and add each row to values list
    for index, row in data.iterrows():
       values.append(row.tolist())
       
    
    body = {"values": values}

    result = (
        service.spreadsheets()
        .values()
        .append(
            spreadsheetId=config.DATABASE_ID,
            range=config.DATABASE_RANGE,
            valueInputOption='USER_ENTERED',
            body=body,
        )
        .execute()
    )

   


if __name__ == '__main__':
    main()
