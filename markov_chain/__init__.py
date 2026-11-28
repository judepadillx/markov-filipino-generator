from markov_chain.metadata import Context


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

            for t in range(self.k, len(name)):
                context = name[t-self.k:t]
                next_letter = name[t]

                # Add context metadata if context has not been recorded yet
                if context not in self.contexts:
                    self.contexts[context] = Context()

                # Add next letter given the context
                self.contexts[context].add_next_letter(next_letter)

        # Calculate the probabilities
        for context_data in self.contexts.values():
            context_data.update_probabilities()

    def _mark(self, text) -> str:
        # Mark beginning and ending of text
        return self.start_marker + text + self.end_marker
