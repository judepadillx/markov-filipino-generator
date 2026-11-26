# Project Spec: Filipino First-Name Generator (Character-Level Markov Chain)

**Version:** 1.0 | **Date:** November 26, 2026 | **Owner:** Jude Gabriel Padilla
**Status:** Project direction approved (Gate 1) and technical plan approved (Gate 2)
**Hard deadline:** November 29, 2026 (Sunday)

**Legend used in every document:**
- **[MVP]**: required for the deadline.
- **[CORE EXTENSION]**: valuable, small, done only if MVP is finished with time to spare.
- **[STRETCH EXTENSION]**: after the deadline; not a commitment.

---

## 1. Project Overview

A Python program that learns letter patterns from a list of Filipino first names and generates new names that sound plausible but are not simply copies of the list. It is modeled on a video that uses Markov chains for procedural name generation. This project adapts the idea to Filipino first names.

**Classification:** Beginner difficulty, Exploratory Project (learning exercise). It can become a Portfolio Development Candidate only after the extensions are done (see `evaluation.md`, Section 9).

## 2. Problem Statement

How can we generate new, believable Filipino first names without (a) producing random letter strings or (b) repeating names from an existing list? The method must learn statistical patterns from real names and must not require hand-written phonetic rules.

## 3. Objectives

1. **[MVP]** Build a working character-level Markov name generator from scratch, with an adjustable chunk size.
2. **[MVP]** Understand the underlying probability: conditional probability, the Markov assumption, and estimating probabilities by counting.
3. **[MVP]** Observe and explain how chunk size changes the output (variety versus realism).
4. **[MVP]** Document the dataset, its sources, and its limitations.
5. **[CORE EXTENSION]** Measure copy rate and uniqueness across chunk sizes.
6. **[STRETCH EXTENSION]** Evaluate quality more rigorously and compare with another method (Section 11).

## 4. Scope

| Tag | In scope |
|---|---|
| **[MVP]** | Self-compiled list of about 200 to 300 Filipino first names; Python standard library only; start and end markers; chunk size configurable; seeded randomness; command-line output; experiments at chunk sizes 1 to 4; README |
| **[CORE EXTENSION]** | Copy rate and uniqueness rate per chunk size, reported in a small table |
| **[STRETCH EXTENSION]** | Held-out likelihood with smoothing; human "sounds Filipino" ratings; regional subsets; comparison with a small neural model; larger dataset via a PSA data request |
| **Out of scope** | Surnames (decided: first names only); gender prediction; meaning or etymology; web app; scraping private or personal data |

## 5. Constraints

- Time: about 3 hours on Saturday (Nov 28) and 3 hours on Sunday (Nov 29), roughly 6 hours total.
- Language and libraries: Python, standard library only, so the logic is implemented by the learner.
- No GPU or paid services needed.
- Implementation code is written by the learner. Mentor feedback is by review, hints, and explanation.

## 6. Functional Requirements

**[MVP]**
- **FR-1** Load a text file with one name per line.
- **FR-2** Normalize names (case, whitespace, special characters). Handling of multi-word names, hyphens, and characters like "ñ" is a decision the learner makes and documents (Section 14).
- **FR-3** Add start and end markers to each name.
- **FR-4** Train: for a given chunk size k, record which character followed each k-character context, and how often.
- **FR-5** Generate: starting from the start marker, repeatedly sample the next character weighted by those counts until the end marker is drawn or a maximum length is reached.
- **FR-6** Chunk size k and the random seed are configurable.
- **FR-7** A command-line run prints N generated names.
- **FR-8** Run experiments at k = 1, 2, 3, 4 and record sample outputs and observations in the README.

**[CORE EXTENSION]**
- **FR-9** Compute copy rate (share of generated names that appear exactly in the training list) and uniqueness rate (share of distinct names among those generated) for each k.

**[STRETCH EXTENSION]**
- **S-1** Held-out likelihood or perplexity with a smoothing method, to choose k objectively.
- **S-2** Human ratings of "sounds Filipino" on a sample of generated names.
- **S-3** Regional subsets (for example Bikolano or Ilocano names), if reliably labeled data can be found.
- **S-4** Comparison against a small neural character model (for example the MLP variant in Karpathy's makemore).
- **S-5** Larger dataset via a formal PSA data request.

## 7. Non-Functional Requirements

- **Reproducibility:** the same seed and settings produce the same output.
- **Readability:** functions have clear names and short docstrings; no unexplained magic numbers.
- **Robustness:** generation always terminates (maximum length enforced); invalid k is rejected with a clear message.
- **Documentation:** README explains how to run it, what the data is, results, and limitations.

## 8. Architecture

```
names.txt --> load & normalize --> add markers --> TRAIN (count next-char per context)
                                                         |
                                           model: context -> {char: count}
                                                         |
                       seed, k  --> GENERATE (sample next char until end) --> names
                                                         |
                                         [CORE EXT] copy rate / uniqueness
```

Components: data loader, trainer, generator, command-line entry point. No other components.

## 9. Technology Stack

| Category | Item |
|---|---|
| **Required** | Python 3, standard library only (for example `random`, `collections`, `argparse`) |
| **Recommended** | Git for version history; a plain text editor or any IDE |
| **Optional / Advanced** | Notebook for experiments; PyTorch only for the stretch comparison |

## 10. Data Requirements

- File `data/names.txt`, one first name per line, about 200 to 300 names.
- File `data/SOURCES.md` listing where each batch of names came from.
- Seed sources: the PSA most-common-baby-names infographics (top 10 per year; small), plus names the learner knows. Do not copy from sources whose terms forbid it, and do not collect private data.
- **Known limitations to state in the README:** the list is small, compiled by one person, and biased toward names the learner knows and toward currently popular names. The PSA only publishes top-10 lists openly, which is why a self-compiled list is needed.

## 11. Implementation Phases

| Phase | When | Objective | Acceptance |
|---|---|---|---|
| 1. Refresher | Sat, 45 min | Conditional probability, Markov assumption (`lecture.md` Part I) | Checkpoints 1.1 to 1.3 answered |
| 2. Dataset | Sat, 60 min (hard cap) | Compile `names.txt` and `SOURCES.md` | AC-1 |
| 3. Core chain, k = 1 | Sat, 75 min | Training and sampling working | AC-2, AC-3 |
| 4. General k | Sun, 60 min | Chunk size and start padding for any k | AC-4 |
| 5. Experiments | Sun, 45 min | Compare k = 1 to 4, record observations | AC-5 |
| 6. **[CORE EXTENSION]** | Sun, 45 min (optional) | Copy rate and uniqueness | AC-6 |
| 7. Wrap-up | Sun, 30 min | README and defense preparation | AC-7 |

If time runs short, drop Phase 6, never Phase 7.

## 12. Expected Deliverables

```
filipino-name-generator/
  README.md
  data/names.txt
  data/SOURCES.md
  generator.py        (or a small package)
  tests/ or test_generator.py   (simple assertions)
```

## 13. Risks and Limitations

| Risk | Mitigation |
|---|---|
| Dataset compilation overruns | Hard cap of 60 minutes; 200 names is enough |
| Six hours is tight | Extensions are explicitly optional |
| Small data gives repetitive or odd output | State it as a limitation; use it as a learning point about overfitting |
| Model captures letter patterns only | State it; it has no concept of meaning or grammar |
| Output may accidentally spell inappropriate or real-person names | Review generated samples before sharing them publicly |

## 14. Design Decisions Left to the Learner

These are deliberate, and you should be able to defend each one:

1. How to treat multi-word names (such as "John Paul"), hyphens, and "ñ".
2. How to pad the start of a name when the chunk size is greater than 1.
3. Maximum generated length.
4. Whether to filter out generated names that exactly match training names (and what that does to the experiment).

## 15. Acceptance Criteria (summary)

Full criteria and tests are in `evaluation.md`. In short: the program trains and generates for k = 1 to 4, is reproducible with a seed, always terminates, and its documented results and limitations match what it actually produces.

## 16. Terminology Note

**Chunk size k** means the number of previous characters used as context (the "state"). So k = 1 is a bigram model, k = 2 a trigram model, and in general this is an n-gram model with n = k + 1.

## 17. Revision History

| Version | Date | Change | Reason | Affected docs | Approval |
|---|---|---|---|---|---|
| 1.0 | 2026-11-26 | Initial version | First complete plan | all | Approved by user |
| (direction) | 2026-11-26 | Scope set to first names only; extensions included and labeled | User request | all | Approved by user |

## 18. References (details in `lecture.md`)

- Jurafsky and Martin, *Speech and Language Processing*, 3rd ed. draft, Chapter 3: https://web.stanford.edu/~jurafsky/slp3/
- PSA most common baby names, 2020 infographic: https://psa.gov.ph/sites/default/files/infographics/VS-most-common-baby-names-2020.pdf
- Karpathy, makemore (stretch comparison): https://raw.githubusercontent.com/karpathy/makemore/master/README.md
- Source video (user-provided): https://youtu.be/rYSVFScr7qw
