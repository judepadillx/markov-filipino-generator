import csv
import unicodedata

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


def mark(text, k) -> str:
    start_marker = '^' * k
    end_marker = '$'

    # Mark beginning and ending of text
    return start_marker + text + end_marker


def train(names, k):
    markov_chain: dict[str, dict[str, float]] = {}

    # For each name, count each occurences of next letters given the sequential occuring contexts
    for name in names:
        # Mark beginning and ending of name
        name = mark(name, k)

        context = ""

        for t in range(k, len(name)):
            context = name[t-k:t]
            next_char = name[t]

            # Add context as key in Markov Chain if it does not exist yet
            if context not in markov_chain:
                markov_chain[context] = {}

            # Increase next character count in markov chain given the context
            if next_char not in markov_chain[context]:
                markov_chain[context][next_char] = 1
            else:
                markov_chain[context][next_char] += 1

    # Calculate the probabilities
    for context in markov_chain:
        # Calculate the total next letter occurences given the current context
        total_next_letters_occurences = 0

        for next_letter_count in markov_chain[context].values():
            total_next_letters_occurences += next_letter_count

        # Calculate the probability for each next letter
        for next_letter, next_letter_count in markov_chain[context].items():
            markov_chain[context][next_letter] = next_letter_count / \
                total_next_letters_occurences

    return markov_chain


def main():
    # Configure project
    k = configure_project()

    # Get the list of Filipino names
    names = read_filipino_names()

    # Lowercase Filipino Names
    names = [name.lower() for name in names]

    # Deaccent each string in names
    names = [deaccent(name) for name in names]

    # Train for Markov Chain
    markov_chain = train(names, k)

    print(markov_chain)


if __name__ == "__main__":
    main()
