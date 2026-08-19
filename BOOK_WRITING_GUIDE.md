# SDR with GNU Radio: Book Writing Guide

This document defines the writing, structure, formatting, experimental, and publication conventions for the **SDR with GNU Radio** book.

The book has now developed a mature style across the manuscript, including the revised early chapters. Chapters should therefore be treated as parts of one continuous learning journey rather than as two separate "early" and "later" styles.

The purpose of this guide is **not** to make every chapter mechanically identical. Different subjects need different amounts of explanation, mathematics, GNU Radio guidance, figures, and experimentation. The purpose is to preserve a consistent teaching philosophy, technical standard, and publication-friendly Markdown format across the whole book.

---

# 1. Teaching Philosophy

The book is written for readers who may be new to digital signal processing, software-defined radio, digital communications, or GNU Radio.

The central teaching principle is:

> **Build intuition first. Use mathematics to explain and formalize what the reader has already begun to understand.**

Whenever practical, prefer the progression:

```text
Question
    |
    v
Intuitive explanation
    |
    v
Prediction
    |
    v
Experiment
    |
    v
Observation
    |
    v
Explanation
    |
    v
Mathematics
    |
    v
Practical SDR/radio connection
```

Do not begin a concept with a dense derivation when a physical explanation, small example, figure, or experiment can establish the idea first.

The reader should understand **why something matters** before being asked to manipulate its equations.

---

# 2. The Book Is a Progressive Learning Journey

Each chapter should feel like the natural next question raised by the previous chapter.

Reuse concepts the reader already knows. Do not restart the subject from first principles every time a familiar idea reappears.

As the book progresses:

- assume increasing familiarity with GNU Radio,
- reduce repetitive block-by-block instructions,
- focus more on the signal-processing idea,
- introduce only a few genuinely new ideas at a time,
- connect new concepts to experiments and representations already developed.

The early chapters may still contain more explicit GNU Radio guidance because the reader is learning the environment. Later chapters should increasingly emphasize reasoning, interpretation, and system behaviour.

---

# 3. Chapter Development Workflow

A chapter should normally be developed experimentally before the final Markdown is written.

Use this workflow:

```text
Choose the chapter's main question
        |
        v
Connect it to the previous chapter
        |
        v
Discuss the concept intuitively
        |
        v
Identify likely beginner questions
        |
        v
Design the simplest useful experiment
        |
        v
Predict the result
        |
        v
Build and run the flowgraph
        |
        v
Interpret unexpected results
        |
        v
Save only useful figures
        |
        v
Extend the experiment if needed
        |
        v
Review the complete development discussion
        |
        v
Write the final chapter
```

Do **not** write the final chapter before the important experiments, observations, settings, figures, and conceptual clarifications have been completed.

The original chapter outline is a starting point, not a contract. If experimental development reveals a clearer progression, follow the clearer progression.

---

# 4. Review the Entire Development Conversation Before Writing

The final chapter must not be reconstructed only from the final flowgraphs and screenshots.

Before writing, review the entire chapter-development discussion and preserve the useful conceptual discoveries that emerged along the way.

These often include:

- why an unexpected spectrum has a particular shape,
- why a waveform appears delayed,
- why two similar-looking concepts are actually different,
- why a particular GNU Radio setting matters,
- why an apparently undesirable component is physically necessary,
- why a simple explanation is incomplete,
- how an ideal mathematical model differs from a practical implementation,
- what a receiver actually gains from a processing stage,
- why a result should not be over-interpreted.

Do not include routine troubleshooting, temporary wiring mistakes, abandoned approaches, syntax errors, or conversational back-and-forth unless they reveal a reusable technical lesson.

A useful rule is:

> **Preserve the insight, not the troubleshooting history that produced it.**

---

# 5. Recommended Chapter Structure

A typical chapter may contain:

```text
Chapter Title
    |
    v
Main Question or motivating question
    |
    v
Connection to the previous chapter
    |
    v
First intuitive idea
    |
    v
Experiment X.1
    |
    +--> Purpose / question
    +--> Conceptual reasoning
    +--> Flowgraph
    +--> Important settings
    +--> Prediction
    +--> Result
    +--> Observation
    +--> Explanation
    |
    v
GNU Radio Toolbox
(only when useful)
    |
    v
Next concept / experiment
    |
    v
Putting It All Together
    |
    v
What We Learned
    |
    v
Connecting to the Next Chapter
```

This is a guide, not a rigid template.

Do not add headings merely to satisfy a pattern. If a concept reads more naturally as continuous prose, keep it continuous. If an experiment needs only a result figure and a short explanation, do not force it to contain a full settings section.

The **flow of learning is more important than identical chapter structures**.

---

# 6. Main Questions and Motivating Questions

Whenever appropriate, begin with a clear question that gives the reader a reason to learn the chapter.

For example:

```markdown
## Main Question

**Why can't we simply transmit abrupt rectangular symbols over the air?**
```

Some chapters may work better with a strong opening question without the literal heading `Main Question`. This is acceptable if the chapter still has a clear motivation.

The question should express the problem the chapter solves rather than merely repeat its title.

---

# 7. Connecting Chapters Naturally

Briefly remind the reader what was established previously and identify the unanswered question.

Prefer:

```text
Previously we learned X.
That allowed us to understand Y.
But one question remains:
How / why / what happens when ... ?
```

Avoid long summaries unless they are necessary.

At the end of the chapter, create the next transition in the same way. The next chapter should feel like the answer to a question the current chapter has just raised.

---

# 8. Intuition Before Mathematics

Prefer:

```text
Observation -> intuition -> equation -> interpretation
```

over:

```text
Equation -> derivation -> explanation
```

When introducing an equation:

1. Explain the physical or conceptual problem.
2. Introduce the variables in context.
3. Show the equation.
4. Interpret what it means.
5. Connect it to the experiment where useful.

Do not use mathematics merely because a topic is traditionally taught mathematically.

At the same time, do not avoid an equation when it makes the idea clearer or prevents an inaccurate simplification.

---

# 9. Experiments

Experiments are central to the book.

Use chapter-based numbering:

```markdown
# Experiment 18.1: Rectangular Symbols and Bandwidth
```

An experiment should answer a meaningful question.

Do not add experiments simply to increase the count. A short conceptual figure, calculation, or discussion may sometimes teach the idea better than another flowgraph.

Whenever useful, ask the reader to predict the result before showing it.

The experiment should reveal **why** a design rule exists, not merely demonstrate that GNU Radio can implement it.

---

# 10. Progressive GNU Radio Detail

GNU Radio settings should be given progressively.

When a block is introduced for the first time:

- explain what it does,
- identify the important settings,
- explain why those settings matter,
- give enough information to reproduce the experiment.

When a familiar block is reused:

- do not repeat every setting,
- state only what changed or what matters in the new context,
- explain a new role if the familiar block is being used differently.

When an experiment extends a previous one, explain the extension rather than rebuilding the whole flowgraph verbally.

A useful progression is:

```text
Early chapter
More explicit GNU Radio guidance

        |
        v

Later chapter
More emphasis on DSP meaning and experimental interpretation
```

Keep every experiment reproducible, but do not let later chapters read like configuration manuals.

---

# 11. GNU Radio Settings

Use a compact Markdown table when the experiment has a small group of important parameters:

```markdown
| Parameter | Value |
|---|---:|
| Sample rate | `32000` samples/s |
| Symbol rate | `1000` symbols/s |
| Samples per symbol | `32` |
```

Use a multiline `text` block when showing a block configuration is clearer:

```text
Sample Rate: samp_rate
Frequency:   10k
Amplitude:   1
```

Do not mechanically list unchanged defaults.

Do not omit a setting that is necessary for reproduction or understanding.

Settings that are especially worth documenting include:

- sample rate,
- symbol/bit rate,
- samples per symbol,
- filter cutoff and transition width,
- interpolation or decimation,
- taps and filter span,
- FFT size and averaging,
- modulation sensitivity/deviation,
- noise amplitude,
- thresholds,
- GUI ranges when they are part of the experiment.

---

# 12. Experimental Settings Must Not Be Invented During Final Writing

The final chapter documents experiments that were actually developed.

Do not silently change:

- sample rates,
- frequencies,
- amplitudes,
- bit or symbol rates,
- samples per symbol,
- filter parameters,
- roll-off factors,
- noise amplitudes,
- FFT settings,
- GUI layouts,
- block types,
- trace meanings,
- experimental conclusions.

If something appears questionable during final writing, flag it for review rather than silently replacing it.

---

# 13. GNU Radio Toolbox

Use a **GNU Radio Toolbox** section when a newly introduced block, control, sink, tap generator, or GNU Radio technique deserves explanation.

Example:

```markdown
> ### GNU Radio Toolbox: Chunks to Symbols
>
> The **Chunks to Symbols** block treats each input value as a symbol index and replaces it with the corresponding entry from a symbol table.
```

A Toolbox explanation should normally cover:

- what the block does,
- what enters it,
- what comes out,
- important settings,
- why it is useful in the current experiment,
- a common misunderstanding if one is likely.

Do not create a Toolbox section merely because a block appears.

Do not reintroduce the same block as "new" in a later chapter.

The companion file `docs/gnu-radio-block-master-list.md` should be updated after completed chapters so the book retains one authoritative record of when each block was introduced.

---

# 14. Controlled Examples Before Random Data

When a transformation is difficult to verify with random data, begin with a short known sequence.

For example:

```text
Known bits
    |
    v
Known symbol indices
    |
    v
Known mapped amplitudes
    |
    v
Verify the transformation
    |
    v
Random data
```

This pattern was especially useful in the digital-communication chapters and should be reused whenever it improves understanding.

Do not introduce randomness before the reader has a way to tell whether the system is behaving correctly.

---

# 15. Build Important Operations Manually Before Hiding Them

When a ready-made GNU Radio block would hide the concept being taught, build the operation from simpler blocks first.

Examples from the book include:

- mixing with Multiply,
- AM construction,
- FM from a VCO,
- BPSK/QPSK/QAM constellation construction,
- matched filtering from FIR taps.

After the underlying operation is understood, convenience blocks can be introduced later without becoming black boxes.

This is not a rule that everything must always be built manually. Use manual construction when it teaches the mechanism.

---

# 16. "Try It Yourself"

Use **Try It Yourself** sections selectively.

They are useful when a small change reveals an additional concept without requiring a new full experiment.

Good examples include:

- changing sample rate,
- changing FFT size,
- increasing noise,
- moving an LO,
- changing filter cutoff,
- changing a threshold,
- changing modulation depth,
- changing roll-off,
- changing symbol rate.

Whenever appropriate, ask the reader to predict what will happen first.

Do not add a Try It Yourself section mechanically after every experiment.

---

# 17. Deliberately Breaking a Working System

A "Now Break the Flowgraph" style discussion is useful when failure teaches the design rule.

Examples include:

- violating a sampling condition,
- moving a filter cutoff into the wanted signal,
- using the wrong local-oscillator frequency,
- creating overmodulation,
- sampling at a poor decision time,
- mismatching communication-system parameters.

Do not create a separate experiment for every possible failure. If the chapter is already long, a concise discussion may be better.

---

# 18. Unexpected Results and Easily Confused Concepts

When an experiment produces something a beginner may misinterpret, address it directly.

Examples include distinctions such as:

```text
Filter delay != ISI
Pulse overlap != necessarily ISI
I/Q description != a different signal from amplitude/phase description
Symbol index != transmitted symbol value
Repeat != proper interpolation filtering
RRC response != complete RC response
Eye diagram != a new signal
Matched filtering != removing all noise
```

These clarifications are often more valuable than another equation.

Never leave a misleading visual result unexplained.

---

# 19. Ideal Models Versus Practical Implementations

The book should use ideal models when they build intuition, but clearly identify their limitations.

Examples:

- ideal impulses,
- ideal sinc pulses,
- ideal brick-wall filtering,
- ideal coherent oscillators,
- perfect symbol timing.

A useful progression is:

```text
Ideal model
    |
    v
What it teaches
    |
    v
Why it cannot be implemented exactly
    |
    v
Practical approximation
```

This prevents the reader from confusing a teaching model with a realizable radio system.

---

# 20. Python and Other Supporting Analysis

GNU Radio should remain the main experimental environment, but a small Python script may be used when it provides a clearer visualization or calculation than forcing the task into a GNU Radio GUI.

When Python is used:

- state exactly what Python is doing,
- state what processing was already performed in GNU Radio,
- do not imply that a Python visualization is a GNU Radio sink,
- include the useful script in the experiment folder,
- include relevant code in the chapter when it improves reproducibility.

For example, an eye diagram may be constructed in Python from samples recorded by a GNU Radio File Sink. In that case:

```text
GNU Radio
generates and processes the signal
        |
        v
File Sink
records the samples
        |
        v
Python
changes only the visualization
```

Generated GNU Radio `.py` files should not be confused with purpose-written analysis scripts.

---

# 21. Writing Style

The writing should sound natural, clear, and human.

Write as if explaining the idea to an intelligent beginner sitting beside you at GNU Radio.

Prefer direct explanations over unnecessarily formal textbook language.

Avoid:

- unnecessary jargon,
- repetitive summaries,
- excessive headings,
- excessive bold text,
- mechanical "definition -> equation -> example" repetition,
- artificial transitions,
- claims that overstate what an experiment proves.

A reader should feel that each question arises naturally from the previous observation.

---

# 22. Technical Accuracy

Beginner-friendly does not mean technically loose.

Be especially careful with:

- real versus complex signals,
- I/Q representations,
- positive and negative frequency,
- FFT magnitude versus power,
- sampling and aliasing,
- filter bandwidth and transition width,
- mixer products,
- modulation bandwidth,
- noise and SNR,
- correlation and matched filtering,
- bit rate versus symbol rate,
- symbol indices versus physical symbol values,
- pulse shaping and ISI,
- physical RF signals versus complex-baseband representations.

If an explanation is simplified, make the simplification clear when necessary.

Avoid teaching a convenient statement that the reader will later need to unlearn.

---

# 23. Mathematical Formatting

Raw Markdown files must use consistent display-math formatting.

Write `$$` on separate lines with the **complete equation on one physical Markdown line** between them.

Correct:

```text
$$
f_{\text{USB}} = f_c + f_m
$$
```

Also correct:

```text
$$
s(t)=\frac{1}{2}\cos[2\pi(f_c-f_m)t]+\frac{1}{2}\cos[2\pi(f_c+f_m)t]
$$
```

Do not split one display equation across several physical lines:

```text
$$
s(t)
=
...
$$
```

Use inline math with single dollar signs where appropriate.

Do not unnecessarily escape `_`, `*`, `=`, `+`, `(`, or `)`.

Avoid LaTeX array environments when a Markdown table communicates the calculation more clearly.

---

# 24. Tables

Use standard Markdown pipe tables.

```markdown
| Symbol index | Amplitude |
|---:|---:|
| 0 | -3 |
| 1 | -1 |
| 2 | +1 |
| 3 | +3 |
```

Do not use Pandoc-generated plain-text tables.

Use tables for structured comparisons and row-by-row calculations when they improve readability.

---

# 25. Fenced Code Blocks and ASCII Diagrams

Preserve every line break inside fenced code blocks, settings blocks, and ASCII/conceptual diagrams.

Correct:

```text
Message
   |
   v
Modulator
   |
   v
RF Signal
```

Never collapse a multiline diagram onto one line.

Use appropriate language identifiers such as `text` and `python`.

---

# 26. Figures

Use standard Markdown image syntax:

```markdown
![Descriptive caption](../figures/ch18/filename.png)
```

Organize figures by chapter:

```text
figures/
    ch01/
    ch02/
    ...
    ch18/
```

Use descriptive filenames that identify the chapter and experiment where practical.

Prefer:

```text
ch18-exp8-matched-filter-noise-flowgraph.png
ch18-exp8-matched-filter-noise.png
```

over generic names such as:

```text
image1.png
result.png
```

Keep high-resolution originals and avoid unnecessary compression.

---

# 27. Decide Whether a Flowgraph Figure Is Actually Needed

Do not include a flowgraph screenshot automatically for every experiment.

A flowgraph figure is useful when:

- the topology is new,
- the reader needs it to reproduce the experiment,
- it clarifies a new signal path,
- it introduces a new GNU Radio operation.

A flowgraph figure may be unnecessary when:

- the experiment is only a small variation of the previous one,
- the result figure carries the important lesson,
- the flowgraph is visually complicated but conceptually trivial,
- a supporting Python figure is purely explanatory.

Use the minimum number of figures needed to tell the experimental story clearly.

---

# 28. Figure Placement and Explanation

Place each figure near the paragraph where the reader needs it.

A useful pattern is:

```text
What are we about to observe?
        |
        v
Figure
        |
        v
What do we see?
        |
        v
Why does it happen?
```

Never insert a screenshot and leave the reader to discover the lesson alone.

When several traces appear, identify the important traces and explain what comparison matters.

Do not describe irrelevant GUI details.

---

# 29. GNU Radio GUI Layout and Naming

When multiple QT GUI sinks are used, arrange them to support the comparison.

Use meaningful:

- Options titles,
- sink titles,
- axis labels,
- trace names,
- GUI Hint values when layout reproduction matters.

Avoid generic trace names such as `Data 0` in final book figures when a descriptive label is practical.

Do not overcrowd a single sink if separate displays would make the comparison clearer.

---

# 30. Raw Markdown Requirements

The final chapter must be written directly as **plain UTF-8 Markdown**.

Do not use:

- Pandoc,
- pypandoc,
- Markdown-to-Markdown conversion,
- document converters that rewrite the source.

Before finalizing, verify:

- headings,
- display equations,
- inline equations,
- fenced code blocks,
- ASCII diagrams,
- Markdown tables,
- image paths,
- lists,
- blockquotes,
- Toolbox sections.

The source should remain readable both as raw text and when rendered.

---

# 31. Publication-Friendly Markdown

GitHub is useful for storage and preview, but it is not the final publishing engine.

Keep the manuscript portable so it can later become:

```text
Markdown source
      |
      +--> PDF
      |
      +--> EPUB
      |
      +--> HTML / website
      |
      +--> print-ready edition
```

Prefer:

- standard Markdown,
- LaTeX math,
- relative image paths,
- fenced code blocks,
- normal Markdown tables.

Avoid unnecessary GitHub-specific syntax.

---

# 32. Repository Organization

The repository should keep manuscript, experiments, figures, and documentation separate.

A typical structure is:

```text
sdr-with-gnu-radio/
|
+-- book/
|   +-- chapter01.md
|   +-- chapter02.md
|   +-- ...
|   +-- chapter18.md
|
+-- experiments/
|   +-- ...
|
+-- figures/
|   +-- ch01/
|   +-- ch02/
|   +-- ...
|   +-- ch18/
|
+-- docs/
|   +-- chapter-plan.md
|   +-- gnu-radio-block-master-list.md
|   +-- gnuradio-feature-map.md
|
+-- BOOK_WRITING_GUIDE.md
```

Experiment folders may contain:

- `.grc` flowgraphs,
- GNU Radio-generated `.py` files when retained,
- purpose-written Python analysis scripts,
- small captured sample files when they materially improve reproducibility.

Keep naming consistent within each chapter.

---

# 33. Supporting Data Files

Small generated data files may be committed when they make an experiment directly reproducible.

For example, a captured matched-filter stream used to generate an eye diagram can be stored with the experiment if the file size is modest.

Do not commit large generated datasets merely because they exist.

The criterion is:

> **Does keeping this file materially improve reproducibility without unnecessarily bloating the repository?**

---

# 34. GNU Radio Block Master List

After a chapter is completed, update:

```text
docs/gnu-radio-block-master-list.md
```

Update only what the completed experiments justify.

A block should be marked **Used** only after it has actually appeared in a completed experiment.

Also update:

- the first-use chapter,
- important new roles for familiar blocks,
- the chapter-by-chapter GNU Radio progression,
- the "What Comes Next?" section.

Do not let the Master List follow an obsolete chapter plan after the manuscript has evolved.

---

# 35. Whole-Book Consistency Review

Because Chapters 1–10 have now been revised into the mature book style, future editorial work should treat Chapters 1 onward as one manuscript rather than preserving a deliberate early/late style difference.

Periodically check:

- concepts used before introduction,
- repeated explanations,
- terminology,
- notation,
- sample-rate conventions,
- chapter transitions,
- experiment numbering,
- figure naming,
- GNU Radio blocks introduced as "new" more than once,
- Toolbox consistency,
- equation formatting,
- Markdown portability,
- references to outdated chapter plans.

Do not make every chapter artificially identical. Consistency means a shared teaching philosophy and presentation standard, not identical templates.

---

# 36. Final Chapter Writing Prompt

The following prompt can be reused after experimental development is complete.

---

## Standard Final-Writing Prompt

Please now write the complete chapter as a **raw Markdown `.md` file**, following the established structure and formatting style of the book, with Chapters 11 and 12 remaining useful reference examples.

Preserve the Markdown exactly as authored. **Do not use Pandoc or any Markdown conversion tool.**

Follow these formatting rules:

- Write display equations using `$$` on separate lines, with the **complete equation on one physical line** between them.
- Do not split a single display equation across multiple physical Markdown lines.
- Preserve **all line breaks** inside fenced code blocks, GNU Radio settings blocks, and ASCII/conceptual diagrams.
- Never collapse a multiline ASCII diagram or settings block onto one line.
- Use proper multiline fenced code blocks with an appropriate language identifier such as `text` or `python` when useful.
- Use normal Markdown pipe tables.
- Use standard Markdown image syntax, for example `![Caption](../figures/chXX/filename.png)`.
- Do not unnecessarily escape normal Markdown characters such as `_`, `*`, `=`, `+`, `(`, or `)`.
- Write the `.md` file **directly as plain UTF-8 text**. Do not pass it through Pandoc, pypandoc, or another Markdown/document conversion process.
- Before providing the final file, verify that equations, fenced code blocks, ASCII diagrams, tables, image paths, headings, lists, and blockquotes remain valid raw Markdown.

The chapter should be clear, intuitive, naturally written, technically accurate, and suitable for a beginner. Follow the experimental development completed for the chapter. Introduce mathematics only after the underlying physical, geometric, or signal-processing idea has been explained intuitively.

Use **progressive GNU Radio detail**:

- explain newly introduced blocks and important settings fully,
- give only changed or conceptually important settings for familiar blocks,
- state when settings remain unchanged rather than repeating them,
- keep every experiment reproducible without turning the chapter into a configuration manual.

Add a **GNU Radio Toolbox** section only when a newly introduced block or a substantially new use deserves explanation.

Use the figures collected during experimental development and insert them where they advance the explanation. Do not automatically include every flowgraph screenshot.

Include the important questions, doubts, clarifications, observations, and conceptual discussions that arose naturally during development. Review the **entire chapter-development conversation**, not just the final experiments and figures. Preserve useful distinctions and interpretations, but omit routine troubleshooting, temporary mistakes, abandoned experiments, and conversational back-and-forth unless they teach a general lesson.

Include a **Try It Yourself** section when a simple modification gives a useful additional insight. Ask the reader to predict the result first when appropriate. Do not add such sections mechanically.

Do not change the technical conclusions, experimental results, GNU Radio settings, figure meanings, or decisions established during development.

Finish with a meaningful **What We Learned** section and a natural **Connecting to the Next Chapter** section.

Keep the Markdown publication-friendly so the manuscript can later be converted to PDF, EPUB, HTML, and print formats.

---

# 37. Final Principle

The goal is not to produce a collection of technically correct chapters.

The goal is to produce a book in which the reader repeatedly experiences:

```text
I see the problem.
        |
        v
I can predict what might happen.
        |
        v
I can build it.
        |
        v
I can observe it.
        |
        v
I understand why it happened.
        |
        v
I am ready for the next question.
```

That learning experience is the standard against which writing, experiments, figures, equations, and GNU Radio detail should be judged.
