# Chapter 18: Pulse Shaping and Matched Filtering

## Main Question

**Why can't we simply transmit abrupt rectangular symbols over the air?**

In Chapter 17, we learned where digital symbols live.

For BPSK, the ideal symbols lie at $-1$ and $+1$ on the I axis. For QPSK, the symbols occupy four points in the I/Q plane. For 16-QAM, the constellation expands into a two-dimensional grid.

That gave us the geometry of digital modulation.

But a constellation diagram does not tell us what happens between one symbol and the next. A radio does not transmit isolated dots on an I/Q plane. It transmits a waveform that changes with time.

The simplest approach is to hold each symbol value constant for one symbol period and then switch immediately to the next value. This produces rectangular symbol pulses.

Rectangular pulses are easy to generate and easy to understand, but their abrupt edges produce substantial spectral sidelobes. If we smooth those edges, the spectrum becomes better contained, but each pulse also spreads farther in time. That creates the possibility of **intersymbol interference**, or ISI.

This chapter develops that problem experimentally. We will begin with rectangular symbols, observe their spectrum, smooth them, and examine how filtering spreads a pulse in time. From there we will introduce the Nyquist zero-ISI idea, raised-cosine and root-raised-cosine shaping, matched filtering, and finally the eye diagram.

The goal is to understand why pulse shaping is needed and what the receiver gains from using a matched filter.

## 18.1 From Constellation Points to Symbol Waveforms

Suppose a BPSK mapper produces the sequence

$$
a[k]\in\{-1,+1\}
$$

These are symbol values. They tell us what the transmitted signal should represent at each symbol time, but they do not yet define the complete waveform.

To create a waveform, each symbol is associated with a pulse shape. A useful general model is

$$
x(t)=\sum_k a[k]p(t-kT_s)
$$

where $p(t)$ is the pulse shape and $T_s$ is the symbol period.

Each symbol creates a shifted copy of the same basic pulse. The symbol value scales that pulse, and all the shifted pulses add together.

If $p(t)$ is rectangular, we obtain rectangular symbol pulses. If $p(t)$ belongs to the raised-cosine family, the waveform is smoother and has very different spectral behaviour.

The pulse shape therefore affects occupied bandwidth, spectral sidelobes, how far one symbol extends into neighbouring intervals, how the receiver should filter the signal, and how reliably the receiver can sample the symbols.

We will begin with the simplest pulse shape.

## 18.2 Experiment 18.1: Rectangular Symbols and Bandwidth

The first question is simple:

> **What is wrong with holding each BPSK symbol constant for one symbol period?**

We already used rectangular symbol waveforms while developing digital modulation. Here we focus on their spectrum.

The experiment maps a symbol stream to $-1$ and $+1$, repeats each symbol for a fixed number of samples, and observes the resulting waveform and spectrum.

A convenient starting point is

| Parameter | Value |
|---|---:|
| Sample rate | `32000` samples/s |
| Samples per symbol | `32` |
| Symbol rate | `1000` symbols/s |
| BPSK levels | `[-1, +1]` |

The relationship between sample rate, symbol rate, and samples per symbol is

$$
sps=\frac{f_s}{R_s}
$$

or equivalently,

$$
R_s=\frac{f_s}{sps}
$$

With $f_s=32000$ samples/s and $sps=32$,

$$
R_s=1000\text{ symbols/s}
$$

The flowgraph maps the symbols, uses Repeat to hold each value for `sps` samples, and sends the resulting waveform to Time and Frequency Sinks.

![Rectangular-symbol bandwidth experiment flowgraph](../figures/ch18/ch18-exp1-rectangular-symbol-bandwidth-flowgraph.png)

The Repeat block creates the rectangular pulse shape. Each mapped symbol remains constant for `sps` output samples before the next symbol appears.

### Why Do Abrupt Edges Create Spectral Sidelobes?

A rectangular symbol can change from $+1$ to $-1$ almost instantaneously at a symbol boundary. That sharp edge is a rapid change in time.

Slowly varying waveforms can be represented mostly by lower-frequency components. Rapid changes require higher-frequency Fourier components as well. An ideal discontinuity is the limiting case: reproducing a perfectly vertical edge requires frequency components extending indefinitely.

For a rectangular pulse of duration $T_s$, the Fourier transform has a sinc-shaped form. Ignoring an unimportant time shift,

$$
P(f)=T_s\,\operatorname{sinc}(fT_s)
$$

where

$$
\operatorname{sinc}(x)=\frac{\sin(\pi x)}{\pi x}
$$

The important feature is not only the main lobe. The sinc function also has sidelobes that extend far from the centre frequency and decay relatively slowly.

This poor spectral containment is a property of the rectangular pulse itself, not an artifact of the GNU Radio FFT display.

### Changing the Symbol Rate

We repeated the observation for three symbol rates:

```text
500 symbols/s
1000 symbols/s
2000 symbols/s
```

![Rectangular-symbol spectrum at 500 symbols/s](../figures/ch18/ch18-exp1-rectangular-spectrum-rs500.png)

![Rectangular-symbol spectrum at 1000 symbols/s](../figures/ch18/ch18-exp1-rectangular-spectrum-rs1000.png)

![Rectangular-symbol spectrum at 2000 symbols/s](../figures/ch18/ch18-exp1-rectangular-spectrum-rs2000.png)

As the symbol rate increases, the waveform can change more rapidly and the spectral structure spreads outward.

The important lesson is that **symbol rate and pulse shape both influence the bandwidth of a digital signal**.

The BPSK constellation is unchanged in all three cases. The two ideal symbol points remain the same, but the waveform used to connect those symbols in time occupies a different spectral width.

## 18.3 Experiment 18.2: Smoothing the Rectangular Waveform

If abrupt edges produce unwanted high-frequency content, the natural next step is to smooth them.

We take the rectangular BPSK waveform from Experiment 18.1 and pass it through an ordinary low-pass FIR filter. The waveform is observed before and after filtering in both time and frequency.

![Pulse-smoothing experiment flowgraph](../figures/ch18/ch18-exp2-pulse-smoothing-flowgraph.png)

The purpose of the low-pass filter is not to build the final communication system. It is to expose the basic time-frequency tradeoff.

The filter suppresses high-frequency components, so the abrupt transitions become rounded.

![Rectangular and smoothed symbol waveforms and spectra](../figures/ch18/ch18-exp2-pulse-smoothing.png)

In the time domain, the transitions are smoother. In the frequency domain, the sidelobes are reduced.

This is the behaviour we expected: reducing abrupt time-domain changes reduces high-frequency content and improves spectral containment.

But the time-domain result contains another clue. The filter does not simply round each transition while leaving every symbol confined to its original interval. The filtered waveform extends around each transition.

To understand that effect more clearly, we need to isolate one pulse.

## 18.4 Experiment 18.3: What Happens to One Pulse?

Instead of using a long sequence of changing symbols, we now examine one isolated rectangular pulse.

The question is:

> **When a filter smooths one rectangular pulse, what happens to that pulse in time?**

![Single rectangular pulse before and after smoothing](../figures/ch18/ch18-exp3-single-pulse-spreading.png)

Before filtering, the pulse is confined to a clear interval.

After filtering, the pulse is smoother, but its influence extends beyond the original rectangular interval.

This is the price of smoothing. A filter that removes high-frequency content cannot preserve an infinitely sharp start and stop. The pulse becomes less compact in time.

Improving spectral containment therefore generally requires giving up some time localization.

### Why Is the Filtered Pulse Shifted?

The filtered pulse also appears later in time.

That shift is not ISI.

A causal linear-phase FIR filter introduces group delay. For an FIR filter with $N$ taps, the group delay is approximately

$$
D=\frac{N-1}{2}
$$

samples.

In seconds,

$$
\tau_g=\frac{N-1}{2f_s}
$$

A filtered waveform may therefore be delayed even when the filtering is working exactly as intended.

Filter delay and ISI describe different effects. Filter delay shifts the waveform in time. ISI changes the contribution of neighbouring symbols to a symbol decision.

Once one pulse spreads beyond its own symbol interval, it can overlap the pulses on either side. The next experiment examines what that means for a symbol inside a sequence.

## 18.5 Experiment 18.4: Building ISI Intuition

Rather than beginning with a formal definition of intersymbol interference, we can ask a more useful question:

> **Can the waveform associated with one symbol depend on the symbols around it?**

To make that visible, we keep the central symbol the same while changing its neighbours. The smoothing filter remains unchanged.

![Same symbol with different neighbouring symbols after filtering](../figures/ch18/ch18-exp4-same-symbol-different-neighbours.png)

The central symbol has the same intended value in each case, but the filtered waveform around it is not identical.

The reason is that filtering spreads the neighbouring pulses in time. Their tails extend into the interval occupied by the symbol we are examining.

The waveform at a particular time is therefore not determined only by the current symbol. It contains contributions from surrounding symbols.

This gives us the useful definition:

> **ISI occurs when the contribution from one symbol affects the observation used to decide another symbol.**

Pulse overlap is part of the picture, but overlap alone is not enough to say that ISI is present.

The next experiment shows why. Pulses can overlap strongly and still contribute zero interference at the correct decision instants.

## 18.6 The Nyquist Idea We Need Here

We have already used the name **Nyquist** earlier in the book.

In Chapter 3, the question was how fast a waveform must be sampled to avoid aliasing. That is the Nyquist sampling criterion.

The Nyquist idea needed here answers a different question: how should symbol pulses behave so that neighbouring symbols do not interfere at the correct decision instants?

| Nyquist idea | Question |
|---|---|
| Sampling criterion | How fast must a waveform be sampled to avoid aliasing? |
| Zero-ISI pulse criterion | How should symbol pulses behave at neighbouring decision instants? |

The two ideas share a name, but they solve different problems.

## 18.7 Experiment 18.5: Overlap Without ISI

Suppose the receiver makes one symbol decision every $T_s$ seconds.

We want the pulse associated with the current symbol to have its full value at its own sampling instant while every shifted neighbouring pulse contributes zero at that same time.

For a normalized pulse $p(t)$, the ideal condition is

$$
p(0)=1
$$

and

$$
p(nT_s)=0,\qquad n=\pm1,\pm2,\pm3,\ldots
$$

This is the central idea behind the Nyquist zero-ISI criterion.

A sinc pulse gives us the clearest visual demonstration.

The sinc extends far beyond one symbol interval, so shifted sinc pulses overlap heavily. Their zero crossings, however, occur at integer multiples of the symbol period.

![Shifted sinc pulses demonstrating the Nyquist zero-ISI condition](../figures/ch18/ch18-exp5-sinc-zero-isi.png)

At the centre of one pulse, that pulse contributes its symbol value. At the same instant, the neighbouring shifted sinc pulses cross zero.

The pulses can therefore overlap strongly between decision instants while contributing no unwanted value at the correct decision time.

This is an important refinement of our earlier ISI intuition:

> **Pulse overlap does not automatically mean intersymbol interference. What matters is the contribution from neighbouring symbols at the decision instant.**

For a symbol sequence $a[k]$, the pulse-shaped waveform can be written as

$$
x(t)=\sum_k a[k]p(t-kT_s)
$$

At a sampling instant $t=mT_s$,

$$
x(mT_s)=\sum_k a[k]p((m-k)T_s)
$$

If the pulse satisfies the zero-ISI condition, every term with $k\neq m$ vanishes, leaving

$$
x(mT_s)=a[m]
$$

The equation now formalizes what the figure shows.

### How the Figure Was Generated

For this idealized illustration, we used a short Python script rather than trying to draw several mathematically shifted sinc functions in GNU Radio.

The complete script is stored with the chapter experiments as

```text
ch18_exp5_sinc_zero_isi.py
```

Its purpose is visualization. The communication-system experiments before and after it remain in GNU Radio.

### Why Not Transmit an Ideal Sinc?

The sinc pulse gives the zero-ISI behaviour we want, but an ideal sinc extends from $-\infty$ to $+\infty$.

A real transmitter cannot implement an infinite-duration pulse or an infinite-length filter.

A practical system therefore needs a pulse family that preserves the zero-ISI idea while allowing some extra bandwidth in exchange for better time-domain behaviour.

That leads to the raised-cosine family.

## 18.8 Raised Cosine and the Roll-Off Factor

A raised-cosine pulse is designed so that its overall response satisfies the Nyquist zero-ISI condition.

Its frequency response does not end with an infinitely sharp rectangular edge. Instead, it contains a smooth transition band controlled by the **roll-off factor**, usually written as $\alpha$.

The roll-off factor lies in the range

$$
0\leq\alpha\leq1
$$

For symbol rate $R_s$, the one-sided baseband bandwidth of the raised-cosine response is

$$
B=\frac{R_s}{2}(1+\alpha)
$$

When $\alpha=0$,

$$
B=\frac{R_s}{2}
$$

This is the minimum Nyquist baseband bandwidth for this idealized case.

As $\alpha$ increases, the transition region becomes wider and the required bandwidth increases.

That extra bandwidth can improve time-domain localization. A very sharp frequency-domain transition corresponds to a pulse with long oscillatory tails. Allowing a wider transition produces a pulse whose tails decay more quickly.

The tradeoff is summarized below.

| Roll-off | Bandwidth | Time-domain behaviour |
|---|---|---|
| Small $\alpha$ | Narrower | Longer tails and more ringing |
| Large $\alpha$ | Wider | Better time localization |

Before examining that tradeoff experimentally, we need one practical detail. Communication systems commonly split the desired raised-cosine response between the transmitter and receiver.

## 18.9 Why Root Raised Cosine?

A common implementation uses a **root-raised-cosine**, or RRC, filter at the transmitter and another RRC filter at the receiver.

Their cascade produces the overall raised-cosine response.

In magnitude-response terms,

$$
|H_{\mathrm{RRC}}(f)|^2=H_{\mathrm{RC}}(f)
$$

The word **root** therefore has a direct meaning. Each RRC filter contributes one square-root part of the desired raised-cosine frequency response.

A single RRC filter by itself is not the complete raised-cosine Nyquist response. The transmitter and receiver filters work together.

The next two experiments make that distinction visible.

## 18.10 Experiment 18.6: Exploring the RRC Roll-Off Factor

We now generate isolated RRC pulses with different roll-off factors and compare them in time and frequency.

The main parameters are

| Parameter | Value |
|---|---:|
| Sample rate | `32000` samples/s |
| Symbol rate | `1000` symbols/s |
| Samples per symbol | `32` |
| Filter span | `8` symbols |
| Number of taps | `span*sps + 1 = 257` |
| Roll-off values | `0.10`, `0.25`, `0.50`, `1.00` |

The pulse-shaping filter uses GNU Radio's RRC tap generator:

```python
firdes.root_raised_cosine(
    sps,
    samp_rate,
    symbol_rate,
    alpha,
    ntaps
)
```

The Interpolating FIR Filter uses

```text
Interpolation: sps
```

so the symbol-rate sequence is converted into a waveform containing `sps` samples per symbol while the RRC filter shapes the pulse.

![RRC roll-off comparison flowgraph](../figures/ch18/ch18-exp6-rrc-rolloff-flowgraph.png)

### Time-Domain Result

![RRC pulse shapes for different roll-off factors](../figures/ch18/ch18-exp6-rrc-rolloff-time.png)

With a small roll-off such as $\alpha=0.10$, the pulse has longer and more pronounced tails.

As $\alpha$ increases, the pulse becomes more concentrated around its main lobe and the tails decay more quickly.

The peak amplitudes do not need to be identical in this comparison. We are interested in pulse shape and tail behaviour rather than individually normalizing every curve.

### Frequency-Domain Result

![RRC spectra for different roll-off factors](../figures/ch18/ch18-exp6-rrc-rolloff-spectrum.png)

The frequency-domain result shows the other half of the tradeoff.

A small $\alpha$ gives the narrowest transition region. A larger $\alpha$ allows the response to roll off over a wider frequency interval.

| Roll-off | Time-domain behaviour | Frequency-domain behaviour |
|---|---|---|
| Small $\alpha$ | Longer tails, more ringing | Narrower transition bandwidth |
| Large $\alpha$ | Faster-decaying tails | Wider transition bandwidth |

The roll-off factor is therefore a design parameter that trades occupied bandwidth against time-domain localization.

## 18.11 Experiment 18.7: TX RRC and RX RRC

Experiment 18.6 showed the response of a single RRC filter.

We now apply a second matching RRC filter at the receiver and observe the combined response.

For this experiment,

```text
samp_rate   = 32000
symbol_rate = 1000
sps         = 32
span        = 8
ntaps       = 257
alpha       = 0.35
```

The transmitter RRC is implemented with an Interpolating FIR Filter. The receiver uses a Decimating FIR Filter with decimation set to `1`, so the sample rate is not reduced in this experiment.

![TX and RX RRC filtering flowgraph](../figures/ch18/ch18-exp7-tx-rx-rrc-flowgraph.png)

For the receiver taps, we use the same RRC shape with gain `1`:

```python
firdes.root_raised_cosine(
    1,
    samp_rate,
    symbol_rate,
    alpha,
    ntaps
)
```

The receiver filter uses

```text
Decimation: 1
```

### What Do We Observe?

![RRC pulse before and after the receiver matched filter](../figures/ch18/ch18-exp7-tx-rx-rrc-response.png)

The TX RRC pulse and the output after the second RRC do not have the same shape.

The cascade of the two finite-length RRC filters approximates a raised-cosine response.

Around the main peak, the combined response approaches zero at symbol-spaced intervals:

$$
\pm T_s,\ \pm2T_s,\ \pm3T_s,\ldots
$$

For our symbol rate,

$$
T_s=\frac{1}{1000}=1\text{ ms}
$$

This is the practical version of the zero-ISI behaviour demonstrated earlier with shifted sinc pulses.

The response after both filters is also shifted farther in time. That is expected because the TX branch has passed through one FIR filter, while the RX output has passed through two. Each filter contributes group delay.

The horizontal shift is therefore filter delay, not a failure of the zero-ISI property.

The receive RRC is also performing another important role: it is a matched filter for the transmitted pulse.

## 18.12 Why Is the Receiver RRC a Matched Filter?

We first met matched filtering in Chapter 11 while asking how a receiver can detect a known waveform in noise.

The same idea appears here, but the known waveform is now the transmitted symbol pulse.

In general, if the expected pulse is $p(t)$, the matched-filter impulse response has the form

$$
h_{\mathrm{MF}}(t)=p^*(T-t)
$$

For the real, symmetric RRC pulse used here, the matching receive filter has the same RRC shape apart from alignment and scaling.

The receiver is therefore not applying an arbitrary low-pass filter. It filters the received waveform with a response matched to the transmitted pulse shape.

In additive white Gaussian noise, the matched filter maximizes the signal-to-noise ratio at the chosen decision instant.

The phrase **at the decision instant** is important. A matched filter does not remove all noise from the waveform. Noise remains at its output.

Instead, the filter shapes the signal and noise so that the known pulse is represented as favourably as possible when the receiver makes the symbol decision.

## 18.13 Experiment 18.8: Matched Filtering in Noise

We return from the isolated pulse to a stream of BPSK symbols.

The transmitter applies RRC pulse shaping. Gaussian noise is added between transmitter and receiver, and we observe the waveform before and after the RX RRC matched filter.

![Matched-filtering-in-noise flowgraph](../figures/ch18/ch18-exp8-matched-filter-noise-flowgraph.png)

The RRC parameters remain the same as in Experiment 18.7.

A QT GUI Range controls the Gaussian-noise amplitude:

```text
ID: noise_amp
Default: 0
Start: 0
Stop: 2
Step: 0.05
```

During development, we examined several values, including `0.2`, `0.5`, and `1.0`.

A noise amplitude of `0.5` gives a useful comparison. The input to the matched filter is visibly noisy, while the pulse structure at the output remains easier to recognize.

![BPSK before and after matched filtering with Gaussian noise](../figures/ch18/ch18-exp8-matched-filter-noise.png)

The matched filter has not removed the noise. It has filtered both the desired signal and the noise.

The correct conclusion is that, because the receive filter is matched to the transmitted pulse, it improves the conditions for symbol detection and maximizes the output SNR at the appropriate decision instant in AWGN.

Looking only at the continuous waveform still leaves one important question: where should the receiver sample?

The eye diagram gives us a useful way to examine that question.

## 18.14 Experiment 18.9: Opening the Eye

An **eye diagram** is a visualization of an oversampled received waveform around possible symbol sampling instants.

It is not a new signal. The same waveform is divided into short sections, usually spanning one or two symbol periods, and many sections are overlaid on the same time axis.

For BPSK, different symbol transitions such as $+1$ to $+1$, $+1$ to $-1$, $-1$ to $+1$, and $-1$ to $-1$ appear together. The open region between the trajectories forms the eye.

The eye diagram should not be confused with a constellation diagram. The eye shows how the **oversampled waveform behaves around the sampling time**, so it is especially useful for judging timing margin, pulse shape, and ISI. A constellation shows the **complex samples actually selected at symbol instants**, so it reveals effects such as carrier phase error, carrier frequency error, noise, residual ISI, and symbol-decision quality.

An open eye therefore does not automatically imply a clean constellation. A receiver can have a reasonably open eye while its constellation rotates because of carrier phase or frequency error.

### Generating the Data in GNU Radio

The signal processing remains in GNU Radio. The chain is:

**Random Source → Chunks to Symbols → TX RRC → Gaussian Noise → RX RRC Matched Filter → File Sink**

![GNU Radio flowgraph used to capture eye-diagram data](../figures/ch18/ch18-exp9-eye-diagram-flowgraph.png)

The File Sink records the matched-filter output as Float32 samples.

Two captures are used:

```text
ch18-eye-clean.dat    noise_amp = 0
ch18-eye-05.dat       noise_amp = 0.5
```

Python is used only to construct the eye-diagram visualization from those recorded samples.

With

$$
R_s=1000\text{ symbols/s}
$$

the symbol period is

$$
T_s=1\text{ ms}
$$

Since

$$
sps=32
$$

two symbol periods contain

$$
2sps=64\text{ samples}
$$

The script reads the GNU Radio Float32 samples, discards the initial filter transient, takes successive 64-sample windows beginning one symbol apart, and overlays them.

The complete script is stored as

```text
ch18_exp9_eye_diagram.py
```

A compact version of the plotting method is:

```python
import numpy as np
import matplotlib.pyplot as plt

samp_rate = 32000
sps = 32
eye_len = 2 * sps
skip = 20 * sps
n_traces = 120

def plot_eye(input_file, output_file, title):
    samples = np.fromfile(input_file, dtype=np.float32)
    x = samples[skip:]

    windows = []

    for k in range(n_traces):
        start = k * sps
        end = start + eye_len

        if end <= len(x):
            windows.append(x[start:end])

    windows = np.asarray(windows)
    t_ms = np.arange(eye_len) / samp_rate * 1000

    plt.figure(figsize=(10, 6))

    for window in windows:
        plt.plot(t_ms, window, linewidth=0.8, alpha=0.22)

    plt.axvline(1.0, linestyle="--", linewidth=1.2)
    plt.title(title)
    plt.xlabel("Time (ms)")
    plt.ylabel("Amplitude")
    plt.xlim(0, 2)
    plt.ylim(-2, 2)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_file, dpi=220, bbox_inches="tight")
    plt.close()

plot_eye(
    "ch18-eye-clean.dat",
    "../../figures/ch18/ch18-exp9-eye-no-noise.png",
    "BPSK Eye Diagram After RRC Matched Filtering"
)

plot_eye(
    "ch18-eye-05.dat",
    "../../figures/ch18/ch18-exp9-eye-noise-05.png",
    "BPSK Eye Diagram with Noise After RRC Matched Filtering"
)
```

The exact relative output path can be adjusted to match the experiment folder. The signal-processing method does not change.

### The Clean Eye

![Clean BPSK eye after RRC matched filtering](../figures/ch18/ch18-exp9-eye-no-noise.png)

The dashed line at $1$ ms marks the symbol sampling instant used in the two-symbol display.

At this time, the trajectories cluster around the two BPSK levels:

$$
+1
$$

and

$$
-1
$$

The receiver does not need the waveform trajectories to remain separated everywhere. It needs the symbol possibilities to be well separated when the decision is made.

For BPSK, the decision boundary is around zero. A large vertical opening near the sampling instant gives good separation between the two possible symbol values.

The horizontal opening carries different information. Sampling near the centre of the open region gives more timing margin. Sampling too early or too late moves the observation toward the transition region, where the separation is smaller and the decision becomes more sensitive to timing error, noise, and residual ISI.

### Adding Noise

Now we use the second GNU Radio capture with

```text
noise_amp = 0.5
```

and apply the same eye-diagram visualization.

![BPSK eye with noise amplitude 0.5 after RRC matched filtering](../figures/ch18/ch18-exp9-eye-noise-05.png)

The trajectories are thicker and more spread out.

At the selected sampling instant, however, the upper and lower symbol groups remain separated.

A useful way to read an eye diagram is:

- **vertical eye opening** indicates the available amplitude and noise margin at a given timing position;
- **horizontal eye opening** indicates timing margin;
- **trajectory thickness** reflects noise and other variations;
- **closure or distortion of the eye** can indicate ISI, timing problems, noise, or other waveform impairments.

The eye diagram summarizes the behaviour of the oversampled waveform around the sampling instant. It does not replace the constellation diagram. The two views answer different receiver questions.

## 18.15 Putting the Pieces Together

We began with an apparently simple question: why not transmit rectangular symbols?

We can now answer it step by step.

### Rectangular Symbols Are Easy but Spectrally Expensive

Holding a symbol constant and changing abruptly at the boundary produces a rectangular pulse.

The sharp transitions require high-frequency Fourier components, producing a sinc-shaped spectrum with sidelobes that extend beyond the main lobe.

### Smoothing Improves the Spectrum but Spreads the Pulse

An ordinary low-pass filter reduces the abruptness of the transitions and suppresses high-frequency components.

The filtered pulse, however, is no longer confined to one symbol interval. Its tails extend into neighbouring intervals.

### Pulse Spreading Creates the Possibility of ISI

Once neighbouring pulses overlap, the observation for one symbol can contain contributions from surrounding symbols.

Our same-symbol/different-neighbours experiment made that dependence visible.

### Overlap Itself Is Not the Problem

The sinc experiment showed that pulses can overlap strongly while contributing zero at the correct symbol decision instants.

That is the key idea behind Nyquist zero-ISI pulse shaping.

### Raised Cosine Provides a Practical Tradeoff

An ideal sinc is infinitely long.

The raised-cosine family allows us to trade excess bandwidth against time-domain localization through the roll-off factor $\alpha$.

### RRC Splits the Filtering Between Transmitter and Receiver

Practical systems commonly use an RRC filter at the transmitter and a matching RRC filter at the receiver.

Together, they approximate the desired raised-cosine response.

### The Receiver Filter Also Acts as a Matched Filter

The receive RRC is matched to the transmitted pulse shape.

In AWGN, this maximizes SNR at the appropriate decision instant. It does not remove all noise, but it improves the conditions under which the receiver makes its decision.

### The Eye Diagram Shows the Sampling Margin

The eye diagram overlays many short sections of the matched-filtered waveform.

Its vertical opening shows separation between possible symbol values, while its horizontal opening shows how much timing error can be tolerated before the sampling position approaches a transition.

This completes the connection from constellation points to a practical pulse-shaped waveform.

## 18.16 A Few Things That Can Go Wrong

The experiments were deliberately focused, but they allow us to predict several important failure modes.

### Sampling at the Wrong Time

The clean eye is most open near the preferred decision instant.

Moving the sampling time toward a transition reduces the separation between symbol possibilities.

A practical receiver therefore needs **symbol timing synchronization**. Knowing that there are `32` samples per symbol is not enough. The receiver must determine which sample position corresponds to the best decision time.

### Using Mismatched Pulse-Shaping Parameters

The transmitter and receiver filters are designed as a pair.

If their pulse shapes, roll-off factors, or other relevant parameters do not correspond properly, the combined response is no longer the intended raised-cosine response and the zero-ISI behaviour can degrade.

### Removing the Matched Filter

Without the receive matched filter, the receiver loses both the intended combined pulse response and the matched-filter SNR advantage at the decision instant.

Experiment 18.8 showed why this matters in noise.

### Choosing Roll-Off Without Considering Bandwidth

A small roll-off reduces excess bandwidth but produces longer time-domain tails and places greater demands on a finite-length filter implementation.

A larger roll-off improves time localization but occupies more spectrum.

There is no universally correct value of $\alpha$. It is a system-design choice.

## 18.17 GNU Radio Toolbox

Several GNU Radio blocks play important pulse-shaping and receiver roles in this chapter.

| GNU Radio Block | Role in This Chapter |
|---|---|
| Chunks to Symbols | Maps symbol indices to BPSK amplitudes |
| Repeat | Creates a simple rectangular symbol waveform for the first experiments |
| Interpolating FIR Filter | Increases the sample rate while applying the TX RRC pulse-shaping filter |
| Decimating FIR Filter | Applies the RX RRC filter; used here with decimation set to `1` |
| Noise Source | Adds Gaussian noise between transmitter and receiver |
| QT GUI Time Sink | Displays pulse and waveform behaviour in time |
| QT GUI Frequency Sink | Displays spectral behaviour |
| File Sink | Records matched-filter output for eye-diagram visualization |

### Interpolating FIR Filter

The **Interpolating FIR Filter** performs filtering while increasing the sample rate by an integer factor.

In the RRC experiments, the interpolation factor is

```text
Interpolation: sps
```

The symbol-rate input is converted into a waveform with `sps` samples per symbol while the RRC taps shape the pulse.

Conceptually, interpolation can be understood as inserting samples between symbols and then filtering, although GNU Radio can implement the operation more efficiently than performing those steps separately.

The important point is that the output stream now runs at `samp_rate`, not at the original symbol rate.

### Decimating FIR Filter

In Experiment 18.7, the receiver uses a **Decimating FIR Filter** with

```text
Decimation: 1
```

With decimation equal to one, the block acts as an ordinary FIR filter and does not reduce the sample rate.

We use it because it accepts the receiver RRC taps directly. Later receiver designs may combine filtering with actual decimation.

### File Sink

The **File Sink** records a GNU Radio stream directly to a file.

For the eye-diagram experiment:

```text
Input Type: Float
Vector Length: 1
Unbuffered: Off
Append File: Overwrite
```

The output is a raw binary Float32 file.

The File Sink does not change the signal. It records the stream so that the same samples can be inspected later with another tool.

This division of work is common in SDR: GNU Radio performs the signal processing, while Python or another analysis environment can be used for specialized visualization.

## 18.18 Explore Further

The experiments in this chapter are well suited to prediction before execution.

1. In Experiment 18.1, halve the symbol rate while keeping the sample rate unchanged. Predict how the spectral structure should change.

2. In Experiment 18.2, change the low-pass filter cutoff and observe the tradeoff between transition smoothness and time-domain spreading.

3. In Experiment 18.6, choose one roll-off factor and increase the RRC filter span. Compare the finite-length approximation of the pulse tails.

4. Compare two values of $\alpha$ with the same symbol rate. Predict which one should occupy more bandwidth before looking at the Frequency Sink.

5. In Experiment 18.8, gradually increase `noise_amp` and compare the waveform before and after the matched filter.

6. Generate eye diagrams for several noise levels and compare the vertical eye opening.

7. Shift the eye-diagram window by a few samples and observe how moving away from the preferred sampling position changes the apparent eye opening.

8. Keep the eye diagram in mind while viewing a constellation in a later receiver experiment. Check whether a clean timing eye necessarily corresponds to a stationary constellation.

## 18.19 What We Learned

In this chapter, we moved from constellation geometry to the time waveform used to carry digital symbols.

A constellation specifies the allowed symbol values. The pulse shape determines how those values evolve with time.

Rectangular symbols are simple, but their abrupt transitions create a sinc-shaped spectrum with slowly decaying sidelobes.

Smoothing the waveform improves spectral containment, but filtering spreads a pulse in time. Filter group delay must not be confused with ISI.

ISI occurs when neighbouring symbols affect the observation used to decide the current symbol. Pulse overlap by itself does not imply ISI. The Nyquist zero-ISI criterion allows shifted pulses to overlap between decision instants while contributing zero interference at the correct sampling times.

An ideal sinc pulse demonstrates this property clearly but is infinitely long. Raised-cosine pulse shaping provides a practical tradeoff between bandwidth and time-domain localization. The roll-off factor $\alpha$ controls that tradeoff.

In practical systems, the raised-cosine response is commonly split between a TX RRC filter and a matching RX RRC filter. Their cascade gives the desired overall response, while the receive RRC also serves as a matched filter.

In AWGN, matched filtering maximizes SNR at the appropriate decision instant. It does not simply remove noise.

Finally, the eye diagram gives us a way to inspect the oversampled waveform around possible sampling instants. Its vertical opening indicates symbol separation and noise margin, while its horizontal opening indicates timing margin.

The eye and the constellation describe different aspects of receiver behaviour. An open eye does not guarantee that the constellation will be clean or stationary if carrier synchronization is poor.

The central idea of the chapter is that a good digital waveform does not require neighbouring pulses to remain separate everywhere. It requires them to combine correctly when the receiver makes its decisions.

## 18.20 Connecting to the Next Chapter

So far, the path between transmitter and receiver has been deliberately controlled.

We added Gaussian noise when needed and otherwise assumed that the pulse-shaped waveform arrived without the more complicated effects of radio propagation.

Over the air, that assumption does not hold.

A signal becomes weaker with distance. Reflections can create several delayed copies of the same waveform. Those copies can combine constructively or destructively. Motion can introduce Doppler effects, and transmitter and receiver oscillators can introduce frequency offsets.

The receiver therefore rarely observes exactly what the transmitter produced.

Chapter 19 begins with a clean digital signal and progressively introduces attenuation, noise, frequency offset, delay, multipath, and fading.

This takes us from pulse shaping and matched filtering into the behaviour of the wireless channel itself.