# GNU Radio Feature Map

## Why This Document Exists

The purpose of this document is to make sure that GNU Radio is taught as carefully as the SDR concepts themselves.

The book should not use GNU Radio only as a place to reproduce experiments.

By the end of the book, the reader should be comfortable enough with GNU Radio to open a blank flowgraph, choose appropriate blocks, connect them correctly, select sensible parameters, understand what the signal is doing, and troubleshoot problems when the result is not what they expected.

This feature map tracks:

- what GNU Radio features we want to teach
- where each feature is introduced
- where it is practised again
- how deeply it should be explained
- which mistakes the reader should intentionally explore

The feature map may change while the book is being written.

If a feature feels forced into a chapter, it should be moved to a chapter where it naturally helps solve a problem.

---

# 1. How We Will Introduce GNU Radio Features

GNU Radio features will normally move through four stages.

## Stage 1: First Encounter

The reader sees the block or feature for the first time.

We explain only what is necessary to use it correctly.

## Stage 2: GNU Radio Toolbox

The reader gets a more focused explanation:

- what the feature does
- why we need it
- important parameters
- input and output types
- common misunderstandings
- where it will appear again

## Stage 3: Reuse

The feature appears in later experiments without being explained from the beginning again.

The reader gradually becomes comfortable with it.

## Stage 4: Independent Use

Eventually the reader should be able to decide for themselves when the feature is required.

The goal is not memorization.

The goal is recognition:

> "I know what needs to happen to the signal, so I know what kind of GNU Radio block I need."

---

# 2. GNU Radio Companion Fundamentals

These ideas should be introduced very early.

| Feature | First Introduced | Practised Again | Expected Level by End |
|---|---|---|---|
| GNU Radio Companion interface | Chapter 1 | Throughout | Independent |
| Flowgraph | Chapter 1 | Throughout | Independent |
| Block library | Chapter 1 | Throughout | Independent |
| Search for blocks | Chapter 1 | Throughout | Independent |
| Adding blocks | Chapter 1 | Throughout | Independent |
| Connecting blocks | Chapter 1 | Throughout | Independent |
| Deleting connections | Chapter 1 | Throughout | Independent |
| Block properties | Chapter 1 | Throughout | Independent |
| Run flowgraph | Chapter 1 | Throughout | Independent |
| Stop flowgraph | Chapter 1 | Throughout | Independent |
| Generate flowgraph | Chapter 1 | Later chapters | Comfortable |
| Source blocks | Chapter 1 | Throughout | Independent |
| Sink blocks | Chapter 1 | Throughout | Independent |
| Processing blocks | Chapter 2 | Throughout | Independent |
| Flowgraph errors | Chapter 1 | Throughout | Independent |
| Warning messages | Chapter 1 | Throughout | Comfortable |

## Main Idea

A GNU Radio flowgraph should be understood as a signal-processing system.

The reader should learn to follow the signal from left to right and ask:

> What type of data is here?

> What operation is this block performing?

> What changes after the block?

---

# 3. Variables and Runtime Control

Variables become important almost immediately because real flowgraphs should not contain the same numerical value manually repeated everywhere.

| Feature | First Introduced | Practised Again | Expected Level |
|---|---|---|---|
| Variable | Chapter 2 | Throughout | Independent |
| Variable ID | Chapter 2 | Throughout | Independent |
| Expressions using variables | Chapter 2 | Throughout | Independent |
| QT GUI Range | Chapter 3 | Many later chapters | Independent |
| Runtime parameter changes | Chapter 3 | Noise, mixing, filters, hardware | Independent |
| QT GUI Chooser | Later | Modulation / hardware | Comfortable |
| QT GUI Entry | Later | Advanced experiments | Familiar |
| QT GUI Push Button | Later | Advanced flowgraphs | Familiar |
| QT GUI Toggle Button | Later | Advanced flowgraphs | Familiar |
| QT GUI Check Box | Later | Advanced flowgraphs | Familiar |

GNU Radio's QT GUI Range behaves like a variable whose value can be changed while the flowgraph is running. This makes it particularly useful for experiments where we want the reader to change frequency, sample rate, gain, or another parameter and immediately observe the effect. :contentReference[oaicite:1]{index=1}

## Important Distinction

The reader should understand the difference between:

**Variable**

A value used by the flowgraph.

and

**QT GUI Range**

A variable that also gives the user an interactive GUI control.

---

# 4. Sample Rate and Flowgraph Timing

This should be treated as a major GNU Radio concept, not simply a parameter that appears in blocks.

| Feature | First Introduced | Reused |
|---|---|---|
| Sample-rate variable | Chapter 2 | Everywhere |
| Throttle | Chapter 1 | Simulation chapters |
| Relationship between sample rates | Chapter 3 | Everywhere |
| Different input/output sample rates | Chapter 10 onward | Filters, resampling |
| Interpolation | Chapter 15/18 | Receiver chapters |
| Decimation | Chapter 10/15 | Receiver chapters |
| Rational resampling | Chapter 15 | Real receiver |

## GNU Radio Toolbox: Throttle

We should make it clear early that Throttle does not perform sampling.

The data in GNU Radio is already represented as samples.

Throttle controls how quickly samples are processed when there is no real-time hardware source or sink controlling the rate.

## Now Break the Flowgraph

Remove Throttle from a software-only flowgraph.

Ask:

- Does the signal frequency change?
- Does CPU usage change?
- Does the flowgraph process samples faster?
- What exactly was Throttle controlling?

---

# 5. GNU Radio Data Types

Data types are important enough to receive serious treatment in Chapter 4.

| Data Type / Concept | First Introduced | Later Use |
|---|---|---|
| Float | Chapter 1/2 | Throughout |
| Complex | Chapter 4 | Almost all SDR chapters |
| Byte | Chapter 16 | Digital communication |
| Short | Later | File/hardware examples |
| Integer | Later | Digital processing |
| Port colours | Chapter 4 | Throughout |
| Type compatibility | Chapter 4 | Throughout |
| Item size | Chapter 20 | Streams/vectors |
| Type conversion | Chapter 4 | Many chapters |

## Important Type Conversion Blocks

Introduce when useful:

- Float to Complex
- Complex to Real
- Complex to Imag
- Complex to Mag
- Complex to Mag^2
- Complex to Arg
- Char to Float
- Float to Char
- Short to Float
- Float to Int
- Int to Float

Not every converter needs a full Toolbox section.

The important goal is that the reader understands **why conversion is necessary**.

## Now Break the Flowgraph

Try connecting incompatible types.

Let GNU Radio show the error.

Then explain why the connection is invalid.

---

# 6. Signal Sources

The reader should gradually become familiar with different ways of creating data.

| Source | First Useful Chapter | Purpose |
|---|---|---|
| Signal Source | Chapter 1 | Generate deterministic waveforms |
| Noise Source | Chapter 8 | Noise experiments |
| Constant Source | Early chapters | Fixed values |
| Vector Source | Chapter 11 | Known sequences |
| Random Source | Chapter 16 | Digital data |
| File Source | Chapter 21 | Recorded signals |
| Hardware Source | Chapter 22 | Real RF |
| Network Source | Chapter 21 | External data |

## Signal Source

This should become one of the most familiar blocks in the first half of the book.

Use it to generate:

- cosine
- sine
- complex exponential
- constant/DC
- possibly square or triangle waves where useful

Do not simply show its settings.

Explain:

- sample rate
- waveform
- frequency
- amplitude
- offset
- phase where applicable

---

# 7. Mathematical Processing Blocks

Simple mathematical blocks are useful because they expose the signal-processing operation clearly.

| Block / Operation | First Introduced | Main Application |
|---|---|---|
| Add | Chapter 2 | Multiple tones, noise |
| Subtract | Later | Signal comparison |
| Multiply | Chapter 9 | Mixing, modulation |
| Divide | As required | Normalization |
| Add Const | Early | DC offset |
| Multiply Const | Chapter 8 | Gain/scaling |
| Conjugate | Chapter 12 | Correlation |
| Complex Conjugate | Chapter 12 | Correlation/mixing |
| Abs / Magnitude | Chapter 4/5 | Signal magnitude |
| Mag Squared | Chapter 8/12 | Power/detection |

The important principle is to connect the GNU Radio operation to the mathematics.

For example, when two signals enter Multiply, the reader should understand what multiplication means for the spectrum.

---

# 8. QT GUI Visualization Tools

The GUI sinks are some of the most important teaching tools in the entire book.

The reader should learn that different visualizations answer different questions.

## QT GUI Time Sink

First introduced: Chapter 1

Used throughout.

Questions it helps answer:

- What does the waveform look like?
- What is its amplitude?
- What is its period?
- Does the waveform change with time?
- Are two signals phase shifted?

Important settings:

- sample rate
- number of points
- update rate
- trigger
- autoscale
- axis limits
- number of inputs

---

## QT GUI Frequency Sink

First introduced lightly: Chapter 3

Explained properly: Chapter 6

Questions:

- Which frequencies are present?
- Where is the signal centred?
- What is the noise floor?
- What is the effect of filtering?
- Are spectral images present?

Important settings:

- centre frequency
- bandwidth
- FFT size
- window
- averaging
- dB scale

---

## QT GUI Waterfall Sink

First introduced: Chapter 6 or 8

Used heavily with real SDR hardware.

Purpose:

Show how the spectrum changes with time.

This is especially useful for:

- intermittent signals
- frequency hopping
- changing signals
- real RF environments

---

## QT GUI Constellation Sink

First introduced: Chapter 5

Explained deeply: Chapter 17

Used for:

- IQ visualization
- BPSK
- QPSK
- QAM
- noise
- phase offset
- frequency offset
- synchronization problems

---

## QT GUI Number Sink

First introduced when useful: Chapter 8

Used for:

- signal power
- magnitude
- measured values
- SNR-related experiments

---

## QT GUI Histogram Sink

Introduce later if it supports the noise/statistics discussion.

Possible use:

- Gaussian noise distribution
- sample distribution

---

## QT GUI Eye Sink

Introduce when discussing pulse shaping and timing if available and suitable for the GNU Radio version used by the book.

Otherwise, construct the visualization another way.

---

# 9. Multiple Sinks and Multiple Views

An important skill is learning to observe the same signal in several ways.

For example:

```text
                     → QT GUI Time Sink
Signal Source →
                     → QT GUI Frequency Sink