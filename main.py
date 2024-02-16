from pprint import pprint
import requests
from bs4 import BeautifulSoup

def is_valid(word):
    return "[" not in word and "]" not in word

def extract_lyrics(url):
    print(f"Fetching lyrics {url}...")
    r = requests.get(url)

    if r.status_code != 200:
        print("Page impossible à récupérer.")
        return []

    soup = BeautifulSoup(r.content, 'html.parser')
    lyrics_container = soup.find("div", class_="Lyrics__Container-sc-1ynbvzw-1 kUgSbL")

    if not lyrics_container:
        return ["stop"]
        # return extract_lyrics(url)

    if "released" in lyrics_container.stripped_strings:
        return []

    all_phrases = [phrase.strip() for phrase in lyrics_container.stripped_strings if is_valid(phrase)]

    return all_phrases

#inutile mais sweetie (pas tant inutile que ça je crois)
def letter(url):
    list_phrases = extract_lyrics(url)
    return list_phrases

#url = 'https://genius.com/Slowthai-inglorious-lyrics'

#phrases = letter(url)
#pprint(phrases)


#renvoie si oui y a le word dedans
def detecter(phrases,word):
    initiales=""
    for i in range(0,len(phrases)):
        initiales=initiales+phrases[i][0]
    print(initiales)
    #SDBTIIIGT1WWCCARTIRINFAIZNFOAIZJA
    if str(word) in initiales:
        return True
    else:
        False


def get_all_urls(page_number=1):
    links = []
    while True:
        #MODIFIER LA LIGNE CI DESSOUS PR CHANGER DARTISTE LAAAAA
        r = requests.get(f"https://genius.com/api/artists/3127026/songs?page={page_number}&sort=popularity")
        if r.status_code == 200:
            print(f"Fetching page {page_number}")
            response = r.json().get("response", {})
            next_page = response.get("next_page")

            songs = response.get("songs")
            links.extend([song.get("url") for song in songs])
            page_number += 1


            if not next_page:
                print("No more pages to fetch.")
                break
    
    print(len(links))
    return links

print(get_all_urls())

#print(detecter(phrases,"FATFNSYA"))

#artiste -> links -> extraction de lyrics individuelle -> detecteur -> oui non

#modifier la suite de chiffres dans la fonction GETALLURLS pour changer d'artiste
#et le WORD ci dessous

liste_reponses=""

def procedure(word,page_number=1):
    for i in get_all_urls(page_number):
        extract_lyrics(i)
        letter(i)
        print(detecter(letter(i),word))
        if detecter(letter(i),word)==True:
            print("-------------------HOPHOPHOPHOPHOP !-------------------")
            return "Le mot a été trouvé :o"
    procedure(page_number+1)

    if page_number==10:
        return "Sur 10 ptn de pages, le mot n'a pas été trouvé."
    
    next=str(input("On continue ? y/n : "))
    if next=="Y" or next=="y":
        procedure(page_number+1)
    else:
        return "Fin de la procédure."

procedure("LALA",1)

#si y a pas, alors on cherche sur une nouvelle page
