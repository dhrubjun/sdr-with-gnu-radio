# SDR with GNU Radio: Chapter Plan

## Purpose of This Book

This book introduces Software Defined Radio from the ground up using simple explanations, visual intuition, essential mathematics, and hands-on GNU Radio experiments.

The aim is not just to teach the reader how to connect GNU Radio blocks.

The reader should understand **why the blocks are there, what happens to the signal inside them, and what goes wrong when they are configured incorrectly**.

Each chapter therefore develops two things in parallel:

1. **SDR and signal-processing understanding**
2. **Practical GNU Radio skills**

The book begins with simple software-generated signals. Real SDR hardware is introduced only after the reader understands the fundamental ideas behind the processing chain.

---

# Part I: Learning to Think in Signals

---

# Chapter 1: What Is Software Defined Radio?

## Main Question

What makes a radio "software defined"?

## Concepts

* What a radio actually does
* Traditional hardware radio
* Software Defined Radio
* Analog and digital processing
* Basic transmitter chain
* Basic receiver chain
* RF front end
* ADC and DAC
* Baseband processing
* Why SDR is useful
* What GNU Radio is
* Where GNU Radio fits into an SDR system

## Intuition We Want the Reader to Leave With

A radio is fundamentally a chain of operations performed on signals.

In a traditional radio, many of these operations are performed by dedicated hardware.

In an SDR, many of them can be performed digitally in software.

GNU Radio gives us a way to build and experiment with those processing chains.

## Mathematics

Very little mathematics is required.

Introduce only the idea of representing a sinusoidal signal as:

$$
x(t)=A\cos(2\pi ft+\phi)
$$

The equation is introduced as a description of a signal rather than something to derive.

## GNU Radio Experiment

Build the reader's first flowgraph:

Signal Source → Throttle → QT GUI Time Sink

Generate a simple sinusoidal signal and observe it.

## Expected Observation

The reader sees a waveform that previously existed only as an equation become visible inside GNU Radio.

## GNU Radio Direction

Introduce:

* GNU Radio Companion
* Flowgraphs
* Blocks
* Connections
* Source blocks
* Sink blocks
* Run and Stop
* Block properties
* Basic data flow

## Break-the-Flowgraph Idea

Disconnect a block, change incompatible settings, or remove an essential connection and observe how GNU Radio reports problems.

## Leads Into

Understanding signals themselves.

---

# Chapter 2: Understanding Signals

## Main Question

What exactly is a signal?

## Concepts

* Signals as information
* Time-domain representation
* Amplitude
* Frequency
* Period
* Phase
* DC offset
* Sinusoids
* Multiple signals
* Adding signals
* Waveform shape
* Basic distinction between continuous-time and discrete-time signals

## Intuition We Want the Reader to Leave With

A signal is simply a quantity that changes and carries information.

Amplitude tells us "how much," frequency tells us "how fast," and phase tells us "where in the cycle."

## Mathematics

Introduce:

$$
T=\frac{1}{f}
$$

and

$$
x(t)=A\cos(2\pi ft+\phi)
$$

Use plots to show what happens when (A), (f), and (\phi) are changed independently.

## GNU Radio Experiment

Create an interactive signal generator.

Use GUI controls to change:

* amplitude
* frequency
* phase

Observe the results in real time.

Then add two sinusoidal signals together.

## Expected Observation

The reader directly sees how amplitude, frequency, and phase affect a waveform.

## GNU Radio Direction

Introduce or expand:

* Signal Source
* Throttle
* QT GUI Time Sink
* Variables
* Add block
* Basic QT GUI controls

## Break-the-Flowgraph Idea

Set unusual amplitudes, frequencies, phases, and offsets and predict what the Time Sink should display.

## Leads Into

Sampling.

---

# Chapter 3: Sampling: How a Computer Sees a Signal

## Main Question

How can a computer represent a continuous waveform using only numbers?

## Concepts

* Continuous signals
* Discrete samples
* Sampling
* Sampling frequency
* Sampling period
* Samples per cycle
* Nyquist criterion
* Nyquist frequency
* Undersampling
* Aliasing
* Apparent frequency
* Why sample rate matters in SDR

## Intuition We Want the Reader to Leave With

GNU Radio does not see a smooth continuous waveform.

It processes a sequence of samples.

If those samples are taken incorrectly, two different analog signals can become indistinguishable after sampling.

## Mathematics

Introduce:

$$
T_s=\frac{1}{f_s}
$$

Samples per cycle:

$$
N=\frac{f_s}{f}
$$

Nyquist criterion:

$$
f_s>2f_{\max}
$$

Introduce aliasing mathematically only after it has been demonstrated visually.

## GNU Radio Experiment

Generate a fixed-frequency sinusoid.

Gradually change the sample rate while observing the waveform.

Example sequence:

48 kHz → 10 kHz → 4 kHz → 2.5 kHz → 2 kHz → 1.5 kHz → 1 kHz → 500 Hz

## Expected Observation

The waveform gradually becomes poorly represented and eventually appears as another frequency or an apparently stationary pattern.

## GNU Radio Direction

Introduce:

* QT GUI Range
* Runtime parameter adjustment
* Sample-rate variables
* Relationship between block parameters
* Time Sink sample rate
* Frequency Sink introduction
* Why software-only flowgraphs use Throttle

## Break-the-Flowgraph Idea

Deliberately violate Nyquist.

Remove Throttle.

Use inconsistent sample-rate variables.

Observe what changes and what does not.

## Leads Into

Discrete-time signals and complex signal representation.

---

# Chapter 4: Complex Numbers for SDR

## Main Question

Why does radio engineering use imaginary numbers to describe real signals?

## Concepts

* Real numbers
* Imaginary numbers
* Complex numbers
* Real and imaginary components
* Complex plane
* Magnitude
* Phase
* Euler's formula
* Rotating vectors
* Complex exponential

## Intuition We Want the Reader to Leave With

Complex numbers give us a convenient way to describe both amplitude and phase at the same time.

They are not imaginary in the everyday sense. They are a mathematical representation that makes radio signals much easier to process.

## Mathematics

Introduce:

$$
z=I+jQ
$$

$$
|z|=\sqrt{I^2+Q^2}
$$

$$
\theta=\tan^{-1}\left(\frac{Q}{I}\right)
$$

and eventually:

$$
e^{j\theta}=\cos\theta+j\sin\theta
$$

## GNU Radio Experiment

Generate real and complex signals.

Separate a complex signal into its real and imaginary components and display both.

## Expected Observation

The reader sees that a complex signal contains two related streams of information.

## GNU Radio Direction

Introduce:

* GNU Radio data types
* Float streams
* Complex streams
* Float to Complex
* Complex to Real
* Complex to Imag
* Data-type colours and port compatibility

## Break-the-Flowgraph Idea

Attempt incompatible data-type connections.

Remove one component of the complex signal.

Swap real and imaginary inputs.

## Leads Into

I/Q representation.

---

# Chapter 5: I and Q Signals

## Main Question

Why do SDR receivers represent signals using I and Q?

## Concepts

* In-phase component
* Quadrature component
* 90-degree relationship
* Complex baseband
* Rotating-vector interpretation
* Magnitude
* Phase
* Positive rotation
* Negative rotation
* Why SDR hardware produces IQ samples

## Intuition We Want the Reader to Leave With

I and Q allow the receiver to preserve information about both the magnitude and phase of a signal.

Together they allow us to distinguish rotations that a single real waveform cannot distinguish.

## Mathematics

Develop:

$$
x[n]=I[n]+jQ[n]
$$

and connect this representation to the complex exponential.

## GNU Radio Experiment

Construct I and Q signals separately.

Combine them into a complex stream.

Display:

* I versus time
* Q versus time
* complex spectrum
* constellation

## Expected Observation

I and Q appear as sinusoidal components separated by 90 degrees.

Together they form a rotating complex vector.

## GNU Radio Direction

Introduce:

* Complex Signal Source
* Float to Complex
* Complex to Mag
* Complex to Arg
* QT GUI Constellation Sink
* Multiple GUI sinks

## Break-the-Flowgraph Idea

Make I and Q identical.

Change the phase relationship from 90 degrees.

Reverse Q.

Set Q to zero.

Observe what happens to the constellation and spectrum.

## Leads Into

Frequency-domain analysis.

---

# Part II: Seeing What Is Inside a Signal

---

# Chapter 6: From Time Domain to Frequency Domain

## Main Question

How can we discover which frequencies are hidden inside a waveform?

## Concepts

* Time domain
* Frequency domain
* Sinusoidal decomposition
* Fourier transform intuition
* Discrete Fourier Transform
* FFT
* FFT bins
* Frequency resolution
* Magnitude spectrum
* Windowing
* Spectral leakage

## Intuition We Want the Reader to Leave With

A complicated waveform can often be understood as a combination of simpler sinusoidal components.

The FFT gives us another way to look at exactly the same signal.

## Mathematics

Introduce the Fourier/DFT idea gradually.

Focus first on interpretation rather than derivation.

## GNU Radio Experiment

Generate several tones.

Add them together.

Observe the combined waveform in the Time Sink and individual components in the Frequency Sink.

Change FFT size and window settings.

## GNU Radio Direction

Introduce:

* QT GUI Frequency Sink in depth
* FFT size
* FFT averaging
* Window functions
* Frequency axis
* dB scale
* Update rate

## Break-the-Flowgraph Idea

Use a poor FFT size.

Choose frequencies that do not align with FFT bins.

Disable or change windowing.

Observe spectral leakage.

## Leads Into

Positive and negative frequency.

---

# Chapter 7: Positive and Negative Frequencies

## Main Question

What does a negative frequency actually mean?

## Concepts

* Positive frequency
* Negative frequency
* Direction of complex rotation
* Real cosine spectrum
* Spectral symmetry
* Complex exponential
* One-sided complex tones
* Relationship to IQ
* Frequency relative to a local oscillator

## Intuition We Want the Reader to Leave With

Negative frequency does not mean that a physical electromagnetic wave is travelling backward.

It describes the opposite direction of rotation in the complex plane and becomes extremely useful when representing frequencies relative to a reference.

## Mathematics

Compare:

$$
\cos(2\pi ft)
=============

\frac{1}{2}e^{j2\pi ft}
+
\frac{1}{2}e^{-j2\pi ft}
$$

with:

$$
e^{j2\pi ft}
$$

## GNU Radio Experiment

Compare the FFT of:

* a real cosine
* a positive complex tone
* a negative complex tone

## Expected Observation

The real cosine produces symmetric components at (+f) and (-f).

A complex tone can produce only one spectral component.

## GNU Radio Direction

Reinforce:

* Float versus Complex signals
* Frequency Sink interpretation
* Complex Signal Source
* Spectrum centre

## Break-the-Flowgraph Idea

Convert the complex signal to real and observe the missing spectral component reappear as a mirror.

## Leads Into

Noise and real-world signals.

---

# Chapter 8: Noise and Signal-to-Noise Ratio

## Main Question

Why do real signals never look perfectly clean?

## Concepts

* Noise
* Random signals
* White noise
* Gaussian noise
* Noise floor
* Signal power
* Noise power
* SNR
* SNR in dB
* Detectability
* Dynamic range

## Intuition We Want the Reader to Leave With

Noise is not simply an ugly waveform added to a signal. It determines how reliably information can be detected and recovered.

## Mathematics

Introduce:

$$
\mathrm{SNR}=\frac{P_s}{P_n}
$$

and

$$
\mathrm{SNR}*{dB}=10\log*{10}\left(\frac{P_s}{P_n}\right)
$$

## GNU Radio Experiment

Generate a tone and add adjustable Gaussian noise.

Gradually increase the noise level.

Observe the signal in:

* Time Sink
* Frequency Sink

## GNU Radio Direction

Introduce:

* Noise Source
* Add
* Multiply Const
* QT GUI Range for noise control
* Number Sink where useful

## Break-the-Flowgraph Idea

Gradually bury the signal below the visible noise floor and investigate whether it can still be identified in the spectrum.

## Leads Into

Mixing and frequency translation.

---

# Part III: Moving and Shaping Signals

---

# Chapter 9: Mixing and Frequency Translation

## Main Question

How does a radio move a signal from one frequency to another?

## Concepts

* Mixer
* Local oscillator
* Frequency translation
* Upconversion
* Downconversion
* Sum and difference frequencies
* Complex mixing
* Baseband
* Frequency offset

## Intuition We Want the Reader to Leave With

Mixing does not destroy the information in a signal. It moves that information to another part of the spectrum.

## Mathematics

Introduce multiplication identities and complex multiplication.

## GNU Radio Experiment

Multiply a signal by a local oscillator.

Watch the spectrum move as the LO frequency changes.

Then demonstrate complex downconversion.

## GNU Radio Direction

Introduce:

* Multiply
* Multiply Conjugate where appropriate
* Complex oscillators
* Frequency translation
* Runtime LO control

## Break-the-Flowgraph Idea

Mistune the LO deliberately.

Place the signal above and below the LO.

Observe positive and negative baseband frequencies.

## Leads Into

Filtering.

---

# Chapter 10: Filters and Channel Selection

## Main Question

How can a receiver keep the signal it wants and reject everything else?

## Concepts

* Filtering
* Low-pass filter
* High-pass filter
* Band-pass filter
* Band-stop filter
* Cutoff frequency
* Transition bandwidth
* Passband
* Stopband
* Filter order
* FIR filters
* Basic IIR idea
* Channel selection

## Intuition We Want the Reader to Leave With

A filter does not simply "remove noise." It selectively changes different frequency components.

## Mathematics

Introduce frequency response and filter taps at an intuitive level.

## GNU Radio Experiment

Generate several signals at different frequencies.

Add them together.

Use filters to select or reject individual components.

## GNU Radio Direction

Introduce:

* Low Pass Filter
* High Pass Filter
* Band Pass Filter
* Band Reject Filter
* FIR taps
* Filter design parameters
* QT GUI Frequency Sink before and after filtering

## Break-the-Flowgraph Idea

Use the wrong cutoff frequency.

Use an extremely narrow transition band.

Change decimation unexpectedly.

Observe both signal quality and computational effects.

## Leads Into

Convolution and impulse response.

---

# Chapter 11: Convolution and Impulse Response

## Main Question

If we know how a system reacts to one impulse, can we predict how it reacts to any signal?

## Concepts

* Systems
* Impulse
* Impulse response
* Convolution
* FIR filtering
* Input/output relationship
* Why convolution appears everywhere in DSP

## Intuition We Want the Reader to Leave With

A signal can be thought of as a collection of shifted impulses.

If we know how a system responds to an impulse, convolution allows us to predict its response to a complete signal.

## Mathematics

Introduce:

$$
y[n]=x[n]*h[n]
$$

and expand it only after establishing the visual interpretation.

## GNU Radio Experiment

Send a simple impulse or short sequence through an FIR filter and observe its response.

Then use a longer signal.

## GNU Radio Direction

Introduce:

* FIR Filter in greater depth
* Filter taps
* Vector Source
* Repeat behaviour
* Head block where useful
* File Sink where useful

## Break-the-Flowgraph Idea

Change taps.

Reverse taps.

Use unexpected tap values.

Observe how the system response changes.

## Leads Into

Correlation and detection.

---

# Chapter 12: Correlation and Finding Signals

## Main Question

How can a receiver find a known signal hidden inside another signal?

## Concepts

* Similarity
* Cross-correlation
* Autocorrelation
* Time delay
* Signal detection
* Matched filtering
* Synchronization intuition

## Intuition We Want the Reader to Leave With

Correlation answers a simple question:

"How much does this part of the received signal look like the signal I am searching for?"

## Mathematics

Introduce discrete correlation and its relationship to convolution.

## GNU Radio Experiment

Create a known sequence.

Delay it and add noise.

Use correlation to locate the sequence.

## GNU Radio Direction

Introduce progressively:

* Delay
* Conjugate
* Multiply
* Moving Average
* Vector concepts
* Stream-to-Vector where appropriate

## Break-the-Flowgraph Idea

Use the wrong reference sequence.

Change the delay.

Increase noise.

Observe when detection becomes unreliable.

## Leads Into

Communication and modulation.

---

# Part IV: Putting Information on Radio Waves

---

# Chapter 13: Why Modulation Exists

## Main Question

Why can't we simply transmit the original information signal directly?

## Concepts

* Baseband
* Passband
* Carrier
* Modulation
* Spectrum allocation
* Antenna considerations
* Frequency division
* Bandwidth

## Intuition We Want the Reader to Leave With

Modulation allows information to be moved to a frequency range where it can be transmitted, separated from other users, and efficiently received.

## GNU Radio Experiment

Move a low-frequency message signal onto a higher-frequency carrier.

Observe both signals in the frequency domain.

## GNU Radio Direction

Reuse mixing blocks while introducing modulation-oriented flowgraph organization.

## Leads Into

Analog modulation.

---

# Chapter 14: Amplitude Modulation

## Main Question

How can information be carried by changing the amplitude of a carrier?

## Concepts

* Carrier
* Message
* AM
* Modulation index
* Sidebands
* Carrier power
* Envelope
* AM demodulation

## GNU Radio Experiment

Build an AM transmitter and receiver.

Message → Modulator → Channel → Demodulator

Compare the original and recovered signals.

## GNU Radio Direction

Introduce:

* AM-related processing blocks
* Audio Sink where appropriate
* Hierarchical organization concepts

## Break-the-Flowgraph Idea

Overmodulate the carrier.

Use incorrect demodulation parameters.

Add noise.

## Leads Into

Frequency modulation.

---

# Chapter 15: Frequency Modulation

## Main Question

What happens if information changes the instantaneous frequency instead of amplitude?

## Concepts

* FM
* Instantaneous frequency
* Frequency deviation
* Modulation index
* FM bandwidth
* FM demodulation
* Narrowband versus wideband FM

## GNU Radio Experiment

Build an FM transmitter and receiver entirely in software.

## GNU Radio Direction

Introduce:

* NBFM/WBFM concepts and blocks
* Audio rates
* Decimation
* Interpolation
* Resampling

## Break-the-Flowgraph Idea

Use incorrect quadrature rate, audio rate, or resampling values.

Observe distortion.

## Leads Into

Digital modulation.

---

# Part V: Digital Radio

---

# Chapter 16: From Bits to Symbols

## Main Question

How can zeros and ones become a radio waveform?

## Concepts

* Bits
* Symbols
* Symbol rate
* Bit rate
* BPSK
* QPSK
* QAM
* Symbol mapping
* Constellations

## GNU Radio Experiment

Generate random bits and map them to BPSK and QPSK symbols.

## GNU Radio Direction

Introduce:

* Random Source
* Symbol mapping
* Constellation objects
* Digital modulation blocks

## Break-the-Flowgraph Idea

Change symbol mappings and constellation parameters.

## Leads Into

Constellation analysis.

---

# Chapter 17: Reading Constellation Diagrams

## Main Question

What can a constellation diagram tell us about a communication system?

## Concepts

* Ideal constellation points
* Decision regions
* Noise
* Phase offset
* Frequency offset
* Amplitude error
* IQ imbalance
* EVM intuition

## GNU Radio Experiment

Create a QPSK signal and deliberately introduce impairments one at a time.

## GNU Radio Direction

Explore:

* QT GUI Constellation Sink in depth
* Channel Model
* Noise voltage
* Frequency offset
* Timing offset

## Break-the-Flowgraph Idea

This entire chapter can act as a controlled "break the signal" laboratory.

## Leads Into

Pulse shaping.

---

# Chapter 18: Pulse Shaping and Symbol Timing

## Main Question

Why can't we simply transmit perfect rectangular digital pulses?

## Concepts

* Bandwidth
* Symbols
* Intersymbol interference
* Pulse shaping
* Raised cosine
* Root-raised cosine
* Samples per symbol
* Eye diagram intuition
* Symbol timing

## GNU Radio Experiment

Compare unfiltered symbols with pulse-shaped symbols.

## GNU Radio Direction

Introduce:

* RRC taps
* Interpolation
* Decimation
* Samples per symbol
* Timing-related processing

## Break-the-Flowgraph Idea

Use incorrect samples-per-symbol values or mismatched pulse-shaping filters.

## Leads Into

Synchronization.

---

# Chapter 19: Synchronization

## Main Question

How does a receiver know when and where to look at the transmitted symbols?

## Concepts

* Carrier frequency offset
* Carrier phase
* Symbol timing
* Clock recovery
* Carrier recovery
* AGC
* Costas loop
* Frame synchronization introduction

## GNU Radio Experiment

Transmit a digital signal with controlled impairments and progressively recover it.

## GNU Radio Direction

Introduce:

* AGC
* Clock Synchronization
* Costas Loop
* Frequency Lock Loop where appropriate
* Tags and synchronization concepts

## Break-the-Flowgraph Idea

Disable synchronization stages one at a time and observe the constellation.

## Leads Into

Packet and stream processing.

---

# Chapter 20: Streams, Vectors, Tags, Messages and PDUs

## Main Question

How does GNU Radio move more than just a continuous stream of samples?

## Concepts

* Streams
* Items
* Vectors
* Stream tags
* Messages
* Message ports
* PDUs
* Metadata
* Packet-oriented processing

## Intuition We Want the Reader to Leave With

Not every piece of information in a radio system is simply another sample.

GNU Radio provides different mechanisms for continuous sample processing and event- or packet-oriented information.

## GNU Radio Experiment

Create small examples showing:

* stream processing
* stream-to-vector conversion
* tags
* message passing
* simple PDU processing

## GNU Radio Direction

This chapter focuses strongly on GNU Radio architecture itself.

## Break-the-Flowgraph Idea

Lose tag alignment, mismatch vector lengths, or route messages incorrectly and inspect the results.

## Leads Into

Building larger GNU Radio systems.

---

# Part VI: Becoming Independent with GNU Radio

---

# Chapter 21: Building Larger GNU Radio Flowgraphs

## Main Question

How do we stop a large flowgraph from becoming an unreadable collection of blocks?

## Concepts

* Flowgraph organization
* Reusable processing chains
* Hierarchical blocks
* Parameters
* Embedded Python Blocks
* Custom processing
* Debugging
* Logging
* File input/output
* Network input/output
* UDP/TCP concepts
* Reproducible experiments

## GNU Radio Experiment

Take one of the earlier large flowgraphs and reorganize it.

Create a reusable hierarchical block.

Implement a small custom operation with an Embedded Python Block.

## GNU Radio Direction

Introduce:

* Hierarchical Blocks
* Embedded Python Block
* File Source/Sink
* network blocks
* probes/debugging tools
* generated Python awareness

## Break-the-Flowgraph Idea

Introduce parameter mismatches and investigate errors systematically.

## Leads Into

Real SDR hardware.

---

# Part VII: Leaving the Simulation

---

# Chapter 22: SDR Hardware

## Main Question

What changes when our samples come from an antenna instead of a Signal Source?

## Concepts

* Antenna
* RF front end
* LNA
* Mixer
* ADC
* DAC
* Centre frequency
* Sample rate
* RF bandwidth
* Gain
* Dynamic range
* Frequency accuracy
* IQ samples
* Hardware limitations

## Hardware Examples

Introduce common SDR platforms conceptually:

* RTL-SDR
* ADALM-Pluto
* HackRF
* USRP

The book should not depend entirely on one specific device.

## GNU Radio Experiment

Connect supported SDR hardware and display a real RF spectrum.

## GNU Radio Direction

Introduce:

* Hardware Source blocks
* Centre frequency
* Sample rate
* RF gain
* bandwidth
* antenna selection where supported
* device arguments

## Break-the-Flowgraph Idea

Use excessive gain.

Use insufficient gain.

Choose inappropriate sample rates.

Tune away from the desired signal.

Observe clipping, noise floor, and other real-world effects.

## Leads Into

A complete receiver.

---

# Chapter 23: Receiving a Real Radio Signal

## Main Question

Can we now use everything we have learned to receive an actual transmission?

## Concepts

Bring together:

* IQ
* sampling
* spectrum
* tuning
* mixing
* filtering
* resampling
* demodulation
* gain
* audio

## GNU Radio Experiment

Build a complete broadcast FM receiver.

Conceptual chain:

Antenna
↓
SDR Source
↓
Channel Selection
↓
Frequency Translation
↓
Filtering
↓
Resampling
↓
FM Demodulation
↓
Audio Processing
↓
Audio Sink

## Expected Observation

For the first time, the reader follows a real RF signal all the way from antenna samples to recovered information.

## Break-the-Flowgraph Idea

Disable or misconfigure each major stage individually.

Ask:

"What does this failure look and sound like?"

## Leads Into

Independent SDR design.

---

# Chapter 24: Build an SDR Receiver from a Blank Flowgraph

## Main Question

Can you design an SDR system without following a recipe?

## Purpose

This is the capstone chapter.

Instead of providing the complete flowgraph immediately, the reader is given a requirement and must decide what processing stages are needed.

## Challenge

Start with a blank GNU Radio Companion window.

Determine:

1. What source is required?
2. What sample rate should be used?
3. How should the desired channel be selected?
4. Is frequency translation required?
5. What filtering is required?
6. Is resampling necessary?
7. Which demodulator is required?
8. How should the result be displayed or played?

## Final Goal

The reader should be able to look at a radio problem and think:

"I understand what needs to happen to the signal, so I can decide which GNU Radio blocks I need."

That is the final goal of the book.

---

# Appendix A: GNU Radio Quick Reference

A compact reference for commonly used blocks and parameters.

---

# Appendix B: GNU Radio Data Types

Reference for:

* Byte
* Short
* Integer
* Float
* Complex
* Vectors
* Type conversions

---

# Appendix C: Common GNU Radio Errors

Examples:

* incompatible data types
* invalid sample rates
* missing blocks
* flowgraph generation errors
* Python errors
* hardware connection errors
* buffer and performance problems

---

# Appendix D: GNU Radio Block Index

Alphabetical list of GNU Radio blocks introduced in the book with the chapter in which each one first appears.

---

# Appendix E: Experiment Index

List of all GNU Radio experiments and corresponding `.grc` files.

---

# Appendix F: Mathematics for SDR

A compact reference covering the mathematical ideas used throughout the book.

This is a reference appendix rather than a prerequisite mathematics chapter.

---

# Appendix G: Where to Go Next

Topics for further study:

* OFDM
* channel coding
* packet radio
* synchronization in greater depth
* channel estimation
* spectrum sensing
* cognitive radio
* direction finding
* radar
* satellite communications
* wireless security
* GNU Radio OOT modules
* FPGA acceleration
* advanced SDR hardware

---

# Overall Learning Path

The book follows this progression:

Signals
↓
Sampling
↓
Complex Numbers
↓
I/Q
↓
FFT and Spectrum
↓
Positive and Negative Frequencies
↓
Noise and SNR
↓
Mixing
↓
Filtering
↓
Convolution
↓
Correlation
↓
Modulation
↓
Analog Communications
↓
Digital Communications
↓
Constellations
↓
Pulse Shaping
↓
Synchronization
↓
GNU Radio Streams, Tags, Messages and PDUs
↓
Advanced GNU Radio Usage
↓
SDR Hardware
↓
Real RF Reception
↓
Independent SDR Design

---

# Core Principle

Every chapter should answer three questions:

**What is happening to the signal?**

**Why are we doing it?**

**How can I see it for myself in GNU Radio?**

The reader should never be asked to use a GNU Radio block simply because "this is the block we need."

By the end of the book, the reader should understand both the signal-processing reason for each operation and how GNU Radio implements that operation.
