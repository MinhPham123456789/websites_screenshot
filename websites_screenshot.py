import asyncio
from playwright.async_api import async_playwright

"""
Note:
+ Make the output dir to be the domain name service of the website
+ Make the output dir contains a subdir for images and a HTML report
+ Make the screenshots' name contains the path of the URLs
+ Make the script taking user input in CLI
+ Make help menu
+ Generate HTML report
+ Look into window size 
+ Look into screenshot size 
"""
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
    for i, url in enumerate(urls):
        filename = f"screenshot_{i + 1}.png" # Create a filename for each screenshot
        save_screenshot_to = f'{output_dir}/{filename}'
        tasks.append(take_screenshot(url, save_screenshot_to))
        # If we have 10 tasks, run them concurrently
        if len(tasks) == threads:
            await asyncio.gather(*tasks) # Run the parallel tasks
            tasks = [] # Reset the tasks list
    # Process any remaining tasks
    if tasks:
        await asyncio.gather(*tasks)

# Example usage
# Must beginning with http protocol
urls = [
    "https://www.google.com",
    "https://www.youtube.com",
    "https://www.stackoverflow.com"
]

# Run the async function
asyncio.run(process_urls(urls, 2, "./sample_output"))