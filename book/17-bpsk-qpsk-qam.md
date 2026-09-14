# Chapter 17: BPSK, QPSK and QAM

## Main Question

**How can I and Q carry digital information?**

In Chapter 16, we learned how to turn abstract digital symbols into actual signal amplitudes. A 2-PAM symbol could be represented by one of two levels,

$$
-1,\quad +1
$$

and 4-PAM extended the same idea to four levels,

$$
-3,\quad -1,\quad +1,\quad +3
$$

All of those symbols lived on one amplitude axis.

Earlier in the book, we also developed the complex I/Q representation,

$$
x[n]=I[n]+jQ[n]
$$

This gives us another possibility. If a digital symbol can choose an amplitude on the I axis, it can also choose an amplitude on the Q axis.

That simple idea leads naturally to many of the constellations used in digital communication.

In this chapter, we will develop the idea experimentally. We will begin with BPSK, where only one dimension is needed. Then we will allow both I and Q to carry information and build QPSK. Finally, we will reuse the 4-PAM levels from Chapter 16 on both axes to construct 16-QAM.

We will not begin with ready-made modulation blocks. Instead, we will build the constellation points ourselves so that their meaning is clear before GNU Radio packages the same operations inside higher-level tools.

## 17.1 From One Amplitude Axis to the I/Q Plane

A PAM symbol can be pictured as a point on a line. With 2-PAM, the two allowed amplitudes are \( -1 \) and \( +1 \).

A complex symbol gives us a second dimension. Instead of choosing only one amplitude, we choose a pair of coordinates,

$$
(I,Q)
$$

and write the resulting complex symbol as

$$
s=I+jQ
$$

For example,

$$
s=1+j
$$

means

$$
I=1,\quad Q=1
$$

so the symbol appears at the point \( (1,1) \) in the I/Q plane.

A digital constellation is therefore a set of allowed I/Q coordinate pairs. Each allowed point represents one information symbol.

We will now build those points directly in GNU Radio.

## 17.2 Experiment 17.1: From 2-PAM to BPSK

### Why Start with PAM Again?

At first glance, BPSK may seem different from the PAM signals in Chapter 16. BPSK stands for **Binary Phase Shift Keying**, while PAM represents information using amplitude.

At complex baseband, however, the connection is direct.

Take the same two levels used for 2-PAM,

$$
-1,\quad +1
$$

and place them on the I axis while keeping Q equal to zero:

$$
s\in\{-1+j0,\,+1+j0\}
$$

These are the two complex-baseband symbols of BPSK.

The experiment therefore begins with something familiar. We map binary symbol indices onto \( -1 \) and \( +1 \), just as we did for 2-PAM. The new step is to treat those values as the real part of a complex signal.

### Flowgraph

![Experiment 17.1 flowgraph: constructing BPSK from the two PAM levels](../figures/ch17/ch17-exp1-bpsk-from-2pam-flowgraph.png)

The symbol mapping is

```text
0 → -1
1 → +1
```

The mapped values are repeated for visualization and connected to the real input of **Float to Complex**. The imaginary input is held at zero.

Important settings are:

```text
Chunks to Symbols
Output Type: Float
Symbol Table: [-1, 1]
Dimension: 1

Float to Complex
Real input: mapped ±1 symbols
Imaginary input: 0
```

The Constellation Sink displays the resulting complex samples.

![Experiment 17.1 result: the two BPSK constellation points on the I axis](../figures/ch17/ch17-exp1-bpsk-constellation.png)

Only two points appear:

$$
(-1,0)\quad\text{and}\quad(+1,0)
$$

At complex baseband, BPSK therefore looks exactly like 2-PAM placed on the I axis.

But this raises an important question. If the complex-baseband symbols are simply \( -1 \) and \( +1 \), why is the modulation called phase shift keying?

To answer that, we need to see what those signs do to a carrier.

## 17.3 Experiment 17.2: Why BPSK Is Phase Shift Keying

### From a Baseband Sign to a Carrier Phase

Let the BPSK symbol be

$$
a(t)\in\{-1,+1\}
$$

and multiply it by a cosine carrier:

$$
x(t)=a(t)\cos(2\pi f_ct)
$$

When the symbol is \( +1 \),

$$
x(t)=\cos(2\pi f_ct)
$$

so the transmitted waveform has the same phase as the reference carrier.

When the symbol is \( -1 \),

$$
x(t)=-\cos(2\pi f_ct)
$$

and since

$$
-\cos(\theta)=\cos(\theta+\pi)
$$

the carrier has been shifted by \( 180^\circ \).

The two baseband signs therefore select two carrier phases separated by \( 180^\circ \).

### Flowgraph

![Experiment 17.2 flowgraph: multiplying the BPSK symbol by a carrier](../figures/ch17/ch17-exp2-bpsk-phase-shift-flowgraph.png)

The important parameters are:

| Parameter | Value |
|---|---:|
| Sample rate | 32 kS/s |
| Symbol rate | 1 ksymbol/s |
| Carrier frequency | 4 kHz |
| BPSK levels | -1, +1 |

The two GUI displays are titled:

```text
BPSK I Component
BPSK Passband Waveform
```

The passband Time Sink contains two traces:

```text
Reference Carrier
BPSK Carrier
```

A 4 kHz carrier and a 1 ksymbol/s symbol rate give four carrier cycles per symbol. This choice is not required for BPSK, but it makes the phase reversal easy to see.

![Experiment 17.2 result: BPSK symbol sequence and passband phase reversal](../figures/ch17/ch17-exp2-bpsk-phase-shift.png)

Reading the two plots together, when the BPSK symbol is \( +1 \), the modulated carrier aligns with the reference carrier. When the symbol is \( -1 \), it has the opposite polarity.

The magnitude of the carrier is unchanged. What changes is its phase:

```text
symbol +1 → 0° carrier phase
symbol -1 → 180° carrier phase
```

This is the connection between the two PAM-like baseband values and the phase-shift-keyed passband waveform.

### Looking Closely at a Phase Transition

The zoomed result makes one symbol transition easier to inspect.

![Zoomed BPSK waveform around a phase transition](../figures/ch17/ch17-exp2-bpsk-phase-transition-zoom.png)

Before the transition, the BPSK carrier is opposite to the reference. After the symbol changes sign, the BPSK carrier becomes aligned with it.

The passband waveform can also change abruptly at a symbol boundary. Our symbol waveform is rectangular, so the multiplier changes instantaneously between \( -1 \) and \( +1 \). If the carrier is not at zero at that instant, the resulting waveform contains a discontinuity.

This is not an error in the flowgraph. It is a consequence of using rectangular symbol pulses.

We will examine the bandwidth consequences of these abrupt transitions in Chapter 18 when we introduce pulse shaping.

### Try It Yourself

We can change the carrier frequency while keeping the symbol rate unchanged and predict where the symbol transitions will occur within the carrier cycle.

The BPSK principle does not depend on having exactly four carrier cycles per symbol. That value was chosen only to make the phase reversal easy to visualize.

## 17.4 Experiment 17.3: BPSK Decision Regions and Noise

Chapter 16 showed that a noisy PAM receiver does not require every received amplitude to land exactly on an ideal level. It only needs to decide which allowed symbol is the most likely.

For BPSK, the two ideal complex-baseband points are

$$
-1+j0\quad\text{and}\quad+1+j0
$$

Their midpoint is

$$
I=0
$$

In one-dimensional PAM, this was a decision threshold. In the I/Q plane, it becomes a vertical **decision boundary**.

For an ideal coherently aligned BPSK receiver, the hard decision is

$$
I<0\Rightarrow -1
$$

$$
I>0\Rightarrow +1
$$

The Q coordinate does not affect this ideal BPSK decision because the two reference symbols differ only along the I axis.

### Adding Complex Gaussian Noise

We add complex Gaussian noise to the clean BPSK signal before displaying the result.

The noise amplitude is controlled with a QT GUI Range:

```text
ID: noise_amp
Default: 0.2
Start: 0
Stop: 1.5
Step: 0.05
```

The Constellation Sink is titled:

```text
BPSK with Gaussian Noise
```

and compares:

```text
Ideal BPSK
Noisy BPSK
```

Because the added noise is complex, the received samples move in both I and Q even though the transmitted BPSK symbols themselves have \( Q=0 \).

![BPSK with Gaussian noise amplitude 0.2](../figures/ch17/ch17-exp3-bpsk-noise-0p2.png)

At a noise amplitude of 0.2, the two ideal points have become compact clouds. Many samples now have nonzero Q components, but the two clouds remain well separated by the \( I=0 \) boundary.

For this ideal detector, a vertical displacement alone does not change the decision. For example,

$$
r=0.8+j0.7
$$

still has positive I and remains in the \( +1 \) decision region.

What matters is whether the received point crosses the decision boundary.

![BPSK with stronger Gaussian noise, showing samples crossing the decision boundary](../figures/ch17/ch17-exp3-bpsk-decision-errors-0p5.png)

At a noise amplitude of 0.5, the clouds spread far enough that some samples enter the opposite region.

If \( +1+j0 \) was transmitted but the received sample becomes

$$
r=-0.1+j0.2
$$

then \( I<0 \), so the hard detector decides \( -1 \).

The useful way to interpret the constellation is geometrically:

> A hard-decision error becomes possible when an impairment moves a received symbol across a decision boundary.

This viewpoint becomes even more useful once both I and Q carry information.

## 17.5 Experiment 17.4: Building QPSK from I and Q

BPSK occupies the I/Q plane, but only one dimension carries information:

$$
I\in\{-1,+1\},\qquad Q=0
$$

The Q dimension is unused.

Now let both coordinates independently take the values \( -1 \) and \( +1 \):

$$
I\in\{-1,+1\}
$$

$$
Q\in\{-1,+1\}
$$

There are

$$
2\times2=4
$$

possible coordinate pairs:

| Bit pair | I | Q | Complex symbol |
|---|---:|---:|---|
| 00 | -1 | -1 | \( -1-j \) |
| 01 | -1 | +1 | \( -1+j \) |
| 10 | +1 | -1 | \( +1-j \) |
| 11 | +1 | +1 | \( +1+j \) |

For this construction, the first bit selects I and the second selects Q. Each bit uses the mapping

```text
0 → -1
1 → +1
```

### Constructing the Two Dimensions Explicitly

We use controlled sequences so that every combination appears:

```text
I bits: 0, 0, 1, 1
Q bits: 0, 1, 0, 1
```

After mapping,

```text
I: -1, -1, +1, +1
Q: -1, +1, -1, +1
```

At each symbol interval, one I value and one Q value form a single complex symbol.

![Experiment 17.4 flowgraph: building QPSK explicitly from separate I and Q symbol streams](../figures/ch17/ch17-exp4-qpsk-iq-construction-flowgraph.png)

The important settings are:

```text
I Vector Source
Output Type: Byte
Vector: [0, 0, 1, 1]
Repeat: Yes

Q Vector Source
Output Type: Byte
Vector: [0, 1, 0, 1]
Repeat: Yes

I Chunks to Symbols
Symbol Table: [-1, 1]
Output Type: Float

Q Chunks to Symbols
Symbol Table: [-1, 1]
Output Type: Float

Float to Complex
Real input: I symbols
Imaginary input: Q symbols
```

The Time Sink is titled

```text
QPSK I and Q Components
```

with traces

```text
I Symbol
Q Symbol
```

and the Constellation Sink is titled

```text
QPSK Constellation
```

![Experiment 17.4 result: I and Q symbol levels and the resulting four-point QPSK constellation](../figures/ch17/ch17-exp4-qpsk-iq-constellation.png)

Both I and Q now carry one binary coordinate. GNU Radio combines the simultaneous values as

$$
s=I+jQ
$$

and each pair becomes one constellation point.

We did not use a ready-made QPSK modulator. The QPSK constellation appeared simply by combining two binary dimensions.

### One Symbol, Not Two Separate Transmissions

The two Time Sink traces show separate I and Q values, but they should not be interpreted as two unrelated symbols.

At each symbol interval, the pair \( (I,Q) \) defines **one complex symbol**.

For example,

$$
I=-1,\qquad Q=+1
$$

gives

$$
s=-1+j
$$

and the Constellation Sink plots one point at \( (-1,+1) \).

I and Q are two orthogonal signal dimensions used to describe the same complex symbol.

### Why QPSK Carries Two Bits per Symbol

There are four possible constellation points, so

$$
k=\log_2(4)=2
$$

bits are required to select one symbol.

Using the bit-rate and symbol-rate relationship from Chapter 15,

$$
R_b=kR_s
$$

QPSK gives

$$
R_b=2R_s
$$

A 1 ksymbol/s QPSK stream can therefore represent 2 kbit/s before coding or other overhead is included.

### Why These Four Points Are Called QPSK

All four points have the same magnitude:

$$
|s|=\sqrt{I^2+Q^2}=\sqrt{2}
$$

but they have different phases.

| I | Q | Phase |
|---:|---:|---:|
| +1 | +1 | \( 45^\circ \) |
| -1 | +1 | \( 135^\circ \) |
| -1 | -1 | \( 225^\circ \) or \( -135^\circ \) |
| +1 | -1 | \( 315^\circ \) or \( -45^\circ \) |

The four symbols therefore have equal magnitude and four possible phases separated by \( 90^\circ \).

That is Quadrature Phase Shift Keying.

## 17.6 I/Q and Amplitude/Phase Are Two Views of the Same Symbol

A complex symbol can be written in Cartesian form as

$$
s=I+jQ
$$

or in polar form as

$$
s=Ae^{j\phi}
$$

where

$$
A=\sqrt{I^2+Q^2}
$$

and

$$
\phi=\operatorname{atan2}(Q,I)
$$

These are two descriptions of the same complex point.

For example,

$$
s=3+j
$$

has coordinates

$$
I=3,\qquad Q=1
$$

and magnitude and phase

$$
A=\sqrt{10}
$$

$$
\phi\approx18.4^\circ
$$

This distinction helps separate two ideas that are easy to mix together:

- **I/Q is a representation** of a complex signal.
- **PSK and QAM are modulation schemes** that define particular sets of allowed complex symbols.

For ideal PSK, all constellation points have the same magnitude and differ in phase.

Rectangular QAM is constructed by choosing amplitude levels independently on I and Q. Its constellation points generally have different overall magnitudes as well as different phases.

Using the quadrature convention adopted in this book, a passband signal can be written as

$$
x(t)=I\cos(2\pi f_ct)-Q\sin(2\pi f_ct)
$$

The cosine and sine carriers are \( 90^\circ \) apart. I controls the amplitude of one quadrature component and Q controls the other. Their sum produces the passband amplitude and phase represented by the complex symbol.

I/Q coordinates and amplitude/phase are therefore different views of the same signal.

## 17.7 Experiment 17.5: QPSK Decision Regions and Noise

BPSK required only one decision boundary because only the I coordinate carried information.

QPSK uses both coordinates, so the receiver must determine the sign of both I and Q.

The two boundaries are

$$
I=0
$$

and

$$
Q=0
$$

These divide the I/Q plane into four decision regions.

An ideal QPSK hard detector can therefore be viewed as two simultaneous binary decisions:

```text
sign of I → I decision
sign of Q → Q decision
```

### Adding Noise

We extend Experiment 17.4 by adding complex Gaussian noise to the QPSK stream. The clean and noisy symbols are displayed together.

The noise control remains:

```text
ID: noise_amp
Default: 0.2
Start: 0
Stop: 1.5
Step: 0.05
```

The Constellation Sink is titled

```text
QPSK with Gaussian Noise
```

with traces

```text
Ideal QPSK
Noisy QPSK
```

![QPSK with Gaussian noise amplitude 0.2](../figures/ch17/ch17-exp5-qpsk-noise-0p2.png)

At a noise amplitude of 0.2, the four clouds remain compact and stay within their respective decision regions.

![QPSK with stronger Gaussian noise, showing overlap across the I and Q decision boundaries](../figures/ch17/ch17-exp5-qpsk-decision-errors-0p6.png)

At 0.6, some received samples cross the boundaries.

A point can cross \( I=0 \) while keeping the same sign of Q, cross \( Q=0 \) while keeping the same sign of I, or cross both boundaries.

For example, suppose

$$
s=1+j
$$

was transmitted.

If the received point becomes

$$
r=-0.2+j0.8
$$

the I decision changes while the Q decision remains positive.

If instead

$$
r=0.7-j0.1
$$

the Q decision changes.

If the received point becomes

$$
r=-0.2-j0.3
$$

both coordinate decisions change.

The threshold-crossing idea from Chapter 16 is now operating independently in two dimensions.

## 17.8 Experiment 17.6: Breaking the QPSK Constellation

Noise is only one reason a received constellation may differ from the ideal one.

Random noise spreads individual samples into clouds. Other impairments can move the entire constellation in a systematic way.

This experiment compares two such cases: uniform amplitude scaling and fixed phase rotation.

### Part A: Uniform Amplitude Scaling

Multiply every QPSK symbol by a positive real gain \( A \):

$$
r=As
$$

The flowgraph adds a complex **Multiply Const** block controlled by a QT GUI Range:

```text
ID: amp_gain
Default: 1.0
Start: 0.2
Stop: 2.0
Step: 0.1

Multiply Const
Constant: amp_gain
```

The Constellation Sink compares

```text
Ideal QPSK
Scaled QPSK
```

and is titled

```text
QPSK Amplitude Scaling
```

![QPSK constellation contracted by an amplitude gain of 0.5](../figures/ch17/ch17-exp6-qpsk-amplitude-scaling-0p5.png)

At \( A=0.5 \),

$$
(\pm1,\pm1)\rightarrow(\pm0.5,\pm0.5)
$$

so the entire constellation contracts toward the origin.

![QPSK constellation expanded by an amplitude gain of 1.5](../figures/ch17/ch17-exp6-qpsk-amplitude-scaling-1p5.png)

At \( A=1.5 \), the constellation expands outward.

The square does not rotate. Each point moves along the radial line connecting it to the origin.

With the ideal zero-threshold detector used here, a positive uniform gain does not change the signs of I or Q. The symbols therefore remain in the same QPSK decision regions. Uniform scaling changes the constellation size but does not, by itself, change these hard decisions.

This experiment applies the same gain to I and Q. Other amplitude distortions can change the constellation shape as well.

### Part B: Phase Rotation

Now multiply each complex symbol by a unit-magnitude phasor:

$$
r=se^{j\theta}
$$

The magnitude remains unchanged, but every point rotates through the same angle.

In GNU Radio, a complex Signal Source at zero frequency provides a stationary phasor. Its phase is controlled by a QT GUI Range:

```text
phase_deg
Default: 0
Start: -90
Stop: 90
Step: 5

Complex Signal Source
Frequency: 0
Amplitude: 1
Initial Phase: phase_deg * math.pi / 180
```

The clean QPSK stream is multiplied by this phasor, and the sink compares

```text
Ideal QPSK
Rotated QPSK
```

under the title

```text
QPSK Phase Rotation
```

![QPSK constellation rotated by 30 degrees](../figures/ch17/ch17-exp6-qpsk-phase-rotation-30deg.png)

At \( 30^\circ \), the entire constellation rotates around the origin. The points remain sharp rather than spreading into clouds, and their distance from the origin is unchanged.

This is visually quite different from Gaussian noise.

![QPSK constellation rotated by 45 degrees onto the original decision boundaries](../figures/ch17/ch17-exp6-qpsk-phase-rotation-45deg.png)

The original QPSK phases were

$$
45^\circ,\quad135^\circ,\quad225^\circ,\quad315^\circ
$$

Adding \( 45^\circ \) gives

$$
90^\circ,\quad180^\circ,\quad270^\circ,\quad360^\circ
$$

The rotated symbols therefore lie on the original I or Q axes. Those axes are also the decision boundaries of the detector we have been using.

A perfectly sharp constellation can therefore still produce unreliable decisions if its orientation is wrong relative to the receiver's reference.

Near this \( 45^\circ \) condition, even a small additional disturbance can move a sample to either side of a decision boundary.

### A Useful Visual Diagnosis

The three impairments now have distinct signatures:

| Impairment | Constellation appearance |
|---|---|
| Gaussian noise | Individual points spread into clouds |
| Uniform amplitude scaling | Whole constellation expands or contracts |
| Fixed phase rotation | Whole constellation rotates |

These patterns make constellation displays useful for diagnosing receiver problems.

### Try It Yourself

We can set the phase rotation slightly above \( 45^\circ \), for example \( 50^\circ \), and predict which neighboring decision region each point will enter.

Then we can return the phase rotation to zero and vary only the amplitude gain. The two impairments produce clearly different geometric changes even though both operate on the complex symbols.

## 17.9 From QPSK to M-PSK

BPSK and QPSK suggest a broader family of modulation schemes.

BPSK uses two allowed phases. QPSK uses four. More points can be placed around the same circle to create M-PSK.

A general ideal M-PSK constellation can be written as

$$
s_k=Ae^{j(2\pi k/M+\phi_0)},\qquad k=0,1,\ldots,M-1
$$

where \( A \) is the common magnitude and \( \phi_0 \) is an optional fixed phase offset that sets the orientation of the constellation.

Our QPSK construction, for example, corresponds to a \( 45^\circ \) offset.

For ideal M-PSK, all points have the same magnitude and differ only in phase.

The number of bits represented by each symbol is

$$
k=\log_2M
$$

for the power-of-two constellations considered here.

| Modulation | Number of points | Bits per symbol |
|---|---:|---:|
| BPSK | 2 | 1 |
| QPSK | 4 | 2 |
| 8-PSK | 8 | 3 |
| 16-PSK | 16 | 4 |

Increasing the number of points increases the number of bits carried by each symbol. For a fixed constellation radius, however, neighboring phase states also become closer together. The receiver therefore becomes more sensitive to noise and phase error.

We do not need a separate 8-PSK experiment here because BPSK and QPSK have already established the underlying geometry.

## 17.10 Experiment 17.7: Building 16-QAM from Two 4-PAM Axes

QPSK allowed both I and Q to take two values:

$$
I,Q\in\{-1,+1\}
$$

Now give each dimension four possible amplitudes.

Chapter 16 already introduced the required 4-PAM levels:

$$
-3,\quad-1,\quad+1,\quad+3
$$

Use the same levels on I and Q:

$$
I\in\{-3,-1,+1,+3\}
$$

$$
Q\in\{-3,-1,+1,+3\}
$$

There are now

$$
4\times4=16
$$

possible I/Q coordinate pairs.

This produces rectangular 16-QAM.

In other words, 16-QAM can be viewed as **4-PAM on I combined with 4-PAM on Q**.

### Visiting All 16 Points Deliberately

We again use controlled symbol-index sequences.

For I:

```text
[0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3]
```

For Q:

```text
[0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3]
```

Both branches use the mapping

```text
0 → -3
1 → -1
2 → +1
3 → +3
```

While I remains at one level, Q cycles through all four levels. I then moves to the next level and the sequence repeats.

![Experiment 17.7 flowgraph: constructing 16-QAM from two 4-PAM branches](../figures/ch17/ch17-exp7-16qam-from-4pam-flowgraph.png)

The important settings are:

```text
I Chunks to Symbols
Output Type: Float
Symbol Table: [-3, -1, 1, 3]

Q Chunks to Symbols
Output Type: Float
Symbol Table: [-3, -1, 1, 3]

Float to Complex
Real input: I 4-PAM levels
Imaginary input: Q 4-PAM levels
```

The Time Sink is titled

```text
16-QAM I and Q Components
```

with traces

```text
I Level
Q Level
```

and the Constellation Sink is titled

```text
16-QAM Constellation
```

with trace

```text
16-QAM Symbols
```

![Experiment 17.7 result: four I levels and four Q levels producing the 16-QAM constellation](../figures/ch17/ch17-exp7-16qam-constellation.png)

The upper plot shows four possible amplitudes on each dimension. The constellation below contains every possible I/Q pair.

The 16-QAM pattern is therefore not an arbitrary predefined arrangement. It follows directly from combining two 4-PAM dimensions.

### Four Bits per Symbol

Sixteen possible symbols require

$$
k=\log_2(16)=4
$$

bits per symbol.

One useful interpretation is that two bits select one of four I levels and another two bits select one of four Q levels. Together, those four bits select one of the 16 complex symbols.

### Why QAM Is Not Just "Amplitude Without Phase"

The 16-QAM points do not all have the same magnitude.

For example,

$$
|1+j|=\sqrt{2}
$$

while

$$
|3+3j|=3\sqrt{2}
$$

and

$$
|3+j|=\sqrt{10}
$$

Their phases also differ.

Rectangular QAM therefore uses I/Q amplitude combinations that generally produce both different overall magnitudes and different phases.

The name **Quadrature Amplitude Modulation** refers to controlling the amplitudes of two orthogonal carrier components. Once I and Q are combined, each complex symbol has both a magnitude and a phase.

## 17.11 Experiment 17.8: 16-QAM Decision Regions and Noise

The receiver must now distinguish among 16 possible symbols. The decision process follows directly from the 4-PAM detector developed in Chapter 16.

Each axis is a 4-PAM problem.

For the levels

$$
-3,\quad-1,\quad+1,\quad+3
$$

the midpoint thresholds are

$$
-2,\quad0,\quad+2
$$

We apply these thresholds independently to I and Q.

For I:

| Received I | Decided I |
|---|---:|
| \( I<-2 \) | -3 |
| \( -2<I<0 \) | -1 |
| \( 0<I<2 \) | +1 |
| \( I>2 \) | +3 |

The same four regions apply to Q. Exact samples on a threshold require a tie-breaking convention, but with continuous noise the probability of landing exactly on one of these boundaries is effectively zero.

Three vertical boundaries and three horizontal boundaries divide the I/Q plane into 16 decision regions.

A rectangular 16-QAM hard detector can therefore be viewed as one 4-PAM detector operating on I and another operating on Q.

### Adding Complex Gaussian Noise

We extend Experiment 17.7 by adding complex Gaussian noise before the Constellation Sink. The ideal points and noisy samples are displayed together with the six decision boundaries.

![16-QAM with Gaussian noise amplitude 0.2 and the decision regions](../figures/ch17/ch17-exp8-16qam-noise-0p2.png)

At a noise amplitude of 0.2, the 16 clusters remain compact and clearly separated.

A received point does not have to land exactly on its ideal symbol. It only has to remain in the correct decision region.

Suppose the receiver observes

$$
r=2.7+j0.8
$$

The I coordinate lies above \( +2 \), so the I detector chooses \( +3 \). The Q coordinate lies between \( 0 \) and \( +2 \), so the Q detector chooses \( +1 \).

The detected symbol is therefore

$$
\hat{s}=3+j
$$

![16-QAM with stronger Gaussian noise amplitude 0.6, showing samples entering neighboring decision regions](../figures/ch17/ch17-exp8-16qam-noise-0p6.png)

At a noise amplitude of 0.6, the clouds spread across some of the decision boundaries.

If \( 3+j \) was transmitted and the received I value falls below the \( +2 \) threshold, the I detector may choose \( +1 \) instead of \( +3 \). The symbol has then entered a neighboring decision region.

The same principle used for PAM still applies. Detection depends on which decision region contains the received point.

In 4-PAM we needed three thresholds on one axis. In rectangular 16-QAM, the same three thresholds are used on I and on Q, producing 16 two-dimensional decision regions.

## 17.12 Why Gray Coding Helps

Each 16-QAM point represents four bits, but the geometry alone does not determine which four-bit pattern belongs to each point. The symbol labels are a design choice.

Consider one 4-PAM axis. A straightforward binary assignment could be

| Amplitude | Binary label |
| --------: | :----------: |
|        -3 |      00      |
|        -1 |      01      |
|        +1 |      10      |
|        +3 |      11      |

The two middle neighboring levels are labeled `01` and `10`, so both bits change between them.

If noise causes a nearest-neighbor error across the threshold at zero, one incorrect amplitude decision could therefore produce two bit errors on that axis.

A Gray-coded assignment avoids this by arranging the labels so that adjacent levels differ by only one bit:

| Amplitude | Gray label |
| --------: | :--------: |
|        -3 |     00     |
|        -1 |     01     |
|        +1 |     11     |
|        +3 |     10     |

The sequence is therefore

```text
00 → 01 → 11 → 10
```

Every neighboring pair differs by one bit.

For rectangular 16-QAM, we can apply the same Gray-coded ordering independently to I and Q. Two bits select the I level and another two bits select the Q level.

If we write the I bits first and the Q bits second, one possible labeling is

| Q level / Q bits | I = -3 / 00 | I = -1 / 01 | I = +1 / 11 | I = +3 / 10 |
| ---------------- | :---------: | :---------: | :---------: | :---------: |
| +3 / 10          |    `0010`   |    `0110`   |    `1110`   |    `1010`   |
| +1 / 11          |    `0011`   |    `0111`   |    `1111`   |    `1011`   |
| -1 / 01          |    `0001`   |    `0101`   |    `1101`   |    `1001`   |
| -3 / 00          |    `0000`   |    `0100`   |    `1100`   |    `1000`   |

The first two bits identify the I level, while the last two bits identify the Q level.

The exact labeling convention can vary between systems. The important property is that neighboring constellation points differ by only one bit whenever possible.

For example, if the symbol labeled `1111` is mistaken for its horizontal neighbor `1011`, only one bit changes.

Gray coding does not reduce the noise, change the constellation geometry, or prevent symbol errors. Its benefit appears when a symbol error occurs: nearest-neighbor mistakes usually produce fewer bit errors.

A sufficiently large disturbance can still move a received point across several decision boundaries, so Gray coding does not guarantee one bit error for every incorrect symbol decision.


## 17.13 Constellation Size, Energy, and Normalization

The amplitudes in this chapter were chosen to make the constellation geometry easy to see.

Our QPSK construction used

$$
I,Q\in\{-1,+1\}
$$

so every symbol has

$$
|s|^2=I^2+Q^2=2
$$

in the arbitrary energy scale used by the experiment.

The 16-QAM construction used

$$
I,Q\in\{-3,-1,+1,+3\}
$$

so its symbols have several different energies. Its average symbol energy is also different from that of our unnormalized QPSK constellation.

That is acceptable for visualization.

When modulation schemes are compared quantitatively, however, their average transmitted power or average symbol energy should normally be normalized. Otherwise, an apparent performance difference may partly come from transmitting one constellation with more energy.

QPSK is commonly normalized using

$$
I,Q\in\left\{-\frac{1}{\sqrt{2}},+\frac{1}{\sqrt{2}}\right\}
$$

which gives each ideal symbol unit magnitude.

Normalization is not needed for the geometric ideas developed in this chapter, but it will matter when we begin making fair performance comparisons.

## 17.14 GNU Radio Toolbox

Several blocks take on important roles in the experiments in this chapter.

### Float to Complex

**Float to Complex** combines two real-valued streams into one complex stream.

If its real input is \( I[n] \) and its imaginary input is \( Q[n] \), the output is

$$
x[n]=I[n]+jQ[n]
$$

We first used it with \( Q=0 \) to place BPSK on the I axis. We then allowed both inputs to vary to construct QPSK and 16-QAM.

This block is useful here because it exposes the two coordinates directly instead of hiding them inside a modulation block.

### Complex Gaussian Noise Source

The Noise Source was configured for complex Gaussian noise so that both I and Q could be disturbed.

This turns ideal constellation points into clouds and allows us to observe decision-boundary crossings directly.

The settings used in this chapter were:

```text
Output Type: Complex
Noise Type: Gaussian
Amplitude: noise_amp
```

### Multiply Const

**Multiply Const** multiplies every input sample by a constant.

For the QPSK amplitude-scaling experiment, we used a positive real constant:

$$
r=As
$$

Changing \( A \) expanded or contracted the constellation without rotating it.

### Complex Signal Source as a Stationary Phasor

A complex Signal Source with zero frequency can provide a constant complex phasor.

With amplitude 1 and phase \( \theta \), its output is

$$
e^{j\theta}
$$

Multiplying the constellation by this phasor rotates every symbol by the same angle without changing its magnitude.

The zero-frequency setting is important. With a nonzero frequency, the phasor would rotate continuously with time. The constellation would then rotate continuously rather than remaining at a fixed phase offset.

### Higher-Level Constellation and Modulation Tools

GNU Radio also provides constellation objects and higher-level digital modulation tools that can perform symbol mapping more directly.

We deliberately avoided starting with them. By constructing BPSK, QPSK, and 16-QAM manually, we have exposed the essential operation: information selects a constellation point, and that point is represented by one complex I/Q symbol.

Higher-level tools make implementation more convenient, but the underlying constellation geometry remains the same.

## 17.15 Comparing BPSK, QPSK, and 16-QAM

The three main constellations developed in this chapter can now be compared directly.

| Modulation | I levels | Q levels | Constellation points | Bits/symbol | Ideal magnitude |
|---|---|---|---:|---:|---|
| BPSK | -1, +1 | 0 | 2 | 1 | Constant |
| QPSK | -1, +1 | -1, +1 | 4 | 2 | Constant |
| 16-QAM | -3, -1, +1, +3 | -3, -1, +1, +3 | 16 | 4 | Multiple values |

BPSK uses two points along one signal dimension.

QPSK uses both I and Q and produces four equal-magnitude points.

16-QAM increases the number of allowed amplitudes on both dimensions and forms a 4-by-4 grid.

More constellation points allow more bits to be represented by each symbol, but the receiver must distinguish among more closely spaced possibilities for a given power constraint. Noise, phase error, gain error, and other impairments therefore become increasingly important as constellations become denser.

## 17.16 What We Learned

In this chapter, we extended the one-dimensional PAM idea into the two-dimensional I/Q plane.

The main ideas are:

- A complex digital symbol is represented as \( s=I+jQ \).
- BPSK uses two complex-baseband points on one signal dimension.
- The BPSK values \( +1 \) and \( -1 \) correspond to carrier phases separated by \( 180^\circ \).
- Decision boundaries divide the I/Q plane into regions associated with valid symbols.
- Noise produces decision errors when received samples cross those boundaries.
- QPSK uses both I and Q and represents two bits with each symbol.
- I/Q coordinates and amplitude/phase are two descriptions of the same complex symbol.
- Uniform gain changes constellation size, while a fixed phase offset rotates the constellation.
- M-PSK extends the same constant-magnitude idea to more allowed phases.
- Rectangular 16-QAM can be constructed directly from 4-PAM on I and 4-PAM on Q.
- A rectangular 16-QAM detector can be viewed as two 4-PAM detectors operating independently on I and Q.
- Gray coding reduces the number of bit errors commonly produced by nearest-neighbor symbol mistakes.
- Normalization becomes important when comparing modulation schemes at equal power or symbol energy.

I/Q is therefore no longer just a mathematical way to represent a complex signal. We have now used its two dimensions directly to represent digital information.

## 17.17 Connecting to the Next Chapter

We now know where BPSK, QPSK, and 16-QAM symbols belong in the I/Q plane and how a receiver can divide that plane into decision regions.

So far, however, we have often represented each symbol with a rectangular pulse. The abrupt transitions were useful for visualization, but they also affect the signal spectrum and are not generally how we want to transmit symbols over a bandwidth-limited channel.

The next step is to control how one symbol transitions into the next while preserving the information carried by the constellation.

That leads to **Chapter 18: Pulse Shaping and Matched Filtering**.