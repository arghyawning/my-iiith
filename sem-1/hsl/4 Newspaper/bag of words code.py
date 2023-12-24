from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

STOPWORDS = set(stopwords.words("english"))

def write_counts(counts, filepath):
    with open(filepath, "w") as outfile:
        for word in counts.keys():
            to_write = word + " : " + str(counts[word]) + "\n"
            outfile.write(to_write)

def get_counts(text):
    # get the tokens(words)
    tokens = word_tokenize(text)
    # Extract only the words and convert to lowercase
    words = [word.lower() for word in tokens if word.isalpha()]
    # words = [stemmer.stem(word) for word in words if word not in STOPWORDS]
    words = [word for word in words if word not in STOPWORDS]

    counts = {}
    # {"words":occurrences}
    for word in words:
        counts[word] = counts.get(word, 0) + 1

    sorted_tuples = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    sorted_counts = {k: v for k, v in sorted_tuples}
    return sorted_counts

def read_txt(filepath):
    with open(filepath, "r") as f:
        text = f.read()
    return text

texts=read_txt("toi.csv")
write_counts(get_counts(texts), f"bowresults.txt")