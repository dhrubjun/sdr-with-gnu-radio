# Chapter 4: Complex Numbers for SDR

## 4.1 Why Are We Talking About Complex Numbers?

At the end of the previous chapter, something interesting appeared in the Frequency Sink.

When we generated a real cosine signal, GNU Radio showed two frequency components: one at a positive frequency and another at the corresponding negative frequency.

That left us with several questions.

What is a negative frequency?

Why would frequency need a sign?

And why do SDR systems so often work with **complex-valued samples** instead of ordinary real numbers?

Before we can answer those questions properly, we need to understand complex numbers.

If you have seen complex numbers before, you may remember expressions such as

$$z=a+jb$$

and perhaps equations involving magnitude and phase.

But our goal here is not to study complex numbers as an abstract mathematical topic.

Instead, we are going to **build one in GNU Radio, take it apart, look at it from several different directions, and even deliberately break it**.

By the end of the chapter, expressions such as

$$e^{j\theta}$$

should no longer look mysterious. They will represent something we can actually visualize.

---

## 4.2 From Real Numbers to Complex Numbers

So far, almost every signal we have generated has been real-valued.

For example, a cosine signal can be written as

$$x(t)=\cos(2\pi ft)$$

At any particular instant, the signal has one numerical value.

It might be

$$0.7$$

or

$$-0.3$$

or

$$1$$

A real number therefore needs only one number to describe it.

We can imagine placing it somewhere along a number line.

Complex numbers extend this idea.

Instead of using one number, we use **two related numbers together**:

$$z=a+jb$$

Here:

- \(a\) is the **real component**
- \(b\) is the **imaginary component**
- \(j\) is defined by

$$j^2=-1$$

You may have seen the symbol \(i\) used instead of \(j\) in mathematics.

In electrical and communications engineering, \(j\) is normally used because \(i\) is commonly used to represent electrical current.

---

## 4.3 Do Not Let the Word "Imaginary" Mislead You

The name *imaginary* can make complex numbers sound less physical than they really are.

For our purposes, a better first intuition is simply this:

> A complex number gives us a convenient way to keep two related quantities together.

Consider

$$z=3+j4$$

Instead of thinking of this as some strange imaginary object, think of it as containing two coordinates:

$$ (3,4) $$

The first tells us how far to move horizontally.

The second tells us how far to move vertically.

That immediately gives us another way to visualize a complex number.

---

## 4.4 The Complex Plane

A real number can be placed on a line.

A complex number can be placed on a **plane**.

The horizontal axis represents the real component, while the vertical axis represents the imaginary component.

For

$$z=a+jb$$

we therefore place the point at

$$(a,b)$$

![A complex number represented on the complex plane](../figures/ch04/complex-plane-concept.png)

**Figure 4.1: A complex number represented by its real component, imaginary component, magnitude, and phase.**

Instead of drawing only a point, we can draw a vector from the origin to that point.

Now something useful happens.

The same complex number can be described in two different ways.

We can describe it using:

- its horizontal and vertical components,

or using:

- the length and direction of the vector.

Those two descriptions will become extremely important in SDR.

---

## 4.5 Magnitude

Suppose

$$z=a+jb$$

From the complex-plane diagram, the real component \(a\), imaginary component \(b\), and the vector itself form a right triangle.

Using the Pythagorean theorem,

$$|z|=\sqrt{a^2+b^2}$$

This is the **magnitude** of the complex number.

For example, if

$$z=3+j4$$

then

$$|z|=\sqrt{3^2+4^2}=5$$

Geometrically, magnitude tells us how far the point is from the origin.

---

## 4.6 Phase

The vector also has a direction.

We describe that direction using an angle \(\theta\), measured from the positive real axis.

The phase is

$$\theta=\mathrm{atan2}(b,a)$$

The `atan2` form is useful because it considers the signs of both components and therefore identifies the correct quadrant.

So we now have two ways to describe exactly the same complex number.

### Component form

$$z=a+jb$$

### Magnitude-phase form

$$z=|z|\angle\theta$$

This is an important idea:

> **Real and imaginary components tell us the coordinates of a complex number. Magnitude and phase tell us its length and direction.**

Nothing about the complex number has changed. We have simply changed the way we describe it.

---

## 4.7 From Geometry to Euler's Formula

Look again at the complex-plane triangle.

From basic trigonometry,

$$a=|z|\cos\theta$$

and

$$b=|z|\sin\theta$$

Since

$$z=a+jb$$

we can substitute these expressions:

$$z=|z|\cos\theta+j|z|\sin\theta$$

Factor out the magnitude:

$$z=|z|(\cos\theta+j\sin\theta)$$

Now we meet one of the most important equations in signal processing:

$$e^{j\theta}=\cos\theta+j\sin\theta$$

This is **Euler's formula**.

Therefore,

$$z=|z|e^{j\theta}$$

If the magnitude is 1, the expression becomes especially simple:

$$z=e^{j\theta}$$

We do not need to prove Euler's formula here.

What matters for SDR is understanding what it represents.

---

## 4.8 A Complex Exponential Is a Rotating Vector

Consider

$$z=e^{j\theta}$$

Using Euler's formula,

$$z=\cos\theta+j\sin\theta$$

Now imagine increasing \(\theta\).

At

$$\theta=0$$

we have

$$z=1+j0$$

The point is at

$$(1,0)$$

At

$$\theta=\frac{\pi}{2}$$

we have

$$z=0+j1$$

At

$$\theta=\pi$$

we have

$$z=-1+j0$$

And at

$$\theta=\frac{3\pi}{2}$$

we have

$$z=0-j1$$

As the angle continues changing, the point moves around the unit circle.

So instead of thinking of

$$e^{j\theta}$$

as a complicated mathematical expression, we can think of it as:

> **a vector rotating around the complex plane.**

Now let's actually build one.

---

## 4.9 GNU Radio Toolbox: Working with Complex Signals

Until now, most of our GNU Radio flowgraphs have used real-valued signals.

This chapter introduces several blocks that allow us to work with complex data.

| GNU Radio block | What it does |
|---|---|
| **Signal Source** | Generates the real-valued sine and cosine signals |
| **Float to Complex** | Combines two float streams into one complex stream |
| **Complex to Real** | Extracts the real component |
| **Complex to Imag** | Extracts the imaginary component |
| **QT GUI Time Sink** | Displays signals against time |

We will introduce more tools only when we need them.

### Watch the Port Colours

Look carefully at the ports in the flowgraph.

GNU Radio uses different port colours to help distinguish different data types.

This matters because a **float stream** and a **complex stream** are not the same thing.

For example, `Float to Complex` accepts two float streams:

$$a[n]$$

and

$$b[n]$$

and creates

$$z[n]=a[n]+jb[n]$$

Its output is therefore a complex stream.

As our flowgraphs become larger, paying attention to data types becomes increasingly important.

---

## 4.10 Experiment 1: Building a Complex Signal

Let's build our first complex signal.

Create two Signal Sources.

For the first source use:

- Waveform: Cosine
- Frequency: 1 kHz
- Amplitude: 1

For the second source use:

- Waveform: Sine
- Frequency: 1 kHz
- Amplitude: 1

Use a sample rate of:

$$f_s=32\text{ kS/s}$$

Connect the cosine to the **real** input of `Float to Complex`.

Connect the sine to the **imaginary** input.

The resulting signal is

$$z(t)=\cos(2\pi ft)+j\sin(2\pi ft)$$

Then connect the complex output to:

- `Complex to Real`
- `Complex to Imag`

and display both outputs using a QT GUI Time Sink.

![GNU Radio flowgraph for building and separating a complex signal](../figures/ch04/complex-components-flowgraph.png)

**Figure 4.2: Building a complex signal from two float streams and separating it back into its real and imaginary components.**

Run the flowgraph.

![Real and imaginary components of the complex signal](../figures/ch04/complex-components-time.png)

**Figure 4.3: Real and imaginary components recovered from the complex signal.**

The blue waveform is the real component:

$$\mathrm{Re}\{z(t)\}=\cos(2\pi ft)$$

while the red waveform is the imaginary component:

$$\mathrm{Im}\{z(t)\}=\sin(2\pi ft)$$

Notice that combining the two signals did not destroy either of them.

Both pieces of information are contained inside one complex stream.

That is the first important idea of this chapter.

---

## 4.11 Experiment 2: What Does the Complex Signal Look Like?

We have created

$$z(t)=\cos(2\pi ft)+j\sin(2\pi ft)$$

But what does that signal look like on the complex plane?

Instead of building another flowgraph, let's extend the one we already have.

Add one new block:

**QT GUI Constellation Sink**

Connect it directly to the complex output of `Float to Complex`.

![Flowgraph with the Constellation Sink added](../figures/ch04/complex-plane-flowgraph.png)

**Figure 4.4: Extending the previous flowgraph with a QT GUI Constellation Sink.**

This is exactly how we will continue using GNU Radio throughout the book: **start simple, understand the result, and then add one new idea at a time.**

---

## 4.12 GNU Radio Toolbox: QT GUI Constellation Sink

The QT GUI Constellation Sink displays complex samples on a two-dimensional plane.

For a complex sample

$$z=a+jb$$

the horizontal coordinate comes from \(a\), while the vertical coordinate comes from \(b\).

GNU Radio labels these axes **In-phase** and **Quadrature**.

You may already be wondering why.

For now, think of them simply as the real and imaginary axes.

We will return to the names **In-phase** and **Quadrature** in the next chapter.

Run the flowgraph.

![Real and imaginary waveforms together with their complex-plane representation](../figures/ch04/complex-plane.png)

**Figure 4.5: The real and imaginary components in time and the corresponding samples on the complex plane.**

Something interesting appears.

The samples form a circle.

Why?

We have

$$a=\cos\theta$$

and

$$b=\sin\theta$$

Therefore,

$$a^2+b^2=\cos^2\theta+\sin^2\theta=1$$

So every point is exactly one unit away from the origin.

That is why GNU Radio shows a **unit circle**.

The two sinusoidal waveforms and the circle are not separate signals.

They are different ways of looking at the **same complex signal**.

---

## 4.13 Experiment 3: Magnitude and Phase

We can now extend the same flowgraph again.

This time add:

- `Complex to Mag`
- `Complex to Arg`

Connect both directly to the output of `Float to Complex`.

Display their outputs using another QT GUI Time Sink.

![Flowgraph extended to calculate magnitude and phase](../figures/ch04/complex-magnitude-phase-flowgraph.png)

**Figure 4.6: The complex-signal flowgraph extended with magnitude and phase measurements.**

---

## 4.14 GNU Radio Toolbox: Complex to Mag and Complex to Arg

### Complex to Mag

For each complex sample

$$z=a+jb$$

`Complex to Mag` calculates

$$|z|=\sqrt{a^2+b^2}$$

### Complex to Arg

`Complex to Arg` calculates the phase:

$$\theta=\mathrm{atan2}(b,a)$$

Its output is expressed in **radians**.

Now run the flowgraph.

![Magnitude, phase, real and imaginary components, and constellation](../figures/ch04/complex-magnitude-phase.png)

**Figure 4.7: Three different views of the same complex signal: magnitude and phase, real and imaginary components, and the complex plane.**

This figure brings almost everything we have learned together.

---

## 4.15 One Signal, Three Views

Look first at the middle plot.

We still have:

$$\mathrm{Re}\{z(t)\}=\cos(2\pi ft)$$

and

$$\mathrm{Im}\{z(t)\}=\sin(2\pi ft)$$

Now look at the constellation.

The samples form a unit circle.

Finally, look at the magnitude.

It remains at:

$$|z|=1$$

That is exactly what we predicted:

$$|z|=\sqrt{\cos^2\theta+\sin^2\theta}=1$$

Meanwhile, the phase continuously changes.

These are not three different signals.

> **They are three different views of the same complex signal.**

We can describe the signal using real and imaginary components:

$$(a,b)$$

or using magnitude and phase:

$$(|z|,\theta)$$

---

## 4.16 Why Does the Phase Look Like a Sawtooth?

The phase plot contains something that may initially look strange.

The phase increases until it reaches approximately

$$+\pi$$

then suddenly jumps to

$$-\pi$$

It then starts increasing again.

Did the complex vector suddenly jump backwards?

No.

The vector continues rotating smoothly.

The `Complex to Arg` block reports phase within a principal interval around

$$-\pi \leq \theta \leq \pi$$

So once the angle passes the positive boundary, its displayed representation wraps around to the negative boundary.

This is called **phase wrapping**.

For our 1 kHz signal,

$$T=\frac{1}{1000}=1\text{ ms}$$

Look at the phase plot again.

One complete phase cycle occurs every approximately 1 ms.

The time-domain waveform, the phase plot, and the rotating-vector interpretation all agree.

---

## 4.17 Now Let's Break the Flowgraph

So far everything has been carefully arranged:

- cosine amplitude = 1
- sine amplitude = 1
- same frequency
- correct relationship between the components

That produced a beautiful unit circle.

But is a circle something that every complex signal produces?

Let's find out.

Instead of adding more blocks, we will deliberately change the signal we already built.

---

## 4.18 Break It 1: Make the Imaginary Component Smaller

Keep the cosine amplitude at 1.

Change the sine amplitude from

$$1$$

to

$$0.5$$

Our complex signal becomes

$$z(t)=\cos(2\pi ft)+j0.5\sin(2\pi ft)$$

Run the flowgraph again.

![Complex signal with a reduced imaginary-component amplitude](../figures/ch04/complex-ellipse.png)

**Figure 4.8: Reducing the imaginary component from 1 to 0.5 changes the unit circle into an ellipse.**

The middle plot immediately shows what changed.

The real component still varies between approximately

$$-1\text{ and }+1$$

but the imaginary component varies only between

$$-0.5\text{ and }+0.5$$

Now look at the constellation.

The circle has become an **ellipse**.

We have

$$a=\cos\theta$$

and

$$b=0.5\sin\theta$$

Therefore,

$$a^2+\frac{b^2}{(0.5)^2}=1$$

which is the equation of an ellipse.

There is another important change.

The magnitude is no longer constant.

Now,

$$|z|=\sqrt{\cos^2\theta+0.25\sin^2\theta}$$

Depending on the angle, the magnitude varies between approximately 0.5 and 1.

So we have discovered something important:

> The circle was not produced simply because the signal was complex. It appeared because the real and imaginary components had the particular amplitudes and relationship required for constant magnitude.

---

## 4.19 Break It 2: Remove the Imaginary Component

Now let's go further.

Change the sine amplitude to:

$$0$$

Our signal becomes

$$z(t)=\cos(2\pi ft)+j0$$

Run the flowgraph.

![Complex signal with zero imaginary component](../figures/ch04/complex-real-only.png)

**Figure 4.9: Removing the imaginary component collapses the complex-plane trajectory onto the real axis.**

The imaginary waveform has disappeared.

Every sample now has the form

$$(a,0)$$

There is no vertical component.

So the constellation collapses onto the horizontal axis.

In other words, we have returned to a purely real signal.

This connects directly back to the signals we used in Chapter 3.

---

## 4.20 What Happened to the Magnitude?

The result at the top is also interesting.

Since

$$z(t)=\cos(2\pi ft)+j0$$

the magnitude is

$$|z|=\sqrt{\cos^2(2\pi ft)}$$

and therefore

$$|z|=|\cos(2\pi ft)|$$

That is why the magnitude looks like a rectified cosine.

Notice something important:

> **Magnitude is never negative.**

The original real waveform can have negative values.

Magnitude cannot.

---

## 4.21 Why Is the Phase Now Either 0 or \(\pi\)?

Look at the phase trace.

When the cosine is positive, the complex point lies on the positive real axis.

Its phase is

$$0$$

When the cosine is negative, the point lies on the negative real axis.

Its phase is

$$\pi$$

or equivalently \(-\pi\), depending on the representation used at the boundary.

So even this strange-looking phase plot has a simple geometric explanation.

The complex plane is helping us understand what GNU Radio is displaying.

---

## 4.22 Break It 3: Reverse the Imaginary Component

Restore the magnitude of the sine component, but this time set its amplitude to:

$$-1$$

Now the complex signal becomes

$$z(t)=\cos(2\pi ft)-j\sin(2\pi ft)$$

Using Euler's formula,

$$z(t)=e^{-j2\pi ft}$$

Compare that with our original signal:

$$z(t)=e^{+j2\pi ft}$$

Run the flowgraph.

![Complex signal after reversing the imaginary component](../figures/ch04/complex-negative-rotation.png)

**Figure 4.10: Reversing the imaginary component leaves the magnitude and circular trajectory unchanged, but reverses the direction of phase evolution.**

At first, surprisingly little appears to have changed.

The magnitude is still:

$$|z|=1$$

The constellation still shows a circle.

But look carefully at the phase.

Previously, the phase increased with time.

Now it decreases.

That difference is fundamental.

---

## 4.23 Positive and Negative Rotation

For the original signal,

$$z(t)=e^{+j2\pi ft}$$

the phase is

$$\theta(t)=+2\pi ft$$

As time increases, the phase increases.

For the modified signal,

$$z(t)=e^{-j2\pi ft}$$

the phase is

$$\theta(t)=-2\pi ft$$

As time increases, the phase decreases.

The two signals therefore travel around the same complex circle in opposite directions.

This gives us our first useful interpretation of **positive and negative complex frequency**.

> The sign tells us the direction in which the phase evolves around the complex plane.

A negative frequency does not mean that a radio somehow performs a negative number of oscillations per second.

It tells us about the direction of rotation in a complex representation.

There is something else worth noticing.

A static constellation plot shows the same circle in both cases.

From the circle alone, we cannot determine the direction of travel.

The phase-versus-time plot reveals what the static constellation cannot.

This is a good example of why signal processing often uses several different views of the same signal.

---

## 4.24 A Connection Back to Chapter 3

Remember the question that brought us here.

In Chapter 3, a real cosine produced frequency components at both positive and negative frequencies.

We now have a much better language for discussing what those signs mean.

We have seen two complex exponentials:

$$e^{+j2\pi ft}$$

and

$$e^{-j2\pi ft}$$

They represent opposite directions of phase evolution.

And Euler's formula tells us that cosine is closely connected to these complex rotations.

We will not complete that story yet.

There is one more idea we need first.

That idea is **I and Q**.

---

## 4.25 GNU Radio Toolbox: What We Added in This Chapter

Our flowgraph started very small and gradually became more capable.

The important new tools were:

| Block | Purpose |
|---|---|
| **Float to Complex** | Combines real and imaginary float streams into a complex stream |
| **Complex to Real** | Extracts the real component |
| **Complex to Imag** | Extracts the imaginary component |
| **Complex to Mag** | Calculates complex magnitude |
| **Complex to Arg** | Calculates complex phase |
| **QT GUI Constellation Sink** | Displays complex samples on a two-dimensional plane |
| **QT GUI Time Sink** | Lets us compare components, magnitude, and phase against time |

But the more important lesson is not memorizing the names of the blocks.

It is understanding the data flowing between them.

A complex sample contains two components:

$$z[n]=a[n]+jb[n]$$

Different blocks simply allow us to construct, separate, measure, or visualize those samples.

---

## 4.26 A Useful GNU Radio Habit: Watch Your Data Types

As flowgraphs become larger, one of the easiest mistakes to make is connecting incompatible data types.

A block expecting a float stream cannot necessarily accept a complex stream.

Similarly, a complex output contains information that a float output does not.

When a connection refuses to work, check:

1. the output data type of the first block,
2. the input data type expected by the second block,
3. the port colours.

Errors involving data types are not merely GNU Radio inconveniences.

They often tell us something important about what kind of signal we are actually processing.

---

## 4.27 Try It Yourself

Before moving to the next chapter, experiment with the flowgraph.

Do not immediately run each modification.

**Predict what you think will happen first.**

### Try 1: Increase the Imaginary Amplitude

Set the imaginary amplitude to:

$$2$$

What shape do you expect in the constellation?

What should happen to the magnitude?

---

### Try 2: Swap the Inputs

Connect the sine to the real input and the cosine to the imaginary input.

What changes?

Does the constellation remain circular?

What happens to the phase evolution?

---

### Try 3: Change the Frequency

Change both sources from 1 kHz to 2 kHz.

Does the radius of the constellation change?

How quickly does the phase complete one cycle?

---

### Try 4: Break the Data Type

Try connecting blocks with incompatible input and output types where GNU Radio permits you to attempt the connection.

What does GNU Radio tell you?

Look at the port colours and determine why the connection is invalid.

---

### Try 5: Use Unequal Frequencies

Keep the real component at 1 kHz and change the imaginary component to another frequency.

Before running it, ask yourself:

> Will the constellation still be a circle?

Then observe what happens.

We will encounter more complicated complex-plane patterns later.

---

## 4.28 What We Learned

We started this chapter with what looked like a strange mathematical object:

$$z=a+jb$$

But after building and manipulating complex signals in GNU Radio, the idea should now feel much more concrete.

A complex number contains two components:

$$\text{Real}+j\,\text{Imaginary}$$

The same complex number can also be described by:

$$\text{Magnitude}+\text{Phase}$$

Magnitude tells us how far the complex point is from the origin.

Phase tells us its angular position.

Euler's formula connects these descriptions:

$$e^{j\theta}=\cos\theta+j\sin\theta$$

When \(\theta\) changes with time, the complex number can be interpreted as a rotating vector.

We saw this directly in GNU Radio.

With

$$\cos\theta+j\sin\theta$$

we obtained a unit circle and increasing phase.

When the imaginary component was reduced, the circle became an ellipse.

When the imaginary component was removed, the trajectory collapsed onto the real axis.

And when the sign of the imaginary component was reversed, the magnitude and circle remained the same, but the direction of phase evolution reversed.

That last observation gave us our first physical intuition for the sign of complex frequency.

---

## 4.29 Where We Go Next

There is one detail we have deliberately ignored throughout this chapter.

Look again at the GNU Radio Constellation Sink.

GNU Radio does not label its axes **Real** and **Imaginary**.

Instead, it calls them:

**In-phase**

and

**Quadrature**.

Why?

Why does SDR use the names **I** and **Q**?

Why are the two components separated by 90 degrees?

And why does keeping both components allow an SDR to distinguish information that a single real waveform cannot?

In the next chapter, the real and imaginary components we have been working with finally receive their radio names:

$$x[n]=I[n]+jQ[n]$$

Now we are ready to understand what **I and Q signals** actually are.