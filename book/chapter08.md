# Chapter 8: Mixing and Frequency Translation

In the previous chapters, we learned how to generate signals, examine their spectra, add noise, measure power, and control bandwidth. We also introduced I/Q signals and saw how complex frequency carries a direction of rotation.

A radio receiver has another practical problem. The signal we want may not be sitting at a convenient frequency.

Suppose a receiver is interested in a signal around 100 MHz. We may eventually want to filter it, demodulate it, measure it, or process its information digitally. It is often more convenient to move that signal to another part of the spectrum first.

This process is called **frequency translation**, and one of the main tools used to perform it is the **mixer**.

In this chapter, we will study frequency translation in two stages. We will begin with real cosine signals and observe the familiar sum and difference products. Then we will repeat the experiment with complex signals and see why complex mixing is especially useful in SDR.

## 8.1 Mixing Means Multiplication

A mixer multiplies one signal by another. The second signal is normally generated locally inside the receiver and is called the **local oscillator**, or **LO**.

If the received signal is $x(t)$ and the local oscillator is $l(t)$, then the mixer output is

$$
y(t)=x(t)l(t)
$$

The important part is what this multiplication does in the frequency domain.

Suppose our signal is at

$$
f_{\text{signal}}=6\text{ kHz}
$$

and the LO is at

$$
f_{\text{LO}}=1\text{ kHz}
$$

We will begin by using ordinary real cosines for both.

## 8.2 Experiment 1: Real Mixing

Use two real Signal Sources, both with amplitude 1. The first generates the 6 kHz signal and the second generates the LO. Their outputs feed a Multiply block.

![GNU Radio flowgraph for real mixing](../figures/ch08/ch08-exp1-real-mixing-flowgraph.png)

Use a common sample rate of

```text
samp_rate = 32000
```

and control the LO using a QT GUI Range:

```text
ID: lo_freq
Label: LO Frequency
Default Value: 1000
Start: 1000
Stop: 7000
Step: 500
```

The signal source remains fixed at 6 kHz while `lo_freq` changes. The mixer output is observed with both a QT GUI Time Sink and a QT GUI Frequency Sink.

The two real signals are

$$
x(t)=\cos(2\pi f_{\text{signal}}t)
$$

and

$$
l(t)=\cos(2\pi f_{\text{LO}}t)
$$

so the mixer output is

$$
y(t)=\cos(2\pi f_{\text{signal}}t)\cos(2\pi f_{\text{LO}}t)
$$

Using

$$
\cos A\cos B=\frac{1}{2}\cos(A-B)+\frac{1}{2}\cos(A+B)
$$

we obtain

$$
y(t)=\frac{1}{2}\cos\left(2\pi(f_{\text{signal}}-f_{\text{LO}})t\right)+\frac{1}{2}\cos\left(2\pi(f_{\text{signal}}+f_{\text{LO}})t\right)
$$

Real mixing therefore produces two components:

$$
f_{\text{difference}}=f_{\text{signal}}-f_{\text{LO}}
$$

and

$$
f_{\text{sum}}=f_{\text{signal}}+f_{\text{LO}}
$$

For a 6 kHz signal and a 1 kHz LO,

$$
f_{\text{difference}}=6-1=5\text{ kHz}
$$

and

$$
f_{\text{sum}}=6+1=7\text{ kHz}
$$

Because the mixer output is real, its centred spectrum is symmetric. We therefore observe components at approximately

$$
-7,\ -5,\ +5,\ +7\text{ kHz}
$$

### Moving the LO

The following figure shows what happens as we change only the LO frequency.

![Real mixing while sweeping the LO frequency](../figures/ch08/ch08-exp1-real-mixing-lo-sweep.png)

With an LO of 1 kHz, the products are 5 kHz and 7 kHz. With an LO of 3 kHz, they move to 3 kHz and 9 kHz.

When the LO reaches 6 kHz, the difference component reaches DC:

$$
6-6=0
$$

while the sum component moves to

$$
6+6=12\text{ kHz}
$$

This is our first glimpse of downconversion to baseband.

If the LO is increased to 7 kHz, the formal difference is

$$
6-7=-1\text{ kHz}
$$

but a real cosine cannot preserve that sign as a unique direction of rotation. Its spectrum remains mirrored, so the real mixer output contains the same cosine behaviour at $\pm1$ kHz.

The experiment gives us the main idea of frequency conversion:

> Multiplication in time can move spectral components in frequency.

## 8.3 Upconversion and Downconversion

If frequency translation moves the desired component toward a higher frequency region, we call it **upconversion**. If it moves the desired component toward a lower frequency region, we call it **downconversion**.

For example, with a 6 kHz signal and a 5 kHz LO, real mixing produces

$$
6-5=1\text{ kHz}
$$

and

$$
6+5=11\text{ kHz}
$$

The 1 kHz term is the low-frequency difference product. The 11 kHz term is also present, so mixing alone does not isolate the component we want.

To keep the low-frequency product and suppress the high-frequency one, we need a filter.

## 8.4 Experiment 2: Real Downconversion and Filtering

We now keep the input fixed at 6 kHz, vary the LO around that frequency, and place a Low Pass Filter after the mixer.

![GNU Radio flowgraph for real downconversion](../figures/ch08/ch08-exp2-real-downconversion-flowgraph.png)

The Low Pass Filter uses:

```text
Decimation: 1
Gain: 1
Sample Rate: samp_rate
Cutoff Frequency: 1000
Transition Width: 500
Window: Hamming
```

Useful LO values are

```text
4000 Hz
5000 Hz
5500 Hz
6000 Hz
6500 Hz
```

The predicted mixer products are:

| LO frequency | Difference component | Sum component |
|---:|---:|---:|
| 4 kHz | 2 kHz | 10 kHz |
| 5 kHz | 1 kHz | 11 kHz |
| 5.5 kHz | 0.5 kHz | 11.5 kHz |
| 6 kHz | 0 Hz | 12 kHz |
| 6.5 kHz | 0.5 kHz | 12.5 kHz |

For the real sinusoidal output, the observable low-frequency component is naturally described by

$$
f_{\text{difference}}=\left|f_{\text{signal}}-f_{\text{LO}}\right|
$$

The high-frequency sum term should be strongly attenuated by the Low Pass Filter. The difference component moves progressively toward DC as the LO approaches 6 kHz.

![Real downconversion as the LO approaches the signal frequency](../figures/ch08/ch08-exp2-real-downconversion-comparison.png)

At an LO of 4 kHz, the 2 kHz difference component lies outside the main passband and is strongly attenuated. At 5 kHz, the difference component has reached 1 kHz, near the cutoff region. At 5.5 kHz, the 0.5 kHz component is clearly retained.

At 6 kHz, the difference component reaches DC.

When the LO moves beyond the signal, for example to 6.5 kHz, the real mixer again produces a 0.5 kHz cosine after filtering. The real output does not preserve whether that 0.5 kHz separation came from the LO being below or above the signal.

### Baseband and Frequency Offset

A **baseband** representation is centred around zero frequency rather than around a higher carrier frequency. Downconversion moves the desired part of the spectrum toward this region so that later processing can operate on a lower-frequency representation.

If the desired signal is at 6 kHz and the LO is exactly 6 kHz, the difference reaches DC. If the LO is instead 5.5 kHz, the output remains 500 Hz from DC:

$$
6-5.5=0.5\text{ kHz}
$$

That remaining separation is a **frequency offset**.

Real receivers experience the same kind of mismatch. Oscillators are not perfectly exact, transmitter and receiver frequencies may differ slightly, and motion can introduce Doppler shifts.

## 8.5 Why Real Mixing Has a Limitation

A real cosine contains both positive- and negative-frequency components. A real LO does too. When the two are multiplied, the positive and negative components interact and produce both sum and difference terms.

This has two consequences:

- additional mixer products appear and often need filtering;
- the sign of a low-frequency offset is not preserved in the same way as it is for a complex signal.

Complex signals allow us to handle frequency translation more directly.

## 8.6 Experiment 3: Complex Frequency Translation

A complex exponential can represent a single signed frequency:

$$
x(t)=e^{j2\pi f_{\text{signal}}t}
$$

Suppose we multiply it by a complex LO rotating in the negative-frequency direction:

$$
l(t)=e^{-j2\pi f_{\text{LO}}t}
$$

Then

$$
y(t)=e^{j2\pi f_{\text{signal}}t}e^{-j2\pi f_{\text{LO}}t}
$$

so

$$
y(t)=e^{j2\pi(f_{\text{signal}}-f_{\text{LO}})t}
$$

There is no second cosine term at the sum frequency. The complex spectrum is translated directly.

![GNU Radio flowgraph for complex frequency translation](../figures/ch08/ch08-exp3-complex-mixing-flowgraph.png)

Use

```text
samp_rate = 32000
Signal Frequency = 6000 Hz
```

and apply the LO in the negative-frequency direction so that

$$
f_{\text{out}}=f_{\text{signal}}-f_{\text{LO}}
$$

For a fixed 6 kHz signal, the predictions are:

| LO magnitude | Output frequency |
|---:|---:|
| 4 kHz | +2 kHz |
| 5 kHz | +1 kHz |
| 6 kHz | 0 Hz |
| 7 kHz | -1 kHz |

![Complex mixing as the signal moves through DC](../figures/ch08/ch08-exp3-complex-mixing-comparison.png)

The spectrum behaves exactly this way. The translated tone moves from positive frequency, through DC, and then into negative frequency.

This is fundamentally different from the real-mixer case. The complex representation preserves the sign of the translated frequency.

## 8.7 What Crossing DC Means in I/Q

At exact tuning,

$$
f_{\text{signal}}=f_{\text{LO}}
$$

so

$$
f_{\text{out}}=0
$$

A zero-frequency complex exponential no longer rotates. For the ideal unit-amplitude case,

$$
e^{j0}=1
$$

so the I and Q values become constant rather than oscillating.

The exact constant values depend on the relative phase and amplitude used in the flowgraph, but the important physical interpretation is simple:

> When a complex tone is translated exactly to DC, its I/Q vector stops rotating.

If a small frequency offset remains, the vector continues to rotate slowly. A larger offset produces faster rotation.

Positive and negative complex frequencies correspond to opposite directions of this rotation. That is why a complex tone can pass through zero and continue naturally to the other side of the spectrum.

## 8.8 Experiment 4: Choosing the Translation Direction

The previous experiment used a negative-frequency LO for downconversion. We can also reverse the LO sign and deliberately shift the signal upward.

Keep the input at

$$
+6\text{ kHz}
$$

and the LO magnitude at

$$
4\text{ kHz}
$$

Use a QT GUI Chooser to select between two signed LO values:

```text
Downshift: -1
Upshift: +1
```

and set the complex LO frequency to

```text
lo_direction * lo_freq
```

with

```text
lo_freq = 4000
```

![GNU Radio flowgraph for reversing the complex LO](../figures/ch08/ch08-exp4-lo-direction-flowgraph.png)

With `lo_direction = -1`, the LO is $-4$ kHz, so

$$
f_{\text{out}}=6+(-4)=+2\text{ kHz}
$$

With `lo_direction = +1`, the LO is $+4$ kHz, so

$$
f_{\text{out}}=6+4=+10\text{ kHz}
$$

![Complex mixing with downshift and upshift LO directions](../figures/ch08/ch08-exp4-lo-direction-comparison.png)

The experiment makes the signed-frequency rule very clear. We are not generating both products simultaneously. We are choosing the direction of translation through the sign of the complex oscillator.

## 8.9 Real Mixing and Complex Mixing Compared

The difference between the two approaches is now easier to see.

For real mixing,

$$
\cos(2\pi f_1t)\cos(2\pi f_2t)=\frac{1}{2}\cos\left(2\pi(f_1-f_2)t\right)+\frac{1}{2}\cos\left(2\pi(f_1+f_2)t\right)
$$

so both sum and difference products appear.

For complex mixing,

$$
e^{j2\pi f_1t}e^{j2\pi f_2t}=e^{j2\pi(f_1+f_2)t}
$$

and

$$
e^{j2\pi f_1t}e^{-j2\pi f_2t}=e^{j2\pi(f_1-f_2)t}
$$

The spectrum shifts directly by the signed LO frequency.

A useful general form is

$$
f_{\text{out}}=f_{\text{in}}+f_{\text{LO}}
$$

where $f_{\text{LO}}$ itself can be positive or negative.

This is one reason complex mixing is such a natural operation in SDR. The LO tells the spectrum how far, and in which direction, to move.

## 8.10 What the Local Oscillator Means in a Receiver

The term **local oscillator** comes from radio hardware. A receiver generates an oscillator locally and combines it with the incoming signal in a mixer.

The mixer operation is multiplication, even though block diagrams sometimes draw the signal and LO as two paths entering the same device.

Suppose a receiver contains a signal centred at

$$
100.1\text{ MHz}
$$

and we want to move that centre to baseband. In an idealised complex receiver, multiplying by an appropriate complex oscillator near

$$
-100.1\text{ MHz}
$$

moves the centre toward zero frequency.

The same principle can be implemented in hardware or digitally. SDR hardware may perform some frequency translation before sampling, and GNU Radio can perform additional digital translation on the resulting complex samples.

The exact receiver architecture can vary, but the underlying mathematical idea remains the same.

### Mistuning the LO

If we intend to translate a signal exactly to DC, ideally

$$
f_{\text{LO}}=-f_{\text{signal}}
$$

so that

$$
f_{\text{out}}=0
$$

If the actual LO is

$$
f_{\text{LO}}=-f_{\text{signal}}+\Delta f
$$

then

$$
f_{\text{out}}=\Delta f
$$

The remaining baseband tone is therefore a direct measure of the frequency mismatch.

## 8.11 GNU Radio Toolbox

This chapter mainly reused familiar blocks in a more radio-like role.

| GNU Radio block | Role in this chapter |
|---|---|
| Signal Source | Generated the input tones and local oscillators |
| Multiply | Performed real or complex mixing |
| QT GUI Range | Varied the LO frequency while the flowgraph was running |
| QT GUI Chooser | Switched between positive and negative complex LO directions |
| Low Pass Filter | Kept the low-frequency difference product and suppressed higher-frequency mixer products |
| Throttle | Limited processing rate in software-only flowgraphs |
| QT GUI Time Sink | Displayed time-domain signals and I/Q components |
| QT GUI Frequency Sink | Showed mixer products and signed complex frequency |

The most important GNU Radio habit here is to keep the **data type** in mind. Real mixing uses float signals and produces a real output. Complex mixing uses complex signals and preserves signed-frequency information.

## 8.12 Explore Further

The existing flowgraphs make several useful extensions possible.

1. Keep the real input at 6 kHz and vary the LO continuously from 1 kHz to 7 kHz. Predict both mixer products before checking the Frequency Sink.
2. In the real downconverter, change the Low Pass Filter cutoff and observe when the desired difference component enters the transition region or becomes strongly attenuated.
3. In the complex mixer, use a negative LO of 5.9 kHz. The 6 kHz input should remain approximately 100 Hz above DC.
4. Match the complex LO exactly to the signal and observe the I/Q traces when the rotation stops.
5. Move the complex LO past the signal so that the output becomes negative frequency. Compare the Frequency Sink with the I/Q time traces.
6. Reverse the complex LO sign while keeping its magnitude fixed. Predict the translated frequency before switching the chooser.

The useful discipline is the same as in earlier chapters: change one parameter, predict the result, and then compare the prediction with the observation.

## 8.13 What We Learned

A mixer performs multiplication, and multiplication can translate spectral components in frequency.

With real cosine mixing, the output contains both sum and difference products:

$$
f_{\text{sum}}=f_{\text{signal}}+f_{\text{LO}}
$$

and

$$
f_{\text{difference}}=f_{\text{signal}}-f_{\text{LO}}
$$

A Low Pass Filter can then keep the low-frequency difference component and suppress the high-frequency sum component. This gives us a simple real downconverter.

We also saw that real mixing does not preserve the sign of a low-frequency offset in the same way as a complex representation.

Complex mixing behaves more directly. Multiplying by a complex oscillator shifts the spectrum by the signed LO frequency:

$$
f_{\text{out}}=f_{\text{in}}+f_{\text{LO}}
$$

A negative LO can shift the signal downward, a positive LO can shift it upward, and the translated tone can pass through DC into negative frequency without creating a mirrored partner automatically.

At exact tuning, a complex tone reaches DC and its I/Q vector stops rotating. If the LO is slightly mistuned, the remaining rotation represents the frequency offset.

These ideas connect several earlier topics: complex numbers, I/Q signals, positive and negative frequency, filtering, and receiver tuning.

## 8.14 Connecting to the Next Chapter

We now know how to move a signal from one part of the spectrum to another.

But moving a signal does not automatically isolate it. A real receiver may contain several signals, noise, and unwanted mixer products. After translation, we still need a way to keep the part of the spectrum we want and reject the rest.

We already used a Low Pass Filter in this chapter, but only as a practical tool for selecting the difference product.

In the next chapter, we will examine filtering directly. We will compare low-pass, high-pass, band-pass, and band-stop behaviour and study what cutoff frequency, transition width, passband, stopband, filter order, and decimation mean in practice.