import requests
import re
from videoDigger import download_ts_files_from_playlist

# URL of the API endpoint
url = "https://turkisaretdili.net/Home/GetWordsWithKey"

# Parameters to send with the request (replace 'your_key' with the actual key)
params = {
    'word': ''
}

# Send an HTTP GET request to the API endpoint
response = requests.get(url, params=params)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

    # Extract .ts file names from the response
    ts_files = [key["VideoURLs"] for key in data if key["VideoURLs"]]

    # Print the list of .ts file names
    print("List of .ts file names:")
    # Initialize an empty list to store filtered URLs
    # Initialize an empty list to store filtered parts of URLs
    filtered_parts = []

    # Iterate over each sublist in the list of URLs
    for sublist in ts_files:
        # Iterate over each URL in the sublist
        for url in sublist:
            # Use regular expression to extract the desired part of the URL
            match = re.search(r'Media/(.*?)\.m3u8', url)
            if match:
                # Add the extracted part to the filtered parts list
                filtered_parts.append(match.group(1))
    for part in filtered_parts:
        download_ts_files_from_playlist(part)
        print(part)
else:
    print("Failed to retrieve .ts file names.")