from markov_chain.metadata import Context


class MarkovChain():
    def __init__(self):
        self.contexts: dict[str, Context] = {}

    def train(self, names, k):
        # For each name, count each occurences of next letters given the sequential occuring contexts
        for name in names:
            # Mark beginning and ending of name
            name = self._mark(name, k)

            for t in range(k, len(name)):
                context = name[t-k:t]
                next_letter = name[t]

                # Add context metadata if context has not been recorded yet
                if context not in self.contexts:
                    self.contexts[context] = Context()

                # Add next letter given the context
                self.contexts[context].add_next_letter(next_letter)

        # Calculate the probabilities
        for context_data in self.contexts.values():
            context_data.update_probabilities()

    def _mark(self, text, k) -> str:
        start_marker = '^' * k
        end_marker = '$'

        # Mark beginning and ending of text
        return start_marker + text + end_marker
