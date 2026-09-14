# Chapter 13: Amplitude Modulation

## Main Question

**How can information be carried by changing the amplitude of a carrier, and what do we gain or lose when we transmit the carrier and one or both sidebands?**

Chapter 12 introduced modulation by multiplying a baseband message by a carrier. For a single-tone message, that operation produced two translated components at

$$
f_c-f_m
$$

and

$$
f_c+f_m.
$$

There was no separate spectral line at the carrier frequency itself.

We called that signal **double-sideband suppressed-carrier**, or **DSB-SC**.

That immediately raises a useful question. If DSB-SC already moves the message to the frequency region we want, why would a transmitter deliberately send the carrier as well?

The answer appears when we look at the receiver.

Conventional amplitude modulation spends transmitter power on a carrier, but that carrier makes a very simple form of demodulation possible. From there, another set of trade-offs appears. We can suppress the carrier to save power, suppress one sideband to save bandwidth, or keep only part of the unwanted sideband when practical filtering becomes difficult.

Rather than treating AM, DSB-SC, SSB, and VSB as unrelated definitions, we will build them as variations of the same spectral idea.

## 13.1 Experiment 13.1: Building Conventional AM

Consider a carrier

$$
c(t)=A_c\cos(2\pi f_ct).
$$

Its amplitude, frequency, and phase are constant.

Amplitude modulation makes the carrier amplitude vary with the message. For a normalized message \(m(t)\), conventional AM can be written as

$$
s(t)=A_c[1+\mu m(t)]\cos(2\pi f_ct),
$$

where \(\mu\) is the **modulation index**.

The factor

$$
1+\mu m(t)
$$

controls the instantaneous carrier amplitude.

For the first experiment, use a 1 kHz cosine message and a 10 kHz carrier:

$$
f_m=1\text{ kHz}
$$

and

$$
f_c=10\text{ kHz}.
$$

The sample rate is

$$
f_s=64\text{ kS/s}.
$$

The flowgraph follows the AM equation directly. The message amplitude is controlled by the QT GUI Range `mu`, a constant 1 is added, and the result is multiplied by the carrier.

![Experiment 13.1 flowgraph for generating conventional AM and varying the modulation index](../figures/ch13/ch13-exp1-am-flowgraph.png)

Use the main parameters:

| Parameter | Value |
|---|---:|
| Sample rate | 64 kS/s |
| Message frequency | 1 kHz |
| Carrier frequency | 10 kHz |
| Carrier amplitude | 1 |
| DC term before multiplication | 1 |

Configure the QT GUI Range as:

```text
ID: mu
Label: Modulation Index (μ)
Default Value: 500m
Start: 0
Stop: 1.5
Step: 100m
```

The message Signal Source uses `mu` as its amplitude, so the signal before the final Multiply block is

$$
1+\mu\cos(2\pi f_mt).
$$

Multiplying by the 10 kHz carrier produces conventional AM.

### Watching the Envelope Change

At

$$
\mu=0.1,
$$

the carrier amplitude changes only slightly.

![Conventional AM at a low modulation index](../figures/ch13/ch13-exp1-am-mu-01.png)

At

$$
\mu=0.5,
$$

the variation is much easier to see.

![Conventional AM at a modulation index of 0.5](../figures/ch13/ch13-exp1-am-mu-05.png)

The rapid oscillation is still the 10 kHz carrier. The slower outer shape follows the 1 kHz message.

That outer shape is the **envelope**.

### What Appears in the Spectrum?

For a single-tone message,

$$
m(t)=\cos(2\pi f_mt),
$$

so

$$
s(t)=A_c[1+\mu\cos(2\pi f_mt)]\cos(2\pi f_ct).
$$

Expanding,

$$
s(t)=A_c\cos(2\pi f_ct)+A_c\mu\cos(2\pi f_mt)\cos(2\pi f_ct).
$$

Using the product-to-sum identity,

$$
s(t)=A_c\cos(2\pi f_ct)+\frac{A_c\mu}{2}\cos[2\pi(f_c-f_m)t]+\frac{A_c\mu}{2}\cos[2\pi(f_c+f_m)t].
$$

The positive-frequency spectrum therefore contains three components:

$$
f_c-f_m,\qquad f_c,\qquad f_c+f_m.
$$

For our experiment,

$$
9\text{ kHz},\qquad10\text{ kHz},\qquad11\text{ kHz}.
$$

The middle component is the carrier. The two outer components are the lower and upper sidebands.

The waveform is real-valued, so the spectrum also contains the corresponding conjugate-symmetric negative-frequency components.

### What Does the Modulation Index Actually Change?

For our normalized cosine message, the envelope-controlling factor is

$$
1+\mu\cos(2\pi f_mt).
$$

Its maximum value is

$$
1+\mu
$$

and its minimum is

$$
1-\mu.
$$

That gives three useful operating regions.

For

$$
0<\mu<1,
$$

the envelope remains positive.

At

$$
\mu=1,
$$

the minimum reaches zero.

![Conventional AM at 100 percent modulation](../figures/ch13/ch13-exp1-100-percent-modulation.png)

This is 100% modulation.

For

$$
\mu>1,
$$

the envelope-controlling factor becomes negative during part of the message cycle.

![Overmodulated conventional AM at a modulation index of 1.5](../figures/ch13/ch13-exp1-overmodulation.png)

This is **overmodulation**.

The transmitted waveform still exists mathematically, but the simple relationship between the visible envelope and the original message has broken down. That becomes important at the receiver.

## 13.2 Experiment 13.2: Recovering AM with an Envelope Detector

Chapter 12 recovered DSB-SC by multiplying the received signal by a synchronized local oscillator.

Conventional AM gives us another option.

Because the message appears in the envelope, we can build a simple digital envelope detector without generating a phase-synchronized carrier.

Our GNU Radio detector is:

`AM Signal → Abs → Low-Pass Filter → DC Blocker → Recovered Message`

![GNU Radio flowgraph for conventional AM envelope detection](../figures/ch13/ch13-exp2-envelope-detection-flowgraph.png)

Use the Low Pass Filter settings:

```text
Decimation: 1
Gain: 1
Sample Rate: samp_rate
Cutoff Frequency: 2k
Transition Width: 1k
Window: Hamming
```

Use the DC Blocker settings:

```text
Length: 32
Long Form: True
```

A two-input Time Sink compares the original and recovered messages.

### Clean Recovery

At

$$
\mu=0.5,
$$

the envelope never reaches zero.

![Clean envelope detection of conventional AM](../figures/ch13/ch13-exp2-envelope-detection-clean.png)

The recovered signal follows the original 1 kHz message.

Its amplitude and timing do not need to match the original trace exactly. Rectification, filtering, and DC removal introduce scaling and delay. The important observation is that the message waveform can be recovered without a synchronized 10 kHz local oscillator.

This is the main practical reason for transmitting the carrier in conventional AM.

The carrier costs power, but it buys receiver simplicity.

### Why the Abs Block Works Here

The Abs block performs full-wave rectification:

$$
y(t)=|x(t)|.
$$

The rapidly changing negative portions of the AM waveform are folded upward. The Low Pass Filter then removes most of the carrier-rate variation, leaving the slower envelope variation.

The DC Blocker removes the constant offset associated with the `1` in

$$
1+\mu m(t),
$$

so the recovered message is centered around zero.

This is a simple digital model of envelope detection. It is not intended to reproduce every detail of a physical diode-and-RC detector, but it exposes the same central idea.

### Why Overmodulation Breaks the Detector

For

$$
\mu\leq1,
$$

the envelope-controlling factor is nonnegative, so

$$
|1+\mu\cos(2\pi f_mt)|=1+\mu\cos(2\pi f_mt).
$$

Once

$$
\mu>1,
$$

that is no longer true.

Negative portions are folded upward by the absolute-value operation. The detector loses the sign information needed to reconstruct the original envelope faithfully.

To make the effect easy to see, the experiment was pushed to

$$
\mu=2.
$$

The envelope factor then ranges from

$$
-1
$$

to

$$
3.
$$

![Envelope-detector distortion during severe overmodulation at a modulation index of 2](../figures/ch13/ch13-exp2-overmodulation-distortion.png)

The recovered waveform is visibly distorted.

The value \(\mu=2\) is not a special threshold. Overmodulation begins immediately above \(\mu=1\). We use 2 only because the failure becomes unmistakable.

## 13.3 Experiment 13.3: Where Does the Transmitted Power Go?

Conventional AM makes the receiver simpler, but the carrier itself does not follow the changing message.

That raises an engineering question: how much transmitted power is spent on the carrier, and how much is in the information-bearing sidebands?

The experiment calculates those percentages directly from the modulation index while also showing the spectrum.

![GNU Radio flowgraph for visualizing conventional AM power distribution](../figures/ch13/ch13-exp3-am-power-flowgraph.png)

Use the same 64 kS/s sample rate, 1 kHz message, and 10 kHz carrier.

For this experiment, limit the modulation-index range to the normal non-overmodulated region:

```text
ID: mu
Label: Modulation Index (μ)
Default Value: 500m
Start: 0
Stop: 1
Step: 100m
```

The four Float Constant Sources use:

```text
Carrier Power: 100 / (1 + mu**2 / 2)
LSB Power: 50 * (mu**2 / 2) / (1 + mu**2 / 2)
USB Power: 50 * (mu**2 / 2) / (1 + mu**2 / 2)
Total Sideband Power: 100 * (mu**2 / 2) / (1 + mu**2 / 2)
```

These values feed the QT GUI Number Sink `AM Power Distribution (%)`.

### No Modulation

At

$$
\mu=0,
$$

the signal reduces to a pure carrier:

$$
s(t)=A_c\cos(2\pi f_ct).
$$

The display shows

$$
P_C=100\%
$$

and

$$
P_{LSB}=P_{USB}=0\%.
$$

![AM power distribution with no modulation](../figures/ch13/ch13-exp3-power-mu-0.png)

A transmitter can radiate a strong carrier while conveying none of our changing message.

### At \(\mu=0.5\)

The displayed values are approximately

$$
P_C=88.89\%,
$$

$$
P_{LSB}=P_{USB}=5.56\%,
$$

and

$$
P_{SB,\text{total}}=11.11\%.
$$

![AM power distribution at a modulation index of 0.5](../figures/ch13/ch13-exp3-power-mu-05.png)

Most of the transmitted power is still in the carrier.

### At 100% Modulation

At

$$
\mu=1,
$$

the displayed values are approximately

$$
P_C=66.67\%,
$$

$$
P_{LSB}=P_{USB}=16.67\%,
$$

and

$$
P_{SB,\text{total}}=33.33\%.
$$

![AM power distribution at 100 percent modulation](../figures/ch13/ch13-exp3-power-mu-1.png)

Even at the largest modulation index normally used with undistorted envelope detection for this normalized single-tone message, about two-thirds of the transmitted power remains in the carrier.

### Deriving the Result

For a sinusoid of peak amplitude \(A\) across a normalized \(1\,\Omega\) load,

$$
P=\frac{A^2}{2}.
$$

The carrier power is

$$
P_C=\frac{A_c^2}{2}.
$$

Each sideband has amplitude

$$
\frac{A_c\mu}{2},
$$

so each sideband power is

$$
P_{SB}=\frac{A_c^2\mu^2}{8}.
$$

The two sidebands together contain

$$
P_{SB,\text{total}}=\frac{A_c^2\mu^2}{4}=P_C\frac{\mu^2}{2}.
$$

The total transmitted power is

$$
P_T=P_C\left(1+\frac{\mu^2}{2}\right).
$$

If we define efficiency as the fraction of total transmitted power in the two sidebands,

$$
\eta=\frac{P_{SB,\text{total}}}{P_T}=\frac{\mu^2/2}{1+\mu^2/2}.
$$

For a single-tone message at

$$
\mu=1,
$$

we obtain

$$
\eta=\frac{1}{3}\approx33.3\%.
$$

So, for single-tone conventional AM at 100% modulation,

$$
\boxed{\eta_{\max}\approx33.3\%}.
$$

This 33.3% result is specific to the standard single-tone calculation used here. For a general message, the exact power distribution depends on the message's mean-square value and modulation conditions.

The engineering trade-off is still clear:

$$
\boxed{\text{simple envelope receiver}\longleftrightarrow\text{poor transmitter power efficiency}}.
$$

## 13.4 Experiment 13.4: Conventional AM vs DSB-SC

Chapter 12 already showed us how DSB-SC works. We can now compare it directly with conventional AM using the same 1 kHz message and 10 kHz carrier.

The only important difference is the added DC term.

For conventional AM:

`Message → Add 1 → Multiply by Carrier`

For DSB-SC:

`Message → Multiply by Carrier`

![GNU Radio flowgraph comparing conventional AM and DSB-SC](../figures/ch13/ch13-exp4-am-vs-dsbsc-flowgraph.png)

![Spectrum comparison between conventional AM and DSB-SC](../figures/ch13/ch13-exp4-am-vs-dsbsc-spectrum.png)

Conventional AM contains

$$
9\text{ kHz},\qquad10\text{ kHz},\qquad11\text{ kHz}.
$$

DSB-SC contains

$$
9\text{ kHz},\qquad11\text{ kHz},
$$

with no separate carrier component at 10 kHz.

Therefore,

$$
\boxed{\text{Conventional AM}=\text{Carrier}+\text{LSB}+\text{USB}}
$$

while

$$
\boxed{\text{DSB-SC}=\text{LSB}+\text{USB}}.
$$

### Suppressing the Carrier Saves Power, Not Bandwidth

If the baseband message has bandwidth \(B\), both conventional AM and DSB-SC occupy approximately

$$
2B
$$

of positive-frequency RF bandwidth.

Thus,

$$
BW_{AM}=BW_{DSB-SC}=2B.
$$

Suppressing the carrier improves power efficiency, but it does not reduce the occupied bandwidth.

The saving also comes with a receiver cost.

Conventional AM can use the simple envelope detector from Experiment 13.2 when the signal is not overmodulated.

DSB-SC normally requires coherent detection, which means the receiver must recreate or recover an oscillator with suitable frequency and phase accuracy.

| Property | Conventional AM | DSB-SC |
|---|---|---|
| Carrier | Transmitted | Suppressed |
| Sidebands | LSB + USB | LSB + USB |
| Bandwidth for message bandwidth \(B\) | \(2B\) | \(2B\) |
| Power efficiency | Poor | Better |
| Simple envelope detection | Yes, when conditions are suitable | No |
| Coherent detection | Not required for basic envelope detection | Required |

This leaves one more obvious question.

If the two sidebands contain mirrored versions of the same baseband information, do we really need to transmit both?

## 13.5 Experiment 13.5: From DSB-SC to SSB-SC

A single sinusoid is useful for locating modulation products, but it is not a convincing demonstration of bandwidth.

For the SSB experiment, use a three-tone message:

$$
m(t)=0.3\cos(2\pi500t)+0.3\cos(2\pi1000t)+0.3\cos(2\pi1500t).
$$

The message therefore contains components at 500 Hz, 1 kHz, and 1.5 kHz.

Multiplication by a 10 kHz carrier produces DSB-SC.

The positive-frequency lower-sideband components are

$$
8.5\text{ kHz},\qquad9\text{ kHz},\qquad9.5\text{ kHz},
$$

while the upper-sideband components are

$$
10.5\text{ kHz},\qquad11\text{ kHz},\qquad11.5\text{ kHz}.
$$

The ordering reveals an important detail.

The upper sideband maps

```text
500 Hz  -> 10.5 kHz
1 kHz   -> 11.0 kHz
1.5 kHz -> 11.5 kHz
```

while the lower sideband maps

```text
500 Hz  -> 9.5 kHz
1 kHz   -> 9.0 kHz
1.5 kHz -> 8.5 kHz
```

The LSB is frequency-reversed around the carrier. The two sidebands are mirrored representations of the same baseband information.

### Selecting the USB

Pass the DSB-SC signal through a Band Pass Filter that retains the upper sideband.

![GNU Radio flowgraph for generating and recovering SSB-SC from DSB-SC](../figures/ch13/ch13-exp5-dsbsc-to-ssbsc-flowgraph.png)

Use:

| Tone | Frequency | Amplitude |
|---|---:|---:|
| 1 | 500 Hz | 0.3 |
| 2 | 1 kHz | 0.3 |
| 3 | 1.5 kHz | 0.3 |

Configure the USB Band Pass Filter as:

```text
Decimation: 1
Gain: 1
Sample Rate: samp_rate
Low Cutoff Frequency: 10.3k
High Cutoff Frequency: 11.7k
Transition Width: 200
Window: Blackman-Harris
```

The USB-only waveform is then coherently mixed with the same 10 kHz carrier.

Use the recovery Low Pass Filter:

```text
Decimation: 1
Gain: 2
Sample Rate: samp_rate
Cutoff Frequency: 2k
Transition Width: 500
Window: Hamming
```

![DSB-SC, USB-only SSB-SC, and recovery of the original multi-tone message](../figures/ch13/ch13-exp5-ssbsc-generation-and-recovery.png)

The DSB-SC spectrum contains both three-tone sidebands.

After the Band Pass Filter, the positive-frequency spectrum contains the USB group around 10.5 to 11.5 kHz.

Because the output waveform is still real-valued, the spectrum also contains the required conjugate-symmetric negative-frequency mirror. That mirror is not the unwanted positive-frequency LSB returning. It is part of the Fourier representation of the real SSB waveform.

### Can One Sideband Recover the Whole Message?

The USB-only signal is coherently mixed with the 10 kHz carrier and low-pass filtered.

The recovered spectrum contains

$$
500\text{ Hz},\qquad1\text{ kHz},\qquad1.5\text{ kHz}.
$$

All three original message frequencies return.

Therefore,

$$
\boxed{\text{one complete sideband contains enough information to reconstruct the original message}}.
$$

The recovered time waveform does not need to lie exactly on top of the original trace. The signal has passed through a Band Pass Filter and a Low Pass Filter, both of which introduce delay and phase response. With several tones, changes in their relative phase alter the detailed time-domain waveform.

The recovered spectrum is therefore particularly useful here because it shows directly that all three message frequencies survived.

### Bandwidth

For a message bandwidth \(B\),

$$
BW_{DSB-SC}=2B
$$

while ideal SSB occupies

$$
BW_{SSB}=B.
$$

Suppressing the carrier saves transmitter power.

Suppressing one complete sideband saves additional power and reduces the required RF bandwidth by approximately half.

## 13.6 A Practical Filtering Lesson from SSB

The first SSB attempt did not suppress the unwanted sideband as strongly as expected.

Changing the Band Pass Filter window to **Blackman-Harris** produced much stronger rejection in the experiment.

That observation matters because real filters are not vertical walls.

A practical FIR filter has finite transition width and finite stopband attenuation. If the message contains energy close to DC, the two translated sidebands approach one another closely near the carrier. Separating them by filtering can then require a demanding filter.

This is why practical systems often speak of **sideband suppression** rather than pretending that an unwanted sideband has vanished perfectly.

The experiment connects directly to our earlier filter chapter. Transition width, window choice, and stopband attenuation are not cosmetic details. Here they determine how well a modulation scheme can be realised.

## 13.7 Generating SSB: Filter Method and Phasing Method

Our experiment used the most intuitive route:

`DSB-SC → Band-Pass Filter → SSB-SC`

This is the **filter method**.

It is conceptually simple, but it becomes difficult when important message frequencies lie very close to DC. In that case, the wanted and unwanted sidebands lie very close together around the carrier, demanding a sharp filter.

Another route is to arrange the signal phases so that one sideband reinforces while the other cancels.

This is the **phasing method**.

Let the real message be

$$
m(t).
$$

Its Hilbert transform is written as

$$
\hat{m}(t).
$$

The Hilbert transform provides the quadrature version needed to build the analytic signal

$$
m_a(t)=m(t)+j\hat{m}(t).
$$

Under a common convention, a positive-frequency cosine and its Hilbert transform form

$$
\cos(2\pi ft)+j\sin(2\pi ft)=e^{j2\pi ft}.
$$

The analytic signal ideally contains only the positive-frequency half of the original real signal spectrum.

Now shift it in frequency using

$$
m_a(t)e^{j2\pi f_ct}.
$$

Taking the real part gives

$$
s_{SSB}(t)=\operatorname{Re}\{m_a(t)e^{j2\pi f_ct}\}.
$$

Expanding,

$$
s_{SSB}(t)=m(t)\cos(2\pi f_ct)-\hat{m}(t)\sin(2\pi f_ct).
$$

With the corresponding opposite sign choice,

$$
s_{SSB}(t)=m(t)\cos(2\pi f_ct)+\hat{m}(t)\sin(2\pi f_ct),
$$

the opposite sideband is selected.

Which sign is labelled USB or LSB depends on the Hilbert-transform and oscillator sign convention. The useful idea is not to memorise a sign without context.

The useful idea is:

> **One quadrature combination reinforces one sideband while cancelling the other.**

This is where complex signals stop being an abstract mathematical convenience and become a practical communication tool.

### Why Analytic Signals Matter in SDR

Earlier chapters introduced I/Q signals, signed frequency, and complex mixing.

SSB brings those ideas together.

A real signal forces positive and negative frequencies into conjugate-symmetric pairs. An analytic complex representation lets us manipulate spectral direction explicitly.

That same idea appears far beyond SSB. Complex baseband is fundamental to modern SDR because it allows frequency translation, filtering, modulation, demodulation, and synchronization to be expressed cleanly in terms of I and Q.

## 13.8 SSB with Carrier, Reduced Carrier, and VSB

SSB does not have to mean complete carrier suppression.

A system may transmit:

- one sideband with no carrier;
- one sideband with a full carrier;
- one sideband with a reduced carrier reference.

Adding carrier power can make some receiver tasks easier, while suppressing it improves transmitter power efficiency.

The same trade-off we saw in conventional AM appears again.

### Vestigial Sideband

Ideal SSB can also create a difficult filtering problem when message energy extends close to DC.

A practical compromise is **vestigial sideband**, or **VSB**.

Instead of removing one sideband completely, VSB keeps one complete sideband and a small vestige of the other.

Its bandwidth is slightly greater than ideal SSB but smaller than full DSB.

Historically, VSB was important in analog television video transmission, where completely separating the sidebands near the carrier was inconvenient.

The broader engineering lesson is more important than that particular application:

> **Communication systems often choose a practical compromise rather than maximising one property in isolation.**

## 13.9 Comparing the Main AM Families

The AM family can now be compared as a set of trade-offs.

| Scheme | Carrier | Sidebands | Approx. Bandwidth for Message Bandwidth \(B\) | Main Trade-off |
|---|---|---|---:|---|
| Conventional AM | Full | LSB + USB | \(2B\) | Simple envelope reception, poor power efficiency |
| DSB-SC | Suppressed | LSB + USB | \(2B\) | Better power efficiency, coherent reception required |
| SSB-SC | Suppressed | LSB or USB | \(B\) | Better power and bandwidth efficiency, more demanding generation/reception |
| SSB with carrier or reduced carrier | Full or partial | One sideband | About \(B\) | Spend some carrier power for an easier reference |
| VSB | Depends on system | One full sideband + vestige | Slightly greater than \(B\) | Relax filtering while still saving bandwidth |

There is no modulation scheme that wins every category.

Conventional AM is attractive when receiver simplicity matters.

DSB-SC avoids spending power on a carrier but still transmits two sidebands.

SSB-SC removes the carrier and one redundant sideband, but the transmitter and receiver become more demanding.

VSB gives up some bandwidth efficiency to make the filter problem easier.

A useful engineering question is therefore not, “Which scheme is best?”

It is:

> **Which combination of bandwidth, transmitter power, receiver complexity, synchronization, and implementation cost fits the system?**

## 13.10 A Note About Bandwidth

Our early experiments used a single message sinusoid.

A perfect sinusoid appears as discrete spectral lines, so it is not the best example for thinking about occupied bandwidth.

The bandwidth advantage of SSB becomes clearer with a message that occupies a range of frequencies, which is why Experiment 13.5 used three message tones.

For a general real baseband message extending to \(B\), conventional AM and DSB-SC occupy approximately

$$
2B
$$

around the carrier on the positive-frequency RF side.

Ideal SSB occupies approximately

$$
B.
$$

The distinction is fundamental:

> **Suppressing the carrier saves power. Suppressing one sideband saves bandwidth.**

These are different improvements.

## 13.11 GNU Radio Toolbox

Most blocks in this chapter were already familiar. A few took on new roles.

| GNU Radio Block | Role in This Chapter |
|---|---|
| Abs | Full-wave rectification for the simple digital envelope detector |
| Low Pass Filter | Smooths the rectified envelope and later recovers baseband after coherent mixing |
| DC Blocker | Removes the residual DC component after envelope extraction |
| QT GUI Number Sink | Displays calculated carrier and sideband power percentages |
| Band Pass Filter | Selects one sideband in the SSB experiment |
| QT GUI Range | Changes the modulation index while the flowgraph is running |
| Multiply | Performs AM/DSB-SC modulation and coherent demodulation |
| Add / Add Const | Adds the carrier-producing DC term for conventional AM |

For the envelope detector, the key chain is

`Abs → Low Pass Filter → DC Blocker`

For SSB generation by the filter method, the key chain is

`DSB-SC → Band Pass Filter → One Sideband`

The SSB experiment also reinforced an old lesson: filter design matters. The selected window, transition width, and stopband attenuation directly affect unwanted-sideband suppression.

## 13.12 Explore Further

The experiments are useful to extend because most outcomes can be predicted before running the flowgraph.

1. Change the message frequency from 1 kHz to 2 kHz while keeping the carrier at 10 kHz. Predict the conventional AM sidebands before checking the Frequency Sink.

2. Move the modulation index through \(0.5\), \(1.0\), \(1.5\), and \(2.0\). Compare the transmitted waveform with the recovered envelope-detector output.

3. In the power experiment, compare the displayed carrier and sideband percentages with the theoretical formulas at several values of \(\mu\).

4. In Experiment 13.5, move the Band Pass Filter to the lower side of the carrier and retain the LSB instead of the USB. Verify that the same three baseband frequencies can still be recovered.

5. Compare the recovered USB and LSB time-domain waveforms. The message frequencies should agree even if the phase relationships are not identical.

6. Widen the SSB Band Pass Filter transition region or change its window. Observe how the residual unwanted-sideband energy changes.

7. Mistune the coherent-demodulation oscillator slightly. Observe how sensitive DSB-SC and SSB-SC recovery are to carrier-frequency error.

## 13.13 What We Learned

Conventional AM can be written as

$$
s(t)=A_c[1+\mu m(t)]\cos(2\pi f_ct).
$$

For a single-tone message, its positive-frequency spectrum contains a carrier, a lower sideband, and an upper sideband.

The modulation index controls the depth of the envelope.

For

$$
0<\mu<1,
$$

the envelope stays above zero.

At

$$
\mu=1,
$$

it just reaches zero.

For

$$
\mu>1,
$$

the waveform is overmodulated and a simple envelope detector becomes distorted.

We recovered conventional AM with

`Abs → Low Pass Filter → DC Blocker`

and saw why transmitting the carrier can simplify the receiver.

That convenience costs power. For the standard single-tone case at 100% modulation, only about

$$
33.3\%
$$

of the transmitted power is in the two sidebands, while about

$$
66.7\%
$$

remains in the carrier.

Suppressing the carrier gives DSB-SC. That improves power efficiency but does not reduce bandwidth:

$$
BW_{AM}=BW_{DSB-SC}=2B.
$$

The three-tone SSB experiment then showed that one complete sideband is enough to recover the whole message.

Ideal SSB therefore needs only

$$
BW_{SSB}=B.
$$

We also connected SSB to practical filtering, the Hilbert transform, analytic signals, I/Q processing, and the phasing method.

The AM family now forms a clear progression:

`Conventional AM → suppress carrier → DSB-SC → suppress one sideband → SSB-SC`

VSB adds another useful lesson: sometimes a small loss in theoretical efficiency makes a real implementation much easier.

The central theme is not a list of modulation names. It is the engineering trade-off between **power, bandwidth, receiver simplicity, synchronization, and implementation difficulty**.

## 13.14 Connecting to the Next Chapter

Throughout this chapter, the message affected the amplitude of the transmitted waveform.

But amplitude is only one property of a sinusoid.

A carrier also has frequency and phase.

That gives us another possibility: keep the carrier amplitude essentially constant and let the message move its instantaneous frequency above and below a center frequency.

That takes us to Chapter 14, **Frequency Modulation**.

There we will build FM experimentally, introduce frequency deviation and modulation index, examine the much richer FM spectrum, and recover the message again.