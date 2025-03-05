# BBC iPlayer Subtitle Downloader

This project allows you to download subtitles from BBC iPlayer using the `get_iplayer` command-line tool. It also checks your download speed and estimates the time required to download the subtitles.

## Prerequisites

- Python 3.11.5
- `get_iplayer` command-line tool
- `speedtest-cli` Python package
- `python-dotenv` Python package
- An API key for IPStack IP geolocation service

## Installation

1. Install Python 3.11.5 from the official website: [Python Downloads](https://www.python.org/downloads/)

2. Install the required Python packages:
    ```sh
    pip install speedtest-cli
    pip install python-dotenv
    ```

3. Install `get_iplayer`:
    ```sh
    sudo apt-get install get-iplayer
    ```

4. Create a `.env` file in the project directory and add your IPStack API key:
    ```env
    IPSTACK_API_KEY=your_api_key_here
    ```

## Usage

1. Add the URLs of the BBC iPlayer episodes you want to download subtitles for in the `urls.txt` file. Each URL should be on a new line.

2. Run the script:
    ```sh
    python main.py
    ```

3. The script will check if you are connected from the UK, check your download speed, estimate the download time, and start downloading the subtitles.

## Notes

- Ensure you are connected from the UK or use a VPN to connect from the UK.
- Your antivirus software may interfere with the VPN connection.
- The files are downloaded in ``C:\Users\yourUser\Desktop\iPlayer Recordings``

## Files

- `main.py`: The main script to run the subtitle downloader.
- `urls.txt`: A file containing the URLs of the BBC iPlayer episodes.
- `.env`: A file containing environment variables, including the IPStack API key.

