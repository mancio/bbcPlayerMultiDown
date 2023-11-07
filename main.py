import concurrent.futures
import subprocess
import time


# Function to run get_iplayer for a given url with verbose output
def get_subtitles(url, attempt=1):
    command = f"get_iplayer --force --overwrite --subtitles {url}"
    print(f"Executing command: {command}")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"Command failed with return code {result.returncode}.")
        if attempt < 3:  # If this is the first attempt, try once more
            print("Retrying...")
            time.sleep(2)
            return get_subtitles(url, attempt + 1)
        else:
            print(f"Failed to process subtitles for {url} after 2 attempts.")
            return False
    else:
        print(f"Successfully processed subtitles for {url}")
        return True


# Function to process URLs with multithreading, starting a new thread every 2 seconds
def process_urls(url_file_path):
    with open(url_file_path, 'r') as file:
        urls = [url.strip() for url in file if url.strip()]

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        for url in urls:
            # Submit a new thread to the executor
            executor.submit(get_subtitles, url)
            time.sleep(2)  # Wait for 2 seconds before starting the next thread


# Main function
def main():
    url_file_path = 'urls.txt'
    print("Starting the subtitle download process.")
    process_urls(url_file_path)
    print("Subtitle download process completed.")


if __name__ == "__main__":
    main()
