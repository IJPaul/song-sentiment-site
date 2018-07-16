import requests
from bs4 import BeautifulSoup
 
 
USER_AGENT = {'User-Agent':'Chrome/61.0.3163.100 Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36'}
 
 
def __getResults(term, numResults, language):
    escaped_search_term = term.replace(' ', '+')
 
    googleUrl = 'https://www.google.com/search?q={}&num={}&hl={}'.format(term, numResults, language)
    response = requests.get(googleUrl, headers=USER_AGENT)
    response.raise_for_status()
 
    return response.text

def __parseResults(html):
    bsObj = BeautifulSoup(html, 'html.parser')
    links = []
    results = bsObj.find_all('div', attrs={'class': 'g'})
    for result in results:
        link = result.find('a', href=True)
        title = result.find('h3', attrs={'class': 'r'})
        if link and title:
            links.append(link['href'])
    return links
     
def scrapeGoogle(term, numResults, language='en'):
    try:
        html = __getResults(term, numResults, language)
        results = __parseResults(html)
        return results
    except requests.HTTPError:
        raise Exception("Blocked by Google")
    except requests.RequestException:
        raise Exception("Issue with connection")
    