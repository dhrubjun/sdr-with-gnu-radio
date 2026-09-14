# Chapter 6: From Time Domain to Frequency Domain

In the previous chapters, we used the frequency domain repeatedly. We watched mixer products move, compared positive and negative complex frequencies, and used the Frequency Sink to understand I/Q signals.

Until now, however, we have mostly treated the spectrum as something GNU Radio displays for us.

This chapter looks more closely at what that display means and how it is produced.

The central question is simple:

> How can several frequencies exist inside one waveform?

We will begin with an experiment, then connect what we observe to the Fourier transform, the DFT and the FFT. After looking briefly inside a radix-2 FFT, we will return to practical GNU Radio experiments involving FFT size, spectral leakage, window functions and the waterfall display.

## 6.1 One Signal, Two Ways of Looking at It

A time-domain plot answers the question:

> How does the signal change with time?

That view is useful for seeing oscillations, pulses, delays, clipping, transients and many other behaviours.

The frequency domain asks a different question:

> What frequency components are present in the signal?

These are not two different signals. They are two different descriptions of the same signal.

| View | Main question |
|---|---|
| Time domain | How does the signal change with time? |
| Frequency domain | What frequency components are present? |

A waveform that looks complicated in time can sometimes have a very simple frequency-domain description. Our first experiment makes that visible.

## 6.2 Experiment 1: Three Simple Tones, One Complicated Waveform

We begin with three cosine waves:

$$
x_1(t)=\cos(2\pi 1000t)
$$

$$
x_2(t)=\cos(2\pi 3000t)
$$

$$
x_3(t)=\cos(2\pi 6000t)
$$

We add them:

$$
x(t)=x_1(t)+x_2(t)+x_3(t)
$$

Before running the flowgraph, we can make a simple prediction. In the time domain, the sum should no longer look like a single sinusoid. In the frequency domain, we should still be able to identify the three frequencies that were deliberately placed in the signal.

![GNU Radio flowgraph for generating and observing three tones](../figures/ch06/ch06-three-tone-flowgraph.png)

The combined signal is sent to both a QT GUI Time Sink and a QT GUI Frequency Sink. Both displays therefore observe the same stream of samples.

![The combined three-tone signal in the time and frequency domains](../figures/ch06/ch06-three-tone-time-frequency.png)

The time-domain waveform looks much more complicated than any of the original cosines. The frequency-domain view, however, reveals the components immediately.

Because the sources are real-valued cosines, each tone has a symmetric pair of complex-frequency components. A real cosine can be written as

$$
\cos(2\pi f_0t)=\frac{1}{2}e^{j2\pi f_0t}+\frac{1}{2}e^{-j2\pi f_0t}
$$

so a centred two-sided spectrum contains components at

$$
+f_0 \qquad\text{and}\qquad -f_0
$$

for each cosine.

Our three tones therefore appear at

$$
\pm1\text{ kHz},\qquad \pm3\text{ kHz},\qquad \pm6\text{ kHz}
$$

We already developed the positive- and negative-frequency interpretation in the previous chapters. Here, the important observation is simpler:

> A waveform that looks complicated in time can have a simple frequency-domain description.

## 6.3 What Is the Fourier Transform Doing?

Suppose we are given an unknown signal and want to know whether it contains a particular frequency.

One possible idea is to compare the signal against a sinusoidal reference at that frequency. If the frequency is strongly present, the comparison should reinforce. If it is absent, positive and negative contributions should tend to cancel.

Fourier analysis formalises this idea across frequency.

For a continuous-time signal, the Fourier transform is

$$
X(f)=\int_{-\infty}^{\infty}x(t)e^{-j2\pi ft}\,dt
$$

and the inverse Fourier transform is

$$
x(t)=\int_{-\infty}^{\infty}X(f)e^{j2\pi ft}\,df
$$

We do not need to derive these integrals here. The physical idea matters more at this stage.

The time-domain function $x(t)$ tells us how the signal changes with time. The frequency-domain function $X(f)$ tells us how the signal is distributed across frequency.

The Fourier transform does not create new frequencies. It provides another representation of the same signal.

## 6.4 From the Fourier Transform to the DFT

An SDR works with sampled data rather than an infinitely long continuous waveform.

Suppose we take a finite block containing $N$ samples:

$$
x[0],x[1],x[2],\ldots,x[N-1]
$$

The Discrete Fourier Transform, or DFT, gives us a frequency-domain representation of that block:

$$
X[k]=\sum_{n=0}^{N-1}x[n]e^{-j2\pi kn/N},\qquad k=0,1,\ldots,N-1
$$

The symbols have straightforward roles:

- $n$ is the sample index,
- $N$ is the number of samples in the block,
- $k$ is the frequency-bin index,
- $X[k]$ is the complex result for bin $k$.

The complex exponential

$$
e^{-j2\pi kn/N}
$$

acts as a frequency-dependent reference. A useful intuition is that the DFT checks how strongly the finite block of samples matches each complex sinusoidal pattern represented by the available bins.

When a component matches a bin well, the contributions add coherently. When it does not, the rotating complex contributions tend to cancel more strongly.

The DFT output is generally complex. Its magnitude

$$
|X[k]|
$$

contains information about the strength of the component, while its angle

$$
\angle X[k]
$$

contains phase information.

### A Practical Warning About Magnitude

The raw value of $|X[k]|$ is not automatically the physical amplitude of a sinusoid, and $|X[k]|^2$ is not automatically calibrated RF power.

The displayed level can depend on FFT length, normalisation, window choice, one-sided or two-sided scaling, and the way a particular display converts the FFT result into amplitude or power.

For now, our main goals are to understand where spectral components appear, how their shapes change, and how they move when we change signal parameters.

## 6.5 DFT and FFT: The Same Transform, Different Computation

The DFT is the mathematical operation we want to calculate.

The FFT, or Fast Fourier Transform, is a family of efficient algorithms for calculating that same DFT.

A direct evaluation of the DFT requires on the order of

$$
O(N^2)
$$

operations, while common FFT algorithms reduce the computational growth to roughly

$$
O(N\log_2N)
$$

for power-of-two transform lengths.

This matters in SDR because FFTs are often calculated continuously on blocks containing hundreds or thousands of samples.

The FFT gains its efficiency by exploiting the regular structure and symmetry of the complex exponential terms instead of recalculating closely related operations independently.

## 6.6 Looking Inside a Radix-2 FFT

We do not normally build FFT algorithms manually in GNU Radio. Still, looking briefly inside one helps us understand words such as *twiddle factor*, *butterfly* and *bit reversal* when they appear in DSP literature.

A radix-2 FFT is convenient when

$$
N=2^m
$$

Examples include 8, 32, 1024 and 2048 points.

One common organisation is the radix-2 Decimation-in-Time, or DIT, FFT.

### Even and Odd Decomposition

DIT begins by separating the input into even- and odd-indexed samples:

$$
x[0],x[2],x[4],\ldots
$$

and

$$
x[1],x[3],x[5],\ldots
$$

Define the basic twiddle factor as

$$
W_N=e^{-j2\pi/N}
$$

The $N$-point DFT can then be written in terms of two $N/2$-point DFTs:

$$
X[k]=E[k]+W_N^kO[k]
$$

$$
X[k+N/2]=E[k]-W_N^kO[k]
$$

where $E[k]$ is the DFT of the even-indexed samples and $O[k]$ is the DFT of the odd-indexed samples.

The same decomposition can be applied repeatedly to the smaller transforms.

### Twiddle Factors

The quantity

$$
W_N^k=e^{-j2\pi k/N}
$$

is called a **twiddle factor**.

Using Euler's relation,

$$
e^{j\theta}=\cos\theta+j\sin\theta
$$

we can write

$$
W_N^k=\cos\left(\frac{2\pi k}{N}\right)-j\sin\left(\frac{2\pi k}{N}\right)
$$

A twiddle factor is therefore a unit-magnitude complex rotation. The same rotating-vector mathematics we used for I/Q signals appears again inside the FFT.

### The Butterfly

The repeated computation used in a radix-2 FFT is called a **butterfly**.

For inputs $A$ and $B$, first form

$$
T=BW_N^k
$$

then calculate

$$
Y_{\text{upper}}=A+T
$$

and

$$
Y_{\text{lower}}=A-T
$$

![Basic radix-2 FFT butterfly operation](../figures/ch06/ch06-fft-butterfly.png)

The butterfly therefore performs one complex rotation followed by an addition and a subtraction.

For example, let

$$
A=3+j
$$

$$
B=1-j
$$

and

$$
W_N^k=-j
$$

Then

$$
T=(1-j)(-j)=-1-j
$$

so

$$
Y_{\text{upper}}=(3+j)+(-1-j)=2
$$

and

$$
Y_{\text{lower}}=(3+j)-(-1-j)=4+2j
$$

### An 8-Point Example

Because

$$
8=2^3
$$

an 8-point radix-2 FFT has three stages. In general,

$$
\text{Number of radix-2 stages}=\log_2N
$$

A common iterative DIT implementation arranges its inputs in bit-reversed order. For an 8-point FFT:

| Normal index | Binary | Bits reversed | New index |
|---:|:---:|:---:|---:|
| 0 | 000 | 000 | 0 |
| 1 | 001 | 100 | 4 |
| 2 | 010 | 010 | 2 |
| 3 | 011 | 110 | 6 |
| 4 | 100 | 001 | 1 |
| 5 | 101 | 101 | 5 |
| 6 | 110 | 011 | 3 |
| 7 | 111 | 111 | 7 |

The corresponding input order is

$$
x[0],x[4],x[2],x[6],x[1],x[5],x[3],x[7]
$$

![Eight-point radix-2 decimation-in-time FFT](../figures/ch06/ch06-8point-dit-fft.png)

Each stage contains $N/2=4$ butterflies, so the complete 8-point transform contains

$$
\frac{N}{2}\log_2N=4\times3=12
$$

butterflies.

Bit reversal is not a property of the DFT itself. It is an organisational feature of certain FFT implementations. Library FFT routines normally hide these details from us.

Decimation in Frequency, or DIF, is another way of organising the radix-2 calculation. DIT and DIF both calculate the same DFT; they arrange the intermediate work differently.

For the rest of this book, we do not need to construct butterflies manually. GNU Radio's FFT block and numerical libraries handle these calculations for us.

## 6.7 FFT Bins and Observation Time

An $N$-point DFT produces $N$ discrete frequency samples, commonly called **FFT bins**.

If the sample rate is $f_s$, adjacent bins are separated by

$$
\Delta f=\frac{f_s}{N}
$$

For example, if

$$
f_s=32\,000\text{ samples/s}
$$

and

$$
N=1024
$$

then

$$
\Delta f=\frac{32000}{1024}=31.25\text{ Hz}
$$

For a fixed sample rate, increasing $N$ makes the frequency grid denser:

$$
N\uparrow\quad\Rightarrow\quad\Delta f\downarrow
$$

But a larger transform also uses a longer block of actual samples. The observation time is

$$
T_{\text{obs}}=\frac{N}{f_s}
$$

This gives us a useful connection:

$$
\Delta f=\frac{1}{T_{\text{obs}}}
$$

when $N$ actual samples are used without zero-padding.

### Bin Spacing Is Not the Whole Story

It is tempting to call $\Delta f$ the frequency resolution. That is useful as an initial intuition, but practical resolution also depends on the observation interval and the window applied to the samples.

| Property | Mainly affected by | Meaning |
|---|---|---|
| Bin spacing | $f_s/N$ | Distance between FFT frequency samples |
| Main-lobe width | Observation length and window | Width of a spectral component's dominant lobe |
| Sidelobe level | Window | Amount of spectral spreading away from the main lobe |

Two nearby tones do not automatically become clearly distinguishable merely because their separation is slightly larger than one FFT-bin interval.

## 6.8 Experiment 2: Building the FFT Chain Explicitly

Until now, the QT GUI Frequency Sink has performed the spectral analysis and display internally. In this experiment, we expose the main processing stages ourselves.

The signal path is:

**Signal Source → Throttle → Stream to Vector → FFT → Complex to Mag² → QT GUI Vector Sink**

![GNU Radio flowgraph for explicit FFT processing](../figures/ch06/ch06-explicit-fft-flowgraph.png)

### Stream to Vector

The Signal Source produces a continuous stream:

```text
x[0], x[1], x[2], x[3], ...
```

An $N$-point FFT operates on a block containing $N$ samples. With

$$
N=1024
$$

Stream to Vector groups consecutive samples into vectors of length 1024 before passing them to the FFT block.

This is an important practical point:

> An FFT repeatedly processes finite blocks of samples. It does not transform an infinitely long stream all at once.

### FFT Configuration

For this experiment, we use a sample rate of 32 kS/s and an FFT size of 1024. The vector display is configured to show a centred frequency axis from approximately $-16$ kHz to $+16$ kHz.

The bin spacing is

$$
\Delta f=\frac{32000}{1024}=31.25\text{ Hz}
$$

GNU Radio's FFT block also provides a shift option for placing DC at the centre of a complex spectrum. The display and FFT ordering must be configured consistently so that the vector indices map to the intended frequency axis.

### Complex to Mag²

The FFT output is complex:

$$
X[k]
$$

Complex to Mag² calculates

$$
|X[k]|^2
$$

for each FFT bin. The QT GUI Vector Sink then plots those real values against the configured frequency positions.

The vertical scale here is raw magnitude-squared. It is not calibrated power in watts or dBm, and it should not be compared directly with the relative dB scale of the QT GUI Frequency Sink.

### Real 1 kHz Cosine

First use a real 1 kHz cosine:

$$
x(t)=\cos(2\pi1000t)
$$

![Explicit FFT of a 1 kHz real cosine showing components at positive and negative frequencies](../figures/ch06/ch06-explicit-fft-real-cosine.png)

The spectrum contains components at

$$
-1\text{ kHz}\qquad\text{and}\qquad+1\text{ kHz}
$$

as expected for a real cosine.

### Complex 1 kHz Tone

Now use a complex tone

$$
x(t)=e^{j2\pi1000t}
$$

![Explicit FFT of a 1 kHz complex tone showing a single positive-frequency component](../figures/ch06/ch06-explicit-fft-complex-tone.png)

Only the positive-frequency component remains:

$$
+1\text{ kHz}
$$

The comparison is useful:

| Input signal | FFT result |
|---|---|
| Real 1 kHz cosine | Components at $-1$ kHz and $+1$ kHz |
| Complex 1 kHz tone | Component at $+1$ kHz |

This is the same positive- and negative-frequency behaviour we studied with I/Q signals, now observed using the FFT block directly.

The experiment also connects three levels of understanding:

**DFT equation → efficient FFT algorithm → GNU Radio FFT block**

The DFT tells us what is being calculated. The FFT tells us how it can be calculated efficiently. The GNU Radio block gives us a practical implementation that we can place inside a signal-processing chain.

## 6.9 Experiment 3: What Changes When We Increase FFT Size?

We now generate two cosine tones at

$$
1.0\text{ kHz}\qquad\text{and}\qquad1.1\text{ kHz}
$$

Their separation is

$$
100\text{ Hz}
$$

and the sample rate remains

$$
f_s=32\text{ kS/s}
$$

![GNU Radio flowgraph for investigating FFT frequency resolution](../figures/ch06/ch06-fft-resolution-flowgraph.png)

### FFT Size 32

For

$$
N=32
$$

we have

$$
\Delta f=\frac{32000}{32}=1000\text{ Hz}
$$

The two tones are only 100 Hz apart, so this transform provides very little frequency detail around them.

![With an FFT size of 32, the two closely spaced tones cannot be clearly separated](../figures/ch06/ch06-fft-resolution-32.png)

### FFT Size 256

For

$$
N=256
$$

we obtain

$$
\Delta f=\frac{32000}{256}=125\text{ Hz}
$$

The frequency grid is much denser, and the two components begin to become distinguishable, although their spectral shapes can still overlap.

![With an FFT size of 256, the two nearby tones begin to separate](../figures/ch06/ch06-fft-resolution-256.png)

### FFT Size 2048

Finally,

$$
N=2048
$$

gives

$$
\Delta f=\frac{32000}{2048}=15.625\text{ Hz}
$$

![With an FFT size of 2048, the 1.0 kHz and 1.1 kHz tones are much more clearly separated](../figures/ch06/ch06-fft-resolution-2048.png)

The two components are now much easier to distinguish.

The extra detail did not appear for free. A larger FFT uses a longer block of actual samples:

| FFT size | Bin spacing | Observation time |
|---:|---:|---:|
| 32 | 1000 Hz | 1 ms |
| 256 | 125 Hz | 8 ms |
| 2048 | 15.625 Hz | 64 ms |

This gives us an important engineering lesson:

> Finer frequency detail from actual samples generally requires a longer observation interval.

## 6.10 Zero-Padding, Frequency Span and dB

Several practical ideas are easy to confuse with FFT size, so it is useful to separate them.

### Zero-Padding

Suppose we collect only 256 actual samples but append zeros before calculating a 2048-point FFT.

The FFT now evaluates a denser frequency grid, so the plotted spectrum may look smoother. But the observation still contains only 256 measured samples.

Zero-padding therefore does not create new information or provide the same resolving ability as observing 2048 actual samples.

> Zero-padding gives a denser frequency grid, not a longer observation of the signal.

### Frequency Span

For a sampled complex-baseband signal with sample rate $f_s$, a centred full spectrum commonly spans approximately

$$
-\frac{f_s}{2}\quad\text{to}\quad+\frac{f_s}{2}
$$

At 32 kS/s, this corresponds to approximately

$$
-16\text{ kHz}\quad\text{to}\quad+16\text{ kHz}
$$

This is the available sampled frequency span. It is not necessarily the occupied bandwidth of the signal.

With actual SDR hardware, the centre of this display may correspond to a tuned RF frequency rather than 0 Hz. The FFT bins then represent offsets around that centre frequency.

### Why Spectrum Displays Use dB

Spectral components can differ by large ratios. A logarithmic scale allows strong and weak components to appear on the same display.

For an amplitude ratio,

$$
A_{\text{dB}}=20\log_{10}\left(\frac{A}{A_{\text{ref}}}\right)
$$

For a power ratio,

$$
P_{\text{dB}}=10\log_{10}\left(\frac{P}{P_{\text{ref}}}\right)
$$

Useful reference points include approximately $-6$ dB for half the amplitude and approximately $-3$ dB for half the power.

A dB value in a GUI is not automatically a dBm measurement. dBm is an absolute power unit referenced to 1 mW. Unless the complete SDR measurement chain has been calibrated, the Frequency Sink should be treated as a relative spectral display rather than an absolute RF power meter.

## 6.11 Experiment 4: Spectral Leakage

A pure sinusoid might seem as though it should always produce one perfectly sharp FFT line. In practice, its energy can spread across neighbouring bins.

This is **spectral leakage**.

A tone lies exactly on an FFT bin when

$$
f_{\text{tone}}=k\frac{f_s}{N}=k\Delta f
$$

for some integer $k$.

### Bin-Centred Tone

For the selected sample rate and FFT size, first choose a tone that satisfies the bin-centred condition.

![Spectrum of a bin-centred tone](../figures/ch06/ch06-bin-centered-tone.png)

Its energy is concentrated strongly at the expected bin location or locations.

### Move the Tone Off the Bin

Next choose a tone that does not fall exactly on an FFT-bin frequency. In the saved experiment, 1.1 kHz is the off-bin example for the chosen configuration.

![GNU Radio flowgraph used to investigate spectral leakage](../figures/ch06/ch06-spectral-leakage-flowgraph.png)

![An off-bin 1.1 kHz tone spreads energy into neighbouring FFT bins](../figures/ch06/ch06-spectral-leakage-1100hz.png)

The tone has not physically turned into many separate sinusoids. The spreading comes from the finite observation used by the FFT.

### Why Leakage Appears

The FFT sees only a finite block of samples. One way to interpret the DFT is to imagine that finite block repeating periodically.

If the beginning and end of the block join smoothly, the repeated sequence can remain continuous. If they do not match, the repeated sequence contains a discontinuity at each boundary.

Those discontinuities require additional spectral components in the finite-block representation, so energy spreads into other bins.

More formally, selecting a finite block is equivalent to multiplying the signal by a window in time. Multiplication in time corresponds to convolution in frequency, so the ideal signal spectrum is shaped by the spectrum of that window.

This leads directly to window functions.

## 6.12 Experiment 5: Window Functions

Before the FFT, we can multiply the sample block by a window $w[n]$:

$$
x_w[n]=x[n]w[n]
$$

The window changes the weighting of samples across the finite observation interval. Many useful windows taper the edges so that the block boundaries contribute less abruptly.

The trade-off appears in the frequency domain. A window affects the main-lobe width, sidelobe levels, leakage behaviour and amplitude characteristics of the spectral estimate.

There is no universally best window.

![GNU Radio flowgraph for comparing FFT window functions](../figures/ch06/ch06-window-comparison-flowgraph.png)

In this experiment, we keep the signal and FFT settings fixed and compare six windows:

1. Rectangular
2. Hann
3. Hamming
4. Blackman-Harris
5. Kaiser
6. Flat-top

![Comparison of six FFT window functions](../figures/ch06/ch06-window-comparison.png)

### Rectangular

A rectangular window gives equal weight to every sample. It provides a narrow main lobe, but its sidelobes are relatively high. Off-bin tones can therefore produce substantial leakage.

### Hann

The Hann window tapers smoothly to zero at the edges. Its sidelobes are much lower than those of the rectangular window, at the cost of a wider main lobe.

### Hamming

The Hamming window uses a different taper and produces a different compromise between main-lobe width and sidelobe behaviour.

### Blackman-Harris

Blackman-Harris strongly suppresses sidelobes. This can help when a weak component lies near a much stronger one, although the main lobe becomes wider.

### Kaiser

The Kaiser window is adjustable through a parameter commonly called $\beta$. Increasing $\beta$ generally gives stronger sidelobe suppression while widening the main lobe.

### Flat-Top

The flat-top window is designed to improve amplitude estimation near spectral peaks when the FFT scaling is handled appropriately. Its main lobe is broad, so it is usually not the first choice when the main objective is separating very closely spaced tones.

The signal itself has not changed during this experiment. Only the analysis window changed, yet the displayed spectral shape changed significantly.

That is an important lesson:

> The spectrum we observe depends on both the signal and the way we analyse the finite block of samples.

## 6.13 Averaging and the Waterfall

Real received signals are rarely as clean and stationary as our generated tones.

### FFT Averaging

Successive spectral estimates can fluctuate, especially in the presence of noise. Averaging smooths those changes and can make persistent components easier to see.

The trade-off is response time. More averaging produces a steadier display, but the display reacts more slowly when the signal changes.

### Experiment 6: Watching Frequency Change Over Time

A normal Frequency Sink shows the current spectrum well, but it does not preserve spectral history. Once a tone moves to another frequency, its old location disappears from the current trace.

A waterfall solves that problem by stacking successive spectral estimates over time.

In this experiment, a QT GUI Range controls the frequency of a cosine while both a Frequency Sink and a Waterfall Sink observe the same signal. Because the flowgraph is software-only, a Throttle block controls the processing rate.

![GNU Radio flowgraph for observing frequency evolution over time](../figures/ch06/ch06-frequency-evolution-flowgraph.png)

![Frequency evolution shown using the Waterfall and Frequency Sinks](../figures/ch06/ch06-frequency-evolution-waterfall.png)

The Frequency Sink shows the current spectral estimate. The Waterfall Sink preserves earlier estimates, so frequency changes remain visible as a history.

A useful way to think about the waterfall is that each horizontal spectral slice represents another FFT-based estimate, and those slices are stacked over time. Depending on the GUI orientation and settings, one axis represents frequency, another represents time, and colour represents spectral magnitude.

This makes several patterns easy to recognise:

- a constant-frequency signal remains at one frequency,
- a drifting signal moves gradually,
- a chirp forms a sloped trace,
- a short transmission appears only for a limited duration,
- a wideband signal occupies a broader frequency region.

The waterfall therefore adds something the ordinary Frequency Sink does not provide: **spectral history**.

## 6.14 GNU Radio Toolbox

This chapter gives several familiar GNU Radio controls a clearer signal-processing meaning.

| Block or setting | Role |
|---|---|
| QT GUI Frequency Sink | Calculates and displays a spectrum for convenient observation |
| Stream to Vector | Groups a stream into fixed-length vectors for block processing |
| FFT | Calculates the DFT efficiently for each input vector |
| Complex to Mag² | Converts complex FFT values to $|X[k]|^2$ |
| QT GUI Vector Sink | Displays vector values directly against a configurable x-axis |
| QT GUI Waterfall Sink | Displays successive spectra over time |
| FFT Size | Sets the number of samples used in each transform |
| Window Type | Controls how the finite sample block is weighted |
| Averaging | Smooths successive spectral estimates |
| Center Frequency | Sets the frequency represented at the centre of the display |
| Bandwidth | Maps the spectral bins onto the displayed frequency axis |

The QT GUI Frequency Sink is the most convenient choice when we simply want to inspect a spectrum. Using the FFT block directly is useful when the FFT results need to feed later processing such as detection, estimation, channelisation or classification.

## 6.15 Explore Further

The best way to reinforce these ideas is to change one parameter at a time and predict the result before running the flowgraph.

1. Use the two closely spaced tones and reduce the FFT size. Calculate $\Delta f=f_s/N$ first and predict how the display will change.

2. Calculate the bin spacing, choose one tone at an exact bin frequency and another between bins, then compare their spectra.

3. Keep the signal unchanged and switch among Rectangular, Hann, Hamming, Blackman-Harris, Kaiser and Flat-top windows. Compare both the main-lobe width and the sidelobe behaviour.

4. Keep $N$ fixed and increase the sample rate. Predict what happens to both $\Delta f$ and $T_{\text{obs}}$.

5. Increase the Frequency Sink averaging, then change the signal quickly. Compare display smoothness with response speed.

6. Return to the explicit FFT flowgraph. Compare a real 1 kHz cosine with a complex 1 kHz tone and observe what happens to the negative-frequency component.

7. Move a tone between several frequencies while watching both the Frequency Sink and Waterfall Sink. Compare what the two displays retain.

## 6.16 What We Learned

We began with a waveform made from several simple tones and saw that the time and frequency domains provide different views of the same signal.

Fourier analysis gives us the mathematical connection between those views. For sampled data, the DFT evaluates a finite block at discrete frequency bins, while the FFT provides an efficient way to calculate the same transform.

Looking briefly inside a radix-2 FFT showed that its efficiency comes from repeatedly reusing smaller calculations. Twiddle factors are complex rotations, butterflies combine intermediate values, and implementation details such as bit reversal help organise the computation.

In GNU Radio, the FFT becomes practical signal processing. Stream to Vector creates finite blocks, the FFT block transforms them, Complex to Mag² provides a magnitude-squared representation, and a Vector Sink can display the result directly.

We also saw that FFT size affects both bin spacing and observation time:

$$
\Delta f=\frac{f_s}{N}
$$

$$
T_{\text{obs}}=\frac{N}{f_s}
$$

A denser FFT grid does not automatically mean better physical resolution. Window shape and observation length also matter, and zero-padding cannot replace a longer observation of the actual signal.

Spectral leakage appears because the FFT analyses a finite block. Window functions change the resulting main-lobe and sidelobe behaviour, so the choice of window should depend on what we are trying to measure.

Finally, we distinguished two useful spectrum displays. The Frequency Sink shows the current spectrum, while the Waterfall Sink shows how that spectrum evolves with time.

The frequency domain should now feel less like a graph that GNU Radio produces for us and more like a representation whose behaviour we can predict from the samples, FFT settings and analysis choices.

## 6.17 Connecting to the Next Chapter

Our experiments so far have used signals that are almost unrealistically clean.

Real receivers contain something else almost all the time: **noise**.

Noise raises the spectral background, disturbs time-domain waveforms and makes weak signals harder to distinguish. Later, it will also spread constellation points and affect symbol decisions.

The next question is therefore practical:

> How weak can a signal become before noise makes it difficult to detect or recover?

In the next chapter, we will study noise, noise floor and signal-to-noise ratio, and observe how noise appears in both the time and frequency domains.