import csv
import unicodedata

FILIPINO_GIVEN_NAMES_FILE_PATH = './data/filipino_given_names.csv'


def read_filipino_names():
    names = []

    with open(file=FILIPINO_GIVEN_NAMES_FILE_PATH, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)

        for row in reader:
            name = row['Name']
            names.append(name)

    return names


def remove_diacritics(text):
    # Decompose characters into base letter + combining mark
    normalized = unicodedata.normalize('NFD', text)

    # Filter out non-spacing marks (diacritics)
    return ''.join(c for c in normalized if not unicodedata.combining(c))


def main():
    names = read_filipino_names()
    deaccented_names = [remove_diacritics(name) for name in names]

    print(deaccented_names)


if __name__ == "__main__":
    main()
