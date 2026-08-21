# GNU Radio Block Master List

**Updated through Chapter 21: PLL and Carrier Synchronization**

---

## Why This Document Exists

GNU Radio contains a very large number of blocks.

Trying to learn all of them at once would not be useful.

This document therefore does **not** attempt to list every block in GNU Radio. It records the blocks, controls, tap generators, objects, and important GNU Radio operations that matter to the learning path of this book.

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
| **Noise Source** | Essential | ✅ Used | Generates Gaussian and other noise | Chapter 7; reused Chapters 14, 16–21 |
| **Constant Source** | Important | ✅ Used | Produces a constant stream | Chapter 13 |
| **Vector Source** | Important | ✅ Used | Produces a predefined sequence | Chapter 10; controlled digital patterns Chapters 15–20 |
| **Random Source** | Essential | ✅ Used | Generates random integer data | Chapter 15; reused Chapters 16–21 |
| **VCO** | Important | ✅ Used | Frequency-controlled oscillator | Chapter 14 |
| **VCO (Complex)** | Important | ✅ Used | Complex frequency-controlled oscillator | Chapter 14 |
| **File Source** | Important | ⏳ Later | Reads stored sample streams | Later |
| **Fast Noise Source** | Important | ⏳ Later | Efficient noise generation | Later |
| **GLFSR Source** | Important | ⏳ Later | Generates pseudo-random sequences | Later digital communications |

## 1.1 Controlled Data Before Random Data

Vector Source remains especially useful because a known sequence makes transformations easy to verify.

```text
Known sequence
      |
      v
Verify operation
      |
      v
Random data
```

Random Source is introduced after the transformation itself is understood.

---

# 2. Flow Control and Flowgraph Utilities

| Block / Object | Importance | Status | What it does | First introduced / major use |
|---|---|---|---|---|
| **Throttle** | Essential | ✅ Used | Limits processing rate in software-only flowgraphs | Early chapters |
| **Variable** | Essential | ✅ Used | Stores reusable values and relationships | Early chapters |
| **Import** | Important | ✅ Used | Makes Python names/functions available to generated code | Chapter 14 |
| **Head** | Important | ✅ Used | Passes only a selected number of items | Chapters 10–11; finite PLL startup capture Chapter 21 |
| **Delay** | Important | ✅ Used | Delays a stream by selected samples | Chapter 11; multipath Chapter 19; one-sample CFO estimator delay Chapter 21 |

Variables increasingly express physical relationships rather than isolated constants:

```text
samples_per_bit = int(samp_rate / bit_rate)
sps             = int(samp_rate / symbol_rate)
```

This keeps the signal-processing relationship visible inside the flowgraph.

---

# 3. Mathematical Operations

| Block / Operation | Importance | Status | What it does | First introduced / major use |
|---|---|---|---|---|
| **Add** | Essential | ✅ Used | Adds streams sample by sample | Early chapters; channel/noise experiments |
| **Multiply** | Essential | ✅ Used | Multiplies streams sample by sample | Chapters 7–14; phase/CFO impairment Chapters 19–21 |
| **Divide** | Important | ✅ Used | Divides one stream by another | Chapter 7 |
| **Multiply Const** | Essential | ✅ Used | Multiplies every sample by a constant | Chapter 7; phase rotation and scaling Chapters 17–21 |
| **Add Const** | Important | ✅ Used | Adds a constant to every sample | Chapter 11; reused Chapters 13–16 |
| **Multiply Conjugate** | Important | ✅ Used | Multiplies one complex stream by the conjugate of the other | Chapter 21 |
| **Exponentiate Const Int** | Important | ✅ Used | Raises each sample to a fixed integer power | Chapter 21 |
| **Log10** | Important | ✅ Used | Calculates base-10 logarithm | Chapter 7 |
| **Abs** | Important | ✅ Used | Calculates absolute value | Chapter 13 |
| **Subtract** | Important | ⏳ Later | Subtracts streams | Later |

## 3.1 Multiply Conjugate

Chapter 21 gave Multiply Conjugate a central synchronization role.

If

```text
x = A exp(jθx)
y = B exp(jθy)
```

then

```text
x y* = AB exp(j(θx - θy))
```

so the resulting phase contains a **phase difference**, not a phase sum.

It was used for:

- known-reference carrier-phase measurement,
- measuring PLL phase error,
- adjacent-sample CFO estimation after fourth-power processing.

### Important distinction

```text
Multiply
   |
   v
phase addition
```

```text
Multiply Conjugate
   |
   v
phase difference
```

---

## 3.2 Exponentiate Const Int

Chapter 21 used **Exponentiate Const Int** with exponent `4` for QPSK.

For QPSK, fourth-power processing removes the fourfold data-dependent phase structure:

```text
QPSK + carrier error
        |
        v
Fourth power
        |
        v
QPSK data phase collapses
        |
        v
carrier phase/frequency information becomes easier to observe
```

The same symmetry also produces the familiar QPSK rotational ambiguity.

---

# 4. Complex-Signal and Type-Conversion Blocks

| Block | Importance | Status | What it does | First introduced / major use |
|---|---|---|---|---|
| **Float to Complex** | Essential | ✅ Used | Combines I and Q float streams into a complex stream | Early I/Q chapters; central Chapters 17–21 |
| **Complex to Real** | Essential | ✅ Used | Extracts the real/I component | Early I/Q chapters; PLL carrier comparison Chapter 21 |
| **Complex to Imag** | Essential | ✅ Used | Extracts the imaginary/Q component | Early I/Q chapters |
| **Complex to Mag** | Essential | ✅ Used | Calculates complex magnitude | Early I/Q chapters; reused Chapters 14, 17 |
| **Complex to Arg** | Essential | ✅ Used | Calculates complex phase | Early I/Q chapters; carrier-phase and CFO estimation Chapter 21 |
| **Complex to Mag²** | Essential | ✅ Used | Calculates squared magnitude | Chapter 6 |
| **Char to Float** | Important | ✅ Used | Converts signed byte/char samples to float | Chapter 11 |
| **UChar to Float** | Important | ✅ Used | Converts unsigned byte values to float | Chapter 15 |
| **Complex to Float** | Important | ⏳ Later | Separates complex stream into float components | Later |
| **Float to Char** | Important | ⏳ Later | Converts float values to byte/char form | Later |

## 4.1 Float to Complex

Chapter 17 gave Float to Complex an especially important communication role.

```text
I stream ----\
              >---- Float to Complex ----> s = I + jQ
Q stream ----/
```

The block does not "create QPSK" by itself. It simply combines the I and Q values chosen by the mapping.

---

# 5. Stream, Bit and Symbol Operations

| Block / Method | Importance | Status | What it does | First introduced / major use |
|---|---|---|---|---|
| **Stream to Vector** | Essential | ✅ Used | Groups stream items into vectors | Chapter 6 |
| **Keep 1 in N** | Important | ✅ Used | Keeps one item out of every N | Chapter 9; symbol-rate observation Chapters 18–20 |
| **Head** | Important | ✅ Used | Limits a stream to a finite number of items | Chapters 10–11; Chapter 21 |
| **Delay** | Important | ✅ Used | Delays a stream | Chapter 11; Chapters 19 and 21 |
| **Repeat** | Important | ✅ Used | Repeats each item a selected number of times | Chapter 15; rectangular symbol pulses Chapters 16–18 |
| **Repack Bits** | Essential | ✅ Used | Regroups meaningful bits into different item widths | Chapter 15; reused Chapter 17 |
| **Chunks to Symbols** | Essential | ✅ Used | Maps symbol indices to chosen symbol values | Chapter 16; central Chapters 17–21 |
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
Map an index to a chosen symbol value
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

---

# 6. Fourier and Spectrum Analysis

| Block / Method | Importance | Status | What it does | First introduced / major use |
|---|---|---|---|---|
| **FFT** | Essential | ✅ Used | Computes the DFT efficiently | Chapter 6 |
| **QT GUI Frequency Sink DFT/FFT view** | Essential | ✅ Used | Displays spectral location and bandwidth | Reused throughout; DFT-based CFO interpretation Chapter 21 |
| **IFFT** | Essential | ⏳ Later | Creates time-domain samples from frequency-domain bins | OFDM chapters |
| **Goertzel** | Important | ⏳ Later | Evaluates selected frequencies efficiently | Later |
| **Log Power FFT** | Important | ⏳ Later | Produces logarithmic spectral power | Later |

Chapter 21 reused the DFT viewpoint for CFO estimation after fourth-power processing.

```text
QPSK + CFO
    |
    v
Fourth power
    |
    v
carrier-like tone at approximately 4 × CFO
    |
    v
DFT / Frequency Sink
```

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
| **Low Pass Filter** | Essential | ✅ Used | Passes lower frequencies | Chapter 7; expanded Chapter 9; smoothing Chapter 18 |
| **High Pass Filter** | Essential | ✅ Used | Passes higher frequencies | Chapter 9 |
| **Band Pass Filter** | Essential | ✅ Used | Passes a selected band | Chapter 9; reused Chapter 13 |
| **Band Reject Filter** | Essential | ✅ Used | Rejects a selected band | Chapter 9 |
| **Decimating FIR Filter** | Essential | ✅ Used | FIR filtering with optional decimation | Chapters 9–11; RX RRC Chapter 18; manual equalizer Chapter 20 |
| **Interpolating FIR Filter** | Essential | ✅ Used | FIR filtering while increasing sample rate | Chapter 18; reused Chapters 19–21 |
| **DC Blocker** | Important | ✅ Used | Removes DC/very-low-frequency offset | Chapter 13 |
| **Linear Equalizer** | Essential receiver tool | ✅ Used | Adaptive FIR equalization of symbol streams | Chapter 20 |
| **Frequency Xlating FIR Filter** | Advanced | ⏳ Later | Frequency translation + filtering + decimation | Later receiver work |
| **FFT Filter** | Important | ⏳ Later | FIR filtering using FFT convolution | Later |
| **FFT Low Pass Filter** | Important | ⏳ Later | FFT-based low-pass filtering | Later |
| **IIR Filter** | Important | ⏳ Later | Infinite impulse response filtering | Later |
| **Single Pole IIR Filter** | Important | ⏳ Later | Simple recursive smoothing/filtering | Later |
| **Hilbert** | Advanced | ⏳ Later | Analytic-signal/quadrature processing | Discussed Chapter 13, not used as a completed experiment |
| **Generic Filterbank** | Advanced | ⏳ Later | Applies a bank of filters | Later |

## 8.1 Interpolating FIR Filter

Chapter 18 introduced the Interpolating FIR Filter for proper pulse shaping.

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

## 8.2 Decimating FIR Filter with Decimation = 1

With

```text
Decimation: 1
```

the block behaves as an FIR filter without changing the stream rate.

This role was used for receive matched filtering and again in Chapter 20 for manually constructed equalization.

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
| **Decimating FIR Filter** | Essential | ✅ Used | Correlation/matched filtering with chosen taps | Chapter 11 |
| **Add Const** | Important | ✅ Used | Moves a threshold relative to zero | Chapter 11 |
| **Binary Slicer** | Essential | ✅ Used | Converts thresholded samples into binary decisions | Chapter 11 |
| **Char to Float** | Important | ✅ Used | Converts decisions for display | Chapter 11 |
| **Moving Average** | Essential | ✅ Used | Accumulation/smoothing where useful | Chapter 11 |
| **Multiply Conjugate / conjugate-product idea** | Important | ✅ Used | Relative phase measurement | Chapter 21 |
| **Correlation Estimator** | Essential receiver tool | ✅ Used | Locates a known complex training sequence and produces correlation-related tags | Chapter 20 |
| **Correlate Access Code** | Important | 🔜 Planned | Detects known bit patterns in streams | Expected Chapter 23 |

## 10.1 Correlation Estimator

Chapter 20 reused the correlation ideas of Chapter 11 for training-assisted equalization.

```text
Received symbol stream
        |
        v
Correlation Estimator
        |
        v
training-start information / corr_est tag
        |
        v
Linear Equalizer
```

Important settings in the completed experiment included:

```text
Symbols:             training_symbols
Samples per Symbol:  1
Tag marking delay:   1
Threshold:           0.5
Threshold Method:    Absolute
```

The Correlation Estimator **locates** the known sequence. It does not equalize the channel.

---

# 11. QT GUI Visualization

| Block | Importance | Status | Main use |
|---|---|---|---|
| **QT GUI Time Sink** | Essential | ✅ Used | Time-domain waveform and loop-state inspection |
| **QT GUI Frequency Sink** | Essential | ✅ Used | Spectrum inspection; FLL before/after comparison Chapter 21 |
| **QT GUI Constellation Sink** | Essential | ✅ Used | I/Q-plane inspection; central Chapters 17–21 |
| **QT GUI Number Sink** | Important | ✅ Used | Numerical measurement display; phase and CFO estimates Chapter 21 |
| **QT GUI Vector Sink** | Important | ✅ Used | Vector-valued display |
| **QT GUI Waterfall Sink** | Important | ✅ Used | Spectrum-versus-time display |
| **QT GUI Histogram Sink** | Important | ⏳ Later | Sample distribution |
| **QT GUI Eye Sink** | Important | ⏳ Later / optional | Dedicated eye-diagram display where available |
| **QT GUI Matrix Sink** | Specialized | ➖ Optional | Matrix-like data |

## 11.1 Eye Diagram Note

Chapter 18 did not mark QT GUI Eye Sink as used.

The completed eye-diagram experiment recorded matched-filter output with a File Sink and used a small external Python plotting script.

---

# 12. QT GUI Controls

| Block | Importance | Status | What it does |
|---|---|---|---|
| **QT GUI Range** | Essential | ✅ Used | Interactive numerical control |
| **QT GUI Chooser** | Important | ✅ Used | Selects predefined values |
| **QT GUI Push Button** | Important | ⏳ Later | Runtime action |
| **QT GUI Entry** | Important | ⏳ Later | Runtime numerical/text entry |
| **QT GUI Check Box** | Important | ⏳ Later | Boolean control |

QT GUI Range has been reused for bit rate, modulation parameters, channel impairments, phase offset, CFO, noise amplitude, and loop-related experiments.

---

# 13. Resampling and Rate Change

| Block / Method | Importance | Status | What it does |
|---|---|---|---|
| **Decimating FIR Filter** | Essential | ✅ Used | Filters with optional integer downsampling |
| **Keep 1 in N** | Important | ✅ Used | Direct selection/downsampling without anti-alias filtering |
| **Repeat** | Important | ✅ Used | Duplicates items; rectangular hold |
| **Interpolating FIR Filter** | Essential | ✅ Used | Filters while increasing sample rate |
| **Rational Resampler** | Essential | ⏳ Later | Rational sample-rate conversion |
| **Fractional Resampler** | Advanced | ⏳ Later | Non-integer resampling |

Chapter 18 marks the important boundary between **repetition for a rectangular hold** and **proper pulse-shaping interpolation**.

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
| **UChar to Float** | Important | ✅ Used | Data-type conversion for display |
| **Repeat** | Important | ✅ Used | Rectangular bit/symbol duration |
| **Repack Bits** | Essential | ✅ Used | Groups bits into symbol indices |
| **Chunks to Symbols** | Essential | ✅ Used | Maps indices to PAM/I/Q values |
| **Float to Complex** | Essential | ✅ Used | Combines I and Q coordinates |
| **Binary Slicer** | Essential | ✅ Used | Binary hard decisions |
| **Interpolating FIR Filter** | Essential | ✅ Used | RRC pulse shaping |
| **RRC taps** | Essential | ✅ Used | Root-raised-cosine pulse design |
| **Linear Equalizer** | Essential receiver tool | ✅ Used | Adaptive channel equalization |
| **Adaptive Algorithm (LMS)** | Essential receiver object | ✅ Used | Updates equalizer taps from error information |
| **Constellation Rect. Object** | Important receiver object | ✅ Used | Defines valid normalized QPSK decision points |
| **Correlation Estimator** | Essential receiver tool | ✅ Used | Finds known training sequences and marks them with tags |
| **Constellation Modulator** | Important | ⏳ Later | Ready-made digital modulation |
| **Constellation Decoder** | Important | ⏳ Later | Ready-made symbol decoding |
| **Differential Encoder** | Important | ⏳ Later | Differential symbol encoding |
| **Differential Decoder** | Important | ⏳ Later | Differential symbol decoding |
| **Correlate Access Code** | Important | 🔜 Planned | Packet/access-code detection |
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
Carrier mismatch -> phase/frequency estimation -> PLL/Costas/FLL recovery
```

This progression is more important than memorizing individual block names.

---

# 16. Synchronization and Carrier Recovery

| Block / Method | Importance | Status | What it does | First use / note |
|---|---|---|---|---|
| **PLL Carrier Regeneration** | Important | ✅ Used | Generates a carrier reference that follows the input carrier | Chapter 21 |
| **Costas Loop** | Essential | ✅ Used | Modulation-aware feedback carrier recovery for PSK | Chapter 21 |
| **FLL Band-Edge** | Essential receiver tool | ✅ Used | Feedback carrier-frequency recovery using pulse-shaped spectral edges | Chapter 21 |
| **Multiply Conjugate** | Important | ✅ Used | Relative phase / phase-increment measurement | Chapter 21 |
| **Exponentiate Const Int** | Important | ✅ Used | M-th-power modulation removal for QPSK | Chapter 21 |
| **PLL Carrier Tracking** | Important | ⏳ Later / explored | Tracks/downconverts a carrier; explored during development but not central to final chapter path |
| **PLL Frequency Detector** | Advanced | ⏳ Later | Exposes PLL frequency-detection behaviour | Later / advanced synchronization |
| **Symbol Sync** | Essential | 🔜 Planned | Symbol timing synchronization | Chapter 22 |
| **Clock Recovery MM** | Important | ⏳ Later | Alternative clock-recovery method | Later |
| **M-th power methods** | Important concept | ✅ Used | Remove M-PSK data symmetry for phase/frequency estimation | Chapter 21 |
| **DFT-based CFO interpretation** | Important concept | ✅ Used | Estimates CFO from spectral location after modulation removal | Chapter 21 |

## 16.1 PLL Carrier Regeneration

Chapter 21 used PLL Carrier Regeneration to make feedback lock visible with a clean complex carrier.

Important ideas included:

- phase detector,
- loop filter,
- oscillator/NCO correction,
- acquisition,
- lock,
- tracking,
- loop bandwidth.

A finite startup segment was captured with `Head` + `File Sink` and plotted externally.

## 16.2 Costas Loop

For QPSK, the completed experiment used:

```text
Order:          4
Loop Bandwidth: pi/100
Use SNR:        No
```

`Order = 4` identifies the QPSK modulation structure. It does **not** mean a fourth-order PLL.

The Costas Loop restored a stable QPSK constellation but can retain the normal QPSK rotational ambiguity.

## 16.3 FLL Band-Edge

The final frequency-recovery experiment operated on the **oversampled pulse-shaped signal**, before symbol-rate sampling.

Important settings were:

```text
Samples per Symbol:     32
Filter Rolloff Factor:  0.35
Prototype Filter Size:  45
Loop Bandwidth:         2*pi/1000
```

The block successfully drove the tested `+2 kHz` and `-2 kHz` CFOs back close to zero frequency.

The larger `+8 kHz` test demonstrated that acquisition capability is finite and depends on the waveform and loop configuration.

### Important distinction

```text
FLL
=
general frequency-feedback architecture
```

```text
Band-edge frequency detector
=
one method for generating frequency error
```

```text
FLL Band-Edge
=
GNU Radio block implementing band-edge-based feedback frequency recovery
```

---

# 17. Channel and Impairment Simulation

| Block / Method | Importance | Status | First use / note |
|---|---|---|---|
| **Noise Source + Add** | Essential concept | ✅ Used | Manual AWGN channel in several chapters |
| **Multiply Const / controlled gain** | Essential concept | ✅ Used | Attenuation experiments Chapter 19 |
| **Complex phasor multiplication** | Essential concept | ✅ Used | Phase and frequency offset experiments Chapters 19 and 21 |
| **Delay + Add / manual multipath** | Essential concept | ✅ Used | Fractional/one-symbol echoes Chapter 19 |
| **Channel Model** | Essential | ✅ Used | Combined controlled channel impairments Chapter 19 |
| **Channel Model Epsilon parameter** | Important concept | ✅ Used | Sample-rate mismatch Chapter 19 |
| **Dynamic Channel Model** | Advanced | ⏳ Later | Time-varying channel simulation |
| **Frequency Selective Fading Model** | Advanced | ⏳ Later | Later |
| **Selective Fading Model** | Advanced | ⏳ Later | Later |

## 17.1 Channel Model

Chapter 19 moved from manually introduced impairments to GNU Radio's Channel Model.

The chapter used it as a controlled way to combine impairments such as:

- noise voltage,
- frequency offset,
- timing/sample-rate mismatch through `epsilon`,
- multipath taps.

The teaching rule remains:

> **Understand each impairment manually before relying on a combined channel block.**

---

# 18. Equalization and Adaptive Receiver Processing

| Block / Object / Method | Importance | Status | Role |
|---|---|---|---|
| **Manual FIR equalizer with Decimating FIR Filter** | Essential concept | ✅ Used | Known-channel inverse-filter intuition |
| **Linear Equalizer** | Essential | ✅ Used | Adaptive FIR equalization |
| **Adaptive Algorithm (LMS)** | Essential | ✅ Used | LMS coefficient adaptation |
| **Constellation Rect. Object** | Important | ✅ Used | Defines valid QPSK decision points |
| **Correlation Estimator** | Essential | ✅ Used | Detects known training sequence |
| **Stream Tags / correlation tags** | Essential concept | ✅ Used | Marks detected training position for downstream equalization |

## 18.1 Linear Equalizer

Important completed settings included:

```text
Num. Taps:                 5
Input Samples per Symbol:  1
Adaptive Algorithm Object: lms
Training Sequence:         []
Adapt After Training:      True
```

The key distinction is:

> **The Linear Equalizer is the filter. The Adaptive Algorithm object supplies the coefficient-update rule.**

## 18.2 Adaptive Algorithm (LMS)

The LMS step size `mu` controls how strongly each observed error changes the equalizer coefficients.

```text
mu = 0        -> no adaptation
small mu      -> cautious, slower adaptation
larger mu     -> more aggressive, faster adaptation
```

The final experiments demonstrated the physical meaning of adaptation speed without claiming that arbitrarily large step sizes are safe.

## 18.3 Constellation Rect. Object

Chapter 20 used normalized QPSK decision points near:

```text
(+/-0.707, +/-0.707)
```

The object is not merely a plotting configuration. It tells the adaptive receiver which complex symbol decisions are valid.

## 18.4 Correlation Estimator and Tags

The Correlation Estimator locates a known training sequence.

The resulting correlation tag identifies where downstream training-assisted equalization should begin.

This introduced an important distinction:

```text
Detection
=
Was the known sequence found?
```

```text
Alignment
=
Does the resulting tag line up with the intended training-symbol position?
```

Detailed tag architecture remains a later topic.

---

# 19. File and Data Storage

| Block / Method | Importance | Status | First use / note |
|---|---|---|---|
| **File Sink** | Essential | ✅ Used | Chapter 18 eye samples; Chapter 21 PLL phase-error capture |
| **External Python plotting scripts** | Important workflow | ✅ Used | Eye diagrams Chapter 18; PLL transient plots Chapter 21 |
| **File Source** | Essential | ⏳ Later | Reads raw stored samples |
| **WAV File Source** | Important | ⏳ Later | Audio files |
| **WAV File Sink** | Important | ⏳ Later | Audio files |
| **Metadata File Source** | Advanced | ⏳ Later | Later |
| **Metadata File Sink** | Advanced | ⏳ Later | Later |

## 19.1 File Sink and External Analysis

The File Sink stores the stream without changing it.

```text
GNU Radio processing
        |
        v
File Sink
        |
        v
raw .dat samples
        |
        v
external Python visualization
```

In Chapter 21, Python did **not** simulate the PLL. It only plotted phase-error samples produced by GNU Radio.

---

# 20. Message, Tags and PDU Processing

| Block / Feature | Importance | Status |
|---|---|---|
| **Stream Tags** | Essential | ✅ Used conceptually | Chapter 20 training/correlation alignment |
| **Tagged Streams** | Essential | ⏳ Later | Full tagged-stream architecture later |
| **Message Debug** | Important | ⏳ Later |
| **Tagged Stream to PDU** | Advanced | ⏳ Later |
| **PDU to Tagged Stream** | Advanced | ⏳ Later |
| **Socket PDU** | Advanced | ⏳ Later |

Chapter 20 used tags because the Correlation Estimator needed to communicate training-sequence location to downstream processing.

The complete tag/PDU architecture is deliberately postponed.

---

# 21. Custom and Advanced Processing

| Block / Feature | Importance | Status | First use / note |
|---|---|---|---|
| **Embedded Python Block** | Important | ✅ Used | Chapter 16 decision/detection experimentation |
| **External Python plotting scripts** | Important workflow | ✅ Used | Chapters 18 and 21 |
| **Hierarchical Block** | Important | ⏳ Later | Later |
| **PDUs** | Important | ⏳ Later | Later |

An **Embedded Python Block** runs inside the GNU Radio flowgraph.

An **external Python plotting script** reads saved data outside the flowgraph.

These are not the same thing.

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

Several operations now used in the digital receiver can look superficially similar.

```text
Repeat
    |
    v
Duplicate values in time
```

```text
Interpolating FIR Filter
    |
    v
Increase sample rate while constructing a filtered pulse shape
```

```text
Keep 1 in N
    |
    v
Select periodic samples
```

```text
Decimating FIR Filter
    |
    v
Filter, with optional rate reduction
```

```text
Multiply
    |
    v
Multiply complex samples; phases add
```

```text
Multiply Conjugate
    |
    v
Compare complex phases; one phase is subtracted
```

```text
Linear Equalizer
    |
    v
Apply adaptive receiver filtering
```

```text
Adaptive Algorithm (LMS)
    |
    v
Decide how the equalizer coefficients change
```

```text
Correlation Estimator
    |
    v
Find a known training sequence
```

```text
Costas Loop
    |
    v
Track carrier phase/frequency with modulation-aware feedback
```

```text
FLL Band-Edge
    |
    v
Track carrier frequency from pulse-shaped spectral-edge information
```

The correct habit remains:

> **What physical operation does the receiver need?**

Then:

> **Which GNU Radio block or object performs that operation?**

---

# 24. Important Conceptual Roles Through Chapter 21

| Need | GNU Radio tool / method |
|---|---|
| Generate a known sinusoid or rotating phasor | Signal Source |
| Generate controlled symbols | Vector Source |
| Generate random digital data | Random Source |
| Add controlled noise | Noise Source + Add |
| Group bits into symbols | Repack Bits |
| Map indices to amplitudes/I/Q | Chunks to Symbols |
| Combine I and Q | Float to Complex |
| Pulse-shape symbols | Interpolating FIR Filter + RRC taps |
| Matched-filter at receiver | Decimating FIR Filter |
| Simulate combined channel impairments | Channel Model |
| Create manual multipath | Delay + scaling + Add |
| Perform manual equalization | FIR taps in Decimating FIR Filter |
| Adapt an equalizer | Linear Equalizer + LMS object |
| Define valid QPSK decisions | Constellation Rect. Object |
| Locate a known training sequence | Correlation Estimator |
| Measure relative complex phase | Multiply Conjugate + Complex to Arg |
| Remove QPSK data symmetry | Exponentiate Const Int with exponent 4 |
| Regenerate/track a clean carrier | PLL Carrier Regeneration |
| Recover QPSK carrier phase | Costas Loop |
| Estimate CFO from phase increment | Delay + Multiply Conjugate + Complex to Arg |
| Interpret CFO spectrally | Fourth power + Frequency Sink/DFT |
| Recover carrier frequency automatically | FLL Band-Edge |
| Record transient data | Head + File Sink |
| Inspect time-domain behaviour | QT GUI Time Sink |
| Inspect spectrum | QT GUI Frequency Sink |
| Inspect constellation geometry | QT GUI Constellation Sink |
| Display numerical estimates | QT GUI Number Sink |

---

# 25. Blocks and Features Used So Far

At the end of Chapter 21, the working GNU Radio toolbox includes:

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
| Char to Float | ✅ |
| UChar to Float | ✅ |
| Stream to Vector | ✅ |
| Keep 1 in N | ✅ |
| Repeat | ✅ |
| Repack Bits | ✅ |
| Chunks to Symbols | ✅ |
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
| Binary Slicer | ✅ |
| Quadrature Demod | ✅ |
| Channel Model | ✅ |
| Linear Equalizer | ✅ |
| Adaptive Algorithm (LMS) | ✅ |
| Constellation Rect. Object | ✅ |
| Correlation Estimator | ✅ |
| Stream Tags / correlation tags | ✅ conceptually |
| PLL Carrier Regeneration | ✅ |
| Costas Loop | ✅ |
| FLL Band-Edge | ✅ |
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

# 26. Chapter-by-Chapter GNU Radio Growth Through Chapter 21

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
| 20 | Manual and adaptive equalization, Linear Equalizer, LMS, Constellation Rect. Object, training and Correlation Estimator |
| 21 | Multiply Conjugate, M-th power processing, PLL carrier regeneration, Costas Loop, CFO estimation and FLL Band-Edge |

This table should always follow the **completed manuscript**, not an old chapter plan.

---

# 27. What Comes Next?

Chapter 21 ends with carrier phase and frequency synchronization understood separately.

The next unresolved receiver question is:

> **Even if the carrier is correct, how does the receiver know exactly when to sample each symbol?**

Chapter 22 moves into **Clock and Symbol Timing Synchronization**.

The expected major GNU Radio addition is:

- **Symbol Sync**

The chapter should first make timing error visible before introducing automatic recovery.

A likely progression is:

```text
Correct carrier
      |
      v
Wrong sampling instant
      |
      v
Early / late symbol samples
      |
      v
Timing-error information
      |
      v
Symbol Sync
      |
      v
Recovered symbol timing
```

`Clock Recovery MM` may be discussed later where it genuinely adds value rather than being introduced merely because the block exists.

The teaching rule remains:

> **Introduce the operation because the communication problem requires it, not because a GNU Radio block happens to exist.**
