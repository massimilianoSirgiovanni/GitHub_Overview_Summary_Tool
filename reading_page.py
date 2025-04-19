import requests

from bs4 import BeautifulSoup

def read_github_profile(username="massimilianoSirgiovanni"):
    url = f"https://github.com/{username}/{username}"
    response = requests.get(url)

    if response.status_code == 200:
        #info_context = ""
        '''profile = response.text.split("\n")
        for line in profile:
            for element in tags_to_remove:
                if element in line:
                    pass
                else:
                    info_context += "\n" + line'''
        soup = BeautifulSoup(response.text, 'html.parser')
        elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a'])
        info_context = ''.join(str(tag) for tag in elements)
        return info_context
    else:
        print(f"Errore nel recupero: {response.status_code}")
        raise Exception("ERROR: Github user not found!")