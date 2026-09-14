# Chapter 4: Complex Numbers for SDR

## 4.1 Why Are We Talking About Complex Numbers?

At the end of the previous chapter, something important appeared in the Frequency Sink. When we generated a real cosine, GNU Radio showed one frequency component at a positive frequency and another at the corresponding negative frequency.

That leaves us with two closely related questions. What does negative frequency mean, and why do SDR systems so often work with **complex-valued samples** instead of ordinary real numbers?

To answer them, we first need a practical understanding of complex numbers.

A complex number is often written as

$$
z=a+jb
$$

and later described using magnitude and phase. Our goal is not to study this as an abstract mathematical topic. We will build a complex signal in GNU Radio, separate it into components, view it on the complex plane, measure its magnitude and phase, and deliberately change it to see what breaks.

By the end of the chapter, an expression such as

$$
e^{j\theta}
$$

should represent something concrete: a point, or equivalently a vector, rotating on the complex plane.

## 4.2 From Real Numbers to the Complex Plane

So far, most of our signals have been real-valued. A cosine, for example, can be written as

$$
x(t)=\cos(2\pi ft)
$$

At any instant it has one numerical value, perhaps `0.7`, `-0.3` or `1`. A real number can therefore be located on a one-dimensional number line.

A complex number contains two components:

$$
z=a+jb
$$

where $a$ is the **real component**, $b$ is the **imaginary component**, and

$$
j^2=-1
$$

Mathematics often uses $i$ instead of $j$. Electrical and communications engineering normally uses $j$ because $i$ is commonly used for electrical current.

The word *imaginary* can make the second component sound less physical than it is. For our purposes, it is more useful to think of a complex number as a convenient way to keep two related quantities together.

For example,

$$
z=3+j4
$$

can be viewed as the coordinate pair

$$
(3,4)
$$

The real component gives the horizontal coordinate and the imaginary component gives the vertical coordinate. This produces the **complex plane**.

![A complex number represented on the complex plane.](../figures/ch04/complex-plane-concept.png)

Instead of drawing only the point, we can draw a vector from the origin to it. The same complex number can then be described in two useful ways: by its horizontal and vertical components, or by the vector's length and direction.

Both descriptions will be useful throughout SDR.

## 4.3 Magnitude and Phase

For

$$
z=a+jb
$$

the real component, imaginary component and the vector form a right triangle. Its length is therefore

$$
|z|=\sqrt{a^2+b^2}
$$

This is the **magnitude** of the complex number.

For example, if

$$
z=3+j4
$$

then

$$
|z|=\sqrt{3^2+4^2}=5
$$

Geometrically, the magnitude tells us how far the point is from the origin.

The vector also has a direction. We describe that direction using an angle $\theta$, measured from the positive real axis. A convenient expression for the phase is

$$
\theta=\operatorname{atan2}(b,a)
$$

Using `atan2` rather than an ordinary one-argument arctangent allows the signs of both components to determine the correct quadrant.

We can therefore describe the same complex number either in component form,

$$
z=a+jb
$$

or in magnitude-phase form,

$$
z=|z|\angle\theta
$$

The first description gives coordinates. The second gives length and direction. The complex number itself has not changed.

## 4.4 Euler's Formula and the Rotating-Vector View

From the geometry of the complex plane,

$$
a=|z|\cos\theta
$$

and

$$
b=|z|\sin\theta
$$

Substituting these into $z=a+jb$ gives

$$
z=|z|\cos\theta+j|z|\sin\theta
$$

or

$$
z=|z|(\cos\theta+j\sin\theta)
$$

Euler's formula tells us that

$$
e^{j\theta}=\cos\theta+j\sin\theta
$$

so a complex number can also be written as

$$
z=|z|e^{j\theta}
$$

When the magnitude is 1,

$$
z=e^{j\theta}=\cos\theta+j\sin\theta
$$

Now let $\theta$ increase. At $\theta=0$, the point is $(1,0)$. At $\theta=\pi/2$, it is $(0,1)$. At $\theta=\pi$, it is $(-1,0)$. At $\theta=3\pi/2$, it is $(0,-1)$.

As the angle continues to increase, the point moves around the unit circle.

That gives us a useful physical interpretation:

> A unit-magnitude complex exponential can be visualised as a vector rotating around the complex plane.

We do not need a proof of Euler's formula here. What matters is learning to connect the equation with something we can observe.

## 4.5 GNU Radio Blocks for Complex Signals

This chapter introduces several blocks for moving between real-valued and complex data.

| GNU Radio block | Role in this chapter |
|---|---|
| **Float to Complex** | Combines real-valued streams into a complex stream |
| **Complex to Real** | Extracts the real component |
| **Complex to Imag** | Extracts the imaginary component |
| **Complex to Mag** | Calculates complex magnitude |
| **Complex to Arg** | Calculates complex phase |
| **QT GUI Constellation Sink** | Displays complex samples on the I-Q plane |

A `Float to Complex` block can take real-valued inputs and form complex samples of the form

$$
z[n]=a[n]+jb[n]
$$

Its output is a complex stream. Blocks such as `Complex to Real`, `Complex to Imag`, `Complex to Mag` and `Complex to Arg` then convert information from that complex stream back into float streams. GNU Radio uses different port colours to help us recognise these data types.

We saw in Chapter 1 that incompatible port types cannot simply be connected. That distinction becomes increasingly important now that complex streams are part of our flowgraphs.

## 4.6 Experiment 1: Build a Complex Signal

We will begin with two real-valued Signal Sources.

Configure the first as:

```text
Waveform: Cosine
Frequency: 1 kHz
Amplitude: 1
```

Configure the second as:

```text
Waveform: Sine
Frequency: 1 kHz
Amplitude: 1
```

Use

$$
f_s=32\text{ kS/s}
$$

for the sample rate.

Connect the cosine to the real input of `Float to Complex` and the sine to the imaginary input. The resulting complex signal is

$$
z(t)=\cos(2\pi ft)+j\sin(2\pi ft)
$$

Then connect the complex stream to `Complex to Real` and `Complex to Imag`, and display both outputs with a QT GUI Time Sink.

![GNU Radio flowgraph for building and separating a complex signal.](../figures/ch04/complex-components-flowgraph.png)

Run the flowgraph.

![Real and imaginary components of the complex signal.](../figures/ch04/complex-components-time.png)

The real component is

$$
\operatorname{Re}\{z(t)\}=\cos(2\pi ft)
$$

and the imaginary component is

$$
\operatorname{Im}\{z(t)\}=\sin(2\pi ft)
$$

Combining the two streams has not destroyed either waveform. Both values are carried together inside each complex sample.

This is the first important practical idea of the chapter: a complex stream carries two related numerical components at every sample instant.

## 4.7 Experiment 2: View the Signal on the Complex Plane

We have built

$$
z(t)=\cos(2\pi ft)+j\sin(2\pi ft)
$$

Now we can ask what those samples look like on the complex plane.

Extend the same flowgraph by connecting a **QT GUI Constellation Sink** directly to the output of `Float to Complex`.

![Flowgraph with the Constellation Sink added.](../figures/ch04/complex-plane-flowgraph.png)

The Constellation Sink plots the real component horizontally and the imaginary component vertically. GNU Radio labels these axes **In-phase** and **Quadrature**. For this chapter, we can treat them simply as the real and imaginary axes. We will explain the radio meaning of I and Q in the next chapter.

Run the flowgraph.

![Real and imaginary waveforms together with their complex-plane representation.](../figures/ch04/complex-plane.png)

The samples form a circle. We can see why directly from the two components:

$$
a=\cos\theta
$$

$$
b=\sin\theta
$$

Therefore,

$$
a^2+b^2=\cos^2\theta+\sin^2\theta=1
$$

Every sample is one unit from the origin, so the trajectory is a unit circle.

The two sinusoids in the Time Sink and the circle in the Constellation Sink are not different signals. They are different views of the same complex samples.

## 4.8 Experiment 3: Measure Magnitude and Phase

Extend the same flowgraph again by adding:

- `Complex to Mag`
- `Complex to Arg`

Connect both blocks directly to the complex output and display their outputs with another QT GUI Time Sink.

![Flowgraph extended to calculate magnitude and phase.](../figures/ch04/complex-magnitude-phase-flowgraph.png)

For each sample

$$
z=a+jb
$$

`Complex to Mag` calculates

$$
|z|=\sqrt{a^2+b^2}
$$

while `Complex to Arg` reports the phase angle in radians.

![Magnitude, phase, real and imaginary components, and constellation.](../figures/ch04/complex-magnitude-phase.png)

This gives us three views of the same signal.

The real and imaginary components are still

$$
\operatorname{Re}\{z(t)\}=\cos(2\pi ft)
$$

and

$$
\operatorname{Im}\{z(t)\}=\sin(2\pi ft)
$$

The complex-plane trajectory is still a unit circle, and the magnitude remains

$$
|z|=1
$$

because

$$
|z|=\sqrt{\cos^2\theta+\sin^2\theta}=1
$$

The phase, however, changes continuously as the vector rotates.

### Why Does the Phase Look Like a Sawtooth?

The phase trace increases until it reaches approximately $+\pi$, then jumps to around $-\pi$ and begins increasing again.

The vector itself has not jumped backwards. `Complex to Arg` reports a principal phase angle over a wrapped interval around $-\pi$ to $+\pi$. Once the rotating vector passes the positive boundary, the displayed angle wraps to the corresponding negative value.

This is **phase wrapping**.

For a 1 kHz signal,

$$
T=\frac{1}{1000}=1\text{ ms}
$$

so the phase completes one full cycle every 1 ms. The waveform period, the phase evolution and the rotating-vector interpretation all describe the same behaviour.

## 4.9 Break It: Make the Imaginary Component Smaller

The unit circle came from a very specific relationship: equal-amplitude cosine and sine components at the same frequency, separated by 90 degrees.

Keep the cosine amplitude at 1, but reduce the sine amplitude from 1 to 0.5. The complex signal becomes

$$
z(t)=\cos(2\pi ft)+j0.5\sin(2\pi ft)
$$

Run the flowgraph again.

![Complex signal with a reduced imaginary-component amplitude.](../figures/ch04/complex-ellipse.png)

The real component still ranges from approximately -1 to +1, while the imaginary component ranges from approximately -0.5 to +0.5.

The circle has become an ellipse. With

$$
a=\cos\theta
$$

and

$$
b=0.5\sin\theta
$$

the components satisfy

$$
a^2+\frac{b^2}{(0.5)^2}=1
$$

The magnitude is no longer constant either:

$$
|z|=\sqrt{\cos^2\theta+0.25\sin^2\theta}
$$

It varies between approximately 0.5 and 1.

The circle therefore did not appear merely because the stream was complex. It appeared because the two components had the equal-amplitude quadrature relationship required for constant magnitude.

## 4.10 Break It Again: Remove the Imaginary Component

Now set the sine amplitude to 0. The signal becomes

$$
z(t)=\cos(2\pi ft)+j0
$$

Run the flowgraph.

![Complex signal with zero imaginary component.](../figures/ch04/complex-real-only.png)

Every sample now has the form

$$
(a,0)
$$

so the complex-plane trajectory collapses onto the real axis. We have returned to a purely real signal.

The magnitude is now

$$
|z|=\sqrt{\cos^2(2\pi ft)}=|\cos(2\pi ft)|
$$

which explains why the magnitude resembles a rectified cosine. Magnitude cannot be negative, even when the original real-valued sample is negative.

The phase also has a simple geometric interpretation. When the cosine is positive, the point lies on the positive real axis and the phase is 0. When the cosine is negative, the point lies on the negative real axis and the phase is $\pi$, or equivalently $-\pi$ at the wrapped boundary.

The complex-plane view makes these otherwise unusual-looking magnitude and phase traces straightforward to interpret.

## 4.11 Reverse the Imaginary Component

Restore the sine amplitude to 1, then reverse its sign:

```text
Sine amplitude: -1
```

The complex signal is now

$$
z(t)=\cos(2\pi ft)-j\sin(2\pi ft)
$$

Using Euler's formula,

$$
z(t)=e^{-j2\pi ft}
$$

Compare this with the original signal,

$$
z(t)=\cos(2\pi ft)+j\sin(2\pi ft)=e^{j2\pi ft}
$$

Only the sign of the imaginary component has changed.

![Complex signal after reversing the imaginary component.](../figures/ch04/complex-negative-rotation.png)

The magnitude is still

$$
|z|=1
$$

and the constellation still forms a circle. A static constellation image therefore does not tell us which direction the samples travel around that circle.

The phase trace does. For $e^{j2\pi ft}$, phase increases with time. For $e^{-j2\pi ft}$, phase decreases with time.

That difference leads directly to positive and negative complex frequency.

## 4.12 Positive and Negative Complex Frequency

For

$$
z(t)=e^{j2\pi ft}
$$

the phase is

$$
\theta(t)=2\pi ft
$$

and increases with time. For

$$
z(t)=e^{-j2\pi ft}
$$

the phase is

$$
\theta(t)=-2\pi ft
$$

and decreases with time.

On the usual complex-plane convention, these two signals rotate in opposite directions.

This gives negative frequency a practical interpretation:

> The magnitude of a complex frequency tells us how fast the phase rotates. Its sign distinguishes the direction of rotation.

For example,

$$
e^{j2\pi(1000)t}
$$

and

$$
e^{-j2\pi(1000)t}
$$

both rotate at a rate corresponding to 1 kHz, but in opposite directions.

Negative frequency does not mean a negative number of cycles somehow occurs. It describes the opposite direction of complex phase evolution.

### Seeing the Sign in the Frequency Sink

Add a QT GUI Frequency Sink directly to the complex output of `Float to Complex`.

Use:

```text
FFT Size: 1024
Center Frequency: 0
Bandwidth: samp_rate
```

![GNU Radio flowgraph for observing positive and negative complex frequencies.](../figures/ch04/positive-negative-frequency-flowgraph.png)

Run the experiment first with:

```text
Cosine amplitude: 1
Sine amplitude: 1
Frequency: 1 kHz
Sample rate: 32 kS/s
```

The signal is

$$
z(t)=e^{j2\pi(1000)t}
$$

![Positive complex frequency in GNU Radio.](../figures/ch04/complex-positive-frequency.png)

The phase increases with time and the Frequency Sink shows the spectral peak at approximately

$$
+1\text{ kHz}
$$

Now change only the sine amplitude from `+1` to `-1`. The signal becomes

$$
z(t)=e^{-j2\pi(1000)t}
$$

![Negative complex frequency in GNU Radio.](../figures/ch04/complex-negative-frequency.png)

The magnitude remains 1 and the real component is unchanged, but the imaginary component is inverted. The phase now decreases with time, and the spectral peak moves to approximately

$$
-1\text{ kHz}
$$

The same distinction is therefore visible in both phase evolution and the frequency-domain display:

| Complex signal | Phase evolution | Spectral peak |
|---|---|---:|
| $e^{j2\pi ft}$ | Increasing | $+f$ |
| $e^{-j2\pi ft}$ | Decreasing | $-f$ |

## 4.13 Why Does a Real Cosine Have Two Frequency Components?

We can now return to the observation that started this chapter. In Chapter 3, a real cosine produced symmetric spectral components at $+f$ and $-f$.

Euler's formula gives

$$
e^{j\theta}=\cos\theta+j\sin\theta
$$

and

$$
e^{-j\theta}=\cos\theta-j\sin\theta
$$

Adding the two expressions gives

$$
e^{j\theta}+e^{-j\theta}=2\cos\theta
$$

so

$$
\cos\theta=\frac{1}{2}e^{j\theta}+\frac{1}{2}e^{-j\theta}
$$

Replacing $\theta$ with $2\pi ft$ gives

$$
\cos(2\pi ft)=\frac{1}{2}e^{j2\pi ft}+\frac{1}{2}e^{-j2\pi ft}
$$

This is why the spectrum of a real cosine is symmetric. Its mathematical representation contains equal positive- and negative-frequency complex exponentials.

A real 1 kHz cosine therefore has spectral components at $+1$ kHz and $-1$ kHz. These are not two independent physical tones being transmitted. They are the positive- and negative-frequency components required by the complex-exponential representation of a real sinusoid.

Compare the three cases:

| Signal | Ideal frequency components |
|---|---|
| $\cos(2\pi ft)$ | $-f$ and $+f$ |
| $\cos(2\pi ft)+j\sin(2\pi ft)$ | $+f$ |
| $\cos(2\pi ft)-j\sin(2\pi ft)$ | $-f$ |

A complex signal can therefore preserve the distinction between positive and negative frequency, while a real cosine contains the conjugate pair together.

This is one of the reasons complex samples are so useful in SDR, and it prepares us for the I and Q representation used by practical radios.

## 4.14 GNU Radio Toolbox

This chapter introduced several blocks that will appear repeatedly later in the book.

### Float to Complex

`Float to Complex` combines real-valued input streams into complex samples. In our experiment, the cosine became the real component and the sine became the imaginary component.

### Complex to Real and Complex to Imag

These blocks extract the two Cartesian components of a complex stream and output float streams.

### Complex to Mag and Complex to Arg

`Complex to Mag` returns the non-negative magnitude of each complex sample. `Complex to Arg` returns its wrapped phase angle in radians.

### QT GUI Constellation Sink

The Constellation Sink plots streaming complex samples on an I-Q plane. In this chapter we used it as a direct picture of the real and imaginary components of each sample.

### Watch the Data Types

A complex sample carries two floating-point components, while a float sample carries one real value. When a GNU Radio connection does not work, the first things to check are the source block's output type, the destination block's input type and the port colours.

## 4.15 Explore Further

The same flowgraph gives us several useful experiments to try before moving on.

1. Set the imaginary amplitude to `2`. Predict the shape of the constellation and whether the magnitude will remain constant.

2. Swap the inputs so that the sine feeds the real input and the cosine feeds the imaginary input. Predict how the phase evolution and rotation direction will change.

3. Change both Signal Sources from 1 kHz to 2 kHz. Predict whether the constellation radius will change, whether the phase will evolve faster or slower, and where the Frequency Sink peak should appear.

4. Switch the imaginary amplitude between `+1` and `-1`. Before each run, predict whether the phase should increase or decrease and whether the Frequency Sink should show $+f$ or $-f$.

5. Keep the real component at 1 kHz and change the imaginary component to a different frequency. Predict whether the complex-plane trajectory can still be a circle, then compare the result with the prediction.

As before, the useful habit is to change one thing at a time and predict the result before running the flowgraph.

## 4.16 What We Learned

A complex sample contains two components:

$$
z=a+jb
$$

The same sample can also be described by its magnitude and phase. Magnitude gives its distance from the origin, while phase gives its direction on the complex plane.

Euler's formula connects these two descriptions:

$$
e^{j\theta}=\cos\theta+j\sin\theta
$$

When $\theta$ changes with time, the complex number can be visualised as a rotating vector.

Our first GNU Radio complex signal,

$$
z(t)=\cos(2\pi ft)+j\sin(2\pi ft)
$$

had constant unit magnitude and traced a circle. Reducing the imaginary amplitude changed that circle into an ellipse. Removing the imaginary component collapsed the trajectory onto the real axis. Reversing the imaginary component left the circular trajectory and magnitude unchanged but reversed the direction of phase evolution.

That last experiment gave us a practical interpretation of frequency sign:

$$
e^{j2\pi ft}\rightarrow +f
$$

while

$$
e^{-j2\pi ft}\rightarrow -f
$$

Finally, we used Euler's formula to explain why a real cosine has symmetric positive- and negative-frequency components:

$$
\cos(2\pi ft)=\frac{1}{2}e^{j2\pi ft}+\frac{1}{2}e^{-j2\pi ft}
$$

Complex samples let us keep those two directions of phase rotation distinct. That ability is central to SDR.

## 4.17 Connecting to the Next Chapter

There is one detail we have deliberately postponed.

The GNU Radio Constellation Sink does not label its axes *Real* and *Imaginary*. It calls them **In-phase** and **Quadrature**.

Why do SDR systems use the names I and Q? Why are the two components associated with signals 90 degrees apart, and why does a receiver benefit from keeping both?

The real and imaginary components we have been using are about to take on their radio names:

$$
x[n]=I[n]+jQ[n]
$$

In the next chapter, we will connect this complex-number view to practical I/Q signals and see why they are fundamental to software-defined radio.