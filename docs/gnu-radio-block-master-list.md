# GNU Radio Block Master List

**Updated through Chapter 7**

---

## Why This Document Exists

GNU Radio contains a very large number of blocks.

Trying to learn all of them at once would not be useful.

This document therefore does **not** attempt to list every block available in GNU Radio. Instead, it keeps track of the blocks that matter to the learning path of this book.

The list grows as the book grows.

When we encounter an important block for the first time, we normally introduce it inside the corresponding chapter through the **GNU Radio Toolbox**.

The chapter answers questions such as:

- Why do we need this block?
- What does it do?
- What enters it?
- What comes out?
- Which settings matter?
- What can go wrong?

This Master List serves a different purpose.

It gives us one place where we can look back and answer:

> **Which GNU Radio blocks have we encountered so far, what do they do, and where did we first meet them?**

So the two resources work together:

```text
Chapter
   ↓
New signal-processing problem
   ↓
GNU Radio Toolbox
   ↓
Learn the new block in context
   ↓
Use it in an experiment
   ↓
GNU Radio Block Master List
```

The **Toolbox teaches the block**.

The **Master List keeps track of it**.

---

## How to Read This List

### Importance

The blocks are grouped into four levels.

- **Essential** — fundamental blocks that we should understand and become comfortable using.
- **Important** — useful blocks that become important when the corresponding DSP or SDR concept appears.
- **Advanced** — blocks that will become useful later as our SDR systems become more realistic.
- **Specialized** — blocks mainly intended for particular applications.

### Status

- ✅ **Used** — already used in one of our completed experiments.
- 🔜 **Planned** — expected to appear soon in the learning path.
- ⏳ **Later** — useful, but the corresponding topic has not been reached yet.
- ➖ **Optional** — useful in some situations, but not required for the main learning path.

The status of this document should be updated as the book progresses.

---

# 1. Signal and Data Sources

Source blocks create the data that enters a flowgraph.

During the early chapters, artificial sources are especially useful because they allow us to work with signals whose behaviour we already know.

| Block | Importance | Status | What it does | First introduced |
|---|---|---|---|---|
| **Signal Source** | Essential | ✅ Used | Generates periodic signals such as sine and cosine waves | Earlier chapters |
| **Noise Source** | Essential | ✅ Used | Generates random noise using distributions such as Gaussian noise | Chapter 7 |
| **Fast Noise Source** | Important | ⏳ Later | Generates noise using a computationally efficient implementation | Later |
| **Random Source** | Important | ⏳ Later | Generates sequences of random values | Later digital communication chapters |
| **Random Uniform Source** | Important | ⏳ Later | Generates uniformly distributed random values | Later |
| **Constant Source** | Important | ⏳ Later | Produces a stream containing a constant value | Later |
| **GLFSR Source** | Important | ⏳ Later | Generates pseudo-random sequences using a linear-feedback shift register | Later digital communications |
| **VCO** | Important | ⏳ Later | Generates an oscillator whose instantaneous frequency is controlled by another signal | Later modulation chapters |
| **VCO (Complex)** | Important | ⏳ Later | Complex-output voltage-controlled oscillator | Later modulation and SDR chapters |
| **File Source** | Important | ⏳ Later | Reads previously stored samples from a file | Later |
| **Vector Source** | Important | ⏳ Later | Produces a repeating or finite sequence of predefined values | Later |

---

## 1.1 Signal Source

### What it does

Signal Source generates known periodic waveforms inside GNU Radio.

Common waveform choices include:

- cosine;
- sine;
- square;
- triangle;
- constant.

### Important parameters

- Output Type
- Sample Rate
- Waveform
- Frequency
- Amplitude
- Offset
- Initial Phase

### Why it matters

Signal Source is one of our main laboratory tools.

It lets us create a signal whose properties are known before the experiment begins.

That makes it possible to predict what should happen and then compare our prediction with GNU Radio.

### Watch out

Signal Source does not generate a physical analog voltage.

It generates numerical samples inside GNU Radio.

---

## 1.2 Noise Source

### What it does

Noise Source generates random samples according to a selected statistical distribution.

In Chapter 7 we used **Gaussian noise**.

### Important parameters

- Output Type
- Noise Type
- Amplitude
- Seed

### Why it matters

Noise Source allows us to investigate:

- random signals;
- noise power;
- signal-to-noise ratio;
- noise floor;
- bandwidth-dependent noise power;
- receiver behaviour in noise.

### Important observation

Noise amplitude and noise power are not the same thing.

For the Gaussian noise used in our Chapter 7 experiments, the measured average power followed approximately

$$
P_n \approx A_n^2
$$

where $A_n$ is the Noise Source amplitude parameter.

---

# 2. Flow Control and Flowgraph Utilities

These blocks and objects help control how a GNU Radio flowgraph operates.

They may not always change the mathematical signal directly, but they are essential for building practical experiments.

| Block / Object | Importance | Status | What it does | First introduced |
|---|---|---|---|---|
| **Throttle** | Essential | ✅ Used | Limits processing rate in software-only flowgraphs | Earlier chapters |
| **Variable** | Essential | ✅ Used | Stores a value that can be reused by multiple blocks | Earlier chapters |

---

## 2.1 Throttle

### What it does

Throttle limits how quickly samples move through a software-only flowgraph.

### Why we use it

A flowgraph containing only software-generated sources may otherwise run as quickly as the CPU allows.

Throttle gives the flowgraph an approximate processing rate.

### Watch out

Throttle does **not** perform analog-to-digital sampling.

The data inside GNU Radio is already represented as samples.

---

## 2.2 Variable

### What it does

A Variable stores a value that can be referenced by other blocks.

A common example is:

```text
samp_rate = 32000
```

Instead of entering `32000` separately into every block, we can use:

```text
samp_rate
```

### Why it matters

Variables make flowgraphs:

- easier to read;
- easier to modify;
- less error-prone;
- easier to control at runtime.

---

# 3. Mathematical Operations

These blocks perform mathematical operations directly on samples.

They are simple individually, but combining them allows us to construct surprisingly powerful measurements and signal-processing operations.

| Block | Importance | Status | What it does | First introduced / major use |
|---|---|---|---|---|
| **Add** | Essential | ✅ Used | Adds input streams sample by sample | Earlier chapters / Chapter 7 |
| **Multiply** | Essential | ✅ Used | Multiplies input streams sample by sample | Chapter 7 power measurement |
| **Divide** | Important | ✅ Used | Divides one input stream by another | Chapter 7 SNR measurement |
| **Multiply Const** | Essential | ✅ Used | Multiplies every sample by a fixed constant | Chapter 7 SNR measurement |
| **Log10** | Important | ✅ Used | Calculates the base-10 logarithm | Chapter 7 SNR measurement |
| **Add Const** | Important | ⏳ Later | Adds a constant to every sample | Later |
| **Subtract** | Important | ⏳ Later | Subtracts one stream from another | Later |
| **Abs** | Important | ⏳ Later | Calculates absolute value | Later |

---

## 3.1 Add

For two input streams,

$$
x[n]
$$

and

$$
y[n]
$$

the Add block produces

$$
z[n]=x[n]+y[n]
$$

### Chapter 7 use

We used Add to construct a noisy signal:

$$
r[n]=s[n]+w[n]
$$

where:

- $s[n]$ was our cosine;
- $w[n]$ was Gaussian noise.

---

## 3.2 Multiply

Multiply performs sample-by-sample multiplication.

For two inputs,

$$
x[n]
$$

and

$$
y[n]
$$

the output is

$$
z[n]=x[n]y[n]
$$

### Chapter 7 use

To measure the power of a real signal, we connected the same signal to both inputs:

$$
x[n]\times x[n]=x^2[n]
$$

This gave us the first step of our power estimator.

### Later use

Multiply will also become important for mixing and modulation.

---

## 3.3 Divide

For two input streams, Divide calculates

$$
z[n]=\frac{x[n]}{y[n]}
$$

### Chapter 7 use

We used it to calculate the signal-to-noise power ratio:

$$
\frac{P_s}{P_n}
$$

---

## 3.4 Log10

Log10 calculates the base-10 logarithm of its input.

### Chapter 7 use

It formed part of our SNR calculation:

$$
\log_{10}
\left(
\frac{P_s}{P_n}
\right)
$$

---

## 3.5 Multiply Const

Multiply Const multiplies every sample by a fixed value.

### Chapter 7 use

Using a constant of `10`, we completed the power-ratio conversion to decibels:

$$
\mathrm{SNR}_{\mathrm{dB}}
=
10\log_{10}
\left(
\frac{P_s}{P_n}
\right)
$$

---

# 4. Complex-Signal and Type-Conversion Blocks

These blocks become important once we start working with I/Q and complex-valued signals.

| Block | Importance | Status | What it does | First introduced |
|---|---|---|---|---|
| **Float to Complex** | Essential | ✅ Used | Combines two float streams into one complex stream | Earlier I/Q chapters |
| **Complex to Real** | Essential | ✅ Used | Extracts the real part of a complex signal | Earlier I/Q chapters |
| **Complex to Imag** | Essential | ✅ Used | Extracts the imaginary part of a complex signal | Earlier I/Q chapters |
| **Complex to Mag** | Essential | ✅ Used | Calculates complex magnitude | Earlier I/Q chapters |
| **Complex to Arg** | Essential | ✅ Used | Calculates complex phase | Earlier I/Q chapters |
| **Complex to Mag²** | Essential | ✅ Used | Calculates squared complex magnitude | Chapter 6 |
| **Complex to Float** | Important | ⏳ Later | Separates complex data into float components | Later |
| **Char to Float** | Important | ⏳ Later | Converts byte/char samples to float | Later digital communications |
| **Float to Char** | Important | ⏳ Later | Converts float samples to byte/char representation | Later |

---

## 4.1 Float to Complex

Float to Complex combines two real-valued streams:

$$
I[n]
$$

and

$$
Q[n]
$$

into

$$
z[n]=I[n]+jQ[n]
$$

This was one of the first blocks that allowed us to construct I/Q signals explicitly.

---

## 4.2 Complex to Real

For

$$
z[n]=I[n]+jQ[n]
$$

Complex to Real returns

$$
I[n]
$$

---

## 4.3 Complex to Imag

Complex to Imag returns

$$
Q[n]
$$

---

## 4.4 Complex to Mag

Complex to Mag calculates

$$
|z[n]|
=
\sqrt{I^2[n]+Q^2[n]}
$$

---

## 4.5 Complex to Arg

Complex to Arg calculates the phase angle of a complex sample.

Conceptually,

$$
\phi[n]
=
\operatorname{atan2}(Q[n],I[n])
$$

---

## 4.6 Complex to Mag²

Complex to Mag² calculates

$$
|z[n]|^2
=
I^2[n]+Q^2[n]
$$

This is especially useful when working with complex-signal power.

---

# 5. Stream and Vector Operations

GNU Radio normally processes continuous streams of items.

Some operations, however, work on groups of samples represented as vectors.

| Block | Importance | Status | What it does | First introduced |
|---|---|---|---|---|
| **Stream to Vector** | Essential | ✅ Used | Groups consecutive stream samples into vectors | Chapter 6 |
| **Vector to Stream** | Essential | 🔜 Planned | Converts vectors back into a continuous stream | Later |
| **Keep 1 in N** | Important | ⏳ Later | Keeps one item from every group of N items | Later |
| **Head** | Important | ⏳ Later | Allows only a specified number of items to pass | Later |
| **Delay** | Important | ⏳ Later | Delays a stream by a specified number of samples | Later |

---

## 5.1 Stream to Vector

Suppose a stream contains:

```text
x0, x1, x2, x3, x4, x5, ...
```

With a vector length of 4, Stream to Vector produces:

```text
[x0, x1, x2, x3]
[x4, x5, x6, x7]
...
```

### Why we needed it

The FFT operates on a block of samples rather than on one isolated sample.

Stream to Vector allowed us to collect consecutive samples into FFT-sized groups.

---

# 6. Fourier and Spectrum Analysis

These blocks allow us to move between time-domain and frequency-domain representations.

| Block | Importance | Status | What it does | First introduced |
|---|---|---|---|---|
| **FFT** | Essential | ✅ Used | Computes the discrete Fourier transform efficiently | Chapter 6 |
| **IFFT** | Essential | ⏳ Later | Converts frequency-domain values into a time-domain sequence | Later OFDM chapters |
| **Goertzel** | Important | ⏳ Later | Efficiently evaluates selected frequency components | Later tone-detection work |
| **Log Power FFT** | Important | ⏳ Later | Produces logarithmic spectral-power information | Later |

---

## 6.1 FFT

The FFT is an efficient algorithm for computing the DFT.

It transforms a vector of time-domain samples into a vector describing the signal in the frequency domain.

### Why it matters

The FFT allows us to investigate:

- frequency components;
- positive and negative frequencies;
- spectral leakage;
- FFT size;
- frequency resolution;
- windowing;
- noise spectrum.

### Important distinction

The FFT does not create frequencies that were not already represented by the input data.

It gives us another way of describing the same sampled signal.

---

## 6.2 Goertzel

Goertzel is useful when we care about one particular frequency rather than an entire spectrum.

Possible uses include:

- tone detection;
- DTMF detection;
- known-frequency monitoring.

We will introduce it later when there is a practical reason to use it.

---

## 6.3 Log Power FFT

Log Power FFT combines FFT processing with logarithmic power-spectrum calculation.

It can be useful when we want spectral-power information directly.

For now, it remains a later block because we already understand the individual operations behind it.

---

# 7. Averaging and Measurement

These blocks help us turn changing sample values into useful measurements.

| Block | Importance | Status | What it does | First introduced |
|---|---|---|---|---|
| **Moving Average** | Essential | ✅ Used | Calculates an average over a moving window | Chapter 7 |
| **RMS** | Important | ⏳ Later | Estimates root-mean-square magnitude | Later |
| **Probe Signal** | Important | ⏳ Later | Allows values from a running flowgraph to be inspected programmatically | Later |

---

## 7.1 Moving Average

Moving Average calculates an average over a finite number of samples.

Conceptually,

$$
y[n]
=
\frac{1}{N}
\sum_{k=0}^{N-1}
x[n-k]
$$

where $N$ is the averaging length.

### Chapter 7 use

We first squared the signal:

$$
x^2[n]
$$

and then averaged those squared samples:

$$
P
\approx
\frac{1}{N}
\sum_{n=0}^{N-1}
x^2[n]
$$

This gave us an estimate of average signal power.

### Important distinction

Moving Average acts on the actual sample stream.

This is different from the **Averaging** option inside the QT GUI Frequency Sink, which smooths successive spectral estimates used for display.

---

# 8. Filters

Filters allow us to keep some frequency components while attenuating others.

Chapter 7 gave us our first practical use of a filter when we investigated how noise power depends on bandwidth.

| Block | Importance | Status | What it does | First introduced |
|---|---|---|---|---|
| **Low Pass Filter** | Essential | ✅ Used | Passes lower frequencies and attenuates higher frequencies | Chapter 7 |
| **High Pass Filter** | Essential | 🔜 Planned | Passes higher frequencies and attenuates lower frequencies | Chapter 9 |
| **Band Pass Filter** | Essential | 🔜 Planned | Passes a selected frequency band | Chapter 9 |
| **Band Reject Filter** | Essential | 🔜 Planned | Rejects a selected frequency band | Chapter 9 |
| **Frequency Xlating FIR Filter** | Advanced | ⏳ Later | Performs frequency translation and filtering together | Later SDR receiver chapters |
| **DC Blocker** | Important | ⏳ Later | Suppresses unwanted DC components | Later |
| **FFT Filter** | Important | ⏳ Later | Performs FIR filtering using FFT-based convolution | Later |
| **FFT Low Pass Filter** | Important | ⏳ Later | Implements low-pass filtering using FFT-based processing | Later |
| **Decimating FIR Filter** | Important | ⏳ Later | FIR filters while reducing sample rate | Later |
| **Interpolating FIR Filter** | Important | ⏳ Later | FIR filters while increasing sample rate | Later |
| **IIR Filter** | Important | ⏳ Later | Implements an infinite impulse response filter | Later |
| **Single Pole IIR Filter** | Important | ⏳ Later | Performs simple recursive smoothing/filtering | Later |
| **Hilbert** | Advanced | ⏳ Later | Produces a quadrature-related signal useful for analytic-signal processing | Later |
| **Generic Filterbank** | Advanced | ⏳ Later | Applies a bank of filters to a signal | Later |

---

## 8.1 Low Pass Filter

A low-pass filter allows frequencies near DC to pass while attenuating sufficiently high frequencies.

### Important parameters

- Decimation
- Gain
- Sample Rate
- Cutoff Frequency
- Transition Width
- Window

### Chapter 7 use

We applied a low-pass filter to Gaussian noise.

As the cutoff frequency increased, a wider portion of the noise spectrum passed through the filter.

The measured output noise power increased with that bandwidth.

This gave us direct experimental evidence that:

> **Noise power depends on how much noise bandwidth we allow into the system.**

### Watch out

A filter does not simply divide the spectrum into a perfectly passed region and a perfectly rejected region.

Real filters have a transition region.

We will study this much more carefully in the filtering chapter.

---

## 8.2 High Pass Filter

A High Pass Filter attenuates lower frequencies while allowing higher frequencies to pass.

It will become useful when we study filter selectivity in detail.

---

## 8.3 Band Pass Filter

A Band Pass Filter allows only a selected frequency region to pass.

This is especially important for channel selection in SDR.

---

## 8.4 Band Reject Filter

A Band Reject Filter attenuates a selected frequency band while allowing frequencies outside that region to pass.

A very narrow rejected band is commonly called a **notch**.

---

## 8.5 DC Blocker

Real SDR receivers can contain an unwanted component around zero frequency.

The DC Blocker suppresses this component.

Its purpose will become more meaningful once we work with real SDR hardware and baseband signals.

---

## 8.6 FFT Filter

FFT Filter implements FIR filtering using FFT-based convolution.

This connects two concepts:

- convolution;
- Fourier transforms.

We will return to it after ordinary FIR filtering is understood.

---

## 8.7 Hilbert

The Hilbert block is closely related to:

- analytic signals;
- quadrature signals;
- I/Q processing;
- single-sideband modulation.

We will introduce it when there is a clear experiment that makes its role intuitive.

---

# 9. Filter-Tap Design Blocks

GNU Radio also provides blocks for generating **filter taps**.

Filter taps are FIR-filter coefficients.

| Block | Importance | Status | What it does |
|---|---|---|---|
| **Low-pass Filter Taps** | Important | ⏳ Later | Generates low-pass FIR coefficients |
| **High-pass Filter Taps** | Important | ⏳ Later | Generates high-pass FIR coefficients |
| **Band-pass Filter Taps** | Important | ⏳ Later | Generates band-pass FIR coefficients |
| **Band-reject Filter Taps** | Important | ⏳ Later | Generates band-reject FIR coefficients |
| **RRC Filter Taps** | Important | ⏳ Later | Generates root-raised-cosine filter coefficients |
| **Filter Taps Loader** | Advanced | ⏳ Later | Loads externally defined filter taps |

A useful relationship to keep in mind for later is:

```text
Filter specification
        ↓
Filter taps
        ↓
Convolution
        ↓
Filtered output
```

---

# 10. Root-Raised-Cosine Filtering

Two important blocks that will appear later are:

- **Root Raised Cosine Filter**
- **RRC Filter Taps**

Root-raised-cosine filtering becomes important in digital communication systems.

It is commonly used for:

- pulse shaping;
- bandwidth control;
- reducing intersymbol interference.

Introducing these blocks before we begin transmitting symbols would be premature, so they remain part of the later communication chapters.

---

# 11. QT GUI Visualization

These blocks allow us to observe what is happening inside a running flowgraph.

Different sinks answer different questions about the same signal.

| Block | Importance | Status | What it does | First introduced |
|---|---|---|---|---|
| **QT GUI Time Sink** | Essential | ✅ Used | Displays sample amplitude versus time | Earlier chapters |
| **QT GUI Frequency Sink** | Essential | ✅ Used | Displays the spectrum of a signal | Earlier frequency-domain chapters |
| **QT GUI Constellation Sink** | Essential | ✅ Used | Displays complex samples on the I/Q plane | Earlier I/Q chapters |
| **QT GUI Number Sink** | Important | ✅ Used | Displays numerical values or measurements | Chapter 7 |
| **QT GUI Vector Sink** | Important | ✅ Used | Displays vector values such as explicit FFT-bin outputs | Chapter 6 |
| **QT GUI Waterfall Sink** | Important | ⏳ Later | Displays how the spectrum changes over time | Later |
| **QT GUI Histogram Sink** | Important | ⏳ Later | Displays the statistical distribution of sample values | Later |
| **QT GUI Eye Sink** | Important | ⏳ Later | Displays an eye diagram | Later digital communications |
| **QT GUI Matrix Sink** | Specialized | ➖ Optional | Displays matrix-like data | Optional |

---

## 11.1 QT GUI Time Sink

The Time Sink displays signal amplitude against time.

It helps us inspect:

- waveform shape;
- amplitude;
- period;
- relative phase;
- distortion;
- time-domain noise.

---

## 11.2 QT GUI Frequency Sink

The Frequency Sink displays a spectral estimate of the input signal.

It helps us inspect:

- spectral peaks;
- positive and negative frequencies;
- noise floor;
- occupied bandwidth;
- spectral leakage;
- filter behaviour.

### Important settings

- Type
- FFT Size
- Window
- Center Frequency
- Bandwidth
- Averaging
- Y-axis range

### Important distinction

The Frequency Sink uses FFT processing internally for display.

That does not mean every flowgraph containing a Frequency Sink contains an explicit FFT block in the signal path.

---

## 11.3 QT GUI Constellation Sink

The Constellation Sink displays complex samples on the I/Q plane.

It helps us understand complex samples geometrically rather than only as separate I and Q waveforms.

Later it will become especially useful for:

- BPSK;
- QPSK;
- QAM;
- noise;
- phase error;
- synchronization.

---

## 11.4 QT GUI Number Sink

The Number Sink displays numerical values from a running flowgraph.

### Chapter 7 use

We used it to display:

- signal power;
- noise power;
- SNR in dB;
- filtered noise power.

It is useful when the quantity we care about is a number rather than a waveform.

---

## 11.5 QT GUI Vector Sink

The Vector Sink displays vector-valued data.

### Chapter 6 use

It allowed us to inspect explicit FFT-bin values after:

```text
Stream to Vector
        ↓
FFT
        ↓
Complex to Mag²
        ↓
QT GUI Vector Sink
```

This helped distinguish between:

> **displaying a spectrum**

and

> **processing the FFT output ourselves**.

---

# 12. QT GUI Controls

QT GUI controls allow us to change flowgraph parameters while the flowgraph is running.

This turns a static experiment into an interactive one.

| Block | Importance | Status | What it does | First introduced |
|---|---|---|---|---|
| **QT GUI Range** | Essential | ✅ Used | Provides an interactive numerical slider/control | Earlier interactive experiments |
| **QT GUI Chooser** | Important | ✅ Used | Allows selection from predefined values | Earlier experiments |
| **QT GUI Push Button** | Important | ⏳ Later | Provides a clickable runtime control | Later |
| **QT GUI Entry** | Important | ⏳ Later | Allows values to be entered at runtime | Later |
| **QT GUI Check Box** | Important | ⏳ Later | Provides a Boolean runtime control | Later |

---

## 12.1 QT GUI Range

QT GUI Range allows a numerical parameter to be changed while the flowgraph is running.

Typical settings include:

- ID
- Label
- Default Value
- Start
- Stop
- Step

### Why it matters

Instead of stopping the flowgraph, editing a parameter, and running it again, we can change the value interactively and immediately observe the effect.

We have used this approach for parameters such as:

- signal frequency;
- sample rate;
- noise amplitude;
- filter cutoff frequency.

---

## 12.2 QT GUI Chooser

QT GUI Chooser allows the user to select one value from a predefined set.

For example:

```text
0.1
0.5
1.0
2.0
```

### Range versus Chooser

Use **QT GUI Range** when a parameter should move through a numerical interval.

Use **QT GUI Chooser** when the experiment should use a small number of specific predefined values.

---

# 13. Resampling and Rate Change

These blocks change the rate at which samples appear in a signal stream.

We will study them properly later.

| Block | Importance | Status | What it does | First introduced |
|---|---|---|---|---|
| **Decimating FIR Filter** | Essential | ⏳ Later | Filters while reducing sample rate | Later |
| **Interpolating FIR Filter** | Essential | ⏳ Later | Filters while increasing sample rate | Later |
| **Rational Resampler** | Essential | ⏳ Later | Changes sample rate by a rational factor | Later |
| **Fractional Resampler** | Advanced | ⏳ Later | Performs non-integer sample-rate conversion | Later |
| **Repeat** | Important | ⏳ Later | Repeats samples | Later |
| **Keep 1 in N** | Important | ⏳ Later | Keeps one sample out of every N | Later |

---

# 14. Modulation and Demodulation

These blocks will become important when we begin transmitting information rather than only studying test signals.

| Block | Importance | Status |
|---|---|---|
| **Frequency Mod** | Essential | ⏳ Later |
| **Quadrature Demod** | Essential | ⏳ Later |
| **NBFM Transmit** | Important | ⏳ Later |
| **NBFM Receive** | Important | ⏳ Later |
| **WBFM Transmit** | Important | ⏳ Later |
| **WBFM Receive** | Important | ⏳ Later |
| **AM Demod** | Important | ⏳ Later |
| **Constellation Modulator** | Important | ⏳ Later |
| **Constellation Decoder** | Important | ⏳ Later |

---

# 15. Digital Communication Blocks

These blocks become useful once the book begins working with bits, symbols, pulse shaping, and digital receivers.

| Block | Importance | Status |
|---|---|---|
| **Chunks to Symbols** | Essential | ⏳ Later |
| **Map** | Important | ⏳ Later |
| **Unpacked to Packed** | Important | ⏳ Later |
| **Packed to Unpacked** | Important | ⏳ Later |
| **Differential Encoder** | Important | ⏳ Later |
| **Differential Decoder** | Important | ⏳ Later |
| **Binary Slicer** | Essential | ⏳ Later |
| **Correlate Access Code** | Important | ⏳ Later |
| **Additive Scrambler** | Important | ⏳ Later |

---

# 16. Synchronization

Synchronization blocks become necessary when the receiver must recover timing and carrier information from a received signal.

| Block | Importance | Status |
|---|---|---|
| **Symbol Sync** | Essential | ⏳ Later |
| **Clock Recovery MM** | Important | ⏳ Later |
| **Costas Loop** | Essential | ⏳ Later |
| **PLL Carrier Tracking** | Important | ⏳ Later |
| **PLL Frequency Detector** | Advanced | ⏳ Later |
| **FLL Band-Edge** | Advanced | ⏳ Later |

---

# 17. Channel and Impairment Simulation

These blocks allow us to deliberately make signals less ideal.

| Block | Importance | Status |
|---|---|---|
| **Channel Model** | Essential | ⏳ Later |
| **Dynamic Channel Model** | Advanced | ⏳ Later |
| **Frequency Selective Fading Model** | Advanced | ⏳ Later |
| **Selective Fading Model** | Advanced | ⏳ Later |

These will eventually allow us to investigate:

- noise;
- frequency offset;
- timing offset;
- multipath;
- fading;
- receiver robustness.

---

# 18. File and Data Storage

| Block | Importance | Status |
|---|---|---|
| **File Source** | Essential | ⏳ Later |
| **File Sink** | Essential | ⏳ Later |
| **WAV File Source** | Important | ⏳ Later |
| **WAV File Sink** | Important | ⏳ Later |
| **Metadata File Source** | Advanced | ⏳ Later |
| **Metadata File Sink** | Advanced | ⏳ Later |

These blocks will become useful when we start recording and replaying signals.

---

# 19. Message and PDU Processing

GNU Radio is not limited to continuous sample streams.

Later we will work with messages, metadata, packets, and PDUs.

| Block | Importance | Status |
|---|---|---|
| **Message Debug** | Important | ⏳ Later |
| **Tagged Stream to PDU** | Advanced | ⏳ Later |
| **PDU to Tagged Stream** | Advanced | ⏳ Later |
| **Socket PDU** | Advanced | ⏳ Later |

---

# 20. SDR Hardware Interfaces

Eventually our samples will come from real RF hardware rather than Signal Source.

| Block / Interface | Importance | Status |
|---|---|---|
| **Osmocom Source** | Important | ⏳ Later |
| **Osmocom Sink** | Important | ⏳ Later |
| **UHD: USRP Source** | Important | ⏳ Later |
| **UHD: USRP Sink** | Important | ⏳ Later |
| **Soapy Source** | Important | ⏳ Later |
| **Soapy Sink** | Important | ⏳ Later |
| **PlutoSDR Source** | Important | ⏳ Later |
| **PlutoSDR Sink** | Important | ⏳ Later |

The exact hardware interface used later will depend on the SDR hardware available for the experiments.

---

# 21. Custom and Advanced Processing

| Block / Feature | Importance | Status |
|---|---|---|
| **Embedded Python Block** | Important | ⏳ Later |
| **Hierarchical Block** | Important | ⏳ Later |
| **Stream Tags** | Essential | ⏳ Later |
| **Tagged Streams** | Essential | ⏳ Later |
| **PDUs** | Important | ⏳ Later |

These become useful once our flowgraphs grow beyond small experiments.

---

# 22. Similar-Looking Blocks Are Not Necessarily the Same

One reason GNU Radio can initially feel overwhelming is that several blocks may appear to perform almost the same job.

For example:

```text
Low Pass Filter
Low-pass Filter Taps
FFT Low Pass Filter
Decimating FIR Filter
```

These are not simply four different names for the same operation.

They represent different levels or implementations of filtering.

The **Low Pass Filter** is a convenient complete filter.

The **Low-pass Filter Taps** block generates coefficients that can be used elsewhere.

The **FFT Low Pass Filter** performs the filtering using an FFT-based implementation.

The **Decimating FIR Filter** combines filtering with sample-rate reduction.

This gives us an important rule:

> **We do not need to learn every similar-looking block at the same time.**

We will first learn the underlying DSP concept using the clearest block.

Once the concept is understood, alternative implementations become much easier to understand.

---

# 23. Blocks We Have Used So Far

At the end of Chapter 7, the core GNU Radio toolbox we have actually worked with includes:

| Block / Feature | Status |
|---|---|
| Signal Source | ✅ |
| Noise Source | ✅ |
| Throttle | ✅ |
| Variable | ✅ |
| Add | ✅ |
| Multiply | ✅ |
| Divide | ✅ |
| Log10 | ✅ |
| Multiply Const | ✅ |
| Float to Complex | ✅ |
| Complex to Real | ✅ |
| Complex to Imag | ✅ |
| Complex to Mag | ✅ |
| Complex to Mag² | ✅ |
| Complex to Arg | ✅ |
| Stream to Vector | ✅ |
| FFT | ✅ |
| Moving Average | ✅ |
| Low Pass Filter | ✅ |
| QT GUI Time Sink | ✅ |
| QT GUI Frequency Sink | ✅ |
| QT GUI Constellation Sink | ✅ |
| QT GUI Vector Sink | ✅ |
| QT GUI Number Sink | ✅ |
| QT GUI Range | ✅ |
| QT GUI Chooser | ✅ |

This is already enough to build much more than the small flowgraphs we started with.

More importantly, we are beginning to think about these blocks as **operations**, not simply names to memorize.

For example:

```text
Need to observe a waveform
        ↓
QT GUI Time Sink
```

```text
Need to inspect frequency content
        ↓
QT GUI Frequency Sink
```

```text
Need average power
        ↓
Square the samples
        ↓
Moving Average
```

```text
Need SNR
        ↓
Measure signal power and noise power
        ↓
Divide
        ↓
Log10
        ↓
Multiply by 10
```

```text
Need to restrict noise bandwidth
        ↓
Low Pass Filter
```

That way of thinking is more important than memorizing the block library.

---

# 24. What Comes Next?

The next major topic is **mixing and frequency translation**.

This will build naturally on several things we already understand:

- real and complex signals;
- positive and negative frequencies;
- multiplication;
- frequency-domain observation;
- runtime parameter control.

The important question will no longer be simply:

> **What frequencies are present?**

It will become:

> **How can we deliberately move a signal from one part of the spectrum to another?**

After mixing, we will study filtering in much greater depth.

That will bring together:

- cutoff frequency;
- passband;
- stopband;
- transition width;
- filter order;
- FIR filters;
- filter windows;
- channel selection;
- decimation.

---

# 25. Rule for Updating This Document

Whenever a new GNU Radio block becomes part of the book:

1. Introduce it naturally when the signal-processing problem requires it.
2. Explain it in the chapter's **GNU Radio Toolbox** if it is important enough to deserve a focused introduction.
3. Use it in a real experiment.
4. Add or update it in this Master List.
5. Mark its status as **Used** only after the corresponding experiment has actually been completed.
6. Record where it was first introduced.
7. Reuse it in later chapters without repeatedly teaching it from the beginning.

The goal is not to collect GNU Radio blocks.

The goal is to gradually reach the point where we can look at a signal-processing problem and decide:

> **What operation needs to happen to this signal?**

Only then should we ask:

> **Which GNU Radio block performs that operation?**

---

## Final Note

This is a **living document**.

As we progress through the GNU Radio experiments:

- new blocks will be added;
- statuses will change;
- first-introduction references will become more precise;
- some blocks may be reclassified;
- practical notes from real experiments can be added.

The purpose is not to memorize GNU Radio's block library.

The purpose is to know:

> **Which block should I reach for when I want to perform a particular DSP or SDR operation, and why?**