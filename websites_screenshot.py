import asyncio
from playwright.async_api import async_playwright
import argparse
from libs.utils import check_and_create_directory, read_file_to_array
from libs.utils import get_url_concat_path_and_param, get_absolute_path
from libs.generate_html import initiate_html_report, generate_html_report

"""
Note:
+ Make the output dir to be the domain name service of the website (the output_dir param of the process_urls()) (depend on user input)
+ Random User Agent
+ Look into window size 
+ Look into screenshot size 
    + Source: https://stackoverflow.com/questions/74559415/how-to-take-a-screenshot-by-passing-coordinates-and-dimensions-in-playwright
"""

async def take_screenshot(url, filename, headless_mode):
    """
    Take a screenshot of a website and save it to a file

    Args:
        url (str): The URL of the website to screenshot
        filename (str): The filename to save the screenshot as
        output_dir (str): The directory to the screenshot in
    """
    async with async_playwright() as p:
        # Launch a headless browser
        browser = await p.chromium.launch(headless=headless_mode)
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

async def process_urls(urls, threads, output_dir, headless_mode):
    """
    Process a list of URLs and take screenshots in batches of {threads}

    Args:
        urls (list): List of URLs to screenshot
        threads (int): number of requests simultaneously
    """
    tasks = []
    base_path, image_path = check_and_create_directory(output_dir)
    html_report = initiate_html_report()
    image_data_list = []
    for url in urls:
        url_concat_path_and_param = get_url_concat_path_and_param(url)
        filename = f"screenshot_{url_concat_path_and_param}.png" # Create a filename for each screenshot
        save_screenshot_to = f'{image_path}/{filename}'
        image_data_list.append([save_screenshot_to, url])
        tasks.append(take_screenshot(url, save_screenshot_to, headless_mode))
        # If we have 10 tasks, run them concurrently
        if len(tasks) == threads:
            await asyncio.gather(*tasks) # Run the parallel tasks
            tasks = [] # Reset the tasks list
    # Process any remaining tasks
    if tasks:
        await asyncio.gather(*tasks)

    # Save the HTML report
    generate_html_report(html_report, image_data_list, base_path)

if __name__ == "__main__":
    # Create the parser
    parser = argparse.ArgumentParser(description='Take URLs\' screenshot with threading.')
    # Add arguments
    parser.add_argument('-urls-file', type=str, required=True, help='Path to the file containing URLs')
    parser.add_argument('-threads', type=int, default=2, help='Number of threads to use (default: 2)')
    parser.add_argument('-output', type=str, default=".",
    help='Directory to store output, recommend using DNS, a new subdirectory will be created to store data (default: .)(your current working directory)')
    parser.add_argument('-disable-headless', action='store_false', help='Disable headless, when you see HTTP2 error, maybe disable headless mode')

    # Parse the arguments
    args = parser.parse_args()

    # Debug arguments
    # print(args)
    
    # # Read the urls
    # # Must beginning with http protocol
    urls = read_file_to_array(args.urls_file)

    # # Run the async function
    output_dir = get_absolute_path(args.output)
    asyncio.run(process_urls(urls, args.threads, output_dir, args.disable_headless))
