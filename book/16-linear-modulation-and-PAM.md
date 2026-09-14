# Chapter 16: Linear Modulation and PAM

## Main Question

**What if we represent digital information using different signal amplitudes?**

Chapter 15 ended with symbol indices.

For two bits per symbol, the bit groups

```text
00
01
10
11
```

became the indices

```text
0
1
2
3
```

Those numbers were useful labels, but they were still abstract. Nothing in the number `2`, for example, says what the transmitted signal should look like.

This chapter completes that missing step.

We will map each symbol index to a real amplitude, turn those amplitudes into a simple waveform, add noise, and then ask the receiver to decide which symbol was most likely transmitted.

That leads us to **Pulse Amplitude Modulation**, or **PAM**, and to several ideas that will remain important throughout digital communication:

- symbol mapping;
- decision thresholds;
- hard decisions;
- noisy observations;
- symbol errors;
- symbol energy.

The geometry is still one-dimensional. Every symbol lies somewhere on one amplitude axis.

That simplicity makes PAM a good place to learn how a digital receiver makes decisions before we move into the two-dimensional I/Q plane.

## 16.1 From Symbol Index to Signal Amplitude

Suppose the transmitter has four symbol indices:

$$
0,\;1,\;2,\;3.
$$

We can choose a mapping such as:

| Symbol Index | PAM Amplitude |
|---:|---:|
| 0 | -3 |
| 1 | -1 |
| 2 | +1 |
| 3 | +3 |

The allowed amplitudes are therefore

$$
\{-3,\;-1,\;+1,\;+3\}.
$$

Because there are four possible levels, this is **4-PAM**.

The important distinction is:

The mapping is `0 → -3`, `1 → -1`, `2 → +1`, and `3 → +3`.

The number on the left is a digital label.

The number on the right is the signal value chosen to represent that label.

There is no requirement that symbol index `2` be transmitted as amplitude `2`. The mapping is a design choice.

## 16.2 Experiment 16.1: Mapping Symbols to 4-PAM Levels

The first experiment adds one new operation to the bit-to-symbol chain from Chapter 15: a lookup from symbol index to amplitude.

Use:

| Parameter | Value |
|---|---:|
| Sample rate | `32k` samples/s |
| Bit rate | `1k` bit/s |
| Bits per symbol | `2` |
| Symbol rate | `500` symbols/s |
| Samples per symbol | `64` |
| 4-PAM symbol table | `[-3, -1, 1, 3]` |

The rate relationship remains

$$
R_b=kR_s.
$$

With two bits per symbol,

$$
R_s=\frac{R_b}{k}=\frac{1000}{2}=500\text{ symbols/s}.
$$

At 32 kS/s,

$$
N_{\text{sps}}=\frac{f_s}{R_s}=\frac{32000}{500}=64.
$$

The flowgraph uses **Chunks to Symbols** as the mapper.

![Experiment 16.1 flowgraph: mapping symbol indices to PAM amplitudes](../figures/ch16/ch16-exp1-symbol-to-amplitude-flowgraph.png)

The actual block uses:

```text
Input Type: byte
Output Type: float
Symbol Table: [-3, -1, 1, 3]
Dimension: 1
Num Ports: 1
```

The incoming symbol index selects one entry from the table:

The mapping is `0 → -3`, `1 → -1`, `2 → +1`, and `3 → +3`.

The result is shown below.

![Experiment 16.1 result: symbol indices and corresponding 4-PAM amplitudes](../figures/ch16/ch16-exp1-symbol-to-amplitude.png)

The two plots contain the same information in different forms.

One shows abstract symbol indices.

The other shows the amplitudes assigned to those indices.

Chunks to Symbols has not created new information. It has changed how the information is represented.

That same idea will return later when integer symbol labels are mapped to complex constellation points.

## 16.3 Experiment 16.2: From PAM Levels to a Waveform

A symbol amplitude still needs a duration.

If the symbol rate is \(R_s\), then

$$
T_s=\frac{1}{R_s}.
$$

For

$$
R_s=500\text{ symbols/s},
$$

the symbol duration is

$$
T_s=\frac{1}{500}=2\text{ ms}.
$$

A simple way to create a sampled waveform is to hold each amplitude constant throughout that interval.

With 64 samples per symbol, the Repeat block outputs 64 copies of every mapped PAM value.

![Experiment 16.2 flowgraph: constructing a rectangular 4-PAM waveform](../figures/ch16/ch16-exp2-rectangular-pam-flowgraph.png)

The result separates two ideas that are easy to mix together.

![Experiment 16.2 result: individual 4-PAM symbol values and the rectangular PAM waveform](../figures/ch16/ch16-exp2-rectangular-pam.png)

A sequence such as

$$
1,\;3,\;-3,\;1,\;1,\;3,\;-3,\;1
$$

is a sequence of symbol values.

After Repeat, each value is held for the full symbol interval. The result is a waveform in time.

For this chapter, the rectangular pulse is useful because its timing is obvious. It is not yet meant to be a realistic band-limited transmit pulse.

### Why This Is PAM

A general baseband linear modulation signal can be written as

$$
x(t)=\sum_k a_kp(t-kT_s),
$$

where:

- \(a_k\) is the symbol value;
- \(p(t)\) is the pulse shape;
- \(T_s\) is the symbol duration.

In this experiment, \(p(t)\) is rectangular.

The pulse shape stays the same. Only its coefficient \(a_k\) changes from symbol to symbol.

That is the basic idea behind Pulse Amplitude Modulation.

It is also why PAM fits naturally into the broader class of **linear modulation**.

## 16.4 Experiment 16.3: Hard Decisions in 2-PAM

Before building a receiver for four levels, it is useful to simplify the problem.

Consider **2-PAM**:

```text
bit 0 -> -1
bit 1 -> +1
```

The allowed levels are

$$
\{-1,\;+1\}.
$$

If the receiver observes \(+0.82\), the value is not exactly \(+1\), but it is clearly closer to the positive symbol than the negative one.

For symmetric 2-PAM, the natural boundary is zero.

The intended decision rule is

$$
r<0\rightarrow\text{bit }0
$$

and

$$
r>0\rightarrow\text{bit }1,
$$

where \(r\) is the received symbol observation.

An observation exactly at zero lies on the decision boundary. In a continuous-noise model, landing exactly there has probability zero, so the important behaviour is what happens on either side.

The GNU Radio experiment uses:

| Parameter | Value |
|---|---:|
| Sample rate | `32k` samples/s |
| Bit rate | `1k` bit/s |
| Bits per symbol | `1` |
| Symbol rate | `1k` symbols/s |
| Samples per symbol | `32` |
| 2-PAM symbol table | `[-1, 1]` |

![Experiment 16.3 flowgraph: hard decisions for a 2-PAM signal](../figures/ch16/ch16-exp3-2pam-hard-decision-flowgraph.png)

The **Binary Slicer** performs the zero-threshold hard decision.

![Experiment 16.3 result: original bits, 2-PAM levels, and detected bits](../figures/ch16/ch16-exp3-2pam-hard-decision.png)

The noiseless chain is now complete:

The noiseless chain is straightforward: bit `0` maps to `-1` and is detected as `0`, while bit `1` maps to `+1` and is detected as `1`.

This is simple, but it establishes an important receiver viewpoint.

The receiver does not need the physical amplitude to equal the original bit value.

It only needs a rule that maps the measured signal back to one of the allowed digital states.

That is a **hard decision**.

## 16.5 Experiment 16.4: 2-PAM with Noise

Real receivers do not observe perfect levels.

A transmitted \(+1\) may arrive as

```text
+0.92
+1.18
+0.55
+1.31
```

and a transmitted \(-1\) may arrive as

```text
-0.87
-1.16
-0.48
-1.29
```

The receiver can still make the correct decision as long as the observation stays on the correct side of zero.

Experiment 16.4 adds real Gaussian noise before the Binary Slicer.

![Experiment 16.4 flowgraph: 2-PAM with adjustable Gaussian noise and hard decisions](../figures/ch16/ch16-exp4-2pam-noise-flowgraph.png)

Use:

```text
QT GUI Range
ID: noise_amp
Label: Noise Amplitude
Default Value: 0
Start: 0
Stop: 2
Step: 0.05

Noise Source
Noise Type: Gaussian
Amplitude: noise_amp
Seed: 0
```

For GNU Radio's real Gaussian Noise Source, `Amplitude` is the standard deviation of the generated noise.

With `Seed = 0`, GNU Radio chooses a seed from the system clock. A non-zero seed is better when exactly repeatable noise is needed.

### A Deliberate Simplification

The order of the blocks matters.

In this experiment, GNU Radio first creates one ideal PAM symbol value, adds one Gaussian noise value to that symbol observation, sends the noisy observation to the Binary Slicer, and only then uses Repeat to stretch the result for display.

So this is not yet a sample-by-sample noisy channel.

It is a **symbol-level observation model**:

$$
r_k=a_k+n_k.
$$

That simplification is intentional. It lets us study decision thresholds without also introducing pulse shaping, matched filtering, timing recovery, and sampling.

With moderate noise:

![Experiment 16.4 result: noisy 2-PAM observations that remain on the correct side of the threshold](../figures/ch16/ch16-exp4-2pam-noise-correct.png)

The received values move away from \(-1\) and \(+1\), but the detected bits remain correct.

A transmitted \(+1\) received as

$$
r=+0.42
$$

is still positive, so the detector returns `1`.

A transmitted \(-1\) received as

$$
r=-0.35
$$

is still negative, so the detector returns `0`.

Now increase the noise.

![Experiment 16.4 result: a noisy 2-PAM observation crosses the threshold and causes a wrong decision](../figures/ch16/ch16-exp4-2pam-wrong-decision.png)

Once an observation crosses zero, the receiver selects the wrong decision region.

For example, if \(+1\) was transmitted but

$$
r=-0.18,
$$

the Binary Slicer sees a negative value and outputs `0`.

The key lesson is:

> **Noise does not cause a digital error merely because it changes the amplitude. An error occurs when the observation crosses a decision boundary.**

## 16.6 From 2-PAM to 4-PAM Decision Regions

Return to the 4-PAM alphabet:

$$
\{-3,\;-1,\;+1,\;+3\}.
$$

With two levels, one boundary at zero was enough.

With four levels, the receiver needs three boundaries.

For equally spaced levels and equal a priori likelihoods in symmetric Gaussian noise, the natural thresholds lie halfway between adjacent symbols:

$$
-2,\;0,\;+2.
$$

The resulting regions are:

| Received Observation | Detected Symbol Index |
|---|---:|
| \(r<-2\) | 0 |
| \(-2\leq r<0\) | 1 |
| \(0\leq r<2\) | 2 |
| \(r\geq2\) | 3 |

These midpoint thresholds are optimal for the simple equal-probability, equal-cost, additive Gaussian model used here.

In a different receiver, unequal symbol probabilities or unequal error costs could shift the optimum boundaries.

That broader detection-theory problem is not needed yet. For our experiment, midpoint thresholds give a clear and physically meaningful receiver.

## 16.7 Experiment 16.5: Hard Decisions in 4-PAM

Experiment 16.5 implements the three thresholds in two ways.

The transmitter uses:

| Parameter | Value |
|---|---:|
| Sample rate | `32k` samples/s |
| Bit rate | `1k` bit/s |
| Bits per symbol | `2` |
| Symbol rate | `500` symbols/s |
| Samples per symbol | `64` |
| 4-PAM table | `[-3, -1, 1, 3]` |

### Building the Detector from Ordinary Blocks

Binary Slicer makes a sign decision around zero.

To test a threshold somewhere else, shift the input first.

For the \(-2\) boundary,

$$
r>-2
$$

can be written as

$$
r+2>0.
$$

For the \(+2\) boundary,

$$
r>2
$$

can be written as

$$
r-2>0.
$$

The receiver therefore performs three tests:

The receiver therefore evaluates three shifted versions of the same observation: `r + 2`, `r`, and `r - 2`, each followed by a Binary Slicer.

Away from the exact boundaries, the three binary outputs form:

| PAM Level | \(r>-2\) | \(r>0\) | \(r>2\) | Sum |
|---:|---:|---:|---:|---:|
| -3 | 0 | 0 | 0 | 0 |
| -1 | 1 | 0 | 0 | 1 |
| +1 | 1 | 1 | 0 | 2 |
| +3 | 1 | 1 | 1 | 3 |

The sum directly gives the symbol index.

![Experiment 16.5 flowgraph: 4-PAM hard decisions using ordinary GNU Radio blocks and an Embedded Python alternative](../figures/ch16/ch16-exp5-4pam-hard-decision-flowgraph.png)

The flowgraph also includes an Embedded Python implementation of the same detector.

![Experiment 16.5 result: transmitted indices, 4-PAM levels, and hard decisions from both detector implementations](../figures/ch16/ch16-exp5-4pam-hard-decision.png)

Both receivers produce the same symbol sequence for the ideal input.

The ordinary-block implementation is valuable because every threshold is visible.

The Python version is valuable because it expresses the same logic compactly.

### Embedded Python Detector

The detector used in the experiment is:

```python
import numpy as np
from gnuradio import gr


class blk(gr.sync_block):

    def __init__(self):
        gr.sync_block.__init__(
            self,
            name='4-PAM Hard Decision',
            in_sig=[np.float32],
            out_sig=[np.uint8]
        )

    def work(self, input_items, output_items):
        x = input_items[0]
        y = output_items[0]

        n = min(len(x), len(y))

        for i in range(n):
            if x[i] < -2:
                y[i] = 0
            elif x[i] < 0:
                y[i] = 1
            elif x[i] < 2:
                y[i] = 2
            else:
                y[i] = 3

        return n
```

The boundary convention is now explicit.

An observation exactly at \(-2\) is assigned to symbol 1, exactly at \(0\) to symbol 2, and exactly at \(+2\) to symbol 3.

In practical continuous-noise operation, exact equality is not normally important. What matters is which region the observation enters.

## 16.8 Experiment 16.6: 4-PAM with Noise

The final experiment adds Gaussian noise to the 4-PAM symbol observations and keeps only the compact Embedded Python detector.

![Experiment 16.6 flowgraph: 4-PAM with adjustable noise and an Embedded Python hard-decision receiver](../figures/ch16/ch16-exp6-4pam-noise-flowgraph.png)

The noise settings remain:

```text
Noise Type: Gaussian
Amplitude: noise_amp
Seed: 0
```

As in Experiment 16.4, the noise is added at the **symbol-observation level before Repeat**.

The model is therefore

$$
r_k=a_k+n_k,
$$

not yet a complete oversampled transmit-channel-receive chain.

With moderate noise:

![Experiment 16.6 result: noisy 4-PAM observations remain inside their correct decision regions](../figures/ch16/ch16-exp6-4pam-noise-correct.png)

The received values no longer sit exactly at \(-3\), \(-1\), \(+1\), and \(+3\), but they remain inside the correct regions.

The detector therefore recovers the correct symbol indices.

With stronger noise:

![Experiment 16.6 result: strong noise pushes 4-PAM observations across decision thresholds and causes symbol errors](../figures/ch16/ch16-exp6-4pam-wrong-decisions.png)

Some observations cross \(-2\), \(0\), or \(+2\).

Once that happens, the receiver chooses another region and produces a symbol error.

For example, if \(+1\) was transmitted, the correct region is

$$
0\leq r<2.
$$

Noise can cause an error in either direction:

$$
r<0
$$

moves the observation into the \(-1\) region, while

$$
r\geq2
$$

moves it into the \(+3\) region.

The receiver is still following its decision rule correctly. The problem is that the channel has moved the observation into the wrong region.

## 16.9 Distance to a Decision Boundary

The experiments suggest a better way to think about noise robustness.

The receiver does not ask:

> Did the observation land exactly on the ideal symbol?

It asks:

> Which decision region contains the observation?

For 2-PAM, the levels are \(-1\) and \(+1\), and the threshold is zero.

Each ideal symbol is therefore one amplitude unit from the nearest decision boundary.

For 4-PAM with levels

$$
-3,\;-1,\;+1,\;+3,
$$

the thresholds are

$$
-2,\;0,\;+2.
$$

Each ideal level is also one amplitude unit from its nearest boundary in this unnormalised constellation.

That does **not** mean the two modulation schemes have identical performance in a fair communication comparison.

Their average energies are different.

This is why distance and energy must be considered together.

## 16.10 Symbol Energy and Normalisation

For a rectangular symbol of constant amplitude \(A\) lasting \(T_s\),

$$
E_s=A^2T_s.
$$

The sign does not matter because the amplitude is squared.

For 2-PAM,

$$
A\in\{-1,+1\},
$$

so both symbols have

$$
E_s=T_s.
$$

For the 4-PAM alphabet

$$
A\in\{-3,-1,+1,+3\},
$$

the squared amplitudes are

$$
9,\;1,\;1,\;9.
$$

If all four symbols are equally likely, the average symbol energy is

$$
\overline{E_s}=\frac{9+1+1+9}{4}T_s=5T_s.
$$

So the raw 4-PAM constellation used in the experiments has five times the average symbol energy of the raw 2-PAM constellation if the symbol durations are the same.

A fair noise-performance comparison must not ignore that.

Dividing the 4-PAM amplitudes by

$$
\sqrt{5}
$$

gives

$$
\left\{-\frac{3}{\sqrt{5}},-\frac{1}{\sqrt{5}},+\frac{1}{\sqrt{5}},+\frac{3}{\sqrt{5}}\right\},
$$

which has unit average squared amplitude.

For our rectangular pulse of duration \(T_s\), its average symbol energy then becomes

$$
\overline{E_s}=T_s.
$$

If the pulse shape itself is normalised to unit energy, the same scaling gives unit average symbol energy.

We keep the simple levels \(-3,-1,+1,+3\) in the experiments because the mapping and thresholds are much easier to see.

The screenshots should therefore be used to understand decision geometry, not to claim a fair BER comparison between 2-PAM and 4-PAM.

## 16.11 Four Different Quantities in One Receiver

Consider symbol index `2`.

In our 4-PAM mapping, symbol index `2` is mapped to the ideal amplitude `+1`. After the channel and noise, the receiver might observe a value such as `+0.63`. Because `+0.63` still lies inside the decision region for symbol index `2`, the detector returns `2`.

These are four different quantities.

**Symbol index** is an abstract digital label.

**Ideal symbol amplitude** is the signal value assigned to that label.

**Received observation** is what the receiver actually measures.

**Detected symbol index** is the receiver's discrete decision.

Keeping these stages separate is essential.

Later, when symbols become complex I/Q points, the same logic will remain:

The same sequence remains: a label is mapped to an ideal point, the channel moves it to a noisy point, and the receiver makes a decision.

Only the geometry will change.

## 16.12 Where PAM Fits in a Complete Link

The experiments deliberately isolate mapping and decisions.

A practical baseband digital link contains more stages:

A practical link proceeds from bits to symbol mapping, pulse shaping, transmission through the channel, receiver filtering, sampling at the symbol instants, symbol decisions, and finally recovered bits.

This chapter focuses on two parts:

- mapping symbol indices to amplitudes;
- turning noisy amplitude observations back into symbol indices.

The omitted stages are not unimportant.

Pulse shaping controls bandwidth and inter-symbol interference.

Receiver filtering improves how the desired signal is collected.

Timing recovery determines when the receiver should sample.

Those topics are easier to understand once the decision problem itself is already clear.

The noise experiments in this chapter are therefore intentionally simple symbol-level models, not complete communication channels.

## 16.13 GNU Radio Toolbox

Several familiar blocks take on important digital-communication roles here.

| GNU Radio Block | Role in This Chapter |
|---|---|
| Repack Bits | Groups incoming bits into symbol indices |
| Chunks to Symbols | Maps symbol indices to real PAM amplitudes |
| Repeat | Holds a symbol value for several display samples to form a rectangular waveform |
| Binary Slicer | Implements a zero-threshold binary hard decision |
| Noise Source | Adds real Gaussian disturbance to symbol observations |
| QT GUI Range | Controls the noise standard deviation interactively |
| Add Const | Moves a non-zero threshold to zero before Binary Slicer |
| Embedded Python Block | Implements compact multi-level 4-PAM decision logic |

### Chunks to Symbols

The block behaves like a lookup table.

For

```text
[-3, -1, 1, 3]
```

index `0` selects `-3`, index `1` selects `-1`, and so on.

### Binary Slicer

The block produces binary `1` for positive input and binary `0` for negative input.

In symmetric 2-PAM, this makes zero the natural decision boundary.

For exact zero, the block documentation does not define the behaviour in the same positive/negative wording, so we treat zero as the mathematical boundary rather than relying on it as an ordinary decision case.

### Add Const

A threshold at \(T\) can be turned into a zero-threshold test by forming

$$
r-T.
$$

Experiment 16.5 uses this idea for the thresholds \(-2\) and \(+2\).

### Embedded Python Block

Once the threshold logic is understood, a short custom block can express the same receiver more compactly.

The block does not use a different detection principle. It simply packages the decision regions into reusable code.

## 16.14 Explore Further

The PAM experiments are well suited to prediction before execution.

1. Change the 4-PAM symbol table to `[-6, -2, 2, 6]`. Predict the new midpoint thresholds.

2. Change the 2-PAM mapping to `[-2, 2]`. Predict how far each ideal level will be from the zero decision boundary.

3. In Experiment 16.4, use a non-zero Noise Source seed so the same noise realisation can be reproduced across runs.

4. In Experiment 16.5, replace the 4-PAM levels with a non-uniform alphabet such as `[-4, -1, 1, 3]`. Calculate the midpoint thresholds before modifying the receiver.

5. Change the 4-PAM detector to output the nearest ideal amplitude instead of the symbol index. Compare the role of a slicer with the role of a symbol decoder.

6. Normalise the 4-PAM levels by \(\sqrt{5}\), then recalculate the corresponding thresholds.

7. Move the Noise Source after Repeat and observe how different the time-domain display becomes when every waveform sample receives an independent disturbance rather than one disturbance per symbol observation.

The last experiment is especially useful because it connects this simplified chapter to the more realistic transmit-channel-receive chain that comes later.

## 16.15 What We Learned

Chapter 15 ended with symbol indices.

This chapter turned those labels into signal amplitudes.

For 4-PAM, we used

$$
0\rightarrow-3,\qquad1\rightarrow-1,\qquad2\rightarrow+1,\qquad3\rightarrow+3.
$$

Chunks to Symbols performed that mapping.

Repeat then held each symbol value for a chosen number of samples, giving us a simple rectangular PAM waveform.

In the general linear modulation model,

$$
x(t)=\sum_k a_kp(t-kT_s),
$$

the data changes the coefficient \(a_k\), while \(p(t)\) describes the pulse shape.

At the receiver, we began with 2-PAM and one decision boundary at zero.

Then we moved to 4-PAM and three boundaries at

$$
-2,\;0,\;+2.
$$

The noise experiments showed that a received symbol does not need to land exactly on its ideal level.

It only needs to stay inside the correct decision region.

A symbol error occurs when noise pushes the observation across a boundary.

We also separated four quantities that will remain important:

A useful sequence to remember is: symbol index, ideal signal value, received observation, and detected symbol index.

Finally, symbol energy showed why raw amplitude spacing alone is not enough for a fair comparison between modulation schemes. Energy normalisation matters when performance is compared quantitatively.

The one-dimensional PAM picture has now given us the essential language of digital detection:

- ideal symbol locations;
- noisy observations;
- distances;
- thresholds;
- decision regions.

## 16.16 Connecting to the Next Chapter

Every PAM symbol in this chapter lived on one real amplitude axis.

But a complex baseband sample has two components:

$$
x[n]=I[n]+jQ[n].
$$

That gives us two dimensions.

Instead of choosing one amplitude on a line, a digital symbol can choose a point in the I/Q plane.

The receiver will still see ideal symbol locations, noisy observations, and decision regions. The same ideas from PAM will survive.

The geometry will simply become two-dimensional.

That takes us to Chapter 17, **BPSK, QPSK and QAM**.