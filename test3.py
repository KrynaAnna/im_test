import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
from statistics import median


def get_address(address, destination):
    # Replace 'YOUR_API_KEY' with your actual API key
    api_key = 'AIzaSyC0wbkBbZ83e9pXqRpx7qhddY96DhOe_zU'
    # Construct the API request URL
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}'
    # Make the API request
    response = requests.get(url)
    data = response.json()

    # Check if the API request was successful
    if data['status'] == 'OK':
        # Extract the latitude and longitude from the response
        location = data['results'][0]['geometry']['location']
        latitude = location['lat']
        longitude = location['lng']

        # Define the origin and destination coordinates (latitude and longitude)
        origin = f'{latitude},{longitude}'

        # Construct the API request URL
        url2 = f'https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={api_key}'

        # Make the API request
        response2 = requests.get(url2)
        data2 = response2.json()

        # Check if the API request was successful
        if data2['status'] == 'OK':
            # Extract the distance and duration from the response
            distance_text = data2['routes'][0]['legs'][0]['distance']['text'].split()[0].replace(',', '')

            return distance_text
        else:
            return 'Error'
    else:

        return 'Error'


def main_func(url, destination_):
    # Define the scope and credentials
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(r'D:\PycharmProjects\test\creds.json', scope)
    # Authenticate
    gc = gspread.authorize(credentials)
    # Open the Google Sheet by URL
    spreadsheet = gc.open_by_url(url)
    # Access a specific worksheet within the spreadsheet
    worksheet = spreadsheet.get_worksheet(0)  # Replace 0 with the index of your desired worksheet
    # Read data from the worksheet
    data3 = worksheet.get_all_records()
    data3 = [item for item in data3 if 'Maximum' not in item.keys() and 'Minimum' not in item.keys() and 'Median' not in item.keys() and item.get('Name') != '']

    lst = []
    for i in range(2, len(data3)+2):
        address_ = list(data3[i-2].values())[1]
        lst.append(float(get_address(address=address_, destination=destination_)))
        # Update a specific cell in the new column
        worksheet.update(f'C{i}', get_address(address=address_, destination=destination_))

    worksheet.update(f'B{len(data3) + 5}', 'Maximum')
    worksheet.update(f'C{len(data3) + 5}', max(lst))

    worksheet.update(f'B{len(data3) + 6}', 'Minimum')
    worksheet.update(f'C{len(data3) + 6}', min(lst))

    worksheet.update(f'B{len(data3) + 7}', 'Median')
    worksheet.update(f'C{len(data3) + 7}', median(lst))

