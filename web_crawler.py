import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_title_and_links(url, domain):
    try:
        # Fetch the content from URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for invalid responses

        soup = BeautifulSoup(response.text, 'html.parser')

        # Get the title of the page
        title = soup.title.string if soup.title else 'No Title'

        links = []
        for link in soup.find_all('a'):
            href = link.get('href')

            if href and not href.startswith('http'):
                href = urljoin(domain, href)

            if href and href.startswith(domain):
                links.append((title, href))

        return links

    except (requests.RequestException, requests.exceptions.HTTPError):
        return []

def crawl_website(start_url):
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=requests.utils.urlparse(start_url))
    visited = set()
    to_visit = set([start_url])
    all_links = []

    while to_visit:
        url = to_visit.pop()
        print("Crawling:", url)
        visited.add(url)

        for title, link in get_title_and_links(url, domain):
            if link not in visited and domain in link:
                to_visit.add(link)
                all_links.append((title, link))

    return all_links

# Ask the user to input a URL
start_url = input("Enter the URL of the website to crawl: ")
all_links = crawl_website(start_url)

# Print the results in a tabular format
print("Page Title\tPage URL")
for title, url in all_links:
    print(f"{title}\t{url}")
