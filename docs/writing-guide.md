# SDR with GNU Radio: Writing Guide

## Why This Guide Exists

This book is not intended to be a conventional textbook on Software Defined Radio or digital signal processing.

There are already many excellent books that explain these subjects mathematically. Our aim is slightly different.

We want a reader who is completely new to SDR to be able to ask:

> What is actually happening to the signal?

and, after working through the chapter, be able to answer that question in their own words.

Mathematics is important and will be used throughout the book, but equations should support understanding rather than replace it.

GNU Radio will act as our laboratory. Whenever possible, the reader should be able to see, change, test, and even deliberately break the ideas discussed in the chapter.

---

# 1. Who Are We Writing For?

Assume the reader:

- is new to Software Defined Radio
- has basic engineering or science knowledge
- may have seen signals and systems before but does not necessarily understand them intuitively
- may know basic mathematics
- may never have used GNU Radio
- is curious about how radio signals actually work

Do not assume that the reader already understands terms simply because they are common in communication engineering.

For example, do not write:

> The received RF signal is downconverted to complex baseband using quadrature mixing.

without first making sure the reader understands:

- RF
- mixing
- downconversion
- baseband
- complex signals
- quadrature

Every new technical term should earn its place.

---

# 2. The Main Writing Principle

Whenever possible, explain concepts in this order:

**Question → Example → Intuition → Visual Explanation → GNU Radio Experiment → Observation → Mathematics → Deeper Understanding**

The exact order may change slightly depending on the topic, but intuition should normally come before formal mathematics.

The reader should ideally reach an equation and think:

> "That equation describes what I already understand."

rather than:

> "I can follow the equation, but I don't know what it means."

---

# 3. Start With a Question

Whenever possible, begin a new concept with a question.

Instead of:

> Sampling is the process of converting a continuous-time signal into a discrete-time signal.

consider:

> A computer cannot continuously watch an analog voltage. It can only record values at particular moments. So how often does it need to look at a signal before it can understand what that signal is doing?

The second version gives the reader a reason to care about sampling before defining it.

Good questions include:

> What exactly is a signal?

> How does a computer see a sine wave?

> Why do SDR receivers need I and Q?

> What does a negative frequency actually mean?

> How can several frequencies exist inside one waveform?

> How does a radio move a signal from one frequency to another?

> How can a receiver find a weak signal buried in noise?

Questions should arise naturally from the problem being discussed.

---

# 4. Build Intuition Before Formalism

Before introducing a mathematical definition, try to create a mental picture.

For example, before introducing sampling mathematically, imagine a 1 kHz sine wave.

It completes 1,000 cycles every second.

Now suppose we measure that waveform 10,000 times every second.

We obtain roughly 10 samples during each cycle.

The reader can already begin thinking about what those samples might look like.

Now reduce the number of measurements.

What happens with five samples per cycle?

Three?

Two?

One?

At this point, the sampling theorem has a purpose.

Only then introduce the mathematical relationship.

$$
T_s = \frac{1}{f_s}
$$

and later:

$$
f_s > 2f_{\max}
$$

The mathematics now describes something the reader has already started to understand.

---

# 5. Use Mathematics Carefully

This is not a mathematics-free book.

Equations are necessary for understanding SDR properly.

However, mathematics should be introduced because it helps explain something, not simply because the equation traditionally appears in a textbook chapter.

## Before an Equation

Explain:

- what problem we are trying to solve
- what quantities matter
- what relationship we expect

## After an Equation

Explain every important term.

For example:

$$
x(t)=A\cos(2\pi ft+\phi)
$$

Do not leave the equation alone.

Explain that:

- $A$ controls the amplitude
- $f$ controls how quickly the signal oscillates
- $\phi$ determines where in its cycle the signal begins
- $t$ represents time

Then change these quantities in an example and show what happens.

## Equation Formatting

All displayed equations in the Markdown source should use:

```text
$$
equation
$$
```

For example:

```text
$$
f_s > 2f_{\max}
$$
```

Avoid using `\[ ... \]` for displayed equations.

---

# 6. Use Numbers, Not Only Symbols

Whenever possible, follow a symbolic relationship with a numerical example.

For example:

Suppose our signal frequency is 1 kHz and our sample rate is 10 kHz.

Then:

$$
N = \frac{f_s}{f}
$$

so:

$$
N = \frac{10000}{1000}=10
$$

We therefore obtain 10 samples during each cycle of the sine wave.

Now the reader can connect the equation to something concrete.

Whenever useful, carry the same numerical example into GNU Radio.

---

# 7. Use Visual Explanations

If a concept is easier to understand with a figure, create the figure.

Do not force the reader to construct a complicated mental picture from a paragraph.

Useful figures may include:

- sine waves
- sampling points
- complex-plane diagrams
- rotating vectors
- spectra
- FFT bins
- filter responses
- convolution steps
- correlation peaks
- modulation waveforms
- constellations
- receiver chains
- before-and-after comparisons

Figures should teach something.

Avoid decorative figures that add visual appeal but no understanding.

Whenever possible, label the important quantities directly on the figure.

---

# 8. GNU Radio Is the Laboratory

GNU Radio should not appear as an unrelated exercise added at the end of a theoretical chapter.

It should allow the reader to test what the chapter has just explained.

The progression should be:

**We discussed it → we predicted it → now let's see whether it actually happens.**

A GNU Radio experiment should answer a specific question.

For example:

> What happens if the sample rate becomes too low?

is better than:

> Build the following GNU Radio flowgraph.

The reader should know why they are building the flowgraph.

---

# 9. Introduce GNU Radio Gradually

Do not introduce ten unfamiliar GNU Radio blocks at once unless there is a very good reason.

Each chapter should introduce a manageable number of new blocks or GNU Radio concepts.

Previously introduced blocks should be reused.

This creates progression.

For example:

Chapter 1 may introduce:

- Signal Source
- Throttle
- QT GUI Time Sink

Later chapters can reuse those blocks while adding:

- QT GUI Range
- Frequency Sink
- Noise Source
- filters
- constellation tools

By the time the reader reaches a complete receiver, most of the blocks should already be familiar.

---

# 10. GNU Radio Toolbox

Whenever an important GNU Radio block or feature appears for the first time, include a **GNU Radio Toolbox** section.

The purpose is to explain the tool itself rather than only telling the reader which values to enter.

Use a structure similar to:

## GNU Radio Toolbox: Throttle

### What does it do?

The Throttle block limits how quickly samples move through a software-only flowgraph.

### Why do we need it here?

Our flowgraph does not contain real hardware that naturally determines the sample rate. Without a Throttle block, GNU Radio may process samples as quickly as the computer allows.

### Important settings

| Setting | Meaning |
|---|---|
| Sample Rate | Intended processing rate |
| Sample Type | Type of samples passing through the block |

### Watch Out

The Throttle block does **not** sample an analog signal.

The signal inside GNU Radio is already represented by samples.

Throttle controls the rate at which those samples are processed in a software-only flowgraph.

### Where will we use it again?

We will reuse Throttle throughout many of the simulation-based chapters.

---

GNU Radio Toolbox entries may describe more than blocks.

They can also explain:

- Variables
- QT GUI controls
- GNU Radio data types
- streams
- vectors
- tags
- messages
- PDUs
- hierarchical blocks
- Embedded Python Blocks
- hardware parameters

Do not repeat the complete Toolbox explanation every time the same feature appears. Briefly refer back to the earlier explanation when necessary.

---

# 11. Explain Every Flowgraph

Never show a GNU Radio flowgraph without explaining the signal path.

For a simple flowgraph such as:

```text
Signal Source → Throttle → QT GUI Time Sink
```

explain what happens from left to right.

For example:

1. Signal Source creates the samples.
2. Throttle controls how quickly those samples are processed.
3. QT GUI Time Sink displays the samples against time.

For larger flowgraphs, divide the system into functional sections.

The reader should eventually learn to look at a flowgraph and mentally follow the signal through it.

---

# 12. Give Exact GNU Radio Settings

Experiments should be reproducible.

When appropriate, provide a table such as:

| Block | Parameter | Value |
|---|---|---:|
| Signal Source | Sample Rate | `samp_rate` |
| Signal Source | Frequency | `1000` |
| Signal Source | Amplitude | `1` |
| Throttle | Sample Rate | `samp_rate` |
| QT GUI Time Sink | Sample Rate | `samp_rate` |

Do not simply say:

> Configure the Signal Source appropriately.

A beginner may not know what "appropriately" means.

---

# 13. Predict Before You Run

Whenever the experiment allows it, ask the reader to predict the result before pressing Run.

For example:

> We are generating a 1 kHz real cosine. Before running the flowgraph, where do you expect peaks to appear in the spectrum?

Or:

> We currently have 10 samples per cycle. What do you think the waveform will look like if we reduce this to only three samples per cycle?

Prediction turns the reader from an observer into a participant.

After running the experiment, compare the result with the prediction.

---

# 14. What Did We Observe?

Do not assume that a screenshot explains itself.

After every important experiment, discuss what is visible.

For example:

> Notice that the waveform still looks smooth when we have many samples per cycle. As the sample rate falls, the individual sample positions become increasingly important. Eventually the displayed waveform no longer resembles the analog sine wave we had in mind.

When both time-domain and frequency-domain views are useful, discuss them separately.

Ask:

- What changed?
- What stayed the same?
- Why?
- Was this what we predicted?

---

# 15. Now Break the Flowgraph

After a flowgraph works correctly, deliberately make it behave incorrectly.

This is a standard part of the book.

The purpose is not simply to generate errors.

The purpose is to understand **why the correct configuration works**.

For example:

## Now Break the Flowgraph

Our sampling experiment is working correctly.

Now keep the signal frequency at 1 kHz and reduce the sample rate.

Try:

```text
10000
5000
2500
2000
1500
1000
500
```

Do not immediately explain what will happen.

Ask the reader to observe the Time Sink and Frequency Sink.

Then discuss:

- when the waveform begins looking unusual
- when aliasing occurs
- why the displayed frequency changes
- why some sample rates may produce surprisingly simple-looking patterns

Finally, restore the correct configuration.

Other chapters may deliberately:

- remove Throttle
- connect incompatible data types
- reverse I and Q
- mistune a local oscillator
- use an incorrect filter cutoff
- increase noise
- overmodulate an AM signal
- introduce frequency offset
- disable synchronization
- use excessive RF gain

Breaking the flowgraph should always teach a specific concept.

---

# 16. Distinguish Two Kinds of Failure

The book should teach the reader that "it doesn't work" can mean very different things.

## GNU Radio Failure

Examples:

- incompatible port types
- invalid block parameter
- missing dependency
- Python error
- hardware not detected

GNU Radio may refuse to run.

## Signal-Processing Failure

The flowgraph runs perfectly, but the result is wrong.

Examples:

- aliasing
- wrong filter cutoff
- incorrect LO frequency
- poor SNR
- wrong samples per symbol
- missing synchronization

The second category is especially important.

A flowgraph that runs without an error is not necessarily a correct flowgraph.

---

# 17. Watch Out

Use short **Watch Out** sections for common misconceptions.

Example:

## Watch Out: Negative Frequency

Negative frequency does not mean that the radio wave is physically travelling backward.

It describes the direction of rotation of a complex signal relative to our chosen frequency reference.

Another example:

## Watch Out: Throttle

Throttle does not create the sample rate of an analog signal.

It controls processing speed in a software-only GNU Radio flowgraph.

These sections should be short and appear only where a misconception is genuinely likely.

---

# 18. Common GNU Radio Mistakes

When appropriate, include mistakes that a beginner is likely to make.

Examples:

- forgetting Throttle in a simulation
- using different sample-rate variables in connected blocks
- confusing centre frequency with sample rate
- connecting Float and Complex ports incorrectly
- misunderstanding interpolation and decimation
- using an unrealistic filter transition width
- confusing RF gain with signal amplitude
- forgetting to change a parameter in multiple blocks

Explain how to recognize the problem and how to correct it.

---

# 19. Try It Yourself

End practical sections with a few small challenges.

They should encourage experimentation rather than test memorization.

For example:

> Change the signal from 1 kHz to 2 kHz. Without changing the sample rate, how many samples do you now have per cycle?

> Find the lowest sample rate at which the waveform still looks reasonably sinusoidal to you.

> Can you create two different analog frequencies that produce the same sampled frequency?

Whenever possible, the reader should be able to answer by changing the GNU Radio flowgraph.

---

# 20. Keep the Language Natural

Write as if an experienced engineer is sitting beside a student and explaining the idea.

Prefer:

> Let's keep the signal at 1 kHz and change only the sample rate. That way, if something strange happens, we know what caused it.

over:

> The sampling frequency shall now be varied while maintaining a constant input signal frequency in order to analyze the resulting effects.

Use technical terminology when it is useful, but do not use complicated language merely to sound technical.

---

# 21. Do Not Overuse Lists

The main explanation should normally be written as connected prose.

Lists are useful for:

- parameters
- steps
- comparisons
- summaries
- settings

They should not replace explanation.

Avoid turning an entire chapter into bullet points.

---

# 22. Do Not Repeat Yourself Mechanically

Important ideas should be reinforced, but not by repeating the same definition every few pages.

If the reader has already learned what sample rate means, later chapters should use that knowledge naturally.

If a previous concept becomes important again, briefly reconnect it:

> Remember what happened in Chapter 3 when we sampled too slowly? The same limitation matters here because...

This helps the book feel connected.

---

# 23. Connect the Chapters

The chapters should not feel like independent tutorials.

At the beginning of a chapter, explain why the previous ideas have led us here.

For example:

> We now know how GNU Radio represents a signal using samples. But so far we have mostly treated those samples as ordinary real numbers. Real SDR receivers usually give us something slightly different: complex I/Q samples. To understand why, we first need a comfortable way of thinking about complex numbers.

At the end, create a natural reason to continue.

---

# 24. Reuse Examples When Helpful

A familiar signal can follow the reader through several chapters.

For example, a 1 kHz sinusoid may first appear when discussing signals.

The same signal can later be:

- sampled
- viewed in the FFT
- represented as I/Q
- mixed
- filtered
- buried in noise
- detected

This reduces unnecessary cognitive load and shows how the concepts connect.

---

# 25. Keep Theory and GNU Radio Connected

Whenever a GNU Radio parameter appears, connect it to the underlying concept.

Do not merely say:

> Set Sample Rate to 32 kHz.

Explain why 32 kHz is appropriate.

Do not merely say:

> Set the Low Pass Filter cutoff to 5 kHz.

Explain what part of the spectrum we are trying to keep.

Do not merely say:

> Set decimation to 4.

Explain what happens to the sample rate after decimation.

The reader should learn to choose values rather than copy them.

---

# 26. Screenshots Should Have a Purpose

Do not fill the book with screenshots of every dialog box.

Use screenshots when they help the reader:

- find an unfamiliar setting
- understand a flowgraph
- compare results
- identify an error
- interpret a plot

Whenever possible, crop screenshots to the relevant area.

Important settings may be highlighted or annotated when that improves understanding.

---

# 27. Keep Experiments Reproducible

Every important GNU Radio experiment should eventually have a corresponding `.grc` file in the repository.

Use a predictable naming scheme.

For example:

```text
experiments/
└── chapter-03/
    ├── 01-basic-sampling.grc
    ├── 02-sample-rate-control.grc
    └── 03-aliasing.grc
```

The book and repository should agree on parameter names and values.

---

# 28. Prefer Understanding Over Coverage

The goal is not to mention every GNU Radio block simply so that it can appear in the book.

Important GNU Radio features should be introduced when they naturally help solve a problem.

A block is worth teaching when the reader can understand:

- what it does
- why it is needed
- what goes into it
- what comes out
- which parameters matter
- what happens when it is configured incorrectly

The GNU Radio Feature Map will be used to track coverage across the book.

---

# 29. Standard Chapter Structure

Not every chapter must follow this structure rigidly, but this is the default.

```text
Chapter Title

Opening Question

Build the Intuition

A Simple Example

What's Actually Happening?

Visual Explanation

Essential Mathematics

Why This Matters in SDR

GNU Radio Toolbox

Build It in GNU Radio

Flowgraph Explanation

Block Settings

Predict Before You Run

Run the Experiment

What Did We Observe?

Watch Out

Now Break the Flowgraph

Why Did It Break?

Fix the Flowgraph

Common GNU Radio Mistakes

Try It Yourself

What We Learned

Where We Go Next
```

Sections that do not help a particular chapter may be omitted.

The structure exists to support the explanation, not constrain it.

---

# 30. End Each Chapter With Two Kinds of Progress

The chapter summary should distinguish between conceptual understanding and practical GNU Radio skills.

For example:

## What We Learned

### SDR Concepts

By this point, you should understand:

- what sampling means
- why sample rate matters
- what the Nyquist limit represents
- why aliasing occurs

### GNU Radio Skills

You should now be comfortable with:

- using Variables
- controlling parameters with QT GUI Range
- configuring Time and Frequency Sinks
- changing parameters while a flowgraph runs
- recognizing a sampling-related problem

This lets the reader see that they are learning both SDR and GNU Radio.

---

# 31. The Final Test for Every Explanation

Before considering a section finished, ask:

**Could a beginner explain this idea back to us without simply repeating the equation?**

Then ask:

**Could they demonstrate the idea in GNU Radio?**

And finally:

**Could they predict what would happen if we changed one important parameter?**

If the answer to all three is yes, the section has probably done its job.

---

# The Principle We Should Never Lose

The reader should not finish this book thinking:

> "I know which GNU Radio blocks to connect."

The reader should finish thinking:

> "I understand what needs to happen to the signal, and I know how to make GNU Radio do it."

That is the difference between following a flowgraph and understanding Software Defined Radio.