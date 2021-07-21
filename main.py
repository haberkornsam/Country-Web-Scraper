from bs4 import BeautifulSoup
import requests, lyricsgenius, json, os, sys

TOP100LIST = "https://playback.fm/charts/country/{year}"
GENIUS_API_KEYS = ["4BS3k-97upk3p39IZNzEptiIjYEd7QTAsUxTgI9n_BdPxg9dwMA-NWsRcO9Nt7aY",
                   "uzMkjkngNmN143Gh3mznBRUSibemBP3zj-XyahSnZ1ACPgi6mFJVu0Yyw8n5vIus",
                    "GdyhzUKPIwLzZ2TeBD4OKzUfQCwhXH2CDvan-vMpOLlnH6t0dL4yc78-w8zvejZK"]

def get_year_songs(year, max_songs=100):
    print(TOP100LIST.format(year=year))
    r = requests.get(TOP100LIST.format(year=year))
    soup = BeautifulSoup(r.text, 'html.parser')
    t = soup.find_all("table", class_ = "chartTbl")[0]

    songs = []

    for tr in t.find_all("tr", itemprop="track"):
        artist = tr.find_all("a", itemprop="byArtist")[0].getText().strip()
        song = tr.find_all("span", class_="song")[0].getText().strip()

        songs.append((song, artist))

    return songs[0:max_songs]

def lyric_lookup(song, genius):
    #artist = genius.search_artist("Shelton")
    song = genius.search_song(title=song[0], artist=song[1])
    try:
        return song.lyrics
    except:
        return ""

def year_analysis(year, max_songs, genius_wrapper):
    #genius_wrapper.verbose = False
    songs = get_year_songs(year, max_songs=max_songs)

    word_counts = {}
    song_counts = {}
    for song in songs:
        lyrics = lyric_lookup(song, genius_wrapper).lower()
        words = []
        for punct in ",.?!()\"{}'":
            lyrics = lyrics.replace(punct, "")
        for word in lyrics.split():
            if word in word_counts:
                word_counts[word] += 1
            else:
                word_counts[word] = 1
            if word not in words:
                words.append(word)
                if word in song_counts:
                    song_counts[word] += 1
                else:
                    song_counts[word] = 1

    sorted_words = dict(sorted(word_counts.items(), key=lambda item: item[1]))
    sorted_songs = dict(sorted(song_counts.items(), key=lambda item: item[1]))
    json.dump(sorted_words, open(f"data/{year}_word_data.json", "w+"), indent=1)
    json.dump(sorted_songs, open(f"data/{year}_song_data.json", "w+"), indent=1)


def combine_all():
    words = {}
    songs = {}
    for file in os.listdir("./data"):
        if "combined" in file:
            continue
        print(f"Combining {file}")
        contents = json.load(open(f"./data/{file}"))
        target = words if "word" in file else songs
        for item in contents.items():
            if item[0] in target:
                target[item[0]] += item[1]
            else:
                target[item[0]] = item[1]


    sorted_words = dict(sorted(words.items(), key=lambda item: item[1]))
    sorted_songs = dict(sorted(songs.items(), key=lambda item: item[1]))
    json.dump(sorted_words, open(f"data/combined_word_data.json", "w+"), indent=1)
    json.dump(sorted_songs, open(f"data/combined_song_data.json", "w+"), indent=1)


def convert_to_csv(file, new_file):
    dict = json.load(open(file))
    csv = open(new_file, "w+")
    for item in dict.items():
        csv.write(f"{item[0]}, {item[1]}\n")
    csv.close()

def convert_all_to_csv():
    for file in os.listdir("./data"):
        print(f"Converting {file} to csv")
        new_name = file.rsplit(".", 1)[0] + ".csv"
        convert_to_csv(f"./data/{file}", f"./csv_data/{new_name}")
def main(start, end):
    wrappers = []
    for key in GENIUS_API_KEYS:
        wrappers.append(lyricsgenius.Genius(key, remove_section_headers=True))
    for i in range(start, end):
        print("########################")
        print(f"   Starting Year {i}")
        print("########################")
        year_analysis(i, max_songs=10, genius_wrapper=wrappers[i%3])
    #combine_all()
    #convert_all_to_csv()



#"https://genius.com/Roy-acuff-write-me-sweetheart-lyrics"
#https://genius.com/Jimmie-davis-is-it-too-late-now
if __name__ == '__main__':
    #print(sys.argv)
    main(int(sys.argv[1]), int(sys.argv[2]))