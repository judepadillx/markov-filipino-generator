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
    """
    markov_chain : dict = {
        context : str = {
            'occurence': int,
            'next-letters': {
                letter : str = {
                    'occurence': int,
                    'probability': float
                }
            }
        }
    }
    """

    markov_chain = {}

    # For each name, count each occurences of next letters given the sequential occuring contexts
    for name in names:
        # Mark beginning and ending of name
        name = mark(name, k)

        context = ""

        for t in range(k, len(name)):
            context = name[t-k:t]
            next_letter = name[t]

            # Increment context occurence whenever it appears
            if context not in markov_chain:
                markov_chain[context] = {'occurence': 1, 'next-letters': {}}
            else:
                markov_chain[context]['occurence'] += 1

            # Increment next character count in markov chain given the context
            if next_letter not in markov_chain[context]['next-letters']:
                markov_chain[context]['next-letters'][next_letter] = {
                    'occurence': 1,
                    'probability': 0
                }
            else:
                markov_chain[context]['next-letters'][next_letter]['occurence'] += 1

    # Calculate the probabilities
    for context, context_data in markov_chain.items():
        for next_letter, next_letter_data in markov_chain[context]['next-letters'].items():
            markov_chain[context]['next-letters'][next_letter]['probability'] = next_letter_data['occurence'] / \
                context_data['occurence']

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
