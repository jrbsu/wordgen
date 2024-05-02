import requests
import os

def get_data():
    """
    Gets data from Google Sheets.
    
    Parameters:
    GOOGLE_SHEET_URL: The URL of the public Google sheet
    GOOGLE_SHEET_GID: The ID of the public Google sheet
    
    Returns:
    Nothing, just downloads to a TSV file.
    """
    print("Getting data...", end="\r")
    sheet_url = os.getenv('GOOGLE_SHEET_URL')
    gid_value = os.getenv('GOOGLE_SHEET_GID')

    if not sheet_url or not gid_value:
        print("Error: Environment variables for sheet URL and GID are not set.")
        return

    params = {
        'gid': gid_value,
        'single': 'true',
        'output': 'tsv',
    }
    response = requests.get(sheet_url, params=params)
    response.encoding = response.apparent_encoding
    content = str(response.text)

    with open("materials/data.tsv", "w") as f:
        f.write(content)
        print("Getting data... Done!")