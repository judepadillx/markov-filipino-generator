# Lecture Notes: Markov Chains for Name Generation

**Version:** 1.0 | **Date:** November 26, 2026
**Companion to:** `project spec.md`, `evaluation.md`

**Legend:** **[MVP]** required for Nov 29. **[CORE EXTENSION]** optional if time remains. **[STRETCH EXTENSION]** after the deadline.

**How to use this file:** Work through the modules in order, one at a time. After each module, answer its checkpoint questions in your own words, then bring them to review. Write the code yourself; these notes deliberately contain no implementation code.

---

## Learning Roadmap (about 45 min of reading and exercises on Saturday, then learning continues while building)

| Module | Topic | Tag | When |
|---|---|---|---|
| 1 | Conditional probability refresher | MVP | Sat, before coding |
| 2 | Markov chains and the Markov assumption | MVP | Sat, before coding |
| 3 | Counting to estimate probabilities | MVP | Sat, while building |
| 4 | Sampling the next character | MVP | Sat, while building |
| 5 | Chunk size, overfitting, and start padding | MVP | Sun |
| 6 | Measuring copy rate and uniqueness | CORE EXTENSION | Sun, if time |
| 7 | Held-out likelihood and smoothing | STRETCH EXTENSION | After deadline |
| 8 | Comparing against a neural character model | STRETCH EXTENSION | After deadline |

---

# PART I: FOUNDATIONS

## Module 1: Conditional Probability [MVP]

**Objectives:** Define P(A | B), compute it from counts, and explain it in plain words.

**Prerequisites:** You have covered this before; this is a refresher.

**Concept.** The conditional probability of A given B is the probability that A happens when we already know B happened:

> P(A | B) = P(A and B) / P(B)

In counts: among all cases where B happened, what fraction also had A?

**Example (letters).** Suppose you look at every place the letter "a" appears in a list of names and ask: what letter comes right after? If "a" appears 5 times, and "n" follows it 3 of those times, then P(next = n | current = a) = 3/5.

**Relevance to the project.** The entire generator is a table of conditional probabilities: given the recent letters, how likely is each possible next letter?

**Checkpoint 1.1.** In your own words, what is the difference between P(n | a) and P(a | n)? Give a concrete example from names.
**Checkpoint 1.2.** Why must the probabilities of all possible next letters after a given context add up to 1?
**Checkpoint 1.3.** Pick any three Filipino names from memory. Compute P(next letter = a | current letter = n) by hand across just those names.

## Module 2: Markov Chains and the Markov Assumption [MVP]

**Objectives:** Explain what a state and a transition probability are, and what the Markov assumption simplifies.

**Concept.** A Markov chain is a system that moves between states, where the next state depends only on the current state (or, in a more general version, only on the last few states), not on everything before.

For text, a full conditional probability would depend on the whole prefix:

> P(x_t | x_1, x_2, ..., x_(t-1))

The **Markov assumption** replaces the entire history with only the last k characters:

> P(x_t | x_1 ... x_(t-1)) is approximated by P(x_t | x_(t-k) ... x_(t-1))

Here **k is the chunk size** from the project: how many previous characters are used as the state. The Jurafsky and Martin textbook calls this an n-gram approximation and notes that an n-gram looks n-1 units into the past (so n = k + 1).

**Why it matters.** Without the assumption, almost every long prefix would be unique and you could not estimate any probabilities from a small list. The assumption trades accuracy for the ability to learn from limited data.

**Checkpoint 2.1.** Explain the Markov assumption to a classmate without using the words "state" or "transition."
**Checkpoint 2.2.** For the name "Angelica" and k = 2, list each (context, next character) pair the model would learn, including start and end markers.
**Checkpoint 2.3.** What is lost when k = 1 compared to k = 3? What is gained?

---

# PART II: TECHNICAL UNDERSTANDING

## Module 3: Counting to Estimate Probabilities [MVP]

**Objectives:** Turn a list of names into a table of transition probabilities.

**Concept.** Use special characters for the start and end of a name (for example `^` and `$`). Count how often each character follows each context, then divide each count by the total count for that context. This is called **maximum likelihood estimation (MLE)**:

> P(c | context) = count(context followed by c) / count(context)

**Worked example (k = 1).** Training names: `ana`, `anna`, `ani`. Marked as `^ana$`, `^anna$`, `^ani$`.

All transitions: ana gives ^→a, a→n, n→a, a→$. anna gives ^→a, a→n, n→n, n→a, a→$. ani gives ^→a, a→n, n→i, i→$.

| Context | Next: counts | Probabilities |
|---|---|---|
| ^ | a: 3 | P(a given ^) = 3/3 = 1 |
| a | n: 3, $: 2 (total 5) | P(n given a) = 3/5, P($ given a) = 2/5 |
| n | a: 2, n: 1, i: 1 (total 4) | P(a given n) = 2/4, P(n given n) = 1/4, P(i given n) = 1/4 |
| i | $: 1 | P($ given i) = 1 |

The model's probability of generating `ana` is P(a given ^) x P(n given a) x P(a given n) x P($ given a) = 1 x 3/5 x 2/4 x 2/5 = 0.12.

**Relevance.** Your trainer builds exactly this table, with larger contexts when k > 1. Notice that it stores counts; probabilities come from dividing by the context total.

**Checkpoint 3.1.** Using the table above, compute the model's probability of generating `ani` and of generating `anna`. Show your steps.
**Checkpoint 3.2.** The model can generate a name that is not in the training list. Using this table, find one and compute its probability.
**Checkpoint 3.3.** Why does the generator not need to compute the probabilities explicitly if the counts are stored with repeats or as weights?

## Module 4: Sampling the Next Character [MVP]

**Objectives:** Explain weighted random choice and why generation needs a stopping rule.

**Concept.** To generate, begin at the start marker and repeatedly choose the next character at random, weighted by the learned probabilities, until the end marker is chosen. Because choices are random, running the program twice gives different names unless you fix the seed.

**Practical points.**
- A **seed** makes randomness repeatable (needed for debugging and for reproducible results).
- A **maximum length** guards against rare very long outputs.
- A context that was never seen in training has no known next character. With real training names, every context reached while generating was seen in training, but check how this changes if you later filter or change the data.

**Checkpoint 4.1.** Why does fixing a seed matter for debugging?
**Checkpoint 4.2.** Is it possible for the model to get stuck at a context with no options? Explain using how the table is built.
**Exercise 4.1 (independent coding, no solution provided).** Write the trainer for k = 1 and print the table for a 5-name list. Compare it with a hand-built table.
**Exercise 4.2.** Write the sampler and generate 10 names from your 5-name list. What do you notice?

## Module 5: Chunk Size, Overfitting, and Start Padding [MVP]

**Objectives:** Explain the variety-versus-realism tradeoff and design start padding.

**Concept.**
- **Small k** (1): little context; names are varied but can be unnatural.
- **Medium k** (2 to 3): captures common endings and beginnings; usually the best balance.
- **Large k** (4 and above, relative to name length): the model has seen each context very few times, so it tends to reproduce training names. This is **overfitting**: it memorizes rather than generalizes.

**Start padding.** When k > 1, the first characters of a name do not yet have k characters of context. You must decide how to represent that (for example by padding with start markers). This is one of the design decisions you must justify.

**Relevance.** This is the main experiment of the project (Phase 5): generate names for k = 1 to 4 and describe the trend.

**Checkpoint 5.1.** Predict, before running, what happens to the share of generated names that appear in your training list as k increases. Then run it and compare.
**Checkpoint 5.2.** Why does a small dataset make high k worse?
**Checkpoint 5.3.** Defend your choice for handling multi-word names such as "John Paul" and hyphens.
**Exercise 5.1.** Modify your k = 1 code so k is a parameter (a refactor of your own code). Test for k = 1, 2, 3, 4.
**Exercise 5.2.** Debugging challenge: deliberately remove start padding for k = 3 and describe what goes wrong in the first characters.

---

## Module 6: Copy Rate and Uniqueness **[CORE EXTENSION]**

**Objectives:** Define and compute two simple quality measures.

**Concept.**
- **Copy rate:** share of generated names that exactly match a name in the training list.
- **Uniqueness rate:** share of distinct names among all generated names (this catches a model that repeats the same few outputs).

Neither measure tells you whether names *sound Filipino*; they only tell you about novelty and diversity. State this limitation when you report results.

**Checkpoint 6.1.** Why can a model have a low copy rate and still produce poor names?
**Checkpoint 6.2.** Explain what trend you expect across k and why, then compare with your results.

---

# PART III: PRACTICAL APPLICATION

## Project Application Checklist [MVP]

1. Complete Modules 1 and 2, then answer checkpoints.
2. Compile `data/names.txt`, recording sources in `data/SOURCES.md`.
3. Implement Modules 3 and 4 (k = 1), then generalize in Module 5.
4. Record experiment observations in the README.

## Modules for After the Deadline **[STRETCH EXTENSION]**

### Module 7: Held-Out Likelihood and Smoothing

**Idea.** To choose k objectively, split the names into training and test parts, train on one, and measure how probable the model finds the test names. Under plain counting, a test name containing a context or transition never seen in training gets probability zero, which breaks the measurement. **Smoothing** fixes this by reserving a little probability for unseen events. The Jurafsky and Martin chapter covers training and test sets, perplexity, and smoothing.

**Checkpoint 7.1.** Why does plain counting assign zero probability to unseen transitions, and why is that a problem for evaluation?

### Module 8: Comparing with a Neural Character Model

**Idea.** Karpathy's makemore project describes a family of character-level models for names, from simple bigram count tables to MLPs and Transformers. A fair comparison needs the same data split and the same evaluation measure for both models.

**Checkpoint 8.1.** What would make a comparison between your Markov model and a neural model unfair?

### Other stretch ideas
- Human ratings of "sounds Filipino" (design a short rating scale and use several raters).
- Regional subsets, if you can find reliable, labeled data.
- Larger dataset via a formal PSA data request (the PSA's FOI portal lists related requests; availability to you is unverified).

---

## Resources

### Essential
- **Jurafsky and Martin, *Speech and Language Processing*, 3rd ed. draft, Chapter 3 "N-gram Language Models"**, Stanford. Primary educational source. Read the sections on n-grams, the Markov assumption, and estimating probabilities by counting. https://web.stanford.edu/~jurafsky/slp3/
- **Source video** (the project's inspiration): https://youtu.be/rYSVFScr7qw

### Recommended
- **PSA most common baby names, 2020 infographic** (official source for seed names; only top 10 per year): https://psa.gov.ph/sites/default/files/infographics/VS-most-common-baby-names-2020.pdf

### Advanced (stretch)
- **Karpathy, makemore** (README describes character-level models for generating names): https://raw.githubusercontent.com/karpathy/makemore/master/README.md
- Perplexity and smoothing sections of the Jurafsky and Martin chapter above.

**Verification note:** These links were located through web search and the content descriptions were checked against the search results. I have not read each document in full. Open each link yourself before relying on it, and report any that fail so they can be corrected.

---

## Revision History

| Version | Date | Change | Approval |
|---|---|---|---|
| 1.0 | 2026-11-26 | Initial version | Approved |
