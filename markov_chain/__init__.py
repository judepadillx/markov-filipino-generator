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
            sample = random.uniform(0, 1)

            cumulative_distribution = self._build_cumulative_distribution(
                context)

            for entry in cumulative_distribution:
                scope = entry['scope']
                letter = entry['letter']

                if scope['min'] <= sample and sample < scope['max']:
                    text += letter
                    break

            # Update context for the next iteration
            context = context[1:] + text[-1]

        return self._strip_mark(text)

    def _build_cumulative_distribution(self, context):
        """Using inverse transform sampling, this builds a cumulative distribution for all possible next letter given a context"""
        cumulative_distribution: list[dict] = []
        min_range = 0
        max_range = 0

        for letter, letter_data in self.contexts[context].next_letters.items():
            # Calculate max range by getting the current cumulative probability
            max_range = min_range + letter_data.probability

            # Construct the current cumulative distribution
            current = {
                'scope': {
                    'min': min_range,
                    'max': max_range
                },
                'letter': letter
            }

            cumulative_distribution.append(current)

            # Update min range for next iteration
            min_range = max_range

        return cumulative_distribution

    def _mark(self, text):
        # Mark beginning and ending of text
        return self.start_marker + text + self.end_marker

    def _strip_mark(self, text: str):
        # Remove beginning and ending marks of text
        return text.removeprefix(self.start_marker).removesuffix(self.end_marker)
