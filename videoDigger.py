import os
import requests
import m3u8
    
def download_ts_files_from_playlist(ts_file, base_url="https://turkisaretdili.net/media/", download_folder="ts"):
    """
    Downloads .ts files from an .m3u8 playlist.

    Args:
        ts_file (str): The name of the .m3u8 playlist file.
        base_url (str): The base URL where the .m3u8 playlist and .ts files are located. Default is "https://turkisaretdili.net/media/".
        download_folder (str): The folder where the downloaded .ts files will be saved. Default is "ts".

    Returns:
        None

    Raises:
        None

    Example:
        >>> download_ts_files_from_playlist("SIYAH2")
        Downloaded SIYAH2_0.ts to ts
        Downloaded SIYAH2_1.ts to ts
        Downloaded SIYAH2_2.ts to ts
        ...
    """
    # Send an HTTP GET request to download the .m3u8 playlist
    m3u8_url = base_url + ts_file + ".m3u8"
    print(m3u8_url)
    response = requests.get(m3u8_url)
    if response.status_code != 200:
        print(f"Failed to download the .m3u8 playlist from {m3u8_url}")
        return

    # Parse the .m3u8 playlist
    playlist = m3u8.loads(response.text)
    # Iterate over the segments in the playlist
    for segment in playlist.segments:
        print(segment.uri)
        ts_url = base_url + segment.uri
        ts_filename = os.path.basename(ts_url)

        # Send an HTTP GET request to download the .ts file
        response_ts = requests.get(ts_url)
        if response_ts.status_code == 200:
            # Construct the path to save the file in the download folder
            file_path = os.path.join(download_folder, ts_filename)

            # Save the content of the response to the file
            with open(file_path, "wb") as f:
                f.write(response_ts.content)

            print(f"Downloaded {ts_filename} to {download_folder}")
        else:
            print(f"Failed to download {ts_filename}")