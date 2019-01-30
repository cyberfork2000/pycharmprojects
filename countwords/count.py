
counts = {}


def count_words(words):

    for word in words.split(' '):
        if word in counts:
            val = counts.get(word)
            val += 1
            counts[word] = val
        else:
            counts[word] = 1
    print(counts)
    return counts


if __name__ == "__main__":
    count_words("oh what a day what a lovely day")

