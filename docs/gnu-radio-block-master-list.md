# GNU Radio Block Master List

**Updated through Chapter 18: Pulse Shaping and Matched Filtering**

---

## Why This Document Exists

GNU Radio contains a very large number of blocks.

Trying to learn all of them at once would not be useful.

This document therefore does **not** attempt to list every block in GNU Radio. It records the blocks, controls, tap generators, and important GNU Radio operations that matter to the learning path of this book.

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
| **Signal Source** | Essential | ✅ Used | Generates periodic test signals | Early chapters |
| **Noise Source** | Essential | ✅ Used | Generates Gaussian and other noise | Chapter 7; reused Chapters 14, 16–18 |
| **Constant Source** | Important | ✅ Used | Produces a constant stream | Chapter 13 |
| **Vector Source** | Important | ✅ Used | Produces a predefined sequence | Chapter 10; controlled digital patterns Chapters 15–18 |
| **Random Source** | Essential | ✅ Used | Generates random integer data | Chapter 15; reused Chapters 16–18 |
| **VCO** | Important | ✅ Used | Frequency-controlled oscillator | Chapter 14 |
| **VCO (Complex)** | Important | ✅ Used | Complex frequency-controlled oscillator | Chapter 14 |
| **File Source** | Important | ⏳ Later | Reads stored sample streams | Later |
| **Fast Noise Source** | Important | ⏳ Later | Efficient noise generation | Later |
| **GLFSR Source** | Important | ⏳ Later | Generates pseudo-random sequences | Later digital communications |

## 1.1 Controlled Data Before Random Data

Vector Source remains especially useful in digital-communication chapters because a known sequence makes transformations easy to verify.

```text
Known sequence
      |
      v
Verify grouping/mapping/decision
      |
      v
Random Source
```

Random Source is introduced only after the transformation is understood.

---

# 2. Flow Control and Flowgraph Utilities

| Block / Object | Importance | Status | What it does | First introduced / major use |
|---|---|---|---|---|
| **Throttle** | Essential | ✅ Used | Limits processing rate in software-only flowgraphs | Early chapters |
| **Variable** | Essential | ✅ Used | Stores reusable values and relationships | Early chapters |
| **Import** | Important | ✅ Used | Makes Python names/functions available to generated code | Chapter 14 |
| **Head** | Important | ✅ Used | Passes only a selected number of items | Chapters 10–11 |
| **Delay** | Important | ✅ Used | Delays a stream by a selected number of samples | Chapter 11 |

Variables increasingly express relationships rather than isolated constants:

```text
samples_per_bit = int(samp_rate / bit_rate)
sps             = int(samp_rate / symbol_rate)
```

This makes the signal-processing relationship visible inside the flowgraph.

---

# 3. Mathematical Operations

| Block | Importance | Status | What it does | First introduced / major use |
|---|---|---|---|---|
| **Add** | Essential | ✅ Used | Adds streams sample by sample | Early chapters; channel/noise experiments |
| **Multiply** | Essential | ✅ Used | Multiplies streams sample by sample | Chapters 7–14 |
| **Divide** | Important | ✅ Used | Divides one stream by another | Chapter 7 |
| **Multiply Const** | Essential | ✅ Used | Scales every sample by a constant | Chapter 7; reused Chapters 14, 17 |
| **Add Const** | Important | ✅ Used | Adds a constant to every sample | Chapter 11; reused Chapters 13–16 |
| **Log10** | Important | ✅ Used | Calculates base-10 logarithm | Chapter 7 |
| **Abs** | Important | ✅ Used | Calculates absolute value | Chapter 13 |
| **Subtract** | Important | ⏳ Later | Subtracts streams | Later |

---

# 4. Complex-Signal and Type-Conversion Blocks

| Block | Importance | Status | What it does | First introduced / major use |
|---|---|---|---|---|
| **Float to Complex** | Essential | ✅ Used | Combines I and Q float streams into a complex stream | Early I/Q chapters; central again Chapter 17 |
| **Complex to Real** | Essential | ✅ Used | Extracts the real/I component | Early I/Q chapters |
| **Complex to Imag** | Essential | ✅ Used | Extracts the imaginary/Q component | Early I/Q chapters |
| **Complex to Mag** | Essential | ✅ Used | Calculates complex magnitude | Early I/Q chapters; reused Chapters 14, 17 |
| **Complex to Arg** | Essential | ✅ Used | Calculates complex phase | Early I/Q chapters; reused Chapter 17 |
| **Complex to Mag²** | Essential | ✅ Used | Calculates squared magnitude | Chapter 6 |
| **Char to Float** | Important | ✅ Used | Converts signed byte/char samples to float | Chapter 11 |
| **UChar to Float** | Important | ✅ Used | Converts unsigned byte values to float | Chapter 15 |
| **Complex to Float** | Important | ⏳ Later | Separates a complex stream into float components | Later |
| **Float to Char** | Important | ⏳ Later | Converts float values to byte/char form | Later |

## 4.1 Float to Complex in Chapter 17

Chapter 17 gave Float to Complex an especially important conceptual role.

```text
I stream ----\
              >---- Float to Complex ----> s = I + jQ
Q stream ----/
```

This made QPSK and 16-QAM geometry visible without hiding the mapping inside a ready-made digital modulator.

The block does not "create QPSK" by itself. It simply combines the I and Q coordinates selected by the experiment.

---

# 5. Stream, Bit and Symbol Operations

| Block | Importance | Status | What it does | First introduced / major use |
|---|---|---|---|---|
| **Stream to Vector** | Essential | ✅ Used | Groups stream items into vectors | Chapter 6 |
| **Keep 1 in N** | Important | ✅ Used | Keeps one item out of every N | Chapter 9 |
| **Head** | Important | ✅ Used | Limits a stream to a finite number of items | Chapters 10–11 |
| **Delay** | Important | ✅ Used | Delays a stream | Chapter 11 |
| **Repeat** | Important | ✅ Used | Repeats each item a selected number of times | Chapter 15; rectangular symbol pulses Chapters 16–18 |
| **Repack Bits** | Essential | ✅ Used | Regroups meaningful bits into different item widths | Chapter 15; reused Chapter 17 |
| **Chunks to Symbols** | Essential | ✅ Used | Maps symbol indices to chosen symbol values | Chapter 16; central Chapters 17–18 |
| **Vector to Stream** | Essential | ⏳ Later | Converts vectors back into a stream | Later OFDM/vector work |
| **Map** | Important | ⏳ Later | General integer/value remapping | Later |

## 5.1 Repeat

Repeat gives each input item a sampled duration by duplicating it.

In Chapter 15 it made bit timing visible.

In Chapters 16 and 17 it created simple rectangular symbol waveforms.

In Chapter 18 that same rectangular construction became the starting point for asking why practical pulse shaping is needed.

### Important distinction

```text
Repeat
    |
    v
Duplicate the same item in time
```

Repeat is useful pedagogically, but it is **not** a proper band-limited interpolation filter.

Chapter 18 makes that distinction explicit by introducing the Interpolating FIR Filter.

## 5.2 Repack Bits

Repack Bits changes how meaningful bits are grouped into stream items.

```text
Bits
  |
  v
Repack Bits
  |
  v
Symbol indices
```

The output values are labels until another operation maps them to physical symbol values.

## 5.3 Chunks to Symbols

Chunks to Symbols became central in Chapter 16.

It treats each input value as an index into a symbol table.

For 4-PAM:

```text
0 -> -3
1 -> -1
2 -> +1
3 -> +3
```

For BPSK:

```text
0 -> -1
1 -> +1
```

Chapter 17 reused the same idea separately on I and Q to build QPSK and 16-QAM manually.

### Important distinction

Chunks to Symbols performs **mapping**.

It does not group bits, repeat symbols in time, add noise, or perform pulse shaping.

---

# 6. Fourier and Spectrum Analysis

| Block | Importance | Status | What it does | First introduced |
|---|---|---|---|---|
| **FFT** | Essential | ✅ Used | Computes the DFT efficiently | Chapter 6 |
| **IFFT** | Essential | ⏳ Later | Creates time-domain samples from frequency-domain bins | OFDM chapters |
| **Goertzel** | Important | ⏳ Later | Evaluates selected frequencies efficiently | Later |
| **Log Power FFT** | Important | ⏳ Later | Produces logarithmic spectral power | Later |

Spectrum analysis is reused throughout the book to connect time-domain behaviour to bandwidth, sidebands, noise, modulation, and pulse shaping.

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
| **Low Pass Filter** | Essential | ✅ Used | Passes lower frequencies | Chapter 7; expanded Chapter 9; smoothing Chapter 18 |
| **High Pass Filter** | Essential | ✅ Used | Passes higher frequencies | Chapter 9 |
| **Band Pass Filter** | Essential | ✅ Used | Passes a selected band | Chapter 9; reused Chapter 13 |
| **Band Reject Filter** | Essential | ✅ Used | Rejects a selected band | Chapter 9 |
| **Decimating FIR Filter** | Essential | ✅ Used | FIR filtering with optional decimation | Chapters 9–11; RX RRC/matched filter Chapter 18 |
| **Interpolating FIR Filter** | Essential | ✅ Used | FIR filtering while increasing sample rate | Chapter 18 |
| **DC Blocker** | Important | ✅ Used | Removes DC/very-low-frequency offset | Chapter 13 |
| **Frequency Xlating FIR Filter** | Advanced | ⏳ Later | Frequency translation + filtering + decimation | Later receiver work |
| **FFT Filter** | Important | ⏳ Later | FIR filtering using FFT convolution | Later |
| **FFT Low Pass Filter** | Important | ⏳ Later | FFT-based low-pass filtering | Later |
| **IIR Filter** | Important | ⏳ Later | Infinite impulse response filtering | Later |
| **Single Pole IIR Filter** | Important | ⏳ Later | Simple recursive smoothing/filtering | Later |
| **Hilbert** | Advanced | ⏳ Later | Analytic-signal/quadrature processing | Discussed Chapter 13, not used as a completed experiment |
| **Generic Filterbank** | Advanced | ⏳ Later | Applies a bank of filters | Later |

## 8.1 Interpolating FIR Filter

Chapter 18 introduced the Interpolating FIR Filter for practical pulse shaping.

It performs two related operations:

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

For RRC pulse shaping, the interpolation factor was the number of samples per symbol.

### Important distinction

This is not the same operation as Repeat.

Repeat creates a rectangular hold by duplicating values.

The Interpolating FIR Filter constructs the waveform according to the selected FIR pulse shape.

## 8.2 Decimating FIR Filter with Decimation = 1

Chapter 18 reused the Decimating FIR Filter as the receive RRC/matched filter.

With

```text
Decimation: 1
```

the block does not reduce the sample rate. It behaves as an FIR filter with one output item per input item.

The name describes what the block *can* do, not what it must do in every experiment.

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

## 9.1 Root-Raised-Cosine Taps

Chapter 18 used:

```python
firdes.root_raised_cosine(
    gain,
    samp_rate,
    symbol_rate,
    alpha,
    ntaps
)
```

Important design quantities include:

- gain,
- sample rate,
- symbol rate,
- roll-off factor `alpha`,
- number of taps.

The transmitter and receiver RRC filters together form the intended overall raised-cosine response.

---

# 10. Correlation, Detection and Decisions

| Block / Operation | Importance | Status | Role |
|---|---|---|---|
| **Decimating FIR Filter** | Essential | ✅ Used | Correlation/matched filtering with selected taps |
| **Add Const** | Important | ✅ Used | Moves a threshold relative to zero |
| **Binary Slicer** | Essential | ✅ Used | Converts thresholded samples into binary decisions |
| **Char to Float** | Important | ✅ Used | Converts decisions for float-domain display |
| **Delay** | Important | ✅ Used | Represents sample delay |
| **Moving Average** | Essential | ✅ Used | Accumulation/smoothing where useful |
| **Conjugate operation** | Important | Concept introduced | Required for general complex correlation/matched filtering |
| **Correlate Access Code** | Important | ⏳ Later | Detects known bit patterns in streams |

Chapter 16 reused threshold/decision ideas for PAM hard decisions.

Chapter 18 returned to matched filtering from a communication-pulse perspective: the receive RRC is matched to the transmitted RRC pulse and improves the SNR at the correct decision instant in AWGN.

---

# 11. QT GUI Visualization

| Block | Importance | Status | Main use |
|---|---|---|---|
| **QT GUI Time Sink** | Essential | ✅ Used | Time-domain waveform inspection |
| **QT GUI Frequency Sink** | Essential | ✅ Used | Spectrum inspection |
| **QT GUI Constellation Sink** | Essential | ✅ Used | I/Q-plane inspection; central Chapter 17 |
| **QT GUI Number Sink** | Important | ✅ Used | Numerical measurement display |
| **QT GUI Vector Sink** | Important | ✅ Used | Vector-valued display |
| **QT GUI Waterfall Sink** | Important | ✅ Used | Spectrum-versus-time display |
| **QT GUI Histogram Sink** | Important | ⏳ Later | Sample distribution |
| **QT GUI Eye Sink** | Important | ⏳ Later / optional | Dedicated eye-diagram display where available |
| **QT GUI Matrix Sink** | Specialized | ➖ Optional | Matrix-like data |

## 11.1 Eye Diagram Note

Chapter 18 did **not** mark QT GUI Eye Sink as used.

The completed eye-diagram experiment recorded the matched-filter output with a File Sink and used a small Python script to overlay two-symbol windows.

That choice keeps the experiment reproducible without depending on a specialized eye sink.

---

# 12. QT GUI Controls

| Block | Importance | Status | What it does |
|---|---|---|---|
| **QT GUI Range** | Essential | ✅ Used | Interactive numerical control |
| **QT GUI Chooser** | Important | ✅ Used | Selects predefined values |
| **QT GUI Push Button** | Important | ⏳ Later | Runtime action |
| **QT GUI Entry** | Important | ⏳ Later | Runtime numerical/text entry |
| **QT GUI Check Box** | Important | ⏳ Later | Boolean control |

QT GUI Range has been reused for bit rate, modulation parameters, phase/amplitude experiments, and noise amplitude.

---

# 13. Resampling and Rate Change

| Block / Method | Importance | Status | What it does |
|---|---|---|---|
| **Decimating FIR Filter** | Essential | ✅ Used | Filters with optional integer downsampling |
| **Keep 1 in N** | Important | ✅ Used | Direct downsampling without anti-alias filtering |
| **Repeat** | Important | ✅ Used | Duplicates items; rectangular hold |
| **Interpolating FIR Filter** | Essential | ✅ Used | Filters while increasing sample rate |
| **Rational Resampler** | Essential | ⏳ Later | Rational sample-rate conversion |
| **Fractional Resampler** | Advanced | ⏳ Later | Non-integer resampling |

Chapter 18 is the important boundary between **repetition for visualization/rectangular pulses** and **proper interpolation with a pulse-shaping filter**.

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

# 15. Digital Communication Blocks and Methods

| Block / Method | Importance | Status | First use / role |
|---|---|---|---|
| **Vector Source** | Important | ✅ Used | Controlled bits/symbols |
| **Random Source** | Essential | ✅ Used | Random binary/symbol data |
| **UChar to Float** | Important | ✅ Used | Data-type conversion for display |
| **Repeat** | Important | ✅ Used | Rectangular bit/symbol duration |
| **Repack Bits** | Essential | ✅ Used | Groups bits into symbol indices |
| **Chunks to Symbols** | Essential | ✅ Used | Maps indices to PAM/I/Q values |
| **Float to Complex** | Essential | ✅ Used | Combines I and Q symbol coordinates |
| **Binary Slicer** | Essential | ✅ Used | Binary hard decisions |
| **Interpolating FIR Filter** | Essential | ✅ Used | RRC pulse shaping |
| **RRC taps** | Essential | ✅ Used | Root-raised-cosine pulse design |
| **Constellation Modulator** | Important | ⏳ Later | Ready-made digital modulation |
| **Constellation Decoder** | Important | ⏳ Later | Ready-made symbol decoding |
| **Differential Encoder** | Important | ⏳ Later | Differential symbol encoding |
| **Differential Decoder** | Important | ⏳ Later | Differential symbol decoding |
| **Correlate Access Code** | Important | ⏳ Later | Detects known bit patterns |
| **Additive Scrambler** | Important | ⏳ Later | Scrambles data sequences |

## 15.1 Digital Communication Progression

Chapter 15:

```text
Bits
  |
  v
Repack Bits
  |
  v
Symbol indices
```

Chapter 16:

```text
Symbol indices
      |
      v
Chunks to Symbols
      |
      v
PAM amplitudes
      |
      v
Decision thresholds
```

Chapter 17:

```text
I symbol values ----\
                     >---- I + jQ ----> constellation
Q symbol values ----/
```

Chapter 18:

```text
Symbols
   |
   v
RRC pulse shaping
   |
   v
Channel noise
   |
   v
Matched RRC filtering
   |
   v
Symbol sampling / eye
```

This progression is more important than memorizing individual block names.

---

# 16. Synchronization

| Block | Importance | Status |
|---|---|---|
| **Symbol Sync** | Essential | 🔜 Planned / later digital receiver |
| **Clock Recovery MM** | Important | ⏳ Later |
| **Costas Loop** | Essential | ⏳ Later |
| **PLL Carrier Tracking** | Important | ⏳ Later |
| **PLL Frequency Detector** | Advanced | ⏳ Later |
| **FLL Band-Edge** | Advanced | ⏳ Later |

Through Chapter 18, symbol timing is controlled/known.

The eye-diagram discussion makes clear why a real receiver eventually needs timing recovery, but no timing-recovery block has yet been used.

---

# 17. Channel and Impairment Simulation

| Block / Method | Importance | Status | First use / note |
|---|---|---|---|
| **Noise Source + Add** | Essential concept | ✅ Used | Manual AWGN channel in several chapters |
| **Channel Model** | Essential | 🔜 Planned | Chapter 19 |
| **Dynamic Channel Model** | Advanced | ⏳ Later | Later |
| **Frequency Selective Fading Model** | Advanced | ⏳ Later | Later |
| **Selective Fading Model** | Advanced | ⏳ Later | Later |

Chapter 19 is expected to move from manually added noise to a more complete controlled channel model including frequency offset, timing/sample-rate offset, and multipath taps.

---

# 18. File and Data Storage

| Block | Importance | Status | First use / note |
|---|---|---|---|
| **File Source** | Essential | ⏳ Later | Reads raw stored samples |
| **File Sink** | Essential | ✅ Used | Chapter 18 eye-diagram sample capture |
| **WAV File Source** | Important | ⏳ Later | Audio files |
| **WAV File Sink** | Important | ⏳ Later | Audio files |
| **Metadata File Source** | Advanced | ⏳ Later | Later |
| **Metadata File Sink** | Advanced | ⏳ Later | Later |

## 18.1 File Sink

Chapter 18 used File Sink to record the matched-filter output as raw Float32 samples.

```text
GNU Radio matched-filter output
             |
             v
          File Sink
             |
             v
        .dat samples
             |
             v
     Python eye plot
```

The File Sink does not change the signal. It stores the stream for later analysis.

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

The conceptual chapters should remain hardware-independent unless the experiment specifically requires hardware.

---

# 21. Custom and Advanced Processing

| Block / Feature | Importance | Status |
|---|---|---|
| **Embedded Python Block** | Important | ⏳ Later |
| **Hierarchical Block** | Important | ⏳ Later |
| **Stream Tags** | Essential | ⏳ Later |
| **Tagged Streams** | Essential | ⏳ Later |
| **PDUs** | Important | ⏳ Later |

Purpose-written external Python scripts used for visualization are not the same as an Embedded Python Block inside a GNU Radio flowgraph.

---

# 22. Similar-Looking Operations Are Not the Same

Several operations used in the digital chapters can look superficially similar.

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
Hold/duplicate the same value for several samples
```

```text
Interpolating FIR Filter
    |
    v
Increase sample rate while constructing a filtered pulse shape
```

```text
Float to Complex
    |
    v
Combine I and Q into one complex stream
```

The correct habit is always:

> **What operation does the signal need?**

Then:

> **Which GNU Radio block performs that operation?**

---

# 23. Important Conceptual Roles Through Chapter 18

| Need | GNU Radio tool / method |
|---|---|
| Generate a known sinusoid | Signal Source |
| Generate a known finite sequence | Vector Source |
| Generate random digital data | Random Source |
| Add controlled noise | Noise Source + Add |
| Group bits into symbol indices | Repack Bits |
| Map indices to amplitudes/I/Q values | Chunks to Symbols |
| Give symbols rectangular duration | Repeat |
| Combine I and Q | Float to Complex |
| Inspect constellation geometry | QT GUI Constellation Sink |
| Build an FIR response | Decimating FIR Filter / filter blocks |
| Increase sample rate with pulse shaping | Interpolating FIR Filter |
| Create RRC taps | `firdes.root_raised_cosine` |
| Apply receive RRC/matched filtering | Decimating FIR Filter with decimation 1 |
| Record samples for external analysis | File Sink |
| Inspect time waveform | QT GUI Time Sink |
| Inspect spectrum | QT GUI Frequency Sink |

---

# 24. Blocks and Features Used So Far

At the end of Chapter 18, the working GNU Radio toolbox includes:

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
| FFT | ✅ |
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

# 25. Chapter-by-Chapter GNU Radio Growth Through Chapter 18

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
| 16 | Chunks to Symbols, 2-PAM/4-PAM mapping, hard decisions and noisy PAM |
| 17 | Manual BPSK/QPSK/16-QAM construction, Float to Complex, constellation geometry, scaling and rotation |
| 18 | Rectangular-symbol spectrum, pulse smoothing, RRC taps, Interpolating FIR Filter, RX matched RRC, File Sink and eye-diagram sample capture |

This table should follow the **completed manuscript**, not an old chapter plan.

---

# 26. What Comes Next?

Chapter 18 ends with a pulse-shaped digital signal and a receiver matched filter under a deliberately simple channel.

The next question is:

> **Why does the receiver never see exactly what the transmitter sent?**

Chapter 19 moves into the wireless channel.

The expected major GNU Radio addition is:

- **Channel Model**

The chapter can progressively introduce:

```text
Clean signal
     |
     v
Noise
     |
     v
Attenuation / scaling
     |
     v
Frequency offset
     |
     v
Timing/sample-rate offset
     |
     v
Multipath taps
```

Blocks should be marked **Used** only after the Chapter 19 experiments are actually completed.

The teaching rule remains:

> **Introduce the operation because the communication problem requires it, not because a GNU Radio block happens to exist.**
