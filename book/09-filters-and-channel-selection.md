# Chapter 9: Filters and Channel Selection

In the previous chapter, we learned how mixing can move signals from one part of the spectrum to another. Moving a signal is useful, but a receiver usually contains more than the signal we want. Other channels, interference, mixer products, and noise may all be present at the same time.

The next problem is therefore selective rather than translational:

> How can we keep the part of the spectrum we want and suppress the rest?

That is the job of a filter.

A filter is sometimes described simply as something that removes noise, but that description is too narrow. A more useful view is that a filter treats different frequency regions differently. Some frequencies pass with little change, while others are attenuated.

In this chapter, we will work with low-pass, high-pass, band-pass, and band-reject filters. We will then look more closely at transition width, FIR taps, filter complexity, and decimation. The experiments will also show why filtering must come before downsampling when the sample rate is reduced.

## 9.1 A Three-Tone Test Signal

We need a signal containing several frequencies so that our filters have something to separate. For most of the chapter, we use three real cosine signals:

$$
x_1(t)=\cos(2\pi 2000t)
$$

$$
x_2(t)=\cos(2\pi 5000t)
$$

$$
x_3(t)=\cos(2\pi 9000t)
$$

Adding them gives

$$
x(t)=x_1(t)+x_2(t)+x_3(t)
$$

or

$$
x(t)=\cos(2\pi 2000t)+\cos(2\pi 5000t)+\cos(2\pi 9000t)
$$

We use

$$
f_s=32\text{ kS/s}
$$

so the Nyquist frequency is

$$
f_N=\frac{f_s}{2}=16\text{ kHz}
$$

All three tones lie below 16 kHz.

### Experiment 1: Build the Test Signal

The GNU Radio flowgraph uses three Signal Source blocks, an Add block, a Throttle, a QT GUI Time Sink, and a QT GUI Frequency Sink.

Use

```text
samp_rate = 32k
```

Configure the three Signal Sources as real cosines with frequencies 2 kHz, 5 kHz, and 9 kHz. Each has amplitude 1, offset 0, and initial phase 0.

![GNU Radio flowgraph for the three-tone test signal](../figures/ch09/ch09-exp1-multifrequency-flowgraph.png)

The time-domain waveform no longer resembles a single sinusoid because all three components are present simultaneously.

The frequency-domain view is much easier to interpret.

![Spectrum of the multi-frequency signal](../figures/ch09/ch09-exp1-multifrequency-spectrum.png)

Because the three sources are real cosines, the centered spectrum contains components at

$$
\pm2\text{ kHz},\quad \pm5\text{ kHz},\quad \pm9\text{ kHz}
$$

A real cosine satisfies

$$
\cos(2\pi f_0t)=\frac{1}{2}e^{j2\pi f_0t}+\frac{1}{2}e^{-j2\pi f_0t}
$$

so each tone contributes a positive- and negative-frequency component.

This three-tone signal will let us see clearly what each filter keeps and what it suppresses.

## 9.2 What a Filter Does

Let the input spectrum be

$$
X(f)
$$

and the filter frequency response be

$$
H(f)
$$

Then the output spectrum is

$$
Y(f)=X(f)H(f)
$$

This equation captures the basic idea of filtering. The filter scales different frequency components by different amounts.

If

$$
|H(f)|\approx1
$$

a component passes with little attenuation. If

$$
|H(f)|\approx0
$$

it is strongly suppressed.

The region intended to pass is the **passband**. The region intended to be strongly attenuated is the **stopband**. Between them is the **transition band**.

A practical finite-length filter cannot move from full transmission to full rejection at an infinitely sharp boundary. The change occurs over a finite frequency range, and that fact becomes important later in the chapter.

## 9.3 Experiment 2: Low-Pass Filtering

Suppose the 2 kHz tone is the signal we want. A low-pass filter is a natural choice because it passes lower frequencies and attenuates higher ones.

We use a cutoff frequency of

$$
f_c=3\text{ kHz}
$$

with the following GNU Radio settings:

```text
FIR Type:          Float -> Float (Decimating)
Decimation:        1
Gain:              1
Sample Rate:       samp_rate
Cutoff Freq:       3000
Transition Width:  500
Window:            Hamming
```

With decimation set to 1, the filter does not change the sample rate.

![GNU Radio low-pass filter flowgraph](../figures/ch09/ch09-exp2-lowpass-flowgraph.png)

The result is shown below.

![Low-pass filtering before and after comparison](../figures/ch09/ch09-exp2-lowpass-comparison.png)

Before filtering, the spectrum contains all three tone pairs. After filtering, the 2 kHz component remains while the 5 kHz and 9 kHz components are strongly attenuated.

The time-domain output also becomes much simpler because one sinusoidal component now dominates.

This experiment gives us two useful lessons. First, filtering is often easier to understand in the frequency domain. Second, practical filters **attenuate** unwanted components rather than making them mathematically vanish.

The settings also introduce several design parameters that will keep returning:

- **Gain** controls the overall scaling.
- **Sample Rate** tells GNU Radio how the specified frequencies relate to the sampled signal.
- **Cutoff Frequency** defines the nominal low-pass edge used by the design.
- **Transition Width** controls how rapidly the response moves from passband toward stopband.
- **Window** affects the FIR design, including transition behaviour, stopband attenuation, and tap count.

## 9.4 Experiments 3 to 5: Selecting and Rejecting Frequency Regions

The same basic idea can produce several different kinds of filters.

### Experiment 3: High-Pass Filtering

A high-pass filter attenuates lower frequencies and passes higher ones. We configure the filter so that the 9 kHz component remains while the 2 kHz and 5 kHz components are strongly reduced.

![GNU Radio high-pass filter flowgraph](../figures/ch09/ch09-exp3-highpass-flowgraph.png)

![High-pass filtering comparison](../figures/ch09/ch09-exp3-highpass-comparison.png)

The output spectrum is now dominated by the 9 kHz tone.

The low-pass and high-pass filters are both FIR filters. What changes is the shape of their frequency response.

### Experiment 4: Band-Pass Filtering and Channel Selection

Suppose the desired signal is the 5 kHz tone. It sits between the other two components, so neither a simple low-pass nor a simple high-pass response is appropriate.

A band-pass filter keeps a selected frequency interval while attenuating frequencies outside it. We configure the passband so that the 5 kHz component lies inside while the 2 kHz and 9 kHz components lie outside.

![GNU Radio channel-selection flowgraph](../figures/ch09/ch09-exp4-channel-flowgraph.png)

![Band-pass filtering and channel selection](../figures/ch09/ch09-exp4-channel-selection.png)

The output contains the real-signal pair around

$$
\pm5\text{ kHz}
$$

while the other two tones are strongly attenuated.

This is a simple example of **channel selection**.

A practical receiver often combines ideas from the previous chapter and this one. Frequency translation can first move the desired channel to a convenient location. Filtering can then isolate the frequency region we want before later processing.

### Experiment 5: Band-Reject Filtering

Sometimes the objective is the opposite. Instead of keeping one band, we want to suppress it.

A **band-reject** or **band-stop** filter attenuates a selected frequency region while leaving frequencies outside that region relatively unchanged. A very narrow band-reject filter is often called a **notch filter**.

Here we treat the 5 kHz component as interference and keep the 2 kHz and 9 kHz components.

![GNU Radio band-reject filter flowgraph](../figures/ch09/ch09-exp5-bandreject-flowgraph.png)

![Band-reject filtering comparison](../figures/ch09/ch09-exp5-bandreject-comparison.png)

The 5 kHz component is strongly suppressed while the other two remain.

The four common filter types can therefore be summarized as follows:

| Filter | Main purpose |
|---|---|
| Low-pass | Keep lower-frequency components |
| High-pass | Keep higher-frequency components |
| Band-pass | Keep a selected frequency band |
| Band-reject | Suppress a selected frequency band |

All four still follow the same underlying relationship:

$$
Y(f)=X(f)H(f)
$$

## 9.5 Experiment 6: Understanding Transition Width

An ideal low-pass filter would have an infinitely sharp boundary:

$$
H(f)=1\quad\text{for }|f|\leq f_c
$$

$$
H(f)=0\quad\text{for }|f|>f_c
$$

A finite-length FIR filter cannot implement that ideal response exactly. Its magnitude response changes over a transition region.

To make this visible, we modify the test signal so that one tone lies close to the low-pass edge. The tones are now approximately

$$
3.5,\quad5,\quad9\text{ kHz}
$$

while the nominal cutoff remains

$$
f_c=3\text{ kHz}
$$

We keep the sample rate at 32 kS/s and use a Hamming window. A QT GUI Range changes the transition width while the flowgraph runs.

![GNU Radio transition-width experiment flowgraph](../figures/ch09/ch09-exp6-transition-width-flowgraph.png)

We test transition widths including

```text
100 Hz
500 Hz
1000 Hz
2000 Hz
```

![Effect of transition width](../figures/ch09/ch09-exp6-transition-width-comparison.png)

With a narrow transition width, the response falls much more rapidly and the nearby 3.5 kHz tone is strongly attenuated. With a wider transition width, the change from passband to stopband is more gradual, so the same tone can experience less attenuation.

The exact attenuation at a particular frequency depends on the complete filter design, not only on one parameter. The experiment nevertheless makes the main trade-off visible:

> A narrower transition produces a sharper frequency response, but that sharpness requires a more demanding FIR filter.

## 9.6 Experiment 7: FIR Taps and Filter Complexity

An FIR filter calculates each output sample as a weighted sum of present and past input samples:

$$
y[n]=\sum_{k=0}^{N-1}h[k]x[n-k]
$$

The coefficients

$$
h[0],h[1],\ldots,h[N-1]
$$

are the **filter taps**.

This operation is convolution:

$$
y[n]=x[n]*h[n]
$$

The Fourier transform of the impulse response gives the frequency response:

$$
H(f)=\mathcal{F}\{h[n]\}
$$

This connects the sample-by-sample FIR calculation to the spectral behaviour we have been observing.

### Exposing the Taps in GNU Radio

Until now, the convenient Low Pass Filter block has designed and applied the coefficients for us. In this experiment, we separate those two jobs.

We use a **Low-pass Filter Taps** block to generate the coefficient vector and a **Decimating FIR Filter** to apply it.

![GNU Radio filter taps flowgraph](../figures/ch09/ch09-exp7-filter-taps-flowgr.png)

The taps block uses:

```text
ID:                lpf_taps
Gain:              1
Sample Rate:       samp_rate
Cutoff Frequency:  3k
Transition Width:  500
Window:            Hamming
```

The Decimating FIR Filter uses:

```text
Type:          Float -> Float (Real Taps)
Decimation:    1
Taps:          lpf_taps
Sample Delay:  0
```

There is no signal wire between these two blocks. `lpf_taps` is a variable containing the coefficient vector, and the FIR filter refers to that vector through its Taps field.

If the coefficient vector contains \(N\) values, then

$$
N=\operatorname{len}(lpf\_taps)
$$

For the 32 kS/s, 3 kHz cutoff, 500 Hz transition-width, Hamming-window design used in the experiment, GNU Radio generated approximately

```text
num_taps = 155
```

When a Blackman window was used with otherwise similar specifications, the observed tap count was approximately

```text
num_taps = 215
```

The exact number depends on the design method and window.

### Transition Width Versus Tap Count

With the Hamming window, the experiment produced:

| Transition Width | Number of Taps |
|---:|---:|
| 2000 Hz | 39 |
| 1000 Hz | 77 |
| 500 Hz | 155 |
| 200 Hz | 385 |
| 100 Hz | 771 |

The trend is clear. As the transition becomes narrower, the tap count rises sharply.

For this family of designs, the observed scaling is roughly consistent with

$$
N\propto\frac{f_s}{\Delta f}
$$

The proportionality constant depends on the window and design method.

A sharper filter therefore carries a computational cost. Each additional tap adds work to the FIR calculation. The useful design question is not simply how sharp a filter can be, but how sharp it actually needs to be.

Window choice is part of the same trade-off.

![Comparison of FIR filter windows](../figures/ch09/ch09-exp7-filter-windows-comparison.png)

Different windows trade transition width, stopband attenuation, and filter length differently. We already explored FFT windows in Chapter 6; here the same window idea appears in FIR filter design rather than spectral display.

## 9.7 Experiment 8: Filtering and Decimation

Filtering becomes even more important when we reduce the sample rate.

If the input sample rate is \(f_s\) and the decimation factor is \(D\), then

$$
f_{s,\text{out}}=\frac{f_s}{D}
$$

Starting from

$$
f_s=32\text{ kS/s}
$$

we obtain:

| Decimation \(D\) | Output Sample Rate | New Nyquist Frequency |
|---:|---:|---:|
| 1 | 32 kS/s | 16 kHz |
| 2 | 16 kS/s | 8 kHz |
| 4 | 8 kS/s | 4 kHz |
| 8 | 4 kS/s | 2 kHz |

The GNU Radio flowgraph uses the explicit filter taps with a Decimating FIR Filter.

![GNU Radio decimation flowgraph](../figures/ch09/ch09-exp8-decimation-flowgraph.png)

The decimation factor is controlled by a QT GUI Range. Downstream GUI blocks must use the **new** sample rate:

```text
QT GUI Time Sink Sample Rate: samp_rate/decimation
QT GUI Frequency Sink Bandwidth: samp_rate/decimation
```

That detail is essential because the samples may be correct while the plotted time or frequency axis is wrong if a downstream display still assumes the old rate.

The measured comparison is shown below.

![Effect of increasing the decimation factor](../figures/ch09/ch09-exp8-decimation-comparison.png)

For the same number of displayed samples, the visible time interval grows as the sample rate falls. That is why the Time Sink spans progressively more time as \(D\) increases.

The new Nyquist limit also shrinks. At \(D=4\), the output rate is 8 kS/s and the new Nyquist frequency is 4 kHz. A 2 kHz desired tone lies safely inside that range, while the original 5 kHz and 9 kHz components must be removed before downsampling.

The \(D=8\) case deserves special care. The output rate becomes 4 kS/s, so 2 kHz lies exactly at the Nyquist boundary. As we saw in Chapter 3, operating exactly at that boundary is phase-sensitive and not a robust design choice. In addition, a low-pass design intended to support decimation by 8 must suppress energy above the new 2 kHz Nyquist limit before samples are discarded. A 3 kHz low-pass specification is therefore not suitable as a safe anti-alias filter for this case.

So \(D=8\) is useful here as a boundary example, not as a recommended operating point for the existing 2 kHz tone and filter settings.

## 9.8 Experiment 8A: What Happens Without Anti-Alias Filtering?

Now we deliberately perform the sample-rate reduction incorrectly.

One branch uses the Decimating FIR Filter. The other uses **Keep 1 in N**, which simply keeps one sample out of every \(N\) input samples.

![GNU Radio flowgraph comparing filtered and unfiltered decimation](../figures/ch09/ch09-exp8a-decimation-without-filtering-flowgraph.png)

For the comparison,

$$
D=4
$$

so

$$
f_s'=\frac{32}{4}=8\text{ kS/s}
$$

and

$$
f_N'=4\text{ kHz}
$$

The original tones are at 2, 5, and 9 kHz. The 2 kHz component is inside the new Nyquist interval. The 5 kHz and 9 kHz components are not.

Without filtering, they alias.

The 5 kHz tone folds to

$$
|5-8|=3\text{ kHz}
$$

and the 9 kHz tone folds to

$$
|9-8|=1\text{ kHz}
$$

So direct downsampling should produce spectral components around

$$
\pm1,\quad\pm2,\quad\pm3\text{ kHz}
$$

The experiment confirms this.

![Comparison of filtering before decimation and direct downsampling](../figures/ch09/ch09-exp8a-filter-before-decimation-comparison.png)

In the Keep 1 in N path, the new 1 kHz and 3 kHz components are aliases. They were not present as original source frequencies.

In the Decimating FIR Filter path, the higher-frequency components are suppressed before samples are discarded, so aliasing is greatly reduced. Small residual components may remain because a finite FIR filter has finite stopband attenuation.

This gives us one of the most important practical rules in multirate DSP:

> **Filter first, then decimate.**

The official GNU Radio Decimating FIR Filter follows exactly this idea: when decimation is greater than 1, the filter must remove energy outside the frequency region that can be represented at the reduced output rate.

## 9.9 Sample Rate Changes Must Propagate Through the Flowgraph

Decimation changes more than the number of samples.

For decimation factor \(D\),

$$
f_s'=\frac{f_s}{D}
$$

Every downstream block that interprets time or frequency must use that new rate.

For a Frequency Sink, the appropriate bandwidth for the decimated stream is

```text
samp_rate/decimation
```

With 32 kS/s and \(D=4\), this becomes

$$
8\text{ kHz}
$$

so a centered display spans approximately

$$
-4\text{ kHz}\quad\text{to}\quad+4\text{ kHz}
$$

Leaving the sink configured for 32 kS/s does not change the samples themselves, but it labels the frequency axis incorrectly.

The same issue appears when comparing pre-decimation and post-decimation signals. If the two streams have different sample rates, separate Frequency Sinks are often clearer because each can use the correct bandwidth.

## 9.10 Common Filter Mistakes

Several mistakes from these experiments are worth recognizing because they recur in larger SDR receivers.

A **wrong sample rate** in the filter design shifts the intended cutoff and transition frequencies relative to the actual data. A **wrong cutoff** may suppress the desired signal even when the filter is working exactly as designed. An **unnecessarily narrow transition** can create a very long and computationally expensive FIR filter.

After decimation, failing to update the sample-rate-dependent GUI settings can make a correct signal look incorrectly scaled in time or frequency.

The most serious mistake is downsampling without sufficient anti-alias filtering. Frequencies outside the new Nyquist interval then fold into the retained spectrum. Once that aliasing has occurred, the receiver cannot determine from the samples alone whether a component is genuine or an alias.

## 9.11 GNU Radio Toolbox

This chapter uses several familiar blocks in more advanced roles.

| GNU Radio block | Purpose in this chapter |
|---|---|
| Low Pass Filter | Pass lower frequencies and attenuate higher frequencies |
| High Pass Filter | Pass higher frequencies and attenuate lower frequencies |
| Band Pass Filter | Keep a selected frequency region |
| Band Reject Filter | Suppress a selected frequency region |
| Low-pass Filter Taps | Generate an FIR coefficient vector |
| Decimating FIR Filter | Apply FIR filtering and downsampling together |
| Keep 1 in N | Downsample without automatically applying an anti-alias filter |
| QT GUI Range | Change transition width or decimation interactively |

The Low-pass Filter Taps block stores the designed coefficient vector in the variable named by its ID. The Decimating FIR Filter can then use that vector directly.

The Keep 1 in N block is useful for demonstrations because it exposes what plain sample dropping does. It should not be mistaken for a complete anti-aliased decimation chain.

## 9.12 Explore Further

The chapter becomes more useful when the filter parameters are treated as engineering choices rather than fixed settings.

A few worthwhile extensions are:

1. Move one test tone progressively closer to the low-pass transition region and observe how its attenuation changes.
2. Keep the same cutoff and transition width but switch among Hamming, Blackman, Hann, Rectangular, and Kaiser windows. Compare both the response and the generated tap count.
3. Repeat the tap-count experiment at another sample rate while keeping the transition width fixed in hertz. Observe how the required filter length changes.
4. For decimation by 4, deliberately weaken the anti-alias filter and watch residual high-frequency energy fold into the output.
5. Design a safer decimation-by-8 example using a desired signal comfortably below 2 kHz and an anti-alias filter whose stopband begins before the new Nyquist boundary.

For each change, it is useful to predict the result before running the flowgraph.

## 9.13 What We Learned

We began with three tones at 2, 5, and 9 kHz and learned how to control which parts of their spectrum survive.

Low-pass, high-pass, band-pass, and band-reject filters all implement different forms of the same basic idea:

$$
Y(f)=X(f)H(f)
$$

A practical filter needs a transition region. Making that transition narrower generally requires more FIR taps, which increases computation.

The FIR calculation itself is

$$
y[n]=\sum_{k=0}^{N-1}h[k]x[n-k]
$$

so the taps are not merely configuration values. They are the coefficients used directly in the sample-by-sample convolution.

We also connected filtering to sample-rate reduction. After decimation by \(D\),

$$
f_{s,\text{out}}=\frac{f_s}{D}
$$

and the new Nyquist range becomes smaller. Frequencies that will not fit inside that range must be sufficiently attenuated **before** samples are discarded.

Experiment 8A made the consequence visible. Direct downsampling by 4 caused the original 5 kHz and 9 kHz tones to alias to 3 kHz and 1 kHz. Filtering first greatly reduced those aliases.

The resulting receiver pattern is fundamental to SDR:

**frequency translation → channel filtering → decimation → later processing**

Each step prepares the signal for the next one.

## 9.14 Connecting to the Next Chapter

We now know how to shape a spectrum deliberately. We can isolate a desired band, suppress an unwanted band, control transition sharpness, inspect FIR coefficients, and reduce the sample rate safely after filtering.

But the FIR equation raises a deeper question:

$$
y[n]=\sum_{k=0}^{N-1}h[k]x[n-k]
$$

Why does a weighted sum of delayed input samples produce the filtered output?

And why do the taps describe the behaviour of the system?

To answer that, we will look at filters from a different direction. Instead of beginning with frequency response, we will begin with the simplest possible discrete-time input: an impulse.

The output produced by that impulse is the **impulse response**. Once we understand it, the FIR taps and the operation of convolution become much more intuitive.

That is the subject of Chapter 10: **Impulse Response and Convolution**.