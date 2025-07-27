BACKGROUND_COLOR = "#B1DDC6"

with open("de_50k.txt", "r") as file:
    data = file.read()
    print(type(data))
    german_words_list = data.split("\n")

with open("data/german_words.csv", "a") as new_file:
    for i in range(100):
        new_file.write(f"{german_words_list[i].split(" ")[0]}\n")