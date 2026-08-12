# GNU Radio Block Master List

This document keeps track of the important GNU Radio blocks that we encounter while learning digital signal processing and software-defined radio.

It is **not intended to list every block available in GNU Radio**. GNU Radio contains hundreds of blocks, including many that are designed for specialized applications.

Instead, this list focuses on the blocks that are useful for building a strong understanding of:

- digital signal processing;
- software-defined radio;
- signal analysis;
- filtering;
- modulation and demodulation;
- digital communications;
- receiver design;
- and practical GNU Radio development.

The list will grow as we progress through the chapters and experiments.

---

## How to Read This List

### Importance

We classify blocks into four groups.

- **Essential** — a fundamental block that we should understand and use.
- **Important** — a useful block that should be introduced when the corresponding concept appears.
- **Advanced** — valuable for later SDR and digital communication topics.
- **Specialized** — mainly useful for a particular application.

### Status

- ✅ **Used** — already used in one of our experiments.
- 🔜 **Planned** — expected to be used soon.
- ⏳ **Later** — useful, but we have not reached the corresponding topic yet.
- ➖ **Optional** — not necessary for the main learning path.

The status will be updated as we progress through the project.

---

# 1. Waveform Generators

Waveform generators provide signals that can be used as inputs to a GNU Radio flowgraph.

They are especially useful while learning because they allow us to create controlled test signals without requiring SDR hardware.

| Block | Importance | Status | What it does | Where we use it |
|---|---|---|---|---|
| **Signal Source** | Essential | ✅ Used | Generates periodic signals such as sine, cosine, square, and triangle waves | Signal fundamentals, sampling, frequency analysis, I/Q experiments |
| **Noise Source** | Essential | 🔜 Planned | Generates random noise with selectable noise distributions | Noise, noise floor, SNR |
| **Fast Noise Source** | Important | ⏳ Later | Generates noise using a computationally efficient implementation | Larger or more demanding noise simulations |
| **Random Source** | Important | ⏳ Later | Generates sequences of random values | Digital data and communication experiments |
| **Random Uniform Source** | Important | ⏳ Later | Generates uniformly distributed random values | Random-signal experiments |
| **Constant Source** | Important | ⏳ Later | Produces a stream containing a constant value | DC signals, offsets, testing |
| **GLFSR Source** | Important | ⏳ Later | Generates pseudo-random sequences using a linear-feedback shift register | PN sequences and digital communications |
| **VCO** | Important | ⏳ Later | Generates a waveform whose instantaneous frequency is controlled by an input signal | Frequency modulation and oscillator experiments |
| **VCO (Complex)** | Important | ⏳ Later | Complex-output version of the voltage-controlled oscillator | Complex baseband and modulation experiments |

---

## 1.1 Signal Source

The **Signal Source** is one of the most useful blocks when learning GNU Radio.

We have already used it extensively to generate controlled signals for experiments involving:

- sine and cosine waves;
- sampling;
- aliasing;
- time-domain analysis;
- frequency-domain analysis;
- I/Q signals;
- FFT experiments;
- spectral leakage;
- and frequency evolution.

Because we know exactly what signal we generated, it becomes much easier to understand what the rest of the flowgraph is doing.

---

## 1.2 Noise Source

The **Noise Source** will become one of the main blocks in our noise experiments.

Instead of trying to construct noise manually, GNU Radio provides a dedicated noise generator.

This will allow us to investigate questions such as:

- What does noise look like in the time domain?
- What does noise look like in the frequency domain?
- What is a noise floor?
- What happens when noise is added to a sinusoid?
- How does SNR affect our ability to detect a signal?
- Can a signal still be detected when it is difficult to see in the time domain?

The Noise Source will therefore be introduced directly in the chapter on noise and SNR.

---

# 2. Fourier Analysis

The Fourier Analysis category contains blocks that perform explicit frequency-domain processing.

This category is particularly important because there is a difference between:

> **calculating an FFT**

and

> **displaying a spectrum**

We have already used the QT GUI Frequency Sink extensively. The Frequency Sink internally performs the processing required to display a spectrum.

The dedicated FFT block, however, exposes the FFT output so that we can process it ourselves.

| Block | Importance | Status | What it does | Where we use it |
|---|---|---|---|---|
| **FFT** | Essential | 🔜 Planned | Computes the Fast Fourier Transform or inverse FFT of a vector | Explicit FFT processing and frequency-domain analysis |
| **Goertzel** | Important | ⏳ Later | Efficiently evaluates a selected frequency component | Tone detection |
| **Log Power FFT** | Important | ⏳ Later | Computes an FFT and produces logarithmic power-spectrum information | Spectrum and power analysis |

---

## 2.1 FFT

The **FFT block** explicitly performs the Fast Fourier Transform.

This is different from the QT GUI Frequency Sink.

The Frequency Sink is mainly a visualization tool. It calculates the spectral information required to draw the spectrum internally.

The FFT block gives us access to the FFT output itself.

A typical explicit FFT processing chain may look like:

```text
Signal
  |
  v
Stream to Vector
  |
  v
FFT
  |
  v
Complex to Mag / Complex to Mag^2
  |
  v
Further processing
```

This distinction is important.

Using the Frequency Sink answers:

> What does the spectrum look like?

Using the FFT block allows us to ask:

> What are the actual FFT outputs, and what can we do with them?

Because we have already studied DFT and FFT theory, the FFT block should be introduced explicitly rather than leaving all FFT processing hidden inside the Frequency Sink.

---

## 2.2 Goertzel

The **Goertzel** block is useful when we are interested in a particular frequency rather than the entire spectrum.

For example, suppose we only want to know whether a particular tone is present.

Calculating a complete FFT may not always be necessary.

The Goertzel algorithm can efficiently examine a selected frequency component.

This makes it useful for applications such as:

- tone detection;
- DTMF detection;
- known-frequency monitoring;
- and narrowband signal detection.

We will introduce it later when we study tone detection.

---

## 2.3 Log Power FFT

The **Log Power FFT** block combines FFT processing with logarithmic power calculation.

It is useful when we want spectral power information directly rather than manually constructing the complete processing chain.

We will introduce this block when power-spectrum analysis becomes important.

For now, it is useful simply to know that the block exists.

---

# 3. Filters

Filtering is one of the most important operations in DSP and SDR.

A receiver rarely wants every frequency that enters the antenna.

We may want to:

- select one channel;
- remove unwanted interference;
- suppress high-frequency noise;
- remove DC;
- reduce bandwidth;
- or prepare a signal for demodulation.

GNU Radio provides both convenient ready-to-use filters and lower-level blocks for building more specialized filtering systems.

| Block | Importance | Status | What it does | Where we use it |
|---|---|---|---|---|
| **Low Pass Filter** | Essential | ⏳ Later | Passes lower frequencies while attenuating higher frequencies | Filtering fundamentals, channel selection |
| **High Pass Filter** | Essential | ⏳ Later | Passes higher frequencies while attenuating lower frequencies | Filtering fundamentals |
| **Band Pass Filter** | Essential | ⏳ Later | Passes frequencies inside a selected frequency band | Channel and signal selection |
| **Band Reject Filter** | Essential | ⏳ Later | Rejects frequencies inside a selected band | Interference removal |
| **DC Blocker** | Important | ⏳ Later | Removes or suppresses a DC component | SDR receiver processing |
| **FFT Filter** | Important | ⏳ Later | Performs FIR filtering using FFT-based convolution | Efficient implementation of long filters |
| **FFT Low Pass Filter** | Important | ⏳ Later | Implements low-pass filtering using FFT-based processing | Efficient filtering |
| **Decimating FIR Filter** | Important | ⏳ Later | FIR filters a signal while reducing its sample rate | Receiver processing and decimation |
| **Interpolating FIR Filter** | Important | ⏳ Later | FIR filters a signal while increasing its sample rate | Interpolation and transmitter processing |
| **IIR Filter** | Important | ⏳ Later | Implements an infinite impulse response filter | IIR filtering |
| **Single Pole IIR Filter** | Important | ⏳ Later | Implements a simple first-order IIR filter | Smoothing and averaging |
| **Hilbert** | Important | ⏳ Later | Implements a Hilbert transform | Analytic signals, I/Q processing, SSB |
| **Generic Filterbank** | Advanced | ⏳ Later | Applies a bank of filters to a signal | Multichannel processing |

---

## 3.1 Low Pass Filter

A **Low Pass Filter** allows lower frequencies to pass while attenuating frequencies above a chosen cutoff region.

This is one of the most fundamental filters in DSP.

In SDR, a low-pass filter can be used after frequency translation to isolate a desired baseband signal.

We will study it properly when we reach filtering rather than treating it as just another GNU Radio block.

---

## 3.2 High Pass Filter

A **High Pass Filter** does the opposite.

It attenuates lower frequencies while allowing higher frequencies to pass.

This can be useful when unwanted low-frequency components need to be removed.

---

## 3.3 Band Pass Filter

A **Band Pass Filter** allows only a selected range of frequencies to pass.

This is particularly important in SDR.

Imagine receiving many signals simultaneously.

A band-pass filter can help isolate the frequency region containing the signal that we actually want.

---

## 3.4 Band Reject Filter

A **Band Reject Filter** suppresses a selected frequency range while allowing frequencies outside that region to pass.

This can be useful when a particular interferer occupies a known frequency band.

It is sometimes also called a band-stop filter.

A very narrow band-reject filter is commonly referred to as a **notch filter**.

---

## 3.5 DC Blocker

Real SDR receivers often contain an unwanted component at or near the center of the spectrum.

This is commonly called a **DC offset** or **DC spike**.

The **DC Blocker** is designed to suppress this unwanted DC component.

This block will become much more meaningful when we begin using actual SDR hardware and examining real received spectra.

---

## 3.6 FFT Filter

The **FFT Filter** performs FIR filtering using FFT-based convolution.

This connects directly with two ideas that we study separately:

- convolution;
- Fourier transforms.

For short filters, direct convolution can be efficient.

For sufficiently long filters, performing the filtering using FFT-based methods can be computationally advantageous.

We will return to this block after we understand ordinary FIR filtering.

---

## 3.7 Hilbert

The **Hilbert** block implements a Hilbert transform.

This is an especially interesting block for SDR because the Hilbert transform is closely related to:

- analytic signals;
- quadrature signals;
- I/Q representation;
- single-sideband modulation;
- and complex signal generation.

We have already studied the idea of I/Q signals, but we will introduce the Hilbert block when we have a clear experiment that demonstrates why it is useful.

---

# 4. Filter-Tap Design Blocks

GNU Radio also provides blocks for generating **filter taps**.

Filter taps are the coefficients used by an FIR filter.

These blocks are different from the ready-to-use filter blocks.

| Block | Importance | Status | What it does |
|---|---|---|---|
| **Low-pass Filter Taps** | Important | ⏳ Later | Generates low-pass FIR coefficients |
| **High-pass Filter Taps** | Important | ⏳ Later | Generates high-pass FIR coefficients |
| **Band-pass Filter Taps** | Important | ⏳ Later | Generates band-pass FIR coefficients |
| **Band-reject Filter Taps** | Important | ⏳ Later | Generates band-reject FIR coefficients |
| **RRC Filter Taps** | Important | ⏳ Later | Generates root-raised-cosine filter coefficients |
| **Filter Taps Loader** | Advanced | ⏳ Later | Loads externally defined filter taps |

Initially, blocks such as the Low Pass Filter allow us to study filtering without manually designing the coefficients.

Later, when we study FIR filters in more depth, the relationship between:

> filter specification → filter taps → convolution → output signal

will become important.

At that point, these blocks will become much more meaningful.

---

# 5. Root-Raised-Cosine Filtering

Two particularly important filtering-related blocks are:

- **Root Raised Cosine Filter**
- **RRC Filter Taps**

Root-raised-cosine filtering is widely used in digital communication systems for pulse shaping.

It becomes important when we start transmitting symbols rather than simple sinusoidal signals.

Among other things, it helps control occupied bandwidth and intersymbol interference.

These blocks are therefore important, but introducing them before modulation and symbol transmission would be premature.

We will return to them in the digital communications part of the project.

---

# 6. Similar-Looking Blocks Are Not Necessarily the Same

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

This is an important principle for the rest of this master list:

> We do not need to learn every similar-looking block at the same time.

We will first learn the underlying DSP concept using the clearest block.

Once the concept is understood, alternative implementations become much easier to understand.

---

# 7. Blocks Flagged for Upcoming Work

From the categories covered so far, several blocks deserve our attention relatively soon.

| Block | Why we need it |
|---|---|
| **FFT** | We studied FFT theory and used the Frequency Sink, but have not yet explicitly used GNU Radio's FFT block |
| **Noise Source** | Central block for the upcoming noise, noise-floor, and SNR experiments |
| **Low Pass Filter** | One of the most fundamental DSP operations |
| **High Pass Filter** | Important for understanding frequency-selective filtering |
| **Band Pass Filter** | Extremely important for SDR channel and signal selection |
| **Band Reject Filter** | Useful for understanding interference rejection |
| **DC Blocker** | Common practical SDR receiver block |
| **Hilbert** | Important when we return to analytic signals and I/Q processing |

The immediate priorities are therefore:

1. **FFT**
2. **Noise Source**

The FFT block closes an important gap in our frequency-domain work.

The Noise Source then becomes one of the main tools for the next chapter.

---

# 8. Categories Still to Add

This master list will be expanded gradually.

The remaining important GNU Radio categories include:

1. Math Operators
2. Type Converters
3. Stream Operators
4. Instrumentation and QT GUI
5. GUI Widgets
6. Channel Models
7. Level Controllers
8. Measurement Tools
9. Resamplers
10. Peak Detectors
11. Synchronizers
12. Modulators
13. Symbol Coding
14. Equalizers
15. Channelizers
16. Coding and FEC
17. OFDM
18. Packet Operators
19. PDU Tools
20. File Operators
21. Message Tools
22. Networking Tools
23. Variables and Flowgraph Utilities
24. Hardware and SDR Interfaces
25. Impairment and I/Q Correction
26. Specialized and application-specific blocks

We will add these categories one at a time rather than filling the document with blocks that we have not yet classified.

---

## Final Note

This is a **living document**.

As we progress through the GNU Radio experiments:

- new blocks will be added;
- statuses will change from **Planned** or **Later** to **Used**;
- chapter references will be added;
- some blocks may be reclassified;
- and practical notes from our experiments can be included.

The purpose is not to memorize GNU Radio's block library.

The purpose is to know:

> **Which block should I reach for when I want to perform a particular DSP or SDR operation, and why?**