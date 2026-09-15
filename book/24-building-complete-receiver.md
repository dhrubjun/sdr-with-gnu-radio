# Chapter 24: Building a Complete Single-Carrier Digital Receiver

## Main Question

**What happens when all of the receiver functions developed in the previous chapters are combined into one complete digital communication system?**

The previous chapters developed the major receiver functions one at a time.

We learned how pulse shaping and matched filtering prepare the waveform for symbol detection, how a wireless channel introduces noise, carrier-frequency offset, sampling-clock mismatch, and multipath, how equalization reduces structured channel distortion, how carrier synchronization corrects phase and frequency errors, how symbol timing synchronization finds useful sampling instants, and how frame synchronization locates meaningful data inside a recovered stream.

Studying these functions separately made each one easier to understand.

A practical receiver, however, must make them work together on the same signal.

This chapter therefore moves from isolated receiver functions to **system integration**.

We will begin with an ideal end-to-end QPSK link, combine timing and carrier recovery, introduce multipath and equalization, recover an actual text payload, and finally remove important receiver functions deliberately so that their failure signatures become visible.

The most important lesson is that receiver success has several levels.

A waveform can look usable while the symbol decisions are wrong.

A constellation can look clean while the bit mapping is still ambiguous.

The bits can even be correct while the receiver fails to locate the frame.

The final question is therefore not merely whether an eye or constellation looks good.

It is whether the receiver recovered the intended information.

## 24.1 From Separate Receiver Functions to a Complete Receiver

A useful conceptual receiver chain is

**Received IQ → Matched Filtering → Synchronization → Equalization when required → Symbol Decisions → Bit Recovery → Frame Detection → Payload Recovery**

This is a guide rather than a universal block ordering.

Real receiver architectures depend on the modulation, synchronization algorithms, sample rate, acquisition strategy, channel conditions, and implementation.

That point becomes important in this chapter because two blocks that work correctly in isolation do not necessarily behave equally well in every ordering when they are combined.

We also avoid adding receiver stages simply because they appear in a generic textbook diagram.

Practical radios may include channel-select filters, automatic gain control, resampling, and many other functions. Those stages are important when the corresponding problems exist, but the experiments here contain only the functions needed for the impairments being studied.

## 24.2 Experiment 24.1: Establishing the Ideal End-to-End Link

Before introducing synchronization loops or channel impairments, we need a reference system.

If the baseline does not work, any later failure becomes ambiguous.

The first experiment uses QPSK with root-raised-cosine pulse shaping and matched filtering.

| Parameter | Value |
|---|---:|
| Sample rate | `32 kHz` |
| Symbol rate | `1 ksymbol/s` |
| Samples per symbol | `32` |
| RRC roll-off factor | `0.35` |
| Filter span | `8` symbols |
| Number of RRC taps | `257` |

Two random binary sources generate the I and Q data.

Each bit is mapped to either `-1` or `+1`, the two branches are combined into a complex QPSK stream, and the transmitter RRC filter interpolates by 32.

The receiver uses the matching RRC filter.

For this ideal reference case, `Keep 1 in N` selects one sample from every 32 matched-filter output samples.

![Ideal end-to-end QPSK flowgraph](../figures/ch24/ch24_exp01_ideal_end_to_end_flowgraph.png)

Random data are useful here because a short repeating pattern contains only a limited set of transitions and can produce an incomplete-looking eye diagram.

A long random sequence exercises many more symbol transitions.

### What We Observe

![Ideal eye diagrams and QPSK constellation](../figures/ch24/ch24_exp01_ideal_eye_constellation.png)

With no noise, carrier offset, timing mismatch, or multipath, the I and Q eye diagrams are open and the selected complex samples form four tight QPSK clusters.

This establishes the reference against which the later receiver experiments can be judged.

### Eye Diagram and Constellation Are Not the Same Measurement

This distinction is essential throughout the chapter.

The **eye diagram** overlays portions of the oversampled waveform. It tells us about timing margin, pulse shape, transitions, and ISI around possible sampling instants.

The **constellation** shows the complex samples actually presented at selected symbol instants. It reveals effects such as carrier phase or frequency error, noise, residual ISI, and incorrect sampling.

An open eye does not guarantee a clean constellation.

For example, carrier-frequency error can rotate the I/Q samples continuously while the waveform still contains useful timing information.

Conversely, four recognizable constellation clusters do not prove that the original bits or frame have been recovered correctly.

The location of each diagnostic sink in the receiver chain therefore matters as much as the appearance of its plot.

## 24.3 Experiment 24.2: Integrating Timing and Carrier Recovery

Carrier synchronization and timing synchronization were studied separately in Chapters 21 and 22.

We now combine them in one receiver.

The signal parameters are changed to

| Parameter | Value |
|---|---:|
| Sample rate | `32 kHz` |
| Symbol rate | `4 ksymbol/s` |
| Samples per symbol | `8` |
| RRC roll-off factor | `0.35` |
| Filter span | `8` symbols |
| Number of RRC taps | `65` |

A GNU Radio Channel Model is placed between transmitter and receiver so that carrier-frequency offset, sample-rate mismatch, and additive noise can be introduced independently.

### Channel-Model Frequency Offset

The Channel Model represents frequency offset as a fraction of the sample rate.

If the physical carrier-frequency offset is $\Delta f$ and the sample rate is $F_s$,

$$
f_{\text{norm}}=\frac{\Delta f}{F_s}
$$

For a 200 Hz offset at 32 kHz,

$$
f_{\text{norm}}=\frac{200}{32000}=0.00625
$$

so

```text
Frequency Offset: 0.00625
```

represents a 200 Hz CFO in this experiment.

For the Channel Model,

```text
Epsilon: 1.0
```

represents no sample-rate mismatch.

Values slightly different from one create a persistent relative clock error.

### Integrating Symbol Sync and the Costas Loop

Symbol Sync uses

```text
Timing Error Detector: Gardner
Samples per Symbol: 8
Expected TED Gain: 1
Loop Bandwidth: 0.045
Damping Factor: 1
Maximum Deviation: 1.5
Output Samples/Symbol: 1
Interpolating Resampler: MMSE, 8-tap FIR
```

The Costas Loop uses

```text
Loop Bandwidth: 0.0314159
Order: 4
Use SNR: No
```

During development, the first attempted ordering was

**Matched Filter → Costas Loop → Symbol Sync**

In this implementation, that combination produced a ring-like constellation even with an ideal channel.

Testing the stages individually showed that both blocks could work, but the integrated ordering

**Matched Filter → Symbol Sync → Costas Loop**

produced a stable QPSK constellation.

This does not establish a universal rule that timing recovery must always precede carrier recovery.

It demonstrates something more useful:

> **Receiver blocks that work correctly in isolation can interact when integrated. Their combined behaviour must be tested.**

The final integrated flowgraph is shown below.

![Integrated timing and carrier recovery flowgraph](../figures/ch24/ch24_exp02_integrated_receiver_flowgraph.png)

The Eye Sink is connected after the matched filter but before Symbol Sync and the Costas Loop.

The Constellation Sink is connected after both synchronization stages.

That placement is deliberate.

### Ideal Integrated Receiver

We first use

```text
Noise Voltage: 0
Frequency Offset: 0
Epsilon: 1.0
Taps: 1
```

![Ideal integrated receiver result](../figures/ch24/ch24_exp02_ideal_integrated_receiver.png)

The pre-synchronization eye is open and the final constellation contains four compact QPSK clusters.

The two synchronization blocks therefore operate correctly together under ideal conditions.

### Sample-Rate Mismatch

We next change only `Epsilon`:

```text
Frequency Offset: 0
Epsilon: 1.001
Noise Voltage: 0
Taps: 1
```

![Timing mismatch with timing recovery enabled](../figures/ch24/ch24_exp02_timing_mismatch.png)

The Eye Sink is located before Symbol Sync, so it shows the incoming timing drift.

The final constellation remains well organized because Symbol Sync continuously tracks the changing sampling phase.

A fixed timing offset and a sample-rate mismatch are different problems.

A fixed offset can be corrected once.

A sample-rate mismatch accumulates, so the timing loop must keep tracking it.

### Carrier-Frequency Offset

We now restore

```text
Epsilon: 1.0
```

and use

```text
Frequency Offset: 0.00625
```

which corresponds to 200 Hz.

![Carrier-frequency offset with synchronization enabled](../figures/ch24/ch24_exp02_cfo_only.png)

The I and Q eye diagrams look much worse, even though the final constellation still forms four recognizable QPSK regions.

The reason is that the Eye Sink is before carrier recovery.

A carrier-frequency offset rotates the complex baseband waveform:

$$
r(t)=s(t)e^{j2\pi\Delta f t}
$$

If

$$
s(t)=I(t)+jQ(t)
$$

then the rotation mixes the two fixed I and Q axes:

$$
I'(t)=I(t)\cos(2\pi\Delta f t)-Q(t)\sin(2\pi\Delta f t)
$$

$$
Q'(t)=I(t)\sin(2\pi\Delta f t)+Q(t)\cos(2\pi\Delta f t)
$$

The pre-carrier-recovery Eye Sink therefore overlays many different projections of the rotating complex signal.

A smeared I/Q eye in this case does **not** mean that timing recovery has necessarily failed.

The Costas Loop removes the rotation later in the chain.

### CFO and Timing Mismatch Together

We next combine

```text
Frequency Offset: 0.00625
Epsilon: 1.001
Noise Voltage: 0
Taps: 1
```

![Combined CFO and timing mismatch](../figures/ch24/ch24_exp02_cfo_timing_mismatch.png)

The pre-synchronization eyes remain heavily smeared, while the final constellation retains four separated regions.

In this particular experiment, the eye appearance is dominated by the carrier rotation while Symbol Sync continues to track the relatively small sample-rate mismatch.

This is why receiver diagnostics must always be interpreted according to both the impairment and the measurement location.

### Adding Noise

We now isolate additive noise.

For

```text
Noise Voltage: 0.5
Frequency Offset: 0
Epsilon: 1.0
Taps: 1
```

we obtain

![Moderate additive noise](../figures/ch24/ch24_exp02_moderate_noise.png)

The eye remains recognizable but the traces become thicker.

The constellation still has four clusters, although each point has become a cloud.

Increasing the noise to

```text
Noise Voltage: 1.0
```

gives

![Strong additive noise](../figures/ch24/ch24_exp02_strong_noise.png)

The eye becomes fuzzier and the constellation clouds spread farther from their ideal locations.

This behaviour is different from deterministic synchronization errors.

Carrier-frequency offset can be estimated and tracked.

Sampling-clock mismatch can also be tracked.

Random noise cannot simply be removed by a synchronization loop.

As the noise becomes strong enough, samples cross decision boundaries and symbol errors appear.

## 24.4 Experiment 24.3: Adding Multipath and Equalization

Carrier offset, timing mismatch, and noise do not damage the signal in the same way.

Multipath introduces another effect: **channel memory**.

A delayed copy of one symbol can contribute to later symbol observations and produce ISI.

### Constructing the Multipath Channel

We create a simple two-path channel manually.

One branch is the direct signal.

The second branch is delayed by 8 samples and multiplied by 0.5 before the two paths are added.

At 8 samples per symbol, the delay is exactly one symbol period.

The channel therefore contains one direct path and one delayed path arriving one symbol later at half the amplitude.

This controlled construction keeps the physical meaning visible.

### Receiver Without Equalization

The first version uses matched filtering, timing recovery, and carrier recovery but no equalizer.

![Multipath receiver before equalization](../figures/ch24/ch24_exp03a_multipath_before_equalization_flowgraph.png)

The received constellation shows structured trajectories and multiple locations rather than a purely random cloud.

That difference matters.

Additive noise creates random spreading.

Multipath creates structured distortion because the current received symbol depends on neighbouring transmitted symbols.

### Adding the Adaptive Equalizer

We now add the adaptive equalizer developed in Chapter 20.

The important settings are

```text
Linear Equalizer
Num Taps: 5
Input Samples per Symbol: 1

Adaptive Algorithm LMS
Step Size: 0.005
```

The decision-directed QPSK reference is

```text
[1+1j, -1+1j, -1-1j, 1-1j]
```

This scale matters.

The decision reference must match the transmitted symbol locations. A normalized reference near `±0.707 ± j0.707` would not match a transmitter using `±1 ± j`.

The equalized flowgraph is

![Multipath receiver with adaptive equalization](../figures/ch24/ch24_exp03b_multipath_after_equalization_flowgraph.png)

The experimentally stable ordering is

**Matched Filter → Symbol Sync → Costas Loop → Linear Equalizer**

Again, this is the architecture that worked for this implementation rather than a universal ordering rule.

### Before and After Equalization

![Multipath before and after equalization](../figures/ch24/ch24_exp03_multipath_before_after_equalization.png)

Before equalization, the constellation shows strong structured ISI.

After equalization, the four QPSK regions become much tighter.

The Eye Sink remains upstream of the equalizer.

It therefore does not suddenly become clean simply because the final constellation improves.

A downstream correction cannot change a measurement taken earlier in the receiver chain.

## 24.5 Experiment 24.4: Recovering an Actual Message

Until now, much of our definition of success has been visual.

A clean eye is useful.

A clean constellation is useful.

But the purpose of a communication receiver is to recover information.

We therefore replace the random source with a known frame and follow the receiver all the way to a text payload.

### Building the Frame

The frame contains 40 bits:

- 16-bit preamble;
- 24-bit payload.

The preamble is

```text
1101001110010110
```

The payload is the ASCII text

```text
SDR
```

with

```text
S = 01010011
D = 01000100
R = 01010010
```

The complete frame is

```text
1101001110010110 | 01010011 01000100 01010010
      preamble   |    S        D        R
```

or

```text
1101001110010110010100110100010001010010
```

The 40 bits correspond to 20 QPSK symbols.

A repeating Vector Source supplies

```text
[1,1,0,1,0,0,1,1,1,0,0,1,0,1,1,0,
 0,1,0,1,0,0,1,1,
 0,1,0,0,0,1,0,0,
 0,1,0,1,0,0,1,0]
```

The transmitter Repack Bits block uses

```text
Bits per input byte: 1
Bits per output byte: 2
Endianness: LSB
```

For an input pair $(b_0,b_1)$,

$$
k=b_0+2b_1
$$

so the packing is

| Input bits | Packed index |
|---|---:|
| `00` | 0 |
| `01` | 2 |
| `10` | 1 |
| `11` | 3 |

The QPSK table is

```text
[1+1j, -1+1j, -1-1j, 1-1j]
```

### The Complete Receiver

![Complete single-carrier receiver](../figures/ch24/ch24_exp04_complete_single_carrier_receiver_flowgraph.png)

The receiver now performs

**Matched Filtering → Timing Recovery → Carrier Recovery → QPSK Decisions → Differential Decoding → Bit Recovery → Frame Detection → Payload Recovery**

The receiver Repack Bits block reverses the earlier packing:

```text
Bits per input byte: 2
Bits per output byte: 1
Endianness: LSB
```

Frame detection uses

```text
Access Code: 1101001110010110
Threshold: 0
Tag Name: frame_start
```

With the ideal channel, repeated `frame_start` tags appear 40 bits apart, matching the transmitted frame length.

### Differential Coding and QPSK Phase Ambiguity

When the complete receiver was tested with carrier-frequency offset, an important issue appeared.

The Costas Loop could remove the continuous rotation caused by CFO while still leaving a constant QPSK phase ambiguity.

QPSK is geometrically unchanged by rotations of 90°.

The Costas Loop can therefore lock to more than one equivalent quadrant orientation.

The constellation may look perfectly clean while the absolute symbol labels are different.

This means:

> **A clean QPSK constellation does not necessarily imply that the original bits are correct.**

To make the information insensitive to this constant quadrant ambiguity, we use GNU Radio's Differential Encoder and Differential Decoder with

```text
Coding: Differential
Modulus: 4
```

Differential coding represents information through changes between successive symbol states rather than relying only on absolute QPSK orientation.

A constant 90° ambiguity changes the absolute labels but preserves the relative state changes.

Differential coding does not replace carrier recovery.

If the carrier continues rotating because CFO has not been corrected, stable symbol decisions are still lost.

### Ideal Information Recovery

We first use

```text
Noise Voltage: 0
Frequency Offset: 0
Epsilon: 1.0
Taps: 1
```

![Ideal complete-receiver eye diagrams and constellation](../figures/ch24/ch24_exp04_ideal_eye_constellation.png)

The short repeating 40-bit frame produces fewer distinct eye trajectories than the random sequence in Experiment 24.1.

That is expected because the deterministic frame contains fewer transition combinations.

The constellation still contains four tight QPSK clusters.

More importantly, the receiver recovers the information itself.

![Ideal payload recovery](../figures/ch24/ch24_exp04_ideal_payload_recovery.png)

The recovered payload bits are

```text
010100110100010001010010
```

which decode to

```text
SDR
```

This is the first direct information-level proof that the complete receiver is working.

### Payload Recovery with Carrier-Frequency Offset

We now introduce the same 200 Hz CFO:

```text
Frequency Offset: 0.00625
```

![Payload recovery with carrier-frequency offset](../figures/ch24/ch24_exp04_cfo_payload_recovery.png)

With differential encoding and decoding enabled, the receiver can recover the payload even if the Costas Loop settles with a constant QPSK quadrant ambiguity.

In one retained run, the first detected payload contained one incorrect bit while the following frames repeatedly recovered `SDR`.

The important interpretation is acquisition.

Timing and carrier loops need an initial interval in which their internal estimates converge.

After acquisition, the receiver enters tracking and repeatedly recovers the correct frame.

The specific first-frame error should not be treated as a universal property of every run.

### Multiple Impairments Together

We next combine

```text
Frequency Offset: 0.00625
Epsilon: 1.01
Noise Voltage: 0.5
Taps: 1
```

This corresponds to 200 Hz CFO, a 1% sample-rate mismatch, and moderate additive noise.

The complete receiver continues to recover `SDR` repeatedly.

This is an important integration result because carrier recovery, timing recovery, differential decoding, bit recovery, frame detection, and payload extraction are now operating together on the same impaired waveform.

### When Noise Becomes Too Strong

We keep the CFO and timing mismatch unchanged and compare two noise levels.

![Payload recovery at noise voltages 0.5 and 1.0](../figures/ch24/ch24_exp04_payload_recovery_noise_0p5_vs_1p0.png)

At

```text
Noise Voltage: 0.5
```

all five observed payloads were recovered as `SDR`.

At

```text
Noise Voltage: 1.0
```

several observed payloads contained incorrect characters, although some complete `SDR` frames were still recovered.

This is the information-level consequence of the constellation spreading seen earlier.

Synchronization can compensate for structured impairments within its operating range.

It cannot remove arbitrary random noise.

Once enough samples cross symbol-decision boundaries, bit errors enter the frame and the payload becomes corrupted.

The value `1.0` is not a universal receiver threshold. It is the observed result for this signal scaling and configuration.

### Payload Decoder

A small Embedded Python Block performs only the final application-level payload interpretation.

The reference implementation is

```text
experiments/ch24/ch24_exp04_payload_decoder.py
```

It watches for the `frame_start` tag, collects the following 24 payload bits, groups them into three 8-bit bytes, converts them to ASCII, and prints the recovered text.

The script does **not** perform carrier recovery, timing recovery, symbol decisions, differential decoding, or frame detection.

Those functions have already been completed by the GNU Radio DSP chain.

This keeps the architectural boundary clear: GNU Radio recovers and synchronizes the communication stream, while the small script interprets the already recovered payload.

## 24.6 Experiment 24.5: Diagnosing Receiver Failures

We now have a receiver that is known to recover the intended information.

That makes deliberate failure especially useful.

Instead of adding another algorithm, we remove important receiver functions one at a time and observe what breaks.

### Removing Carrier Recovery

The channel contains

```text
Noise Voltage: 0
Frequency Offset: 0.00625
Epsilon: 1.0
Taps: 1
```

Timing recovery remains enabled, but the Costas Loop is bypassed.

![Receiver failure without carrier recovery](../figures/ch24/ch24_exp05_no_carrier_recovery.png)

The constellation forms a ring-like pattern rather than four stationary QPSK clusters.

The uncompensated 200 Hz CFO makes the carrier phase rotate continuously.

Stable symbol decisions are therefore lost, frame detection fails, and no payload is recovered.

This also clarifies the role of differential coding.

Differential coding handles a **constant quadrant ambiguity after carrier recovery**.

It does not replace the Costas Loop when the phase itself is continuously rotating.

### Removing Timing Recovery

Carrier recovery is restored and Symbol Sync is removed.

The channel is

```text
Noise Voltage: 0
Frequency Offset: 0
Epsilon: 1.01
Taps: 1
```

A fixed `Keep 1 in N` sampler with

```text
N: 8
```

replaces Symbol Sync.

![Receiver failure without timing recovery](../figures/ch24/ch24_exp05_no_timing_recovery.png)

The fixed sampler has no mechanism for following the timing drift created by the 1% sample-rate mismatch.

Its selected sample positions progressively move away from the symbol centres.

The constellation develops structured trajectories through the decision regions and reliable information recovery is lost.

This failure looks different from the no-carrier-recovery ring because the physical error is different.

### Breaking Frame Synchronization

Finally, we restore a working waveform and symbol receiver but replace the correct access code with an incorrect pattern.

The eye can still be open.

The constellation can still contain four clean clusters.

The bit stream can still be recovered.

But the frame synchronizer never finds the expected preamble, so no `frame_start` tag is generated and the Payload Decoder produces no output.

This failure is conceptually different from the earlier two.

The physical signal has been recovered correctly, but the receiver cannot identify where the meaningful information begins.

That gives us another central lesson:

> **Correct waveform recovery and correct symbol recovery are not sufficient if the receiver cannot locate the frame.**

## 24.7 Reading Receiver Diagnostics Correctly

Different failures produce different signatures.

These signatures are useful clues, but they are not universal rules unless the measurement location and surrounding receiver state are also known.

| Impairment or failure | Eye-diagram signature | Constellation signature | Information-level consequence |
|---|---|---|---|
| Additive noise | traces become thicker and fuzzier | clusters spread randomly | symbol and bit errors increase |
| Multipath | eye opening degrades because of ISI | structured spreading or multiple trajectories | errors increase unless the channel is equalized |
| CFO without carrier recovery | pre-recovery I/Q eye can be heavily smeared | rotating or ring-like constellation | stable decisions, frame detection, and payload recovery fail |
| Sample-rate mismatch without timing recovery | sampling position drifts through the eye | structured trajectories between symbol locations | symbol decisions become unreliable |
| QPSK phase ambiguity | eye may remain usable | four clean clusters can still have the wrong absolute orientation | bit labels can be wrong unless the ambiguity is handled |
| Frame-synchronization failure | eye can remain open | constellation can remain clean | correct symbols or bits may exist, but the payload cannot be located |

Two principles are worth keeping.

First:

> **Never interpret an eye diagram or constellation without knowing where in the receiver chain it was measured.**

An eye before carrier recovery can look badly smeared because the I and Q axes are rotating.

An eye before equalization cannot show an improvement produced later by the equalizer.

Second:

> **A clean constellation demonstrates symbol-domain recovery, not necessarily information recovery.**

The QPSK ambiguity experiment shows that a geometrically correct constellation can still correspond to the wrong absolute symbol labels.

Frame-synchronization failure goes one level further: even correct bits are not enough if the receiver cannot locate the payload.

## 24.8 The Receiver as a Hierarchy

The complete system can be understood at three levels.

### Signal Recovery

The receiver first creates a usable signal representation.

Matched filtering improves the waveform for detection.

Timing synchronization finds useful sampling instants.

Carrier synchronization creates a stable complex reference.

Equalization compensates for channel memory when multipath creates ISI.

### Symbol Recovery

The receiver then decides which constellation symbol was transmitted.

For QPSK, each observation is assigned to one of four symbol states.

A clean constellation is strong evidence that this level is working.

### Information Recovery

Finally, the symbol decisions must be converted back into the transmitted information.

Differential decoding resolves the relative QPSK state changes.

Repack Bits reconstructs the bit stream.

Frame synchronization locates the preamble.

The payload is extracted and interpreted.

Only at this level can we say that the communication system has accomplished its actual purpose.

In Experiment 24.4, the final proof is simply

```text
Recovered payload: SDR
```

## 24.9 GNU Radio Toolbox

Several familiar GNU Radio blocks take on system-level roles in the complete receiver.

| GNU Radio Block | Role in This Chapter |
|---|---|
| RRC Filters | pulse shaping and matched filtering |
| Channel Model | controlled noise, CFO, and sample-rate mismatch |
| Symbol Sync | timing acquisition and tracking |
| Costas Loop | QPSK carrier recovery |
| Linear Equalizer | adaptive compensation for multipath-induced channel memory |
| Repack Bits | conversion between bit items and QPSK symbol indices |
| Differential Encoder / Decoder | protection against constant QPSK quadrant ambiguity |
| Correlate Access Code - Tag | frame-boundary detection |
| Embedded Python Block | extraction and interpretation of the recovered payload |
| Keep 1 in N | fixed sampler used for the no-timing-recovery failure test |

### Repack Bits

At the transmitter,

```text
Bits per input byte: 1
Bits per output byte: 2
Endianness: LSB
```

groups pairs of bits into QPSK symbol indices.

At the receiver, the inverse configuration reconstructs individual bits.

### Differential Encoder and Decoder

Both use

```text
Coding: Differential
Modulus: 4
```

because QPSK has four symbol states.

They address a constant quadrant ambiguity after carrier recovery.

They do not correct a continuously rotating carrier.

### Correlate Access Code - Tag

The block searches the recovered bit stream for

```text
1101001110010110
```

with zero tolerated bit mismatches in the retained experiment.

A successful match creates the `frame_start` tag used by the payload decoder.

## 24.10 Explore Further

The complete receiver supports several useful diagnostic experiments.

1. Increase `Epsilon` from `1.001` toward `1.01` while keeping CFO and noise at zero. Compare the pre-Symbol-Sync eye with the final constellation.

2. Keep timing recovery enabled and gradually increase CFO. Observe the pre-carrier-recovery eye and the post-Costas constellation together.

3. Add moderate noise while keeping CFO and timing mismatch active. Compare symbol-level appearance with actual payload recovery.

4. In the multipath experiment, remove the Linear Equalizer while keeping the echo unchanged. Compare the structured constellation distortion with the equalized result.

5. Change the equalizer decision constellation to the normalized `±0.707 ± j0.707` points while leaving the transmitted QPSK at `±1 ± j`. Observe why reference scaling matters.

6. Disable differential coding while keeping carrier recovery enabled and repeat the CFO payload experiment. Check whether a clean constellation always produces the correct bit mapping.

7. Bypass the Costas Loop while leaving differential coding enabled. Confirm that differential coding does not repair continuous carrier rotation.

8. Replace the correct frame access code with a one-bit-different pattern while keeping the tolerated mismatch count at zero. Confirm that clean symbol recovery can coexist with complete payload failure.

9. Move a diagnostic sink to a different point in the receiver chain and compare how the same impairment appears before and after the corresponding correction stage.

## 24.11 Practical Lessons from the Complete Receiver

Several lessons become much clearer only after the receiver functions are integrated.

Receiver stages interact.

A block cannot be assumed to behave identically when its input sample rate, waveform, or preceding processing changes.

Receiver ordering matters, but the correct ordering depends on the algorithms and signal conditions rather than on one universal diagram.

Acquisition and tracking are different operating phases.

A receiver can make transient errors while its synchronization loops converge and then operate reliably after lock.

Different impairments create different signatures because they arise from different physical mechanisms.

Noise causes random spreading.

Multipath creates structured channel memory.

Uncompensated CFO creates continuous phase rotation.

Sampling-clock mismatch causes the preferred sampling phase to drift.

Each receiver correction addresses a particular problem.

Equalization does not remove CFO.

Carrier recovery does not remove random noise.

Differential decoding does not replace carrier recovery.

Frame synchronization does not improve the waveform or constellation.

Intermediate plots are diagnostic tools.

They are not the final definition of communication success.

The final question is:

> **Did the receiver recover the intended information?**

## 24.12 What We Learned

This chapter combined the major receiver functions developed throughout the preceding chapters into progressively more complete single-carrier communication systems.

The ideal QPSK experiment established a clean reference and reinforced the distinction between an eye diagram and a constellation.

The eye describes the oversampled waveform, timing margin, pulse shape, and ISI around possible sample positions.

The constellation describes the complex samples actually selected for symbol decisions and reveals symbol-domain effects such as carrier rotation, noise, timing error, and residual distortion.

Integrating Symbol Sync and the Costas Loop showed that receiver blocks can interact when combined. The ordering that worked for this implementation had to be established experimentally.

Controlled channel tests then showed the different effects of timing mismatch, carrier-frequency offset, and additive noise.

A 200 Hz CFO could make the pre-carrier-recovery I/Q eyes look badly smeared while the downstream Costas Loop still recovered four QPSK regions.

Multipath created structured ISI rather than random spreading, and the adaptive equalizer tightened the recovered constellation.

The known-frame experiment moved the definition of success beyond plots.

A Costas Loop could recover a clean QPSK geometry while leaving a constant 90° phase ambiguity. Differential encoding and decoding made the information insensitive to that constant quadrant ambiguity.

The complete receiver then recovered the text `SDR` under carrier-frequency offset, sample-rate mismatch, and moderate noise simultaneously.

Increasing the noise eventually produced actual payload corruption.

The deliberate failure experiments completed the diagnostic picture.

Without carrier recovery, CFO left the constellation rotating and no payload was recovered.

Without timing recovery, sample-rate mismatch caused the fixed sampling phase to drift through the waveform and symbol decisions failed.

With an incorrect frame access code, waveform and symbol recovery could still succeed while payload recovery produced nothing.

The complete receiver is therefore best understood as a hierarchy:

**Signal Recovery → Symbol Recovery → Information Recovery**

Successful digital communication requires all three.

## 24.13 Connecting to the Next Chapter

We have now built a complete single-carrier digital receiver.

It can recover timing, correct carrier error, compensate for channel distortion, make symbol decisions, reconstruct bits, locate frames, and recover an actual payload.

But the multipath experiment points to a deeper limitation.

Multipath creates delayed copies of the transmitted waveform.

When the symbol period is long compared with the channel delay spread, the resulting overlap may be manageable.

As the symbol rate increases, the symbol period becomes shorter.

The same physical path delay then occupies a larger fraction of one symbol interval, and the equalizer has to work harder to undo the resulting frequency-selective distortion.

This suggests a different approach:

> **Instead of transmitting one high-rate symbol stream through a difficult multipath channel, what if we divided the information among many slower parallel streams?**

That idea leads to multicarrier communication and, in particular, OFDM.

The next chapter asks why this approach is useful and how closely spaced subcarriers can overlap in frequency without necessarily interfering.

That leads to **Chapter 25: Why OFDM?**