import asyncio
from playwright.async_api import async_playwright
import os
import argparse
import sys

"""
Note:
+ Make the output dir to be the domain name service of the website (the output_dir param of the process_urls())
+ Make the output dir contains a subdir for images and a HTML report
+ Make the screenshots' name contains the path of the URLs
+ Random User Agent
+ Generate HTML report
+ Look into window size 
+ Look into screenshot size 
    + Source: https://stackoverflow.com/questions/74559415/how-to-take-a-screenshot-by-passing-coordinates-and-dimensions-in-playwright
"""

def check_and_create_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Directory '{directory_path}' created.")
    else:
        print(f"Directory '{directory_path}' already exists.")
    image_path = f'{directory_path}/images'
    if not os.path.exists(image_path):
        os.makedirs(image_path)
        print(f"Directory '{image_path}' created.")
    else:
        print(f"Directory '{image_path}' already exists.")
    return directory_path, image_path

def read_file_to_array(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            # Strip newline characters from each line
            lines = [line.strip() for line in lines]
            return lines

    except FileNotFoundError:
        print("The file was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

async def take_screenshot(url, filename):
    """
    Take a screenshot of a website and save it to a file

    Args:
        url (str): The URL of the website to screenshot
        filename (str): The filename to save the screenshot as
        output_dir (str): The directory to the screenshot in
    """
    async with async_playwright() as p:
        # Launch a headless browser
        browser = await p.chromium.launch()
        page = await browser.new_page()
        try:
            # Navigate to the URL
            await page.goto(url)
            # Wait for the page to load completely
            await page.wait_for_timeout(2000) # wait for 2 seconds
            # Take the screenshot
            await page.screenshot(path=filename)
            # Close the browser
        except Exception as e:
            print(f"Error taking screenshot of {url}: {e}")
        finally:
            await browser.close()

async def process_urls(urls, threads, output_dir):
    """
    Process a list of URLs and take screenshots in batches of {threads}

    Args:
        urls (list): List of URLs to screenshot
        threads (int): number of requests simultaneously
    """
    tasks = []
    base_path, image_path = check_and_create_directory(output_dir)
    for i, url in enumerate(urls):
        filename = f"screenshot_{i + 1}.png" # Create a filename for each screenshot
        save_screenshot_to = f'{image_path}/{filename}'
        tasks.append(take_screenshot(url, save_screenshot_to))
        # If we have 10 tasks, run them concurrently
        if len(tasks) == threads:
            await asyncio.gather(*tasks) # Run the parallel tasks
            tasks = [] # Reset the tasks list
    # Process any remaining tasks
    if tasks:
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    # Create the parser
    parser = argparse.ArgumentParser(description='Take URLs\' screenshot with threading.')
    # Add arguments
    parser.add_argument('-urls-file', type=str, required=True, help='Path to the file containing URLs')
    parser.add_argument('-threads', type=int, default=2, help='Number of threads to use (default: 2)')
    parser.add_argument('-output', type=str, default=".",
    help='Directory to store output, a new subdirectory will be created to store data (default: .)(your current working directory)')

    # Parse the arguments
    args = parser.parse_args()
    
    # Read the urls
    # Must beginning with http protocol
    urls = read_file_to_array(args.urls_file)

    # Run the async function
    output_dir = f'{args.output}/sample_output'
    asyncio.run(process_urls(urls, args.threads, output_dir))
