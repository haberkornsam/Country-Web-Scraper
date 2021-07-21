import os, json

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


def singular(keyword):
    word_list = json.load(open(f"./data/combined_{keyword}_data.json"))
    final = {}
    for word in word_list.items():
        final[word[0]] = {}
    for file in os.listdir("./data"):
        if keyword not in file:
            continue
        if "combined" in file or "singular" in file:
            continue
        year_data = json.load(open(f"./data/{file}"))
        year = file.split("_")[0]
        for word in word_list.items():
            val = year_data.get(word[0], 0)
            final[word[0]][year] = val
    sort_singular(final)
    json.dump(final, open(f"./data/singular_{keyword}.json", "w+"), indent=3)
    singular_to_csv(final, keyword)


def sort_singular(word_list):
    for word in word_list.items():
        word_list[word[0]] = dict(sorted(word[1].items(), key=lambda item: item[0]))

def singular_to_csv(word_list, keyword):
    f = open(f"./csv_data/singular_{keyword}.csv", "w+")
    for word in word_list.items():
        to_write = word[0]
        for year in word[1].items():
            to_write += f", {year[1]}"
        to_write += "\n"
        f.write(to_write)


def combine_all():
    words = {}
    songs = {}
    for file in os.listdir("./data"):
        if "combined" in file or "singular" in file:
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
    json.dump(sorted_words, open(f"./data/combined_word_data.json", "w+"), indent=1)
    json.dump(sorted_songs, open(f"./data/combined_song_data.json", "w+"), indent=1)


def main():
    #combine_all()
    singular("word")
    print("Starting Song Singulation")
    singular("song")
    #convert_all_to_csv()


if __name__ == '__main__':
    main()