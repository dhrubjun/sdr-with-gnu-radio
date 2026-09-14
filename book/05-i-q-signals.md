# Chapter 5: I and Q Signals

In the previous chapter, we introduced complex numbers and saw that a complex signal can be written as

$$
x(t)=I(t)+jQ(t)
$$

We also learned to picture a complex sinusoid as a vector rotating in the complex plane. That leads to an important question for SDR:

> Why do we keep two components, I and Q, instead of using one ordinary real waveform?

In this chapter, we will answer that experimentally. We will first compare positive and negative complex frequencies, then introduce mixing and frequency translation, and finally build a simple quadrature downconverter in GNU Radio.

## 5.1 What Are I and Q?

In SDR, a complex sample is normally written as

$$
x(t)=I(t)+jQ(t)
$$

where $I(t)$ is the **in-phase component** and $Q(t)$ is the **quadrature component**.

Mathematically, they are simply the real and imaginary parts of the complex signal:

$$
I(t)=\operatorname{Re}\{x(t)\}
$$

$$
Q(t)=\operatorname{Im}\{x(t)\}
$$

So the real and imaginary components from Chapter 4 now receive their radio names: **I** and **Q**.

The important point is that I and Q are not two unrelated signals. Together, they describe one complex signal.

### Why Is It Called Quadrature?

Consider the complex exponential

$$
e^{j\theta}=\cos(\theta)+j\sin(\theta)
$$

If $\theta=2\pi ft$, then

$$
e^{j2\pi ft}=\cos(2\pi ft)+j\sin(2\pi ft)
$$

We can identify

$$
I(t)=\cos(2\pi ft)
$$

and

$$
Q(t)=\sin(2\pi ft)
$$

Sine and cosine are separated by $90^\circ$. Signals with this quarter-cycle phase relationship are said to be in **quadrature**, which is where the name Q comes from.

The I component gives the horizontal coordinate of the complex vector and Q gives the vertical coordinate. Together, they tell us where the vector is in the complex plane.

## 5.2 Experiment 1: Why Do We Need Both I and Q?

Consider two complex sinusoids with the same frequency magnitude but opposite signs:

$$
x_+(t)=e^{j2\pi ft}
$$

$$
x_-(t)=e^{-j2\pi ft}
$$

One has positive complex frequency and the other has negative complex frequency. We want to know whether the two can be distinguished if only one component is retained.

Using Euler's formula,

$$
x_+(t)=\cos(2\pi ft)+j\sin(2\pi ft)
$$

so

$$
I_+(t)=\cos(2\pi ft)
$$

$$
Q_+(t)=\sin(2\pi ft)
$$

For the negative-frequency signal,

$$
x_-(t)=\cos(-2\pi ft)+j\sin(-2\pi ft)
$$

Cosine is an even function and sine is an odd function:

$$
\cos(-\theta)=\cos(\theta)
$$

$$
\sin(-\theta)=-\sin(\theta)
$$

Therefore,

$$
x_-(t)=\cos(2\pi ft)-j\sin(2\pi ft)
$$

and hence

$$
I_-(t)=\cos(2\pi ft)
$$

$$
Q_-(t)=-\sin(2\pi ft)
$$

For this pair of signals,

$$
\boxed{I_+(t)=I_-(t)}
$$

while

$$
\boxed{Q_+(t)=-Q_-(t)}
$$

The I components are identical. The Q components carry the sign difference.

### Building the Comparison in GNU Radio

We generate complex tones at $+1$ kHz and $-1$ kHz. Each complex signal is separated into real and imaginary components using **Complex to Real** and **Complex to Imag**. The I components are compared in one Time Sink, the Q components in another, and the original complex signals are also observed in a Frequency Sink.

![GNU Radio flowgraph for comparing positive and negative complex frequencies](../figures/ch05/iq-positive-negative-flowgraph.png)

The result is shown below.

![Comparison of positive and negative complex frequencies](../figures/ch05/iq-positive-negative-comparison.png)

The two I waveforms lie on top of one another:

$$
I_{+1\text{ kHz}}(t)=I_{-1\text{ kHz}}(t)
$$

The Q waveforms have opposite signs:

$$
Q_{-1\text{ kHz}}(t)=-Q_{+1\text{ kHz}}(t)
$$

The Frequency Sink, which receives the complete complex signals, separates them clearly at $+1$ kHz and $-1$ kHz.

> For these complex tones, I alone cannot distinguish the sign of frequency. I and Q together can.

This connects directly to the rotating-vector picture from Chapter 4. For $e^{j2\pi ft}$, phase increases with time. For $e^{-j2\pi ft}$, phase decreases with time. The magnitude of the frequency tells us how fast the vector rotates, while the sign tells us the direction.

The next question is where I and Q come from in a receiver. To answer that, we first need to understand mixing.

## 5.3 Experiment 2: Mixing and Frequency Translation

Suppose a receiver contains a real signal at

$$
f_{RF}=10\text{ kHz}
$$

and we want to move it to a lower frequency for processing. We can multiply it by another sinusoid generated inside the receiver. This second signal is called the **local oscillator**, or LO.

Let

$$
f_{LO}=8\text{ kHz}
$$

A mixer performs multiplication. For this simplified example,

$$
x_{RF}(t)=\cos(2\pi f_{RF}t)
$$

$$
x_{LO}(t)=\cos(2\pi f_{LO}t)
$$

and the mixer output is

$$
y(t)=x_{RF}(t)x_{LO}(t)
$$

Using

$$
\cos A\cos B=\frac{1}{2}\left[\cos(A-B)+\cos(A+B)\right]
$$

we obtain

$$
y(t)=\frac{1}{2}\cos\left(2\pi(f_{RF}-f_{LO})t\right)+\frac{1}{2}\cos\left(2\pi(f_{RF}+f_{LO})t\right)
$$

For our frequencies,

$$
f_{\text{difference}}=10-8=2\text{ kHz}
$$

$$
f_{\text{sum}}=10+8=18\text{ kHz}
$$

Multiplication therefore creates both a difference-frequency component and a sum-frequency component.

### Why We Use 64 kS/s

If we used the 32 kS/s sample rate from earlier chapters, the Nyquist frequency would be

$$
f_N=\frac{32}{2}=16\text{ kHz}
$$

The 18 kHz mixer product would lie above Nyquist and would alias. To observe both products correctly, we use

$$
f_s=64\text{ kS/s}
$$

which gives a Nyquist frequency of 32 kHz.

### Building the Mixer

The GNU Radio experiment uses a **Multiply** block for mixing and a Low Pass Filter to retain the difference-frequency component.

![GNU Radio flowgraph for mixing and filtering](../figures/ch05/iq-mixing-flowgraph.png)

Before filtering, the real-valued mixer output contains components at approximately

$$
\pm2\text{ kHz}\quad\text{and}\quad\pm18\text{ kHz}
$$

The positive and negative pairs appear because the mixer output is real-valued.

We are interested in the 2 kHz difference term, so the Low Pass Filter uses approximately:

| Parameter | Value |
|---|---:|
| Sample Rate | 64 kS/s |
| Cutoff Frequency | 4 kHz |
| Transition Width | 2 kHz |
| Gain | 1 |
| Decimation | 1 |
| Window | Hamming |

The 2 kHz component lies in the passband, while 18 kHz lies far into the stopband.

![Mixer output before and after filtering](../figures/ch05/iq-mixing-filtering-results.png)

Before filtering, the time-domain waveform contains both mixer products. After filtering, it becomes approximately a clean 2 kHz sinusoid. The Frequency Sink shows the same result more directly: the 18 kHz component is strongly suppressed while the 2 kHz component remains.

The filtered sinusoid has an amplitude of approximately 0.5. This follows from the factor $1/2$ in the product identity and is not an error.

We started with 10 kHz, mixed it with 8 kHz, and retained the 2 kHz difference term. We have therefore translated the signal downward in frequency. This is **downconversion**.

## 5.4 Experiment 3: Building an I/Q Downconverter

A single real mixer gives us one real-valued downconverted signal. To form a complex representation, we use two mixer branches in quadrature.

The same received signal is sent to both branches. One branch uses a cosine LO and the other uses a sine LO. After low-pass filtering, the two outputs become I and Q.

The signal path is therefore: **RF signal → quadrature mixers → low-pass filters → I and Q → Float to Complex**.

### The I Branch

Our received signal is

$$
x_{RF}(t)=\cos(2\pi\,10{,}000t)
$$

For the I branch,

$$
LO_I(t)=\cos(2\pi\,8{,}000t)
$$

After multiplication and low-pass filtering, the 18 kHz sum term is removed and the remaining component is approximately

$$
I(t)=\frac{1}{2}\cos(2\pi\,2{,}000t)
$$

### The Q Branch

If the second branch uses

$$
LO_Q(t)=\sin(2\pi\,8{,}000t)
$$

then

$$
\cos(2\pi\,10{,}000t)\sin(2\pi\,8{,}000t)=\frac{1}{2}\sin(2\pi\,18{,}000t)-\frac{1}{2}\sin(2\pi\,2{,}000t)
$$

After low-pass filtering,

$$
Q(t)=-\frac{1}{2}\sin(2\pi\,2{,}000t)
$$

If we reverse the sign of the sine LO, the sign of Q also reverses. This sign convention determines whether the resulting complex baseband tone appears at positive or negative frequency.

### GNU Radio I/Q Downconverter

The complete flowgraph is shown below.

![GNU Radio I/Q downconversion flowgraph](../figures/ch05/iq-downconversion-flowgraph.png)

The received 10 kHz signal feeds two Multiply blocks. The upper branch uses the cosine LO, the lower branch uses the sine LO, and both outputs pass through identical Low Pass Filters.

The filtered outputs are connected to **Float to Complex**:

- I goes to the real input,
- Q goes to the imaginary input.

The resulting complex signal is

$$
x_{BB}(t)=I(t)+jQ(t)
$$

The Time Sink shows that I and Q are both approximately 2 kHz and have amplitudes near 0.5, but they are separated by approximately $90^\circ$.

## 5.5 Complex Baseband and the Sign Convention

The original signal was at 10 kHz and the LO was at 8 kHz. After downconversion, the useful signal appears 2 kHz away from the LO.

Instead of continuing to process the original 10 kHz waveform, the receiver can work with a lower-frequency representation whose frequencies are measured relative to the LO or tuning frequency. When both I and Q are retained, this is a **complex baseband** representation.

Complex baseband preserves amplitude, phase, and the sign of frequency relative to the chosen centre frequency.

### Using a Positive Sine LO for Q

With the sign convention above,

$$
I(t)=\frac{1}{2}\cos(2\pi\,2{,}000t)
$$

$$
Q(t)=-\frac{1}{2}\sin(2\pi\,2{,}000t)
$$

so

$$
x_{BB}(t)=\frac{1}{2}\cos(2\pi\,2{,}000t)-j\frac{1}{2}\sin(2\pi\,2{,}000t)
$$

Using Euler's formula,

$$
\boxed{x_{BB}(t)=\frac{1}{2}e^{-j2\pi\,2{,}000t}}
$$

The baseband tone therefore appears at

$$
\boxed{-2\text{ kHz}}
$$

![Negative complex baseband frequency](../figures/ch05/iq-negative-baseband.png)

The Frequency Sink shows the dominant component on the negative-frequency side. The I-Q plane shows a circle with a radius of approximately 0.5.

### Reversing Q

Now reverse the sign of the Q-branch local oscillator, for example by changing its amplitude from `+1` to `-1`.

The I branch is unchanged, while Q becomes

$$
Q(t)=+\frac{1}{2}\sin(2\pi\,2{,}000t)
$$

The complex baseband signal is now

$$
x_{BB}(t)=\frac{1}{2}\cos(2\pi\,2{,}000t)+j\frac{1}{2}\sin(2\pi\,2{,}000t)
$$

or

$$
\boxed{x_{BB}(t)=\frac{1}{2}e^{j2\pi\,2{,}000t}}
$$

so the spectral peak moves to

$$
\boxed{+2\text{ kHz}}
$$

![Positive complex baseband frequency](../figures/ch05/iq-positive-baseband.png)

Nothing about the RF input or I branch has changed. Reversing Q reverses the direction of complex rotation and therefore the sign of the baseband frequency.

Different receiver architectures may adopt different I/Q sign conventions. What matters is that the convention is used consistently.

## 5.6 What the Static I-Q Plane Does Not Show

Compare the positive- and negative-frequency baseband figures. The Frequency Sink clearly distinguishes $-2$ kHz from $+2$ kHz, but the static I-Q plots both look like circles.

That is because a static constellation or I-Q scatter plot shows the **locations** visited by the samples. It does not, by itself, make the order of those samples obvious.

For one tone, the vector travels around the circle in one direction. For the other, it travels around the same circle in the opposite direction. The geometric path is the same, but the direction of travel is different.

> A static I-Q plot does not necessarily reveal the sign of a complex tone's frequency.

The Frequency Sink or an explicit phase-versus-time view makes that distinction much easier to see.

## 5.7 Frequencies Relative to the Tuning Frequency

The I/Q representation becomes especially useful when we think about an SDR tuned to a centre frequency $f_c$.

A signal below the tuning frequency can be represented at one side of zero in complex baseband, while a signal above the tuning frequency appears on the other side. The precise sign depends on the receiver's I/Q convention, but the two sides remain distinguishable.

For example, the RF offsets

$$
f_c-\Delta f\qquad\text{and}\qquad f_c+\Delta f
$$

can map to opposite complex-baseband frequencies around zero.

If we kept only one real component, positive and negative complex frequency would no longer be independently represented in the same way. Retaining I and Q preserves that directional information.

This is one of the main reasons complex samples are so useful throughout SDR.

## 5.8 Real Filters Leave Residual Mixer Products

In the complex-baseband spectrum, we may still see a much smaller component near the 18 kHz sum frequency, with its sign depending on the branch convention and display.

This does not mean the downconverter has failed. The Low Pass Filters strongly attenuate the sum-frequency term, but practical FIR filters do not have infinite stopband attenuation.

A small residual is therefore possible. This is a useful reminder that real filters do not have ideal brick-wall responses.

## 5.9 How This Relates to a Real SDR

Our GNU Radio receiver is deliberately simplified. A real SDR may perform frequency translation and quadrature processing in several different ways.

Some receivers use analog I/Q mixers before conversion. Others use low-IF architectures, direct RF sampling followed by digital downconversion, or other combinations of analog and digital processing.

So we should not assume that every SDR literally contains the two analog mixer branches used in our educational flowgraph.

The important point is the representation. By the time samples reach GNU Radio, SDR data is commonly represented as

$$
x[n]=I[n]+jQ[n]
$$

That complex representation lets later DSP stages work naturally with amplitude, phase, frequency offsets, filtering, modulation, demodulation, and many other operations.

## 5.10 GNU Radio Toolbox

This chapter mainly combined blocks we had already encountered into a more complete receiver structure.

### Multiply

The **Multiply** block multiplies corresponding input samples:

$$
y[n]=x_1[n]x_2[n]
$$

When the inputs are sinusoids, multiplication creates sum- and difference-frequency components. In this chapter, that operation acts as a simplified mixer.

### Low Pass Filter

The Low Pass Filter retains the desired low-frequency mixer product while suppressing the high-frequency sum term. Its cutoff and transition width therefore help determine which part of the downconverted spectrum remains available to later stages.

### Float to Complex

**Float to Complex** combines two real-valued streams into one complex stream:

$$
x[n]=I[n]+jQ[n]
$$

Here, its two inputs are the outputs of the quadrature mixer branches.

### Complex Displays

The QT GUI Frequency Sink lets us see whether the complex tone lies on the positive- or negative-frequency side. The QT GUI Constellation Sink shows the trajectory in the I-Q plane, while the Time Sink lets us compare I and Q directly.

### GUI Hint

As the number of displays grows, GUI Hint becomes useful for arranging them in a readable layout. It changes only the presentation of the generated interface, not the signal processing.

## 5.11 Explore Further

Before moving on, we can use the quadrature-downconversion flowgraph to test several predictions.

### Reverse Q

Change the Q oscillator amplitude from `+1` to `-1`. Before running the flowgraph, predict whether I will change and which side of zero the complex-frequency peak will occupy.

### Set Q to Zero

Set the Q branch amplitude to zero. The complex signal becomes

$$
x(t)=I(t)+j0
$$

Observe what happens to the I-Q plane and consider what information has been lost.

### Make the Two LO Signals Identical

Use cosine in both mixer branches instead of cosine and sine. The two branches are no longer in quadrature. Predict what should happen to I, Q, the I-Q plane, and the complex spectrum.

### Change the LO Frequency

Change

$$
f_{LO}=8\text{ kHz}
$$

to

$$
f_{LO}=9\text{ kHz}
$$

The expected difference frequency becomes

$$
f_{BB}=10-9=1\text{ kHz}
$$

Check whether the Frequency Sink agrees. This is the basic idea behind tuning by frequency translation.

### Change the Low-Pass Filter Cutoff

Reduce the cutoff frequency gradually. Once the desired baseband tone approaches the transition band or stopband, its amplitude should begin to fall. This connects filter design directly to usable receiver bandwidth.

## 5.12 What We Learned

This chapter connected three ideas.

First, we compared positive and negative complex frequencies. For the pair

$$
e^{j2\pi ft}\qquad\text{and}\qquad e^{-j2\pi ft}
$$

the I components are identical while the Q components have opposite signs. I and Q together therefore preserve the direction of complex rotation.

Second, we used multiplication to translate frequency. Mixing a 10 kHz signal with an 8 kHz local oscillator produced 2 kHz and 18 kHz components, and a Low Pass Filter retained the desired 2 kHz term.

Finally, we used two mixer branches in quadrature and combined their outputs as

$$
\boxed{x_{BB}(t)=I(t)+jQ(t)}
$$

This produced a complex representation whose frequency is measured relative to the LO. Reversing Q reversed the direction of complex rotation and moved the spectral peak from one side of zero to the other.

I and Q are therefore not an abstract mathematical convenience. They provide a practical representation that preserves amplitude, phase, and signed frequency information in a form that is extremely useful for SDR processing.

## 5.13 Connecting to the Next Chapter

Throughout the last few chapters, we have relied heavily on the Frequency Sink. It has shown us aliasing, mixer products, positive and negative frequencies, and the effect of quadrature downconversion.

So far, however, we have mostly treated the spectrum as something GNU Radio simply displays for us.

How can a collection of time-domain samples be converted into a frequency-domain representation? Why does a sinusoid produce a peak at a particular frequency, and what determines the detail we can see in the spectrum?

Those questions lead us to one of the most important tools in digital signal processing: the **Fourier transform**.