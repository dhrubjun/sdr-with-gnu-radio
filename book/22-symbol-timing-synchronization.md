# Chapter 22: Symbol Timing Synchronization

## Main Question

**How can a receiver determine the correct instant at which to measure each symbol?**

Chapter 21 recovered the carrier reference. A PLL, Costas Loop, FLL, or another carrier-recovery method can correct carrier phase and frequency errors, but that still does not tell the receiver **when to sample each symbol**.

That is the problem of **symbol timing synchronization**.

A digital receiver does not receive one isolated number for each transmitted symbol. It receives a sampled waveform. After pulse shaping and matched filtering, several digital samples may represent one symbol interval. Somewhere within those samples is the best instant for making the symbol decision.

If the receiver samples at the wrong instant, the constellation can spread even when the carrier is perfectly synchronized. If the transmitter and receiver sampling clocks run at slightly different rates, the correct instant does not remain fixed. It drifts with time.

This chapter develops the timing-recovery problem experimentally.

We will first deliberately sample QPSK at different positions inside a symbol interval. Then we will build a simple timing-error detector to develop early-versus-late intuition. After that, GNU Radio's **Symbol Sync** block will close the timing loop automatically. Finally, we will introduce sampling-clock mismatch and observe the receiver tracking a timing position that moves continuously.

The central distinction is:

> **Carrier synchronization determines the correct constellation rotation. Timing synchronization determines the correct instant at which that constellation should be observed.**

## 22.1 From Pulse Shaping to Timing Recovery

Chapter 18 introduced pulse shaping and matched filtering.

A Nyquist pulse can be designed so that, at the correct symbol instants, neighbouring symbols do not interfere with the symbol being measured.

If the symbol period is $T$, the desired receiver samples occur at times such as

$$
t=kT+\tau
$$

where $k$ is the symbol index and $\tau$ represents the receiver's timing phase.

The important phrase is **at the correct symbol instants**.

The matched filter does not determine those instants automatically. It produces an oversampled waveform, and the receiver must decide where inside each symbol interval to measure the signal.

For the experiments in this chapter,

$$
f_s=32000\text{ samples/s}
$$

and

$$
R_s=4000\text{ symbols/s}
$$

so

$$
sps=\frac{f_s}{R_s}=8
$$

There are therefore eight digital samples per symbol.

A fixed sampler can choose one of those existing sample positions, but it does not know by itself which one is best.

This is not a carrier problem. A receiver can have correct carrier phase and frequency and still make poor symbol decisions because its timing is wrong.

## 22.2 Experiment 22.1: Effect of Symbol Timing Offset

Before trying to recover timing, we first observe what incorrect timing does.

We generate pulse-shaped QPSK, pass it through a receive matched filter, and deliberately choose different samples from each eight-sample symbol interval.

The main parameters are

| Parameter | Value |
|---|---:|
| Sample rate | `32 kS/s` |
| Symbol rate | `4 ksymbol/s` |
| Samples per symbol | `8` |
| RRC roll-off, $\alpha$ | `0.35` |
| RRC taps | `65` |
| Timing-offset range | `0` to `7` samples |

![Flowgraph for deliberately changing the QPSK symbol-sampling position](../figures/ch22/ch22-exp1-symbol-timing-offset-flowgraph.png)

The transmitted symbols and pulse shape are unchanged. Only the sampling position changes.

The eight integer offsets span one complete symbol interval. After eight samples, the same relative position repeats in the next symbol interval.

### What We Observe

We retain offsets 0, 2, 4, and 6 for the comparison.

![Effect of different symbol-timing offsets on the QPSK constellation](../figures/ch22/ch22-exp1-symbol-timing-offset-comparison.png)

At a favourable sampling position, the constellation forms four compact QPSK clusters.

At poor positions, the receiver samples while the pulse-shaped waveform is moving between symbol values. The selected complex samples then spread through the space between the ideal constellation points.

This gives an important diagnostic lesson:

> **A smeared constellation does not automatically imply noise, multipath, or failed carrier recovery. Incorrect symbol timing can produce a similar visual symptom.**

### Physical Meaning

Each pulse-shaped symbol has a region where its value is best observed.

Sampling near that region gives a reliable estimate. Sampling closer to a transition increases the influence of neighbouring symbols and makes the selected sample more sensitive to timing error and ISI.

A fixed `Keep 1 in N` sampler can choose one existing sample position, but it cannot determine whether that position is too early or too late.

The receiver therefore needs a timing-error measurement.

## 22.3 How Can a Receiver Know It Is Early or Late?

Suppose the receiver is examining a candidate symbol time.

A useful timing detector can compare waveform behaviour slightly before and slightly after that candidate position.

These measurements are commonly described as **early**, **on-time**, and **late** observations.

If the timing is correctly centred, the early and late observations satisfy the balance expected by the detector.

If that balance is disturbed, the detector produces a **timing error**.

The sign of the error tells the timing loop which direction the sampling position should move.

This is analogous to carrier recovery.

A carrier loop needs a phase- or frequency-error detector before it can correct the carrier reference. A timing loop needs a timing-error detector before it can correct the sampling instant.

## 22.4 Experiment 22.2: Timing-Error Detection

To expose the idea directly, we build a simple Early-Late-style timing-error detector rather than beginning with Symbol Sync.

A controlled alternating sequence is useful because it produces regular transitions:

```text
+1, -1, +1, -1, +1, -1, ...
```

After interpolation and matched filtering, two nearby branches provide early and late observations. Their energies are compared and averaged.

![Flowgraph for the Early-Late timing-error detector](../figures/ch22/ch22_exp2_early_late_ted_flowgraph.png)

The assumed timing offset is swept over a small neighbourhood:

```text
Timing Offset
Start: -3
Stop: 3
Step: 1
```

This range serves a different purpose from the 0-to-7 sweep in Experiment 22.1.

Experiment 22.1 explored an entire symbol interval. Here we are asking a local question around a candidate operating point: is the receiver early or late?

### Why Compare Squared Values?

A simple energy-style Early-Late error can be written conceptually as

$$
e[k]=|r_E[k]|^2-|r_L[k]|^2
$$

where $r_E[k]$ and $r_L[k]$ are the early and late observations.

The sign convention can be reversed depending on the detector construction. What matters is that opposite timing directions produce opposite error signs.

Squaring also removes symbol polarity.

For real-valued samples,

$$
(+a)^2=(-a)^2=a^2
$$

so an alternating positive and negative data sequence does not cause the detector to confuse data sign with timing direction.

### Squaring and Timing Information

There is a broader reason nonlinear operations such as squaring appear in timing-recovery theory.

The transmitted data may look random, so the symbol clock is not necessarily visible as an obvious sinusoid. Pulse shaping still creates statistical structure that repeats at the symbol rate.

A nonlinear operation can reveal some of that periodic timing structure.

In this experiment, squaring has a direct purpose: it allows early and late **energy** to be compared without dependence on symbol polarity.

Other timing-error detectors, including Gardner and Mueller and Müller, obtain timing information differently and do not require this exact squaring operation.

### What We Observe

The retained comparison uses offsets $-2$, $-1$, $0$, and $+1$.

![Timing-error detector response for selected assumed timing offsets](../figures/ch22/ch22_exp2_timing_error_detector_comparison.png)

The experimental detector produced approximately

| Assumed offset | Average timing error |
|---:|---:|
| -3 | -0.738 |
| -2 | -0.522 |
| -1 | approximately 0 |
| 0 | +0.522 |
| +1 | +0.738 |
| +2 | +0.522 |
| +3 | approximately 0 |

At first, it may seem surprising that GUI offset 0 does not produce zero error.

The detector contains filter delay, branch delays, and a particular early/late sampling geometry. In this implementation, the useful balance point occurs near an assumed offset of $-1$.

The important lesson is:

> **The zero-error point of a timing detector is determined by the complete signal path and detector geometry, not by the numerical label assigned to one delay control.**

A practical timing loop does not care whether its internal balance point is numerically called 0, -1, or a fractional value. It cares about finding the point where the timing error is balanced.

### Why Transitions Matter

Timing information is strongest when the waveform changes.

If the signal remains almost constant over a long interval, early and late observations can look very similar. The detector then has little evidence about which direction to move.

Transitions create slope, and slope carries timing information.

This is why timing recovery is closely connected to pulse shape, transition density, and excess bandwidth.

## 22.5 From Timing Error to a Timing Loop

A timing-error detector does not synchronize the receiver by itself.

It only produces an error indicating whether the current sampling phase should move earlier or later.

A complete timing-recovery loop combines:

- a timing-error detector;
- a loop filter or controller;
- an estimate of the current timing phase;
- an interpolator that evaluates the waveform at the desired time.

The feedback principle is closely related to the carrier loops of Chapter 21.

| Carrier synchronization | Timing synchronization |
|---|---|
| phase/frequency-error detector | timing-error detector |
| loop filter | loop filter |
| oscillator or NCO control | interpolator timing control |
| corrected carrier reference | corrected symbol-sampling time |

The quantity being corrected is different, but the feedback idea is the same.

## 22.6 Why an Interpolator Is Necessary

With eight samples per symbol, it is tempting to think that timing recovery only needs to choose sample 0, 1, 2, and so on.

Real timing is not restricted to integer sample positions.

The optimum symbol instant might correspond to a position such as 3.42 samples relative to some reference.

There is no ADC sample exactly at 3.42.

A properly sampled bandlimited waveform, however, contains enough information to estimate values between the existing samples. An **interpolator** provides that estimate.

Conceptually,

$$
y(kT+\hat{\tau})=\text{interpolated value of the received waveform}
$$

where $\hat{\tau}$ is the receiver's current timing estimate.

This is why Symbol Sync is fundamentally more capable than `Keep 1 in N`.

`Keep 1 in N` can only select one of the samples that already exists.

A timing-recovery interpolator can estimate the waveform at the fractional-sample time where the receiver actually wants to make the symbol decision.

## 22.7 Experiment 22.3: Automatic Timing Recovery with Symbol Sync

We now return to pulse-shaped QPSK and replace manual timing selection with a feedback synchronization loop.

One branch uses fixed sampling as a reference. The second branch passes the matched-filter output through GNU Radio's Symbol Sync block.

![Flowgraph for automatic QPSK timing recovery using Symbol Sync](../figures/ch22/ch22_exp3_symbol_sync_timing_recovery_flowgraph.png)

The principal settings are

| Parameter | Value |
|---|---:|
| Sample rate | `32 kS/s` |
| Symbol rate | `4 ksymbol/s` |
| Samples per symbol | `8` |
| RRC roll-off | `0.35` |
| Symbol Sync TED | Gardner |
| Symbol Sync loop bandwidth | `0.045` |
| Output samples/symbol | `1` |

### What We Observe

![Automatic timing recovery using the Gardner TED in Symbol Sync](../figures/ch22/ch22_exp3_symbol_sync_timing_recovery.png)

When the fixed sampling position is poor, its constellation spreads.

The Symbol Sync output remains concentrated around the QPSK decision points because the timing loop estimates the appropriate sampling phase and uses interpolation to obtain the symbol values at those times.

The receiver has changed from a fixed sampler into an adaptive sampler.

### Acquisition and Tracking

The same terms used for carrier synchronization are useful here.

**Acquisition** is the process of finding a useful timing phase after the receiver starts.

**Tracking** is the continued adjustment used to follow timing after acquisition.

A fixed timing offset mainly tests acquisition. Once the correct phase is found, it can remain approximately constant.

Independent transmitter and receiver sampling clocks create a harder problem because their relative timing can drift continuously.

## 22.8 Timing Offset Is Not the Same as Sampling-Clock Mismatch

This distinction is essential.

A **fixed timing offset** means the sampling phase is displaced but does not necessarily keep moving.

A **sampling-clock mismatch** means the transmitter and receiver sampling rates differ slightly, so their relative timing position drifts.

If the receiver's sampling clock is slightly fast or slow, the preferred symbol-sampling position gradually moves through the sampled waveform.

This is the impairment introduced with the Channel Model's `Epsilon` parameter in Chapter 19. There we observed the problem without correcting it.

Here we use timing recovery to track it.

For the model used in the experiments, the ideal setting is

$$
\epsilon=1
$$

and values slightly different from 1 introduce a persistent sample-rate mismatch.

For example,

$$
\epsilon=1.004
$$

produces an intentionally exaggerated mismatch that is easy to observe.

The exact ratio convention should always be interpreted according to the block implementation. The practical meaning here is that $\epsilon\neq1$ causes the receiver's sample timing to slip progressively relative to the transmitted symbols.

## 22.9 Experiment 22.4: Sampling-Clock Mismatch and Timing Tracking

We extend the previous QPSK receiver by introducing a controlled clock-rate mismatch with the Channel Model.

The matched-filter output is observed through two receiver paths:

**Matched Filter → Keep 1 in N → Fixed Sampling**

and

**Matched Filter → Symbol Sync → Timing-Recovered QPSK**

The first path cannot adapt. The second can.

![Flowgraph for sampling-clock mismatch and timing tracking](../figures/ch22/ch22_exp4_clock_mismatch_tracking_flowgraph.png)

The main parameters are

| Parameter | Value |
|---|---:|
| Sample rate | `32 kS/s` |
| Symbol rate | `4 ksymbol/s` |
| Samples per symbol | `8` |
| RRC roll-off | `0.35` |
| Channel noise voltage | `0` |
| Channel frequency offset | `0` |
| Symbol Sync TED | Gardner |
| Symbol Sync loop bandwidth | `0.045` |

We compare

```text
Matched clocks
epsilon = 1.000

Exaggerated clock mismatch
epsilon = 1.004
```

The value `1.004` is intentionally large enough to make the effect easy to see. It is a teaching value rather than a claim about typical hardware accuracy.

### Eye Diagram and Constellation Together

![Eye diagrams and timing recovery with matched and mismatched sampling clocks](../figures/ch22/ch22_exp4_clock_mismatch_eye_timing_recovery.png)

At $\epsilon=1.000$, the transmitter and receiver sample rates agree and the eye diagrams show a stable timing structure.

At $\epsilon=1.004$, the receiver's sample grid moves continuously relative to the waveform. Over time, the display contains traces at different timing phases, so the pre-synchronization eye becomes horizontally smeared.

The fixed-sampling constellation degrades because it continues taking the same relative sample positions even though the preferred position is moving.

The timing-recovered constellation remains concentrated near the four QPSK symbol locations because Symbol Sync continuously adjusts its interpolation phase.

### Eye Diagram and Constellation Are Different Measurements

This experiment is especially useful for separating the two views.

The Eye Sink is connected **before Symbol Sync**. It shows the oversampled, clock-impaired matched-filter waveform on the receiver's current sample grid.

The constellation after Symbol Sync shows the complex samples that the timing loop has selected or interpolated at its recovered symbol instants.

It is therefore possible to observe a smeared pre-synchronization eye and, at the same time, a clean timing-recovered constellation.

There is no contradiction.

The eye describes timing structure and timing margin in the oversampled waveform. The constellation describes the complex samples actually used for symbol decisions.

More generally, an open eye does not guarantee a clean constellation. Carrier phase or frequency error can rotate or smear the selected complex samples even when the timing eye remains reasonably open.

### Physical Meaning

A sampling-clock mismatch is similar to two watches that run at slightly different rates.

They may agree initially, but their readings gradually separate.

A one-time delay correction cannot solve that problem because the required timing correction keeps changing.

The receiver must track the timing continuously.

## 22.10 The Role of Excess Bandwidth

The experiments use an RRC roll-off factor of

$$
\alpha=0.35
$$

Earlier, $\alpha$ was discussed mainly in terms of pulse shape and occupied bandwidth.

It also affects timing recovery.

Timing-error detectors extract information from waveform changes around symbol transitions. The amount and form of that timing-sensitive structure depend on the pulse shape and excess bandwidth.

This does not mean that a larger roll-off is always better.

Increasing excess bandwidth consumes more spectrum.

The useful lesson is that pulse shaping, spectral efficiency, and synchronization are connected design choices.

## 22.11 Gardner and Mueller and Müller

GNU Radio's Symbol Sync block offers several timing-error detectors, including Gardner, Early-Late, Mueller and Müller, modified Mueller and Müller, Zero Crossing, and maximum-likelihood-related methods.

We use Gardner for the main synchronization experiments.

### Gardner

Gardner is naturally used with an oversampled waveform and can generate timing information without requiring correct symbol decisions before acquisition begins.

A representative complex form of the Gardner timing error is

$$
e[k]=\operatorname{Re}\{(x[k]-x[k-1])x^*[k-\tfrac{1}{2}]\}
$$

with indexing and sign convention depending on the implementation.

The important idea is that the detector uses symbol-spaced samples and a midpoint sample to determine how the sampling phase should move.

### Mueller and Müller

Mueller and Müller, often abbreviated M&M, is more closely associated with symbol-rate, decision-directed timing recovery.

It uses relationships between received samples and estimated symbol values to form a timing error.

Its behaviour also depends on the pulse shape and excess bandwidth.

During development, M&M was tested in the same clean QPSK receiver and produced essentially the same practical recovery. A separate full experiment would therefore add little here.

The broader lesson is that there is no single timing-error detector that is best for every receiver.

The choice depends on the modulation, samples per symbol, pulse shape, available transition information, decision reliability, acquisition requirements, and expected operating conditions.

## 22.12 Experiment 22.5: Effect of Timing-Loop Bandwidth

A timing loop must decide how aggressively to react to its error signal.

One important control is the **loop bandwidth**.

For this experiment, we retain the sampling-clock mismatch

$$
\epsilon=1.001
$$

and compare

```text
Narrow Timing Loop
Loop Bandwidth: 0.005

Wide Timing Loop
Loop Bandwidth: 0.100
```

All other important settings remain unchanged.

![Effect of timing-loop bandwidth on timing recovery](../figures/ch22/ch22_exp5_timing_loop_bandwidth.png)

### What We Observe

Both settings recover timing in this controlled experiment, but the recovered constellations do not have identical quality.

With the narrower loop bandwidth, the recovered QPSK points are more tightly concentrated.

With the larger value of `0.100`, the recovered constellation is more degraded and jittery.

A larger timing-loop bandwidth therefore does not automatically mean better synchronization.

A wider loop reacts more quickly to changing timing error, but it also follows rapid variations in the timing-error estimate more strongly.

A narrower loop responds more slowly and smooths those variations more strongly.

| Narrow loop bandwidth | Wide loop bandwidth |
|---|---|
| slower response | faster response |
| stronger smoothing | follows rapid timing changes more readily |
| lower steady-state timing jitter in this clean case | more sensitive to rapid TED variation |
| may struggle with rapid timing drift | can track faster timing changes |

The preferred loop bandwidth depends on the expected clock dynamics, signal conditions, noise, and acquisition requirements.

### Acquisition Transient

A feedback timing loop needs time to acquire.

Immediately after startup, the internal timing estimate may not yet have settled.

The settling time depends on the loop bandwidth, initial timing error, signal conditions, and implementation.

A narrower loop usually takes longer to settle than a wider one.

This is the same acquisition-versus-tracking distinction encountered with carrier loops in Chapter 21.

## 22.13 What Is Actually Being Recovered?

Symbol Sync recovers **symbol timing**.

It does not recover carrier frequency.

It does not correct arbitrary carrier phase rotation.

It does not equalize a multipath channel.

It does not remove independent random noise.

These are separate receiver functions.

| Receiver problem | Typical correction |
|---|---|
| carrier frequency/phase error | carrier synchronization |
| wrong or drifting symbol timing | timing recovery |
| multipath-induced channel memory | equalization |
| independent random noise | cannot simply be inverted |

The exact order of receiver blocks can vary, and practical synchronization loops can interact.

The conceptual responsibilities remain different.

A constellation can reveal that something is wrong, but diagnosing the cause requires understanding whether the dominant problem is carrier reference, timing, channel distortion, or noise.

## 22.14 Fixed Timing Error Versus Timing Drift

The chapter has exposed two different timing problems.

| Problem | What happens? | Receiver requirement |
|---|---|---|
| timing phase offset | sampling position is displaced | acquire the correct timing phase |
| sampling-clock mismatch | sampling position progressively drifts | continuously track timing |

This explains why Experiments 22.1 and 22.4 are related but not redundant.

Experiment 22.1 manually chooses different fixed positions within the eight-sample symbol interval.

Experiment 22.4 makes the preferred position move because the transmitter and receiver clocks disagree.

A practical receiver generally has to handle both acquisition and tracking.

## 22.15 The Timing-Recovery Mechanism

The complete timing-recovery process can now be described without hiding behind a single GNU Radio block.

First, the receiver keeps an oversampled version of the waveform.

Next, a timing-error detector examines timing-sensitive waveform structure and produces an error indicating whether the current sampling phase should move.

A loop filter controls how strongly the receiver reacts.

An interpolator then evaluates the waveform at the required fractional-sample position.

The process repeats continuously so that timing drift can be tracked.

The receiver is repeatedly answering one question:

> **Given the waveform just observed, where should the next symbol be sampled?**

That is symbol timing synchronization.

## 22.16 Other Timing-Recovery Approaches

This chapter focuses on feedback timing recovery because it gives a clear path from timing error to practical GNU Radio synchronization.

Timing recovery is broader than one algorithm.

Receivers may use Early-Late detectors, derivative-based detectors, zero-crossing detectors, Gardner, Mueller and Müller, maximum-likelihood methods, feedforward estimators, polyphase filter-bank techniques, and other specialized approaches.

Some estimate timing from a block of data and then apply a correction.

Others continuously update timing in a feedback loop.

Some depend on symbol decisions or known training information. Others can begin without them.

The common objective remains the same:

$$
\text{estimate the correct symbol times and sample the waveform there}
$$

The detailed method depends on the signal and receiver architecture.

## 22.17 Practical SDR Interpretation

In a real SDR, the transmitter DAC clock and receiver ADC clock are produced by different physical oscillators.

Even if both devices are configured for the same nominal sample rate, their actual clock frequencies can differ slightly.

For example,

```text
Transmitter: 1.000000 MS/s
Receiver:    1.000000 MS/s
```

describes the configured rates, not a guarantee that the two physical clocks are exactly identical.

A tiny clock error may be negligible over one symbol but significant over thousands or millions of symbols because the timing difference accumulates.

Knowing the configured sample rate is therefore not enough.

A practical receiver estimates timing from the received waveform and continually compensates for relative clock error.

The same problem appears in wireless links, cable modems, satellite systems, telemetry, acoustic communication, optical links, and many other independently clocked digital systems.

## 22.18 GNU Radio Toolbox

Several GNU Radio blocks are especially important in this chapter.

| GNU Radio Block | Role in This Chapter |
|---|---|
| Keep 1 in N | demonstrates fixed integer sample selection |
| Delay | creates controlled timing offsets and early/late branches |
| Symbol Sync | performs feedback symbol timing recovery |
| Channel Model | introduces sample-rate mismatch through `Epsilon` |
| Eye Sink | shows the oversampled waveform and timing structure |
| QT GUI Constellation Sink | shows the selected complex symbol samples |

### Keep 1 in N

`Keep 1 in N` selects an existing sample at a fixed interval.

It is useful for demonstrating how strongly the constellation depends on sampling phase, but it is not a timing-recovery algorithm.

It cannot interpolate between samples or track a moving timing phase.

### Symbol Sync

Symbol Sync combines the main elements of feedback timing recovery:

- timing-error detection;
- timing-loop control;
- timing-phase estimation;
- interpolation;
- symbol-rate output.

The retained Gardner configuration uses

```text
I/O Type: Complex
Timing Error Detector: Gardner
Samples per Symbol: 8
Expected TED Gain: 1.0
Loop Bandwidth: 0.045
Damping Factor: 1.0
Maximum Deviation: 1.5
Output Samples/Symbol: 1
Interpolating Resampler: MMSE, 8 tap FIR
```

The exact values are experiment settings rather than universal defaults.

### Eye Sink

The Eye Sink displays many short segments of an oversampled waveform on the same time axis.

It is useful for observing timing margin, transition structure, ISI, and timing drift.

It should not be confused with a constellation display.

### Channel Model

In this chapter, the Channel Model is used mainly to introduce sample-rate mismatch through `Epsilon`.

With the other impairment controls neutral, this isolates the timing-drift problem.

## 22.19 Explore Further

The timing experiments support several useful extensions.

1. In Experiment 22.1, compare all eight integer sampling positions and identify the region that produces the tightest constellation.

2. In Experiment 22.2, change the Early-Late branch spacing and observe how the detector's balance point and sensitivity change.

3. In Experiment 22.3, start from several poor fixed sampling positions and compare the fixed-sampling and Symbol Sync outputs.

4. In Experiment 22.4, increase `epsilon` gradually from `1.000` toward `1.004` and compare the pre-synchronization eye with both constellations.

5. Reverse the direction of the sample-rate mismatch and observe whether the timing loop can track drift in the opposite direction.

6. With `epsilon = 1.001`, compare timing-loop bandwidths near `0.005`, `0.045`, and `0.100`.

7. Add moderate noise while keeping a clock mismatch and observe how the timing-loop bandwidth tradeoff changes.

8. Compare Gardner and Mueller and Müller in the same controlled receiver while keeping the pulse shape and sample rate unchanged.

9. Introduce carrier-frequency offset while observing the eye and constellation. Check whether a reasonably open eye can coexist with a rotating constellation.

## 22.20 What We Learned

A matched filter produces the waveform needed for reliable symbol decisions, but the receiver must still determine when to sample it.

With eight samples per symbol, different sampling positions can produce very different constellation quality.

Incorrect timing can smear a constellation even when carrier offset, noise, and multipath are absent.

A timing-error detector produces information about whether the receiver is sampling early or late.

The Early-Late experiment showed how energy on opposite sides of a candidate timing point can provide that error.

The zero of a timing-error detector depends on the complete detector geometry and processing delays rather than on an arbitrary GUI value called zero.

Transitions carry useful timing information, which connects timing recovery to pulse shape and excess bandwidth.

A timing-error detector must be placed inside a feedback loop to create automatic synchronization.

Interpolation is essential because the preferred symbol time generally lies between existing ADC samples.

GNU Radio's Symbol Sync combines timing-error detection, loop control, interpolation, and symbol-rate output.

The Gardner TED is well suited to the oversampled QPSK experiments and can begin operating without requiring correct symbol decisions.

Timing **acquisition** finds a useful sampling phase. Timing **tracking** follows that phase as it changes.

A fixed timing offset and a sampling-clock mismatch are different impairments.

A sampling-rate mismatch causes timing error to accumulate continuously.

The eye diagram shows the oversampled waveform and timing structure, while the constellation shows the complex samples actually selected at symbol instants. The two views are complementary, not interchangeable.

Symbol Sync can recover clean QPSK symbol samples even while the pre-synchronization eye shows the effect of sampling-clock mismatch.

Gardner and Mueller and Müller obtain timing information differently and should not be treated as competing versions of the same algorithm.

Timing-loop bandwidth trades response speed against smoothing and steady-state jitter.

Finally, timing synchronization corrects sampling time. It does not replace carrier recovery, equalization, or noise handling.

The receiver now knows both how the constellation should be oriented and when each symbol should be observed.

## 22.21 Connecting to the Next Chapter

The last several chapters have progressively repaired the received signal.

The wireless channel introduced attenuation, noise, carrier offset, multipath, and sample-rate mismatch.

Equalization addressed structured channel distortion.

Carrier synchronization corrected carrier frequency and phase.

This chapter recovered symbol timing.

The receiver can now obtain stable symbol samples at the appropriate instants.

But recovering individual symbols is not the same as recovering a complete transmitted message.

A practical receiver must also determine where a packet or frame begins, identify known synchronization structures, establish boundaries in the incoming stream, and organize recovered symbols or bits into meaningful units.

That leads to **Chapter 23: Frame Synchronization and Packet Detection**.