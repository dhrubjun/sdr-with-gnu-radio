# GNU Radio Block Master List

**Updated through Chapter 23: Frame Synchronization and Packet Detection**

---

## Why This Document Exists

GNU Radio contains a very large number of blocks.

Trying to learn all of them at once would not be useful.

This document therefore does **not** attempt to list every block in GNU Radio. It records the blocks, controls, tap generators, objects, synchronization tools, tagging features, and important GNU Radio operations that matter to the learning path of this book.

The list grows with the completed manuscript.

When an important block first appears, the chapter normally teaches it in context through a **GNU Radio Toolbox** discussion. This Master List serves a different purpose:

> **Which GNU Radio tools have we encountered so far, what do they do, and where did we first use them?**

```text
Chapter
   |
   v
Signal-processing problem
   |
   v
GNU Radio Toolbox
   |
   v
Experiment
   |
   v
GNU Radio Block Master List
```

The **Toolbox teaches the block**.

The **Master List keeps track of it**.

---

## Status and Importance

### Importance

- **Essential** — fundamental to the book's DSP/SDR workflow.
- **Important** — becomes important when the corresponding concept appears.
- **Advanced** — useful when systems become more realistic.
- **Specialized** — mainly for particular applications.

### Status

- ✅ **Used** — appeared in a completed experiment.
- 🔜 **Planned** — expected soon in the current learning path.
- ⏳ **Later** — useful, but its topic has not yet been developed.
- ➖ **Optional** — useful but not required for the main path.

A block is marked **Used** only after it has appeared in a completed experiment.

---

# 1. Signal and Data Sources

| Block | Importance | Status | What it does | First introduced / major use |
|---|---|---|---|---|
| **Signal Source** | Essential | ✅ Used | Generates periodic test signals and complex rotating phasors | Early chapters; CFO experiments Chapter 21 |
| **Noise Source** | Essential | ✅ Used | Generates Gaussian and other noise | Chapter 7; reused throughout later receiver chapters |
| **Constant Source** | Important | ✅ Used | Produces a constant stream | Chapter 13; threshold reference Chapter 23 |
| **Vector Source** | Important | ✅ Used | Produces a predefined sequence | Chapter 10; controlled digital patterns Chapters 15–23 |
| **Random Source** | Essential | ✅ Used | Generates random integer data | Chapter 15; reused digital communication chapters |
| **VCO** | Important | ✅ Used | Frequency-controlled oscillator | Chapter 14 |
| **VCO (Complex)** | Important | ✅ Used | Complex frequency-controlled oscillator | Chapter 14 |
| **File Source** | Important | ⏳ Later | Reads stored sample streams | Later |
| **Fast Noise Source** | Important | ⏳ Later | Efficient noise generation | Later |
| **GLFSR Source** | Important | ⏳ Later | Generates pseudo-random sequences | Later digital communications |

## 1.1 Controlled Data Before Random Data

Vector Source remains especially useful because a known sequence makes transformations and synchronization easier to verify.

```text
Known sequence
      |
      v
Verify operation
      |
      v
Random data
```

This principle became especially important again in Chapter 23, where a deliberately known access code was required for frame detection.

---

# 2. Flow Control and Flowgraph Utilities

| Block / Object | Importance | Status | What it does | First introduced / major use |
|---|---|---|---|---|
| **Throttle** | Essential | ✅ Used | Limits processing rate in software-only flowgraphs | Early chapters |
| **Variable** | Essential | ✅ Used | Stores reusable values and relationships | Early chapters |
| **Import** | Important | ✅ Used | Makes Python names/functions available to generated code | Chapter 14 |
| **Head** | Important | ✅ Used | Passes only a selected number of items | Chapters 10–11; finite captures Chapter 21; finite Tag Debug output Chapter 23 |
| **Delay** | Important | ✅ Used | Delays a stream by selected samples | Chapter 11; multipath Chapter 19; CFO estimation Chapter 21 |

Variables increasingly express physical relationships rather than isolated constants:

```text
samples_per_bit = int(samp_rate / bit_rate)
sps             = int(samp_rate / symbol_rate)
```

---

# 3. Mathematical Operations

| Block / Operation | Importance | Status | What it does | First introduced / major use |
|---|---|---|---|---|
| **Add** | Essential | ✅ Used | Adds streams sample by sample | Early chapters; channel/noise experiments |
| **Multiply** | Essential | ✅ Used | Multiplies streams sample by sample | Early chapters; mixing, modulation, impairment experiments |
| **Divide** | Important | ✅ Used | Divides one stream by another | Chapter 7 |
| **Multiply Const** | Essential | ✅ Used | Multiplies every sample by a constant | Chapter 7; scaling and phase experiments |
| **Add Const** | Important | ✅ Used | Adds a constant to every sample | Chapter 11; reused later |
| **Multiply Conjugate** | Important | ✅ Used | Multiplies one complex stream by the conjugate of another | Chapter 21 |
| **Exponentiate Const Int** | Important | ✅ Used | Raises each sample to a fixed integer power | Chapter 21 |
| **Log10** | Important | ✅ Used | Calculates base-10 logarithm | Chapter 7 |
| **Abs** | Important | ✅ Used | Calculates absolute value | Chapter 13 |
| **Subtract** | Important | ⏳ Later | Subtracts streams | Later |

## 3.1 Multiply Conjugate

If

```text
x = A exp(jθx)
y = B exp(jθy)
```

then

```text
x y* = AB exp(j(θx - θy))
```

so the result contains a phase difference.

This was used for phase-error and CFO-related measurements in Chapter 21.

## 3.2 Exponentiate Const Int

Chapter 21 used exponent `4` for QPSK to remove the fourfold data-dependent phase structure before carrier-frequency interpretation.

---

# 4. Complex-Signal and Type-Conversion Blocks

| Block | Importance | Status | What it does | First introduced / major use |
|---|---|---|---|---|
| **Float to Complex** | Essential | ✅ Used | Combines I and Q float streams into a complex stream | Early I/Q chapters; central digital modulation chapters |
| **Complex to Real** | Essential | ✅ Used | Extracts the real/I component | Early I/Q chapters |
| **Complex to Imag** | Essential | ✅ Used | Extracts the imaginary/Q component | Early I/Q chapters |
| **Complex to Mag** | Essential | ✅ Used | Calculates complex magnitude | Early I/Q chapters; manual preamble correlation Chapter 23 |
| **Complex to Arg** | Essential | ✅ Used | Calculates complex phase | Early I/Q chapters; carrier/CFO estimation Chapter 21 |
| **Complex to Mag²** | Essential | ✅ Used | Calculates squared magnitude | Chapter 6 |
| **Complex to Float** | Important | ✅ Used | Splits a complex stream into real and imaginary float outputs | Chapter 23 complete QPSK frame detector |
| **Char to Float** | Important | ✅ Used | Converts signed byte/char samples to float | Chapter 11 |
| **UChar to Float** | Important | ✅ Used | Converts unsigned byte values to float | Chapter 15 |
| **Float to Char** | Important | ⏳ Later | Converts float values to byte/char form | Later |

## 4.1 Complex to Float in the Receiver

Chapter 23 gave **Complex to Float** a practical receiver role:

```text
Recovered QPSK symbols
        |
        v
Complex to Float
      /     \
     I       Q
     |       |
     v       v
Binary decisions
```

It separated synchronized QPSK symbols into I and Q values before hard bit decisions.

---

# 5. Stream, Bit and Symbol Operations

| Block / Method | Importance | Status | What it does | First introduced / major use |
|---|---|---|---|---|
| **Stream to Vector** | Essential | ✅ Used | Groups stream items into vectors | Chapter 6 |
| **Keep 1 in N** | Important | ✅ Used | Keeps one item out of every N | Chapter 9; symbol-rate observation later |
| **Head** | Important | ✅ Used | Limits a stream to a finite number of items | Chapters 10–11; Chapters 21 and 23 |
| **Delay** | Important | ✅ Used | Delays a stream | Chapter 11; Chapters 19 and 21 |
| **Repeat** | Important | ✅ Used | Repeats each item a selected number of times | Chapter 15; rectangular pulses Chapters 16–18 |
| **Repack Bits** | Essential | ✅ Used | Regroups meaningful bits into different item widths | Chapter 15; reused Chapter 17 |
| **Chunks to Symbols** | Essential | ✅ Used | Maps symbol indices to chosen symbol values | Chapter 16; central Chapters 17–23 |
| **Interleave** | Important | ✅ Used | Alternates items from multiple streams into one stream | Chapter 23 QPSK I/Q bit serialization |
| **Vector to Stream** | Essential | ⏳ Later | Converts vectors back into a stream | Later OFDM/vector work |
| **Map** | Important | ⏳ Later | General integer/value remapping | Later |

### Important distinctions

```text
Repack Bits
    |
    v
Change how bits are grouped
```

```text
Chunks to Symbols
    |
    v
Map an index to a chosen signal value
```

```text
Repeat
    |
    v
Duplicate an item in time
```

```text
Keep 1 in N
    |
    v
Select one sample out of every N
```

```text
Interleave
    |
    v
Reconstruct one serial stream from multiple input streams
```

---

# 6. Fourier and Spectrum Analysis

| Block / Method | Importance | Status | What it does | First introduced / major use |
|---|---|---|---|---|
| **FFT** | Essential | ✅ Used | Computes the DFT efficiently | Chapter 6 |
| **QT GUI Frequency Sink DFT/FFT view** | Essential | ✅ Used | Displays spectral location and bandwidth | Reused throughout; CFO interpretation Chapter 21 |
| **IFFT** | Essential | ⏳ Later | Creates time-domain samples from frequency-domain bins | OFDM chapters |
| **Goertzel** | Important | ⏳ Later | Evaluates selected frequencies efficiently | Later |
| **Log Power FFT** | Important | ⏳ Later | Produces logarithmic spectral power | Later |

---

# 7. Averaging and Measurement

| Block / Method | Importance | Status | What it does | First introduced / major use |
|---|---|---|---|---|
| **Moving Average** | Essential | ✅ Used | Averages over a moving window | Chapter 7 |
| **QT GUI Number Sink** | Important | ✅ Used | Displays live numerical quantities | Early use; phase/CFO estimates Chapter 21 |
| **RMS** | Important | ⏳ Later | Estimates root-mean-square magnitude | Later |
| **Probe Signal** | Important | ⏳ Later | Exposes live values programmatically | Later |

---

# 8. Filters

| Block | Importance | Status | What it does | First introduced / major use |
|---|---|---|---|---|
| **Low Pass Filter** | Essential | ✅ Used | Passes lower frequencies | Chapter 7; expanded Chapter 9 |
| **High Pass Filter** | Essential | ✅ Used | Passes higher frequencies | Chapter 9 |
| **Band Pass Filter** | Essential | ✅ Used | Passes a selected band | Chapter 9 |
| **Band Reject Filter** | Essential | ✅ Used | Rejects a selected band | Chapter 9 |
| **Decimating FIR Filter** | Essential | ✅ Used | FIR filtering with optional decimation | Chapters 9–11; RX RRC Chapter 18; equalization Chapter 20; manual correlation Chapter 23 |
| **Interpolating FIR Filter** | Essential | ✅ Used | FIR filtering while increasing sample rate | Chapter 18; reused Chapters 19–23 |
| **DC Blocker** | Important | ✅ Used | Removes DC/very-low-frequency offset | Chapter 13 |
| **Linear Equalizer** | Essential receiver tool | ✅ Used | Adaptive FIR equalization of symbol streams | Chapter 20 |
| **Frequency Xlating FIR Filter** | Advanced | ⏳ Later | Frequency translation + filtering + decimation | Later receiver work |
| **FFT Filter** | Important | ⏳ Later | FIR filtering using FFT convolution | Later |
| **IIR Filter** | Important | ⏳ Later | Infinite impulse response filtering | Later |
| **Single Pole IIR Filter** | Important | ⏳ Later | Simple recursive smoothing/filtering | Later |

## 8.1 Interpolating FIR Filter

```text
Symbol-rate stream
        |
        v
Increase sample rate by sps
        |
        v
Apply FIR pulse-shaping taps
        |
        v
Sample-rate waveform
```

This is not the same as Repeat, which simply duplicates values.

---

# 9. Filter-Tap Design

| Tap generator / method | Importance | Status | What it does | First introduced / major use |
|---|---|---|---|---|
| **Low-pass Filter Taps** | Important | ✅ Used | Generates low-pass FIR coefficients | Chapter 9 |
| **High-pass Filter Taps** | Important | ⏳ Later | Generates high-pass FIR coefficients | Later |
| **Band-pass Filter Taps** | Important | ⏳ Later | Generates band-pass FIR coefficients | Later |
| **Band-reject Filter Taps** | Important | ⏳ Later | Generates band-reject FIR coefficients | Later |
| **RRC Filter Taps / `firdes.root_raised_cosine`** | Essential | ✅ Used | Generates root-raised-cosine FIR taps | Chapter 18 |
| **Filter Taps Loader** | Advanced | ⏳ Later | Loads externally defined taps | Later |

---

# 10. Correlation, Detection and Decisions

| Block / Operation | Importance | Status | Role | First introduced / major use |
|---|---|---|---|---|
| **Decimating FIR Filter** | Essential | ✅ Used | Correlation/matched filtering with chosen taps | Chapter 11; known-preamble correlator Chapter 23 |
| **Add Const** | Important | ✅ Used | Moves a threshold relative to zero | Chapter 11 |
| **Threshold** | Important | ✅ Used | Converts a continuous input into a state using High/Low levels | Chapter 23 preamble detection threshold experiment |
| **Binary Slicer** | Essential | ✅ Used | Converts samples into binary hard decisions | Chapter 11; QPSK bit recovery Chapter 23 |
| **Char to Float** | Important | ✅ Used | Converts decisions for display | Chapter 11 |
| **Moving Average** | Essential | ✅ Used | Accumulation/smoothing where useful | Chapter 11 |
| **Correlation Estimator** | Essential receiver tool | ✅ Used | Locates a known complex training sequence and produces correlation-related tags | Chapter 20 |
| **Correlate Access Code - Tag** | Essential packet/frame tool | ✅ Used | Searches a bit stream for a known access code and inserts a tag | Chapter 23 |
| **Tag Debug** | Important | ✅ Used | Displays stream tags, offsets, keys and values | Chapter 23 |

## 10.1 Manual Preamble Correlation in Chapter 23

Chapter 23 deliberately returned to the correlation idea from Chapter 12.

```text
Known preamble
      |
      v
FIR correlation
      |
      v
Complex to Mag
      |
      v
Correlation magnitude
      |
      v
Threshold / detection output
```

This made packet detection understandable before introducing a dedicated access-code detector.

## 10.2 Threshold

The **Threshold** block uses:

```text
Low
High
Initial State
```

and provides hysteresis.

In Chapter 23 it converted correlation magnitude into a detection state while a separate constant reference made the numerical decision level visible.

## 10.3 Correlate Access Code - Tag

Completed Chapter 23 settings included:

```text
Access Code: 10110010
Threshold: 0
Tag Name: frame_start
```

The block's `Threshold` does **not** mean correlation magnitude.

It means the number of bit mismatches allowed in the access-code comparison.

```text
Threshold = 0
      |
      v
Exact bit match required
```

```text
Threshold = 1
      |
      v
One bit mismatch allowed
```

Chapter 23 experimentally demonstrated both cases.

---

# 11. QT GUI Visualization

| Block | Importance | Status | Main use |
|---|---|---|---|
| **QT GUI Time Sink** | Essential | ✅ Used | Time-domain waveform, correlation and loop-state inspection |
| **QT GUI Frequency Sink** | Essential | ✅ Used | Spectrum inspection and carrier-frequency studies |
| **QT GUI Constellation Sink** | Essential | ✅ Used | I/Q-plane inspection; central Chapters 17–23 |
| **QT GUI Number Sink** | Important | ✅ Used | Numerical measurement display |
| **QT GUI Vector Sink** | Important | ✅ Used | Vector-valued display |
| **QT GUI Waterfall Sink** | Important | ✅ Used | Spectrum-versus-time display |
| **QT GUI Histogram Sink** | Important | ⏳ Later | Sample distribution |
| **QT GUI Eye Sink** | Important | ⏳ Later / optional | Dedicated eye-diagram display where available |
| **QT GUI Matrix Sink** | Specialized | ➖ Optional | Matrix-like data |

Chapter 23 deliberately stopped showing constellation plots when they no longer answered the experimental question. For preamble-sequence comparison, the correlation plot was the useful visualization.

---

# 12. QT GUI Controls

| Block | Importance | Status | What it does |
|---|---|---|---|
| **QT GUI Range** | Essential | ✅ Used | Interactive numerical control |
| **QT GUI Chooser** | Important | ✅ Used | Selects predefined values |
| **QT GUI Push Button** | Important | ⏳ Later | Runtime action |
| **QT GUI Entry** | Important | ⏳ Later | Runtime numerical/text entry |
| **QT GUI Check Box** | Important | ⏳ Later | Boolean control |

Chapter 23 reused QT GUI Range for:

- noise voltage,
- correlation detection threshold.

---

# 13. Resampling and Rate Change

| Block / Method | Importance | Status | What it does |
|---|---|---|---|
| **Decimating FIR Filter** | Essential | ✅ Used | Filters with optional integer downsampling |
| **Keep 1 in N** | Important | ✅ Used | Direct selection/downsampling without anti-alias filtering |
| **Repeat** | Important | ✅ Used | Duplicates items; rectangular hold |
| **Interpolating FIR Filter** | Essential | ✅ Used | Filters while increasing sample rate |
| **Symbol Sync internal interpolator** | Essential receiver method | ✅ Used | Fractional-sample interpolation inside timing recovery | Chapter 22 |
| **Rational Resampler** | Essential | ⏳ Later | Rational sample-rate conversion |
| **Fractional Resampler** | Advanced | ⏳ Later | General non-integer resampling |

---

# 14. Analog Modulation and Demodulation

| Block / Method | Importance | Status | First use / note |
|---|---|---|---|
| **Manual AM using Add/Multiply** | Essential concept | ✅ Used | Chapters 12–13 |
| **Abs + LPF + DC Blocker envelope detector** | Important | ✅ Used | Chapter 13 |
| **Band Pass Filter SSB method** | Important | ✅ Used | Chapter 13 |
| **VCO** | Important | ✅ Used | Chapter 14 |
| **VCO (Complex)** | Important | ✅ Used | Chapter 14 |
| **Quadrature Demod** | Essential | ✅ Used | Chapter 14 |
| **Frequency Mod** | Essential | ⏳ Later / convenience | Manual FM already understood |
| **NBFM Transmit/Receive** | Important | ⏳ Later / optional | Convenience blocks |
| **WBFM Transmit/Receive** | Important | ⏳ Later / practical | Convenience blocks |
| **AM Demod** | Important | ⏳ Later / convenience | Manual AM demodulation already understood |

---

# 15. Digital Communication Blocks and Objects

| Block / Method / Object | Importance | Status | First use / role |
|---|---|---|---|
| **Vector Source** | Important | ✅ Used | Controlled bits/symbols |
| **Random Source** | Essential | ✅ Used | Random binary/symbol data |
| **UChar to Float** | Important | ✅ Used | Data-type conversion |
| **Repeat** | Important | ✅ Used | Rectangular bit/symbol duration |
| **Repack Bits** | Essential | ✅ Used | Groups bits into symbol indices |
| **Chunks to Symbols** | Essential | ✅ Used | Maps indices to PAM/I/Q values |
| **Float to Complex** | Essential | ✅ Used | Combines I and Q coordinates |
| **Complex to Float** | Important | ✅ Used | Splits recovered complex symbols into I/Q components |
| **Binary Slicer** | Essential | ✅ Used | Binary hard decisions |
| **Interleave** | Important | ✅ Used | Reconstructs serial bit stream from I/Q decisions |
| **Interpolating FIR Filter** | Essential | ✅ Used | RRC pulse shaping |
| **RRC taps** | Essential | ✅ Used | Root-raised-cosine pulse design |
| **Linear Equalizer** | Essential receiver tool | ✅ Used | Adaptive channel equalization |
| **Adaptive Algorithm (LMS)** | Essential receiver object | ✅ Used | Updates equalizer taps |
| **Constellation Rect. Object** | Important receiver object | ✅ Used | Defines valid normalized QPSK decision points |
| **Correlation Estimator** | Essential receiver tool | ✅ Used | Finds known training sequences |
| **Symbol Sync** | Essential receiver tool | ✅ Used | Symbol timing recovery | Chapter 22 |
| **Correlate Access Code - Tag** | Essential frame tool | ✅ Used | Access-code/frame detection | Chapter 23 |
| **Constellation Modulator** | Important | ⏳ Later | Ready-made digital modulation |
| **Constellation Decoder** | Important | ⏳ Later | Ready-made symbol decoding |
| **Differential Encoder** | Important | ⏳ Later | Differential symbol encoding |
| **Differential Decoder** | Important | ⏳ Later | Differential symbol decoding |
| **Additive Scrambler** | Important | ⏳ Later | Scrambles data sequences |

## 15.1 Digital Communication Progression

```text
Chapter 15
Bits -> symbol indices
```

```text
Chapter 16
Symbol indices -> PAM amplitudes -> decisions
```

```text
Chapter 17
I/Q mapping -> QPSK and QAM constellations
```

```text
Chapter 18
Pulse shaping -> matched filtering -> symbol sampling
```

```text
Chapter 19
Channel impairments -> noise, CFO, multipath, sample-rate mismatch
```

```text
Chapter 20
Channel memory -> equalization -> training-assisted adaptation
```

```text
Chapter 21
Carrier mismatch -> phase/frequency estimation and recovery
```

```text
Chapter 22
Sampling-time uncertainty -> timing-error detection -> Symbol Sync
```

```text
Chapter 23
Known preamble/access code -> frame detection -> stream tags
```

---

# 16. Synchronization and Carrier Recovery

| Block / Method | Importance | Status | What it does | First use / note |
|---|---|---|---|---|
| **PLL Carrier Regeneration** | Important | ✅ Used | Generates a carrier reference that follows the input carrier | Chapter 21 |
| **Costas Loop** | Essential | ✅ Used | Modulation-aware feedback carrier recovery for PSK | Chapter 21 |
| **FLL Band-Edge** | Essential receiver tool | ✅ Used | Feedback carrier-frequency recovery using pulse-shaped spectral edges | Chapter 21 |
| **Multiply Conjugate** | Important | ✅ Used | Relative phase / phase-increment measurement | Chapter 21 |
| **Exponentiate Const Int** | Important | ✅ Used | M-th-power modulation removal for QPSK | Chapter 21 |
| **Symbol Sync** | Essential receiver tool | ✅ Used | Automatic symbol timing acquisition and tracking | Chapter 22 |
| **Gardner TED** | Essential timing concept | ✅ Used | Timing-error detector selected inside Symbol Sync | Chapter 22 |
| **Early-Late-style detector** | Important concept | ✅ Used conceptually | Builds timing-error intuition before automatic recovery | Chapter 22 |
| **Mueller and Müller TED** | Important | ➖ Discussed | Alternative timing-error detector discussed but not used in final experiment | Chapter 22 |
| **Clock Recovery MM** | Important | ⏳ Later | Alternative timing-recovery implementation | Later |

## 16.1 Symbol Sync

Chapter 22 used GNU Radio's **Symbol Sync** block after developing timing-error intuition manually.

Important completed settings included:

```text
Timing Error Detector: Gardner
Samples per Symbol: 8
Expected TED Gain: 1
Loop Bandwidth: 0.045
Damping Factor: 1
Maximum Deviation: 1.5
Output Samples/Symbol: 1
Interpolating Resampler: MMSE, 8 tap FIR
```

The key distinction established in Chapter 22 was:

```text
Fixed timing offset
      |
      v
Timing acquisition
```

```text
Sampling-clock mismatch
      |
      v
Timing phase keeps drifting
      |
      v
Continuous timing tracking
```

Symbol Sync corrects **when** the receiver samples. It does not correct carrier phase, multipath distortion, or random noise.

## 16.2 Carrier vs Timing vs Frame Synchronization

By Chapter 23, the receiver synchronization roles are:

```text
Carrier synchronization
        |
        v
Correct carrier phase/frequency
```

```text
Timing synchronization
        |
        v
Correct symbol sampling instant
```

```text
Frame synchronization
        |
        v
Correct message/frame boundary
```

These are related receiver stages, but they solve different problems.

---

# 17. Channel and Impairment Simulation

| Block / Method | Importance | Status | First use / note |
|---|---|---|---|
| **Noise Source + Add** | Essential concept | ✅ Used | Manual AWGN channel in several chapters |
| **Multiply Const / controlled gain** | Essential concept | ✅ Used | Attenuation experiments Chapter 19 |
| **Complex phasor multiplication** | Essential concept | ✅ Used | Phase and frequency offset experiments |
| **Delay + Add / manual multipath** | Essential concept | ✅ Used | Multipath Chapter 19 |
| **Channel Model** | Essential | ✅ Used | Combined controlled channel impairments Chapter 19; reused Chapters 20–23 |
| **Channel Model Epsilon parameter** | Important concept | ✅ Used | Sample-rate mismatch Chapters 19 and 22 |
| **Dynamic Channel Model** | Advanced | ⏳ Later | Time-varying channel simulation |
| **Frequency Selective Fading Model** | Advanced | ⏳ Later | Later |

Chapter 22 used `Epsilon` specifically to create sampling-clock mismatch and demonstrate timing tracking.

Chapter 23 reused Channel Model noise in the complete QPSK frame detector to show missed and false frame detections.

---

# 18. Equalization and Adaptive Receiver Processing

| Block / Object / Method | Importance | Status | Role |
|---|---|---|---|
| **Manual FIR equalizer with Decimating FIR Filter** | Essential concept | ✅ Used | Known-channel inverse-filter intuition |
| **Linear Equalizer** | Essential | ✅ Used | Adaptive FIR equalization |
| **Adaptive Algorithm (LMS)** | Essential | ✅ Used | LMS coefficient adaptation |
| **Constellation Rect. Object** | Important | ✅ Used | Defines valid QPSK decision points |
| **Correlation Estimator** | Essential | ✅ Used | Detects known training sequence |
| **Stream Tags / correlation tags** | Essential concept | ✅ Used | Marks detected sequence location |

---

# 19. File and Data Storage

| Block / Method | Importance | Status | First use / note |
|---|---|---|---|
| **File Sink** | Essential | ✅ Used | Chapter 18 eye samples; Chapter 21 transient capture |
| **External Python plotting scripts** | Important workflow | ✅ Used | Eye diagrams Chapter 18; carrier plots Chapter 21 |
| **File Source** | Essential | ⏳ Later | Reads raw stored samples |
| **WAV File Source** | Important | ⏳ Later | Audio files |
| **WAV File Sink** | Important | ⏳ Later | Audio files |
| **Metadata File Source** | Advanced | ⏳ Later | Later |
| **Metadata File Sink** | Advanced | ⏳ Later | Later |

---

# 20. Tags, Tagged Streams and Message Processing

| Block / Feature | Importance | Status | First use / note |
|---|---|---|---|
| **Stream Tags** | Essential | ✅ Used | Introduced conceptually Chapter 20; used directly for frame detection Chapter 23 |
| **Tag Debug** | Important | ✅ Used | Displays `frame_start` tags, offsets and values | Chapter 23 |
| **Correlate Access Code - Tag** | Essential frame tool | ✅ Used | Creates a tag when a known bit sequence is detected | Chapter 23 |
| **Tagged Streams** | Essential | ⏳ Later | Full tagged-stream architecture later |
| **Message Debug** | Important | ⏳ Later | Message/PDU inspection |
| **Tagged Stream to PDU** | Advanced | ⏳ Later | Converts tagged streams into PDUs |
| **PDU to Tagged Stream** | Advanced | ⏳ Later | Converts PDUs into tagged streams |
| **Socket PDU** | Advanced | ⏳ Later | Network/PDU interfacing |

## 20.1 Stream Tags in Chapter 23

Chapter 23 deliberately introduced only the minimum tag concept needed for frame synchronization.

```text
Recovered bit stream
        |
        v
Known access code detected
        |
        v
frame_start tag
        |
        v
Downstream receiver gets a frame reference
```

The full GNU Radio tag architecture is still postponed.

## 20.2 Tag Position

With the direct repeated frame

```text
10110010 01100101
^^^^^^^^ ^^^^^^^^
access    payload
code
```

the 8-bit access code was detected once every 16 bits, producing tags at:

```text
8, 24, 40, 56, 72, 88, 104, 120
```

The tag appeared immediately after the detected access code in this experiment.

In the complete QPSK receiver, upstream filtering and synchronization changed the absolute offset, but the tag spacing remained 16 bits.

---

# 21. Custom and Advanced Processing

| Block / Feature | Importance | Status | First use / note |
|---|---|---|---|
| **Embedded Python Block** | Important | ✅ Used | Chapter 16 decision/detection experimentation |
| **External Python plotting scripts** | Important workflow | ✅ Used | Chapters 18 and 21 |
| **Hierarchical Block** | Important | ⏳ Later | Later |
| **PDUs** | Important | ⏳ Later | Later |

---

# 22. SDR Hardware Interfaces

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

The conceptual chapters remain hardware-independent unless an experiment specifically requires hardware.

---

# 23. Similar-Looking Operations Are Not the Same

Several operations now used in the receiver can look superficially similar.

```text
Keep 1 in N
    |
    v
Select periodic samples blindly
```

```text
Symbol Sync
    |
    v
Estimate and track the correct sampling instant
```

```text
Correlation Estimator
    |
    v
Find a known complex training sequence
```

```text
Correlate Access Code - Tag
    |
    v
Find a known binary access code and create a tag
```

```text
Threshold
    |
    v
Turn a continuous-valued measurement into a state
```

```text
Correlate Access Code - Tag threshold
    |
    v
Allow a selected number of bit mismatches
```

```text
Binary Slicer
    |
    v
Make a hard binary decision from a real-valued sample
```

```text
Interleave
    |
    v
Serialize multiple streams into one stream
```

The correct habit remains:

> **What physical operation does the receiver need?**

Then:

> **Which GNU Radio block or object performs that operation?**

---

# 24. Important Conceptual Roles Through Chapter 23

| Need | GNU Radio tool / method |
|---|---|
| Generate a known sinusoid or rotating phasor | Signal Source |
| Generate controlled symbols or frame bits | Vector Source |
| Generate random digital data | Random Source |
| Add controlled noise | Noise Source + Add / Channel Model |
| Group bits into symbols | Repack Bits |
| Map indices to amplitudes/I/Q | Chunks to Symbols |
| Combine I and Q | Float to Complex |
| Split recovered complex symbols into I/Q | Complex to Float |
| Pulse-shape symbols | Interpolating FIR Filter + RRC taps |
| Matched-filter at receiver | Decimating FIR Filter |
| Simulate combined channel impairments | Channel Model |
| Create manual multipath | Delay + scaling + Add |
| Perform manual/adaptive equalization | FIR equalizer / Linear Equalizer + LMS |
| Locate a known training sequence | Correlation Estimator |
| Recover carrier phase | Costas Loop |
| Recover carrier frequency | FLL Band-Edge |
| Recover symbol timing | Symbol Sync with Gardner TED |
| Make hard bit decisions | Binary Slicer |
| Reconstruct serial I/Q bit order | Interleave |
| Detect a known binary frame marker | Correlate Access Code - Tag |
| Inspect frame tags | Tag Debug |
| Convert correlation magnitude into detection state | Threshold |
| Limit debug/capture length | Head |
| Inspect time-domain behaviour | QT GUI Time Sink |
| Inspect spectrum | QT GUI Frequency Sink |
| Inspect constellation geometry | QT GUI Constellation Sink |

---

# 25. Blocks and Features Used So Far

At the end of Chapter 23, the working GNU Radio toolbox includes:

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
| Delay | ✅ |
| Add | ✅ |
| Multiply | ✅ |
| Divide | ✅ |
| Multiply Const | ✅ |
| Add Const | ✅ |
| Multiply Conjugate | ✅ |
| Exponentiate Const Int | ✅ |
| Log10 | ✅ |
| Abs | ✅ |
| Float to Complex | ✅ |
| Complex to Real | ✅ |
| Complex to Imag | ✅ |
| Complex to Mag | ✅ |
| Complex to Mag² | ✅ |
| Complex to Arg | ✅ |
| Complex to Float | ✅ |
| Char to Float | ✅ |
| UChar to Float | ✅ |
| Stream to Vector | ✅ |
| Keep 1 in N | ✅ |
| Repeat | ✅ |
| Repack Bits | ✅ |
| Chunks to Symbols | ✅ |
| Interleave | ✅ |
| FFT / DFT analysis | ✅ |
| Moving Average | ✅ |
| Low Pass Filter | ✅ |
| High Pass Filter | ✅ |
| Band Pass Filter | ✅ |
| Band Reject Filter | ✅ |
| Decimating FIR Filter | ✅ |
| Interpolating FIR Filter | ✅ |
| DC Blocker | ✅ |
| Low-pass Filter Taps | ✅ |
| RRC Filter Taps | ✅ |
| Threshold | ✅ |
| Binary Slicer | ✅ |
| Quadrature Demod | ✅ |
| Channel Model | ✅ |
| Linear Equalizer | ✅ |
| Adaptive Algorithm (LMS) | ✅ |
| Constellation Rect. Object | ✅ |
| Correlation Estimator | ✅ |
| PLL Carrier Regeneration | ✅ |
| Costas Loop | ✅ |
| FLL Band-Edge | ✅ |
| Symbol Sync | ✅ |
| Gardner TED | ✅ |
| Stream Tags | ✅ |
| Correlate Access Code - Tag | ✅ |
| Tag Debug | ✅ |
| Embedded Python Block | ✅ |
| File Sink | ✅ |
| QT GUI Time Sink | ✅ |
| QT GUI Frequency Sink | ✅ |
| QT GUI Constellation Sink | ✅ |
| QT GUI Vector Sink | ✅ |
| QT GUI Number Sink | ✅ |
| QT GUI Waterfall Sink | ✅ |
| QT GUI Range | ✅ |
| QT GUI Chooser | ✅ |

---

# 26. Chapter-by-Chapter GNU Radio Growth Through Chapter 23

This table records the practical progression of the completed manuscript.

| Chapter | Main GNU Radio development |
|---|---|
| 1 | SDR/GRC foundations, Signal Source, Throttle, Time Sink |
| 2 | Variables, expressions, Add, branching and waveform relationships |
| 3 | Sampling experiments, QT GUI Range and aliasing visualization |
| 4 | Complex-number/I-Q foundations and complex signal representation |
| 5 | I/Q signal construction and constellation-oriented visualization |
| 6 | FFT, Stream to Vector, Vector Sink and spectrum analysis |
| 7 | Noise, power, SNR, Moving Average and numerical measurement |
| 8 | Mixing and frequency translation with Multiply |
| 9 | LPF/HPF/BPF/BRF, FIR taps, decimation and Keep 1 in N |
| 10 | Vector Source, impulses, FIR response and convolution experiments |
| 11 | Correlation, matched filtering, thresholding, Binary Slicer and decisions |
| 12 | Mixing/filtering reused to explain why modulation and channel selection are needed |
| 13 | Conventional AM, envelope detection, DC Blocker, SSB and AM power observations |
| 14 | VCO, complex VCO, Import, Quadrature Demod, FM sidebands and noise |
| 15 | Controlled/random bits, UChar to Float, Repeat, Repack Bits, bit rate and symbol rate |
| 16 | Chunks to Symbols, PAM mapping, hard decisions, noisy PAM, Embedded Python Block experimentation |
| 17 | Manual BPSK/QPSK/16-QAM construction, Float to Complex, constellation geometry, scaling and rotation |
| 18 | Rectangular-symbol spectrum, RRC pulse shaping, matched filtering, File Sink and eye-diagram capture |
| 19 | Channel Model, attenuation, CFO, manual multipath, channel memory, sample-rate mismatch and `epsilon` |
| 20 | Manual/adaptive equalization, Linear Equalizer, LMS, Constellation Rect. Object, training and Correlation Estimator |
| 21 | Multiply Conjugate, M-th power processing, PLL carrier regeneration, Costas Loop, CFO estimation and FLL Band-Edge |
| 22 | Timing-error intuition, Gardner TED, interpolation, Symbol Sync, timing acquisition/tracking and clock-rate mismatch |
| 23 | Manual preamble correlation, Threshold, access-code detection, Stream Tags, Tag Debug, Interleave and QPSK frame detection |

This table should always follow the **completed manuscript**, not an old chapter plan.

---

# 27. What Comes Next?

Chapter 23 ends with a receiver that can identify a repeated frame boundary using a known access code.

The next unresolved question is:

> **How does the receiver know whether the bits inside the detected frame are correct, and can some errors be corrected?**

Chapter 24 moves into **Error Detection and Forward Error Correction**.

Likely GNU Radio additions may include suitable FEC encoder/decoder blocks, but the exact FEC block chain should be validated against the supported GNU Radio version before being frozen into the book.

The conceptual progression should be:

```text
Recovered frame
      |
      v
Possible bit errors
      |
      v
Add structured redundancy
      |
      v
Detect / correct errors
      |
      v
More reliable communication
```

Do not teach the complete GNU Radio FEC API merely because it exists.

The teaching rule remains:

> **Introduce the operation because the communication problem requires it, not because a GNU Radio block happens to exist.**

---

# 28. Rule for Updating This Document

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

This remains a **living document**.

At the end of Chapter 23, the practical receiver toolbox now spans:

```text
Generate
   |
   v
Measure
   |
   v
Transform
   |
   v
Mix
   |
   v
Filter
   |
   v
Modulate / demodulate
   |
   v
Pulse-shape / matched-filter
   |
   v
Model channel impairments
   |
   v
Equalize
   |
   v
Recover carrier
   |
   v
Recover symbol timing
   |
   v
Make bit decisions
   |
   v
Detect frame boundaries
   |
   v
Attach receiver metadata with tags
```

The purpose of this list is not to memorize GNU Radio's block library.

The goal is to reach the point where the reader can look at a signal-processing requirement and ask:

> **What operation needs to happen to this signal?**

Only then:

> **Which GNU Radio block or object should perform that operation?**
