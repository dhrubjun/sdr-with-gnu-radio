# Chapter 2: Understanding Signals

In Chapter 1, we generated our first signal in GNU Radio: a simple cosine wave. Even that basic waveform had several properties we had not yet explored properly, including amplitude, frequency, period, phase, offset and waveform shape.

These ideas appear throughout signal processing and communication systems. Before going deeper into SDR, we need to develop an intuitive feel for what each one means and what changes when we adjust it.

Rather than starting with definitions alone, we will change one property at a time and observe the result in GNU Radio. Later in the chapter, we will combine signals and see how amplitude, frequency and phase interact.

## 2.1 A Signal Is Something That Changes

A microphone produces an electrical signal that changes as sound reaches it. A temperature sensor may produce a slowly varying voltage. A radio antenna responds to electromagnetic fields that can change extremely quickly.

In signal processing, a **signal** represents a quantity that varies with time or with some other independent variable. In this book, time will usually be the variable of interest.

For much of this chapter, we will use a cosine because it is simple, predictable and fundamental to communication systems.

A cosine signal can be written as
$$
x(t)=A\cos(2\pi ft+\phi)+C
$$
Each quantity controls something we can observe directly:

- $A$ controls the amplitude,
- $f$ controls the frequency,
- $\phi$ controls the phase,
- $C$ controls the DC offset.

Instead of trying to understand all of them at once, we will change them one at a time.

## 2.2 Amplitude: How Large Is the Signal?

A useful intuition for amplitude comes from audio. If the electrical signal driving a speaker becomes larger while everything else remains unchanged, the sound will generally become louder. The signal is larger, but it does not play faster simply because its amplitude increased.

For a cosine centred around zero,
$$
x(t)=A\cos(2\pi ft)
$$
the value $A$ is the amplitude. It tells us how far the waveform moves away from its centre value.

If
$$
A=1
$$
the signal reaches approximately +1 and -1. If
$$
A=2
$$
it reaches approximately +2 and -2.

The waveform becomes taller, but its repetition rate does not change.

### GNU Radio Experiment: Comparing Amplitudes

We will generate three cosine waves with identical frequency, phase and offset, but different amplitudes.

| Signal | Frequency | Amplitude | Phase | Offset |
|---|---:|---:|---:|---:|
| Signal 1 | 1 kHz | 0.5 | 0 | 0 |
| Signal 2 | 1 kHz | 1 | 0 | 0 |
| Signal 3 | 1 kHz | 2 | 0 | 0 |

The sample rate remains
$$
f_s=32\,000\text{ samples/s}
$$
The important experimental rule is simple:

> Change one property at a time.

Because frequency, phase and offset remain fixed, any difference between the three waveforms comes from amplitude.

![GNU Radio flowgraph for comparing three signal amplitudes.](../figures/ch02/amplitude-comparison-flowgraph.png)

The three signals are connected to the same QT GUI Time Sink by setting **Number of Inputs** to `3`.

![Three 1 kHz cosine signals with different amplitudes.](../figures/ch02/amplitude-comparison.png)

The peaks and zero crossings occur at the same times, so the three signals are oscillating at the same rate. Only their vertical size changes.

That vertical size is the amplitude.

### A Small GNU Radio Detail

GNU Radio may display an amplitude of `0.5` as

```text
500m
```

Here, `m` means **milli**, so
$$
500m=500\times10^{-3}=0.5
$$
GNU Radio frequently uses engineering prefixes such as `m`, `k` and `M`. We will see them often as the flowgraphs become more complicated.

## 2.3 Frequency: How Fast Does the Signal Repeat?

Imagine two blinking lights. One flashes once every second, while the other flashes ten times every second. Both repeat, but one repeats much faster.

**Frequency** tells us how many complete cycles occur per second. Its unit is hertz (Hz).

A frequency of
$$
f=1\text{ Hz}
$$
means one cycle per second, while
$$
f=1000\text{ Hz}
$$
means 1000 cycles per second. We can also write
$$
1000\text{ Hz}=1\text{ kHz}
$$
A higher frequency therefore means more cycles in the same amount of time.

## 2.4 Period: How Long Does One Cycle Take?

Frequency tells us how many cycles occur in one second. **Period** asks the complementary question: how long does one cycle take?

The period is represented by $T$, and frequency and period are related by
$$
T=\frac{1}{f}
$$
or equivalently
$$
f=\frac{1}{T}
$$
For a 1 kHz signal,
$$
T=\frac{1}{1000}=0.001\text{ s}=1\text{ ms}
$$
Each cycle therefore lasts 1 ms.

### GNU Radio Experiment: Frequency and Period

We can reuse the same three-signal flowgraph from the amplitude experiment. This time, all amplitudes remain at `1`, while only the frequencies change.

| Signal | Frequency | Amplitude |
|---|---:|---:|
| Signal 1 | 500 Hz | 1 |
| Signal 2 | 1000 Hz | 1 |
| Signal 3 | 2000 Hz | 1 |

Keep the phase and offset at zero.

![Comparison of 500 Hz, 1 kHz, and 2 kHz cosine signals.](../figures/ch02/frequency-period-comparison.png)

Over a 4 ms interval:

- the 500 Hz signal completes 2 cycles,
- the 1 kHz signal completes 4 cycles,
- the 2 kHz signal completes 8 cycles.

The corresponding periods are:

| Frequency | Period |
|---:|---:|
| 500 Hz | 2 ms |
| 1000 Hz | 1 ms |
| 2000 Hz | 0.5 ms |

When frequency doubles, the period is halved. That inverse relationship is exactly what $T=1/f$ describes.

### GNU Radio Toolbox: Number of Points

This experiment also gives us a useful reason to look more closely at the QT GUI Time Sink.

In Chapter 1, we used:

```text
Number of Points = 1024
Sample Rate = 32000
```

At a sample rate of 32,000 samples/s, 1024 displayed samples correspond to
$$
\frac{1024}{32000}=0.032\text{ s}=32\text{ ms}
$$
For the frequency comparison, 32 ms shows many cycles. If we want to examine only a few cycles, a shorter window is more useful.

With

```text
Number of Points = 128
```

the displayed duration becomes
$$
\frac{128}{32000}=0.004\text{ s}=4\text{ ms}
$$
For a streaming Time Sink, the approximate time span represented by $N$ displayed samples is
$$
T_{\text{display}}=\frac{N}{f_s}
$$
This connection between sample rate, number of displayed samples and visible time will be useful throughout the book.

## 2.5 Phase: Where Is the Signal in Its Cycle?

Two signals can have the same amplitude and frequency and still fail to line up. One may reach its peak earlier than the other even though both complete each cycle in the same amount of time.

That relative position within a cycle is described by **phase**.

A useful picture is to imagine two people moving around the same circular track at the same speed. If they start side by side, they remain together. If one starts a quarter of a lap ahead, their speed is unchanged, but their positions around the track differ.

A complete cycle corresponds to
$$
360^\circ=2\pi\text{ radians}
$$
Some common phase values are:

| Degrees | Radians |
|---:|---:|
| 0° | $0$ |
| 90° | $\pi/2$ |
| 180° | $\pi$ |
| 270° | $3\pi/2$ |
| 360° | $2\pi$ |

GNU Radio's Signal Source specifies **Initial Phase** in radians.

Phase is most useful when a reference exists. Saying that one signal is 90° ahead of another tells us how the two cycles are positioned relative to each other.

### GNU Radio Experiment: Comparing Phase

Keep the following parameters fixed:

```text
Frequency = 1 kHz
Amplitude = 1
Offset = 0
```

Use three initial phases:

```text
Signal 1: 0
Signal 2: pi/2
Signal 3: pi
```

To make `pi` available in the flowgraph, add a Variable block:

```text
ID: pi
Value: 3.14159
```

GNU Radio can then evaluate expressions such as `pi/2` directly in block properties. This is often clearer than entering a decimal approximation everywhere.

![Three equal-frequency signals with different initial phases.](../figures/ch02/phase-comparison.png)

At $t=0$, the 0° cosine starts at +1, the 90° cosine starts at 0, and the 180° cosine starts at -1.

Their amplitudes and frequencies are identical. What changes is their position within the cycle.

## 2.6 DC Offset: Moving the Whole Signal Up or Down

Until now, our cosine waves have been centred around zero. A cosine with amplitude 1 therefore moves between -1 and +1.

If we add 1 to every value,
$$
x(t)=\cos(2\pi ft)+1
$$
the waveform now moves between 0 and 2.

Its shape and frequency have not changed, and its amplitude about its centre is still 1. The entire waveform has simply moved upward.

That shift in the centre value is called a **DC offset**.

### GNU Radio Experiment: Comparing Offset

Reuse the same three-signal structure and keep:

```text
Frequency = 1 kHz
Amplitude = 1
Phase = 0
```

Change only the offsets:

```text
Signal 1: Offset = 0
Signal 2: Offset = +1
Signal 3: Offset = -1
```

![Cosine signals with different DC offsets.](../figures/ch02/dc-offset-comparison.png)

The first waveform is centred at 0, the second at +1 and the third at -1.

The +1-offset signal reaches a maximum value of +2, but its amplitude is **not 2**. It moves one unit above and below its centre value of +1, so its amplitude remains 1.

This distinction between amplitude and absolute signal level will matter later when we work with more complicated signals.

## 2.7 Waveform Shape

Frequency tells us how often a periodic signal repeats, but it does not tell us what happens during one cycle.

A cosine, square wave and triangle wave can all repeat 1000 times per second while having very different shapes.

### GNU Radio Experiment: Comparing Waveforms

Generate three 1 kHz periodic signals:

- cosine,
- square,
- triangle.

![Comparison of cosine, square, and triangle waveforms.](../figures/ch02/waveform-shape-comparison.png)

The cosine changes smoothly. The square wave switches abruptly between two levels. The triangle wave changes linearly between its minimum and maximum.

We do not need a separate sine example here. Sine and cosine have the same basic waveform shape and differ by a phase shift, which we have already explored.

### A Note About the Square-Wave Settings

For this comparison, we want the real-valued square wave to switch between approximately -1 and +1.

With GNU Radio's Signal Source, a real square wave uses `Offset` for one level and `Amplitude + Offset` for the other. Therefore we use:

```text
Amplitude = 2
Offset = -1
```

which gives levels of approximately -1 and +1.

This is a GNU Radio block-parameter detail worth noticing. For a cosine, the Amplitude field directly corresponds to the centre-to-peak amplitude. For this square-wave implementation, the same field controls the separation between the two output levels together with Offset.

All three waveforms repeat at 1 kHz, yet their shapes are different. The reason becomes much clearer when we later examine signals in the **frequency domain**. For now, the important observation is that repetition frequency alone does not completely describe a waveform.

## 2.8 What Happens When Signals Meet?

So far, we have mainly studied signals one at a time. Real radio systems rarely have that luxury.

An antenna may receive signals from several transmitters. Noise is added to useful signals. Reflections create delayed copies. Interference can arrive at the same receiver together with the signal we want.

To understand these situations, we need to see what happens when signals are combined.

## 2.9 Adding Two Signals

Suppose we have two signals, $x_1(t)$ and $x_2(t)$. Their sum is
$$
y(t)=x_1(t)+x_2(t)
$$
At each instant, the two signal values are added. If $x_1=1$ and $x_2=0.5$, then $y=1.5$. If $x_1=-1$ while $x_2=0.5$, then $y=-0.5$.

GNU Radio lets us observe this directly.

### GNU Radio Experiment: The Add Block

Generate two cosine signals:

```text
Signal 1
Frequency = 1 kHz
Amplitude = 1
Signal 2
Frequency = 2 kHz
Amplitude = 0.5
```

Then add an **Add** block.

![GNU Radio flowgraph showing two signals being added.](../figures/ch02/signal-addition-flowgraph.png)

The Add block performs sample-by-sample addition:
$$
y[n]=x_1[n]+x_2[n]
$$
Each original signal is also branched to the QT GUI Time Sink so that the two inputs and their sum can be compared directly.

![Two cosine signals and their sum.](../figures/ch02/signal-addition.png)

The sum no longer looks like either original cosine. A more complicated waveform has appeared simply because two simple signals were added together.

This is a basic operation, but it is central to what happens in real receivers. Desired signals, interference, noise and multipath components can all combine at the receiver input.

### GNU Radio Toolbox: Branching a Stream

The flowgraph also introduces a useful GNU Radio behaviour. The output of each Throttle block is connected to two destinations: one path goes directly to the Time Sink, while the other goes to the Add block.

No special splitter block is required. A stream can feed multiple downstream blocks directly.

Branching does **not** divide the numerical amplitude of the stream. Each downstream block receives the same sample values.

## 2.10 Phase Changes the Result of Addition

We can now connect two ideas from earlier in the chapter: **phase** and **addition**.

Consider two cosine signals with the same frequency and the same amplitude. If their relative phase changes, their sum changes too.

Use two 1 kHz cosine signals, each with amplitude 1. Keep the first signal at

```text
Phase = 0
```

and run the experiment three times while changing only the initial phase of the second signal.

### Case 1: Phase Difference = 0°

The two signals are aligned. When one reaches +1, the other also reaches +1, and when one reaches -1, the other reaches -1.

Their sum therefore reaches approximately +2 and -2.

![Addition of two equal signals with 0 degree phase difference.](../figures/ch02/phase-addition-0deg.png)

The two signals reinforce each other completely. This is **constructive interference**.

### Case 2: Phase Difference = 90°

Now shift the second signal by
$$
90^\circ=\frac{\pi}{2}
$$
The signals still have the same amplitude and frequency, but their peaks no longer occur at the same time.

![Addition of two signals with a 90 degree phase difference.](../figures/ch02/phase-addition-90deg.png)

The sum is still a sinusoid at the same frequency. Its amplitude is approximately
$$
\sqrt{2}\approx1.414
$$
and its phase lies between the phases of the two original signals.

The signals still reinforce each other, but less strongly than in the 0° case.

### Case 3: Phase Difference = 180°

Finally, shift the second signal by
$$
180^\circ=\pi
$$
Now the second cosine is the negative of the first:
$$
x_2(t)=-x_1(t)
$$
so
$$
x_1(t)+x_2(t)=0
$$
![Addition of two signals with a 180 degree phase difference.](../figures/ch02/phase-addition-180deg.png)

The sum becomes a line at zero. The two input signals have not disappeared individually; their instantaneous values simply cancel in the sum.

This is **destructive interference**, and in this ideal equal-amplitude case the cancellation is complete.

### The Bigger Lesson

For two equal-amplitude sinusoids of the same frequency, the amplitude of their sum depends on the phase difference $\Delta\phi$.

For individual amplitude $A$,
$$
A_{\text{sum}}=2A\left|\cos\left(\frac{\Delta\phi}{2}\right)\right|
$$
There is no need to memorise this expression yet. The experiment already shows the important behaviour:

- 0° gives maximum reinforcement,
- 90° gives partial reinforcement,
- 180° gives complete cancellation.

Relative phase matters whenever signals of the same frequency combine.

## 2.11 Beats: When Frequencies Are Almost the Same

Now consider two signals whose frequencies are close, but not identical:
$$
f_1=1000\text{ Hz}
$$
and
$$
f_2=1050\text{ Hz}
$$
The 1050 Hz signal completes its cycles slightly faster. Even if the two signals begin aligned, they cannot stay aligned because their relative phase changes continuously.

At some times they reinforce each other strongly. Later they move towards opposite phase and nearly cancel. Eventually they align again.

This repeated reinforcement and cancellation produces **beats**.

### GNU Radio Experiment: Beats

Reuse the addition flowgraph with:

```text
Signal 1
Frequency = 1000 Hz
Amplitude = 1
Signal 2
Frequency = 1050 Hz
Amplitude = 1
```

To make the slow amplitude variation visible, increase the Time Sink window to about 40 ms.

With
$$
f_s=32000\text{ samples/s}
$$
a 40 ms window requires
$$
N=32000\times0.04=1280
$$
samples, so set

```text
Number of Points = 1280
```

![Beat pattern produced by adding 1000 Hz and 1050 Hz signals.](../figures/ch02/beats.png)

The summed waveform grows in amplitude, becomes very small, grows again and continues repeating.

Around 0 ms, the two signals are approximately aligned and reinforce strongly. Around 10 ms, they are approximately 180° apart and nearly cancel. Around 20 ms, they align again.

The frequency difference is
$$
\Delta f=|1050-1000|=50\text{ Hz}
$$
For two nearby sinusoids, the beat rate is the magnitude of this difference:
$$
f_{\text{beat}}=|f_2-f_1|=50\text{ Hz}
$$
so the beat pattern repeats every
$$
T_{\text{beat}}=\frac{1}{50}=20\text{ ms}
$$
which matches the spacing between successive strong-reinforcement regions in the plot.

### Beats Are a Phase Story

Beats are not a separate mystery. They follow directly from the phase-addition behaviour we just observed.

With equal frequencies, the relative phase stays fixed. With slightly different frequencies, the relative phase changes steadily with time. The signals therefore move repeatedly through constructive and destructive combinations.

The chain of ideas is:

**frequency difference → changing relative phase → changing reinforcement and cancellation**

That physical connection is more useful than memorising the beat-frequency formula by itself.

## 2.12 GNU Radio Toolbox
This chapter introduced several useful GNU Radio concepts.

### Multiple Time Sink Inputs

A QT GUI Time Sink can display several streams at once by increasing **Number of Inputs**. This lets us compare signals on the same time axis.

### Number of Points

For a streaming Time Sink, the approximate displayed duration is
$$
T_{\text{display}}=\frac{N}{f_s}
$$
where $N$ is the Number of Points and $f_s$ is the sample rate.

### Variables and Expressions

We continued using

```text
samp_rate
```

and introduced

```text
pi
```

as another variable. GNU Radio block properties can also evaluate expressions such as

```text
pi/2
```

which makes parameter relationships easier to read and modify.

### Add

The **Add** block accepts multiple compatible input streams and produces their sample-by-sample sum.

### Branching

One output stream can feed more than one downstream block. We used this to send the same signal both to the Add block and directly to the Time Sink.

### Reusing a Flowgraph

Several experiments used the same basic flowgraph while changing only one parameter. This is often the clearest way to investigate a signal property because everything else remains fixed.

## 2.13 Explore Further
Before moving on, we can use the same flowgraphs to test a few predictions.

1. Change the amplitude comparison from `0.5, 1, 2` to `1, 2, 3`. Which features of the waveforms change, and which stay fixed?
2. Change the frequency comparison to `250 Hz, 500 Hz, 1 kHz`. Before running it, predict how many cycles of each signal will appear in the same time window.
3. Try a phase difference of 45°:
$$
45^\circ=\frac{\pi}{4}
$$
Before running the flowgraph, predict whether the resulting amplitude should be closer to 2, closer to 0, or somewhere in between.

4. Change the beat experiment from

```text
1000 Hz + 1050 Hz
```

to

```text
1000 Hz + 1010 Hz
```

Predict whether the beat pattern will become faster or slower.

5. Then try

```text
1000 Hz + 1100 Hz
```

and compare the result.

The useful habit is the same one we established in Chapter 1: change one thing, predict the effect, run the experiment and compare the observation with the prediction.

## 2.14 What We Learned
By changing one property at a time, we found that:

- **amplitude** controls how far a waveform moves from its centre value,
- **frequency** tells us how many cycles occur per second,
- **period** tells us how long one cycle takes,
- **phase** describes position within a cycle relative to a reference,
- **DC offset** moves the centre value of a waveform,
- **waveform shape** describes how the signal changes during each cycle.

We then allowed signals to interact. The experiments showed that signals add sample by sample, relative phase determines how equal-frequency sinusoids reinforce or cancel, and a small frequency difference makes the relative phase change continuously, producing beats.

These ideas are simple in isolation, but they will reappear throughout the rest of the book.

## 2.15 Connecting to the Next Chapter
So far, the signals in our GNU Radio experiments have already existed as digital samples inside the computer.

A physical signal arriving from the real world is different. Before software can process it, the analog waveform must be represented by a sequence of samples.

That raises several practical questions. How often should the signal be measured? What happens if the sampling rate is too low? Can two different analog frequencies produce the same sequence of digital samples?

These questions lead directly to one of the most important ideas in digital signal processing: **sampling and aliasing**.