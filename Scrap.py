from bs4 import BeautifulSoup
import json, re, requests, time, threading

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        
        try:
            result = func(*args, **kwargs)
        finally:
            end = time.time()
            elapsed_time = end - start
            print(f"{func.__name__} timer : {elapsed_time:.0f}sec")

        return result

    return wrapper


def fetchAllInstrument(session, base_url):
    response = session.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    pattern = re.compile(r'https://www\.musicalchairs\.info/.*/competitions') #regex101.com
    links = []

    divs = soup.find_all('div', class_='menu_body')
    for div in divs:
        for a in div.find_all('a', href=True):
            if pattern.match(a['href']):
                links.append(a['href'])
    return links

def fetchByInstrument(session, link):
    response = session.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')

    instrument = link.split('/')[-2]

    results = []
    previews = soup.find_all('li', class_='preview')
    
    for preview in previews:
        post_date = preview.find('div', class_='post_item_date').text.split(":")[1].strip()
        closing_date = preview.find('div', class_='post_item_closingdate').span.text.strip()
        country = preview.find('div', class_='post_item_flag').img['alt']
        link = preview.a['href']
        
        results.append({
            'post_date': post_date,
            'closing_date': closing_date,
            'country': country,
            'link': link,
            'instrument': instrument
        })
    return results

def get_final_url(session, url):
    try:
        response = session.get(url, allow_redirects=True)
        return response.url
    except Exception as e:
        print(f"Erreur lors de la récupération de l'URL finale pour {url}: {e}")
        return None

def fetchContestWebsite(session, details):
    for detail in details:
        response = session.get(detail['link'])
        soup = BeautifulSoup(response.content, 'html.parser')

        pattern = re.compile(r'https://www\.musicalchairs\.info/goto-url.*') #regex101.com le retour :D

        divs = soup.find_all('div', class_='post_button_row')
        for div in divs:
            for a in div.find_all('a', href=True):
                if pattern.match(a['href']):
                    goto_url = a['href']
                    final_url = get_final_url(session, goto_url)
                    if final_url:
                        detail['link'] = final_url
                    break
    return details


def saveToJson(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@timer
def main():
    base_url = 'https://www.musicalchairs.info/competitions'
    res = []
    with requests.Session() as session:
        links = fetchAllInstrument(session, base_url)
        for link in links:
            details = fetchByInstrument(session, link)
            details_updated = fetchContestWebsite(session, details)
            res.extend(details_updated)
    saveToJson(res, 'data.json')


        
    
if __name__ == "__main__":
    main()

