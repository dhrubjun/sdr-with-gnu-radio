# GNU Radio Block Master List

**Updated through Chapter 15: Bits, Symbols and Digital Communication**

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
| **Vector Source** | Important | ✅ Used | Produces a predefined sequence of values | Chapter 10; reused Chapter 15 for controlled bit patterns |
| **Random Source** | Essential | ✅ Used | Generates random integer values; used for binary data by restricting output to 0 and 1 | Chapter 15 |
| **VCO** | Important | ✅ Used | Generates a frequency-controlled oscillator | Chapter 14 |
| **VCO (Complex)** | Important | ✅ Used | Generates a complex frequency-controlled oscillator | Chapter 14 |
| **Fast Noise Source** | Important | ⏳ Later | Efficient noise generation | Later |
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

It has been reused for waveform fundamentals, sampling, I/Q, FFT experiments, mixing, filtering, modulation, and correlation test signals.

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

It was first used to study noise, power, SNR, and noise bandwidth.

In Chapter 14 it was reused as a complex Gaussian noise source added directly to an FM signal to simulate additive channel noise.

---

## 1.3 Constant Source

Constant Source produces the same value continuously.

In Chapter 13 it was useful when numerical quantities such as AM power percentages were sent to a QT GUI Number Sink.

Typical uses include DC values, fixed control streams, numerical displays, and testing.

---

## 1.4 Vector Source

Vector Source produces samples from a predefined list.

Chapter 10 used it for impulses, delayed impulses, short finite sequences, and convolution experiments.

Chapter 15 gave the same block an important new role: controlled digital data.

For example:

```text
1, 0, 1, 1, 0, 0, 1, 0
```

was used because the exact bit pattern was known in advance. That let us verify every bit grouping and symbol index before moving to random data.

This is a useful teaching pattern:

```text
Known sequence first
        ↓
Understand the transformation
        ↓
Random data later
```

---

## 1.5 Random Source

Random Source entered the book in Chapter 15 after the controlled bit-to-symbol experiments were already understood.

For binary data we used:

```text
Minimum: 0
Maximum: 2
```

with byte output, so the generated values were restricted to:

```text
0
1
```

The important distinction is that the source emits byte-sized stream items whose values are 0 or 1. The **information is binary**, even though each GNU Radio item occupies a byte-sized data type.

Random Source is useful once we no longer need a hand-picked sequence for visual verification.

---

## 1.6 VCO

VCO stands for **Voltage-Controlled Oscillator**.

In GNU Radio, the input controls the oscillator's phase rate and therefore its instantaneous frequency.

Chapter 14 used the VCO to build FM from first principles.

---

## 1.7 VCO (Complex)

The complex VCO produces a rotating complex phasor.

Chapter 14 used it with Quadrature Demod so the receiver could measure phase evolution directly.

Important settings included:

```text
Sample Rate: samp_rate
Sensitivity: 2*pi
Amplitude: 1
```

---

# 2. Flow Control and Flowgraph Utilities

| Block / Object | Importance | Status | What it does | First introduced / major use |
|---|---|---|---|---|
| **Throttle** | Essential | ✅ Used | Limits processing rate in software-only flowgraphs | Earlier chapters |
| **Variable** | Essential | ✅ Used | Stores reusable values and relationships | Earlier chapters; heavily reused Chapter 15 |
| **Import** | Important | ✅ Used | Makes Python names/functions available to generated flowgraph code | Chapter 14 |
| **Head** | Important | ✅ Used | Passes only a selected number of items | Chapter 10/11 finite-sequence work |

Chapter 15 continued the move toward relationship-based variables. For example:

```text
samples_per_bit = int(samp_rate / bit_rate)
```

made the connection between sample rate and bit rate explicit instead of hiding it inside fixed numbers.

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

# 4. Complex-Signal and Type-Conversion Blocks

| Block | Importance | Status | What it does | First introduced / major use |
|---|---|---|---|---|
| **Float to Complex** | Essential | ✅ Used | Combines float streams into a complex stream | Earlier I/Q chapters; reused Chapter 14 |
| **Complex to Real** | Essential | ✅ Used | Extracts real/I component | Earlier I/Q chapters |
| **Complex to Imag** | Essential | ✅ Used | Extracts imaginary/Q component | Earlier I/Q chapters |
| **Complex to Mag** | Essential | ✅ Used | Calculates complex magnitude | Earlier I/Q chapters; reused Chapter 14 |
| **Complex to Arg** | Essential | ✅ Used | Calculates complex phase | Earlier I/Q chapters |
| **Complex to Mag²** | Essential | ✅ Used | Calculates squared complex magnitude | Chapter 6 |
| **Char to Float** | Important | ✅ Used | Converts signed byte/char samples to float | Chapter 11 |
| **UChar to Float** | Important | ✅ Used | Converts unsigned byte values to float without changing their numerical meaning | Chapter 15 |
| **Complex to Float** | Important | ⏳ Later | Separates complex data into float components | Later |
| **Float to Char** | Important | ⏳ Later | Converts float values to byte/char representation | Later |

---

## 4.1 UChar to Float

Chapter 15 used **UChar to Float** because the digital data stream contained unsigned byte values such as 0, 1, 2, and 3.

For the first bit experiment:

```text
byte 0 -> float 0.0
byte 1 -> float 1.0
```

Later, after bit grouping:

```text
symbol index 0 -> 0.0
symbol index 1 -> 1.0
symbol index 2 -> 2.0
symbol index 3 -> 3.0
```

The conversion was used so the values could be handled and displayed as a float signal.

### Important distinction

UChar to Float does **not** perform modulation or symbol mapping. It only changes the numerical data type.

---

# 5. Stream, Bit and Vector Operations

| Block | Importance | Status | What it does | First introduced / major use |
|---|---|---|---|---|
| **Stream to Vector** | Essential | ✅ Used | Groups stream samples into vectors | Chapter 6 |
| **Keep 1 in N** | Important | ✅ Used | Keeps one item out of every N | Chapter 9 |
| **Head** | Important | ✅ Used | Limits a stream to a finite number of items | Chapter 10/11 |
| **Delay** | Important | ✅ Used | Delays a signal by a chosen number of samples | Chapter 11 |
| **Repeat** | Important | ✅ Used | Repeats each input item a selected number of times | Chapter 15 |
| **Repack Bits** | Essential | ✅ Used | Regroups a stream using a different number of bits per item | Chapter 15 |
| **Vector to Stream** | Essential | ⏳ Later | Converts vectors to streams | Later OFDM/vector work |

---

## 5.1 Repeat

Repeat became important in Chapter 15 because a single information bit should occupy a finite time interval in the sampled waveform.

With:

```text
samp_rate = 32000
bit_rate = 1000
```

we obtained:

$$
N_{\text{samples/bit}}=\frac{32000}{1000}=32
$$

Using:

```text
Interpolation: samples_per_bit
```

made each bit value persist for 32 samples.

Conceptually:

```text
Bit stream:
1        0        1

After Repeat:
111...111 000...000 111...111
<--32--> <--32--> <--32-->
```

The block does not create extra information. It creates multiple waveform samples representing the same bit or symbol interval.

Chapter 15 also used larger repeat factors for grouped symbols:

```text
1 bit/symbol  -> samples_per_bit
2 bits/symbol -> 2*samples_per_bit
4 bits/symbol -> 4*samples_per_bit
```

This made bit rate and symbol rate visually comparable on the same time axis.

---

## 5.2 Repack Bits

Repack Bits was one of the central new blocks in Chapter 15.

It allowed us to change how many meaningful bits are carried by each stream item.

For example:

```text
Input bits:
1 0 1 1 0 0 1 0

Group 2 bits at a time:
10 | 11 | 00 | 10

Symbol indices:
 2 |  3 |  0 |  2
```

In the Chapter 15 experiments we used:

```text
Bits per input byte: 1
Bits per output byte: 2
```

and also:

```text
Bits per input byte: 1
Bits per output byte: 4
```

The selected bit ordering was kept consistent so the grouped values matched the intended binary interpretation.

### Important distinction

Repack Bits creates grouped numerical values. Those values are still **symbol indices**, not transmitted amplitudes, phases, or frequencies.

That physical mapping begins in later digital modulation chapters.

---

# 6. Fourier and Spectrum Analysis

| Block | Importance | Status | What it does | First introduced |
|---|---|---|---|---|
| **FFT** | Essential | ✅ Used | Computes the DFT efficiently | Chapter 6 |
| **IFFT** | Essential | ⏳ Later | Creates time-domain data from frequency-domain bins | OFDM chapters |
| **Goertzel** | Important | ⏳ Later | Evaluates selected frequencies efficiently | Later |
| **Log Power FFT** | Important | ⏳ Later | Produces logarithmic spectral power | Later |

---

# 7. Averaging and Measurement

| Block | Importance | Status | What it does | First introduced |
|---|---|---|---|---|
| **Moving Average** | Essential | ✅ Used | Averages over a moving window | Chapter 7 |
| **RMS** | Important | ⏳ Later | Estimates root-mean-square magnitude | Later |
| **Probe Signal** | Important | ⏳ Later | Exposes live values programmatically | Later |

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

# 9. Filter-Tap Design Blocks

| Block | Importance | Status | What it does | First introduced |
|---|---|---|---|---|
| **Low-pass Filter Taps** | Important | ✅ Used | Generates low-pass FIR coefficients | Chapter 9 |
| **High-pass Filter Taps** | Important | ⏳ Later | Generates high-pass FIR coefficients | Later |
| **Band-pass Filter Taps** | Important | ⏳ Later | Generates band-pass FIR coefficients | Later |
| **Band-reject Filter Taps** | Important | ⏳ Later | Generates band-reject FIR coefficients | Later |
| **RRC Filter Taps** | Important | ⏳ Later | Generates root-raised-cosine taps | Digital communications |
| **Filter Taps Loader** | Advanced | ⏳ Later | Loads externally defined taps | Later |

---

# 10. Correlation, Matched Filtering and Detection

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

Chapter 15 reused the QT GUI Time Sink in a different visual role: displaying bit values and symbol indices against time.

---

# 12. QT GUI Controls

| Block | Importance | Status | What it does |
|---|---|---|---|
| **QT GUI Range** | Essential | ✅ Used | Interactive numerical control |
| **QT GUI Chooser** | Important | ✅ Used | Selects predefined values |
| **QT GUI Push Button** | Important | ⏳ Later | Clickable runtime action |
| **QT GUI Entry** | Important | ⏳ Later | Runtime numerical/text entry |
| **QT GUI Check Box** | Important | ⏳ Later | Boolean control |

Chapter 15 reused QT GUI Range for **Bit Rate (bit/s)**.

The experiment reinforced:

$$
T_b=\frac{1}{R_b}
$$

and:

$$
N_{\text{samples/bit}}=\frac{f_s}{R_b}
$$

---

# 13. Resampling and Rate Change

| Block | Importance | Status | What it does |
|---|---|---|---|
| **Decimating FIR Filter** | Essential | ✅ Used | Filters while reducing sample rate |
| **Keep 1 in N** | Important | ✅ Used | Direct downsampling without anti-alias filtering |
| **Repeat** | Important | ✅ Used | Repeats items; used in Chapter 15 to represent bit and symbol intervals with multiple samples |
| **Interpolating FIR Filter** | Essential | ⏳ Later | Filters while increasing sample rate |
| **Rational Resampler** | Essential | ⏳ Later | Rational sample-rate conversion |
| **Fractional Resampler** | Advanced | ⏳ Later | Non-integer resampling |

Repeat should not be confused with a proper interpolation filter. In Chapter 15 it was deliberately used as a simple repetition mechanism so the bit and symbol timing could be seen clearly before pulse shaping is introduced later.

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

# 15. Digital Communication Blocks

Chapter 15 begins the transition from continuously varying analog messages to bits, symbols, and digital data representation.

| Block / Operation | Importance | Status | First use / role |
|---|---|---|---|
| **Vector Source** | Important | ✅ Used | Controlled binary sequences for verifying bit and symbol transformations |
| **Random Source** | Essential | ✅ Used | Generates arbitrary binary data after the controlled examples are understood |
| **UChar to Float** | Important | ✅ Used | Converts byte-valued bits/symbol indices to float for waveform display |
| **Repeat** | Important | ✅ Used | Gives each bit or symbol a finite sampled duration |
| **Repack Bits** | Essential | ✅ Used | Groups 1-bit items into 2-bit and 4-bit symbol indices |
| **QT GUI Range** | Essential | ✅ Used | Changes bit rate interactively |
| **Chunks to Symbols** | Essential | 🔜 Planned | Maps symbol indices to actual signal values; natural next step for PAM |
| **Map** | Important | ⏳ Later | General symbol/value remapping |
| **Unpacked to Packed** | Important | ⏳ Later | Packs multiple bits into larger items |
| **Packed to Unpacked** | Important | ⏳ Later | Expands packed data into smaller bit groups |
| **Binary Slicer** | Essential | ✅ Used in detection; reused later | Makes binary decisions |
| **Differential Encoder** | Important | ⏳ Later | Differential symbol encoding |
| **Differential Decoder** | Important | ⏳ Later | Differential symbol decoding |
| **Correlate Access Code** | Important | ⏳ Later | Detects known bit patterns |
| **Additive Scrambler** | Important | ⏳ Later | Scrambles data sequences |

## 15.1 Chapter 15 Data Path

The main GNU Radio progression was:

```text
Known bits
    ↓
Vector Source
    ↓
UChar to Float
    ↓
Repeat
    ↓
Sampled bit waveform
```

then:

```text
Bits
  ↓
Repack Bits
  ↓
Symbol indices
```

and finally:

```text
Random Source
    ↓
Random binary data
    ↓
Repack Bits
    ↓
Random symbol indices
```

This chapter deliberately stopped **before** mapping symbol indices to physical amplitudes, phases, or frequencies.

That boundary is important because Chapter 16 begins with the simplest physical mapping: amplitude levels in PAM.

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

These remain later topics because the current digital experiments assume ideal timing.

---

# 17. Channel and Impairment Simulation

| Block / Method | Importance | Status |
|---|---|---|
| **Manual Noise Source + Add channel** | Essential concept | ✅ Used |
| **Channel Model** | Essential | ⏳ Later |
| **Dynamic Channel Model** | Advanced | ⏳ Later |
| **Frequency Selective Fading Model** | Advanced | ⏳ Later |
| **Selective Fading Model** | Advanced | ⏳ Later |

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

For digital data, Chapter 15 adds another useful example:

```text
Repeat
Repack Bits
Chunks to Symbols
```

These do very different jobs.

```text
Repeat
    ↓
Repeats the same item in time
```

```text
Repack Bits
    ↓
Changes how bits are grouped into stream items
```

```text
Chunks to Symbols
    ↓
Maps a symbol index to an actual chosen signal value
```

The important habit remains:

> What operation does my signal need?

Then:

> Which GNU Radio block performs that operation?

---

# 23. Blocks We Have Used So Far

At the end of Chapter 15, the working GNU Radio toolbox includes:

| Block / Feature | Status |
|---|---|
| Signal Source | ✅ |
| Noise Source | ✅ |
| Constant Source | ✅ |
| Vector Source | ✅ |
| Random Source | ✅ |
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
| UChar to Float | ✅ |
| Stream to Vector | ✅ |
| Keep 1 in N | ✅ |
| Delay | ✅ |
| Repeat | ✅ |
| Repack Bits | ✅ |
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

More importantly, the blocks are beginning to map to operations naturally.

```text
Need a known finite sequence
        ↓
Vector Source
```

```text
Need arbitrary binary test data
        ↓
Random Source
```

```text
Need one bit to occupy several waveform samples
        ↓
Repeat
```

```text
Need to group bits into symbol indices
        ↓
Repack Bits
```

```text
Need to change byte-valued data into float for display
        ↓
UChar to Float
```

This way of thinking is more important than memorizing block names.

---

# 24. Chapter-by-Chapter GNU Radio Growth Through Chapter 15

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
| 15 | Controlled and random binary data, UChar to Float, Repeat, Repack Bits, bit rate vs symbol rate, symbol-index mapping |

This table should be updated after each completed chapter rather than following the original plan mechanically.

---

# 25. What Comes Next?

Chapter 16 moves from **abstract symbol indices** to the first physical digital signal mapping.

At the end of Chapter 15 we have values such as:

```text
0
1
2
3
```

but these are only labels.

The next question is:

> How can a symbol index become an actual signal value?

For Chapter 16, the simplest answer is amplitude.

The likely next GNU Radio addition is therefore:

- **Chunks to Symbols**, for mapping symbol indices to chosen PAM levels.

The chapter can then build 2-PAM and 4-PAM before adding noise and decision thresholds.

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

At the end of Chapter 15, the learning path has reached a major transition.

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
Bits
   ↓
Group bits
   ↓
Symbols
```

The next stage adds another layer:

```text
Symbol index
    ↓
Physical signal value
    ↓
Digital modulation
```

The purpose of the Master List is not to collect block names.

It is to help the reader gradually reach the point where they can look at a signal-processing requirement and ask:

> **What operation needs to happen to this signal?**

Only then:

> **Which GNU Radio block should perform that operation?**
