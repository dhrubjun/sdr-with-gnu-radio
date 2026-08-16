# SDR with GNU Radio: Book Writing Guide

This document defines the writing, structure, formatting, experimental, and publication conventions for the **SDR with GNU Radio** book.

The purpose of this guide is not to make every chapter look mechanically identical. Different topics need different amounts of explanation, mathematics, and experimentation. The purpose is to make the book feel like one continuous learning journey, with a consistent teaching philosophy and reliable Markdown formatting.

The conventions developed in **Chapters 11 and 12** should be treated as the main reference for future chapters.

---

# 1. Teaching Philosophy

The book is written for readers who may be new to digital signal processing, software-defined radio, or GNU Radio.

The main principle is:

> **Build intuition first. Use mathematics to explain and formalize what the reader has already begun to understand.**

Whenever possible, the learning sequence should be:

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
GNU Radio experiment
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

Do not begin a new concept with a dense derivation when an experiment, example, or physical explanation can establish the idea first.

The reader should understand **why something matters** before being asked to manipulate its equations.

---

# 2. Chapter Development Workflow

A chapter should normally be developed experimentally before the final Markdown is written.

Use the following workflow:

```text
Choose the chapter's main question
        |
        v
Discuss the concept intuitively
        |
        v
Identify important beginner questions
        |
        v
Design a simple GNU Radio experiment
        |
        v
Predict the result
        |
        v
Build and run the flowgraph
        |
        v
Troubleshoot if necessary
        |
        v
Understand the result
        |
        v
Save the useful figures
        |
        v
Extend the experiment if needed
        |
        v
Only then write the final chapter
```

Do **not** write the final chapter before the important experiments, observations, settings, and conceptual discussions have been completed.

Experiments should normally progress from simple to more complex. Reuse or extend an earlier flowgraph when possible rather than introducing many unrelated blocks at once.

---

# 3. Recommended Chapter Structure

Use Chapters 11 and 12 as the main structural reference.

A typical chapter may follow this pattern:

```text
Chapter Title
    |
    v
Main Question
    |
    v
Connection to the Previous Chapter
    |
    v
First Intuitive Concept
    |
    v
Experiment X.1
    |
    +--> What are we trying to discover?
    +--> GNU Radio Flowgraph
    +--> GNU Radio Settings
    +--> What do we expect?
    +--> Experimental result
    +--> What do we see?
    +--> Why did it happen?
    |
    v
GNU Radio Toolbox
(if a new block/tool needs explanation)
    |
    v
Next Concept / Experiment
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

This is a guide, not a rigid form.

Do not add headings merely to satisfy the template. If two ideas read more naturally as one continuous explanation, keep them together. If an experiment does not need a separate prediction subsection, do not force one.

The **flow of learning is more important than identical section structures**.

---

# 4. Main Question

Whenever appropriate, begin the chapter with a clear **Main Question**.

For example:

```markdown
## Main Question

**Why can't we simply transmit our original low-frequency information signal directly?**
```

The Main Question should express the problem the chapter is trying to solve, not merely repeat the chapter title.

A good Main Question gives the reader a reason to continue.

---

# 5. Connection to the Previous Chapter

New chapters should feel like the next step in one continuous book.

Briefly remind the reader what was established previously and identify the unanswered question that motivates the new chapter.

Do not provide a long summary of the previous chapter unless it is genuinely necessary.

A useful transition often follows this pattern:

```text
Previously we learned X.

That allowed us to do Y.

But one question is still unanswered:

Why / how / what happens when ... ?
```

---

# 6. Intuition Before Mathematics

Explain a concept in ordinary language before introducing its formal equation whenever possible.

Prefer:

```text
Observation -> intuition -> equation -> interpretation
```

over:

```text
Equation -> derivation -> explanation
```

Equations should support understanding, not replace it.

When introducing an equation:

1. Explain what problem it describes.
2. Introduce the variables in context.
3. Show the equation.
4. Interpret what the equation tells us physically or experimentally.
5. Connect it to the GNU Radio result where appropriate.

---

# 7. Experiments

Experiments are central to the book.

Use numbered experiment titles such as:

```markdown
# Experiment 13.1: Observing the AM Envelope
```

Use chapter-based numbering consistently:

```text
Experiment 13.1
Experiment 13.2
Experiment 13.3
```

An experiment should answer a meaningful question. Do not add experiments simply to increase their number.

Whenever useful, tell the reader what to expect **before** showing the result.

This encourages the reader to reason rather than merely copy a flowgraph.

---

# 8. GNU Radio Settings

Provide GNU Radio settings whenever the reader needs them to reproduce an experiment.

Use either a Markdown table or a multiline `text` block, depending on which is clearer.

For compact structured settings, prefer a table:

```markdown
| Setting | Value |
|---|---|
| Sample Rate | `samp_rate` |
| Frequency | `10k` |
| Amplitude | `1` |
| Waveform | Cosine |
```

For a short block configuration, this is also acceptable:

````markdown
```text
Sample Rate:    samp_rate
Frequency:      10k
Amplitude:      1
Waveform:       Cosine
```
````

Do not omit an important setting merely because it seems obvious to an experienced GNU Radio user.

At the same time, do not repeatedly list every unchanged default setting if doing so adds no value.

---

# 9. Progressive GNU Radio Flowgraphs

Build flowgraphs progressively.

Prefer:

```text
Experiment 1: Source -> Sink
Experiment 2: Source -> New operation -> Sink
Experiment 3: Extend Experiment 2 with another stage
```

rather than constructing a large receiver with many unfamiliar blocks at once.

Whenever possible, reuse blocks and ideas introduced earlier in the book.

If a familiar block takes on a new role, explain the new role even if the block itself is not new.

---

# 10. GNU Radio Toolbox Sections

When a GNU Radio block, control, display, or tool is introduced for the first time, add a **GNU Radio Toolbox** section when an explanation will help the reader.

Example:

```markdown
> ### GNU Radio Toolbox: Multiply
>
> The **Multiply** block multiplies its input streams sample by sample.
>
> In a mixer or modulator, this operation creates new frequency components related to the sum and difference of the input frequencies.
```

The Toolbox should explain:

- what the block does,
- what its important settings mean,
- why it is being used in the current experiment,
- where the reader may encounter it again.

Do not create a Toolbox section merely because a block appears in a flowgraph. Use it when the block is new or when its role deserves clarification.

---

# 11. Important Questions and Discussions from Chapter Development

The final chapter must not be limited to the original outline or the final screenshots.

Include important questions, doubts, clarifications, observations, and conceptual discussions that arose naturally while developing the chapter.

These often contain some of the most useful explanations for a beginner.

Examples include:

- a question raised by an unexpected spectrum,
- why a particular GNU Radio setting was chosen,
- the difference between two easily confused concepts,
- why an apparently unwanted spectral component is actually necessary,
- how the GNU Radio experiment relates to a real receiver,
- why an experimental amplitude differs from the original signal,
- what a mathematical term means physically.

Place these discussions at the most natural point in the final chapter.

Do **not** include routine troubleshooting, accidental wiring mistakes, temporary syntax errors, abandoned experiments, or conversational back-and-forth unless they reveal a useful general lesson for the reader.

Before writing the final chapter, review the **entire chapter-development conversation**, not only the final experiment and figures.

---

# 12. Try It Yourself

Use **Try It Yourself** sections selectively.

They are useful when a small modification of an existing experiment can reveal an additional concept without requiring a completely new experiment.

Example:

```markdown
### Try It Yourself

Keep the carrier frequency unchanged and gradually increase the message amplitude.

Before running the flowgraph, predict what you expect to happen to the envelope.

Then compare your prediction with the result.
```

Good Try It Yourself activities include:

- changing sample rate and observing aliasing,
- changing FFT size,
- changing noise amplitude or SNR,
- moving a local oscillator,
- changing filter cutoff or transition width,
- changing a detection threshold,
- changing modulation depth,
- deliberately breaking an otherwise correct flowgraph.

Whenever appropriate, ask the reader to **predict the result before changing the parameter**.

Do not add a Try It Yourself section mechanically after every experiment.

---

# 13. "Now Break the Flowgraph" Experiments

When deliberately changing a correct system helps expose an important limitation, use a **Now Break the Flowgraph** style section.

Examples include:

- violating the Nyquist criterion,
- moving a filter cutoff into the desired signal,
- using the wrong LO frequency,
- setting an unsuitable threshold,
- creating overmodulation.

These sections should have a clear learning purpose. They should show the reader not only what works, but also **why a particular design rule exists**.

---

# 14. Writing Style

The writing should sound natural, clear, and human.

Prefer short, direct explanations over formal textbook language when both are equally accurate.

Write as if explaining the idea to an intelligent beginner sitting beside you at GNU Radio.

Avoid unnecessary jargon. When technical terminology is necessary, explain it immediately.

Avoid phrases that sound formulaic or artificial.

Do not overuse headings, bullet lists, bold text, or boxed statements. Use them when they genuinely improve readability.

A reader should feel that each question arises naturally from the previous observation.

---

# 15. Technical Accuracy

Beginner-friendly does not mean technically loose.

Be careful with statements about:

- real and complex signals,
- positive and negative frequency,
- FFT magnitude and power,
- sample rate and Nyquist limits,
- filtering,
- mixer products,
- modulation bandwidth,
- SNR,
- correlation,
- physical RF signals versus complex baseband representations.

If a simplified explanation is being used, make clear what is simplified when necessary.

Avoid teaching a convenient explanation that will need to be "unlearned" later.

---

# 16. Mathematical Formatting

The raw Markdown files must use consistent display-math formatting.

Use `$$` on separate lines, with the **complete equation on one physical line** between them.

Correct:

```text
$$
f_{\text{USB}} = f_c + f_m
$$
```

Also correct:

```text
$$
s(t) = \frac{1}{2}\cos[2\pi(f_c-f_m)t] + \frac{1}{2}\cos[2\pi(f_c+f_m)t]
$$
```

Do not write one equation across several physical Markdown lines such as:

```text
$$
s(t)
=
\frac{1}{2}\cos(...)
+
\frac{1}{2}\cos(...)
$$
```

Use inline math with single dollar signs when appropriate:

```markdown
The carrier frequency is $f_c$ and the message frequency is $f_m$.
```

Do not unnecessarily escape underscores, asterisks, equals signs, plus signs, or parentheses in normal Markdown or LaTeX.

Avoid LaTeX array environments for calculations that are clearer as Markdown tables.

---

# 17. Tables

Use standard Markdown pipe tables.

Example:

```markdown
| Frequency | Wavelength | Quarter wavelength |
|---:|---:|---:|
| 1 MHz | 300 m | 75 m |
| 100 MHz | 3 m | 0.75 m |
```

Do not use converted plain-text or Pandoc-style tables.

For row-by-row convolution or similar calculations, prefer a normal Markdown table rather than a LaTeX `array` environment.

---

# 18. Fenced Code Blocks and ASCII Diagrams

All line breaks inside code blocks, settings blocks, and ASCII diagrams must be preserved exactly.

Correct:

````markdown
```text
Message
   |
   v
Modulator
   |
   v
RF Signal
```
````

Never collapse the diagram into a single line.

GNU Radio settings should likewise remain multiline:

````markdown
```text
Sample Rate: samp_rate
Frequency:   10k
Amplitude:   1
```
````

Use appropriate language identifiers such as `text` or `python` when useful.

---

# 19. Figures

Use standard Markdown image syntax:

```markdown
![Descriptive caption](../figures/ch13/filename.png)
```

Do not escape the parentheses.

Organize figures by chapter:

```text
figures/
    ch01/
    ch02/
    ...
    ch13/
```

Use descriptive filenames that identify both the chapter and experiment where practical.

For example:

```text
../figures/ch13/ch13-exp1-am-envelope-flowgraph.png
../figures/ch13/ch13-exp1-am-envelope.png
```

Keep figure naming consistent within a chapter.

Use high-resolution source images and avoid unnecessary compression, because the same figures may later be used in PDF, EPUB, web, or print editions.

---

# 20. Figure Placement and Explanation

Place a figure close to the paragraph where the reader needs it.

Do not insert a screenshot without explaining what the reader should look at.

A useful sequence is:

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

When several traces appear in a GNU Radio sink, identify them clearly in the text and explain the important differences.

Do not describe every visual detail if it does not contribute to the lesson.

---

# 21. GNU Radio GUI Layout

When an experiment uses multiple QT GUI sinks, arrange them so the comparison is easy to understand.

Prefer layouts that tell a visual story, for example:

```text
┌──────────────────────┬──────────────────────┐
│ Transmitted Signals  │ Channel Selection    │
└──────────────────────┴──────────────────────┘
┌─────────────────────────────────────────────┐
│              Message Recovery               │
└─────────────────────────────────────────────┘
```

Include GUI Hint values when they are important for reproducing the intended layout.

Do not overcrowd one sink with too many traces when separate displays would be easier to interpret.

---

# 22. Experimental Settings Must Not Be Invented During Final Writing

The final-writing stage should document the experiments that were actually developed.

Do not silently change:

- sample rates,
- frequencies,
- amplitudes,
- filter cutoffs,
- transition widths,
- FFT sizes,
- GUI layouts,
- block types,
- experimental conclusions.

If a setting appears questionable during final writing, flag it for review rather than silently replacing it.

The final chapter should reflect the decisions and results established during chapter development.

---

# 23. What We Learned

End each chapter with a concise but meaningful **What We Learned** section.

This should not merely repeat every section heading.

Summarize the conceptual journey and the important conclusions the reader should carry forward.

Use bullets when they improve clarity.

Where useful, include the one or two equations or mental models that are most important to remember.

---

# 24. Connecting to the Next Chapter

Every chapter should end by creating a natural reason to continue.

The next chapter should feel like an answer to a question that the current chapter has just raised.

For example:

```text
We now understand why modulation is necessary.

But there are several ways to place information onto a carrier.

What happens if the amplitude of the carrier follows the message?

That leads us to amplitude modulation.
```

Do not make the transition sound like an administrative statement such as "Chapter 13 will discuss AM."

Use the unresolved technical question to create the bridge.

---

# 25. Raw Markdown Requirements

The final chapter must be written as **raw Markdown**.

Do not use:

- Pandoc,
- pypandoc,
- Markdown-to-Markdown conversion,
- document converters that rewrite the source.

Write the `.md` file directly as plain UTF-8 text.

Before finalizing a chapter, verify that the following remain valid raw Markdown:

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

The Markdown source should be readable both as source code and when rendered.

---

# 26. Publication-Friendly Markdown

GitHub is a useful place to store and preview the manuscript, but GitHub is not the final publishing engine.

Keep the source portable so that it can later be converted to:

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
- ordinary Markdown tables.

Avoid GitHub-specific formatting unless it is genuinely necessary.

Do not optimize the manuscript so heavily for GitHub that conversion to PDF or EPUB becomes difficult later.

---

# 27. Repository Organization

Keep the manuscript and figures organized consistently.

A typical structure is:

```text
sdr-with-gnu-radio/
|
+-- book/
|   +-- chapter01.md
|   +-- chapter02.md
|   +-- ...
|   +-- chapter13.md
|
+-- figures/
|   +-- ch01/
|   +-- ch02/
|   +-- ...
|   +-- ch13/
|
+-- BOOK_WRITING_GUIDE.md
```

GNU Radio `.grc` files should also follow a consistent experiment-based naming convention in the appropriate project location.

---

# 28. Final Chapter Writing Prompt

The following prompt can be reused when the experimental development of a chapter is complete.

---

## Standard Final-Writing Prompt

Please now write the complete chapter as a **raw Markdown `.md` file**, following the structure and formatting style established in Chapter 11.

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
- Use the Chapter 11 style for headings, equations, Toolbox sections, experiments, separators, and general Markdown formatting.
- Write the `.md` file **directly as plain UTF-8 text**. Do not pass it through Pandoc, pypandoc, or any other Markdown/document conversion process.
- Before providing the final file, verify that equations, fenced code blocks, ASCII diagrams, tables, image paths, headings, lists, and blockquotes remain valid raw Markdown.

The chapter should be clear, intuitive, naturally written, and suitable for a beginner. Follow the experimental development completed in this chat. Introduce mathematics only after the underlying idea has been explained intuitively.

Include the GNU Radio settings wherever necessary. Add a **GNU Radio Toolbox** section whenever a newly introduced GNU Radio block or tool needs explanation. Use the figures collected during the experiments and insert them at the appropriate points in the discussion.

Follow the established **Chapter 11/12 pedagogical structure**, but do not force every section into an identical mechanical template. The flow of the explanation is more important than rigidly repeating headings.

Include the important questions, doubts, clarifications, observations, and conceptual discussions that came up naturally while developing the chapter. Do not restrict the final chapter to the originally planned outline or experiments. If a discussion helped clarify something a beginner is likely to misunderstand, incorporate it at the most natural point in the chapter. Include useful interpretations of unexpected experimental results, distinctions between easily confused concepts, and connections to practical SDR or real radio systems. Do not include routine troubleshooting, temporary mistakes, abandoned experiments, or conversational back-and-forth unless they teach something genuinely useful.

Include a **Try It Yourself** section when a simple modification of an experiment gives the reader an additional useful insight. Keep these exercises short and exploratory. Whenever appropriate, ask the reader to predict what will happen before changing the GNU Radio flowgraph. Do not add a Try It Yourself section mechanically after every experiment.

Finish the chapter with a clear **What We Learned** section and a natural **Connecting to the Next Chapter** section.

**Do not change the technical conclusions, experimental results, GNU Radio settings, or decisions that were established while developing the chapter.**

Before writing the final chapter, review the **entire chapter-development conversation**, not just the final experiments and figures. Make sure that important insights discovered during discussion are not lost in the final Markdown.

Keep the Markdown publication-friendly. Avoid GitHub-specific formatting unless necessary. Use standard Markdown, LaTeX math, standard fenced code blocks, normal tables, and relative figure paths so the manuscript can later be converted to PDF, EPUB, HTML, and other publishing formats.

---

# 29. End-of-Book Editorial Pass

Do not interrupt development of later chapters merely to make every early chapter conform immediately to this guide.

After the first complete manuscript is finished, perform two dedicated editorial passes.

## Pass 1: Modernize the Early Chapters

Review Chapters 1–10 and bring them into the mature book style where appropriate.

Check:

- Main Questions,
- chapter transitions,
- experiment numbering,
- intuition-first explanations,
- GNU Radio settings,
- Toolbox sections,
- Try It Yourself sections,
- equation formatting,
- tables,
- figures,
- What We Learned sections,
- connections to the next chapter.

Preserve the technical progression and useful personality of each chapter. Do not make every chapter artificially identical.

## Pass 2: Whole-Book Consistency Review

Read the complete manuscript as one continuous book.

Check for:

- concepts used before they are introduced,
- repeated explanations,
- inconsistent terminology,
- inconsistent notation,
- inconsistent sample-rate conventions,
- GNU Radio blocks introduced as "new" more than once,
- missing cross-references,
- inconsistent experiment numbering,
- inconsistent figure naming,
- uneven chapter difficulty,
- abrupt chapter transitions,
- formatting inconsistencies,
- publication issues affecting PDF or EPUB conversion.

The final goal is not merely a collection of good chapters.

It is one coherent book.
