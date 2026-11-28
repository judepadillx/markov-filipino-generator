class Context():
    def __init__(self):
        self.occurence: int = 0
        self.next_letters: dict[str, Letter] = {}

    def add_next_letter(self, next_letter):
        self.occurence += 1

        if next_letter not in self.next_letters:
            self.next_letters[next_letter] = Letter()

        self.next_letters[next_letter].increment_occurence()

    def update_probabilities(self):
        for letter_data in self.next_letters.values():
            letter_data.update_probability(self.occurence)


class Letter():
    def __init__(self):
        self.occurence: int = 0
        self.probability: float = 0

    def increment_occurence(self):
        self.occurence += 1

    def update_probability(self, context_occurence: int):
        self.probability = self.occurence / context_occurence
