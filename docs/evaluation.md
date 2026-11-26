# Evaluation Framework: Filipino First-Name Generator

**Version:** 1.0 | **Date:** November 26, 2026
**Companion to:** `project spec.md`, `lecture.md`

**Legend:** **[MVP]** required for Nov 29. **[CORE EXTENSION]** optional if time remains. **[STRETCH EXTENSION]** after the deadline.

**Status values (used everywhere below):** Not started | In progress | Submitted for review | Passed | Failed | Not applicable.
A task is only marked **Passed** after the evidence listed has been reviewed. Saying "it's done" moves it to *Submitted for review*, not *Passed*.

---

## 1. Progress Checklist

| ID | Task | Tag | Evidence required | Status |
|---|---|---|---|---|
| P1 | Conditional probability and Markov refresher; checkpoints 1.1 to 2.3 answered | MVP | Written answers | Not started |
| P2 | `data/names.txt` compiled (about 200 to 300 names) | MVP | The file | Not started |
| P3 | `data/SOURCES.md` documents sources and limitations | MVP | The file | Not started |
| P4 | Trainer and sampler working for k = 1 | MVP | Code and sample output | Not started |
| P5 | Chunk size k generalized (k = 1 to 4) with start padding | MVP | Code and sample output | Not started |
| P6 | Experiments k = 1 to 4 recorded | MVP | README section | Not started |
| P7 | README complete | MVP | README | Not started |
| P8 | Simple tests pass | MVP | Test output | Not started |
| P9 | Copy rate and uniqueness computed per k | CORE EXTENSION | Results table | Not started |
| P10 | Held-out likelihood with smoothing | STRETCH EXTENSION | Code and results | Not started |
| P11 | Human ratings of generated names | STRETCH EXTENSION | Ratings data and summary | Not started |
| P12 | Regional subsets | STRETCH EXTENSION | Labeled data and results | Not started |
| P13 | Comparison with a neural character model | STRETCH EXTENSION | Code and comparison | Not started |
| P14 | Larger dataset via PSA request | STRETCH EXTENSION | Data and documentation | Not started |
| P15 | Final technical defense | MVP | Live or written explanation | Not started |

---

## 2. Technical Acceptance Criteria

| ID | Criterion | Tag | How verified |
|---|---|---|---|
| AC-1 | `names.txt` has at least 200 names, one per line, normalized consistently; `SOURCES.md` lists where names came from and states limitations | MVP | File inspection |
| AC-2 | Trainer builds a context-to-next-character count structure; for a hand-built 3-name list it matches your hand calculation | MVP | Comparison with hand table (Lecture Module 3) |
| AC-3 | Generator produces names for k = 1; every output ends via the end marker or the maximum-length cap | MVP | Run and inspect |
| AC-4 | k is configurable for k = 1 to 4; invalid k is rejected with a clear message | MVP | Run with valid and invalid k |
| AC-5 | The README reports sample names and your written observations for each k | MVP | README review |
| AC-6 | Copy rate and uniqueness rate are computed per k and reported with a stated limitation | CORE EXTENSION | Results table and code review |
| AC-7 | README explains how to run, data sources, results, and limitations; claims match actual output | MVP | README review |
| AC-8 | Same seed and settings give identical output | MVP | Run twice and compare |

---

## 3. Testing Requirements [MVP]

Write simple assertion-based tests (no framework needed). Minimum set:

1. Seed reproducibility: two runs with the same seed give the same list.
2. No generated name contains a start or end marker character.
3. Every generated name has length between 1 and the maximum.
4. Every character in every generated name appears in the training data.
5. Training on a tiny list gives the counts you computed by hand.
6. Invalid chunk size (0, negative, non-integer) is rejected.

Report which tests pass and show the output. A test that you did not run is not counted.

---

## 4. Personal Performance Rubric (100 points)

Scores are assigned only from evidence (code, results, written answers, live explanation). I will not assign scores without evidence.

| Criterion | Weight | Excellent | Proficient | Developing | Needs Improvement |
|---|---|---|---|---|---|
| Theoretical understanding | 30 | Explains conditional probability, Markov assumption, MLE counting, and chunk size tradeoff correctly in own words, with examples | Explains most correctly with minor gaps | Explains some parts but mixes up key ideas (for example P(A given B) versus P(B given A)) | Cannot explain without prompting |
| Implementation | 25 | Clean, correct, tested code for all MVP requirements | Works for MVP with minor issues | Partly works; significant bugs | Does not run |
| Experiments and interpretation | 15 | Compares k = 1 to 4 with evidence; explains trends and limits of the conclusions | Compares and describes trends | Lists outputs without interpretation | No comparison |
| Debugging and independence | 10 | Diagnoses and fixes problems by reasoning; uses hints sparingly | Fixes most problems with some hints | Needs frequent guidance | Cannot debug |
| Technical decisions | 10 | Defends every item in Section 14 of the spec with reasons | Defends most | Gives reasons for some | No reasons |
| Documentation | 10 | README is accurate, complete, honest about limitations | Mostly complete | Missing important parts | Missing or inaccurate |

Core and stretch extension work is **not required** for a full score. It is recorded separately under Portfolio Assessment.

---

## 5. Knowledge Assessment

Checkpoints are in `lecture.md`. Additional integrative questions (answer in your own words, no code):

1. Explain what the model "knows" after training and what it does not know.
2. Why is the generated name list not just a shuffled copy of the training list?
3. Suppose your list contains many names ending in "-ito" and few ending in "-ay". How will the model's output reflect this, and is that a feature or a problem?
4. A classmate says "k = 5 gives the best names because they look the most real." What is wrong with that reasoning?
5. Predict how the output changes if you double the dataset. Which k benefits most, and why?
6. **[CORE EXTENSION]** Why does copy rate alone not measure whether names "sound Filipino"?
7. **[STRETCH EXTENSION]** Why can plain count-based probabilities fail when scoring unseen test names, and what does smoothing do?

**Challenge exercises** (combine earlier ideas, independent work):
- Modify your trainer to treat multi-word names differently, then compare outputs.
- Find a bug in a deliberately broken short trainer description provided by the mentor.

---

## 6. Final Technical Defense [MVP]

Be prepared to explain, without reading from notes:

1. The problem and why a naive approach (random letters or sampling from the list) fails.
2. The mathematics: conditional probability, Markov assumption, MLE counting, with the worked example from Lecture Module 3.
3. Your architecture and data flow.
4. Your dataset: sources, size, biases, and limitations.
5. Each design decision from the spec (multi-word names, start padding, maximum length, filtering copies).
6. Your results across k = 1 to 4 and what they show.
7. Limitations (what the model cannot do) and honest weaknesses of your evaluation.
8. Possible improvements, including the extensions.

Format: a 10-minute explanation followed by questions from the mentor. Score it under "Theoretical understanding" and "Technical decisions."

---

## 7. Definition of Done

### 7.1 Universal completion standards

- [ ] Objectives are satisfied.
- [ ] Required deliverables are implemented.
- [ ] Technical requirements are met.
- [ ] Appropriate tests have been run.
- [ ] Results are documented.
- [ ] Limitations are identified.
- [ ] Documentation is updated.
- [ ] Work is reproducible (seed, instructions).
- [ ] You can explain the important technical decisions.
- [ ] Final evaluation is completed.

### 7.2 Project-specific standards (machine learning / statistical modeling)

- [ ] The probabilities the model uses can be traced to counts in the training data.
- [ ] Chunk size effects are demonstrated with evidence, not only claimed.
- [ ] Claims about output quality are limited to what was actually measured. Anything beyond that is labeled as opinion.
- [ ] **[CORE EXTENSION]** Copy rate and uniqueness reported with their limitations.
- [ ] **[STRETCH EXTENSION]** Any claim of "better" or "more Filipino-sounding" is backed by held-out measurement or human ratings.

### 7.3 Three completion states (reported separately)

| State | Meaning | Current |
|---|---|---|
| **Implementation Complete** | AC-1 to AC-5, AC-7, AC-8 passed and Section 3 tests pass | Not started |
| **Learning Complete** | Rubric total of at least 70 with Theoretical understanding at Proficient or above, and the defense completed | Not started |
| **Portfolio Ready** | Standards in Section 9 met | Not started (not expected by Nov 29) |

A project can reach one state without the others.

---

## 8. Evidence-Based Assessment Rules

- Source code, test output, experiment output, written explanations, and your live explanation count as evidence.
- "I finished it" is not evidence.
- A task that depends on measurement (for example copy rate) is only Passed if I can see how it was computed.
- Results must be reproducible by running your README instructions.

---

## 9. Portfolio Assessment

**Current classification: Exploratory Project.** This follows from its scope: a small, self-compiled dataset, one method, and limited evaluation. This is an honest label, not a judgment of effort.

**Target career relevance:** Data and AI roles, mainly as evidence of probabilistic modeling and clean small-scale implementation.

| Criterion | Where it stands after the MVP | What would improve it |
|---|---|---|
| Technical depth | Basic | Held-out likelihood with smoothing; comparison with a neural model [STRETCH] |
| Problem significance | Modest | A clear use case or an analysis of Filipino naming patterns |
| Originality / adaptation | Moderate (Filipino adaptation of a known technique) | Regional subsets; analysis of what patterns the model learned [STRETCH] |
| Implementation quality | Depends on your code and tests | Cleaner structure, more tests |
| Evaluation rigor | Weak (only observation) | Copy and uniqueness [CORE]; held-out likelihood and human ratings [STRETCH] |
| Reproducibility | Good if seed and README are complete | Pinned environment notes, fixed data splits |
| Documentation | Depends on README | Include limitations and results tables |
| Ability to defend decisions | Assessed in the defense | Written decision log |
| Dataset quality | Small, self-compiled | Documented, larger, ethically sourced data [STRETCH] |
| Relevance to target roles | Moderate | Add a comparison and rigorous evaluation |

**Path from Exploratory to Portfolio Development Candidate:** complete the core extension, then at least two stretch items (held-out evaluation plus either human ratings or a comparison model), with results written up honestly.

---

## 10. Revision History

| Version | Date | Change | Approval |
|---|---|---|---|
| 1.0 | 2026-11-26 | Initial version | Approved |
