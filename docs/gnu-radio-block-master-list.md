# GNU Radio Block Master List

**Updated through Chapter 14: Frequency Modulation**

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

A block should only be marked **Used** after it has actually appeared in a completed experiment.

---

# 1. Signal and Data Sources

Source blocks create data that enters a flowgraph.

| Block | Importance | Status | What it does | First introduced / major use |
|---|---|---|---|---|
| **Signal Source** | Essential | ✅ Used | Generates periodic signals such as sine and cosine waves | Earlier chapters |
| **Noise Source** | Essential | ✅ Used | Generates random noise such as Gaussian noise | Chapter 7; reused Chapter 14 |
| **Constant Source** | Important | ✅ Used | Produces a constant-valued stream | Chapter 13 |
| **Vector Source** | Important | ✅ Used | Produces a predefined sequence of values | Chapter 10 |
| **VCO** | Important | ✅ Used | Generates a frequency-controlled oscillator | Chapter 14 |
| **VCO (Complex)** | Important | ✅ Used | Generates a complex frequency-controlled oscillator | Chapter 14 |
| **Fast Noise Source** | Important | ⏳ Later | Efficient noise generation | Later |
| **Random Source** | Important | 🔜 Planned | Generates random digital values | Digital communication chapters |
| **Random Uniform Source** | Important | ⏳ Later | Generates uniformly distributed random values | Later |
| **GLFSR Source** | Important | ⏳ Later | Generates pseudo-random sequences | Later digital communications |
| **File Source** | Important | ⏳ Later | Reads stored samples | Later |

---

## 1.1 Signal Source

Signal Source remains one of the main laboratory tools in the book.

It is useful when we want a signal whose properties are completely known before the experiment begins.

Important settings include:

- Output Type
- Sample Rate
- Waveform
- Frequency
- Amplitude
- Offset
- Initial Phase

It has been reused for:

- waveform fundamentals;
- sampling;
- I/Q;
- FFT experiments;
- mixing;
- filtering;
- modulation;
- correlation test signals.

### Watch out

Signal Source generates **digital samples inside GNU Radio**. It does not directly create a physical RF voltage at an antenna connector.

---

## 1.2 Noise Source

Noise Source generates random samples according to a selected distribution.

Important parameters include:

- Output Type
- Noise Type
- Amplitude
- Seed

It was first used to study:

- noise;
- power;
- SNR;
- noise bandwidth.

In Chapter 14 it was reused in a new way: a **complex Gaussian Noise Source** was added directly to an FM signal to simulate additive channel noise.

That experiment reinforced an important distinction:

```text
Multiplicative amplitude variation
        ≠
Additive complex channel noise
```

The second can disturb both magnitude and phase.

---

## 1.3 Constant Source

Constant Source produces the same value continuously.

In Chapter 13 it was useful when numerical quantities such as AM power percentages were sent to a QT GUI Number Sink.

Typical uses include:

- DC values;
- fixed control streams;
- numerical displays;
- testing.

---

## 1.4 Vector Source

Vector Source produces samples from a predefined list.

For example:

```text
(1, 0, 0, 0)
```

Chapter 10 used it extensively for:

- impulses;
- delayed impulses;
- scaled impulses;
- short finite sequences;
- convolution experiments.

This was an important transition from continuously generated sinusoids to deliberately constructed discrete-time sequences.

---

## 1.5 VCO

VCO stands for **Voltage-Controlled Oscillator**.

In GNU Radio, the input controls the oscillator's phase rate and therefore its instantaneous frequency.

Chapter 14 used the VCO to build FM from first principles.

Conceptually:

```text
Control input
     ↓
Phase rotates faster or slower
     ↓
Instantaneous frequency changes
```

This made the physical meaning of FM visible before using any all-in-one FM transmitter block.

---

## 1.6 VCO (Complex)

The complex VCO produces a rotating complex phasor rather than only a real cosine.

A useful representation is:

$$
x(t)=Ae^{j\phi(t)}
$$

Chapter 14 used the complex VCO because the Quadrature Demod block needs a complex signal whose phase evolution can be measured directly.

Important settings used:

```text
Sample Rate: samp_rate
Sensitivity: 2*pi
Amplitude: 1
```

Using:

```text
from math import pi
```

allowed `2*pi` to be entered directly instead of typing a decimal approximation.

---

# 2. Flow Control and Flowgraph Utilities

| Block / Object | Importance | Status | What it does | First introduced / major use |
|---|---|---|---|---|
| **Throttle** | Essential | ✅ Used | Limits processing rate in software-only flowgraphs | Earlier chapters |
| **Variable** | Essential | ✅ Used | Stores reusable values | Earlier chapters |
| **Import** | Important | ✅ Used | Makes Python names/functions available to generated flowgraph code | Chapter 14 |
| **Head** | Important | ✅ Used | Passes only a selected number of items | Chapter 10/11 finite-sequence work |

---

## 2.1 Throttle

Throttle limits the rate at which a software-only flowgraph processes samples.

A useful rule remains:

> If no hardware device or other real-time sink/source controls the rate, a Throttle block is often needed.

Throttle does **not** perform sampling. The signal is already represented by samples.

---

## 2.2 Variable

Variables keep important parameters consistent across a flowgraph.

Examples include:

```text
samp_rate
fc
fm
freq_dev
```

As the book progresses, variables increasingly describe relationships instead of isolated numbers.

For example:

```text
1.0/freq_dev
```

lets a demodulator automatically remain correctly normalized when the deviation changes.

---

## 2.3 Import

The Import object lets GNU Radio's generated Python code use external Python names.

Chapter 14 used:

```python
from math import pi
```

This allowed expressions such as:

```text
2*pi
```

inside VCO and Quadrature Demod settings.

### Why it matters

Expressions are usually clearer than unexplained decimal constants.

For example:

```text
2*pi
```

communicates the conversion between cycles and radians immediately.

---

## 2.4 Head

Head allows only a specified number of items to pass.

It is useful when an experiment should work with a finite observation rather than an endless stream.

This became relevant once the book moved from continuous sinusoidal experiments toward short sequences, convolution, and detection.

---

# 3. Mathematical Operations

| Block | Importance | Status | What it does | First introduced / major use |
|---|---|---|---|---|
| **Add** | Essential | ✅ Used | Adds streams sample by sample | Earlier chapters |
| **Multiply** | Essential | ✅ Used | Multiplies streams sample by sample | Chapters 7–14 |
| **Divide** | Important | ✅ Used | Divides one stream by another | Chapter 7 |
| **Multiply Const** | Essential | ✅ Used | Scales every sample by a constant | Chapter 7; reused Chapter 14 |
| **Add Const** | Important | ✅ Used | Adds a constant to every sample | Chapter 11; reused Chapters 13–14 |
| **Log10** | Important | ✅ Used | Calculates base-10 logarithm | Chapter 7 |
| **Abs** | Important | ✅ Used | Calculates absolute value | Chapter 13 |
| **Subtract** | Important | ⏳ Later | Subtracts streams | Later |

---

## 3.1 Add

For two streams:

$$
z[n]=x[n]+y[n]
$$

Important uses have included:

- adding signal and noise;
- building multi-tone test signals;
- combining modulation branches;
- adding complex channel noise to FM.

Chapter 14's additive-noise experiment used:

$$
r(t)=s_{\mathrm{FM}}(t)+n(t)
$$

This was deliberately different from multiplying the FM signal by a varying amplitude.

---

## 3.2 Multiply

Multiply performs sample-by-sample multiplication:

$$
z[n]=x[n]y[n]
$$

It has taken on several different roles:

- squaring a real signal for power measurement;
- mixing;
- modulation;
- applying multiplicative amplitude disturbance.

This is a good example of why the book focuses on **operations**, not memorized block recipes.

---

## 3.3 Multiply Const

Multiply Const scales a signal by a fixed or variable-controlled value.

Chapter 14 used it for several conceptually meaningful operations:

```text
Message × freq_dev
```

to convert a normalized message into frequency deviation, and:

```text
Demodulated deviation × (1/freq_dev)
```

to recover a normalized message.

---

## 3.4 Add Const

Add Const became important in Chapter 11 for threshold detection.

To test:

$$
y[n]>8
$$

we used:

```text
Add Const = -8
```

before a Binary Slicer.

It was later reused in modulation work.

For FM:

```text
+fc
```

created the desired instantaneous-frequency control:

$$
f_i(t)=f_c+\Delta f\,m(t)
$$

At the receiver:

```text
-fc
```

removed the carrier-frequency offset.

---

## 3.5 Abs

Abs outputs the absolute value of each real sample.

Chapter 13 used it as the first stage of a simple AM envelope detector:

```text
AM signal
   ↓
Abs
   ↓
Low Pass Filter
   ↓
DC Blocker
```

The experiment also showed why rectification alone does not recover a clean message.

---

# 4. Complex-Signal and Type-Conversion Blocks

| Block | Importance | Status | What it does | First introduced / major use |
|---|---|---|---|---|
| **Float to Complex** | Essential | ✅ Used | Combines float streams into a complex stream | Earlier I/Q chapters; reused Chapter 14 |
| **Complex to Real** | Essential | ✅ Used | Extracts real/I component | Earlier I/Q chapters |
| **Complex to Imag** | Essential | ✅ Used | Extracts imaginary/Q component | Earlier I/Q chapters |
| **Complex to Mag** | Essential | ✅ Used | Calculates complex magnitude | Earlier I/Q chapters; reused Chapter 14 |
| **Complex to Arg** | Essential | ✅ Used | Calculates complex phase | Earlier I/Q chapters |
| **Complex to Mag²** | Essential | ✅ Used | Calculates squared complex magnitude | Chapter 6 |
| **Char to Float** | Important | ✅ Used | Converts byte/char samples to float | Chapter 11 |
| **Complex to Float** | Important | ⏳ Later | Separates complex data into float components | Later |
| **Float to Char** | Important | ⏳ Later | Converts float values to byte/char representation | Later |

---

## 4.1 Float to Complex

Float to Complex forms:

$$
z[n]=I[n]+jQ[n]
$$

Chapter 14 reused it in the controlled amplitude-disturbance experiment.

A real amplitude-control stream was converted to a complex stream with zero imaginary component so it could multiply the complex FM signal without intentionally adding phase rotation.

---

## 4.2 Complex to Mag

Complex to Mag calculates:

$$
|z[n]|=\sqrt{I^2[n]+Q^2[n]}
$$

Chapter 14 gave this familiar block a new role.

It allowed us to see the difference between:

- ideal constant-envelope FM;
- multiplicative amplitude variation;
- additive complex noise.

The magnitude display was especially useful because the recovered message could remain clean even when magnitude varied strongly, provided the phase trajectory was preserved.

---

## 4.3 Char to Float

Binary Slicer produces byte/char output.

Chapter 11 used Char to Float so the binary detector output could be displayed alongside floating-point matched-filter data.

Conceptually:

```text
0 -> 0.0
1 -> 1.0
```

It changes representation, not the detection decision.

---

# 5. Stream and Vector Operations

| Block | Importance | Status | What it does | First introduced / major use |
|---|---|---|---|---|
| **Stream to Vector** | Essential | ✅ Used | Groups stream samples into vectors | Chapter 6 |
| **Keep 1 in N** | Important | ✅ Used | Keeps one item out of every N | Chapter 9 |
| **Head** | Important | ✅ Used | Limits a stream to a finite number of items | Chapter 10/11 |
| **Delay** | Important | ✅ Used | Delays a signal by a chosen number of samples | Chapter 11 |
| **Vector to Stream** | Essential | ⏳ Later | Converts vectors to streams | Later OFDM/vector work |
| **Repeat** | Important | ⏳ Later / optional | Repeats samples/items | Later if required |

---

## 5.1 Delay

Delay shifts a stream by a specified number of samples.

It became useful in correlation and detection because known delays let us test whether a correlation peak appears at the expected position.

Delay is a simple block, but it represents a major receiver concept:

```text
Known waveform
     ↓
Channel / propagation delay
     ↓
Receiver searches for shifted match
```

---

# 6. Fourier and Spectrum Analysis

| Block | Importance | Status | What it does | First introduced |
|---|---|---|---|---|
| **FFT** | Essential | ✅ Used | Computes the DFT efficiently | Chapter 6 |
| **IFFT** | Essential | ⏳ Later | Creates time-domain data from frequency-domain bins | OFDM chapters |
| **Goertzel** | Important | ⏳ Later | Evaluates selected frequencies efficiently | Later |
| **Log Power FFT** | Important | ⏳ Later | Produces logarithmic spectral power | Later |

The FFT and Frequency Sink have now been reused to inspect:

- real and complex tones;
- leakage;
- noise;
- mixing;
- filtering;
- AM;
- DSB-SC;
- SSB;
- FM sidebands;
- FM bandwidth.

---

# 7. Averaging and Measurement

| Block | Importance | Status | What it does | First introduced |
|---|---|---|---|---|
| **Moving Average** | Essential | ✅ Used | Averages over a moving window | Chapter 7 |
| **RMS** | Important | ⏳ Later | Estimates root-mean-square magnitude | Later |
| **Probe Signal** | Important | ⏳ Later | Exposes live values programmatically | Later |

Moving Average was first used for power estimation and later helped connect accumulation operations with correlation-style processing.

---

# 8. Filters

| Block | Importance | Status | What it does | First introduced / major use |
|---|---|---|---|---|
| **Low Pass Filter** | Essential | ✅ Used | Passes lower frequencies | Chapter 7; expanded Chapter 9 |
| **High Pass Filter** | Essential | ✅ Used | Passes higher frequencies | Chapter 9 |
| **Band Pass Filter** | Essential | ✅ Used | Passes a selected band | Chapter 9; reused Chapter 13 |
| **Band Reject Filter** | Essential | ✅ Used | Rejects a selected band | Chapter 9 |
| **Decimating FIR Filter** | Essential | ✅ Used | FIR filtering with optional decimation | Chapters 9–11 |
| **DC Blocker** | Important | ✅ Used | Removes DC/very-low-frequency offset | Chapter 13 |
| **Frequency Xlating FIR Filter** | Advanced | ⏳ Later | Frequency translation + filtering + decimation | Real receiver chapter |
| **FFT Filter** | Important | ⏳ Later | FIR filtering using FFT convolution | Later |
| **FFT Low Pass Filter** | Important | ⏳ Later | FFT-based low-pass filtering | Later |
| **Interpolating FIR Filter** | Important | ⏳ Later | FIR filtering while increasing sample rate | Later |
| **IIR Filter** | Important | ⏳ Later | Infinite impulse response filtering | Later |
| **Single Pole IIR Filter** | Important | ⏳ Later | Simple recursive filtering/smoothing | Later |
| **Hilbert** | Advanced | ⏳ Later | Produces quadrature/analytic-signal processing | Discussed Chapter 13, not used |
| **Generic Filterbank** | Advanced | ⏳ Later | Applies a bank of filters | Later |

---

## 8.1 Band Pass Filter Reuse in SSB

Band Pass Filter was first learned as a channel-selection tool.

Chapter 13 reused the same operation to build SSB from DSB-SC.

Conceptually:

```text
DSB-SC
  ↓
Band Pass Filter
  ↓
One sideband retained
```

The experiment also showed that practical sideband suppression depends on transition width and window choice.

---

## 8.2 DC Blocker

Chapter 13 used DC Blocker after envelope detection.

The rectified and low-pass-filtered AM signal contained a DC component. The DC Blocker removed that offset so the recovered message could be centered around zero.

Important settings used:

```text
Length: 32
Long Form: True
```

This gave the block a concrete role before its later use in real SDR baseband receivers.

---

# 9. Filter-Tap Design Blocks

| Block | Importance | Status | What it does | First introduced |
|---|---|---|---|---|
| **Low-pass Filter Taps** | Important | ✅ Used | Generates low-pass FIR coefficients | Chapter 9 |
| **High-pass Filter Taps** | Important | ⏳ Later | Generates high-pass FIR coefficients | Later |
| **Band-pass Filter Taps** | Important | ⏳ Later | Generates band-pass FIR coefficients | Later |
| **Band-reject Filter Taps** | Important | ⏳ Later | Generates band-reject FIR coefficients | Later |
| **RRC Filter Taps** | Important | ⏳ Later | Generates root-raised-cosine taps | Digital communications |
| **Filter Taps Loader** | Advanced | ⏳ Later | Loads externally defined taps | Later |

The key connection established by Chapters 9 and 10 is:

```text
Filter taps
    =
FIR impulse response
    ↓
Convolution with input
    ↓
Filtered output
```

---

# 10. Correlation, Matched Filtering and Detection

Chapter 11 turned familiar FIR operations into a receiver detector.

| Block / Operation | Importance | Status | Role |
|---|---|---|---|
| **Decimating FIR Filter** | Essential | ✅ Used | Implements correlation/matched filtering through selected taps |
| **Add Const** | Important | ✅ Used | Moves a detection threshold to zero |
| **Binary Slicer** | Essential | ✅ Used | Converts thresholded values into binary decisions |
| **Char to Float** | Important | ✅ Used | Converts decisions for float-domain visualization |
| **Delay** | Important | ✅ Used | Introduces/represents sample delay |
| **Moving Average** | Essential | ✅ Used | Accumulation/smoothing where useful |
| **Conjugate** | Important | Concept introduced | Required for general complex correlation |
| **Correlate Access Code** | Important | ⏳ Later | Detects known bit patterns in digital streams |

---

## 10.1 Binary Slicer

Binary Slicer makes a binary decision around zero.

In Chapter 11 we wanted to test:

$$
y[n]>8
$$

so we first used:

```text
Add Const = -8
```

and then passed the shifted signal to Binary Slicer.

Conceptually:

```text
Matched Filter
      ↓
Subtract threshold
      ↓
Binary Slicer
      ↓
0 or 1
```

This was the point where a similarity measurement became an actual detector decision.

---

# 11. QT GUI Visualization

| Block | Importance | Status | Main use |
|---|---|---|---|
| **QT GUI Time Sink** | Essential | ✅ Used | Time-domain waveform inspection |
| **QT GUI Frequency Sink** | Essential | ✅ Used | Spectrum inspection |
| **QT GUI Constellation Sink** | Essential | ✅ Used | I/Q-plane inspection |
| **QT GUI Number Sink** | Important | ✅ Used | Numerical measurement display |
| **QT GUI Vector Sink** | Important | ✅ Used | Vector-valued display |
| **QT GUI Waterfall Sink** | Important | ✅ Used | Spectrum-versus-time display |
| **QT GUI Histogram Sink** | Important | ⏳ Later | Sample distribution |
| **QT GUI Eye Sink** | Important | ⏳ Later | Eye diagram |
| **QT GUI Matrix Sink** | Specialized | ➖ Optional | Matrix-like data |

---

## 11.1 QT GUI Number Sink

The Number Sink was first used for numerical measurements such as power and SNR.

Chapter 13 reused it to display:

- carrier power percentage;
- LSB power percentage;
- USB power percentage;
- total sideband power percentage.

This was a good reminder that a Frequency Sink is excellent for spectral structure but is not automatically the right tool for reporting exact engineering percentages.

---

## 11.2 QT GUI Frequency Sink in Modulation Chapters

The Frequency Sink became central to Chapters 12–14.

It was used to inspect:

- baseband and translated spectra;
- AM carrier and sidebands;
- DSB-SC;
- SSB-SC;
- FM sideband spacing;
- FM spectral spreading;
- narrowband FM.

The FM experiments also reinforced an important display lesson:

> Changing a Frequency Sink's center-frequency label does not itself frequency-shift the incoming signal.

Signal processing and display labeling are different operations.

---

# 12. QT GUI Controls

| Block | Importance | Status | What it does |
|---|---|---|---|
| **QT GUI Range** | Essential | ✅ Used | Interactive numerical control |
| **QT GUI Chooser** | Important | ✅ Used | Selects predefined values |
| **QT GUI Push Button** | Important | ⏳ Later | Clickable runtime action |
| **QT GUI Entry** | Important | ⏳ Later | Runtime numerical/text entry |
| **QT GUI Check Box** | Important | ⏳ Later | Boolean control |

Chapter 14 made heavy use of QT GUI Range for:

```text
Frequency Deviation (Hz)
Message Frequency (Hz)
FM Amplitude Scale
Amplitude Noise Level
Channel Noise Amplitude
```

The ranges allowed us to keep the flowgraph fixed while changing one physical property at a time.

---

# 13. Resampling and Rate Change

| Block | Importance | Status | What it does |
|---|---|---|---|
| **Decimating FIR Filter** | Essential | ✅ Used | Filters while reducing sample rate |
| **Keep 1 in N** | Important | ✅ Used | Direct downsampling without anti-alias filtering |
| **Interpolating FIR Filter** | Essential | ⏳ Later | Filters while increasing sample rate |
| **Rational Resampler** | Essential | ⏳ Later | Rational sample-rate conversion |
| **Fractional Resampler** | Advanced | ⏳ Later | Non-integer resampling |
| **Repeat** | Important | ⏳ Later | Repeats items |

Although the original chapter plan considered introducing Rational Resampler during FM, the experimentally developed Chapter 14 focused on FM fundamentals first.

Audio-rate conversion and practical broadcast-FM resampling remain available for the later real-radio receiver chapter, where multiple hardware/audio sample rates will have a concrete purpose.

---

# 14. Modulation and Demodulation

| Block / Method | Importance | Status | First use / note |
|---|---|---|---|
| **Manual AM chain using Add/Multiply** | Essential concept | ✅ Used | Chapters 12–13 |
| **Abs + LPF + DC Blocker envelope detector** | Important | ✅ Used | Chapter 13 |
| **Band Pass Filter SSB method** | Important | ✅ Used | Chapter 13 |
| **VCO** | Important | ✅ Used | Chapter 14 |
| **VCO (Complex)** | Important | ✅ Used | Chapter 14 |
| **Quadrature Demod** | Essential | ✅ Used | Chapter 14 |
| **Frequency Mod** | Essential | ⏳ Later / convenience block | Underlying FM operation already understood |
| **NBFM Transmit** | Important | ⏳ Later / optional | Convenience block |
| **NBFM Receive** | Important | ⏳ Later / optional | Convenience block |
| **WBFM Transmit** | Important | ⏳ Later / optional | Convenience block |
| **WBFM Receive** | Important | ⏳ Later / practical receiver | Convenience block |
| **AM Demod** | Important | ⏳ Later / convenience block | Manual AM demodulation already understood |
| **Constellation Modulator** | Important | ⏳ Later | Digital modulation |
| **Constellation Decoder** | Important | ⏳ Later | Digital demodulation |

---

## 14.1 Why We Did Not Start with Convenience Modulation Blocks

The book deliberately built AM and FM from simpler operations.

For AM:

```text
Message
   ↓
Scaling / DC term
   ↓
Multiply by carrier
```

For FM:

```text
Message
   ↓
Scale by frequency deviation
   ↓
Add center-frequency term
   ↓
VCO
```

This keeps the signal-processing idea visible.

Convenience blocks become much more useful after the reader understands what operation they are replacing.

---

## 14.2 Quadrature Demod

Quadrature Demod estimates phase change between consecutive complex samples.

If:

$$
x[n]=A[n]e^{j\phi[n]}
$$

then the phase of:

$$
x[n]x^*[n-1]
$$

contains the difference:

$$
\phi[n]-\phi[n-1]
$$

That phase change is related to instantaneous frequency.

Chapter 14 used:

```text
Gain = samp_rate/(2*pi)
```

so the raw output could be interpreted approximately in hertz.

For the 10 kHz carrier with ±2 kHz deviation, the raw demodulator output moved approximately between:

```text
8 kHz
and
12 kHz
```

Then:

```text
Add Const = -fc
Multiply Const = 1.0/freq_dev
```

recovered the normalized message.

---

# 15. Digital Communication Blocks

The next part of the book moves from continuous analog messages to bits and symbols.

| Block | Importance | Status |
|---|---|---|
| **Random Source** | Essential | 🔜 Planned |
| **Vector Source** | Important | ✅ Used, new digital role coming |
| **Chunks to Symbols** | Essential | 🔜 Planned |
| **Map** | Important | ⏳ Later |
| **Unpacked to Packed** | Important | ⏳ Later |
| **Packed to Unpacked** | Important | ⏳ Later |
| **Binary Slicer** | Essential | ✅ Used in detection; reused later |
| **Differential Encoder** | Important | ⏳ Later |
| **Differential Decoder** | Important | ⏳ Later |
| **Correlate Access Code** | Important | ⏳ Later |
| **Additive Scrambler** | Important | ⏳ Later |

---

# 16. Synchronization

| Block | Importance | Status |
|---|---|---|
| **Symbol Sync** | Essential | ⏳ Later |
| **Clock Recovery MM** | Important | ⏳ Later |
| **Costas Loop** | Essential | ⏳ Later |
| **PLL Carrier Tracking** | Important | ⏳ Later |
| **PLL Frequency Detector** | Advanced | ⏳ Later |
| **FLL Band-Edge** | Advanced | ⏳ Later |

These remain later topics because the current experiments still assume ideal timing and carrier references where required.

---

# 17. Channel and Impairment Simulation

| Block / Method | Importance | Status |
|---|---|---|
| **Manual Noise Source + Add channel** | Essential concept | ✅ Used | Chapter 14 |
| **Channel Model** | Essential | ⏳ Later |
| **Dynamic Channel Model** | Advanced | ⏳ Later |
| **Frequency Selective Fading Model** | Advanced | ⏳ Later |
| **Selective Fading Model** | Advanced | ⏳ Later |

Chapter 14 gave us a first simple channel-like impairment without using Channel Model:

```text
Complex FM
    +
Complex Gaussian noise
    ↓
Noisy received FM
```

Later Channel Model will combine several impairments in one place.

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

Recorded IQ will later provide a bridge between simulated flowgraphs and real RF experiments.

---

# 19. Message and PDU Processing

| Block | Importance | Status |
|---|---|---|
| **Message Debug** | Important | ⏳ Later |
| **Tagged Stream to PDU** | Advanced | ⏳ Later |
| **PDU to Tagged Stream** | Advanced | ⏳ Later |
| **Socket PDU** | Advanced | ⏳ Later |

---

# 20. SDR Hardware Interfaces

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

The conceptual chapters should not depend on one hardware manufacturer.

---

# 21. Custom and Advanced Processing

| Block / Feature | Importance | Status |
|---|---|---|
| **Embedded Python Block** | Important | ⏳ Later |
| **Hierarchical Block** | Important | ⏳ Later |
| **Stream Tags** | Essential | ⏳ Later |
| **Tagged Streams** | Essential | ⏳ Later |
| **PDUs** | Important | ⏳ Later |

---

# 22. Similar-Looking Blocks Are Not Necessarily the Same

Several GNU Radio blocks can appear to solve similar problems.

For example:

```text
Low Pass Filter
Low-pass Filter Taps
FFT Low Pass Filter
Decimating FIR Filter
```

They are not interchangeable names.

The important habit is to ask:

> What operation does my signal need?

Then ask:

> Which implementation is appropriate here?

The same principle now applies to modulation.

For example:

```text
Manual VCO-based FM
Frequency Mod
NBFM Transmit
WBFM Transmit
```

All relate to FM, but they expose different amounts of the underlying processing.

The book should normally introduce the clearest underlying operation first and use convenience blocks later when they solve a real practical problem.

---

# 23. Blocks We Have Used So Far

At the end of Chapter 14, the working GNU Radio toolbox includes:

| Block / Feature | Status |
|---|---|
| Signal Source | ✅ |
| Noise Source | ✅ |
| Constant Source | ✅ |
| Vector Source | ✅ |
| VCO | ✅ |
| VCO (Complex) | ✅ |
| Throttle | ✅ |
| Variable | ✅ |
| Import | ✅ |
| Head | ✅ |
| Add | ✅ |
| Multiply | ✅ |
| Divide | ✅ |
| Log10 | ✅ |
| Multiply Const | ✅ |
| Add Const | ✅ |
| Abs | ✅ |
| Float to Complex | ✅ |
| Complex to Real | ✅ |
| Complex to Imag | ✅ |
| Complex to Mag | ✅ |
| Complex to Mag² | ✅ |
| Complex to Arg | ✅ |
| Char to Float | ✅ |
| Stream to Vector | ✅ |
| Keep 1 in N | ✅ |
| Delay | ✅ |
| FFT | ✅ |
| Moving Average | ✅ |
| Low Pass Filter | ✅ |
| High Pass Filter | ✅ |
| Band Pass Filter | ✅ |
| Band Reject Filter | ✅ |
| Decimating FIR Filter | ✅ |
| DC Blocker | ✅ |
| Low-pass Filter Taps | ✅ |
| Binary Slicer | ✅ |
| Quadrature Demod | ✅ |
| QT GUI Time Sink | ✅ |
| QT GUI Frequency Sink | ✅ |
| QT GUI Constellation Sink | ✅ |
| QT GUI Vector Sink | ✅ |
| QT GUI Number Sink | ✅ |
| QT GUI Waterfall Sink | ✅ |
| QT GUI Range | ✅ |
| QT GUI Chooser | ✅ |

This is already a substantial toolbox.

More importantly, the blocks are beginning to map to operations naturally.

```text
Need a known periodic waveform
        ↓
Signal Source
```

```text
Need a known finite sequence
        ↓
Vector Source
```

```text
Need to observe frequency content
        ↓
QT GUI Frequency Sink
```

```text
Need to translate frequency
        ↓
Multiply by an oscillator
```

```text
Need a selected frequency region
        ↓
Appropriate filter
```

```text
Need to detect a known waveform
        ↓
Matched filter / correlation
        ↓
Threshold
        ↓
Binary Slicer
```

```text
Need conventional AM
        ↓
Add the carrier/DC term
        ↓
Multiply by carrier
```

```text
Need simple AM envelope recovery
        ↓
Abs
        ↓
Low Pass Filter
        ↓
DC Blocker
```

```text
Need FM from first principles
        ↓
Message × deviation
        ↓
+ center frequency
        ↓
VCO
```

```text
Need to recover FM
        ↓
Quadrature Demod
        ↓
Remove center-frequency offset
        ↓
Normalize by deviation
```

```text
Need to inspect complex-signal magnitude
        ↓
Complex to Mag
```

This way of thinking is more important than memorizing names.

---

# 24. Chapter-by-Chapter GNU Radio Growth Through Chapter 14

This section records the practical progression the completed book has actually followed.

| Chapter | Main GNU Radio development |
|---|---|
| 1 | GRC basics, Signal Source, Throttle, Time Sink |
| 2 | Variables, expressions, Add, branching |
| 3 | QT GUI Range, runtime changes, sampling/aliasing displays |
| 4–5 | Complex data, Float to Complex, I/Q inspection, Constellation Sink |
| 6 | FFT, Stream to Vector, Vector Sink, spectrum tools |
| 7 | Noise, power, SNR, Moving Average, Number Sink |
| 8 | Mixing and frequency translation using Multiply |
| 9 | LPF/HPF/BPF/BRF, taps, decimation, Keep 1 in N |
| 10 | Vector Source and explicit FIR impulse/convolution experiments |
| 11 | Correlation, matched filtering, Add Const thresholding, Binary Slicer, Char to Float |
| 12 | Reuse mixing/filtering tools to understand why modulation exists |
| 13 | Conventional AM, envelope detection, DC Blocker, AM power display, SSB filtering |
| 14 | VCO, Import, Quadrature Demod, FM sidebands, magnitude inspection, additive-noise testing |

This table should be updated after each completed chapter rather than following the original plan mechanically.

---

# 25. What Comes Next?

The next chapter begins the transition from analog communication to digital communication.

The new question is no longer:

> How should a continuous message change a carrier?

It becomes:

> How do zeros and ones become physical signal states?

The first likely GNU Radio additions are therefore digital-data and mapping tools such as:

- Random Source;
- controlled Vector Source sequences;
- bit/byte manipulation where necessary;
- Chunks to Symbols when symbol mapping begins.

The key teaching rule remains unchanged:

> Introduce the operation because the communication problem requires it, not because a block happens to exist.

---

# 26. Rule for Updating This Document

Whenever a new GNU Radio block becomes part of the book:

1. Introduce it naturally when the signal-processing problem requires it.
2. Explain it in the chapter's **GNU Radio Toolbox** when a focused explanation is useful.
3. Use it in a completed experiment.
4. Add or update it in this Master List.
5. Mark its status as **Used** only after that experiment works.
6. Record where it first appeared or first became important.
7. Reuse it later without repeatedly teaching it from the beginning.
8. If the actual experiments differ from the original chapter plan, update this Master List to reflect the experiments that were really completed.

---

## Final Note

This is a **living document**.

At the end of Chapter 14, we can now do much more than generate and inspect simple signals.

```text
Generate
   ↓
Measure
   ↓
Transform
   ↓
Mix
   ↓
Filter
   ↓
Decimate
   ↓
Convolve
   ↓
Correlate
   ↓
Detect
   ↓
Modulate
   ↓
Demodulate
   ↓
Disturb with controlled noise
   ↓
Observe receiver degradation
```

The next stage of the book will add a new layer:

```text
Bits
  ↓
Symbols
  ↓
Waveforms
  ↓
Digital communication
```

The purpose of the Master List is not to collect block names.

It is to help the reader gradually reach the point where they can look at a signal-processing requirement and ask:

> **What operation needs to happen to this signal?**

Only then:

> **Which GNU Radio block should perform that operation?**
