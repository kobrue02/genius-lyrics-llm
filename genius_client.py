import requests
import os
import trafilatura

from string import punctuation
from bs4 import BeautifulSoup

class GeniusClient:

    def __init__(self, url: str = "https://genius.com/artists/Tempesst/songs", artist: str = "Tempesst") -> None:
        self.url = url
        self.artist = artist.lower()

    def __iterate_over_song_list(self, url: str) -> list[str]:
        re = requests.get(url)
        soup = BeautifulSoup(re.text, features='lxml')
        soup = soup.find("ul", {"class": "ListSectiondesktop__Items-sc-53xokv-8 kbIuNQ"})

        urls = []
        itemList = soup.find_all("li", {"class": 'ListItem__Container-sc-122yj9e-0 eRBVjI'})
        for a in itemList:
            url = a.a['href']
            title = self.__title(a.text)
            urls.append({'url': url, 'title': title})
        
        return urls

    def __title(self, title: str) -> str:
        title = title.replace(' ', '_')
        title = title.lower()
        for _ in punctuation:
            if _ == '_':
                continue
            title = title.replace(_, '')
        title = title.replace("'", "")
        return title

    def __get_lyrics(self, url: str) -> str:
        re = requests.get(url)
        soup = BeautifulSoup(re.text, features='lxml')

        soup = soup.find_all("div", {"data-lyrics-container": "true"})
        lyric = ""
        for item in soup:
            lyric += "\n".join(item.get_text(strip=True, separator='\n').splitlines())

        return lyric

    def run(self) -> None:
        os.makedirs('lyrics', exist_ok=True)
        os.makedirs(f'lyrics/{self.artist}', exist_ok=True)

        songUrls = self.__iterate_over_song_list(self.url)

        for song in songUrls:
            song_url = song['url']
            song_title = song['title']
            lyrics = self.__get_lyrics(song_url)
            with open(f'lyrics/{self.artist}/{song_title}.txt', 'w', encoding='utf-8') as f:
                f.write(lyrics)


if __name__ == "__main__":
    artist = "Tempesst"
    url = "https://genius.com/artists/Tempesst/songs"

    genius = GeniusClient(url, artist)
    genius.run()