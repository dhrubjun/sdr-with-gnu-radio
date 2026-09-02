# SDR with GNU Radio: Chapter Plan

**Version 0.4**

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

# Teaching Philosophy

The book should continue to follow these principles throughout.

## Intuition Before Mathematics

Equations should support an idea after the reader has developed a physical or visual understanding of it.

Whenever possible:

```text
Question
↓
Intuition
↓
Experiment
↓
Observation
↓
Mathematics
↓
Engineering meaning
```

## Build Flowgraphs Progressively

Do not introduce a large final system all at once.

Start from the smallest experiment that demonstrates the idea, then extend it one stage at a time.

## Observe Before Correcting

When a signal impairment is introduced, first observe what it does.

Only after the failure signature is understood should the receiver correction be introduced.

## Break the Flowgraph Deliberately

Important chapters should include controlled failures.

The goal is not only to learn what works, but also to recognize what failure looks like.

## Keep Physical Meaning Visible

Whenever a parameter or algorithm has a physical interpretation, explain it.

Examples include:

- carrier-frequency offset as oscillator mismatch
- timing error as looking at the waveform at the wrong instant
- multipath as delayed copies of the transmitted signal
- equalization as compensation for channel memory
- correlation as a measure of similarity
- OFDM orthogonality as cancellation over the useful symbol interval

## Distinguish Measurements Carefully

Different displays answer different questions.

For example, an eye diagram and a constellation are not the same measurement.

The eye diagram characterizes the oversampled waveform around possible symbol-sampling instants and reveals timing margin and inter-symbol interference.

The constellation shows the complex samples actually selected at particular sampling instants and reflects symbol-domain effects such as carrier phase/frequency error, timing error, noise, and channel distortion.

A clean eye or constellation alone does not prove that the payload has been recovered correctly.

---

# Part I: Learning to Think in Signals

---

# Chapter 1: What Is Software Defined Radio?

## Main Question

What makes a radio "software defined"?

## Concepts

- what a radio actually does
- traditional hardware radio
- Software Defined Radio
- analog and digital signal processing
- transmitter and receiver chains
- RF front end
- ADC
- DAC
- baseband processing
- why SDR is useful
- what GNU Radio is
- where GNU Radio fits into an SDR system

## Intuition We Want to Build

A radio is fundamentally a chain of operations performed on signals.

Traditional radios perform many of those operations using dedicated hardware.

An SDR moves many of them into the digital domain, where software can perform and change the processing.

GNU Radio gives us a practical way to build those signal-processing chains.

## Mathematics

Keep mathematics very light.

Introduce a sinusoidal signal only as an example:

$$
x(t)=A\cos(2\pi ft+\phi)
$$

There is no need to derive it yet.

## GNU Radio Experiment

Build the first flowgraph:

```text
Signal Source
↓
Throttle
↓
QT GUI Time Sink
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

Briefly point out that GNU Radio ports have different colours without explaining data types in depth yet.

## Now Break the Flowgraph

- disconnect a block
- use an invalid parameter
- observe GNU Radio error messages

## Leads Into

What signals actually are.

---

# Chapter 2: Understanding Signals

## Main Question

What exactly is a signal?

## Concepts

- signals as information
- time-domain representation
- amplitude
- frequency
- period
- phase
- DC offset
- sinusoids
- waveform shape
- multiple signals
- addition of signals
- continuous-time and discrete-time signals

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

Use numerical examples rather than leaving the expressions abstract.

## GNU Radio Experiment

Generate a sinusoid and change:

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
- Time Sink controls
- multiple signal paths

## Now Break the Flowgraph

Use unusual values for amplitude, frequency, phase, and offset.

Predict what should happen before running the flowgraph.

## Leads Into

Sampling.

---

# Chapter 3: Sampling and Aliasing

## Main Question

How does a computer see a continuous signal?

## Concepts

- continuous signals
- samples
- discrete-time signals
- sampling frequency
- sampling period
- samples per cycle
- Nyquist criterion
- Nyquist frequency
- undersampling
- aliasing
- apparent frequency

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

Only introduce aliasing mathematically after the reader has seen it experimentally.

## GNU Radio Experiment

Generate a fixed-frequency sinusoid.

Gradually reduce the sample rate.

Observe both the Time Sink and Frequency Sink.

Distinguish carefully between:

- having only a few samples per cycle
- a rough-looking waveform
- reaching the Nyquist boundary
- actual aliasing

## GNU Radio Direction

Introduce:

- QT GUI Range
- runtime parameter control
- sample-rate variables
- QT GUI Frequency Sink
- sample-rate relationships
- Throttle in greater depth

## Now Break the Flowgraph

- violate Nyquist deliberately
- try special frequency/sample-rate relationships
- remove Throttle
- use inconsistent sample-rate values

## Leads Into

The numbers GNU Radio uses to represent signals.

---

# Chapter 4: Complex Numbers for SDR

## Main Question

Why would a radio need imaginary numbers to describe a real signal?

## Concepts

- real numbers
- imaginary numbers
- complex numbers
- real and imaginary components
- complex plane
- magnitude
- phase
- Euler's formula
- complex exponential
- rotating-vector interpretation

## Intuition We Want to Build

A complex number gives us a convenient way to keep two related quantities together.

For SDR, a complex sample can represent both magnitude and phase information.

## Mathematics

Introduce:

$$
z=I+jQ
$$

Magnitude:

$$
|z|=\sqrt{I^2+Q^2}
$$

Phase:

$$
\theta=\mathrm{atan2}(Q,I)
$$

Then gradually introduce:

$$
e^{j\theta}=\cos(\theta)+j\sin(\theta)
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

- connect incompatible types
- swap real and imaginary components
- remove one component

## Leads Into

I and Q.

---

# Chapter 5: I and Q Signals

## Main Question

Why do SDR receivers represent signals using I and Q?

## Concepts

- in-phase component
- quadrature component
- 90-degree relationship
- complex baseband
- magnitude
- phase
- complex rotation
- positive and negative rotation
- why SDR hardware produces IQ samples

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

- Signal Source with Complex output
- Float to Complex
- Complex to Mag
- Complex to Arg
- QT GUI Constellation Sink
- multiple GUI views

## Now Break the Flowgraph

- make I and Q identical
- set Q to zero
- reverse Q
- change their phase relationship

## Leads Into

Looking inside signals using frequency.

---

# Part II: Seeing What Is Inside a Signal

---

# Chapter 6: From Time Domain to Frequency Domain

## Main Question

How can several frequencies exist inside one waveform?

## Concepts

- time domain
- frequency domain
- sinusoidal decomposition
- Fourier transform intuition
- DFT
- FFT
- FFT bins
- frequency resolution
- magnitude spectrum
- windowing
- spectral leakage
- FFT normalization
- averaging
- waterfall display

## Intuition We Want to Build

The time-domain waveform and frequency-domain spectrum are two different views of the same signal.

A complicated-looking waveform may simply be several sinusoids added together.

## GNU Radio Experiment

Generate several tones.

Add them together.

Observe the same signal using:

- Time Sink
- Frequency Sink
- Waterfall Sink

Then experiment with:

- FFT size
- frequency resolution
- observation time
- window functions
- averaging

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

- create spectral leakage deliberately
- use poor FFT resolution
- compare windows
- change FFT size
- use different observation times

## Leads Into

Noise, power, and SNR.

---

# Chapter 7: Noise, Noise Floor, and SNR

## Main Question

Why do real signals never look perfectly clean?

## Concepts

- noise
- random signals
- Gaussian noise
- white noise
- noise floor
- signal power
- noise power
- SNR
- decibels
- detectability
- dynamic range

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
\mathrm{SNR}_{dB}=10\log_{10}\left(\frac{P_s}{P_n}\right)
$$

## GNU Radio Experiment

Add adjustable Gaussian noise to a sinusoid.

Observe the signal in time and frequency.

Construct meaningful signal/noise measurements rather than treating a Number Sink as an automatic SNR meter.

## GNU Radio Direction

Introduce:

- Noise Source
- Multiply Const
- Number Sink where useful
- averaging
- power interpretation

## Now Break the Flowgraph

Gradually bury the signal in noise.

Ask when it becomes difficult to identify in time and frequency.

## Leads Into

Moving signals around the spectrum.

---

# Part III: Moving and Shaping Signals

---

# Chapter 8: Mixing and Frequency Translation

## Main Question

How does a radio move a signal from one frequency to another?

## Concepts

- mixer
- local oscillator
- frequency translation
- upconversion
- downconversion
- sum frequency
- difference frequency
- real mixing
- complex mixing
- baseband
- frequency offset

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

- mistune the LO
- place the signal above the LO
- place it below the LO
- reverse the complex LO

## Leads Into

Channel selection and filtering.

---

# Chapter 9: Filters and Channel Selection

## Main Question

How can a receiver keep the signal it wants and reject everything else?

## Concepts

- filtering
- low-pass filter
- high-pass filter
- band-pass filter
- band-stop filter
- cutoff frequency
- transition bandwidth
- passband
- stopband
- FIR filters
- filter order
- channel selection

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

- use the wrong cutoff
- use an unrealistic transition width
- use the wrong sample rate
- change decimation unexpectedly

## Leads Into

What a filter is actually doing to the signal.

---

# Chapter 10: Impulse Response and Convolution

## Main Question

If we know how a system responds to one impulse, can we predict how it responds to any signal?

## Concepts

- system
- impulse
- impulse response
- linear time-invariant system intuition
- convolution
- FIR filtering
- input/output relationship

## Intuition We Want to Build

A complicated signal can be thought of as many shifted and scaled impulses.

If we know what the system does to one impulse, we can build its response to the entire signal.

## Mathematics

Only after building the intuition, introduce:

$$
y[n]=\sum_{k=-\infty}^{\infty}x[k]h[n-k]
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

- change the taps
- reverse the taps
- insert unexpected tap values

## Leads Into

Correlation.

---

# Chapter 11: Correlation, Matched Filtering and Signal Detection

## Main Question

How can a receiver find a known signal hidden inside another signal?

## Concepts

- similarity
- cross-correlation
- autocorrelation
- delay estimation
- detection
- correlation peak
- matched-filter intuition
- noise and detection

## Intuition We Want to Build

Correlation asks:

> How much does this part of the received signal look like the signal I am searching for?

## GNU Radio Experiment

Create a known sequence.

Delay it.

Add noise.

Try to find where the sequence occurs.

Develop matched-filter intuition and connect correlation peaks with detection.

## GNU Radio Direction

Possible tools include:

- Delay
- Conjugate
- Multiply
- Multiply Conjugate
- Moving Average
- vector processing
- correlation-related blocks

## Now Break the Flowgraph

- use the wrong reference
- increase noise
- change delay
- weaken the signal

## Leads Into

Putting information onto carriers.

---

# Part IV: Analog Communication

---

# Chapter 12: Why Modulation Exists

## Main Question

Why can't we simply transmit the original information signal directly?

## Concepts

- baseband
- passband
- carrier
- modulation
- spectrum allocation
- antenna considerations
- frequency sharing
- bandwidth

## GNU Radio Experiment

Take a low-frequency message and move it to a higher-frequency region.

Observe the spectrum before and after.

## Leads Into

Amplitude modulation.

---

# Chapter 13: Amplitude Modulation

## Main Question

How can information be carried by changing the amplitude of a carrier?

## Concepts

- carrier
- message
- AM
- modulation index
- sidebands
- carrier component
- envelope
- overmodulation
- AM demodulation

## GNU Radio Experiment

Construct AM from simple blocks first:

```text
Message
↓
Scaling
↓
Add Carrier/DC Term
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

# Chapter 14: Frequency Modulation

## Main Question

What happens if information changes the instantaneous frequency instead of amplitude?

## Concepts

- FM
- instantaneous frequency
- frequency deviation
- modulation index
- FM bandwidth
- FM demodulation
- narrowband FM
- wideband FM

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

# Chapter 15: Bits, Symbols and Digital Communication

## Main Question

How can zeros and ones eventually become a radio waveform?

## Concepts

- bits
- bit rate
- symbols
- symbol rate
- bits per symbol
- mapping
- binary data
- why symbols are useful

## Intuition We Want to Build

A transmitter does not normally send abstract zeros and ones directly.

It maps groups of bits onto physical signal states that can be transmitted.

## Mathematics

For a modulation carrying \(k\) bits per symbol:

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
- Repack Bits
- Vector Source for controlled examples

## Leads Into

Linear digital modulation.

---

# Chapter 16: Linear Modulation

## Main Question

How can digital information be represented using signal amplitudes and symbol waveforms?

## Concepts

- linear modulation
- baseband symbols
- PAM
- 2-PAM
- 4-PAM
- symbol levels
- hard decisions
- decision thresholds
- symbol energy
- noise and wrong decisions

## Intuition We Want to Build

A digital symbol can be represented by choosing one signal state from a known set.

For 2-PAM:

```text
Bit 0 → -1
Bit 1 → +1
```

The receiver then asks which valid signal state is most likely to have been transmitted.

## GNU Radio Experiment

Generate a controlled bit sequence.

Map it to PAM symbols.

Add noise and observe the received values spreading around their ideal levels.

## Now Break the Flowgraph

Increase the noise until symbols begin crossing decision boundaries.

## Leads Into

Using both I and Q to carry symbols.

---

# Chapter 17: BPSK, QPSK and QAM

## Main Question

How can I and Q carry digital information?

## Concepts

- BPSK
- QPSK
- M-PSK
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

# Chapter 18: Pulse Shaping and Matched Filtering

## Main Question

Why can't we simply transmit abrupt rectangular symbols over the air?

## Concepts

- symbol waveform
- bandwidth
- rectangular pulses
- inter-symbol interference
- pulse shaping
- Nyquist pulse-shaping idea
- raised cosine
- root-raised cosine
- samples per symbol
- matched filtering
- eye diagram

## Intuition We Want to Build

The way we shape each transmitted symbol affects both bandwidth and how easily neighbouring symbols can be distinguished.

The receiver can use a matching filter to improve detection.

## Watch Out: Two Different Nyquist Ideas

Nyquist sampling asks:

> How fast must we sample a signal to avoid aliasing?

Nyquist pulse shaping asks:

> How can pulses be shaped so that neighbouring symbols do not interfere at the correct sampling instants?

These are different problems.

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
- eye diagram

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

The wireless channel.

---

# Part VI: The Wireless Channel

---

# Chapter 19: The Wireless Channel

## Main Question

Why does the receiver never see exactly what the transmitter sent?

## Concepts

- attenuation
- AWGN
- carrier-frequency offset
- phase offset
- delay
- multipath
- reflections
- fading
- channel memory
- inter-symbol interference
- Doppler introduction
- sample-rate mismatch
- channel impulse response

## Intuition We Want to Build

The channel changes the waveform before it reaches the receiver.

A useful discipline is to separate:

```text
Channel impairment
```

from:

```text
Receiver correction
```

This chapter deliberately observes impairments without correcting them prematurely.

## GNU Radio Experiment

Start with the clean pulse-shaped QPSK link from Chapter 18.

Introduce impairments one at a time:

```text
Clean
↓
Attenuation
↓
Noise
↓
Carrier-Frequency Offset
↓
Multipath
↓
Sample-Rate Mismatch
```

Observe the resulting failure signatures.

## GNU Radio Direction

Introduce or expand:

- Multiply Const
- Noise Source
- Channel Model
- frequency offset
- Epsilon
- Delay
- Add
- manually constructed echoes
- channel taps

## Important Distinction

A distorted constellation does not automatically tell us which impairment caused it.

Use time-domain, frequency-domain, constellation, and eye observations together.

## Now Break the Flowgraph

This chapter is intentionally a controlled signal-breaking laboratory.

## Leads Into

Equalization.

---

# Chapter 20: Channel Equalization

## Main Question

If multipath creates inter-symbol interference, can the receiver compensate for the channel?

## Concepts

- multipath revisited
- channel impulse response
- channel memory
- inter-symbol interference
- equalization
- manual equalization
- adaptive equalization
- LMS intuition
- training sequence
- decision-directed operation
- acquisition
- tracking

## Intuition We Want to Build

Equalization attempts to compensate for predictable distortion caused by channel memory.

It does not correct:

- carrier-frequency offset
- carrier phase error
- timing error
- noise

Those are separate receiver problems.

## GNU Radio Experiments

Progress through:

### Manual Equalization

Use a known channel and manually chosen equalizer taps.

### Adaptive Decision-Directed Equalization

Let the equalizer adapt using detected symbols.

Explore adaptation-rate trade-offs.

### Training-Assisted Equalization

Use known symbols to help acquisition before switching to decision-directed operation.

## GNU Radio Direction

Introduce or expand:

- Linear Equalizer
- LMS decision-directed adaptation
- constellation objects
- training sequences
- tag-assisted training where useful

## Now Break the Flowgraph

- use incorrect taps
- change adaptation rate
- add more multipath
- introduce time-varying distortion
- remove training
- add noise

## Leads Into

Carrier synchronization.

---

# Part VII: Teaching the Receiver Where to Look

---

# Chapter 21: PLL and Carrier Synchronization

## Main Question

The transmitter and receiver have different oscillators. How can the receiver lock onto the transmitted carrier?

## Concepts

- oscillator mismatch
- carrier-frequency offset
- carrier phase offset
- phase detector
- feedback
- loop filter
- PLL
- lock
- acquisition
- tracking
- Costas Loop
- FLL
- frequency estimation

## Intuition We Want to Build

A synchronization loop repeatedly measures an error and uses feedback to reduce it.

For carrier synchronization, the receiver needs to estimate and correct how its local carrier differs from the received signal.

## Learning Order

Progress through:

```text
Phase Error
↓
Relative Phase Measurement
↓
PLL Intuition
↓
Frequency Error
↓
Carrier Tracking
↓
Costas Loop for QPSK
↓
Acquisition and Tracking
```

## GNU Radio Experiment

Create controlled phase and frequency errors.

Observe:

- phase difference
- constellation rotation
- frequency offset
- loop acquisition
- tracking behaviour

Compare the signal before and after correction.

## GNU Radio Direction

Introduce or expand:

- Multiply Conjugate
- PLL Carrier Tracking
- Costas Loop
- FLL Band-Edge
- loop bandwidth
- simple DFT-based frequency estimation where useful

## Now Break the Flowgraph

- increase frequency offset
- increase phase offset
- use inappropriate loop bandwidth
- set loop bandwidth near zero
- add noise
- disable carrier recovery

## What We Want the Reader to Understand

Carrier synchronization corrects carrier-related errors.

It does not correct timing error, multipath, or noise.

## Leads Into

Symbol timing.

---

# Chapter 22: Symbol Timing Synchronization

## Main Question

How does the receiver know exactly when to measure each symbol?

## Concepts

- transmitter and receiver clocks
- symbol timing
- timing offset
- sample-rate mismatch
- clock mismatch
- sampling instant
- timing error detector
- interpolation
- timing loop
- acquisition
- tracking
- Gardner timing recovery
- Mueller and Müller introduction

## Intuition We Want to Build

Even if the receiver knows the correct carrier frequency and phase, it can still make wrong decisions if it looks at the waveform at the wrong moment.

The timing loop estimates whether the receiver is sampling too early or too late and adjusts the sampling position.

## Important Distinction

A fixed timing offset and a clock-rate mismatch are not the same problem.

A fixed offset can remain constant.

A clock mismatch causes the correct sampling position to drift over time.

## Eye Diagram and Constellation

An open eye diagram and a clean constellation are not the same measurement.

The eye diagram characterizes the oversampled waveform around possible symbol-sampling instants, including timing margin and ISI.

The constellation shows the complex samples actually selected at specific sampling instants.

## GNU Radio Experiment

Introduce:

- fixed timing offsets
- early and late sampling
- sample-rate mismatch
- timing recovery

Compare before and after synchronization.

## GNU Radio Direction

Introduce or expand:

- Symbol Sync
- Gardner TED
- interpolation
- timing loop bandwidth
- Channel Model Epsilon
- eye-diagram analysis

Mention Mueller and Müller after Gardner has been understood.

## Now Break the Flowgraph

- disable Symbol Sync
- introduce timing offset
- introduce sample-rate mismatch
- use inappropriate loop bandwidth
- add noise
- combine timing and carrier errors

## Leads Into

Finding packets and frames.

---

# Chapter 23: Frame Synchronization and Packet Detection

## Main Question

Even after recovering the symbols, how does the receiver know where a meaningful message begins?

## Concepts

- frames
- packets
- preambles
- access codes
- known sequences
- correlation revisited
- packet detection
- frame synchronization
- false detection
- missed detection
- detection threshold
- tags
- frame-start indication

## Important Connection

Return to Chapter 11.

Correlation now solves a practical receiver problem:

> Where inside this stream does the known synchronization sequence occur?

## Important Distinction

Symbol synchronization asks:

> Where should I sample each symbol?

Frame synchronization asks:

> Which recovered symbol marks the beginning of the message?

These are different receiver problems.

## GNU Radio Experiment

Create:

```text
Preamble + Payload
```

Transmit it repeatedly.

Progress through:

- correct preamble
- wrong preamble
- shorter preamble
- threshold changes
- increasing noise

Observe successful detections, missed detections, and false detections.

## GNU Radio Direction

Introduce or expand:

- Correlate Access Code - Tag
- Tag Debug
- access codes
- threshold
- stream tags
- frame-start tags

Do not teach the entire tag architecture yet.

## Now Break the Flowgraph

- use the wrong preamble
- shorten the preamble
- increase noise
- make the threshold too strict
- make it too permissive

## Leads Into

Building the complete single-carrier receiver.

---

# Chapter 24: Building a Complete Single-Carrier Digital Receiver

## Main Question

What happens when all of the receiver functions developed in the previous chapters are combined into one digital communication system?

## Purpose

This chapter integrates the single-carrier receiver chain.

The aim is not merely to build a larger flowgraph.

The aim is to understand how the receiver stages work together and what happens when one stage fails.

## Conceptual Receiver

```text
Received IQ
↓
Channel Filtering
↓
Automatic Gain Control
↓
Matched Filtering
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

The exact order of some stages depends on the receiver architecture and should be discussed rather than presented as one universal sequence.

## Three Levels of Recovery

Develop the hierarchy:

```text
Signal Recovery
↓
Symbol Recovery
↓
Information Recovery
```

A receiver can succeed at one level and still fail at the next.

## Important Observation

A clean eye or constellation is not proof that the payload has been recovered.

The final test is whether the transmitted information can be reconstructed correctly.

## GNU Radio Experiments

### Experiment 1: Ideal End-to-End QPSK Link

Verify symbol and bit recovery under ideal conditions.

### Experiment 2: Carrier and Timing Recovery Together

Introduce carrier and timing impairments and recover both in the same receiver.

### Experiment 3: Multipath and Equalization

Introduce channel memory and add equalization.

### Experiment 4: Recover a Known Payload

Move beyond display-only validation and recover actual transmitted information.

### Experiment 5: Disable Receiver Stages

Disable important stages one at a time:

- matched filtering
- carrier recovery
- timing recovery
- equalization
- frame synchronization

Observe the characteristic failure of each.

## GNU Radio Direction

Bring together previously introduced tools rather than adding unnecessary new algorithms.

## What We Want the Reader to Understand

Every major receiver stage exists because it solves a different problem.

A complete receiver is a coordinated chain, not a single algorithm.

## Leads Into

Multicarrier communication.

---

# Part VIII: OFDM and Multicarrier Communication

---

# Chapter 25: Why OFDM?

## Main Question

Why transmit data on many subcarriers instead of one fast carrier?

## Concepts

- high-rate single-carrier transmission
- symbol duration
- multipath
- ISI
- multicarrier communication
- parallel data streams
- subcarriers
- spectral overlap
- orthogonality
- useful symbol duration
- subcarrier spacing
- correlation

## Intuition We Want to Build

A high-rate single-carrier system has short symbols, making multipath more difficult to handle.

Multicarrier transmission divides the high-rate stream into several slower parallel streams.

OFDM then chooses the subcarriers so that they can overlap spectrally while remaining mathematically separable.

## Orthogonality

Explain with rotating complex carriers.

Multiply one subcarrier by the conjugate of another.

The result reveals their relative rotation.

If the relative carrier completes an integer number of cycles over the useful symbol duration, the contributions cancel when averaged over that duration.

Then introduce:

$$
\Delta f=\frac{k}{T_u}
$$

where \(k\) is a nonzero integer.

## GNU Radio Experiments

### Experiment 1: Two Subcarriers

Generate two complex carriers.

### Experiment 2: Spectral Overlap

Move them closer together and observe overlapping spectra.

### Experiment 3: Demonstrating Orthogonality

Compare integer and non-integer values of \(\Delta f T_u\).

Use Multiply Conjugate and averaging/integration.

### Experiment 4: QPSK on Two Subcarriers

Modulate two orthogonal subcarriers independently.

### Experiment 5: Simple Multicarrier Receiver

Recover each subcarrier and deliberately destroy orthogonality.

## What We Want the Reader to Understand

OFDM does not work because the subcarriers are widely separated.

It works because they are orthogonal over the useful symbol duration.

## Leads Into

Generating many subcarriers efficiently.

---

# Chapter 26: Building an OFDM Signal with the IFFT

## Main Question

Do we really need hundreds of individual oscillators to generate hundreds of OFDM subcarriers?

## Concepts

- frequency-domain symbols
- subcarrier bins
- DFT revisited
- IFFT
- FFT
- OFDM symbol
- time-domain waveform
- active subcarriers
- null subcarriers
- DC subcarrier
- pilot introduction

## Important Connection

Earlier, the FFT was used to inspect a signal.

Now the IFFT is used to build a waveform from specified frequency-domain values.

## Conceptual Transmitter

```text
Bits
↓
QPSK / QAM Symbols
↓
Place Symbols into Subcarrier Bins
↓
IFFT
↓
Time-Domain OFDM Symbol
```

## Conceptual Receiver

```text
Received OFDM Symbol
↓
FFT
↓
Recover Subcarrier Bins
↓
QPSK / QAM Symbols
↓
Recovered Bits
```

## GNU Radio Experiment

Begin with only a few active bins.

Progress through:

- one active bin
- two active bins
- several active bins
- QPSK symbols placed into bins

Apply the FFT at the receiver and verify recovery.

## GNU Radio Direction

Introduce or expand:

- Stream to Vector
- Vector to Stream
- FFT block
- Forward versus Reverse FFT
- vector length
- subcarrier mapping

Avoid complete OFDM blocks until the IFFT-based structure is understood.

## Now Break the Flowgraph

- place symbols in unexpected bins
- use the wrong FFT direction
- change FFT size
- mismatch transmitter and receiver
- shift the bin mapping

## Leads Into

Multipath protection.

---

# Chapter 27: Cyclic Prefix, OFDM Channel and Basic Channel Estimation

## Main Question

How does OFDM deal with multipath?

## Concepts

- useful OFDM symbol duration
- guard interval
- cyclic prefix
- multipath delay spread
- inter-symbol interference
- circular convolution intuition
- channel frequency response
- pilot carriers
- channel estimation
- one-tap equalization
- frequency-offset sensitivity

## Intuition We Want to Build

The cyclic prefix gives delayed copies of the waveform somewhere safe to land, provided the channel delay spread is shorter than the prefix.

Copying the end of the OFDM symbol also preserves the circular structure required by FFT-based processing.

After the FFT, the channel can often be treated approximately as one complex gain per subcarrier.

## GNU Radio Experiment

Build:

```text
QPSK / QAM
↓
Subcarrier Mapping
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
Recovered Symbols
```

Compare:

- no cyclic prefix
- adequate cyclic prefix
- cyclic prefix that is too short

## Channel Estimation

Introduce known pilots and use them to estimate how the channel has changed amplitude and phase.

## Now Break the Flowgraph

- remove the cyclic prefix
- make it too short
- increase multipath delay
- remove channel correction
- introduce CFO
- use an incorrect channel estimate

## Leads Into

Understanding GNU Radio itself more deeply.

---

# Part IX: From Simulation to Real Radio

---

# Chapter 28: Understanding SDR Hardware

## Main Question

What changes when our samples come from an antenna and real SDR hardware instead of a simulated Signal Source?

## Concepts

- antenna
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
- DC offset
- centre-frequency spike
- IQ imbalance
- oscillator frequency error
- hardware limitations

## Intuition We Want to Build

The signal-processing ideas developed in simulation still apply when real hardware is connected.

What changes is that the samples now come through a physical RF front end and are affected by real hardware limitations and the real electromagnetic environment.

The reader should recognize that concepts studied earlier now have physical counterparts.

For example:

```text
Sampling
↓
Actual SDR sample rate

I and Q
↓
Actual complex samples from the receiver

Noise and SNR
↓
Real receiver noise floor

Mixing
↓
RF tuning and frequency translation

Channel impairments
↓
The real wireless environment
```

## Real Hardware Does Not Look Perfect

A real SDR spectrum may contain effects that were absent from ideal simulations.

Examples include:

- a strong component at the centre of the spectrum
- oscillator-frequency error
- IQ imbalance
- additional spurious components
- gain compression
- clipping
- external interference
- environmental noise

Some visible components may come from the receiver itself rather than from an actual transmission.

## Hardware Examples

Discuss common devices conceptually:

- RTL-SDR
- ADALM-Pluto
- HackRF
- USRP

The book should not depend completely on one device.

## GNU Radio Experiment

Connect supported SDR hardware.

Begin with observation rather than demodulation.

Display a real RF spectrum and explore:

- centre frequency
- sample rate
- RF bandwidth
- gain
- noise floor
- nearby signals

## Important Distinction

**Centre frequency** determines where the receiver is looking in the RF spectrum.

**Sample rate** determines how much digital spectrum can be represented around that centre frequency and how many samples are produced every second.

**RF bandwidth** describes the analogue front-end bandwidth and is not automatically identical to the digital sample rate.

## Now Break the Flowgraph

- use too much gain
- use too little gain
- create clipping
- choose a poor sample rate
- tune away from the desired signal
- exceed practical computer throughput

Observe the real-world consequences.

## Leads Into

Receiving and demodulating a real transmission.

---

# Chapter 29: Receiving a Real Signal with GNU Radio

## Main Question

Can we follow a real radio signal all the way from the antenna to recovered information?

## Purpose

This chapter connects the concepts developed throughout the book to a complete real-world receiver.

A broadcast FM signal provides a useful first example because the reader can inspect the signal visually and hear whether the receiver works correctly.

## Conceptual Receiver

```text
Antenna
↓
SDR Source
↓
IQ Samples
↓
Frequency Translation
↓
Channel Filtering
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
- FFT and spectrum observation
- centre frequency
- mixing
- frequency translation
- filtering
- resampling
- gain
- noise
- demodulation
- audio

## Learning Approach

Do not begin by presenting one finished receiver.

Build it progressively.

### Stage 1: Observe the RF Spectrum

Connect the SDR and find real signals.

### Stage 2: Select a Station

Tune the receiver and identify the desired broadcast FM channel.

### Stage 3: Isolate the Channel

Apply frequency translation and filtering.

### Stage 4: Adjust the Sample Rate

Use decimation or resampling so that the following stages operate at appropriate rates.

### Stage 5: Demodulate

Recover the FM information.

### Stage 6: Produce Audio

Filter and resample the recovered audio as required and send it to the Audio Sink.

## Important Teaching Principle

Do not treat a complete WBFM receiver block as a substitute for understanding the receiver chain.

At every stage ask:

> What problem is this operation solving?

and:

> What should the signal look like before and after this stage?

## GNU Radio Direction

Introduce or expand where useful:

- hardware Source blocks
- Frequency Translating FIR Filter
- QT GUI Frequency Sink
- Waterfall Sink
- runtime tuning
- gain controls
- Rational Resampler
- FM demodulation
- Audio Sink

## Now Break the Flowgraph

Misconfigure one stage at a time.

Examples:

- tune away from the station
- use the wrong channel-filter bandwidth
- use too much RF gain
- use too little RF gain
- use an inappropriate decimation factor
- use the wrong audio sample rate

Ask:

> What does this failure look like?

and, where applicable:

> What does this failure sound like?

## What We Want the Reader to Understand

The real receiver is not a completely new subject.

It is the practical combination of ideas developed throughout the book.

## Leads Into

Designing an SDR system independently.

---

# Chapter 30: Designing an SDR Receiver from Scratch

## Main Question

Can you now solve an SDR problem without following somebody else's finished flowgraph?

## Purpose

This is the capstone chapter.

The reader begins with a blank GNU Radio Companion window.

Instead of receiving a completed flowgraph, the reader receives a requirement and must decide what processing the signal needs.

The chapter should deliberately provide less step-by-step guidance than earlier chapters.

## Design Questions

The reader should ask:

1. What signal enters the system?
2. Is it real or complex?
3. What frequency range contains the desired signal?
4. What centre frequency should be used?
5. What sample rate is appropriate?
6. Is frequency translation required?
7. What filtering is required?
8. Is interpolation, decimation, or resampling required?
9. What type of demodulation is required?
10. Is carrier synchronization required?
11. Is symbol timing synchronization required?
12. Is equalization required?
13. Is frame synchronization required?
14. How should the recovered information be represented?
15. Where should intermediate signals be inspected?
16. How can the design be tested before hardware is used?
17. How can failures be isolated systematically?

## Design Philosophy

The reader should no longer begin with:

> Which GNU Radio block should I use?

They should begin with:

> What needs to happen to the signal?

Only after answering that question should they choose the GNU Radio blocks that perform those operations.

## Capstone Approach

Give the reader one or more receiver requirements rather than complete solutions.

A generic reasoning process might look like:

```text
Understand the Signal
↓
Choose the Sampling Strategy
↓
Locate the Desired Spectrum
↓
Translate if Necessary
↓
Filter
↓
Adjust the Sample Rate
↓
Demodulate / Recover Symbols
↓
Synchronize if Required
↓
Recover Information
↓
Verify the Result
```

The exact processing chain should depend on the problem.

## Testing Strategy

Encourage the reader to build progressively.

For example:

```text
Can I see the signal?
↓
Can I isolate it?
↓
Does the spectrum look correct?
↓
Is the sample rate appropriate?
↓
Can I demodulate it?
↓
Can I recover the information?
```

Intermediate observation points should be treated as engineering tools, not merely illustrations.

## Main Goal

By the end of the chapter, the reader should be able to approach an unfamiliar SDR problem systematically.

They should understand enough signal processing to design the processing chain, enough GNU Radio to implement it, and enough experimental reasoning to diagnose why it fails.

The book should end with the reader thinking about the signal first and the GNU Radio blocks second.

---

# Appendix A: GNU Radio Quick Reference

A compact reference to commonly used GNU Radio blocks and important parameters.

Organize the reference by function where useful:

- sources
- sinks
- arithmetic
- filtering
- modulation
- synchronization
- equalization
- stream/vector conversion
- tags and messages
- hardware interfaces

---

# Appendix B: GNU Radio Data Types and Data Flow

Cover:

- Byte
- Short
- Integer
- Float
- Complex
- vectors
- type conversions
- port colours
- item sizes
- streams
- Stream to Vector
- Vector to Stream
- stream tags
- tagged streams
- messages
- message ports
- PMTs
- PDUs
- metadata

## Purpose

Concepts such as vectors and tags may already have appeared naturally in the main chapters.

This appendix explains the GNU Radio data mechanisms more systematically without interrupting the main SDR learning progression.

---

# Appendix C: GNU Radio Beyond Basic Flowgraphs

Cover practical GNU Radio application-development topics that are useful but do not require separate chapters in the main learning journey.

Topics may include:

- Hierarchical Blocks
- reusable processing chains
- parameters
- Embedded Python Blocks
- generated Python
- debugging
- logging
- scheduler intuition
- buffers
- performance
- CPU limitations
- network input/output

The purpose is to help readers move from experimental flowgraphs toward larger applications without turning the main book into a GNU Radio software-development manual.

---

# Appendix D: Recording and Replaying IQ Data

Cover:

- File Source
- File Sink
- complex IQ files
- sample format
- sample rate metadata
- recording
- playback
- finite versus repeating files
- file size
- documenting centre frequency and sample rate
- using recorded IQ for reproducible experiments

## Important Idea

An IQ recording is useful only when the information required to interpret the samples is also known.

At minimum, the reader should understand the importance of recording:

- sample rate
- centre frequency
- sample format
- relevant receiver settings

---

# Appendix E: Introduction to Error Detection and Forward Error Correction

## Main Question

Why do practical communication systems deliberately add redundancy?

## Concepts

- bit errors
- error detection
- CRC concept
- redundancy
- forward error correction
- coding rate
- encoder
- decoder
- hard decisions
- soft information
- convolutional coding introduction
- LDPC introduction

## Intuition We Want to Build

A communication system can intentionally transmit additional information so that the receiver has a better chance of detecting or correcting errors.

For a code that converts \(k\) information bits into \(n\) transmitted bits, introduce:

$$
R_c=\frac{k}{n}
$$

## Conceptual Chain

```text
Information Bits
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

Compare coded and uncoded communication conceptually and experimentally where practical.

## Scope

This appendix is an introduction, not a complete coding-theory course.

The exact GNU Radio FEC block chain should be validated using the supported GNU Radio version before the experiment is finalized.

---

# Appendix F: Common GNU Radio Errors

Include both:

**Flowgraph errors**

and:

**The flowgraph runs, but the signal processing is wrong**

Examples:

- incompatible data types
- invalid parameters
- sample-rate mistakes
- missing dependencies
- Python errors
- hardware connection problems
- buffer problems
- excessive CPU load
- incorrect filter parameters
- incorrect synchronization settings
- wrong vector sizes
- tag-related mistakes

The appendix should encourage systematic debugging rather than random parameter changes.

---

# Appendix G: GNU Radio Block Index

Maintain an alphabetical index of important GNU Radio blocks used in the book.

For each block record:

- block name
- functional purpose
- chapter where it is first introduced
- later chapters where it is used in greater depth

This should remain synchronized with the separate GNU Radio block master list.

---

# Appendix H: GNU Radio Experiment Index

List every experiment and its corresponding source file.

For example:

```text
Chapter 03
    Sampling experiment
    experiments/ch03/...

Chapter 21
    Carrier synchronization experiment
    experiments/ch21/...

Chapter 25
    OFDM orthogonality experiment
    experiments/ch25/...
```

Where available, include:

- `.grc` flowgraph
- supporting `.py` script
- associated figure filenames
- a short description of what the experiment demonstrates

---

# Current Development Status

At the time of Version 0.4:

```text
Chapters 1–25     Developed
Chapter 25        Why OFDM? complete
Chapter 26        Next: Building an OFDM Signal with the IFFT
Chapter 27        Planned: Cyclic Prefix, OFDM Channel and Basic Channel Estimation
Chapters 28–30    Planned: Real hardware and capstone
Appendices        Planned / progressively maintained
```

The chapter plan should continue to evolve when experimental development shows that a different chapter order produces a clearer learning progression.

The plan is a guide to the book, not a constraint that prevents experimental results from improving its structure.