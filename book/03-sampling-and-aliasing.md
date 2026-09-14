# Chapter 3: Sampling and Aliasing

In Chapter 2, we generated signals inside GNU Radio and changed their amplitude, frequency, phase, offset and waveform shape. We also added signals together and observed how phase and frequency affect the result.

So far, however, those signals have already existed as numbers inside the computer.

A real radio signal is different. It arrives at the receiver as a continuously varying electrical signal, while a computer can process only numerical data. Somehow, the analog waveform has to be converted into a sequence of numbers.

That conversion begins with **sampling**.

Sampling is fundamental to digital signal processing and SDR because it determines which parts of an analog signal can be represented digitally. It also introduces an important limitation: if we sample too slowly, one analog frequency can appear as another frequency in the digital data.

Rather than beginning with the sampling theorem, we will first build an intuitive picture of sampling, observe it in GNU Radio, and then use the experiment to understand why the Nyquist limit exists.

## 3.1 From a Continuous Signal to Samples

Imagine measuring the temperature of a room. The actual temperature changes continuously, but a computer might record one measurement every minute:

```text
10:00 → 21.2 °C
10:01 → 21.3 °C
10:02 → 21.4 °C
10:03 → 21.3 °C
```

Each measurement gives us one number. That number is a **sample**.

A radio receiver follows the same basic idea, only much faster. The electrical signal presented to an analog-to-digital converter, or **ADC**, varies continuously with time. The ADC measures that signal at discrete instants and converts those measurements into numbers.

A simplified signal path is:

**Analog signal → ADC → Digital samples → Software processing**

Once the signal is represented by samples, software such as GNU Radio can process it.

> **Sampling is the bridge between the analog and digital domains.**

## 3.2 Sampling Period and Sample Rate

Suppose we have a continuous-time signal $x(t)$.

Instead of knowing its value at every possible instant, we measure it at regularly spaced times:

$$
t=0,\ T_s,\ 2T_s,\ 3T_s,\ldots
$$

The resulting sequence is

$$
x[0],\ x[1],\ x[2],\ x[3],\ldots
$$

with

$$
x[n]=x(nT_s)
$$

where $T_s$ is the **sampling period**, the time between consecutive samples.

The number of samples taken each second is the **sampling frequency**, or **sample rate**, $f_s$.

The two quantities are related by

$$
f_s=\frac{1}{T_s}
$$

or equivalently

$$
T_s=\frac{1}{f_s}
$$

For example, if

$$
f_s=8000\text{ samples/s}
$$

then

$$
T_s=\frac{1}{8000}=125\ \mu\text{s}
$$

so one sample is taken every 125 microseconds.

## 3.3 Seeing Sampling

The figure below shows the idea visually.

![A continuous-time signal measured at regularly spaced sampling instants. The points represent the samples retained by the digital system.](../figures/ch03/sampling-concept.png)

The smooth curve represents the continuously varying signal. The individual points represent the values retained by the sampling system.

The digital system does not receive the complete smooth curve. It receives a sequence of values such as $x[0]$, $x[1]$, $x[2]$ and so on.

Those samples are all that the subsequent digital processing has available.

This immediately raises an important question: **how frequently should we sample the signal?**

We will answer that experimentally.

## 3.4 Building the Sampling Experiment in GNU Radio

We will generate a cosine and gradually reduce the sample rate while observing the signal in both the time and frequency domains.

The completed GNU Radio flowgraph is shown below.

![GNU Radio flowgraph used for the sampling and aliasing experiment.](../figures/ch03/sampling-basics-flowgraph.png)

The Signal Source generates the cosine. Throttle limits the processing rate in this software-only experiment, while the QT GUI Time Sink and QT GUI Frequency Sink let us observe the same sample stream in two different ways.

We will also use two interactive controls:

- a **QT GUI Chooser** to select the sample rate,
- a **QT GUI Range** to vary the signal frequency while the flowgraph is running.

These controls make it possible to explore the sampling boundary without repeatedly editing and restarting the flowgraph.

## 3.5 Interactive Controls: Chooser and Range

The **QT GUI Chooser** lets us select one value from a predefined set. In this experiment its ID is:

```text
sample_rate
```

with the choices:

```text
32 kS/s
8 kS/s
4 kS/s
2.5 kS/s
0.5 kS/s
```

We will use the first four in the main experiment and leave `0.5 kS/s` for further exploration.

The **QT GUI Range** creates another run-time variable:

```text
ID: sig_freq
```

The Signal Source uses:

```text
Frequency: sig_freq
```

so moving the Range control changes the generated signal frequency while the flowgraph is running.

The distinction is useful:

- a normal **Variable** stores a value,
- a **QT GUI Chooser** selects one value from a predefined set,
- a **QT GUI Range** varies a value over a specified range.

We will use these run-time controls frequently in later experiments.

## 3.6 Time-Domain and Frequency-Domain Views

The **QT GUI Time Sink** shows how the sampled signal varies with time.

The **QT GUI Frequency Sink** shows how the signal energy is distributed with frequency. We will study the frequency domain properly later, so for now we only need to watch where the spectral peaks appear.

For this experiment, the Frequency Sink is configured to show the full spectrum. A real cosine therefore appears with symmetric components at positive and negative frequencies. For a 2 kHz cosine, we expect peaks around

$$
+2\text{ kHz}
$$

and

$$
-2\text{ kHz}
$$

The meaning of positive and negative frequency will become much clearer when we study complex signals and I/Q representation.

## 3.7 Our Experiment: A 2 kHz Cosine

For the main experiment, use:

```text
Signal frequency = 2 kHz
Amplitude = 1
Waveform = Cosine
```

Keep the signal frequency fixed and change only the sample rate:

```text
32 kS/s
8 kS/s
4 kS/s
2.5 kS/s
```

This keeps the experiment controlled. If only the sample rate changes, we know that differences in the result come from the sampling condition rather than from a change in the original signal.

Before looking at the four cases, we need one useful quantity.

## 3.8 Samples per Cycle

For a sinusoid with frequency $f$ sampled at $f_s$, the number of samples taken during one cycle is

$$
N_{\text{cycle}}=\frac{f_s}{f}
$$

For our 2 kHz cosine at 32 kS/s,

$$
N_{\text{cycle}}=\frac{32000}{2000}=16
$$

so each cycle is represented by 16 samples.

This gives us an intuitive way to think about sampling. The sample rate tells us how many measurements are taken each second, while $f_s/f$ tells us how many of those measurements fall within one cycle of a particular sinusoid.

## 3.9 Reducing the Sample Rate

The figure below shows the same 2 kHz cosine at four different sample rates.

![A 2 kHz cosine sampled at progressively lower sample rates. At 2.5 kS/s, the 2 kHz input aliases and appears at approximately 0.5 kHz.](../figures/ch03/sampling-rate-comparison.png)

### 32 kS/s: 16 Samples per Cycle

With

$$
f_s=32\text{ kS/s}
$$

we obtain

$$
\frac{32}{2}=16
$$

samples per cycle.

The Time Sink appears smooth because many samples are available across each cycle. The Frequency Sink shows the expected components near $\pm2$ kHz.

### 8 kS/s: 4 Samples per Cycle

Reducing the sample rate to

$$
f_s=8\text{ kS/s}
$$

gives

$$
\frac{8}{2}=4
$$

samples per cycle.

The Time Sink now looks much less smooth, but the Frequency Sink still places the signal at approximately $\pm2$ kHz. The signal frequency has not changed; we are simply representing each cycle with fewer samples.

### 4 kS/s: The Nyquist Boundary

At

$$
f_s=4\text{ kS/s}
$$

we have

$$
\frac{4}{2}=2
$$

samples per cycle, and the signal frequency is exactly

$$
f=\frac{f_s}{2}
$$

This is the **Nyquist frequency**.

The exact boundary needs care. At $f_s/2$, the sample values depend strongly on the phase between the sinusoid and the sampling instants. A particular phase may produce alternating positive and negative samples, while another phase can produce very different values. The boundary is therefore not a comfortable operating point for practical systems.

### 2.5 kS/s: Aliasing

Now reduce the sample rate to

$$
f_s=2.5\text{ kS/s}
$$

The number of samples per cycle becomes

$$
\frac{2.5}{2}=1.25
$$

The most important change is not simply that the Time Sink looks unusual. The Frequency Sink no longer places the sampled signal at $\pm2$ kHz. Instead, it appears around

$$
\pm0.5\text{ kHz}
$$

The 2 kHz analog frequency is now represented in the sampled data by a 0.5 kHz alias.

This is **aliasing**.

The four cases can be summarised as follows:

| Signal Frequency | Sample Rate | Samples per Cycle | Observation |
|---:|---:|---:|---|
| 2 kHz | 32 kS/s | 16 | Correct frequency representation |
| 2 kHz | 8 kS/s | 4 | Correct frequency representation |
| 2 kHz | 4 kS/s | 2 | Nyquist boundary |
| 2 kHz | 2.5 kS/s | 1.25 | Aliased to 0.5 kHz |

The change at 2.5 kS/s points directly to the sampling theorem.

## 3.10 The Nyquist Sampling Theorem

For a band-limited baseband signal whose highest frequency component is $f_{\max}$, the sample rate must be greater than twice that highest frequency if we want to avoid aliasing:

$$
f_s>2f_{\max}
$$

The frequency

$$
f_N=\frac{f_s}{2}
$$

is called the **Nyquist frequency**.

For example, if

$$
f_s=8\text{ kS/s}
$$

then

$$
f_N=4\text{ kHz}
$$

and our 2 kHz cosine lies safely below the Nyquist limit.

If instead

$$
f_s=2.5\text{ kS/s}
$$

then

$$
f_N=1.25\text{ kHz}
$$

and the 2 kHz signal lies above the representable baseband range.

The sampled sequence can no longer identify that analog frequency uniquely, so aliasing occurs.

## 3.11 Why "Two Samples per Cycle" Needs Care

The sampling theorem is often shortened to the statement that we need at least two samples per cycle. That is useful intuition, but it is not a safe design rule by itself.

Our 4 kS/s case illustrates why. A 2 kHz sinusoid sampled at 4 kS/s lies exactly at the Nyquist frequency. The sample positions depend on the phase relationship between the signal and the sampling clock. In an extreme case, the sampling instants can repeatedly land on zero crossings.

Practical systems therefore operate with margin rather than trying to place the highest desired frequency exactly at $f_s/2$.

> **The Nyquist frequency is a theoretical boundary, not a target operating point.**

## 3.12 A Rough Waveform Does Not Automatically Mean Aliasing

At 8 kS/s, the Time Sink already looks less smooth than at 32 kS/s. At 4 kS/s, the plotted waveform can look extremely angular.

That appearance alone does not prove that aliasing has occurred.

GNU Radio is displaying discrete samples and drawing line segments between them. With many samples per cycle, those segments give the visual impression of a smooth curve. With only a few samples, the individual segments become obvious.

The 2.5 kS/s case is different. There, the sampled sequence corresponds to a different frequency inside the Nyquist interval.

> **A rough-looking time-domain trace and aliasing are not the same thing.**

## 3.13 What Aliasing Really Means

Aliasing occurs when different analog frequencies produce indistinguishable sampled sequences.

A frequency above the Nyquist limit can therefore appear inside the representable digital frequency range at another frequency.

In our experiment, the Signal Source was configured for

$$
f=2\text{ kHz}
$$

while the sample rate was

$$
f_s=2.5\text{ kS/s}
$$

The resulting samples correspond to an apparent frequency of

$$
0.5\text{ kHz}
$$

The original analog signal did not physically slow down. The ambiguity was introduced by the sampling process.

A precise way to state the result is:

> **The 2 kHz analog signal appears as a 0.5 kHz signal in the sampled data.**

Once the samples have been produced, the digital system cannot determine from those samples alone which of the aliased analog frequencies was originally present.

## 3.14 Predicting the Alias Frequency

For our first example,

$$
f=2\text{ kHz}
$$

and

$$
f_s=2.5\text{ kS/s}
$$

The Nyquist frequency is

$$
f_N=\frac{2.5}{2}=1.25\text{ kHz}
$$

so the 2 kHz input lies outside the Nyquist interval.

For this first-fold case, the alias is

$$
f_{\text{alias}}=|f-f_s|
$$

which gives

$$
f_{\text{alias}}=|2-2.5|=0.5\text{ kHz}
$$

This is the frequency observed in the GNU Radio Frequency Sink.

Consider another example. Suppose

$$
f=7\text{ kHz}
$$

and

$$
f_s=10\text{ kS/s}
$$

The Nyquist frequency is 5 kHz, so 7 kHz lies above Nyquist. The first-fold alias is

$$
f_{\text{alias}}=|7-10|=3\text{ kHz}
$$

A 7 kHz analog sinusoid can therefore produce the same sampled sinusoidal pattern as a 3 kHz signal under this sampling condition.

## 3.15 Frequency Folding

A useful way to picture aliasing is to imagine the frequency axis folding at the Nyquist boundary.

Suppose

$$
f_s=4\text{ kS/s}
$$

so

$$
f_N=2\text{ kHz}
$$

For real sinusoids, increasing the analog input frequency gives the following pattern over the first fold:

| Analog Input Frequency | Apparent Frequency |
|---:|---:|
| 0.5 kHz | 0.5 kHz |
| 1.0 kHz | 1.0 kHz |
| 1.5 kHz | 1.5 kHz |
| 2.0 kHz | Nyquist boundary |
| 2.5 kHz | 1.5 kHz |
| 3.0 kHz | 1.0 kHz |
| 3.5 kHz | 0.5 kHz |

Below 2 kHz, the apparent frequency rises with the input. Beyond 2 kHz, it folds back downward.

More generally, aliases of a real sinusoid are related by integer multiples of the sample rate. A useful expression is

$$
f_{\text{alias}}=|f-kf_s|
$$

where the integer $k$ is chosen so that the resulting frequency lies within the baseband Nyquist interval from 0 to $f_s/2$.

The equation is useful, but the physical idea matters more: **different analog frequencies can map to the same digital sequence**.

## 3.16 Preventing Aliasing Before the ADC

Once an unwanted analog component has aliased into the digital band, software may not be able to distinguish it from a legitimate signal already present at that apparent frequency.

For that reason, practical sampling systems use analog filtering before the ADC. The purpose of an **anti-aliasing filter** is to reduce frequency components that the chosen sample rate cannot represent safely.

A simplified receiver path is:

**Antenna → RF Front End → Analog Filtering → ADC → Digital Samples → DSP**

The exact filter may be low-pass or band-pass depending on the receiver architecture, but the principle is the same: unwanted analog energy should be suppressed before sampling if it could fold into the digital band of interest.

This is why sample rate and analog front-end filtering are closely connected in SDR design.

## 3.17 Why This Matters in SDR

GNU Radio can perform sophisticated digital processing, but it can only work with the samples it receives.

If the analog front end and ADC have already allowed unwanted signals to alias into the sampled band, later software processing cannot simply reconstruct the original analog frequencies from the ambiguous samples.

The sample rate therefore determines how much frequency information can be represented unambiguously in the digital domain, while the analog front end determines which parts of the RF spectrum are presented to the ADC in the first place.

Both sides matter.

## 3.18 Sample Rate and Signal Frequency Are Different Quantities

These two values appear together constantly in GNU Radio, so it is worth keeping their meanings separate.

Suppose

```text
Signal frequency = 2 kHz
Sample rate = 32 kS/s
```

The **signal frequency** tells us how quickly the waveform oscillates. A 2 kHz sinusoid completes 2000 cycles each second.

The **sample rate** tells us how many numerical samples represent the signal each second. A rate of 32 kS/s means 32,000 samples per second.

Their ratio tells us how many samples represent one cycle:

$$
\frac{32000}{2000}=16
$$

So signal frequency describes the waveform, while sample rate describes how often that waveform is measured or represented digitally.

## 3.19 GNU Radio Toolbox

This chapter introduced several GNU Radio features that we will reuse.

### QT GUI Chooser

The **QT GUI Chooser** creates a run-time variable whose value is selected from a predefined set. In this experiment, it lets us switch among several sample rates.

### QT GUI Range

The **QT GUI Range** creates a run-time variable that can be adjusted across a specified range. We use `sig_freq` to change the Signal Source frequency while the flowgraph is running.

### QT GUI Frequency Sink

The **QT GUI Frequency Sink** displays the spectral content of a stream. In this chapter, it lets us distinguish a merely coarse time-domain trace from a genuine frequency alias.

### Shared Sample-Rate Variable

The same `sample_rate` value is used by the blocks that generate, throttle and interpret the stream. Using one shared value keeps the flowgraph internally consistent and makes the experiment easier to modify.

## 3.20 Explore Further

The same flowgraph lets us test several useful predictions.

1. Keep the signal frequency at `2 kHz` and select `0.5 kS/s`. Before running the case, calculate $N_{\text{cycle}}=f_s/f$. Then compare the Time Sink and Frequency Sink. What frequency does the sampled sequence appear to contain?

2. Set the sample rate to `4 kS/s`, so the Nyquist frequency is `2 kHz`. Move the signal frequency through `500 Hz`, `1 kHz`, `1.5 kHz`, `2 kHz`, `2.5 kHz` and `3 kHz`. Predict the apparent frequency before each change and watch what happens after crossing the Nyquist boundary.

3. Replace the cosine with a square wave and repeat part of the experiment. Then try a triangle wave. These waveforms contain more than one sinusoidal frequency component, so their sampling behaviour is more complicated than that of a single cosine. We will understand why when we study the frequency domain in more detail.

The same habit from the earlier chapters still applies: change one thing, predict the result, run the experiment and compare the observation with the prediction.

## 3.21 What We Learned

Sampling converts a continuously varying analog signal into a sequence of discrete values:

$$
x[n]=x(nT_s)
$$

The sampling period and sample rate are related by

$$
f_s=\frac{1}{T_s}
$$

and for a sinusoid, the number of samples per cycle is

$$
N_{\text{cycle}}=\frac{f_s}{f}
$$

Our 2 kHz experiment gave 16 samples per cycle at 32 kS/s, 4 samples per cycle at 8 kS/s, and reached the Nyquist boundary at 4 kS/s. When the rate fell to 2.5 kS/s, the 2 kHz input appeared in the sampled data at 0.5 kHz.

That experiment demonstrated the central danger of undersampling: a frequency outside the Nyquist interval can become indistinguishable from another frequency inside it.

This is why practical SDR systems combine suitable sample rates with analog filtering before the ADC.

## 3.22 Connecting to the Next Chapter

One feature appeared repeatedly in the Frequency Sink during this chapter. A real 2 kHz cosine produced spectral components around both

$$
+2\text{ kHz}
$$

and

$$
-2\text{ kHz}
$$

What does a negative frequency mean? Why do SDR systems often represent a signal using two components called **I** and **Q**? And why are complex-valued samples so useful in radio processing?

To answer those questions, we need to move beyond real-valued sinusoids and start thinking about complex signals, rotating vectors, and positive and negative frequencies.