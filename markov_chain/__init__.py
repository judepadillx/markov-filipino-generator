from markov_chain.metadata import Context
import random


class MarkovChain():
    def __init__(self, k):
        self.contexts: dict[str, Context] = {}
        self.k = k
        self.start_marker = '^' * k
        self.end_marker = '$'

    def train(self, names):
        # For each name, count each occurences of next letters given the sequential occuring contexts
        for name in names:
            # Mark beginning and ending of name
            name = self._mark(name)

            context = name[0:self.k]

            for t in range(self.k, len(name)):
                next_letter = name[t]

                # Add context metadata if context has not been recorded yet
                if context not in self.contexts:
                    self.contexts[context] = Context()

                # Add next letter given the context
                self.contexts[context].add_next_letter(next_letter)

                # Update context for next iteration
                context = context[1:] + next_letter

        # Calculate the probabilities
        for context_data in self.contexts.values():
            context_data.update_probabilities()

    def generate(self):
        text = self.start_marker

        context = text

        while text[-1] != self.end_marker:
            x = random.uniform(0, 1)

    def _mark(self, text) -> str:
        # Mark beginning and ending of text
        return self.start_marker + text + self.end_marker
