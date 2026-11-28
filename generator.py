import csv
import unicodedata
from markov_chain import MarkovChain

# Project Configuration
FILIPINO_GIVEN_NAMES_FILE_PATH = './data/filipino_given_names.csv'


def configure_project():
    k = int(input("Context length: "))

    return k


def read_filipino_names():
    names = []

    with open(file=FILIPINO_GIVEN_NAMES_FILE_PATH, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)

        for row in reader:
            name = row['Name']
            names.append(name)

    return names


def deaccent(text) -> str:
    # Decompose characters into base letter + combining mark
    normalized = unicodedata.normalize('NFD', text)

    # Filter out non-spacing marks (diacritics)
    return ''.join(c for c in normalized if not unicodedata.combining(c))


def main():
    # Configure project
    k = configure_project()

    # Initialize Markov Chain
    markov_chain = MarkovChain(k)

    # Get the list of Filipino names
    names = read_filipino_names()

    # Lowercase Filipino Names
    names = [name.lower() for name in names]

    # Deaccent each string in names
    names = [deaccent(name) for name in names]

    # Train Markov Chain
    markov_chain.train(names, k)

    print(markov_chain.contexts.keys())


if __name__ == "__main__":
    main()
