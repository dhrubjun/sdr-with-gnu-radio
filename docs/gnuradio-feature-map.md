# GNU Radio Feature Map

**Version 0.2**

---

# Why This Document Exists

The SDR concepts and GNU Radio skills in this book should develop together.

GNU Radio is not being used simply to produce screenshots at the end of each chapter. It is our practical laboratory.

By the end of the book, the reader should be able to open a blank flowgraph and ask:

> What needs to happen to this signal?

Then they should be able to choose suitable GNU Radio blocks, set meaningful parameters, inspect intermediate signals, and diagnose problems when the result is wrong.

This document helps us keep track of that progression.

For every important GNU Radio feature, we want to know:

- where it first appears
- why it appears there
- how deeply it is explained
- where it is used again
- what mistake or failure we can demonstrate with it
- what level of independence we expect from the reader later

This is a working document.

It can change as we build and test the actual GNU Radio experiments.

---

# 1. GNU Radio Version Strategy

The first edition of the book should use one consistent GNU Radio environment.

The main flowgraphs, screenshots, block names and parameter tables should be based on the GNU Radio 3.10-style GNU Radio Companion environment.

Do not mix different GNU Radio generations inside the main experiments.

If a block name or workflow changes significantly in a later GNU Radio release, mention that separately rather than disrupting the main explanation.

Before publishing the book, all experiments should be tested again using the exact GNU Radio version stated in the book.

---

# 2. How a GNU Radio Feature Should Be Learned

Important GNU Radio features should normally pass through four stages.

## Stage 1: First Encounter

The reader meets the block or feature because it solves a problem in the current chapter.

Only the information needed to use it is introduced.

## Stage 2: GNU Radio Toolbox

The feature receives a focused explanation.

The Toolbox should answer questions such as:

- What does it do?
- Why do we need it?
- What enters it?
- What comes out?
- What data type does it use?
- Which parameters matter?
- What units are those parameters in?
- Which parameters can change while the flowgraph is running?
- What is a common beginner mistake?

## Stage 3: Reuse

The feature appears again without being fully reintroduced.

The reader gradually becomes comfortable using it.

## Stage 4: Independent Use

Eventually the book stops telling the reader:

> Add this block.

Instead, the reader should recognize:

> I need this operation, so this is the kind of block I should use.

---

# 3. GNU Radio Companion Fundamentals

## First Introduced

Chapter 1

## Features

- GNU Radio Companion interface
- block library
- block search
- adding a block
- moving blocks
- deleting blocks
- connecting blocks
- disconnecting blocks
- source blocks
- processing blocks
- sink blocks
- block properties
- block IDs
- parameter fields
- Run
- Stop
- Generate
- saving a `.grc` file
- reading simple GRC errors
- reading warnings
- understanding signal flow from left to right

## Reused

Every chapter.

## Goal

By the middle of the book, navigating GNU Radio Companion should feel routine rather than like a separate skill.

## Now Break the Flowgraph

- disconnect a required block
- leave a required parameter invalid
- create an incompatible connection
- observe the error indicator before running

---

# 4. Flowgraph Organization

## First Introduced

Chapter 1 lightly.

Developed progressively throughout the book.

## Features

- left-to-right signal flow
- sensible placement of sources and sinks
- grouping related processing blocks
- comments
- meaningful variable names
- meaningful block IDs where useful
- avoiding unnecessary crossing connections
- dividing large flowgraphs into functional areas

Later examples may use comments such as:

```text
SIGNAL GENERATION

CHANNEL

RECEIVER

SYNCHRONIZATION

VISUALIZATION
```

## Goal

The reader should learn that a flowgraph is also a technical diagram.

A good flowgraph should help explain how the system works.

---

# 5. Variables and Expressions

## First Introduced

Chapter 2

## Features

- Variable block
- variable ID
- variable value
- referring to a variable from another block
- simple expressions
- dependent variables

Example:

```text
samp_rate = 32000
signal_freq = 1000
```

Later:

```text
symbol_rate = samp_rate / sps
```

## Reused

Almost every chapter.

## Goal

The reader should stop repeating important numerical parameters manually in several blocks.

---

# 6. Runtime Controls

## First Introduced

Chapter 3

## Main Feature

QT GUI Range

## Later Controls

Introduce only when there is a useful reason:

- QT GUI Range
- QT GUI Chooser
- QT GUI Entry
- QT GUI Push Button
- QT GUI Toggle Button
- QT GUI Check Box

## Typical Uses

Use runtime controls for:

- signal frequency
- amplitude
- sample rate in suitable simulations
- noise amplitude
- LO frequency
- filter cutoff
- carrier offset
- timing offset
- loop bandwidth
- hardware centre frequency
- RF gain

## Main Lesson

A normal Variable gives the flowgraph a value.

A QT GUI control allows the user to change a value interactively.

---

# 7. Sample Rate

## First Introduced

Chapter 1 lightly.

Explained properly in Chapter 3.

## Features

- sample-rate variable
- sample-rate consistency
- samples per second
- sample rate at source
- sample rate at sink
- sample-rate changes inside a flowgraph
- rate relationships between blocks

## Reused

Throughout the entire book.

## Goal

The reader should eventually trace sample rate through a large receiver without guessing.

---

# 8. Throttle

## First Introduced

Chapter 1

## Explained Properly

Chapter 3

## Toolbox Questions

Explain:

- what Throttle does
- why software-only flowgraphs often need it
- why it does not perform analog sampling
- why hardware-based flowgraphs normally should not rely on it to establish the hardware rate

## Now Break the Flowgraph

Remove Throttle from a software-generated flowgraph and investigate:

- CPU activity
- GUI behaviour
- processing speed
- whether the mathematical samples themselves changed

---

# 9. GNU Radio Data Types

## First Introduced

Port colours are noticed in Chapter 1.

Formal treatment begins in Chapter 4.

## Important Types

- Float
- Complex
- Byte
- Short
- Integer

## Concepts

- scalar item
- item type
- port colour
- compatible and incompatible ports
- type conversion
- item size later in the book

## Goal

The reader should understand that the colour of a GNU Radio connection is meaningful.

---

# 10. Type Conversion Blocks

## First Major Use

Chapter 4

## Important Blocks

- Float to Complex
- Complex to Real
- Complex to Imag
- Complex to Mag
- Complex to Mag^2
- Complex to Arg
- Char to Float
- Float to Char where appropriate
- Int to Float
- Short to Float where useful

Not every conversion block needs its own Toolbox entry.

The reader needs to understand the general idea:

> The representation of the data is changing, not necessarily the underlying physical information.

## Now Break the Flowgraph

Attempt to connect incompatible port types.

---

# 11. Signal Source

## First Introduced

Chapter 1

## Used Extensively

Chapters 1 to 15 and many later experiments.

## Parameters to Teach Gradually

- output type
- waveform
- sample rate
- frequency
- amplitude
- offset
- phase where applicable

## Uses

Generate:

- cosine
- sine
- complex tone
- constant/DC signal
- other simple deterministic waveforms where useful

## Important Language

Do not create the impression that there is a separate conceptual block called "Complex Signal Source."

Instead say:

> Signal Source configured for Complex output.

---

# 12. Other Signal and Data Sources

Introduce only when the reader has a reason to use them.

| Source | First Major Use | Purpose |
|---|---|---|
| Signal Source | Ch. 1 | Deterministic waveforms |
| Constant Source | Early chapters if useful | Fixed signal/value |
| Noise Source | Ch. 8 | Controlled noise |
| Vector Source | Ch. 11 | Finite known sequences |
| Random Source | Ch. 16 | Digital data |
| File Source | Ch. 30 | Recorded data/IQ |
| WAV File Source | Analog/audio chapters if useful | Audio |
| SDR hardware source | Ch. 31 | Real RF |
| Network source | Ch. 30 | External applications |

---

# 13. QT GUI Time Sink

## First Introduced

Chapter 1

## Reused

Throughout the book.

## Questions It Helps Answer

- What does the waveform look like?
- What is its amplitude?
- What is its period?
- Is there a phase difference?
- Is the waveform distorted?
- Is timing changing?

## Features to Introduce Gradually

- sample rate
- number of points
- number of inputs
- autoscale
- axis limits
- triggering
- update rate

Do not teach every setting in Chapter 1.

---

# 14. QT GUI Frequency Sink

## First Encounter

Chapter 3

## Full Treatment

Chapter 6

## Questions It Helps Answer

- Which frequencies are present?
- Where are they?
- How wide is the signal?
- What happened after mixing?
- What happened after filtering?
- Where is the noise floor?
- Is the spectrum symmetric?
- Is there leakage?

## Features

- centre frequency
- bandwidth
- FFT size
- window
- averaging
- dB scale
- update rate

## Reused

Almost every RF/DSP chapter.

---

# 15. QT GUI Waterfall Sink

## First Introduced

Chapter 6

## Reused Heavily

Chapter 31 onward with real RF.

## Purpose

Show how the spectrum changes with time.

Particularly useful for:

- intermittent signals
- changing frequencies
- real RF environments
- tuning demonstrations
- bursts

---

# 16. QT GUI Constellation Sink

## First Introduced

Chapter 5

At this stage it is only a way to view complex I/Q samples.

## Full Digital-Communication Use

Chapter 18 onward.

## Questions It Helps Answer

- Where are the I/Q samples?
- What modulation is being used?
- How much noise is present?
- Is there phase rotation?
- Is there carrier frequency offset?
- Is there timing error?
- Is the channel distorting the symbols?
- Did equalization help?

## Main Lesson

The same display introduced for I/Q becomes a powerful receiver diagnostic tool later.

---

# 17. QT GUI Number Sink

## First Useful Appearance

Chapter 8 or later.

## Uses

- magnitude
- power-related quantities
- measured numerical values
- error metrics where useful

## Important Warning

Number Sink does not automatically calculate SNR.

It displays the value supplied to it.

If we want SNR, we must first calculate the required signal and noise powers.

---

# 18. QT GUI Histogram Sink

## Possible First Use

Chapter 8

## Purpose

Useful if it genuinely improves the explanation of:

- Gaussian noise
- amplitude distribution
- random samples

This is optional rather than mandatory.

---

# 19. Multiple Views of One Signal

## First Introduced

Chapter 2 or 3.

Example:

```text
                    → Time Sink
Signal Source →
                    → Frequency Sink
```

Later:

```text
                    → Time Sink
Complex Signal →
                    → Frequency Sink
                    → Constellation Sink
```

## Main Lesson

Several sinks can observe the same stream.

They do not represent several different copies of the physical signal.

---

# 20. Arithmetic Blocks

Introduce naturally when their mathematical operations become useful.

| Operation | First Major Use |
|---|---|
| Add | Ch. 2 |
| Add Const | Early chapters where useful |
| Subtract | When comparison requires it |
| Multiply | Ch. 9 |
| Multiply Const | Ch. 8 |
| Conjugate | Ch. 12 |
| Magnitude | Ch. 5 |
| Magnitude Squared | Ch. 8/12 |
| Phase / Arg | Ch. 5 |

## Goal

Never teach an arithmetic block as just a GUI object.

Connect it to what the operation does mathematically to the signal.

---

# 21. Real and Complex Mixing

## First Introduced

Chapter 9

## Blocks / Tools

- Multiply
- Signal Source configured for real output
- Signal Source configured for complex output
- runtime LO frequency control
- Frequency Sink

## Experiment A

Real signal × real oscillator

Observe:

- sum frequency
- difference frequency

## Experiment B

Complex signal × complex oscillator

Observe directional frequency translation.

## Main Lesson

Real mixing and complex mixing should not be presented as if they were identical operations.

---

# 22. Filtering

## First Introduced

Chapter 10

## Blocks

- Low Pass Filter
- High Pass Filter
- Band Pass Filter
- Band Reject Filter
- FIR Filter
- FFT Filter later if useful

## Parameters

Teach:

- gain
- sample rate
- cutoff
- transition width
- window
- decimation
- taps

## Reused

Throughout receivers, modulation and channel processing.

## Main Goal

The reader should be able to choose filter parameters from the signal problem instead of copying values.

---

# 23. Filter Taps

## First Encounter

Chapter 10

## Proper Connection to Theory

Chapter 11

## Main Lesson

For an FIR filter, the taps are closely connected to its impulse response.

This becomes the bridge between:

```text
Filtering
↓
Impulse response
↓
Convolution
```

---

# 24. Finite Sequences

## First Major Use

Chapter 11

## Blocks

- Vector Source
- Vector Sink where useful
- Head
- Repeat

## Uses

Demonstrate:

- impulses
- short sequences
- convolution
- correlation
- known preambles
- symbol mapping

## Goal

Not every teaching experiment should use an endless stream.

Small numerical sequences often make DSP ideas easier to see.

---

# 25. Delay and Stream Manipulation

## First Major Use

Chapter 12

## Useful Blocks

- Delay
- Head
- Skip Head
- Keep 1 in N
- Repeat
- Selector where useful

## Applications

- controlled delay
- alignment
- correlation
- timing experiments
- synchronization experiments

---

# 26. Correlation and Detection

## First Introduced

Chapter 12

## Reused

Chapter 24 for packet/frame detection.

## Possible GNU Radio Tools

The exact flowgraph should be chosen after testing.

Possible ingredients include:

- Delay
- Conjugate
- Multiply
- Moving Average
- magnitude-squared processing
- correlation-specific blocks
- access-code correlation blocks later

## Important Rule

Do not begin by hiding correlation inside a sophisticated convenience block.

First make the idea visible.

---

# 27. Audio Source and Sink

## First Major Use

Chapter 14 or 15.

## Features

- Audio Source
- Audio Sink
- audio sample rate
- audio device selection where necessary

## Main Lesson

Audio rate and RF/baseband rate are often different.

This becomes an important reason to learn sample-rate conversion.

---

# 28. Resampling

## First Encounter

Decimation appears in filtering.

## Proper Treatment

Chapter 15 onward.

## Features

- decimation
- interpolation
- Rational Resampler
- FIR-based rate changes where appropriate

## Mathematics

The reader should always know the output rate.

$$
f_{\text{out}}
=
f_{\text{in}}
\frac{L}{M}
$$

where $L$ is interpolation and $M$ is decimation.

## Main Rule

Never let Rational Resampler become a "make the rates work somehow" block.

The reader should calculate why the chosen factors are needed.

---

# 29. Analog Modulation Blocks

## Chapters

14 and 15

## AM

Prefer manual construction first using simple arithmetic blocks.

The reader should see how AM is created before using convenience blocks.

## FM

Introduce suitable:

- FM modulation/demodulation blocks
- NBFM/WBFM processing
- Quadrature Demod where useful
- audio-rate conversion

## Goal

GNU Radio convenience blocks should come after the underlying signal operation is understood.

---

# 30. Digital Data Representation

## First Introduced

Chapter 16

## Features

- Random Source
- byte streams
- bit values
- packed versus unpacked data
- Repack Bits where useful
- groups of bits
- symbol values

## Main Signal Progression

```text
Bits
↓
Symbol values
↓
I/Q constellation points
↓
Samples
↓
Waveform
```

---

# 31. PAM

## First Introduced

Chapter 17

## Useful GNU Radio Features

The exact implementation should remain simple.

Possible ingredients:

- Vector Source for controlled data
- Random Source
- mapping operation
- repeat/interpolation where needed
- Time Sink
- Histogram Sink if useful
- noise

## Goal

Make symbol levels and decision thresholds visible before moving into complex constellations.

---

# 32. Constellation Objects and Symbol Mapping

## First Major Use

Chapter 18

## Features

- constellation definitions
- constellation encoder/decoder where useful
- symbol mapping
- BPSK
- QPSK
- QAM
- decision points

## Progression

```text
BPSK
↓
QPSK
↓
16-QAM
```

## Main Lesson

A constellation is a mapping between digital symbols and I/Q coordinates.

---

# 33. Pulse Shaping

## First Introduced

Chapter 19

## Features

- interpolation
- samples per symbol
- root-raised-cosine taps
- suitable FIR filtering
- roll-off / excess bandwidth
- spectrum observation

## Main Experiment

Compare:

```text
Symbols without useful shaping
↓
Pulse-shaped symbols
```

Observe:

- time domain
- spectrum
- constellation

---

# 34. Matched Filtering

## First Introduced Conceptually

Chapter 12

## Used Properly in Digital Receiver

Chapter 19

## Features

- RRC receive filter
- matching transmit/receive filtering
- signal-to-noise improvement intuition
- timing preparation

## Main Lesson

The matched filter is not just "another low-pass filter."

It is selected in relation to the transmitted pulse shape.

---

# 35. Eye-Diagram Visualization

## First Major Use

Chapter 19 or 23.

Use a dedicated GNU Radio visualization only if it is available and stable in the selected book environment.

Otherwise create the eye view using another reproducible method.

## Uses

Show:

- open eye
- ISI
- wrong timing
- noise
- timing recovery improvement

The concept matters more than the exact GUI block.

---

# 36. Channel Model

## First Introduced

Chapter 20

## Parameters to Explore

- noise voltage
- frequency offset
- timing/sample-rate offset
- multipath taps

## Experiments

Add one impairment at a time.

Do not switch on every impairment simultaneously.

Sequence:

```text
Ideal channel
↓
Noise
↓
Frequency offset
↓
Timing offset
↓
Multipath
```

## Reused

Chapters 21 to 28.

## Main Goal

The Channel Model becomes our controlled laboratory for receiver impairments.

---

# 37. Wireless Channel Visualization

## Chapter

20

## GNU Radio Tools

Use combinations of:

- Time Sink
- Frequency Sink
- Constellation Sink
- Channel Model
- controlled delays
- controlled taps

## Goal

The reader should see how each impairment changes the signal rather than only reading its definition.

---

# 38. Equalization

## First Introduced

Chapter 21

## Preferred Modern Direction

Use the modern GNU Radio equalization architecture suitable for the selected GNU Radio version.

Expected tools include:

- Linear Equalizer
- Adaptive Algorithm
- suitable constellation/decision object
- training sequence where appropriate

## Concepts to Connect

- adaptive algorithm
- filter taps
- training
- blind operation where relevant
- decision-directed operation
- convergence

## Main Experiment

```text
Clean constellation
↓
Multipath
↓
Distorted constellation
↓
Equalizer
↓
Improved constellation
```

## Now Break the Flowgraph

- incorrect equalizer configuration
- too little training
- severe multipath
- high noise
- unsuitable adaptive algorithm

---

# 39. Automatic Gain Control

## First Major Use

Chapter 22 or Chapter 25.

## Feature

AGC

## Purpose

Normalize varying received amplitude before later receiver stages where appropriate.

## Main Lesson

AGC solves an amplitude-control problem.

It does not correct:

- frequency offset
- phase offset
- timing offset

---

# 40. PLL Concepts

## First Introduced

Chapter 22

## Possible GNU Radio Tools

- PLL Carrier Regeneration
- PLL Carrier Tracking
- PLL Frequency Detector

Use only the tools that genuinely help the explanation.

## Learning Order

```text
Reference signal
↓
Phase error
↓
Feedback correction
↓
Lock
```

Only then move toward modulated carrier recovery.

---

# 41. Costas Loop

## First Introduced

Chapter 22 after PLL intuition.

## Purpose

Carrier recovery for appropriate digitally modulated signals.

## Parameters to Teach

- loop bandwidth
- modulation/order where applicable
- phase/frequency behaviour

## Main Experiment

Show the constellation:

```text
Without carrier recovery
↓
rotating / incorrectly oriented constellation

With carrier recovery
↓
stable constellation
```

## Now Break the Flowgraph

- excessive frequency offset
- poor loop bandwidth
- disable loop
- inappropriate configuration

---

# 42. Symbol Sync

## First Introduced

Chapter 23

## Purpose

Recover symbol timing from an oversampled digital waveform.

## Concepts to Connect

- samples per symbol
- timing error detector
- loop bandwidth
- interpolation
- sampling instant

## Main Experiment

Show:

```text
Wrong sampling time
↓
uncertain symbols

Symbol synchronization
↓
stable decisions
```

## Important Rule

Teach timing as a problem before opening the Symbol Sync properties.

---

# 43. Frame and Packet Detection

## First Introduced

Chapter 24

## Features

Possible tools include:

- known preamble
- correlation
- access-code correlator
- tags
- packet-length information later

## Main Goal

Connect Chapter 12 correlation to a real communications purpose.

## Main Experiment

```text
Preamble + Payload
↓
Noise / Channel
↓
Correlation
↓
Frame detected
```

---

# 44. Stream Tags: First Encounter

## First Light Use

Chapter 24 if packet detection naturally creates tags.

## Rule

Do not fully explain tag architecture yet.

Say only enough for the experiment:

> GNU Radio can attach information to a particular location in a stream.

The formal explanation comes in Chapter 29.

---

# 45. Complete Single-Carrier Receiver

## Chapter

25

## GNU Radio Features Reused

This chapter should introduce very little that is completely new.

Reuse:

- source
- filtering
- resampling
- AGC
- matched filtering
- Costas Loop
- Symbol Sync
- equalizer
- constellation display
- correlation/frame detection

## Goal

The reader should see that earlier isolated blocks now form one receiver.

---

# 46. OFDM: Teaching Strategy

## Chapters

26 to 28

## Important Rule

Do not begin with GNU Radio's complete OFDM transmitter/receiver hierarchy.

First build the idea using familiar components.

Progression:

```text
Several subcarriers
↓
QAM symbols in frequency bins
↓
IFFT
↓
OFDM symbol
↓
Cyclic Prefix
↓
Channel
↓
FFT
↓
Recovered subcarriers
```

Only after this is understood should convenience OFDM blocks be explored.

---

# 47. FFT and IFFT for OFDM

## First FFT Use

Chapter 6 for analysis.

## New Use

Chapter 27 for synthesis and demodulation.

## Main Connection

Earlier:

> FFT tells us what frequencies are in a waveform.

Now:

> IFFT can construct the time-domain waveform corresponding to chosen frequency bins.

## GNU Radio Features

Possible use of:

- FFT
- IFFT
- Stream to Vector
- Vector to Stream
- complex vectors

This becomes a useful bridge into Chapter 29's deeper treatment of vectors.

---

# 48. OFDM Carrier Allocator

## First Introduced

Chapter 27 after manual OFDM intuition.

## Purpose

Map complex modulation symbols onto selected OFDM subcarriers before the IFFT.

## Concepts

- occupied carriers
- pilot carriers
- sync words where used
- FFT length
- frequency bins

## Rule

The reader should understand why carrier allocation exists before using the block.

---

# 49. OFDM Cyclic Prefix

## First Introduced

Chapter 28

## Possible Feature

OFDM Cyclic Prefixer

## Concepts

- OFDM symbol
- guard interval
- copied tail samples
- multipath delay
- symbol protection

## Experiment

Compare identical multipath channels:

```text
without cyclic prefix
```

and:

```text
with cyclic prefix
```

---

# 50. OFDM Channel Estimation and Equalization

## Chapter

28

## Possible GNU Radio Features

- OFDM Channel Estimation
- OFDM Frame Equalizer
- suitable equalizer objects
- pilot carriers

## Teaching Order

First show that different subcarriers emerge with different amplitude and phase changes.

Then ask:

> How could the receiver estimate those changes?

Only then introduce channel estimation.

---

# 51. Other OFDM Convenience Blocks

Introduce only after the manual signal path is understood.

Possible blocks include:

- OFDM Serializer
- OFDM Receiver
- OFDM Carrier Allocator
- OFDM Cyclic Prefixer
- OFDM Channel Estimation
- OFDM Frame Equalizer

Do not make the beginner memorise the entire GNU Radio OFDM stack.

The goal is to understand what each stage is solving.

---

# 52. Streams

## Used Implicitly

From Chapter 1 onward.

## Explained Formally

Chapter 29

## Concepts

- item
- continuous sequence of items
- input port
- output port
- block consumption
- block production
- buffers
- scheduler intuition

## Main Lesson

Most early GNU Radio connections carry a stream of items.

---

# 53. Vectors

## First Practical Encounter

Possibly Chapter 27 with FFT/IFFT.

## Explained Formally

Chapter 29

## Example

Input stream:

```text
1, 2, 3, 4, 5, 6, ...
```

Stream-to-Vector with vector length 3:

```text
[1,2,3], [4,5,6], ...
```

## Blocks

- Stream to Vector
- Vector to Stream
- Streams to Vector
- Vector to Streams

## Goal

The reader should understand that a vector is one stream item containing several values.

---

# 54. Stream Tags

## Formal Treatment

Chapter 29

## Concepts

- metadata associated with a stream position
- key
- value
- offset
- tag propagation
- packet-length tags
- synchronization/event information

## Simple Visual

```text
sample sample sample sample sample sample
                    ↑
                   TAG
```

## Goal

The reader should understand that metadata can travel alongside a continuous stream without becoming another sample.

---

# 55. Tagged Streams

## Formal Treatment

Chapter 29

## Concepts

- packet boundaries
- length tags
- tagged-stream processing
- packet-oriented blocks operating on stream data

## Useful Blocks

- Stream to Tagged Stream
- Tagged Stream Mux where useful
- Tagged Stream to PDU

---

# 56. Messages

## Formal Treatment

Chapter 29

## Concepts

- asynchronous information
- message ports
- PMT concept at a beginner level
- control/status information
- packet-oriented processing

## Visual Distinction

```text
Stream:
Block A ======> Block B

Message:
Block A ------> Block B
```

## Useful Feature

Message Debug

## Goal

The reader should understand that messages do not behave like continuous sample streams.

---

# 57. PDUs

## Formal Treatment

Chapter 29

## Conceptual Structure

```text
PDU
├── Metadata
└── Data
```

## Useful Conversion Blocks

- Tagged Stream to PDU
- PDU to Tagged Stream

## Main Lesson

Packet-oriented information sometimes makes more sense as a complete object than as an endless stream of samples.

---

# 58. Message Debug

## First Major Use

Chapter 29

## Purpose

Inspect messages and learn what is travelling over message ports.

## Reused

Packet and debugging work.

---

# 59. Hierarchical Blocks

## First Introduced

Chapter 30

## Main Experiment

Take a processing chain the reader already understands.

For example:

```text
Frequency Translation
+
Filtering
+
Decimation
```

Package it as a reusable block.

## Main Lesson

Hierarchical blocks are useful because a large design can be built from smaller meaningful subsystems.

---

# 60. Embedded Python Block

## First Introduced

Chapter 30

## Start Very Simply

Example:

```text
Input x[n]
↓
Embedded Python Block
↓
Output 2x[n]
```

Then show that custom processing can expose parameters.

Only later mention more advanced possibilities such as:

- vectors
- tags
- messages

## Goal

The reader should realize that GNU Radio is extensible.

If the desired operation does not exist as a standard block, custom processing can be created.

---

# 61. Generated Python

## First Introduced

Chapter 30

## Concepts

Explain lightly:

- GRC generates executable code
- blocks become objects
- connections become code
- variables become Python values
- runtime controls create corresponding code

## Goal

The reader should not be frightened when a GNU Radio error includes Python source lines.

Do not turn this into a generated-code programming chapter.

---

# 62. File Input and Output

## First Major Use

Chapter 30

## Blocks

- File Source
- File Sink
- WAV File Source/Sink where useful

## Applications

- record IQ
- replay IQ
- save experiments
- distribute sample data with the book
- reproduce hardware experiments without the hardware

## Important Idea

Recorded IQ data can become a bridge between the simulation chapters and hardware chapters.

---

# 63. Network Input and Output

## First Introduced

Chapter 30 if useful.

## Possible Tools

- TCP
- UDP
- ZeroMQ
- Socket PDU

Do not attempt to cover every networking block.

## Goal

Show that a GNU Radio flowgraph can exchange information with another application or system.

---

# 64. Scheduler and Buffer Intuition

## Formal Introduction

Chapter 30

## Concepts

- blocks process chunks rather than the entire infinite signal
- buffers exist between stream blocks
- blocks consume items
- blocks produce items
- runtime scheduling coordinates processing

## Goal

Give just enough understanding for:

- performance troubleshooting
- Embedded Python Blocks
- stream behaviour
- buffer-related issues

Do not introduce internal scheduler mathematics unless it directly helps.

---

# 65. Performance Awareness

## Developed Throughout

More explicit in Chapter 30.

## Factors to Explore

- sample rate
- FFT size
- very narrow filter transition width
- number of GUI sinks
- expensive resampling
- complex processing
- high hardware rates
- inefficient custom blocks

## Main Lesson

A mathematically valid flowgraph may still fail to operate in real time if the computer cannot process samples quickly enough.

---

# 66. Debugging Strategy

Debugging should be taught throughout the book.

## Core Habit

Ask:

```text
What should the signal look like here?
↓
What does it actually look like?
↓
At which block did those two begin to differ?
```

## Tools

Use:

- Time Sink
- Frequency Sink
- Constellation Sink
- Number Sink
- Message Debug
- console output
- file recording
- temporarily bypassing blocks
- replacing hardware with Signal Source
- simplifying the flowgraph

## Goal

The reader should learn signal-processing debugging, not only software-error debugging.

---

# 67. Two Kinds of GNU Radio Failure

This distinction should appear repeatedly.

## Flowgraph / Software Failure

Examples:

- incompatible port types
- invalid block parameter
- missing dependency
- Python exception
- hardware connection failure

The flowgraph may refuse to run.

## Signal-Processing Failure

Examples:

- aliasing
- wrong filter cutoff
- incorrect local oscillator
- poor timing
- carrier offset
- equalizer not converged
- excessive noise

The flowgraph may run perfectly while producing the wrong result.

This second kind is especially important.

---

# 68. Hardware Sources

## First Introduced

Chapter 31

## Possible Hardware Families

- RTL-SDR
- ADALM-Pluto
- HackRF
- USRP
- other supported SDR devices

Do not make the conceptual chapter depend on one manufacturer.

## Parameters

Teach:

- centre frequency
- sample rate
- RF bandwidth
- gain
- antenna/source channel where supported
- device arguments
- frequency correction where relevant

---

# 69. Centre Frequency vs Sample Rate

## Formal Treatment

Chapter 31

This distinction should be reinforced repeatedly.

## Centre Frequency

Where the SDR is tuned in RF.

## Sample Rate

How many digital samples are produced per second and, together with the receiver architecture, what span of spectrum can be digitally represented around the tuning point.

## Main Lesson

These are completely different quantities even though both are measured in hertz.

---

# 70. Hardware Gain

## First Introduced

Chapter 31

## Concepts

- gain
- LNA/VGA stages where applicable
- automatic gain
- manual gain
- noise floor
- clipping
- dynamic range

## Now Break the Flowgraph

Use too much gain.

Observe:

- clipping
- strong unwanted components
- raised/distorted spectrum

Then use too little gain.

Observe weak-signal visibility.

---

# 71. Frequency Translating FIR Filter

## First Major Use

Chapter 32

## Why It Is Important

It combines ideas the reader already knows:

```text
Frequency Translation
+
Filtering
+
Decimation
```

## Teaching Rule

Do not introduce it as a mysterious shortcut.

First connect every part of the block to an earlier chapter.

---

# 72. Real Receiver GUI

## Chapter

32

## Features

Combine:

- tuning control
- RF gain control
- filter control where useful
- Frequency Sink
- Waterfall Sink
- audio controls

## Goal

The reader should learn that a usable SDR application includes both processing and sensible controls.

---

# 73. GNU Radio Toolbox Coverage by Chapter

This is the working chapter-level map.

---

## Chapter 1: What Is Software Defined Radio?

### New GNU Radio Features

- GNU Radio Companion
- block library
- Signal Source
- Throttle
- QT GUI Time Sink
- block properties
- connections
- Run
- Stop
- Generate
- save `.grc`
- simple GRC errors

### Main Skill

Build, save and run a basic flowgraph.

---

## Chapter 2: Understanding Signals

### New Features

- Variable
- expressions
- Add
- multiple branches
- Time Sink controls

### Main Skill

Generate and manipulate simple signals.

---

## Chapter 3: Sampling and Aliasing

### New Features

- QT GUI Range
- runtime parameter changes
- Frequency Sink introduction
- sample-rate consistency
- Throttle in depth

### Break Experiment

Create aliasing deliberately.

---

## Chapter 4: Complex Numbers for SDR

### New Features

- GNU Radio data types
- Float
- Complex
- port colours
- Float to Complex
- Complex to Real
- Complex to Imag

### Main Skill

Work with complex streams without treating them as mysterious objects.

---

## Chapter 5: I and Q Signals

### New Features

- Signal Source with Complex output
- Complex to Mag
- Complex to Arg
- Constellation Sink
- multiple views of complex data

### Main Skill

Inspect I/Q samples.

---

## Chapter 6: Time and Frequency Domain

### New Features

- Frequency Sink in depth
- FFT size
- windows
- averaging
- Waterfall Sink

### Main Skill

Use spectrum tools intelligently.

---

## Chapter 7: Positive and Negative Frequencies

### New Features

Very few.

This chapter deliberately reuses existing tools.

### Main Skill

Interpret real and complex spectra.

---

## Chapter 8: Noise, Power and SNR

### New Features

- Noise Source
- Multiply Const
- Number Sink where useful
- Histogram Sink if useful

### Main Skill

Create and observe controlled noise.

---

## Chapter 9: Mixing

### New Features

- Multiply
- real LO
- complex LO
- runtime LO control

### Main Skill

Perform and interpret frequency translation.

---

## Chapter 10: Filtering

### New Features

- Low Pass Filter
- High Pass Filter
- Band Pass Filter
- Band Reject Filter
- taps
- decimation

### Main Skill

Select signals by frequency.

---

## Chapter 11: Convolution

### New Features

- FIR Filter in depth
- Vector Source
- Head
- Repeat
- finite sequences

### Main Skill

Connect FIR filtering with impulse response and convolution.

---

## Chapter 12: Correlation and Detection

### New Features

- Delay
- Conjugate
- correlation-processing chain
- Moving Average where useful

### Main Skill

Detect a known pattern and estimate delay.

---

## Chapter 13: Why Modulation Exists

### New Features

Minimal.

Reuse mixing and spectrum tools.

### Main Skill

Understand modulation as frequency placement.

---

## Chapter 14: AM

### New Features

- manual modulation chain
- Audio Source/Sink if useful

### Main Skill

Build AM from basic operations.

---

## Chapter 15: FM

### New Features

- NBFM/WBFM blocks where suitable
- Quadrature Demod where useful
- Rational Resampler
- interpolation
- decimation
- audio-rate conversion

### Main Skill

Manage several sample rates inside one radio.

---

## Chapter 16: Bits and Symbols

### New Features

- Random Source
- byte data
- Repack Bits where useful
- controlled digital sequences

### Main Skill

Follow data from bits to symbol values.

---

## Chapter 17: PAM

### New Features

- mapping digital symbols to amplitude levels
- decision visualization

### Main Skill

Understand symbol levels before complex modulation.

---

## Chapter 18: BPSK, QPSK and QAM

### New Features

- constellation objects
- constellation encoding/decoding where useful
- symbol mapping
- Constellation Sink in depth

### Main Skill

Map bits to complex symbol points.

---

## Chapter 19: Pulse Shaping and Matched Filtering

### New Features

- RRC taps
- interpolation
- samples per symbol
- matched receive filtering
- eye visualization where practical

### Main Skill

Turn discrete symbols into bandwidth-controlled waveforms.

---

## Chapter 20: Wireless Channel

### New Features

- Channel Model
- frequency offset
- timing/sample-rate offset
- multipath taps

### Main Skill

Create controlled receiver impairments.

---

## Chapter 21: Equalization

### New Features

- Linear Equalizer
- Adaptive Algorithm
- training/equalization controls

### Main Skill

Compensate for channel distortion.

---

## Chapter 22: PLL and Carrier Synchronization

### New Features

- PLL concepts/tools
- Costas Loop
- loop bandwidth
- carrier phase/frequency recovery

### Main Skill

Recover a reference carrier.

---

## Chapter 23: Clock and Symbol Timing Synchronization

### New Features

- Symbol Sync
- timing-error configuration
- samples-per-symbol relationships

### Main Skill

Recover the correct symbol sampling instants.

---

## Chapter 24: Frame Synchronization

### New Features

- preamble processing
- correlation-based detection
- access-code tools where suitable
- first light use of tags

### Main Skill

Find message boundaries in a continuous stream.

---

## Chapter 25: Complete Single-Carrier Receiver

### New Features

Ideally almost none.

### Main Skill

Integrate:

- filtering
- AGC
- matched filtering
- carrier recovery
- timing recovery
- equalization
- frame detection

---

## Chapter 26: Why OFDM?

### New Features

Minimal.

Use existing signal-generation and spectrum tools.

### Main Skill

Understand orthogonal multicarrier transmission.

---

## Chapter 27: Building OFDM with IFFT

### New Features

- FFT/IFFT block processing
- vectors
- Stream to Vector
- Vector to Stream
- OFDM Carrier Allocator after manual explanation

### Main Skill

Build OFDM symbols from frequency-domain data.

---

## Chapter 28: Cyclic Prefix and OFDM Channel

### New Features

- OFDM Cyclic Prefixer
- OFDM Channel Estimation
- OFDM Frame Equalizer
- OFDM Serializer/Receiver where useful

### Main Skill

Understand how OFDM handles a multipath channel.

---

## Chapter 29: Streams, Vectors, Tags, Messages and PDUs

### New Features

- streams formally
- vectors formally
- Stream to Vector
- Vector to Stream
- stream tags
- tagged streams
- Stream to Tagged Stream
- Message Debug
- messages
- PDUs
- Tagged Stream to PDU
- PDU to Tagged Stream

### Main Skill

Understand GNU Radio's different data-transfer mechanisms.

---

## Chapter 30: Building Larger GNU Radio Systems

### New Features

- Hierarchical Blocks
- Embedded Python Block
- generated Python
- File Source/Sink
- IQ recording
- networking
- scheduler intuition
- buffers
- logging
- performance debugging

### Main Skill

Move from experiments to reusable GNU Radio applications.

---

## Chapter 31: SDR Hardware

### New Features

- SDR hardware Source
- centre frequency
- RF sample rate
- RF bandwidth
- gain
- antenna/channel selection
- device configuration

### Main Skill

Acquire and interpret real RF samples.

---

## Chapter 32: Real Radio Receiver

### New Features

- Frequency Translating FIR Filter
- integrated receiver GUI
- real-time tuning
- RF gain controls
- Waterfall in real RF use

### Main Skill

Build and debug a complete real receiver.

---

## Chapter 33: Independent SDR Design

### New Features

None should be required.

That is intentional.

### Main Skill

Choose GNU Radio tools from the signal-processing requirement rather than from a tutorial.

---

# 74. GNU Radio Toolbox Checklist

Whenever a block or feature receives a Toolbox section, make sure we can answer:

- What does it do?
- Why are we using it here?
- What enters it?
- What leaves it?
- What data type does it use?
- Does it change the sample rate?
- Which parameters matter?
- What are the units?
- Can any parameters change at runtime?
- What common mistake should the reader avoid?
- What would incorrect configuration look like?
- Where will we use it again?

If we cannot explain those things simply, we are probably introducing the feature too early.

---

# 75. Now Break the Flowgraph Map

Every chapter does not require an artificial error, but most practical chapters should contain a useful failure experiment.

| Chapter | Deliberate Problem |
|---|---|
| 1 | Disconnect a block |
| 2 | Change waveform parameters unexpectedly |
| 3 | Violate Nyquist / remove Throttle |
| 4 | Connect incompatible data types |
| 5 | Remove or reverse Q |
| 6 | Create leakage / poor FFT resolution |
| 7 | Convert complex signal to real |
| 8 | Bury signal in noise |
| 9 | Mistune or reverse LO |
| 10 | Wrong filter cutoff |
| 11 | Change impulse response |
| 12 | Wrong correlation reference |
| 14 | Overmodulate AM |
| 15 | Wrong resampling ratio |
| 17 | Cross PAM decision thresholds |
| 18 | Rotate/noise the constellation |
| 19 | Remove matched filter / wrong RRC parameters |
| 20 | Add channel impairments one by one |
| 21 | Make equalizer fail to converge |
| 22 | Poor PLL/Costas settings |
| 23 | Introduce timing mismatch |
| 24 | Wrong/weak preamble |
| 25 | Disable one receiver stage |
| 26 | Destroy subcarrier orthogonality |
| 27 | Misplace OFDM bins |
| 28 | Cyclic prefix too short |
| 29 | Mismatch vector/tag/message assumptions |
| 30 | Trigger performance or custom-block problems |
| 31 | Too much/too little RF gain |
| 32 | Misconfigure receiver stages |
| 33 | Diagnose an unknown fault without instructions |

---

# 76. Features That Should Be Revisited Several Times

Some GNU Radio features are too important to appear only once.

## Signal Source

Used from beginner waveform generation through mixing and IQ.

## Time Sink

Used for:

- waveform basics
- sampling
- I/Q components
- modulation
- timing

## Frequency Sink

Used for:

- aliasing
- FFT
- mixing
- filtering
- noise
- modulation
- hardware

## Constellation Sink

Used for:

- I/Q
- PSK/QAM
- channel impairment
- equalization
- synchronization

## QT GUI Range

Used for:

- frequency
- amplitude
- noise
- LO
- offsets
- gains

## Channel Model

Used across:

- channel chapter
- equalization
- synchronization
- complete receiver
- OFDM

This repetition is intentional.

The reader learns a tool by using it in different situations.

---

# 77. Features We Should Not Force Into the Main Book

GNU Radio contains many specialised blocks.

The goal is not to mention every installed block.

The book should teach the major concepts and block families well enough that the reader can later approach unfamiliar blocks independently.

Topics that may be left for a later volume or advanced appendix include:

- detailed FEC API
- convolutional coding
- LDPC
- polar coding
- advanced trellis processing
- MIMO
- advanced adaptive filtering
- PFB channelizers
- advanced packet protocols
- advanced OFDM
- OFDMA
- DSSS
- frequency hopping
- advanced ZeroMQ architectures
- ControlPort
- RFNoC
- FPGA acceleration
- custom C++ blocks
- full OOT-module development

We may later decide to add one beginner-friendly FEC chapter, but it should not be inserted simply to increase coverage.

---

# 78. Features That Need Experimental Validation Before We Freeze the Book

Some chapters should not have their final block chain decided on paper.

We need to build and test them first.

In particular:

- Chapter 12 correlation
- Chapter 17 PAM mapping
- Chapter 19 eye visualization
- Chapter 21 equalization
- Chapter 22 PLL versus Costas Loop demonstrations
- Chapter 23 Symbol Sync demonstration
- Chapter 24 packet detection
- Chapters 27–28 OFDM
- hardware-independent flowgraphs for Chapter 31/32

For these topics, choose the flowgraph that makes the idea easiest to understand rather than the one that uses the fewest blocks.

---

# 79. GNU Radio Version Check Before Publication

Before the first release of the book:

1. Choose the exact supported GNU Radio version.
2. Open every `.grc` experiment using that version.
3. Run every experiment.
4. Verify every block name.
5. Verify every parameter name.
6. Verify screenshots against the actual GUI.
7. Check deprecated blocks.
8. Check hardware-source availability.
9. Check the companion repository from a clean installation.
10. Record the tested version clearly in the README and book.

Do not assume that a flowgraph created months earlier still matches the final software version.

---

# 80. Final GNU Radio Goal

At the beginning of the book, the reader may think:

> I need to know which blocks to connect.

By the middle of the book, we want that to become:

> I need to filter this signal and then reduce its sample rate.

Later:

> I need carrier recovery, timing recovery and equalization before I can make reliable symbol decisions.

And by the final chapter:

> I understand what the receiver must do. Now I can decide how to implement it in GNU Radio.

That is the real purpose of this feature map.