import concurrent.futures
import subprocess
import time
import requests
from dotenv import load_dotenv
import os
import speedtest

# Load the environment variables from .env file
load_dotenv()


def check_download_speed():
    st = speedtest.Speedtest(secure=True)
    st.download()
    download_speed_mbps = st.results.download / 1024 / 1024  # Convert from bits per second to Mbps
    download_speed_mbs = download_speed_mbps / 8  # Convert Mbps to MB/s
    return download_speed_mbps, download_speed_mbs


def estimate_download_time(urls, file_size_gb, speed_mbs):
    total_size_gb = len(urls) * file_size_gb
    total_size_mb = total_size_gb * 1024  # Convert GB to MB
    estimated_time_seconds = total_size_mb / speed_mbs

    # Convert seconds into hh:mm:ss format
    hours = estimated_time_seconds // 3600
    minutes = (estimated_time_seconds % 3600) // 60
    seconds = estimated_time_seconds % 60
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"


def am_i_connected_from_uk():
    # Replace 'YOUR_API_KEY' with your actual API key for the IP geolocation service
    api_key = os.getenv('IPSTACK_API_KEY')
    url = f"http://api.ipstack.com/check?access_key={api_key}"

    try:
        response = requests.get(url)
        data = response.json()
        return data['country_code'] == 'GB'
    except requests.RequestException as e:
        print(f"Error: {e}")
        return False


# Function to run get_iplayer for a given url with verbose output
def get_subtitles(url, thread_number, attempt=1):
    command = f"get_iplayer --force --subtitles {url}"
    print(f"[Thread {thread_number}] Executing command: {command}")

    try:
        with subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1,
                              universal_newlines=True) as proc:
            for line in proc.stdout:
                print(f"[Thread {thread_number}] {line}", end='')  # end='' avoids double newlines
        # Check the return code after the subprocess has finished
        if proc.returncode != 0:
            print(f"[Thread {thread_number}] Command failed with return code {proc.returncode}.")
            if attempt < 5:
                print(f"[Thread {thread_number}] Retrying...")
                time.sleep(10)
                return get_subtitles(url, thread_number, attempt + 1)
            else:
                print(f"[Thread {thread_number}] Failed to process subtitles for {url} after 3 attempts.")
                return False
        else:
            print(f"[Thread {thread_number}] Successfully processed subtitles for {url}")
            return True
    except Exception as e:
        print(f"[Thread {thread_number}] An error occurred: {e}")
        return False


# Function to process URLs with multithreading, starting a new thread every 2 seconds
def process_urls(url_file_path):
    with open(url_file_path, 'r') as file:
        return [url.strip() for url in file if url.strip()]


def run_concurrent(urls):
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        thread_number = 1
        futures = []
        for url in urls:
            # Submit a new thread to the executor
            future = executor.submit(get_subtitles, url, thread_number)
            futures.append(future)
            thread_number += 1
            time.sleep(120)  # Wait for 2 min before starting the next thread
        # Wait for all futures to complete
        concurrent.futures.wait(futures)


# Main function
def main():
    if am_i_connected_from_uk():
        print("You are in UK I will try to download...")
        speed_mbps, speed_mbs = check_download_speed()
        print("Checking download speed please wait...")
        print(f"Download Speed: {speed_mbps:.2f} Mbps ({speed_mbs:.2f} MB/s)")

        urls = process_urls('urls.txt')
        estimated = estimate_download_time(urls, 2, speed_mbs)
        print("estimated time " + estimated)

        print("Starting the subtitle download process.")
        run_concurrent(urls)
        print("Subtitle download process completed.")
    else:
        print("your IP is not in UK you need a VPN. Your antivirus can interfere.")


if __name__ == "__main__":
    main()
