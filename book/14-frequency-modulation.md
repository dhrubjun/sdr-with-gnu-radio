# Chapter 14: Frequency Modulation

In Chapter 13, the message changed the amplitude of a carrier.

But amplitude is only one property of a sinusoid. A carrier also has frequency and phase.

That gives us another way to carry information: keep the carrier magnitude essentially constant and let the message change how quickly its phase rotates.

That is **frequency modulation**, or **FM**.

FM is familiar from broadcast radio, but the underlying idea is more general. It shows that information does not need to appear as a changing amplitude. It can be carried by the evolution of phase and instantaneous frequency.

In this chapter, we will build that idea experimentally. We will watch the carrier speed up and slow down, examine the sidebands that appear, introduce frequency deviation and modulation index, estimate bandwidth, recover the message, and then disturb the signal in two different ways.

The final pair of experiments answers an important question:

> **If FM does not carry information in amplitude, does that mean noise cannot affect it?**

## 14.1 Let the Frequency Carry the Message

Consider an unmodulated carrier:

$$
c(t)=A_c\cos(2\pi f_ct).
$$

Its amplitude is fixed at \(A_c\), and its frequency is fixed at \(f_c\).

With FM, the message controls the **instantaneous frequency**.

For a normalized message \(m(t)\), we can write

$$
f_i(t)=f_c+\Delta f\,m(t),
$$

where \(\Delta f\) is the peak frequency deviation.

Suppose

$$
f_c=10\text{ kHz}
$$

and

$$
\Delta f=2\text{ kHz}.
$$

If the message reaches \(+1\), the instantaneous frequency becomes

$$
f_i=12\text{ kHz}.
$$

If the message reaches \(-1\),

$$
f_i=8\text{ kHz}.
$$

At a message value of zero,

$$
f_i=10\text{ kHz}.
$$

The carrier therefore speeds up and slows down around its center frequency.

For a sinusoidal message,

$$
m(t)=\cos(2\pi f_mt),
$$

the instantaneous frequency is

$$
f_i(t)=f_c+\Delta f\cos(2\pi f_mt).
$$

Three quantities will appear repeatedly:

| Quantity | Meaning | What it mainly controls |
|---|---|---|
| \(f_c\) | Carrier frequency | Center of the FM spectrum |
| \(f_m\) | Message frequency | How quickly the deviation changes and the spacing of single-tone sidebands |
| \(\Delta f\) | Peak frequency deviation | How far the instantaneous frequency moves from \(f_c\) |

Keeping these three roles separate makes the rest of the chapter much easier to follow.

## 14.2 Experiment 14.1: Seeing Frequency Modulation

The first experiment makes FM visible in both time and frequency.

A sinusoidal message controls a complex VCO. Two QT GUI Range controls let us change the message frequency and frequency deviation while the flowgraph is running.

![GNU Radio flowgraph for exploring the basic behavior of frequency modulation](../figures/ch14/ch14-exp1-fm-basics-flowgraph.png)

Use:

| Parameter | Value |
|---|---:|
| Sample rate | 64 kS/s |
| Carrier frequency \(f_c\) | 10 kHz |
| Initial message frequency \(f_m\) | 500 Hz |
| Message amplitude | 1 |
| Initial frequency deviation \(\Delta f\) | 2 kHz |

The VCO control signal is arranged so that it represents

$$
u(t)=f_c+\Delta f\,m(t)
$$

in hertz.

The complex VCO uses:

```text
Sample Rate: 64k
Sensitivity: 6.28319
Amplitude: 1
```

GNU Radio defines VCO sensitivity in radians/s per input unit. Since

$$
2\pi\text{ rad/s}=1\text{ Hz},
$$

using

$$
\text{Sensitivity}=2\pi
$$

means a VCO input value of 10,000 produces a 10 kHz output frequency.

### Start with Zero Deviation

Set:

```text
Frequency Deviation = 0 Hz
Message Frequency   = 500 Hz
Carrier Frequency   = 10 kHz
```

![FM experiment with zero frequency deviation](../figures/ch14/ch14-exp1-zero-frequency-deviation.png)

The message is still present in the flowgraph, but it has no effect on the VCO because its contribution has been multiplied by zero.

The output is simply an unmodulated 10 kHz complex carrier.

Now increase the frequency deviation.

![Effect of increasing frequency deviation on the FM waveform and spectrum](../figures/ch14/ch14-exp1-combined-frequency-deviation.png)

The time-domain waveform begins to crowd together in some regions and spread apart in others.

That is the visual signature we expect.

Closely spaced cycles correspond to higher instantaneous frequency. Widely spaced cycles correspond to lower instantaneous frequency.

The amplitude does not need to change. What changes is the **rate of phase rotation**.

## 14.3 From Instantaneous Frequency to the FM Equation

Frequency and phase are directly related:

$$
f_i(t)=\frac{1}{2\pi}\frac{d\theta(t)}{dt}.
$$

So if the message controls instantaneous frequency, it also controls how phase accumulates.

For a single-tone message,

$$
m(t)=\cos(2\pi f_mt),
$$

integrating the frequency deviation gives the familiar FM signal

$$
s_{\mathrm{FM}}(t)=A_c\cos\left(2\pi f_ct+\beta\sin(2\pi f_mt)\right),
$$

where

$$
\beta=\frac{\Delta f}{f_m}.
$$

The quantity \(\beta\) is the **FM modulation index**.

Unlike conventional AM, the message-dependent term is not multiplying the carrier amplitude. It appears inside the phase.

That is the mathematical reason FM behaves so differently from AM.

## 14.4 Experiment 14.2: Exploring the FM Sidebands

The time-domain plot shows frequency changing with time. The Frequency Sink reveals another property of FM: a single-tone message can create many spectral components.

We reuse the first flowgraph and change the two controls.

### Change Deviation While Keeping the Message Frequency Fixed

Keep

$$
f_m=500\text{ Hz}
$$

and increase \(\Delta f\).

![FM sidebands as frequency deviation is increased while message frequency remains fixed](../figures/ch14/ch14-exp2-sidebands-vs-frequency-deviation.png)

With \(f_m=500\) Hz:

| \(\Delta f\) | \(f_m\) | \(\beta=\Delta f/f_m\) |
|---:|---:|---:|
| 500 Hz | 500 Hz | 1 |
| 1000 Hz | 500 Hz | 2 |
| 2000 Hz | 500 Hz | 4 |

As the deviation grows, more sideband orders become significant and the practical spectrum spreads farther from the carrier.

The spacing between neighbouring spectral lines remains 500 Hz because the message frequency has not changed.

### Change Message Frequency While Keeping Deviation Fixed

Now keep

$$
\Delta f=2000\text{ Hz}
$$

and change \(f_m\).

![FM sideband spacing as message frequency is changed while frequency deviation remains fixed](../figures/ch14/ch14-exp2-sideband-spacing-vs-message-frequency.png)

For single-tone FM, adjacent spectral components are separated by

$$
f_m.
$$

At the same time, increasing \(f_m\) while holding \(\Delta f\) fixed reduces the modulation index:

| \(\Delta f\) | \(f_m\) | \(\beta\) |
|---:|---:|---:|
| 2000 Hz | 500 Hz | 4 |
| 2000 Hz | 1000 Hz | 2 |
| 2000 Hz | 2000 Hz | 1 |

So the two controls do different jobs.

Increasing \(\Delta f\) at fixed \(f_m\) tends to make more sideband orders important.

Changing \(f_m\) changes the sideband spacing and also changes \(\beta\) if the deviation is held fixed.

Changing \(f_c\) simply moves the entire FM spectrum to another center frequency.

## 14.5 Why FM Produces Many Sidebands

Single-tone conventional AM gave us only

$$
f_c-f_m,\qquad f_c,\qquad f_c+f_m.
$$

Single-tone FM can contain components at

$$
f_c\pm nf_m,\qquad n=0,1,2,3,\ldots
$$

The amplitudes are governed by **Bessel functions of the first kind**.

For

$$
s_{\mathrm{FM}}(t)=A_c\cos\left(2\pi f_ct+\beta\sin(2\pi f_mt)\right),
$$

the carrier coefficient is \(J_0(\beta)\), the first sideband pair is associated with \(J_1(\beta)\), the second pair with \(J_2(\beta)\), and so on.

| Spectral Component | Relative Coefficient |
|---|---|
| Carrier at \(f_c\) | \(J_0(\beta)\) |
| \(f_c\pm f_m\) | \(J_1(\beta)\) |
| \(f_c\pm2f_m\) | \(J_2(\beta)\) |
| \(f_c\pm3f_m\) | \(J_3(\beta)\) |
| Higher orders | \(J_n(\beta)\) |

The signs of the Bessel coefficients also carry phase information, so it is safer to think of \(J_n(\beta)\) as the spectral coefficient rather than only as a positive amplitude.

The practical lesson is simpler:

> **Changing \(\beta\) redistributes FM energy among the carrier and different sideband orders.**

This explains why one spectral line may grow while another becomes weaker as the modulation index changes.

At certain values of \(\beta\),

$$
J_0(\beta)=0,
$$

so the spectral line at the carrier frequency disappears even though the FM waveform is still present.

Ideal single-tone FM has infinitely many mathematical sidebands, but distant high-order terms eventually become very small. Engineering bandwidth therefore depends on the **significant** sidebands rather than on every mathematically nonzero term.

## 14.6 Experiment 14.3: Narrowband FM

To see the other extreme, reduce the modulation index to

$$
\beta=0.1.
$$

![Narrowband FM spectrum for a modulation index of 0.1](../figures/ch14/ch14-exp3-narrowband-fm-beta-0p1.png)

For

$$
\beta\ll1,
$$

the useful approximations are

$$
J_0(\beta)\approx1
$$

and

$$
J_1(\beta)\approx\frac{\beta}{2},
$$

while higher-order terms are very small.

Most of the visible energy is therefore concentrated in the carrier and first sideband pair.

This is the **narrowband FM** region.

As \(\beta\) becomes larger, more sideband orders become important and we move toward **wideband FM**.

There is no need to treat the names as a switch at one magical numerical value. The important behaviour is gradual: small \(\beta\) gives relatively few important sidebands, while larger \(\beta\) spreads the spectrum across more orders.

## 14.7 Estimating FM Bandwidth

FM creates an awkward theoretical result: ideal single-tone FM has infinitely many sidebands.

A useful engineering estimate is **Carson's rule**.

For a single-tone message,

$$
B\approx2(\Delta f+f_m).
$$

For a general message, \(f_m\) is replaced by the highest significant message frequency \(f_{m,\max}\):

$$
B\approx2(\Delta f+f_{m,\max}).
$$

Carson's rule is an approximation. It does not say that all spectrum outside this range is exactly zero.

Using the values from our experiment,

$$
\Delta f=2000\text{ Hz}
$$

and

$$
f_m=500\text{ Hz},
$$

we have

$$
\beta=\frac{2000}{500}=4.
$$

Carson's rule gives

$$
B\approx2(2000+500)=5000\text{ Hz}.
$$

So the useful occupied bandwidth is roughly 5 kHz for this single-tone case.

This gives us an important engineering trade-off: larger deviation can improve some FM performance characteristics, but it also consumes more spectrum.

## 14.8 Experiment 14.4: Recovering the Message

At the transmitter, the message moved the instantaneous frequency around the 10 kHz center frequency.

At the receiver, we need to estimate that instantaneous frequency and convert the deviation back into the message.

Add a **Quadrature Demod** block.

![GNU Radio flowgraph for FM demodulation and message recovery](../figures/ch14/ch14-exp4-fm-demodulation-flowgraph.png)

Use:

| Parameter | Value |
|---|---:|
| Sample rate | 64 kS/s |
| Carrier frequency | 10 kHz |
| Message frequency | 500 Hz |
| Frequency deviation | 2 kHz |
| Message amplitude | 1 |

The Quadrature Demod block estimates the phase change between consecutive complex samples.

If

$$
x[n]=A[n]e^{j\phi[n]},
$$

then the product

$$
x[n]x^*[n-1]
$$

has phase approximately

$$
\phi[n]-\phi[n-1].
$$

That phase difference is proportional to instantaneous frequency.

### Scaling the Demodulator Output into Hertz

For a sampled complex sinusoid, the phase change per sample is

$$
\Delta\phi=2\pi\frac{f}{f_s}.
$$

Therefore,

$$
f=\frac{f_s}{2\pi}\Delta\phi.
$$

Use the Quadrature Demod gain

$$
G=\frac{f_s}{2\pi}.
$$

With

$$
f_s=64\,000\text{ samples/s},
$$

this becomes

$$
G\approx10\,185.9.
$$

In GNU Radio:

```text
Gain = 10.1859k
```

With this scaling, the raw demodulator output can be interpreted approximately in hertz.

For our FM signal it moves between about

$$
8\text{ kHz}
$$

and

$$
12\text{ kHz}.
$$

Subtract the 10 kHz center frequency:

```text
Constant = -10k
```

Then scale by the inverse of the 2 kHz deviation:

```text
Constant = 500u
```

because

$$
\frac{1}{\Delta f}=\frac{1}{2000}=0.0005.
$$

The result should have approximately unit amplitude.

![Original message compared with the message recovered from FM](../figures/ch14/ch14-exp4-original-and-recovered-message.png)

The recovered trace follows the original message closely.

The receiver has effectively implemented

$$
\hat{m}(t)\approx\frac{f_i(t)-f_c}{\Delta f}.
$$

This closes the FM loop: message values became frequency deviation at the transmitter, and frequency deviation became message values again at the receiver.

## 14.9 Where the Information Lives

For ideal complex FM,

$$
s_{\mathrm{FM}}(t)=A_ce^{j\theta(t)},
$$

so its magnitude is

$$
|s_{\mathrm{FM}}(t)|=A_c.
$$

The information therefore does not require a changing magnitude.

A useful I/Q picture is a vector whose length stays constant while its rotation rate changes.

That gives FM its **constant-envelope** property.

The receiver from Experiment 14.4 reinforces the same point. Quadrature Demod looks at phase change between samples, not at the absolute magnitude itself.

This suggests a useful test.

What happens if we deliberately disturb only the amplitude while leaving the phase trajectory intact?

## 14.10 Experiment 14.5: Multiplicative Amplitude Variation

The original figure names use the phrase *amplitude noise*, but the experiment is more accurately described as **multiplicative amplitude variation**.

We form

$$
r(t)=A(t)s_{\mathrm{FM}}(t),
$$

where \(A(t)\) changes the magnitude.

![GNU Radio flowgraph for applying amplitude variation to an FM signal](../figures/ch14/ch14-exp5-amplitude-noise-flowgraph.png)

First observe the undisturbed case.

![FM message recovery with no amplitude disturbance](../figures/ch14/ch14-exp5-no-amplitude-noise.png)

The FM magnitude is approximately 1, and the recovered message follows the original.

Now increase the amplitude variation.

![FM message recovery with amplitude disturbance level 0.3](../figures/ch14/ch14-exp5-amplitude-noise-0p3.png)

The received magnitude fluctuates, but the recovered message remains essentially unchanged.

For positive real amplitude scaling,

$$
r[n]=A[n]e^{j\phi[n]},\qquad A[n]>0,
$$

the amplitude factors affect the magnitude of

$$
r[n]r^*[n-1]
$$

but not its phase.

The phase difference still contains approximately

$$
\phi[n]-\phi[n-1].
$$

That is why the ideal quadrature demodulator can tolerate this kind of amplitude variation.

The condition \(A[n]>0\) matters. If the multiplier crosses through zero or changes sign, the phase behaviour can become ambiguous or acquire a \(\pi\) reversal. So the experiment should not be interpreted as saying that every possible amplitude disturbance is harmless.

The practical lesson is that FM receivers can use **amplitude limiting** to reduce unwanted magnitude variation before demodulation, provided the phase information is preserved.

But this does not mean FM is immune to noise.

## 14.11 Experiment 14.6: Additive Noise

Now disturb the FM signal in a fundamentally different way.

Instead of multiplying by a changing amplitude, add complex Gaussian noise:

$$
r(t)=s_{\mathrm{FM}}(t)+n(t).
$$

![GNU Radio flowgraph for passing FM through an additive Gaussian noise channel](../figures/ch14/ch14-exp6-fm-additive-noise-flowgraph.png)

Keep:

| Parameter | Value |
|---|---:|
| Sample rate | 64 kS/s |
| Carrier frequency | 10 kHz |
| Message frequency | 500 Hz |
| Frequency deviation | 2 kHz |
| FM amplitude scale | 1 |

Observe three quantities:

- original and recovered messages;
- raw Quadrature Demod output;
- magnitude of the noisy FM signal.

### Clean Channel

Set:

```text
Channel Noise Amplitude = 0
```

![FM transmission through a clean channel with zero additive noise](../figures/ch14/ch14-exp6-fm-additive-noise-000.png)

The magnitude remains close to 1.

The raw demodulator output follows the instantaneous frequency cleanly between roughly 8 kHz and 12 kHz.

The recovered message follows the original.

### Moderate Noise

Set:

```text
Channel Noise Amplitude = 0.10
```

![FM transmission with additive channel-noise amplitude 0.10](../figures/ch14/ch14-exp6-fm-additive-noise-010.png)

The magnitude now fluctuates.

More importantly, the raw instantaneous-frequency estimate becomes noisy, and the recovered message begins to show visible corruption.

### Stronger Noise

Set:

```text
Channel Noise Amplitude = 0.30
```

![FM transmission with additive channel-noise amplitude 0.30](../figures/ch14/ch14-exp6-fm-additive-noise-030.png)

The degradation is much stronger.

The important difference from Experiment 14.5 is that additive noise changes the I and Q components themselves. It therefore perturbs both magnitude and phase.

Since the demodulator extracts information from phase change, random phase perturbations become instantaneous-frequency errors.

| Disturbance | Magnitude Affected? | Phase Affected? | Simple FM Demodulation |
|---|---|---|---|
| Constant positive amplitude scaling | Yes | No | Essentially unchanged |
| Positive multiplicative amplitude variation | Yes | Ideally no | Largely unchanged |
| Additive complex noise | Yes | Yes | Increasingly degraded |

The conclusion is precise:

> **FM is relatively insensitive to pure positive amplitude variation, but it is not immune to additive noise.**

A practical FM receiver would usually include filtering, limiting, and other stages. Our deliberately simple receiver exposes the raw effect so that the mechanism is easy to see.

## 14.12 FM and Phase Modulation

FM has a close relative: **phase modulation**, or PM.

With PM, the message changes carrier phase directly:

$$
s_{\mathrm{PM}}(t)=A_c\cos\left(2\pi f_ct+k_pm(t)\right),
$$

where \(k_p\) sets the phase sensitivity.

The difference between FM and PM is easiest to state in terms of what the message controls directly.

| Modulation | Message Directly Controls |
|---|---|
| AM | Carrier amplitude |
| FM | Instantaneous frequency |
| PM | Carrier phase |

For PM,

$$
\phi_{\mathrm{PM}}(t)\propto m(t).
$$

For FM,

$$
f_i(t)-f_c\propto m(t).
$$

Because frequency is the rate of phase change,

$$
f_i(t)=\frac{1}{2\pi}\frac{d\phi(t)}{dt},
$$

FM and PM are closely related and are often grouped together as **angle modulation**.

For a general FM message, the phase is

$$
\theta_{\mathrm{FM}}(t)=2\pi f_ct+2\pi k_f\int_0^t m(\tau)\,d\tau,
$$

so

$$
s_{\mathrm{FM}}(t)=A_c\cos\left(2\pi f_ct+2\pi k_f\int_0^t m(\tau)\,d\tau\right).
$$

In PM, the message itself appears in the phase term:

$$
s_{\mathrm{PM}}(t)=A_c\cos\left(2\pi f_ct+k_pm(t)\right).
$$

We will not build a separate PM experiment here. Its main purpose in this chapter is to connect the analog idea of changing phase continuously with the digital phase states we will meet later in PSK.

## 14.13 GNU Radio Toolbox

The chapter introduces a small number of blocks in important new roles.

| GNU Radio Block | Role in This Chapter |
|---|---|
| VCO (complex) | Generates a complex oscillator whose instantaneous frequency is controlled by a float input |
| Quadrature Demod | Measures phase change between consecutive complex samples to recover frequency information |
| Complex to Mag | Displays the magnitude of the complex FM signal |
| Noise Source | Adds random channel noise for the additive-noise experiment |
| QT GUI Range | Changes message frequency, deviation, and disturbance strength interactively |

### VCO (complex)

GNU Radio defines VCO sensitivity in radians/s per input unit.

In our experiment, the control input is expressed directly in hertz, so we use

$$
\text{Sensitivity}=2\pi.
$$

That makes the VCO input numerically equal to the desired instantaneous frequency.

### Quadrature Demod

The block estimates the phase difference between adjacent complex samples.

Using

$$
G=\frac{f_s}{2\pi}
$$

converts that phase increment into a frequency-like output in hertz.

The block therefore gives us a direct experimental bridge between phase evolution and instantaneous frequency.

### Complex to Mag

For

$$
z=I+jQ,
$$

the magnitude is

$$
|z|=\sqrt{I^2+Q^2}.
$$

This lets us see whether an FM disturbance changes the signal magnitude even when the message is carried in phase/frequency.

## 14.14 Explore Further

The FM flowgraphs are especially useful for prediction-driven experiments.

1. Keep \(f_m=500\) Hz and increase \(\Delta f\). Predict how \(\beta\) and the number of significant sidebands should change.

2. Keep \(\Delta f=2\) kHz and increase \(f_m\). Predict both the sideband spacing and the new modulation index.

3. Reduce \(\beta\) well below 1 and compare the observed spectrum with the narrowband approximations.

4. Use Carson's rule before changing the controls, then compare the estimated bandwidth with the Frequency Sink.

5. Change the carrier frequency while leaving \(f_m\) and \(\Delta f\) unchanged. The spectral shape should stay similar while its center moves.

6. Change the Quadrature Demod gain away from \(f_s/(2\pi)\). The recovered shape should remain related to the message, but the numerical scaling will no longer represent hertz directly.

7. Increase the multiplicative amplitude variation and watch both magnitude and recovered message. Then compare the result with additive noise at a similar visible magnitude fluctuation.

8. In the additive-noise experiment, increase the noise gradually through values such as `0.05`, `0.10`, `0.20`, and `0.30`. Observe how the raw demodulator output degrades before deciding that the receiver has simply “failed.”

The useful habit is to predict which quantity should change before moving a slider.

## 14.15 What We Learned

FM carries information through instantaneous frequency and phase evolution rather than through the signal magnitude.

For a normalized message,

$$
f_i(t)=f_c+\Delta f\,m(t).
$$

For a sinusoidal message,

$$
s_{\mathrm{FM}}(t)=A_c\cos\left(2\pi f_ct+\beta\sin(2\pi f_mt)\right),
$$

with

$$
\beta=\frac{\Delta f}{f_m}.
$$

The carrier frequency sets the spectral center.

The message frequency sets the spacing between single-tone FM components.

The frequency deviation controls how far the instantaneous frequency moves.

The modulation index helps describe how strongly the spectrum spreads among different sideband orders.

Those sideband coefficients are governed by Bessel functions, which explains why FM contains many sidebands and why individual spectral components can grow, shrink, or even pass through zero as \(\beta\) changes.

For small \(\beta\), only the first few components matter and the spectrum behaves like narrowband FM.

Carson's rule gives a practical bandwidth estimate:

$$
B\approx2(\Delta f+f_{m,\max}).
$$

At the receiver, Quadrature Demod recovers frequency information by measuring phase change from sample to sample.

The last two experiments made another distinction clear.

Pure positive amplitude variation can leave the phase trajectory intact, so an ideal FM demodulator may be largely unaffected.

Additive noise is different. It disturbs I and Q, which can disturb phase and therefore the instantaneous-frequency estimate.

So the useful conclusion is not that FM is “immune to noise.”

It is:

> **FM does not need amplitude to carry the message, but anything that corrupts phase can corrupt the recovered information.**

## 14.16 Connecting to the Next Chapter

Across Chapters 12 through 14, we have moved from asking why modulation is necessary to building the main ideas of analog carrier modulation.

AM used changing amplitude.

FM used changing instantaneous frequency.

PM showed that information can also be placed directly into phase.

The next part of the book begins from a different kind of information:

```text
1 0 1 1 0 0 1 0 ...
```

These are bits.

But a bit is an abstract piece of information, not a radio waveform. Before we can build BPSK, QPSK, QAM, or other digital modulation schemes, we need to understand how bits are grouped, what symbols are, how bit rate differs from symbol rate, and how digital information is mapped onto physical signal states.

That takes us to Chapter 15, **Bits, Symbols and Digital Communication**.