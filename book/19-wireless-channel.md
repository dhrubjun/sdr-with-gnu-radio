# Chapter 19: The Wireless Channel

## Main Question

**Why does the receiver never see exactly what the transmitter sent?**

Chapter 18 developed the pulse-shaping and matched-filtering structure of a digital link.

We saw how symbols can be shaped with a root-raised-cosine (RRC) filter, passed through a matching receiver filter, and sampled at suitable symbol instants. Under ideal conditions, the receiver can recover clean symbol observations.

This chapter keeps that same basic architecture but uses QPSK so that channel effects are easy to recognize in the constellation.

The important new assumption to remove is the channel itself.

A real wireless channel is not a transparent connection between transmitter and receiver. The electromagnetic wave propagates through space and through an environment containing distance, obstacles, reflections, noise, and independent transmitter and receiver oscillators.

By the time the waveform reaches the receiver, it may be weaker, noisy, frequency shifted, mixed with delayed copies of itself, or sampled with a clock that does not quite agree with the transmitter clock.

This chapter focuses on those **impairments**, not on correcting them.

We will begin with a clean pulse-shaped QPSK link and then disturb one assumption at a time. For each impairment, we will ask what it means physically, what it does to the waveform or constellation, and what problem it creates for the receiver.

## 19.1 Experiment 19.1: A Clean Reference Link

Our first experiment establishes a reference.

We reuse the pulse-shaping and matched-filtering structure from Chapter 18, now with QPSK symbols.

| Parameter | Value |
|---|---:|
| Sample rate | `32000` samples/s |
| Symbol rate | `1000` symbols/s |
| Samples per symbol | `32` |
| RRC span | `8` symbols |
| Number of RRC taps | `257` |
| RRC roll-off factor | `0.35` |
| QPSK I values | `[-1, +1]` |
| QPSK Q values | `[-1, +1]` |

![Clean QPSK reference flowgraph](../figures/ch19/ch19-exp1-clean-reference-flowgraph.png)

The signal passes through the TX RRC filter, an ideal channel, the RX matched RRC filter, and a fixed symbol-rate sampler before reaching the Constellation Sink.

For an ideal channel,

$$
r(t)=s(t)
$$

The channel does not attenuate, rotate, delay, distort, or add noise to the waveform.

![Clean received QPSK constellation](../figures/ch19/ch19-exp1-clean-reference-constellation.png)

The four clusters remain close to

$$
(\pm1,\pm1)
$$

This is our reference. Each later experiment changes one part of the channel and compares the result with this clean case.

## 19.2 The Simplest Channel Effect: Attenuation

Imagine increasing the distance between a transmitter and receiver.

The radio wave spreads as it propagates. Buildings, terrain, walls, antenna orientation, absorption, and other propagation effects can further reduce the signal reaching the receiving antenna.

A simple first model is

$$
r(t)=A\,s(t)
$$

where $A$ is the channel amplitude gain.

If

$$
0<A<1
$$

the signal is attenuated.

Attenuation changes the signal amplitude without, by itself, adding randomness or memory to the channel.

## 19.3 Experiment 19.2: Channel Attenuation

We extend the clean link by scaling the transmitted complex signal before the receiver matched filter.

The control is

```text
ID: channel_gain
Label: Channel Gain
Default Value: 1.0
```

For the retained result,

```text
Channel Gain: 0.5
```

If the original QPSK points are near $(\pm1,\pm1)$, multiplying the signal by 0.5 should move them toward $(\pm0.5,\pm0.5)$.

![QPSK constellation with channel gain 0.5](../figures/ch19/ch19-exp2-attenuation-constellation.png)

That is what we observe.

### Physical Meaning of the Gain

A lower `channel_gain` represents a smaller received signal amplitude.

If the complex amplitude is multiplied by $A$, signal power scales as

$$
P_r=A^2P_t
$$

For

$$
A=0.5
$$

we obtain

$$
A^2=0.25
$$

so halving the amplitude corresponds to one quarter of the original signal power.

The constellation has contracted, but the four symbol locations are still clearly distinguishable. Attenuation becomes more serious when the desired signal must compete with noise.

## 19.4 A Weak Signal Must Compete with Noise

Every practical receiver contains unwanted random contributions from thermal processes, receiver electronics, and the surrounding electromagnetic environment.

A simple model is

$$
r(t)=A\,s(t)+n(t)
$$

where $n(t)$ represents additive noise.

If the desired signal becomes weaker while the noise level does not decrease by the same proportion, the receiver has less separation between the desired signal and the random disturbance.

This is the physical meaning of a falling signal-to-noise ratio.

## 19.5 Experiment 19.3: Attenuation and Noise

We now combine attenuation with Gaussian noise.

The useful controls are

```text
Channel Gain
Noise Amplitude
```

For the retained comparison,

```text
Noise Amplitude: 0.1
```

is held fixed while the channel gain is changed.

At the higher received signal level, the four noisy clusters remain well separated.

![High-SNR received QPSK constellation](../figures/ch19/ch19-exp3-high-snr-constellation.png)

Now reduce the desired signal strength while leaving the noise unchanged.

![Low-SNR received QPSK constellation](../figures/ch19/ch19-exp3-low-snr-constellation.png)

The two mechanisms have different signatures.

Attenuation contracts the constellation toward the origin. Additive noise spreads individual samples randomly around their ideal locations.

When the desired signal becomes too small relative to the noise, the constellation clouds approach or cross the decision boundaries and symbol decisions become less reliable.

## 19.6 When the Transmitter and Receiver Disagree About Frequency

Real radios use independent oscillators. Their carrier references are never mathematically identical.

If the residual carrier-frequency difference is $\Delta f$, the complex-baseband signal can be represented as

$$
r(t)=s(t)e^{j2\pi\Delta f t}
$$

The corresponding phase error is

$$
\phi(t)=2\pi\Delta f t
$$

A fixed frequency error therefore does not produce one fixed phase rotation. The phase error continues to accumulate with time.

Oscillator tolerance, temperature drift, differences between hardware references, and Doppler can all contribute to this relative frequency error.

## 19.7 Experiment 19.4: Carrier Frequency Offset

We introduce a carrier-frequency mismatch into the clean link.

The retained result uses

```text
Frequency Offset: 20 Hz
```

![QPSK constellation with 20 Hz carrier-frequency offset](../figures/ch19/ch19-exp4-frequency-offset-20hz.png)

Instead of four stationary clusters, the accumulated samples trace a ring-like pattern.

### Why Does a Frequency Offset Produce a Ring?

At any one instant, QPSK still has four symbol states separated by $90^\circ$.

The modulation has not changed into a continuous ring constellation.

The frequency offset rotates all four QPSK points continuously. The Constellation Sink displays a history of samples collected during that rotation, so the four points sweep around the origin and eventually produce a ring-like trace.

This is very different from attenuation.

Attenuation changes the radius of the constellation. Carrier-frequency offset continuously changes its angle.

We deliberately do not correct the offset in this chapter. Carrier synchronization is a receiver function, not a channel impairment.

## 19.8 The Channel Can Deliver More Than One Copy

A radio wave can reach the receiver through several propagation paths.

One path may be direct. Another may reflect from a wall, building, vehicle, terrain feature, or another object.

The reflected path is usually longer, so its copy arrives later. It is also often weaker because it has travelled farther and because a reflecting surface does not redirect all incident energy toward the receiving antenna.

A reflected component can also have a different phase. Extra propagation distance creates additional carrier phase accumulation, and the reflection itself may introduce another phase change.

A multipath component is therefore characterized by its delay and by a generally complex path coefficient that describes its amplitude and phase.

A simple two-path model is

$$
r(t)=s(t)+a\,s(t-\tau)
$$

where $\tau$ is the relative delay and $a$ is the coefficient of the delayed path.

In the retained experiment, `echo_gain` is a positive real value, so we vary the delayed-path strength without separately introducing a path phase shift.

## 19.9 Experiment 19.5: One Delayed Copy

Before using a packaged channel model, we build one delayed path explicitly.

The transmitted waveform is split into two branches. One branch passes directly to an Add block. The second passes through Delay and Gain before being added back to the direct path.

The controls are

```text
ID: echo_delay
Label: Echo Delay (samples)
Default Value: 8
Start: 0
Stop: 32
Step: 1
```

and

```text
ID: echo_gain
Label: Echo Gain
Default Value: 0
Start: 0
Stop: 1
Step: 0.05
```

### What Does Changing the Delay Mean Physically?

If a reflected path is longer than the direct path by an excess distance $\Delta d$, its relative propagation delay is approximately

$$
\tau=\frac{\Delta d}{c}
$$

In the discrete-time simulation,

$$
\tau=\frac{D}{f_s}
$$

where $D$ is the delay in samples.

With `sps = 32`,

```text
8 samples  = 0.25 symbol period
16 samples = 0.50 symbol period
32 samples = 1.00 symbol period
```

Increasing `echo_delay` therefore represents a greater excess propagation delay relative to the symbol duration.

### Zero Relative Delay

First use

```text
Echo Gain: 0.5
Echo Delay: 0 samples
```

Then

$$
r(t)=s(t)+0.5s(t)=1.5s(t)
$$

The two copies are aligned and add constructively.

This is an important result: the mere existence of a second path does not automatically create ISI.

### Quarter-Symbol Delayed Echo

Now use

```text
Echo Gain: 0.5
Echo Delay: 8 samples
```

so that

$$
\tau=0.25T_s
$$

![QPSK with a quarter-symbol delayed echo](../figures/ch19/ch19-exp5-quarter-symbol-delayed-echo.png)

The constellation spreading is structured rather than random.

The echo is not independent noise. It is a delayed copy of the transmitted pulse-shaped waveform, so its effect depends on the transmitted symbol sequence.

This delayed copy disturbs the zero-ISI relationships established by the pulse-shaping and matched-filtering pair.

### One-Symbol Delayed Echo

Now set

```text
Echo Gain: 0.5
Echo Delay: 32 samples
```

At the symbol sampling instants, the retained setup is well described by

$$
r_k=s_k+0.5s_{k-1}
$$

The current received sample now contains the current QPSK symbol plus half of the previous symbol.

The channel has memory.

![QPSK with a one-symbol delayed echo](../figures/ch19/ch19-exp5-one-symbol-delayed-echo.png)

For example, if

$$
s_k=1+j
$$

then the previous symbol can be

$$
s_{k-1}\in\{1+j,\;1-j,\;-1+j,\;-1-j\}
$$

and therefore

$$
0.5s_{k-1}\in\{0.5+j0.5,\;0.5-j0.5,\;-0.5+j0.5,\;-0.5-j0.5\}
$$

The resulting I and Q coordinates are drawn from

$$
I,Q\in\{-1.5,-0.5,+0.5,+1.5\}
$$

so the received samples can form approximately sixteen locations.

### This Is Not 16-QAM

The transmitter is still sending QPSK.

The additional locations appear because each received sample depends on both the current and previous QPSK symbols. They are a channel-distortion pattern, not a new modulation format.

This is ISI in a direct form: one symbol contributes to the observation used to decide another.

### Connection to Chapter 18

Nyquist pulse shaping allows neighbouring pulses to overlap while their unwanted contributions vanish at the intended sampling instants.

Multipath adds shifted copies of the waveform. Those copies are no longer guaranteed to have their zero crossings aligned with the receiver's symbol decisions.

The wireless channel can therefore reintroduce ISI even when the transmitter and receiver pulse-shaping filters are correctly designed.

## 19.10 Multipath and Fading

The two-path experiment used a positive real echo coefficient.

In a real channel, different paths can have different amplitudes, delays, and phases.

Their contributions may reinforce one another or partially cancel. If the transmitter, receiver, or surrounding environment moves, those relationships can change with time, causing the received signal strength to rise and fall.

This is the beginning of the idea of **fading**.

Path loss describes an overall reduction in received signal strength. Multipath describes the presence of several propagation copies. Fading describes variation in the received signal as those path contributions combine differently.

We do not develop Rayleigh or Rician fading statistics here. The purpose is to establish the physical connection between multiple propagation paths and time-varying received signal strength.

## 19.11 Experiment 19.6: GNU Radio Channel Model

Until now, we built impairments separately so that their meanings remained visible.

GNU Radio also provides a **Channel Model** block that packages several common channel effects into one simulation component.

![QPSK link using the GNU Radio Channel Model](../figures/ch19/ch19-exp6-channel-model-flowgraph.png)

The neutral settings are

```text
Noise Voltage: 0
Frequency Offset: 0
Epsilon: 1
Taps: [1.0]
Seed: 0
```

With these values, the clean QPSK link is preserved.

Increasing `Noise Voltage` adds random spreading, as expected from Experiment 19.3.

The Channel Model frequency offset is normalized to the sample rate:

$$
f_{\text{norm}}=\frac{\Delta f}{f_s}
$$

For a 20 Hz offset at 32 kHz,

$$
f_{\text{norm}}=\frac{20}{32000}=0.000625
$$

We therefore use the physical control

```text
ID: freq_offset_hz
Label: Frequency Offset (Hz)
Default Value: 0
Start: 0
Stop: 100
Step: 5
```

and supply

```text
freq_offset_hz / samp_rate
```

to the Channel Model.

The `Taps` parameter represents a discrete-time channel impulse response:

$$
r[n]=\sum_{\ell}h[\ell]s[n-\ell]
$$

Tap delay represents relative propagation delay. Tap magnitude represents path strength, and tap phase represents path phase shift.

The explicit Delay + Gain + Add experiment remains the clearer physical demonstration of a second propagation path. The Channel Model is useful once that physical meaning is understood.

`Seed` is different from the other parameters. It selects a pseudorandom noise realization for the simulation; it is not itself a physical channel impairment.

One parameter remains: `Epsilon`.

## 19.12 When the Sampling Clocks Disagree

A digital receiver depends on a sampling clock as well as a carrier reference.

If the transmitter and receiver sampling rates differ slightly, their relative timing position does not remain fixed. It drifts.

This is different from a fixed timing offset.

A fixed timing offset shifts the sampling position by approximately the same amount from symbol to symbol. A sample-rate mismatch accumulates, so the receiver gradually samples different parts of the symbol waveform.

Chapter 18 showed why the sampling position matters. The eye diagram describes the oversampled waveform around possible sampling instants and therefore shows the available timing margin.

The constellation is a different view. It shows the complex samples actually selected by the receiver. If a fixed sampler gradually moves away from the correct symbol centres, those selected constellation samples become distorted even though the transmitted QPSK constellation itself has not changed.

## 19.13 Experiment 19.7: Sample-Rate Mismatch

We reuse the Channel Model with

```text
Noise Voltage: 0
Frequency Offset: 0
Taps: [1.0]
```

and vary `Epsilon`.

The ideal value is

```text
Epsilon: 1.0
```

The retained result uses

```text
Epsilon: 1.001
```

so

$$
\epsilon-1=0.001
$$

which corresponds to a 0.1% relative mismatch in this model.

![QPSK with sample-rate mismatch](../figures/ch19/ch19-exp7-sample-rate-mismatch.png)

The mismatch is small, but a rate error accumulates with time.

Our fixed `Keep 1 in N` sampler does not contain a timing-recovery loop that can follow that drift.

At some moments it samples near the desired symbol centre. At others it samples closer to transitions, where neighbouring pulse contributions are larger.

The transmitter has not changed the QPSK symbol alphabet. The receiver is progressively observing the waveform at the wrong times.

| Impairment | What changes with time? | Typical constellation effect |
|---|---|---|
| Carrier-frequency offset | carrier phase | constellation rotates |
| Sample-rate mismatch | sampling position | constellation spreads and distorts |

Larger exploratory values such as `1.01` and `1.1` make the effect more obvious, but `1.001` is more instructive because it shows why a small persistent mismatch cannot simply be ignored.

Timing recovery is deliberately not added here. It is a receiver correction that will be introduced later.

## 19.14 Reading Channel Impairments from the Constellation

The same QPSK link now shows several distinct visual signatures.

| Impairment | Physical cause | Main constellation signature |
|---|---|---|
| Attenuation | weaker received propagation path | constellation contracts toward origin |
| Additive noise | unwanted random contributions | random clouds around symbol locations |
| Frequency offset | TX/RX carrier mismatch | continuous constellation rotation |
| Delayed copy | multipath propagation | structured distortion or splitting |
| Sample-rate mismatch | TX/RX sampling-rate mismatch | drifting sampling phase and widespread distortion |

These are useful patterns, not perfect diagnostic rules.

A real receiver may contain several impairments at the same time, and their signatures can overlap.

## 19.15 Channel Impairment Is Not Receiver Correction

It is important to separate what the channel does from what the receiver later does in response.

| Channel or link impairment | Typical receiver response |
|---|---|
| attenuation | gain control |
| carrier-frequency offset | carrier synchronization |
| timing drift | timing recovery |
| multipath-induced ISI | equalization |
| unknown channel response | channel estimation |

This chapter focuses on the left-hand side.

The next chapters progressively develop the receiver mechanisms on the right-hand side.

## 19.16 GNU Radio Toolbox

Several GNU Radio blocks play important roles in the channel experiments.

| GNU Radio Block | Role in This Chapter |
|---|---|
| Multiply Const | models simple amplitude scaling |
| Noise Source | adds Gaussian disturbance |
| Delay | creates a delayed copy of the waveform |
| Add | combines direct and delayed paths |
| Channel Model | packages noise, frequency offset, sample-rate mismatch, and channel taps |
| Keep 1 in N | provides the fixed symbol-rate sampling used for observation |
| QT GUI Constellation Sink | shows the complex samples selected by the receiver |

### Delay

The **Delay** block shifts a stream by a specified number of samples.

In Experiment 19.5, it represents the additional propagation time of the reflected path.

The block does not create new information. It creates a later copy of the same complex-baseband waveform.

### Channel Model

The **Channel Model** block combines several common effects:

| Parameter | Physical interpretation |
|---|---|
| `Noise Voltage` | additive random noise |
| `Frequency Offset` | normalized carrier-frequency mismatch |
| `Epsilon` | relative sample-rate mismatch |
| `Taps` | discrete-time channel impulse response |
| `Seed` | pseudorandom noise realization |

The block is most useful after the effects have been understood separately.

It is a convenient simulator, not a substitute for the underlying physical interpretation.

### Keep 1 in N

The **Keep 1 in N** block selects one sample out of every `N` samples.

In these experiments it acts as a deliberately simple fixed symbol-rate sampler.

It does not perform timing recovery. If the correct sampling phase changes, as it does under sample-rate mismatch, the block continues selecting samples at the same fixed pattern and eventually moves away from the desired decision instants.

## 19.17 Explore Further

The channel experiments are well suited to prediction before execution.

1. Keep the noise level fixed and gradually reduce `channel_gain`. Predict how the constellation radius and decision margin should change.

2. Keep the gain fixed and increase the Gaussian-noise amplitude. Compare this random spreading with the structured distortion produced by multipath.

3. In the carrier-frequency-offset experiment, compare small and larger offsets. Observe how the rate of constellation rotation changes.

4. In the two-path experiment, keep `Echo Gain = 0.5` and compare delays of 0, 8, 16, and 32 samples.

5. Keep the echo delay fixed and change the echo gain. Observe how strongly the delayed path influences the received constellation.

6. Replace a positive real echo coefficient with a complex coefficient and observe how path phase changes the multipath pattern.

7. In the Channel Model, compare `Epsilon = 1.0`, `1.001`, and `1.01`. Watch how a small rate mismatch accumulates over time.

8. Compare an oversampled time or eye view with the constellation when timing is drifting. Keep in mind that the eye describes timing margin around possible sample positions, while the constellation shows the samples actually selected.

## 19.18 What We Learned

The wireless channel is not a transparent wire.

Attenuation reduces the received signal amplitude, and signal power scales with the square of that amplitude.

Attenuation becomes more important when the receiver noise does not decrease with the desired signal. Additive noise spreads constellation samples randomly, while attenuation contracts the entire constellation.

Carrier-frequency mismatch creates a phase error that accumulates with time. In a Constellation Sink, the history of continuously rotating QPSK points can appear as a ring.

Multipath means that the receiver can observe delayed, scaled, and phase-shifted copies of the transmitted waveform. A second path with zero relative delay does not automatically create ISI, but delayed copies can disturb the zero-ISI relationships created by pulse shaping and matched filtering.

A one-symbol echo makes the current received sample depend on the previous symbol. The additional received locations in that experiment are not 16-QAM. The transmitter remains QPSK; the extra points are created by channel memory.

Multiple propagation paths can reinforce or cancel one another, which leads naturally to the idea of fading.

GNU Radio's Channel Model packages several common impairments after their physical meanings are understood. Its frequency-offset input is normalized to the sample rate, its channel taps describe a discrete-time impulse response, and `Epsilon` models relative sample-rate mismatch.

Sample-rate mismatch differs from a fixed timing offset because the timing error accumulates. Even a small persistent mismatch can cause a fixed sampler to move away from the desired symbol centres.

The eye diagram and constellation remain different measurements. The eye describes the oversampled waveform and timing margin around possible sampling instants. The constellation shows the complex samples actually selected for symbol decisions.

Most importantly, each simulation control now has a physical interpretation.

A smaller gain represents a weaker received signal. Added noise represents random unwanted contributions. Frequency offset represents disagreement between carrier references. A delayed copy represents another propagation path. Echo delay represents excess path delay. Echo gain represents path strength. `Epsilon` represents sampling rates that do not exactly agree.

Once those meanings are clear, the changing constellation becomes a picture of what the communication link is doing to the waveform.

## 19.19 Connecting to the Next Chapter

Chapter 18 showed how pulse shaping and matched filtering can create clean symbol observations when the channel is ideal.

This chapter showed how the wireless channel can break that result.

Among the impairments we introduced, multipath is especially important because it gives the channel memory. A delayed copy can make the current received symbol depend on previous symbols:

$$
r_k=s_k+0.5s_{k-1}
$$

The receiver now needs a way to compensate for that predictable channel distortion.

That leads directly to **Chapter 20: Channel Equalization**.

We will begin by assuming that the multipath channel is known and ask how a receiver filter can undo part of its effect. From there, we can move toward adaptive equalizers that learn the required correction from the received signal itself.