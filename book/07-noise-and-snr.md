# Chapter 7: Noise, Noise Floor, and SNR

Until now, most of our signals have been unusually clean. We generated tones with exact frequencies and amplitudes, observed their spectra, and could usually identify every component without much difficulty.

Real receivers are different. Even when no obvious transmission is present, a spectrum display rarely becomes empty. Receiver electronics contribute noise. The environment contributes noise and interference. Thermal motion inside electronic components also produces noise.

A useful signal therefore rarely arrives by itself. A more realistic description is

$$
\text{Received signal}=\text{wanted signal}+\text{noise}+\text{other unwanted signals}
$$

In this chapter, we will focus on noise. We will first observe noise by itself, then add it to a known signal, measure signal and noise power, calculate signal-to-noise ratio, and finally investigate how receiver bandwidth affects the amount of noise we collect.

The main question is simple:

> How weak can a signal become before it disappears into the noise?

There is no single universal answer, but by the end of the chapter we will have the tools needed to discuss that question much more precisely.

## 7.1 What Do We Mean by Noise?

In signal processing, noise is an unwanted random component that interferes with the signal we are interested in.

A sinusoid is predictable. Once its amplitude, frequency, and phase are known, its future waveform is determined. Noise is different. Knowing one random sample does not generally tell us the exact value of the next one.

Instead of describing noise sample by sample, we use statistical properties. We can ask about its mean, variance, power, and how that power is distributed across frequency.

For our experiments, we will use **Gaussian noise**. Gaussian describes the statistical distribution of the sample amplitudes. For zero-mean Gaussian noise, values near zero occur more often than large positive or negative values.

The GNU Radio Noise Source uses its `Amplitude` parameter as the standard deviation of a real one-dimensional Gaussian noise process. Therefore, an amplitude of `1` does not restrict the samples to the range -1 to +1. Larger values can occur naturally.

We will also describe the noise as approximately **white**. White describes how the noise power is distributed across frequency. Ideally,

$$
S_n(f)=\text{constant}
$$

over the frequency range of interest.

Gaussian and white therefore describe different properties:

| Term | What it describes |
|---|---|
| Gaussian | Statistical distribution of sample amplitudes |
| White | Distribution of noise power across frequency |

Noise can be Gaussian without being white, and it can be white without having a Gaussian amplitude distribution.

In a sampled system, we do not observe unlimited bandwidth. With

$$
f_s=32\text{ kS/s}
$$

the represented Nyquist interval is approximately

$$
-16\text{ kHz}\leq f<+16\text{ kHz}
$$

so when we describe the GNU Radio noise as white, we mean that its spectral behaviour is approximately uniform across the finite band represented by the sampled system.

## 7.2 Experiment 1: Observing Gaussian Noise

Before adding noise to a useful signal, we will look at noise by itself.

A Noise Source generates real Gaussian noise. A Throttle controls the processing rate in this software-only flowgraph, and the same stream is observed in both a QT GUI Time Sink and QT GUI Frequency Sink.

We use

$$
f_s=32\text{ kS/s}
$$

with an initial noise amplitude of `1`.

![GNU Radio flowgraph for observing Gaussian noise in the time and frequency domains.](../figures/ch07/ch07-exp1-noise-flowgraph.png)

The important settings are:

| Block | Parameter | Setting |
|---|---|---|
| Variable | ID | `samp_rate` |
| Variable | Value | `32e3` |
| Noise Source | Output Type | Float |
| Noise Source | Noise Type | Gaussian |
| Noise Source | Amplitude | `1` |
| Noise Source | Seed | `0` |
| Throttle | Sample Rate | `samp_rate` |
| QT GUI Time Sink | Type | Float |
| QT GUI Time Sink | Sample Rate | `samp_rate` |
| QT GUI Frequency Sink | Type | Float |
| QT GUI Frequency Sink | FFT Size | `1024` |
| QT GUI Frequency Sink | Center Frequency | `0` |
| QT GUI Frequency Sink | Bandwidth | `samp_rate` |

For the first observation, frequency-sink averaging is disabled.

### Noise in the Time Domain

The Time Sink looks very different from the clean sinusoids used earlier. There is no obvious repeating waveform. The samples move irregularly above and below zero.

Individual samples can also exceed a magnitude of 1 even though the Noise Source amplitude is set to `1`. This is expected because the amplitude parameter sets the standard deviation of the Gaussian process, not a hard limit.

### Noise in the Frequency Domain

The Frequency Sink shows another important feature. Instead of producing one narrow spectral line, the noise occupies the displayed frequency range broadly.

![Gaussian noise in the time and frequency domains without FFT averaging.](../figures/ch07/ch07-exp1-noise-no-averaging.png)

The spectrum is not perfectly flat. It fluctuates from bin to bin because each FFT is based on a finite block of random samples.

A flat power spectral density is a statistical statement. It does not mean that every finite FFT of white noise must produce a perfectly horizontal line.

### What FFT Averaging Changes

The QT GUI Frequency Sink can average successive spectral estimates. Conceptually, we can think of several estimates

$$
S_1[k],\ S_2[k],\ S_3[k],\ldots
$$

being combined so that some of the random frame-to-frame variation is reduced.

With averaging enabled, the noise spectrum becomes visibly smoother:

![Gaussian noise spectrum with FFT averaging enabled.](../figures/ch07/ch07-exp1-noise-with-averaging.png)

The important distinction is that **FFT averaging does not remove noise from the underlying signal**. The time-domain samples are unchanged. Only the displayed spectral estimate becomes smoother.

More averaging therefore gives us a familiar trade-off:

$$
\text{More averaging}\longleftrightarrow\text{smoother display but slower response}
$$

This becomes useful when a persistent spectral component must be observed against a fluctuating noise background.

## 7.3 Experiment 2: A Signal Inside Noise

We now add noise to a familiar signal:

$$
x(t)=\cos(2\pi1000t)
$$

The received signal in our simulation is

$$
r(t)=x(t)+n(t)
$$

where \(n(t)\) is Gaussian noise.

A QT GUI Range controls the noise amplitude while the flowgraph is running.

![GNU Radio flowgraph for adding Gaussian noise to a 1 kHz cosine.](../figures/ch07/ch07-exp2-signal-plus-noise-flowgraph.png)

The important settings are:

| Block | Parameter | Setting |
|---|---|---|
| Signal Source | Output Type | Float |
| Signal Source | Waveform | Cosine |
| Signal Source | Frequency | `1e3` |
| Signal Source | Amplitude | `1` |
| Signal Source | Sample Rate | `samp_rate` |
| Noise Source | Output Type | Float |
| Noise Source | Noise Type | Gaussian |
| Noise Source | Amplitude | controlled by QT GUI Range |
| Add | Type | Float |
| Throttle | Sample Rate | `samp_rate` |
| QT GUI Frequency Sink | FFT Size | `1024` |
| QT GUI Frequency Sink | Bandwidth | `samp_rate` |

We test four noise amplitudes:

$$
A_n=0.1,\quad0.5,\quad1.0,\quad2.0
$$

At \(A_n=0.1\), the cosine remains easy to recognize in both the time and frequency domains.

At \(A_n=0.5\), the time-domain waveform becomes noticeably rougher, but the spectral components near \(\pm1\) kHz remain clear.

At \(A_n=1.0\), the noise is comparable in scale to the sinusoid. The waveform is heavily corrupted, but the frequency-domain peaks are still present.

At \(A_n=2.0\), the time-domain waveform is dominated by random fluctuations. Even then, the Frequency Sink can still show evidence of the persistent 1 kHz component.

![Effect of increasing Gaussian noise on a 1 kHz cosine for noise amplitudes 0.1, 0.5, 1.0, and 2.0.](../figures/ch07/ch07-exp2-signal-noise-comparison.png)

This gives us an important lesson:

> A signal that is difficult to recognize in the time domain may still be identifiable in the frequency domain.

The sinusoid concentrates energy at particular frequencies, while the approximately white noise spreads its energy broadly across the represented band.

## 7.4 Noise Floor and Spectral Averaging

The broadband background visible in the Frequency Sink is commonly called the **noise floor**.

A strong spectral component rises clearly above the surrounding background. As the signal becomes weaker, or the noise becomes stronger, the peak approaches that background and detection becomes more difficult.

The total noise power in a signal and the displayed FFT noise floor are related, but they are not identical quantities. The level shown by a spectrum display can depend on FFT size, window type, normalization, averaging, gain, bandwidth, and display configuration.

For this reason, an uncalibrated GNU Radio Frequency Sink should not automatically be treated as an absolute RF power measurement.

Now enable averaging in the Frequency Sink and repeat the four noise-amplitude cases.

![Signal and Gaussian noise observed with FFT averaging enabled for noise amplitudes 0.1, 0.5, 1.0, and 2.0.](../figures/ch07/ch07-exp2-signal-noise-averaged-comparison.png)

The broadband trace becomes smoother, while the persistent components near \(\pm1\) kHz remain at consistent frequencies.

This can make a stable tone easier to distinguish visually, but again, the received samples themselves have not been cleaned. Only the spectral display has changed.

## 7.5 From "Noisy" to Signal-to-Noise Ratio

Descriptions such as "clean," "noisy," or "hard to see" are useful while learning, but engineering measurements need something more precise.

The **signal-to-noise ratio**, or **SNR**, compares signal power with noise power:

$$
\mathrm{SNR}=\frac{P_s}{P_n}
$$

where \(P_s\) is signal power and \(P_n\) is noise power.

SNR is usually expressed in decibels:

$$
\mathrm{SNR}_{\mathrm{dB}}=10\log_{10}\left(\frac{P_s}{P_n}\right)
$$

If \(P_s=P_n\), the linear SNR is 1 and

$$
\mathrm{SNR}_{\mathrm{dB}}=0\text{ dB}
$$

If \(P_s<P_n\), the SNR in decibels is negative. Negative SNR does not mean negative power. It simply means that the noise power is greater than the signal power.

To understand the calculation properly, we will measure \(P_s\) and \(P_n\) directly from the samples.

## 7.6 Measuring Power from Samples

For a real discrete-time signal, average power can be estimated as

$$
P\approx\frac{1}{N}\sum_{n=0}^{N-1}x^2[n]
$$

Our amplitude-1 cosine has theoretical average power

$$
P_s=\frac{A^2}{2}=\frac{1^2}{2}=0.5
$$

In GNU Radio, we can measure this by sending the same Float stream to both inputs of a Multiply block:

$$
x[n]\times x[n]=x^2[n]
$$

A Moving Average block then averages those squared samples.

With

```text
Length = 1000
Scale = 1/1000
```

the block estimates power over a moving window of 1000 samples.

For the cosine, the measured value should settle near

$$
P_s=0.5
$$

### Real and Complex Power

This method is appropriate because the current experiment uses real-valued Float streams.

For a complex signal

$$
z[n]=I[n]+jQ[n]
$$

we instead use magnitude squared:

$$
|z[n]|^2=z[n]z^*[n]=I^2[n]+Q^2[n]
$$

GNU Radio provides blocks such as **Complex to Mag²** for this purpose.

### Gaussian-Noise Power

For zero-mean Gaussian noise with standard deviation \(\sigma\),

$$
P_n=E\{w^2[n]\}=\sigma^2
$$

For the real GNU Radio Gaussian Noise Source, the amplitude parameter is the standard deviation. Therefore,

$$
P_n=A_n^2
$$

in expectation.

For our four settings:

| Noise amplitude \(A_n\) | Expected noise power \(P_n\) |
|---:|---:|
| 0.1 | 0.01 |
| 0.5 | 0.25 |
| 1.0 | 1 |
| 2.0 | 4 |

This relationship is important:

$$
P_n\propto A_n^2
$$

Doubling noise amplitude therefore increases expected noise power by a factor of four.

## 7.7 Experiment 3: Measuring SNR in GNU Radio

The complete SNR-measurement flowgraph is shown below.

![GNU Radio flowgraph for measuring signal power, noise power, and SNR.](../figures/ch07/ch07_exp3_power_snr_flowgraph.png)

The signal branch performs

$$
x[n]\rightarrow x^2[n]\rightarrow\text{average}\rightarrow P_s
$$

and the noise branch performs

$$
w[n]\rightarrow w^2[n]\rightarrow\text{average}\rightarrow P_n
$$

The two estimates are then combined:

$$
P_s,P_n\rightarrow\frac{P_s}{P_n}\rightarrow10\log_{10}(\cdot)\rightarrow\mathrm{SNR}_{\mathrm{dB}}
$$

The important settings are:

| Setting | Value |
|---|---:|
| `samp_rate` | `32e3` |
| `avg_len` | `1000` |
| Moving Average Scale | `1.0/avg_len` |
| Divide | Float |
| Log10 | `n = 1`, `k = 0` |
| Multiply Const | `10` |

QT GUI Number Sinks display signal power, noise power, and SNR.

### Measured Results

The measurements from the experiment were approximately:

| Noise amplitude | Signal power | Noise power | Measured SNR |
|---:|---:|---:|---:|
| 0.1 | 0.5005 | 0.0090 | +17.43 dB |
| 0.5 | 0.5005 | 0.2285 | +3.40 dB |
| 1.0 | 0.4995 | 1.0298 | -3.13 dB |
| 2.0 | 0.5005 | 4.0843 | -9.13 dB |

![Measured signal power, noise power, and SNR for different Gaussian-noise amplitudes.](../figures/ch07/ch07_exp3_snr_vs_noise_amplitude.png)

The signal power remains close to 0.5 because the cosine itself is unchanged. The measured noise power follows the expected square-law trend.

Using

$$
P_s=0.5
$$

and

$$
P_n=A_n^2
$$

we predict

$$
\mathrm{SNR}_{\mathrm{dB}}=10\log_{10}\left(\frac{0.5}{A_n^2}\right)
$$

which gives:

| Noise amplitude | Theoretical SNR | Measured SNR |
|---:|---:|---:|
| 0.1 | +16.99 dB | +17.43 dB |
| 0.5 | +3.01 dB | +3.40 dB |
| 1.0 | -3.01 dB | -3.13 dB |
| 2.0 | -9.03 dB | -9.13 dB |

The agreement is good. Small differences are expected because the noise is random and the power estimate uses a finite moving window.

A longer averaging window generally gives a more stable estimate, but it responds more slowly when the signal or noise changes.

This is different from Frequency Sink averaging. The Moving Average block operates on the actual stream of squared samples and produces a power estimate. Frequency Sink averaging only smooths successive spectral displays.

### A Useful 6 dB Rule

If the noise amplitude doubles,

$$
A_n\rightarrow2A_n
$$

then the expected noise power increases by four:

$$
P_n\rightarrow4P_n
$$

With signal power fixed, the SNR falls by

$$
10\log_{10}(4)\approx6.02\text{ dB}
$$

So:

> Doubling Gaussian-noise amplitude reduces SNR by approximately 6 dB when signal power remains unchanged.

## 7.8 Noise Power Depends on Bandwidth

SNR depends on noise power, but what determines how much noise power reaches a receiver?

One important factor is **bandwidth**.

If approximately white noise has an almost constant power spectral density over the region of interest, then accepting a wider frequency range collects more total noise power.

The basic relationship is

$$
P_n\propto B
$$

where \(B\) is the effective noise bandwidth.

If the accepted noise bandwidth doubles, we expect the total noise power to approximately double:

$$
B\rightarrow2B\quad\Rightarrow\quad P_n\rightarrow2P_n
$$

In decibels,

$$
10\log_{10}(2)\approx3.01\text{ dB}
$$

so doubling the accepted noise bandwidth produces approximately 3 dB more total noise power for white noise.

## 7.9 Experiment 4: Filter Bandwidth and Noise Power

We now test the bandwidth relationship directly.

A Gaussian Noise Source feeds two measurement branches. One measures the original noise power. The other passes the noise through a Low Pass Filter before measuring the remaining power.

![GNU Radio flowgraph for measuring noise power as a function of bandwidth.](../figures/ch07/ch07-exp4-noise-power-bandwidth-flowgraph.png)

The important settings are:

| Parameter | Setting |
|---|---:|
| `samp_rate` | `32e3` |
| `avg_len` | `10000` |
| Initial `cutoff` | `1000` Hz |
| Noise Source Amplitude | `1` |
| Low Pass Filter Decimation | `1` |
| Low Pass Filter Gain | `1` |
| Low Pass Filter Transition Width | `500` Hz |
| Low Pass Filter Window | Hamming |
| QT GUI Range Start | `500` Hz |
| QT GUI Range Stop | `4000` Hz |
| QT GUI Range Step | `500` Hz |

The Frequency Sink is connected after the Low Pass Filter, so it shows the filtered-noise spectrum.

We test cutoff frequencies of 500 Hz, 1 kHz, 2 kHz, and 4 kHz.

Because this real low-pass filter is centred on DC, a cutoff \(f_c\) corresponds roughly to a two-sided pass region from \(-f_c\) to \(+f_c\), before accounting for the transition band. We therefore avoid treating the entered cutoff value as if it were an exact rectangular noise bandwidth.

What matters for this experiment is that increasing the cutoff widens the accepted frequency region.

### Results

The measured values were approximately:

| LPF Cutoff | Input Noise Power | Filtered Noise Power |
|---:|---:|---:|
| 500 Hz | 0.996 | 0.025 |
| 1 kHz | 0.977 | 0.055 |
| 2 kHz | 0.999 | 0.122 |
| 4 kHz | 0.992 | 0.242 |

![Effect of low-pass filter bandwidth on measured Gaussian-noise power.](../figures/ch07/ch07-exp4-noise-power-vs-bandwidth.png)

The input noise power stays close to 1, showing that the Noise Source itself has not changed.

The filtered noise power rises as the filter becomes wider.

Comparing the 2 kHz and 4 kHz cutoff settings,

$$
\frac{0.242}{0.122}\approx1.98
$$

so doubling the cutoff approximately doubled the measured passed-noise power in that part of the experiment.

This is consistent with the white-noise relationship

$$
P_n\propto B
$$

and with the engineering rule:

> Doubling noise bandwidth increases total white-noise power by approximately 3 dB.

The relationship is not exact because the input is random and the Low Pass Filter is not an ideal brick-wall filter. Its transition region passes some frequencies partially, so the true effective noise bandwidth depends on the complete filter response.

This leads naturally to the idea of **equivalent noise bandwidth**, which we will not calculate yet.

## 7.10 Bandwidth, Filtering, and Receiver SNR

The bandwidth experiment connects directly to practical SDR receivers.

Suppose a desired signal occupies only a small part of the spectrum, but the receiver accepts a much wider band. The additional spectrum also brings additional noise.

If we apply an appropriate filter around the desired signal, much of the out-of-band noise can be rejected. If the desired signal power is preserved while the accepted noise power falls, SNR improves.

That does not mean the filter should be made arbitrarily narrow. A real signal occupies finite bandwidth. If the filter becomes narrower than the signal itself, part of the desired signal is attenuated or distorted.

A better rule is:

> Use enough bandwidth to preserve the desired signal, but avoid accepting substantially more bandwidth than necessary.

This is one of the fundamental reasons filtering matters in receivers.

## 7.11 GNU Radio Toolbox

This chapter introduced several blocks in measurement roles rather than only as signal-generation or display tools.

| GNU Radio block | What we used it for |
|---|---|
| Noise Source | Generated Gaussian noise |
| Add | Combined the cosine and noise |
| Multiply | Squared real samples for power measurement |
| Moving Average | Averaged squared samples to estimate power |
| Divide | Calculated \(P_s/P_n\) |
| Log10 | Calculated the base-10 logarithm |
| Multiply Const | Multiplied the logarithmic result by 10 |
| QT GUI Number Sink | Displayed signal power, noise power, and SNR |
| QT GUI Range | Changed noise amplitude or filter cutoff while running |
| Low Pass Filter | Restricted the accepted noise bandwidth |

A useful pattern from this chapter is

$$
x[n]\rightarrow x^2[n]\rightarrow\text{average}\rightarrow P
$$

for real-signal power, followed by

$$
P_s,P_n\rightarrow\frac{P_s}{P_n}\rightarrow10\log_{10}(\cdot)\rightarrow\mathrm{SNR}_{\mathrm{dB}}
$$

This is an important shift in how we use GNU Radio. We are no longer only generating and viewing signals. We are beginning to build measurements directly from basic processing blocks.

## 7.12 Explore Further

The same flowgraphs give us several useful experiments to try.

1. Increase the Moving Average length in the SNR experiment. Observe how the power and SNR readings become steadier, then change the noise amplitude quickly and compare the response time.

2. Set the noise amplitude to `1` and compare the signal in the Time Sink with the Frequency Sink. The measured SNR should be near -3 dB. Does the spectral tone remain identifiable?

3. Double the noise amplitude from `0.5` to `1.0`, then from `1.0` to `2.0`. Check whether each doubling reduces the measured SNR by approximately 6 dB.

4. In the bandwidth experiment, compare the filtered noise power at 1 kHz, 2 kHz, and 4 kHz cutoff settings. Does each approximate doubling produce close to 3 dB more noise power?

5. Reduce the Low Pass Filter cutoff until it begins to affect a useful signal placed inside the same branch. This shows why receiver bandwidth cannot be reduced indefinitely.

Before changing a parameter, predict the effect first. Then run the flowgraph and compare the observation with the prediction.

## 7.13 What We Learned

We began with noise by itself. Gaussian noise looked irregular in the time domain, while its approximately white spectrum occupied a broad frequency range.

A single finite FFT of random noise did not look perfectly flat because each block contains a different random realization. FFT averaging reduced some of the frame-to-frame variation without changing the underlying noisy samples.

We then added a 1 kHz cosine to the noise. As the noise amplitude increased, the sinusoid became progressively harder to recognize in the time domain, while its persistent spectral components could remain visible near \(\pm1\) kHz.

This led to the idea of the noise floor and then to a more quantitative description:

$$
\mathrm{SNR}=\frac{P_s}{P_n}
$$

and

$$
\mathrm{SNR}_{\mathrm{dB}}=10\log_{10}\left(\frac{P_s}{P_n}\right)
$$

For our real amplitude-1 cosine,

$$
P_s\approx0.5
$$

and for the real Gaussian Noise Source,

$$
P_n=A_n^2
$$

in expectation.

We built those measurements directly from GNU Radio blocks and confirmed the predicted SNR values experimentally.

Two decibel relationships are especially useful:

$$
\text{Noise amplitude}\times2\Rightarrow\text{noise power}\times4\Rightarrow\text{SNR decreases by about }6\text{ dB}
$$

and

$$
\text{Noise bandwidth}\times2\Rightarrow\text{noise power}\times2\Rightarrow\text{noise power increases by about }3\text{ dB}
$$

These are different effects. One comes from the square relationship between amplitude and power. The other comes from collecting approximately white noise over a wider frequency range.

Most importantly, we now have a clearer picture of how noise, bandwidth, filtering, and SNR are connected inside a receiver.

## 7.14 Connecting to the Next Chapter

Throughout this chapter, the useful signal was already located at the frequency where we wanted to observe it.

A radio receiver often has another task first: move a signal from one part of the spectrum to another while preserving the information it carries.

We introduced the basic idea of mixing earlier when building I/Q signals. In the next chapter, we will study frequency translation more directly and systematically.

We will see why real mixing produces both sum and difference frequencies, how downconversion moves a signal toward baseband, and why complex mixing is particularly useful in SDR.
