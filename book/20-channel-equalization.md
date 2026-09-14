# Chapter 20: Channel Equalization

## Main Question

**If the wireless channel has distorted the received symbols, how can the receiver compensate for that distortion?**

Chapter 19 showed that a wireless channel can give the receiver more than one delayed copy of the transmitted waveform.

For the one-symbol echo used there, the sampled signal was approximately

$$
r[k]=s[k]+0.5s[k-1]
$$

The current received sample contains the desired symbol plus part of the previous one. The channel therefore has memory, and that memory produces intersymbol interference.

This chapter starts from that result rather than introducing ISI again.

The new question is what the receiver can do about it.

The answer is **equalization**.

An equalizer is a receiver filter designed to compensate for predictable distortion introduced by the channel. It does not reconstruct information that has been completely lost, and it does not correct every receiver impairment. Its job is to make the combined channel-plus-equalizer response closer to the response we want.

We will develop the idea in stages.

First, we will assume that the channel is known and construct an approximate inverse manually. Then we will remove that unrealistic assumption and let an adaptive equalizer adjust its own coefficients. Finally, we will introduce known training symbols, examine how the receiver finds and aligns them, and test what happens when the multipath becomes stronger or random noise is added.

## 20.1 From Channel Memory to Receiver Correction

There is a useful connection back to Chapter 10.

An LTI system can be described by its impulse response, and its output is produced by convolving the input with that response.

In Chapter 19, multipath gave that idea a physical wireless meaning.

A direct path plus one echo delayed by one symbol can be represented at the symbol rate by

$$
h=[1,0.5]
$$

The first coefficient represents the direct path. The second represents a copy delayed by one symbol and arriving with half the direct-path amplitude.

The receiver can therefore ask a natural question:

> **If the channel behaves like a filter, can another filter after it approximately undo the channel?**

That second filter is the equalizer.

If the channel impulse response is $h$ and the equalizer impulse response is $g$, their combined response is

$$
h*g
$$

Ideally, we would like the combination to behave approximately like an impulse:

$$
h*g\approx\delta
$$

Convolution with an impulse leaves the signal unchanged, so this gives the basic intuition behind channel inversion and zero-forcing equalization.

## 20.2 Experiment 20.1: Manually Undoing a Known Channel

Our first experiment deliberately gives the receiver an easier problem than it would have in a real radio.

We create the channel ourselves, so we know exactly what it is.

The main parameters are

| Parameter | Value |
|---|---:|
| Sample rate | `32000` samples/s |
| Symbol rate | `1000` symbols/s |
| Samples per symbol | `32` |
| RRC span | `8` symbols |
| RRC taps | `257` |
| RRC roll-off factor | `0.35` |
| Echo delay | `32` samples = 1 symbol |
| Echo gain | `0.5` |

The channel is built from a direct path and one delayed copy, as in Chapter 19.

![Manual channel equalization flowgraph](../figures/ch20/ch20-exp1-manual-equalization-flowgraph.png)

After matched filtering and symbol-rate sampling, the channel is approximately

$$
r[k]=s[k]+0.5s[k-1]
$$

so the symbol-rate channel is

$$
h=[1,0.5]
$$

### How Did the Receiver Know the Channel?

It did not discover it.

We created the direct path with gain 1 and the delayed path with gain 0.5 at exactly one symbol of delay. As experiment designers, we therefore know the channel in advance.

That is intentionally unrealistic.

A real receiver does not normally begin with exact knowledge of the number of propagation paths, their delays, amplitudes, phases, or how quickly those quantities may change.

For this experiment, however, the known channel lets us isolate one question: if the channel were known perfectly, what receiver filter would compensate for it?

### Channel Taps and Equalizer Taps Are Different

The channel taps

```text
[1, 0.5]
```

describe the distortion introduced before the equalizer.

The equalizer taps

```text
[1, -0.5, 0.25, -0.125, ...]
```

describe the receiver filter used to compensate for that distortion.

They represent different systems and should not be confused.

## 20.3 Building the Inverse One Tap at a Time

Instead of writing down the inverse immediately, we build it progressively.

Start with

$$
g=[1]
$$

Then

$$
[1,0.5]*[1]=[1,0.5]
$$

Nothing has changed. The one-symbol echo remains.

Now use

$$
g=[1,-0.5]
$$

The combined response becomes

$$
[1,0.5]*[1,-0.5]=[1,0,-0.25]
$$

The original one-symbol contribution has disappeared, but a smaller residual remains two symbols later.

The equalizer output is therefore

$$
y[k]=s[k]-0.25s[k-2]
$$

Add another tap:

$$
g=[1,-0.5,0.25]
$$

Now

$$
[1,0.5]*[1,-0.5,0.25]=[1,0,0,0.125]
$$

so

$$
y[k]=s[k]+0.125s[k-3]
$$

With four equalizer taps,

$$
[1,0.5]*[1,-0.5,0.25,-0.125]=[1,0,0,0,-0.0625]
$$

and with five,

$$
[1,0.5]*[1,-0.5,0.25,-0.125,0.0625]=[1,0,0,0,0,0.03125]
$$

The residual contribution therefore follows

$$
0.5\rightarrow0.25\rightarrow0.125\rightarrow0.0625\rightarrow0.03125
$$

For this particular channel, every added term halves the magnitude of the remaining contribution and changes its sign.

That pattern is not universal. It occurs because the echo coefficient in this example is exactly 0.5.

![Progressive manual equalization](../figures/ch20/ch20-exp1-progressive-manual-equalization.png)

With only `[1]`, no correction is applied.

With `[1, -0.5]`, the strongest one-symbol contribution is cancelled, although a weaker residual remains.

As more taps are added, the residual channel memory becomes smaller and the received pattern moves closer to four QPSK clusters.

The five-tap result is not mathematically perfect because the exact inverse is not a five-tap FIR filter.

### Why Does the Inverse Continue Indefinitely?

The channel transfer function is

$$
H(z)=1+0.5z^{-1}
$$

The ideal inverse is

$$
G(z)=\frac{1}{1+0.5z^{-1}}
$$

which can be expanded as

$$
G(z)=1-0.5z^{-1}+0.25z^{-2}-0.125z^{-3}+0.0625z^{-4}-\cdots
$$

The exact inverse therefore has infinitely many terms.

Our finite equalizer is an approximation.

Five taps are a design choice, not a special property of the channel. A longer equalizer can approximate this inverse more closely, but it also requires more computation and more coefficients to determine or adapt.

### Zero-Forcing Intuition

The manual equalizer gives a simple form of zero-forcing intuition.

We choose coefficients that drive unwanted channel-memory terms toward zero.

This idea also has a limitation. If a channel strongly suppresses some frequency components, an inverse filter may require very large gain in those regions. That can amplify noise as well as the desired signal.

We will return to that limitation later in the chapter.

## 20.4 The Real Problem: The Correct Taps Are Unknown

Experiment 20.1 succeeded because we already knew the answer.

We created

$$
h=[1,0.5]
$$

and calculated a useful inverse approximation ourselves.

A practical receiver normally does not know the correct equalizer taps in advance.

The next question is therefore:

> **Can the equalizer adjust its own coefficients automatically?**

This is the purpose of an **adaptive equalizer**.

Instead of choosing the taps once and keeping them fixed, the receiver uses an error signal to update them repeatedly.

Let the equalizer output be $y[k]$ and the desired symbol be $d[k]$. The error is

$$
e[k]=d[k]-y[k]
$$

The difficult part is obtaining $d[k]$.

At first, the receiver does not know the transmitted payload sequence. It does, however, know the valid QPSK constellation points.

That allows **decision-directed adaptation**.

The equalizer output is mapped to the nearest valid QPSK point. That decision is used as an approximate desired symbol, and the resulting error is used to update the equalizer taps.

## 20.5 Experiment 20.2: Adaptive LMS Equalization

We keep the same one-symbol echo channel but replace the manually designed FIR equalizer with GNU Radio's **Linear Equalizer** and an **LMS Adaptive Algorithm**.

The adaptive experiments use normalized QPSK.

Let

$$
a=\frac{1}{\sqrt{2}}\approx0.70710678
$$

The four constellation points are

$$
(a,-a),\;(-a,a),\;(-a,-a),\;(a,a)
$$

or, in complex notation,

$$
\{a-ja,\;-a+ja,\;-a-ja,\;a+ja\}
$$

Each point has unit magnitude.

The important experiment settings are

| Parameter | Value |
|---|---:|
| Echo gain | `0.5` |
| Echo delay | `32` samples |
| Linear Equalizer taps | `5` |
| Input samples per symbol | `1` |
| Adaptive algorithm | LMS |
| Training sequence | none |
| QPSK constellation magnitude | `1` |

![Adaptive LMS equalization flowgraph](../figures/ch20/ch20-exp2-adaptive-lms-flowgraph.png)

With an empty training sequence, the equalizer begins without an explicit known-symbol training interval. Its adaptation is therefore decision-directed.

The **Linear Equalizer is the filter** whose coefficients change. The **LMS Adaptive Algorithm** supplies the rule used to change those coefficients.

## 20.6 What Does the QPSK Constellation Object Do?

Decision-directed LMS needs to know what valid symbol decisions look like.

GNU Radio's **Constellation Rect. Object** provides that information.

The object used in this experiment contains

```text
Symbol Map:
[0, 1, 2, 3]

Constellation Points:
[ 0.707-0.707j,
 -0.707+0.707j,
 -0.707-0.707j,
  0.707+0.707j ]

Rotational Symmetry: 4
Real Sectors: 2
Imaginary Sectors: 2
```

The most important field is the list of constellation points.

It tells the adaptive receiver that valid QPSK decisions lie near

$$
(\pm0.707,\pm0.707)
$$

The equalizer output can then be associated with the nearest valid point, giving the decision-directed reference used to form the error.

The constellation object is therefore not merely a plotting configuration. It is part of the receiver algorithm.

### Why Use 0.707 Instead of 1?

Both

$$
(\pm1,\pm1)
$$

and

$$
(\pm0.707,\pm0.707)
$$

have the same QPSK geometry and phases.

The difference is normalization.

For the point $1+j$,

$$
|1+j|^2=2
$$

For the normalized point

$$
\frac{1}{\sqrt{2}}+j\frac{1}{\sqrt{2}}
$$

we obtain

$$
\left|\frac{1}{\sqrt{2}}+j\frac{1}{\sqrt{2}}\right|^2=1
$$

The normalized QPSK symbols therefore have unit energy in this symbol-domain representation.

The transmitter and adaptive decision reference use the same normalized constellation so that the alphabet presented to the channel matches the alphabet expected by the equalizer.

## 20.7 What Does the LMS Step Size Mean?

The LMS step size is written as

$$
\mu
$$

It controls how strongly each error observation changes the equalizer coefficients.

A representative complex LMS update can be written as

$$
w_i[k+1]=w_i[k]+\mu e[k]x^*[k-i]
$$

with the exact placement of complex conjugation depending on the filter and error convention used by the implementation.

The main idea is unchanged: $\mu$ scales the tap update.

If

$$
\mu=0
$$

the coefficients do not adapt.

That is exactly what the experiment demonstrates.

![LMS with adaptation disabled and enabled](../figures/ch20/ch20-exp2-lms-no-adaptation-vs-adaptation.png)

With $\mu=0$, the adaptive output remains at the equalizer's initial zero-output state in this setup.

With

```text
μ = 0.005
```

adaptation is enabled and the received multipath structure contracts toward the four normalized QPSK points.

We also tested several nonzero step sizes. Within the retained range, the equalizer converged to essentially the same steady-state QPSK constellation. The clearest visible difference was convergence speed: smaller values adapted more slowly, while larger values converged more quickly.

This does not mean that arbitrarily large $\mu$ is safe. Adaptive-filter theory predicts a tradeoff among convergence speed, residual error, and stability. The tested range simply did not produce visible instability in this experiment.

A practical GNU Radio detail is also worth recording. We initially considered changing $\mu$ with a QT GUI Range while the flowgraph was running, but the Adaptive Algorithm object's step size did not update reliably through that runtime control in this setup.

The tested values were therefore changed manually between runs while the rest of the flowgraph remained unchanged.

## 20.8 Decision-Directed Adaptation and Acquisition

Decision-directed adaptation contains an obvious weakness.

The equalizer is not yet correct when adaptation begins. Its initial output may therefore be badly distorted.

If the receiver makes the wrong QPSK decision, the desired symbol used to form the error is also wrong. The resulting update can then move the equalizer in an unhelpful direction.

This creates an acquisition problem.

Once the equalizer is already close to the correct solution, decision-directed adaptation can work well because most symbol decisions are reliable. Before convergence, however, relying entirely on those decisions can be risky.

A common solution is to begin with a **training sequence**.

## 20.9 Experiment 20.3: Training-Assisted Equalization

A training sequence is a predetermined sequence of symbols known to both transmitter and receiver.

The receiver does not know the payload data in advance, but it does know what the training symbols should be.

During the training interval, the LMS error can therefore use known desired symbols instead of decision-directed guesses.

The transmitted frame in this experiment is

```text
8 known training symbols
256 payload symbols
```

and the complete frame repeats because the Vector Source uses `Repeat = Yes`.

This repeated structure is convenient for the experiment. In a practical system, training may appear at the beginning of every packet, once during acquisition, periodically during a long transmission, or in the form of pilot symbols.

There is no universal rule that training is transmitted only once.

### Constructing the Frame

Let

$$
a=0.70710678
$$

The eight-symbol training sequence is

```python
training_symbols = [
    a+1j*a,
    a-1j*a,
    -a+1j*a,
    -a-1j*a,
    a-1j*a,
    -a-1j*a,
    a+1j*a,
    -a+1j*a
]
```

This exact sequence was chosen for the experiment. It was not derived from the channel.

Its purpose is to provide a fixed known QPSK sequence containing all four constellation states.

The payload is a deterministic pseudo-random sequence of 256 QPSK symbols:

```python
import numpy as np

a = 0.70710678
qpsk_points = [a-1j*a, -a+1j*a, -a-1j*a, a+1j*a]
payload_indices = list(np.random.default_rng(20).integers(0, 4, 256))
payload_symbols = [qpsk_points[i] for i in payload_indices]
frame_symbols = training_symbols + payload_symbols
```

The seed `20` has no communications significance. It simply makes the experiment reproducible.

The receiver is given `training_symbols`, but it is not given `payload_symbols` as known data.

![Training-assisted equalization flowgraph](../figures/ch20/ch20-exp3-training-assisted-equalization-flowgraph.png)

The important receiver stages are

**RX Matched RRC → Keep 1 in N → Correlation Estimator → Linear Equalizer → Constellation Sink**

The Correlation Estimator locates the known sequence. The Linear Equalizer then uses the training interval to adapt its taps.

## 20.10 Why Does the Receiver Need a Correlation Estimator?

Knowing the training symbols is not enough.

The receiver also needs to know where the training sequence begins in the received stream.

The two receiver tasks are different:

- **Correlation Estimator:** find where the known sequence appears.
- **Linear Equalizer:** use the known symbols to update the equalizer taps.

This connects directly to Chapter 11, where correlation was introduced as a method for finding a known pattern in a received signal.

The Correlation Estimator settings used here are

```text
Symbols: training_symbols
Samples per Symbol: 1
Tag marking delay: 1
Threshold: 0.5
Threshold Method: Absolute
```

The block produces correlation-related tags for downstream processing. In this experiment, the Linear Equalizer uses the `corr_est` tag to identify the training interval.

The Correlation Estimator does not equalize the channel. It only helps locate the known sequence.

## 20.11 The Meaning of the Correlation Threshold

The Correlation Estimator continuously measures how strongly the incoming sequence resembles the known training pattern.

The threshold determines how strong that match must be before the receiver declares that the training sequence has been found.

A high threshold is conservative. It requires a strong match but may miss a distorted training sequence.

A low threshold is more permissive, but ordinary payload or noise is then more likely to be mistaken for training.

We first tested

```text
Threshold = 0.9
```

with the multipath-distorted training sequence.

The equalizer output remained essentially at the origin because the receiver did not obtain a useful training trigger.

Reducing the threshold to

```text
Threshold = 0.5
```

allowed the training process to begin and the equalizer recovered four QPSK regions.

![Correlation threshold comparison](../figures/ch20/ch20_exp3_correlation_threshold_comparison.png)

The conclusion is not that `0.5` is the correct threshold for QPSK.

It is only the value that worked better for this training sequence and this channel condition.

In a practical receiver, the correlation statistic is studied when the sequence is absent and when it is present. The threshold can then be chosen from requirements such as acceptable false-alarm probability and desired detection probability.

The manual sweep here is an educational experiment that makes the tradeoff visible.

## 20.12 Detection Is Not the Same as Alignment

Even when the receiver detects the correct training sequence, the downstream equalizer still needs the training-start information to line up with the correct symbol.

This is the purpose of the **Tag marking delay**.

We tested small integer values including 0, 1, 2, and 3.

Values 1 and 2 gave much better equalizer behaviour than 0 or 3, and the final configuration uses

```text
Tag marking delay: 1
```

The important lesson is not the number 1.

Detection and alignment are separate requirements.

The correct tag offset depends on the receiver architecture, filter delays, correlation convention, sample-rate relationship, and block implementation.

A practical receiver would determine the intended alignment from the design and verify it through simulation or measurement.

## 20.13 From Acquisition to Tracking

The Linear Equalizer uses

```text
Adapt After Training: True
```

During the training interval, the desired symbols are known.

After training ends, the payload is no longer known in advance. The receiver therefore continues in decision-directed mode.

This gives us two useful terms.

**Acquisition** is the process of reaching a useful initial equalizer state.

**Tracking** is the continued adjustment used to follow changes after acquisition.

This distinction also explains why training cannot always be sent once and forgotten forever. If the propagation channel changes, previously learned coefficients may become less appropriate.

A system can respond by continuing decision-directed tracking, inserting periodic training or pilots, or using another channel-tracking strategy.

## 20.14 What If the Training Sequence Is Noisy?

A real training sequence travels through the same channel as the payload.

The receiver knows what was transmitted, but the received training symbols are still distorted and noisy.

For example, the transmitter may send

$$
d[k]=0.707+j0.707
$$

while the receiver observes a different complex value.

That difference is exactly what makes training useful. The receiver knows what should have arrived and can use the error to adapt.

Noise still limits the process.

The equalizer should learn repeatable channel distortion, not the particular random noise sample added to one observation. Multiple known training symbols provide more evidence about the systematic channel behaviour.

Sufficiently strong noise can nevertheless make equalizer adaptation less reliable and can even make detection of the training sequence difficult.

Training provides useful reference information, not perfect information.

## 20.15 How Long Should the Training Sequence Be?

The retained experiment uses 8 training symbols and 256 payload symbols.

The training overhead is

$$
\frac{8}{8+256}\approx3.0\%
$$

We also tested 32 training symbols with the same 256-symbol payload.

The overhead then becomes

$$
\frac{32}{32+256}\approx11.1\%
$$

Longer training gives the equalizer more known-symbol updates during acquisition, but it also uses more transmission time for non-payload symbols.

In this experiment, increasing the training interval from 8 to 32 symbols did not produce a dramatic improvement in the observed steady-state constellation.

That result is useful.

Longer training can improve acquisition opportunity, but it does not guarantee that the steady-state constellation will continue to become tighter. With `Adapt After Training = True`, most of the payload interval is still handled in decision-directed mode.

We therefore retained the shorter eight-symbol sequence.

## 20.16 Stronger Echoes Make Equalization Harder

Training improves the quality of the initial reference information, but it does not make the physical channel disappear.

We keep the equalizer configuration fixed and vary the echo strength.

The one-symbol channel is

$$
r[k]=s[k]+a\,s[k-1]
$$

with

$$
a=0.2,\;0.5,\;0.8
$$

![Training-assisted LMS equalization for increasing echo gain](../figures/ch20/ch20_exp3_training_assisted_lms_echo_gain_comparison.png)

At `echo_gain = 0.2`, the delayed path is weak and the equalizer has an easier task.

At `echo_gain = 0.5`, the previous symbol contributes half the direct-path amplitude. The unequalized multipath structure is clear, but the adaptive equalizer still provides useful compensation.

At `echo_gain = 0.8`, the delayed symbol contributes almost as strongly as the direct path. Four equalized QPSK regions are still visible, but the residual spread is much larger.

This is not increased random noise.

The stronger echo is a stronger delayed copy of the same transmitted waveform.

The experiment therefore shows that equalization does not make channel severity irrelevant.

## 20.17 How Are Receiver Parameters Chosen?

Several parameters were changed manually in this chapter:

- LMS step size;
- equalizer length;
- correlation threshold;
- tag marking delay;
- training length.

A practical receiver is not normally designed by adjusting each value until a constellation happens to look good.

Different parameters come from different design considerations.

Tag alignment is largely determined by the receiver architecture and processing delays.

A correlation threshold can be chosen from false-alarm and missed-detection requirements.

The LMS step size and equalizer length depend on convergence speed, tracking ability, residual error, expected channel memory, computational cost, and stability.

Training length trades acquisition opportunity against overhead.

Simulation, laboratory measurements, and field testing are then used to verify or refine the design.

The manual sweeps in this chapter are useful because they expose what each parameter controls before those choices are hidden inside a more complete receiver.

## 20.18 Experiment 20.4: Equalization in the Presence of Noise

So far, the equalizer has been compensating for structured multipath distortion.

We now add something fundamentally different: random Gaussian noise.

The approximate symbol-rate model becomes

$$
r[k]=s[k]+0.5s[k-1]+w[k]
$$

The term

$$
0.5s[k-1]
$$

has predictable structure because it comes from channel memory.

The term

$$
w[k]
$$

is random.

The equalizer can learn a useful correction for the repeatable channel structure. It cannot know the particular random noise sample added to each symbol.

The final flowgraph adds a complex Gaussian Noise Source to the same direct-plus-delayed channel.

![Adaptive LMS equalization with noise flowgraph](../figures/ch20/ch20-exp4-equalization-with-noise-flowgraph.png)

The important settings are

| Parameter | Value |
|---|---:|
| Echo gain | `0.5` |
| Echo delay | `32` samples |
| Linear Equalizer taps | `5` |
| Input samples per symbol | `1` |
| LMS step size | `0.01` |
| Noise amplitudes tested | `0`, `0.3`, `0.8` |

The Noise Source amplitude is a relative simulation parameter. It is not itself an SNR value in dB.

![Effect of additive Gaussian noise on adaptive LMS equalization](../figures/ch20/ch20-exp4-lms-equalization-noise-comparison.png)

With `Noise Amplitude = 0`, the received constellation shows the familiar structured multipath pattern, and LMS reduces it toward four QPSK regions.

At `Noise Amplitude = 0.3`, the received states become fuzzy. The equalizer still removes much of the structured channel memory, but random spread remains in the equalized constellation.

At `Noise Amplitude = 0.8`, both the unequalized and equalized constellations are much more dispersed. Four equalized regions remain visible, but the receiver is operating under a much more difficult condition.

Noise also affects the adaptation itself. LMS forms updates from noisy observations, and decision-directed adaptation becomes less reliable when noise pushes samples toward the wrong decision regions.

The central lesson is:

> **Equalization is not a general-purpose signal cleaner. It compensates predictable channel structure; it cannot simply remove independent random noise.**

## 20.19 What Equalization Can and Cannot Fix

Equalization mainly addresses channel memory and waveform distortion caused by multipath.

It does not automatically correct every impairment introduced in Chapter 19.

| Receiver problem | Appropriate response |
|---|---|
| multipath / channel memory | equalization |
| carrier-frequency offset | carrier synchronization |
| carrier-phase error | carrier / phase recovery |
| incorrect symbol-sampling instant | timing recovery |
| independent random noise | cannot simply be inverted |

A receiver can be well equalized and still have a rotating constellation because of carrier-frequency offset.

It can have correct carrier phase but still sample at the wrong time.

It can have correct timing and equalization but still make errors because the noise is too strong.

The eye-versus-constellation distinction remains important here. Equalization can reduce ISI and improve the waveform around symbol decisions, but an open eye does not guarantee a stationary or correctly oriented constellation if carrier synchronization is still poor.

Equalization is therefore one part of receiver recovery, not the entire receiver.

## 20.20 Equalization Without Explicit Channel Estimation

Experiment 20.1 raises an obvious question: how does the receiver know the channel?

There are two broad approaches.

One is to estimate the channel explicitly and then design a correction from that estimate.

The other is to adapt the equalizer directly from an error signal without first producing a separate channel estimate.

Experiments 20.2 and 20.3 follow the second approach.

LMS does not require us to provide

```text
h = [1, 0.5]
```

and then ask the receiver to calculate its inverse.

Instead, it changes the equalizer coefficients according to the observed error. Training symbols improve the quality of that error during acquisition.

The distinction is useful:

> **Channel estimation asks what the channel is. Adaptive equalization asks what correction reduces the resulting error.**

The two ideas are related, but they are not identical.

## 20.21 GNU Radio Toolbox

Several GNU Radio blocks and objects take on new receiver roles in this chapter.

| GNU Radio Block or Object | Role in This Chapter |
|---|---|
| Decimating FIR Filter | implements the manually chosen equalizer in Experiment 20.1 |
| Linear Equalizer | adaptive FIR equalizer whose coefficients change during operation |
| Adaptive Algorithm (LMS) | supplies the coefficient-update rule |
| Constellation Rect. Object | defines the normalized QPSK decision alphabet |
| Correlation Estimator | locates the known training sequence |
| Noise Source | adds complex Gaussian noise to test equalization under random disturbance |
| Keep 1 in N | provides the fixed symbol-rate samples used by the equalizer experiments |

### Decimating FIR Filter

In Experiment 20.1, the Decimating FIR Filter uses

```text
Decimation: 1
```

so it acts as an ordinary FIR filter.

Its role is different from the filtering roles used earlier in the book. The taps are chosen to compensate for channel memory rather than to perform pulse shaping or matched filtering.

### Linear Equalizer

The Linear Equalizer is the adaptive FIR filter.

The important settings in Experiment 20.2 are

```text
Num. Taps: 5
Input Samples per Symbol: 1
Adaptive Algorithm Object: lms
Training Sequence: []
Adapt After Training: True
```

With an empty training sequence, adaptation is decision-directed.

When a training sequence is supplied, the equalizer can use the known symbols during acquisition and continue decision-directed tracking afterward.

### Adaptive Algorithm (LMS)

The LMS object determines how the equalizer taps change.

The step size $\mu$ controls the strength of each update.

A smaller step usually gives more cautious adaptation. A larger step can converge more quickly but also increases the risk of larger residual error or instability.

### Constellation Rect. Object

The Constellation Rect. Object defines the valid normalized QPSK symbols.

It is part of the decision-directed receiver algorithm, not merely a display object.

### Correlation Estimator

The Correlation Estimator searches the incoming symbol stream for the known training sequence.

In the retained configuration,

```text
Symbols: training_symbols
Samples per Symbol: 1
Tag marking delay: 1
Threshold: 0.5
Threshold Method: Absolute
```

Its job is detection and tagging. It does not equalize the signal.

## 20.22 Explore Further

The equalization experiments are well suited to prediction before execution.

1. In Experiment 20.1, shorten the manual equalizer to two taps and predict the remaining channel response.

2. Replace the manual coefficient `-0.5` with `-0.3` and compare the resulting residual distortion.

3. Keep the one-symbol echo fixed and compare several nonzero LMS step sizes. Observe convergence speed as well as the final constellation.

4. Change the number of equalizer taps while keeping the channel unchanged. Compare residual distortion, convergence behaviour, and computational complexity.

5. In the training-assisted experiment, compare correlation thresholds around the retained value and note the difference between missed training and false or unreliable detections.

6. Change the tag marking delay by one symbol and observe how correct detection can still lead to poor training alignment.

7. Compare 8 and 32 training symbols while keeping the payload length fixed. Relate any acquisition improvement to the change in overhead.

8. With noise set to zero, increase `echo_gain`. Then remove the echo and increase only the noise. The two tests separate structured channel memory from random disturbance.

9. After equalization, deliberately introduce carrier-frequency offset. Observe that the constellation can still rotate even though the multipath correction is working.

## 20.23 What We Learned

Equalization is a receiver correction for predictable channel distortion, especially channel memory and ISI caused by multipath.

For the simple one-symbol channel

$$
h=[1,0.5]
$$

we first assumed that the channel was known and constructed a finite inverse approximation manually.

The channel taps and equalizer taps describe different systems.

For this particular channel, adding inverse-filter terms progressively reduced the residual contribution from 0.5 to 0.25, 0.125, 0.0625, and 0.03125. The exact inverse is infinite, so a finite FIR equalizer is only an approximation.

The adaptive experiments removed the assumption that we already knew the correct equalizer taps.

GNU Radio's Linear Equalizer is the filter whose coefficients change. LMS is the adaptation rule that controls those changes.

The step size $\mu$ controls how strongly the coefficients respond to each error observation. With $\mu=0$, the equalizer does not adapt. Within the nonzero range retained in the experiment, the clearest difference was convergence speed.

Decision-directed adaptation uses the known QPSK decision alphabet rather than the unknown payload sequence itself.

That creates an acquisition problem when the equalizer is initially poor. A known training sequence provides reliable reference symbols during acquisition.

The receiver must still detect and align that sequence. The Correlation Estimator performs the detection task, while the tag marking delay affects where the training interval is marked for downstream processing.

A threshold that worked in one experiment is not a universal receiver constant. Practical thresholds depend on the statistics of the detector and on false-alarm and missed-detection requirements.

Training length also involves a tradeoff. More training gives more known-symbol updates but increases overhead. In the retained experiment, increasing the training interval from 8 to 32 symbols did not dramatically improve the steady-state constellation.

Stronger multipath made the equalizer's task harder because more energy from the previous symbol entered the current observation.

Random Gaussian noise created a different limitation. Equalization can compensate for repeatable channel structure, but it cannot predict and invert independent random noise.

Equalization also does not replace carrier recovery or timing recovery.

The central idea is that an equalizer is not a mysterious block that cleans a constellation. It is a filter trying to compensate for a physical channel, and its success depends on the channel, the available reference information, the adaptation rule, and the remaining noise.

## 20.24 Connecting to the Next Chapter

Chapter 19 separated channel impairments from receiver corrections.

This chapter addressed one of those receiver problems: channel memory caused by multipath.

Another major impairment remains.

A carrier-frequency offset causes the QPSK constellation to rotate because the transmitter and receiver carrier references do not agree.

An equalizer does not solve that problem.

The receiver therefore needs a mechanism that estimates carrier phase or frequency error and continuously corrects it.

That leads to **Chapter 21: PLL and Carrier Synchronization**.

We will develop the carrier-recovery problem from phase error and feedback, then move into phase-locked loops, acquisition and tracking, the Costas Loop, and related carrier-synchronization methods.