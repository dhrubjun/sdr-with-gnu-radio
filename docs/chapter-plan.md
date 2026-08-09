# SDR with GNU Radio: Chapter Plan

**Version 0.2**

---

# Purpose of This Book

This book introduces Software Defined Radio from the ground up.

The aim is not to teach GNU Radio by asking the reader to copy flowgraphs, and it is not to teach SDR by beginning with pages of equations.

Instead, we will try to understand what is actually happening to a signal.

Whenever possible, a new idea will begin with a question, a simple example, or a problem that needs to be solved. We will build the intuition first, use figures and numerical examples where they help, and then introduce the mathematics needed to describe the idea properly.

GNU Radio will be our laboratory.

We will use it to:

- generate signals
- look at signals in different ways
- change parameters while the system is running
- test our predictions
- deliberately create problems
- understand why those problems occur
- build increasingly realistic transmitters and receivers

By the end of the book, the reader should be able to look at an SDR problem and think about what needs to happen to the signal before deciding which GNU Radio blocks to use.

---

# Part I: Learning to Think in Signals

---

# Chapter 1: What Is Software Defined Radio?

## Main Question

What makes a radio "software defined"?

## Concepts

- What a radio actually does
- Traditional hardware radio
- Software Defined Radio
- Analog and digital signal processing
- Basic transmitter
- Basic receiver
- RF front end
- ADC
- DAC
- Baseband processing
- Why SDR is useful
- What GNU Radio is
- Where GNU Radio fits into an SDR system

## Intuition We Want to Build

A radio is fundamentally a chain of operations performed on signals.

Traditional radios perform many of those operations using dedicated hardware.

An SDR moves many of them into the digital domain, where software can perform and change the processing.

GNU Radio gives us a practical way to build those signal-processing chains.

## Mathematics

Keep mathematics very light.

Introduce a sinusoidal signal only as an example of how a signal can be described:

$$
x(t)=A\cos(2\pi ft+\phi)
$$

There is no need to derive this yet.

## GNU Radio Experiment

Build the first flowgraph:

```text
Signal Source → Throttle → QT GUI Time Sink
```

Generate a sinusoid and observe it.

## GNU Radio Direction

Introduce:

- GNU Radio Companion
- block library
- blocks
- connections
- source blocks
- sink blocks
- block properties
- Run
- Stop
- basic flowgraph errors

Briefly point out that GNU Radio ports have different colours, without explaining data types in detail yet.

## Now Break the Flowgraph

- Disconnect a block
- Leave an important parameter invalid
- Observe how GNU Radio reports a problem

## Leads Into

What signals actually are.

---

# Chapter 2: Understanding Signals

## Main Question

What exactly is a signal?

## Concepts

- Signals as information
- Time-domain representation
- Amplitude
- Frequency
- Period
- Phase
- DC offset
- Sinusoids
- Multiple signals
- Adding signals
- Waveform shape
- Continuous-time and discrete-time signals

## Intuition We Want to Build

A signal is a quantity that changes and carries information.

Amplitude tells us how large the signal is.

Frequency tells us how quickly it repeats.

Phase tells us where it is in its cycle.

## Mathematics

Introduce:

$$
T=\frac{1}{f}
$$

and revisit:

$$
x(t)=A\cos(2\pi ft+\phi)
$$

Use numerical examples instead of leaving the expressions abstract.

## GNU Radio Experiment

Generate a sinusoid.

Change:

- amplitude
- frequency
- phase
- offset

Then generate two signals and add them.

## GNU Radio Direction

Introduce or expand:

- Signal Source
- Throttle
- QT GUI Time Sink
- Variable
- Add
- Time Sink display controls
- multiple signal paths

## Now Break the Flowgraph

Use unusual values for amplitude, frequency, phase and offset.

Before running the flowgraph, predict what should happen.

## Leads Into

Sampling.

---

# Chapter 3: Sampling and Aliasing

## Main Question

How does a computer see a continuous signal?

## Concepts

- Continuous signals
- Samples
- Discrete-time signals
- Sampling frequency
- Sampling period
- Samples per cycle
- Nyquist criterion
- Nyquist frequency
- Undersampling
- Aliasing
- Apparent frequency

## Intuition We Want to Build

A computer does not see the smooth curve we draw on paper.

It sees individual numbers taken at particular moments.

If those measurements are taken too slowly, different analog signals can produce the same sequence of samples.

## Mathematics

Introduce:

$$
T_s=\frac{1}{f_s}
$$

Samples per cycle:

$$
N=\frac{f_s}{f}
$$

Then introduce the Nyquist criterion:

$$
f_s>2f_{\max}
$$

Only introduce aliasing mathematically after the reader has seen it.

## GNU Radio Experiment

Generate a fixed-frequency sinusoid.

Gradually reduce the sample rate.

Observe both the Time Sink and Frequency Sink.

Distinguish carefully between:

- having only a few samples per cycle
- poor-looking waveform reconstruction
- reaching the Nyquist boundary
- actual aliasing

## GNU Radio Direction

Introduce:

- QT GUI Range
- runtime parameter control
- sample-rate variables
- QT GUI Frequency Sink lightly
- sample-rate relationships
- Throttle in greater depth

## Now Break the Flowgraph

- Violate Nyquist deliberately
- Try special relationships such as signal frequency equal to sample rate
- Remove Throttle
- Use inconsistent sample-rate values

## Leads Into

The numbers GNU Radio uses to represent signals.

---

# Chapter 4: Complex Numbers for SDR

## Main Question

Why would a radio need imaginary numbers to describe a real signal?

## Concepts

- Real numbers
- Imaginary numbers
- Complex numbers
- Real component
- Imaginary component
- Complex plane
- Magnitude
- Phase
- Euler's formula
- Complex exponential
- Rotating-vector interpretation

## Intuition We Want to Build

A complex number gives us a convenient way to keep two related quantities together.

For SDR, this becomes extremely useful because a complex sample can represent both magnitude and phase information.

## Mathematics

Introduce:

$$
z = I + jQ
$$

Magnitude:

$$
|z| = \sqrt{I^2 + Q^2}
$$

Phase:

$$
\theta = \mathrm{atan2}(Q,I)
$$

Then gradually introduce:

$$
e^{j\theta} = \cos(\theta) + j\sin(\theta)
$$

## GNU Radio Experiment

Generate real and complex samples.

Separate a complex signal into its real and imaginary components.

Display both.

## GNU Radio Direction

Introduce:

- GNU Radio data types
- Float
- Complex
- Float to Complex
- Complex to Real
- Complex to Imag
- port colours
- type compatibility

## Now Break the Flowgraph

- Connect incompatible types
- Swap real and imaginary components
- Remove one component

## Leads Into

I and Q.

---

# Chapter 5: I and Q Signals

## Main Question

Why do SDR receivers represent signals using I and Q?

## Concepts

- In-phase component
- Quadrature component
- 90-degree relationship
- Complex baseband
- Magnitude
- Phase
- Complex rotation
- Positive and negative rotation
- Why SDR hardware produces IQ samples

## Important Connection

The real and imaginary components from the previous chapter now receive their radio names:

$$
x[n]=I[n]+jQ[n]
$$

## Intuition We Want to Build

I and Q are not two unrelated signals.

Together they describe one complex signal.

This representation lets us preserve information that would be lost if we kept only a single real waveform.

## GNU Radio Experiment

Generate I and Q separately.

Combine them into a complex stream.

Display:

- I against time
- Q against time
- magnitude
- phase
- constellation

## GNU Radio Direction

Introduce:

- Signal Source configured for Complex output
- Float to Complex
- Complex to Mag
- Complex to Arg
- QT GUI Constellation Sink
- multiple GUI views

## Now Break the Flowgraph

- Make I and Q identical
- Set Q to zero
- Reverse Q
- Change their phase relationship

Observe what happens to the complex signal.

## Leads Into

Looking inside signals using frequency.

---

# Part II: Seeing What Is Inside a Signal

---

# Chapter 6: From Time Domain to Frequency Domain

## Main Question

How can several frequencies exist inside one waveform?

## Concepts

- Time domain
- Frequency domain
- Sinusoidal decomposition
- Fourier transform intuition
- DFT
- FFT
- FFT bins
- Frequency resolution
- Magnitude spectrum
- Windowing
- Spectral leakage

## Intuition We Want to Build

The time-domain waveform and frequency-domain spectrum are two different views of the same signal.

A complicated-looking waveform may simply be several sinusoids added together.

## GNU Radio Experiment

Generate several tones.

Add them together.

Observe the same signal using:

- Time Sink
- Frequency Sink

Then experiment with:

- FFT size
- frequency resolution
- window functions

## GNU Radio Direction

Introduce in depth:

- QT GUI Frequency Sink
- FFT size
- FFT averaging
- window functions
- dB scale
- frequency axis
- Waterfall Sink

## Now Break the Flowgraph

Create spectral leakage deliberately.

Use poor FFT resolution.

Compare different windows.

## Leads Into

Positive and negative frequencies.

---

# Chapter 7: Positive and Negative Frequencies

## Main Question

What does a negative frequency actually mean?

## Concepts

- Positive frequency
- Negative frequency
- Direction of complex rotation
- Real cosine spectrum
- Spectral symmetry
- Complex exponential
- One-sided complex tones
- Frequencies relative to a reference

## Intuition We Want to Build

Negative frequency does not mean that an electromagnetic wave is travelling backward.

It describes the opposite direction of rotation in the complex plane.

## Mathematics

Compare:

$$
\cos(2\pi ft)
\=
\frac{1}{2}e^{j2\pi ft}
+
\frac{1}{2}e^{-j2\pi ft}
$$

with:

$$
e^{j2\pi ft}
$$

## GNU Radio Experiment

Compare the spectra of:

- a real cosine
- a positive complex tone
- a negative complex tone

## Expected Observation

A real cosine contains symmetric components at positive and negative frequencies.

A complex tone can contain only one of them.

## Now Break the Flowgraph

Convert the complex tone to a real signal.

Observe the mirror component appear.

## Leads Into

Noise and real-world signals.

---

# Chapter 8: Noise, Power and SNR

## Main Question

Why do real signals never look perfectly clean?

## Concepts

- Noise
- Random signals
- Gaussian noise
- White noise
- Noise floor
- Signal power
- Noise power
- SNR
- Decibels
- Detectability
- Dynamic range

## Intuition We Want to Build

Noise is not simply an ugly waveform added to our signal.

It determines how reliably we can detect and recover information.

## Mathematics

Introduce:

$$
\mathrm{SNR}=\frac{P_s}{P_n}
$$

and:

$$
\mathrm{SNR}_{dB}
\=
10\log_{10}
\left(
\frac{P_s}{P_n}
\right)
$$

## GNU Radio Experiment

Add adjustable Gaussian noise to a sinusoid.

Observe the signal in:

- time
- frequency

Later construct a proper signal/noise power measurement rather than treating Number Sink as an automatic SNR meter.

## GNU Radio Direction

Introduce:

- Noise Source
- Multiply Const
- Number Sink where useful
- averaging

## Now Break the Flowgraph

Gradually bury the signal in noise.

Ask when it becomes difficult to identify in time and frequency.

## Leads Into

Moving signals around the spectrum.

---

# Part III: Moving and Shaping Signals

---

# Chapter 9: Mixing and Frequency Translation

## Main Question

How does a radio move a signal from one frequency to another?

## Concepts

- Mixer
- Local oscillator
- Frequency translation
- Upconversion
- Downconversion
- Sum frequency
- Difference frequency
- Real mixing
- Complex mixing
- Baseband
- Frequency offset

## Intuition We Want to Build

Mixing moves information from one part of the spectrum to another.

Real and complex mixing do not behave in exactly the same way.

## GNU Radio Experiment 1: Real Mixing

Multiply a real signal by a real local oscillator.

Observe the sum and difference frequencies.

## GNU Radio Experiment 2: Complex Mixing

Repeat the experiment using complex signals.

Observe how complex mixing can translate the spectrum in one direction.

## GNU Radio Direction

Introduce:

- Multiply
- complex oscillators
- runtime LO control
- frequency translation

## Now Break the Flowgraph

- Mistune the LO
- Place the signal above the LO
- Place it below the LO
- Reverse the complex LO

## Leads Into

Channel selection and filtering.

---

# Chapter 10: Filters and Channel Selection

## Main Question

How can a receiver keep the signal it wants and reject everything else?

## Concepts

- Filtering
- Low-pass filter
- High-pass filter
- Band-pass filter
- Band-stop filter
- Cutoff frequency
- Transition bandwidth
- Passband
- Stopband
- FIR filters
- Filter order
- Channel selection

## Intuition We Want to Build

A filter does not simply "remove noise."

It changes different parts of the spectrum by different amounts.

## GNU Radio Experiment

Generate several signals at different frequencies.

Add them together.

Use filters to keep or remove selected components.

Observe the signal before and after filtering.

## GNU Radio Direction

Introduce:

- Low Pass Filter
- High Pass Filter
- Band Pass Filter
- Band Reject Filter
- filter taps
- filter windows
- decimation

## Now Break the Flowgraph

- Use the wrong cutoff
- Use an unrealistic transition width
- use the wrong sample rate
- change decimation unexpectedly

## Leads Into

What a filter is actually doing to the signal.

---

# Chapter 11: Impulse Response and Convolution

## Main Question

If we know how a system responds to one impulse, can we predict how it responds to any signal?

## Concepts

- System
- Impulse
- Impulse response
- Linear time-invariant system intuition
- Convolution
- FIR filtering
- Input/output relationship

## Intuition We Want to Build

A complicated signal can be thought of as many shifted and scaled impulses.

If we know what the system does to one impulse, we can build its response to the entire signal.

## Mathematics

Only after building the intuition, introduce:

$$
y[n]
\=
\sum_{k=-\infty}^{\infty}
x[k]h[n-k]
$$

## GNU Radio Experiment

Use simple finite sequences first.

Observe the impulse response of an FIR filter.

Then pass a more complicated signal through the same system.

## GNU Radio Direction

Introduce or expand:

- FIR Filter
- filter taps
- Vector Source
- Head
- Repeat
- finite sequences

## Now Break the Flowgraph

- Change the taps
- Reverse the taps
- insert unexpected tap values

Observe how the output changes.

## Leads Into

Correlation.

---

# Chapter 12: Correlation, Matched Filtering and Signal Detection

## Main Question

How can a receiver find a known signal hidden inside another signal?

## Concepts

- Similarity
- Cross-correlation
- Autocorrelation
- Delay estimation
- Detection
- Correlation peak
- Matched-filter intuition
- Noise and detection

## Intuition We Want to Build

Correlation asks:

> How much does this part of the received signal look like the signal I am searching for?

## GNU Radio Experiment

Create a known sequence.

Delay it.

Add noise.

Try to find where the sequence occurs.

The exact GNU Radio implementation should be finalized only after testing several approaches and choosing the clearest one for a beginner.

## GNU Radio Direction

Possible tools include:

- Delay
- Conjugate
- Multiply
- Moving Average
- Vector processing
- correlation-related blocks

## Now Break the Flowgraph

- Use the wrong reference
- increase noise
- change delay
- weaken the signal

## Leads Into

Putting information onto carriers.

---

# Part IV: Analog Communication

---

# Chapter 13: Why Modulation Exists

## Main Question

Why can't we simply transmit the original information signal directly?

## Concepts

- Baseband
- Passband
- Carrier
- Modulation
- Spectrum allocation
- antenna considerations
- frequency sharing
- bandwidth

## GNU Radio Experiment

Take a low-frequency message and move it to a higher-frequency region.

Observe the spectrum before and after.

## Leads Into

Amplitude modulation.

---

# Chapter 14: Amplitude Modulation

## Main Question

How can information be carried by changing the amplitude of a carrier?

## Concepts

- Carrier
- Message
- AM
- Modulation index
- Sidebands
- Carrier component
- Envelope
- Overmodulation
- AM demodulation

## GNU Radio Experiment

Construct AM from simple blocks first rather than hiding the operation inside an all-in-one block.

Conceptually:

```text
Message
   ↓
Scaling
   ↓
Add carrier/DC term
   ↓
Multiply by Carrier
```

Observe the waveform and spectrum at each stage.

Then build the receiver.

## Now Break the Flowgraph

Overmodulate deliberately.

Observe what happens to the envelope and recovered signal.

## Leads Into

Frequency modulation.

---

# Chapter 15: Frequency Modulation

## Main Question

What happens if information changes the instantaneous frequency instead of amplitude?

## Concepts

- FM
- Instantaneous frequency
- Frequency deviation
- Modulation index
- FM bandwidth
- FM demodulation
- Narrowband FM
- Wideband FM

## GNU Radio Experiment

Build an FM transmitter and receiver in software.

## GNU Radio Direction

Introduce:

- NBFM/WBFM processing
- Audio Source
- Audio Sink
- quadrature rate
- audio rate
- interpolation
- decimation
- Rational Resampler

## Important Connection

This is where the reader begins working seriously with several sample rates inside one flowgraph.

## Now Break the Flowgraph

Use incorrect:

- quadrature rate
- audio rate
- interpolation
- decimation

Listen to and observe the result.

## Leads Into

Digital communication.

---

# Part V: From Bits to Waveforms

---

# Chapter 16: Bits, Symbols and Digital Communication

## Main Question

How can zeros and ones eventually become a radio waveform?

## Concepts

- Bits
- Bit rate
- Symbols
- Symbol rate
- Bits per symbol
- Mapping
- Binary data
- Why symbols are useful

## Intuition We Want to Build

A transmitter does not normally send abstract zeros and ones directly.

It maps groups of bits onto physical signal states that can be transmitted.

## Mathematics

Introduce the relationship between bit rate and symbol rate using simple examples.

For a modulation carrying $k$ bits per symbol:

$$
R_b=kR_s
$$

## GNU Radio Experiment

Generate digital data.

Group bits into symbols.

Inspect the values before modulation.

## GNU Radio Direction

Introduce:

- Random Source
- byte streams
- bit manipulation
- Repack Bits where useful
- Vector Source for controlled examples

## Leads Into

The simplest forms of linear digital modulation.

---

# Chapter 17: Linear Modulation and PAM

## Main Question

What if we represent information using different signal amplitudes?

## Concepts

- Linear modulation
- Baseband symbols
- Pulse Amplitude Modulation
- 2-PAM
- 4-PAM
- Symbol levels
- Symbol decisions
- Hard decisions
- Decision thresholds
- Symbol energy
- Noise and wrong decisions

## Intuition We Want to Build

A digital symbol can be represented by choosing one signal level from a known set.

For example:

```text
Bit 0 → -1
Bit 1 → +1
```

Now the receiver's problem becomes:

> Which level was most likely transmitted?

## GNU Radio Experiment

Generate a known bit sequence.

Map it to 2-PAM.

Then try 4-PAM.

Add noise and observe how the received levels spread.

## Important Receiver Idea

At the receiver, the measured value will not usually land exactly on one of the ideal symbol levels.

The receiver therefore has to make a decision.

For a simple 2-PAM signal, a received value might look like:

```text
Received value: +0.82
        ↓
Which valid symbol is closest?
        ↓
Detected symbol: +1
```

The same idea will later extend from points on a line to points in the I/Q plane.

## Now Break the Flowgraph

Increase the noise until symbols begin crossing decision boundaries.

## Leads Into

Using both I and Q to carry symbols.

---

# Chapter 18: BPSK, QPSK and QAM

## Main Question

How can I and Q carry digital information?

## Concepts

- BPSK
- QPSK
- M-PSK idea
- QAM
- 16-QAM
- constellation points
- bits per symbol
- decision regions
- symbol mapping
- Gray coding intuition

## Important Connection

Earlier we learned:

$$
x[n]=I[n]+jQ[n]
$$

Now we use those two dimensions to represent information.

## Intuition We Want to Build

A constellation point is simply a particular combination of I and Q.

Different points can represent different groups of bits.

## GNU Radio Experiment

Progress through:

```text
BPSK
↓
QPSK
↓
16-QAM
```

Display each using the Constellation Sink.

## GNU Radio Direction

Introduce:

- constellation objects
- symbol mapping
- digital modulation tools
- Constellation Sink in greater depth

## Now Break the Flowgraph

Introduce:

- amplitude error
- phase rotation
- noise

Observe how the constellation changes.

## Leads Into

Turning symbols into practical waveforms.

---

# Chapter 19: Pulse Shaping and Matched Filtering

## Main Question

Why can't we simply transmit abrupt rectangular symbols over the air?

## Concepts

- Symbol waveform
- Bandwidth
- Rectangular pulses
- Intersymbol interference
- Pulse shaping
- Nyquist pulse-shaping idea
- Raised cosine
- Root-raised cosine
- Samples per symbol
- Matched filtering
- Eye diagram

## Intuition We Want to Build

The way we shape each transmitted symbol affects both bandwidth and how easily neighbouring symbols can be distinguished.

The receiver can use a matching filter to improve detection.

## Watch Out: Two Different Nyquist Ideas

We already met Nyquist in Chapter 3 when discussing sampling.

There, the question was:

> How fast must we sample a signal to avoid aliasing?

Here, Nyquist appears again in a different context.

Now the question is:

> How can we shape transmitted pulses so that neighbouring symbols do not interfere at the correct sampling instants?

These are different problems. Do not confuse the Nyquist sampling criterion with the Nyquist zero-ISI pulse-shaping criterion.

## GNU Radio Experiment

Compare:

- unshaped symbols
- rectangular pulses
- RRC-shaped symbols

Then add the receiver matched filter.

Observe:

- time waveform
- spectrum
- constellation
- eye behaviour where practical

## GNU Radio Direction

Introduce:

- RRC taps
- interpolation
- samples per symbol
- matched filtering
- timing visualization

## Now Break the Flowgraph

- use mismatched filters
- use the wrong samples per symbol
- change roll-off
- remove the matched filter

## Leads Into

What happens between transmitter and receiver.

---

# Part VI: The Wireless Channel

---

# Chapter 20: What Happens to a Signal Over the Air?

## Main Question

Why does the receiver never see exactly what the transmitter sent?

## Concepts

- Wireless channel
- Path loss
- Attenuation
- AWGN
- Delay
- Multipath
- Reflections
- Fading
- Flat fading
- Frequency-selective fading
- Doppler introduction
- Channel impulse response

## Intuition We Want to Build

The receiver may receive several delayed and weakened copies of the same transmitted signal.

These copies add together.

Sometimes they help each other.

Sometimes they partially cancel.

## GNU Radio Experiment

Begin with a clean digital signal.

Pass it through progressively more realistic channels:

```text
Clean
↓
Noise
↓
Attenuation
↓
Frequency offset
↓
Multipath
```

Observe the constellation and spectrum after each impairment.

## GNU Radio Direction

Introduce in depth:

- Channel Model
- noise voltage
- frequency offset
- timing/sample-rate offset
- multipath taps

## Now Break the Flowgraph

This chapter is largely a controlled signal-breaking laboratory.

## Leads Into

Multipath distortion and equalization.

---

# Chapter 21: Multipath, ISI and Equalization

## Main Question

If the channel distorts our symbols, can the receiver undo some of that distortion?

## Concepts

- Multipath revisited
- Delayed copies
- Channel impulse response
- Intersymbol interference
- Equalization
- Zero-forcing intuition
- Adaptive equalization intuition
- Training sequence
- Decision-directed operation

## Intuition We Want to Build

Equalization attempts to compensate for distortion introduced by the channel.

It does not magically recreate information that has disappeared. It tries to undo predictable channel effects.

## GNU Radio Experiment

Start with a clean QPSK or QAM signal.

Then:

```text
Clean signal
↓
Multipath channel
↓
Distorted constellation
↓
Equalizer
↓
Improved constellation
```

## GNU Radio Direction

Introduce suitable GNU Radio equalization tools only after the underlying problem is visible.

## Now Break the Flowgraph

- use the wrong equalizer settings
- increase multipath
- remove training
- add more noise

## Leads Into

Receiver synchronization.

---

# Part VII: Teaching the Receiver Where to Look

---

# Chapter 22: PLL and Carrier Synchronization

## Main Question

The transmitter and receiver have different oscillators. How can the receiver lock onto the transmitted carrier?

## Concepts

- Oscillator mismatch
- Carrier frequency offset
- Carrier phase offset
- Phase detector
- Feedback
- Loop filter
- Oscillator correction
- Phase-Locked Loop
- Carrier recovery
- Costas Loop
- Lock
- Acquisition
- Tracking

## Intuition We Want to Build

A PLL repeatedly asks:

> Am I ahead or behind the signal I am trying to follow?

It uses the answer to continuously correct its local oscillator.

## Learning Order

First:

- simple phase error

Then:

- PLL intuition

Then:

- frequency error

Then:

- carrier recovery for modulated signals

Finally:

- Costas Loop

## GNU Radio Experiment

Create a signal with controlled carrier phase and frequency errors.

Observe the constellation before and after recovery.

## GNU Radio Direction

Introduce:

- PLL-related tools
- Costas Loop
- frequency/phase controls
- loop bandwidth concept

## Now Break the Flowgraph

- increase frequency offset
- increase phase offset
- use an inappropriate loop bandwidth
- disable carrier recovery

## Leads Into

Symbol timing.

---

# Chapter 23: Clock and Symbol Timing Synchronization

## Main Question

How does the receiver know exactly when to measure each symbol?

## Concepts

- Transmitter clock
- Receiver clock
- Symbol timing
- Timing offset
- Clock mismatch
- Sampling instant
- Timing error
- Eye diagram
- Timing recovery
- Symbol synchronization

## Intuition We Want to Build

Even if the receiver knows the correct carrier frequency and phase, it can still make wrong decisions if it looks at the waveform at the wrong moment.

## GNU Radio Experiment

Create a pulse-shaped digital signal.

Introduce timing error.

Observe what happens when samples are taken:

- near the centre of the symbol
- too early
- too late

Then apply timing recovery.

## GNU Radio Direction

Introduce:

- Symbol Sync
- timing-error concepts
- clock recovery tools where appropriate

## Now Break the Flowgraph

- disable Symbol Sync
- introduce timing offset
- introduce sample-rate mismatch

## Leads Into

Finding packets and frames.

---

# Chapter 24: Frame Synchronization and Packet Detection

## Main Question

Even after recovering the symbols, how does the receiver know where a message begins?

## Concepts

- Continuous symbol stream
- Frames
- Packets
- Preambles
- Access codes
- Known sequences
- Correlation revisited
- Packet detection
- Frame synchronization
- False detection
- Detection threshold

## Important Connection

Return to Chapter 12.

Correlation is no longer an isolated mathematical idea.

It now solves a real receiver problem.

## GNU Radio Experiment

Create:

```text
Preamble + Payload
```

Transmit it repeatedly.

Add noise.

Detect the preamble and determine where each frame begins.

## GNU Radio Direction

Introduce appropriate:

- correlation blocks
- access-code tools
- tags where useful

Do not explain the complete GNU Radio tag architecture yet. That comes later.

## Now Break the Flowgraph

- use the wrong preamble
- shorten the preamble
- increase noise
- change detection threshold

## Leads Into

Error detection and forward error correction.

---

# Chapter 25: Error Detection and Forward Error Correction

## Main Question

Why would a communication system intentionally transmit extra bits?

## Concepts

- Transmission errors
- Redundancy
- Error detection
- Error correction
- Parity intuition
- Forward Error Correction
- Coding rate
- Coding gain intuition
- Trade-off between reliability and data rate
- Hard decisions
- Soft decisions introduction
- Why practical communication systems use channel coding

## Intuition We Want to Build

Noise and channel distortion sometimes cause the receiver to make the wrong symbol or bit decision.

One way to improve reliability is to add carefully structured redundancy before transmission.

Those extra bits give the receiver clues that can help it detect, and in some cases correct, errors.

## A Simple Example

Begin with a deliberately simple repetition example.

Instead of sending one bit:

```text
1
```

suppose we send:

```text
1 1 1
```

If the receiver gets:

```text
1 0 1
```

it can still make a reasonable guess that the original bit was `1`.

This is not an efficient coding method, but it makes the basic idea easy to see: we spend extra transmitted data in exchange for greater reliability.

## Mathematics

If $k$ information bits become $n$ coded bits, the coding rate is

$$
R_c=rac{k}{n}
$$

For example, if 2 information bits become 3 coded bits:

$$
R_c=rac{2}{3}
$$

Do not begin with generator matrices or advanced coding theory.

## GNU Radio Experiment

Build a simple coded digital link:

```text
Bits
↓
Encoder
↓
Modulation
↓
Noisy Channel
↓
Demodulation
↓
Decoder
↓
Recovered Bits
```

Compare the received data:

```text
Without coding
```

and:

```text
With coding
```

The exact GNU Radio FEC block chain should be validated using the supported GNU Radio version before this chapter is written.

## GNU Radio Direction

Introduce conceptually:

- FEC encoder
- FEC decoder
- coding rate
- hard versus soft information where useful

Do not try to teach the complete GNU Radio FEC API here.

## Now Break the Flowgraph

- increase the channel noise
- remove the decoder
- use mismatched encoder and decoder settings
- compare coded and uncoded performance

## What We Want the Reader to Understand

The reader does not need to become a coding-theory specialist.

They should understand why practical communication systems deliberately add redundancy and where coding sits inside an SDR transmitter and receiver.

## Leads Into

Building the complete single-carrier digital receiver.

---

# Chapter 26: Building a Complete Single-Carrier Digital Receiver

## Main Question

Can we now combine everything into one receiver?

## Purpose

This chapter brings together the ideas developed since Chapter 16.

## Conceptual Receiver

```text
Received IQ
    ↓
Channel Filtering
    ↓
AGC
    ↓
Matched Filter
    ↓
Carrier Recovery
    ↓
Timing Recovery
    ↓
Equalization
    ↓
Symbol Decisions
    ↓
Frame Detection
    ↓
Recovered Bits
```

The exact order of some stages may depend on the receiver design. This itself should become part of the discussion.

## GNU Radio Experiment

Build a complete software transmitter, channel and receiver.

Start with ideal conditions.

Then introduce impairments one at a time.

## Main Goal

The reader should now understand why each receiver stage exists.

## Now Break the Flowgraph

Disable one receiver stage at a time.

Observe what failure looks like.

## Leads Into

Multicarrier communication.

---

# Part VIII: OFDM and Multicarrier Communication

---

# Chapter 27: Why OFDM?

## Main Question

Why transmit data on many subcarriers instead of one fast carrier?

## Concepts

- Single-carrier communication
- High symbol rate
- Multipath problem
- Multicarrier idea
- Subcarriers
- Orthogonality
- OFDM
- Subcarrier spacing
- Parallel data streams

## Intuition We Want to Build

Instead of sending one very fast stream through a difficult multipath channel, OFDM divides the data among many slower subcarriers.

The word "orthogonal" should be explained visually and intuitively before being treated mathematically.

## GNU Radio Experiment

Generate several equally spaced subcarriers.

Observe:

- individual subcarriers
- combined waveform
- combined spectrum

Explore why overlapping spectra do not automatically mean that the subcarriers interfere.

## Leads Into

How an OFDM waveform is actually created.

---

# Chapter 28: Building an OFDM Signal with the IFFT

## Main Question

Do we really need hundreds of individual oscillators to generate hundreds of subcarriers?

## Concepts

- Frequency-domain symbols
- Subcarrier bins
- IFFT
- FFT
- OFDM symbol
- Active subcarriers
- Null subcarriers
- DC carrier
- Pilot carriers introduction

## Important Connection

Return to the FFT from Chapter 6.

Earlier we used the FFT to **\*\*look at a signal\*\***.

Now we use the IFFT to **\*\*build a signal\*\***.

## Conceptual Transmitter

```text
Bits
↓
QAM Symbols
↓
Place Symbols on Subcarriers
↓
IFFT
↓
Time-Domain OFDM Symbol
```

## GNU Radio Experiment

Construct a simple OFDM symbol.

Inspect it in both time and frequency.

Then recover the subcarrier symbols using an FFT.

## Leads Into

Multipath protection.

---

# Chapter 29: Cyclic Prefix, OFDM Channel and Basic Channel Estimation

## Main Question

How does OFDM deal with multipath?

## Concepts

- OFDM symbol duration
- Multipath delay
- Guard interval
- Cyclic prefix
- Why the prefix is copied rather than filled with zeros
- Inter-symbol interference
- Channel response
- Pilot carriers
- Basic channel estimation
- One-tap equalization intuition
- Frequency offset sensitivity

## Intuition We Want to Build

The cyclic prefix gives delayed copies of the previous part of the waveform somewhere safe to land, provided the channel delay is not too long.

Channel estimation then helps us understand how each subcarrier has been altered.

## GNU Radio Experiment

Build:

```text
QAM
↓
IFFT
↓
Add Cyclic Prefix
↓
Multipath Channel
↓
Remove Cyclic Prefix
↓
FFT
↓
Channel Correction
↓
Recovered QAM
```

Compare the receiver:

- without cyclic prefix
- with cyclic prefix

## Now Break the Flowgraph

- make the cyclic prefix too short
- increase multipath delay
- introduce carrier frequency offset
- remove channel correction

## Leads Into

Understanding GNU Radio itself more deeply.

---

# Part IX: Understanding GNU Radio Beyond Flowgraphs

---

# Chapter 30: Streams, Vectors, Tags, Messages and PDUs

## Main Question

What is actually moving between GNU Radio blocks?

## Concepts

- Items
- Streams
- Vectors
- Stream to Vector
- Vector to Stream
- Stream tags
- Tagged streams
- Messages
- Message ports
- PMT concept
- PDUs
- Metadata
- Packet-oriented processing

## Intuition We Want to Build

Not everything in a radio system is simply another endless stream of samples.

GNU Radio provides different mechanisms for:

- continuous sample processing
- grouped data
- metadata
- asynchronous events
- packets

## GNU Radio Experiment

Build small examples showing each mechanism separately.

For example:

```text
Stream:
1, 2, 3, 4, 5, 6 ...
```

then:

```text
Vector length 3:
[1,2,3], [4,5,6] ...
```

Then demonstrate:

- a stream tag
- a message
- a simple PDU

## GNU Radio Direction

Introduce in depth:

- Stream to Vector
- Vector to Stream
- tags
- tagged streams
- Message Debug
- PDUs
- Tagged Stream to PDU
- PDU to Tagged Stream

## Leads Into

Building larger GNU Radio applications.

---

# Chapter 31: Building Larger GNU Radio Systems

## Main Question

How do we move from experimental flowgraphs to reusable SDR applications?

## Concepts

- Flowgraph organization
- Reusable processing chains
- Hierarchical blocks
- Parameters
- Embedded Python Blocks
- Generated Python
- File input/output
- Recorded IQ
- Network input/output
- Debugging
- Logging
- Scheduler intuition
- Buffers
- Performance
- CPU limitations

## Part A: Building Reusable Processing

Introduce:

- Hierarchical Blocks
- parameters
- Embedded Python Block
- generated Python

Take an existing processing chain and turn it into a reusable component.

## Part B: Working with the Outside World

Introduce:

- File Source
- File Sink
- IQ recording
- playback
- network blocks
- debugging
- logging
- performance awareness

## Now Break the Flowgraph

Introduce:

- parameter mismatches
- Python errors
- excessive sample rates
- expensive filters
- too many GUI sinks

Learn to locate where the problem begins.

## Leads Into

Real SDR hardware.

---

# Part X: Leaving the Simulation

---

# Chapter 32: SDR Hardware

## Main Question

What changes when our samples come from an antenna instead of Signal Source?

## Concepts

- Antenna
- RF front end
- LNA
- mixer
- ADC
- DAC
- centre frequency
- sample rate
- RF bandwidth
- gain
- dynamic range
- clipping
- frequency accuracy
- IQ samples
- hardware limitations
- DC offset
- Centre-frequency or DC spike
- IQ imbalance introduction
- Oscillator frequency error

## Real Hardware Does Not Look Perfect

When we first connect an actual SDR, the spectrum may contain things that did not appear in our simulations.

For example:

- a strong component at the exact centre of the spectrum
- a small frequency error
- unequal I and Q behaviour
- additional spurious components

These are not necessarily real radio transmissions. Some may come from imperfections inside the receiver itself.

We will introduce these effects here without turning this chapter into an RF calibration course.

## Hardware Examples

Discuss common devices conceptually:

- RTL-SDR
- ADALM-Pluto
- HackRF
- USRP

The book should not depend completely on one device.

## GNU Radio Experiment

Connect supported SDR hardware.

Display a real RF spectrum.

Explore:

- centre frequency
- sample rate
- bandwidth
- gain

## Important Distinction

Make absolutely clear that:

**\*\*Centre frequency\*\*** determines where we are looking in the RF spectrum.

**\*\*Sample rate\*\*** determines how much spectrum can be represented around that centre and how many samples are produced per second.

## Now Break the Flowgraph

- use too much gain
- use too little gain
- choose a poor sample rate
- tune away from the signal

Observe real-world consequences.

## Leads Into

Receiving a real transmission.

---

# Chapter 33: Receiving a Real Radio Signal

## Main Question

Can we follow a real radio signal all the way from the antenna to recovered information?

## First Practical Receiver

Build a broadcast FM receiver.

Conceptually:

```text
Antenna
↓
SDR Source
↓
IQ Samples
↓
Frequency Translation
↓
Channel Filter
↓
Decimation / Resampling
↓
FM Demodulation
↓
Audio Processing
↓
Audio Sink
```

## Concepts Revisited

Bring together:

- IQ
- sampling
- FFT
- centre frequency
- mixing
- filtering
- resampling
- gain
- demodulation
- audio

## GNU Radio Direction

Introduce where useful:

- hardware Source
- Frequency Translating FIR Filter
- GUI layout
- Waterfall
- runtime tuning
- gain controls

## Now Break the Flowgraph

Misconfigure one stage at a time.

Ask:

> What does this failure look like?

and, where applicable:

> What does this failure sound like?

## Leads Into

Independent SDR design.

---

# Chapter 34: Build an SDR System from a Blank Flowgraph

## Main Question

Can you now solve an SDR problem without following somebody else's flowgraph?

## Purpose

This is the capstone chapter.

The reader begins with a blank GNU Radio Companion window.

Instead of receiving a finished flowgraph, they receive a requirement.

They must decide:

1. What signal enters the system?
2. What sample rate is appropriate?
3. Where is the desired signal in the spectrum?
4. Is frequency translation required?
5. What filtering is required?
6. Is resampling required?
7. Is synchronization required?
8. How should information be recovered?
9. How should intermediate signals be inspected?
10. How can the design be tested before hardware is used?

## Main Goal

The reader should no longer begin with:

> Which GNU Radio block should I use?

They should begin with:

> What needs to happen to the signal?

Then choose the GNU Radio tools that perform those operations.

---

# Appendix A: GNU Radio Quick Reference

A compact reference to commonly used GNU Radio blocks and important parameters.

---

# Appendix B: GNU Radio Data Types

Cover:

- Byte
- Short
- Integer
- Float
- Complex
- Vectors
- type conversions

---

# Appendix C: Common GNU Radio Errors

Examples:

- incompatible data types
- invalid parameters
- sample-rate mistakes
- missing dependencies
- Python errors
- hardware connection problems
- buffer problems
- performance problems

Include both:

**\*\*Flowgraph errors\*\***

and:

**\*\*Flowgraph runs, but the signal processing is wrong\*\***

---

# Appendix D: GNU Radio Block Index

Alphabetical index of the important GNU Radio blocks used in the book.

For each block, record the chapter where it is first introduced.

---

# Appendix E: GNU Radio Experiment Index

List every experiment and its corresponding `.grc` file.

For example:

```text
Chapter 03
├── basic-sampling.grc
├── interactive-sampling.grc
└── aliasing.grc
```

---

# Appendix F: Mathematics for SDR

A compact reference to mathematics used throughout the book.

Possible topics:

- complex numbers
- trigonometry
- logarithms
- decibels
- summation
- convolution
- correlation
- Fourier transform
- probability basics

This appendix is a reference.

It should not become a prerequisite mathematics course that the reader must finish before beginning Chapter 1.

---

# Appendix G: GNU Radio Toolbox Index

List every GNU Radio Toolbox entry in the book.

Examples:

- Signal Source
- Throttle
- Variable
- QT GUI Range
- Time Sink
- Frequency Sink
- Constellation Sink
- Channel Model
- Symbol Sync
- Costas Loop
- Stream Tags
- Message Debug
- Embedded Python Block

---

# Appendix H: Where to Go Next

Topics that deserve deeper study after this book:

- advanced OFDM
- MIMO
- advanced channel coding
- convolutional codes in depth
- turbo codes
- LDPC
- polar codes
- coding theory
- advanced channel estimation
- adaptive filters
- advanced equalization
- spread spectrum
- DSSS
- frequency hopping
- cognitive radio
- spectrum sensing
- direction finding
- beamforming
- radar
- satellite communications
- GNSS
- wireless security
- GNU Radio OOT modules
- custom C++ blocks
- FPGA acceleration
- RFNoC

---

# Overall Learning Path

The book now follows this progression:

```text
What Is SDR?
        ↓
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
Correlation and Detection
        ↓
Why Modulation?
        ↓
AM
        ↓
FM
        ↓
Bits and Symbols
        ↓
PAM
        ↓
BPSK / QPSK / QAM
        ↓
Pulse Shaping and Matched Filtering
        ↓
Wireless Channel
        ↓
Multipath and Equalization
        ↓
PLL and Carrier Recovery
        ↓
Clock / Symbol Timing Recovery
        ↓
Frame Synchronization
        ↓
Complete Digital Receiver
        ↓
Why OFDM?
        ↓
IFFT / FFT OFDM
        ↓
Cyclic Prefix and Channel Estimation
        ↓
GNU Radio Streams / Vectors / Tags / Messages / PDUs
        ↓
Larger GNU Radio Systems
        ↓
SDR Hardware
        ↓
Real RF Receiver
        ↓
Independent SDR Design
```

---

# A Rule for Advanced Chapters

As the book progresses, the subjects naturally become more advanced.

The writing style should not suddenly become more difficult just because the topic is difficult.

For topics such as:

- equalization
- PLL
- carrier recovery
- timing synchronization
- OFDM
- channel estimation

always begin with the **\*\*problem\*\***.

For example, do not begin the PLL chapter by deriving a feedback-loop transfer function.

Begin with:

> The transmitter and receiver each have their own oscillator. What happens if those oscillators are not exactly the same?

Let the reader see the problem.

Then try to solve it.

Only introduce the mathematics needed to explain why the solution works.

---

# Core Principle

Every major concept in this book should eventually answer four questions:

**\*\*What problem are we trying to solve?\*\***

**\*\*What is happening to the signal?\*\***

**\*\*Why does the solution work?\*\***

**\*\*Can I see it happen in GNU Radio?\*\***

The reader should not finish the book having memorized a collection of flowgraphs.

They should finish with enough understanding to build their own.