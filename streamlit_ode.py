import networkx as nx
import streamlit as st

# create placeholder flowchart - i.e. a directed graph
G = nx.DiGraph()

start = r"Let's start with this: does your differential equation contain derivatives with respect to more than variable? For example, you may have both $\frac{\partial}{\partial t}$ and $\frac{\partial}{\partial x}$ in the equation?"
G.add_node(0, label=start)
is_ode = "Then it is an ODE! Let's standardise things a little: from now on, the variable with respect to which we derive is always called $x$, and $x$-derivatives will be denoted with a prime $(\ldots)'$. Is there more than one unknown function of $x$ kicking around in your equation?"
is_pde = "This is not an ODE, but rather a partial differential equation (PDE). These are much more advanced and require completely different techniques."

G.add_node(1, label=is_ode)
G.add_node(2, label=is_pde)
G.add_edge(0, 1, label='no, just one kind of derivative')
G.add_edge(0, 2, label='yes, more than one')

is_single_ode = r'''
Let's standardise further: we have a single unknown function, let's call it $y(x)$. Can you rearrange your equation such that the highest-order derivative of $y$ is isolated on the left-hand side?
'''

G.add_node(17, label=is_single_ode)
G.add_edge(1, 17, label='just one unknown function')

is_explicit_ode = r'''
Your equation now looks like 
$$
y^{(n)}(x) = \frac{d^n y(x)}{dx^n} = F\left(x, y, y', y'', \ldots, y^{(n-1)}\right)
$$
for some possibly complicated function $F(\ldots)$. 
The order of the highest derivative, $n$, is now the _order of your ODE_. 

Is $n=1$?
'''
is_implicit_ode = "TBD"

is_coupled_ode_system = "Looks like you have a system of coupled ODEs. "

G.add_node(3, label=is_explicit_ode)
G.add_node(18, label=is_implicit_ode)
G.add_node(4, label=is_coupled_ode_system)
G.add_edge(17, 3, label='yes, no problem!')
G.add_edge(17, 18, label='no, that is impossible')
G.add_edge(1, 4, label='more than one unknown function')

is_firstorder = r'''
So we have a single first-order ODE. Does the right-hand side $F$ depend on $x$ or $y$ at all?
'''
is_higher_than_first_order = r"Is $n=2$?"
G.add_node(5, label=is_firstorder)
G.add_node(6, label=is_higher_than_first_order)
G.add_edge(3, 5, label="yes, $y'$ is the highest derivative to appear")
G.add_edge(3, 6, label='no, we have higher derivatives of $y$ than the first')

can_be_integrated_directly = r'''
You're in luck! This ODE is as simple as can be. You can just throw an integral onto the RHS and write
$$
y(x) = y_0 + \int_{x_0}^{x} d\tilde x\,F(\tilde x),
$$
where $y(x_0)=y_0$ is your given initial condition.
'''
is_autonomous = r'''
So your equation looks like 
$$
y'(x) = F(y).
$$
This is known as an _autonomous_ ODE. We can solve it like a separable one: shuffle all $y$-dependent stuff onto the LHS, all, $x$-dependent stuff onto the RHS, and integrate:
$$
\int \frac{dy}{F(y)} = \int dx = x + C,
$$
or if you'd prefer to avoid futzing around with the integration constant $C$ in favour of the initial value $y(x_0) = y_0$, then you may write it as
$$
\int_{y_0}^{y(x)} \frac{d\tilde y}{F(\tilde y)} = \int_{x_0}^x d\tilde x = x - x_0.
$$
Now all that is left to do is: crack the LHS integral, and manipulate until you manage to isolate $y(x)$.

You will notice that $y(x)$ depends only on the distance to the starting point $x-x_0$. This strictly constrains the possible shape of $y(x)$, so we found a general and very useful feature of autonomous ODEs: shifting one solution in $x$-direction will again yield a solution.
'''
is_nonautonomous = r'''
Your equation looks like
$$
y'(x) = F(x, y).
$$
Does the RHS perhaps factorise like this: $F(x, y) = f(x)g(y)$? It might not be immediately obvious, so keep trying to bring it into this form.
'''

G.add_node(7, label=can_be_integrated_directly)
G.add_node(8, label=is_autonomous)
G.add_node(9, label=is_nonautonomous)
G.add_edge(5, 7, label='$F$ is a function of $x$ only')
G.add_edge(5, 8, label='$F$ is a function of $y$ only')
G.add_edge(5, 9, label='$F$ contains both variables')

is_separable = r'''
Nice! Your ODE is _separable_. What this means is that you can accumulate everything $y$-dependent on the LHS, and everything $x$-dependent on the RHS, and integrate:
$$
\frac{dy}{dx} = f(x)g(y) \Rightarrow \int \frac{dy}{g(y)} = \int dx\,f(x) + C,
$$
where we can mash both integration constants into one. Now you need to crack both integrals, and isolate $y(x)$ on the LHS, and you are done.
If you have an initial value $y(x_0) = y_0$, then you can write this cleaner by incorporating it - obviously that will remove the integration constant $C$:
$$
\int_{y_0}^{y(x)} d\tilde y\frac{1}{g(\tilde y)} = \int_{x_0}^xd\tilde x f(\tilde x)
$$
'''
is_nonseparable = r'''
Next try: does $y$ appear only linearly, meaning in the first power and not inside some other function? In other words, can you find functions $p(x)$ and $q(x)$ _of $x$ only_ so that you can write the ODE as
$$
y' + p(x) y = q(x)?
$$
'''

G.add_node(10, label=is_separable)
G.add_node(11, label=is_nonseparable)
G.add_edge(9, 10, label='yes, it factorises')
G.add_edge(9, 11, label="I tried long enough, it won't")

is_linear_firstorder = r'''
We have a _linear_ first-order ODE $y' + p(x) y = q(x)$. There is a general solution formula that applies to all of them, known by the name _integrating factor_. In its full glory it is somewhat intimidating:
$$
y = \frac{\int \mu(x) q(x) dx + C}{\mu(x)}
$$
with
$$
\mu = \exp\int p(x) dx. 
$$
If you read off $p(x)$ and $q(x)$ from comparing your ODE to the general form $y' + p(x)y = q(x)$, and plug those two functions into the above formula, you get your general solution $y(x)$ upon cracking all of the integrals.

If that formula above looks scary you, no worries! It's totally possible to solve every linear first-order ODE without ever breaking it out. There is an alternative more benign method which will get you to the solution step by step, and it also memorises easier. Ultimately, it's a matter of personal preference.
'''

G.add_node(12, label=is_linear_firstorder)
G.add_edge(11, 12, label='yes, that works!')

can_be_simplified_voc_firstorder = r'''
We have a first-order ODE with an _inhomogeneity_, meaning a term that depends only on $x$. One example is the most general linear first-order form $y' + p(x)y = q(x)$. Here, the right-hand side term $q(x)$ is the inhomogeneity. 

The method to solve these is a two-step process. First, we solve a related auxiliary ODE, which is _simpler_. The solution will allow us to smartly guess an ansatz for the full ODE, leaving us with another _simpler_ ODE. 

Firstly: rewrite the ODE by dropping the inhomogeneity. This simplifies the equation - in the above example we have $y_h' + p(x) y_h = 0$ left. Since it's a different equation than the one we actually want to solve, we swapped $y(x)$ for $y_h(x)$ - the latter is the solution to our _auxiliary_ ODE. Solve this by whatever means - the above example can be cracked by separation of variables (you can review that method via the button below). Or return to start, if you began with something nonlinear - you can find the substitution you need. 

Either way, you should get an expression for the function $y_h(x)$ with one constant of integration, say, $C$. This $y_h(x)$ is sometimes known as the _particular_ or _complementary_ solution.

Secondly, a sleight of hand: we promote $C$ to a function of $x$. Our ansatz for $y$ is just the expression of $y_h$, except that we replace $C$ by $C(x)$. Ultimately that does only takes all our ignorance about the function $y(x)$ and mashes it into $C(x)$. When we plug that ansatz into the _full_ equation (including the inhomogeneity again!), we will receive a first-order ODE for $C(x)$. But, as if by magic, many terms will drop out! In the end the ODE for $C(x)$ will be easier than the original one for $y(x)$ - you can return to start to crack it.

For reasons that are probably obvious, this trick is known as _variation of constants_. It can also be applied to higher-order ODEs - except that there you have as many unknown functions as you have constants of integration in your particular solution, so it's going to be more complicated.
'''
has_inhomogeneity_higherorder = r'''
TBD
'''

G.add_node(13, label=can_be_simplified_voc_firstorder)
G.add_node(20, label=has_inhomogeneity_higherorder)
G.add_edge(12, 13, label='please take me to the alternative method')
G.add_edge(13, 10, label='please take me to separation of variables')
G.add_edge(13, 20, label='please tell me more how to apply this to higher-order ODEs')
G.add_edge(20, 13, label='please let me review variation of constants for first-order ODEs')

is_nonlinear_firstorder = r'''
Before we jump into possible substitutions, let's check if there is an obvious candidate ansatz. Plug in the following test functions and see if you can crack whatever equation falls out:
* power law: $y(x) = x^\alpha$ for some unknown real number $\alpha$
* exponential: $y(x) = \exp [\lambda x]$ for some unknown real or complex $\lambda$
* trig functions: $y(x) = \sin(x), \cos(x), \tan(x)$
* be creative!

It's often a good idea to take an inspiration from the terms already kicking around in your equation: the best way to cancel an expression containing an $\exp$ is with another $\exp$. Also, it may well be that a well-chosen ansatz does not outright solve the equation, but simplifies it: for example, if your ansatz makes all terms cancel except purely $x$-dependent ones, have a look at _variation of constants_.
'''

has_no_obvious_ansatz = r'''
Let's check if your equation is of the _Bernoulli_ type: does $y$ appear as a power $\nu$, such that you can bring the equation into the form
$$
y' + P(x) y = Q(x)y^\nu?
$$
Here, $P$ and $Q$ can be any functions of $x$, and $\nu$ can be any _real_ number except 0 (then we'd have used integrating factor or variation of constants) or 1 (then we'd have used separation of variables). Note: in the literature, you will see $n$ in place of $\nu$, but we already use $n$ to denote the order of the highest derivative.
'''

is_bernoulli = r'''
Great! The way to crack it is to pull a clever substitution out of a hat. Define a new function 
$$
u(x) = y(x)^{1-\nu}
$$
In your original ODE, replace all $y$, $y'$ by $u$, $u'$ and after some algebra you will have a _linear_ first-order ODE for $u(x)$ which you can solve by conventional means. Then take that to the power $\frac{1}{1-\nu}$ to get $y$.
'''

G.add_node(29, label=is_nonlinear_firstorder)
G.add_node(15, label=has_no_obvious_ansatz)
G.add_node(16, label=is_bernoulli)

G.add_edge(29, 13, label='please explain variation of constants')
G.add_edge(29, 15, label='nothing has worked')
G.add_edge(11, 29, label='nope, we have some nastier function of $y$')
G.add_edge(15, 16, label='yes it does!')
G.add_edge(16, 12, label='please tell me how to solve the ODE for $u(x)$')

is_not_bernoulli = r'''
Is the right-hand side of your ODE some monomial in $x$ and $y$?
'''

is_monomial = r'''
If your nonlinear $F(x, y)$ has a monomial shape, try the substitution
$$
y(x) = x^r [u(x)]^s
$$
with unknown real numbers $r, s$. Insert into the ODE and try to choose $r$ and $s$ such that as many terms as possible drop out, and make the ODE for $u(x)$ as simple as possible - ideally linear! 
'''

is_not_monomial = r'''
Is the right-hand side your ODE of the form 
$$
y' = f(ax+by+c)
$$
for some real numbers $a, b, c$ and some nonlinear function $f$?
'''

G.add_node(19, label=is_not_bernoulli)
G.add_node(40, label=is_monomial)
G.add_node(41, label=is_not_monomial)
G.add_edge(15, 19, label='no, I have some other nonlinearity')
G.add_edge(19, 40, label='yes it is')
G.add_edge(40, 41, label='nothing useful came of it')
G.add_edge(19, 41, label='it is not')

is_ax_by_c = r'''
If your equation has the shape $y' = f(ax+by+c)$ for real numbers $a, b, c$ and some given function $f$, you can crack it this way: define a new function $z(x) = ax+by(x)+c$ and substitute into the existing ODE. The result is this:
$$
z = ax + by + c \Rightarrow z' = \frac{dz}{dx} = a + by' = a + b f(z)
$$
The resulting ODE $z' = a + b f(z)$ is now easy to solve - it is an autonomous equation!
'''

G.add_node(21, label=is_ax_by_c)
G.add_edge(41, 21, label='yes it is!')
G.add_edge(21, 8, label='please tell me how to solve the ODE for $z$')

is_not_ax_by_c = r'''
Is your equation of the shape
$$
y' = f\left(\frac{y}{x}\right)?
$$
It may not be immediately obvious - as in this example:
$$
y' = \frac{y-x}{y+x} = \frac{\frac{y}{x}-1}{\frac{y}{x}+1}
$$
'''

is_homogeneous = r'''
An equation of the type
$$
y' = f\left(\frac{y}{x}\right)
$$
is known as _homogeneous_. Confusingly so, because any ODE without an inhomogeneity (a term in $F(x, y)$ containing only $x$) is _also_ called homogeneous! Always make sure which sense of homogeneity applies.

The substitution we need to crack this is $u(x) = y(x)/x$. This means that $y = xu$ and $y' = u + xu'$, so
$$
y' = u + xu' = f(u)\Rightarrow u' = \frac{f(u)-u}{x}
$$
which is separable:
$$
\int\frac{du}{f(u)-u} = \int\frac{dx}{x} = \ln(x)+C
$$
'''

G.add_node(23, label=is_not_ax_by_c)
G.add_node(24, label=is_homogeneous)
G.add_edge(41, 23, label='my $F(x, y)$ looks different')
G.add_edge(23, 24, label='yes, that applies')

is_not_homogeneous = r'''
Does your ODE have the shape
$$
y' = f\left(\frac{ax+by+c}{r x+s y+t}\right)
$$
with $a, b, c, r, s, t$ some real numbers? If yes, is $a s =r b$?
'''

is_shiftable_nonzero_det = r'''
If $as \neq rb$, then you can solve the linear system
$$
\left\{\begin{align*}
a\xi + b\eta + c = 0\\
r\xi + s\eta + t = 0
\end{align*}\right.
$$
by whichever linear algebra technique you are most familiar with - there will always be one unique pair of numbers $(\xi, \eta)$. Substitute $u = x - \xi$ and $v = y-\eta$. We plan to replace $y(x)$ by $v(u)$ in the ODE - with some algebra you will find two equations:
$$
\frac{dv}{du} = \frac{dy}{dx}\qquad;\qquad\frac{ax+by+c}{r x+s y+t} = \frac{au+bv}{ru+sv} = \frac{a + b\frac{v}{u}}{r + s\frac{v}{u}}.
$$
This means that we have reduced our ODE to one of the homogeneous type
$$
\frac{dv}{du} = g\left(\frac{v}{u}\right)
$$
which we have dealt with before. Specifically, $g(z) = f\left(\frac{a+bz}{r+sz}\right)$.
'''

is_shiftable_zero_det = r'''
We can reduce the equation $y' = f\left(\frac{ax+by+c}{r x+s y+t}\right)$ to a system we have handled before. If $as = rb$, then we can define $\mu = \frac{a}{r} = \frac{b}{s}$, and
$$
\frac{ax+by+c}{rx+sy+t} = \frac{\mu rx+\mu sy + \mu t - \mu t+c}{rx+sy+t} = \mu + \frac{c-\mu t}{rx+sy+t}.
$$
This means that $f\left(\frac{ax+by+c}{r x+s y+t}\right)$ has the shape $g(rx+sy+t)$, which we have dealt with before. In particular, take 
$$
g(z) = f\left(\mu + \frac{c-\mu t}{z}\right).
'''


G.add_node(26, label=is_not_homogeneous)
G.add_node(27, label=is_shiftable_nonzero_det)
G.add_node(28, label=is_shiftable_zero_det)
G.add_edge(23, 26, label='my $F$ looks different still')
G.add_edge(26, 27, label='yes that works, and $a s ≠ r b$')
G.add_edge(26, 28, label='yes that works, and $a s = r b$')
G.add_edge(28, 21, label='how do I solve the simplifed $g$ equation, again?')
G.add_edge(27, 24, label='how do I solve the simplified $g$ equation again?')

is_not_shiftable = r'''
Does your equation have the shape
$$
y' = p(x) + q(x)y + r(x)y^2
$$
with $p, q, r$ three functions of $x$ only?
'''

is_riccati = r'''
Any equation $y' = p(x) + q(x)y + r(x)y^2$ is of _general Riccati_ type. It is a generalisation of the Bernoulli type with exponent $\nu=2$ (set $p\equiv 0$). It is a nonlinear first-order equation, so there may be more than one family of solutions - as opposed to linear first-order equations, where there is always one family (particular solution + integration constant * homogeneous solution). Indeed this is the case here.

There are two things you can try. First, a strategy to find the general solution from a guess for a particular solution. To do this, assume that by skillful staring and/or sheer guessing luck you have found one solution $y_1(x)$. Now substitute the following ansatz for the general solution into the equation:
$$
y(x) = y_1(x) + \frac{1}{z(x)}
$$
with a new unknown function $z(x)$. After a benign amount of algebra you reach the following ODE in $z$:
$$
z' = -[2r(x)y_1(x) + q(x)] z - r(x),
$$
which is a first-order linear inhomogeneous equation which you can solve by standard methods. The solutions for your Riccati-type equation are $y_1$ and $y_1 + z^{-1}$.

The second trick does not assume you to guess, but rather shows a way to reduce your first-order Riccati equation to a second order linear homogeneous equation. This is how to do it: assume that there is a function $u(x)$ satisfying $u'/u = - r y$. Then, after some algebra you find that it reduces the Riccati equation to the following ODE
$$
u'' = \left[q(x)+\frac{r'(x)}{r(x)}\right]u' - p(x)r(x)
$$
which is second-order, linear and homogeneous. Find a solution, and then find $y = -u'/(ru)$.

'''
is_second_order_linear_homogeneous = r'''
TBD
'''

G.add_node(30, label=is_not_shiftable)
G.add_node(31, label=is_riccati)
G.add_node(33, label=is_second_order_linear_homogeneous)

G.add_edge(26, 30, label='neither that one')
G.add_edge(30, 31, label='that matches!')
G.add_edge(30, 32, label='again, no match')
G.add_edge(31, 32, label='none of that helped')
G.add_edge(31, 12, label='how do I solve linear first-order inhomogeneous again?')
G.add_edge(31, 33, label='and how do I solve linear second-order homogeneous?')

is_not_general_riccati = r'''
Does your equation have the shape
$$
y' = a x^\alpha + b y^2,
$$
where $a, b\in\mathbb{R}$ and the negative exponent $\alpha$ equals 
* either $\alpha = -2$,  
* or a negative number of shape $\alpha = -\frac{4m}{2m-1}$ with an integer $m\in\mathbb{N}$ (so $\alpha = -4, -8/3, -12/5, -16/7, \ldots$), 
* or a negative number of shape $\alpha = -\frac{4m}{2m+1}$ with an integer $m\in\mathbb{N}$ (so $\alpha = -4/3, -8/5, -12/7, -16/9, \ldots$).
'''

is_special_riccati_2 = r'''
Your equation is 
$$
y' = \frac{a}{x^2}+ b y^2
$$
with real numbers $a, b$. Substitute in a new function $u(x) = 1/y(x)$, so $y' = -u'/u^2$. You get an ODE for $u$ of the shape
$$
u' = -a\left(\frac{u}{x}\right)^2-b
$$
which is of the "homogeneous" type $y' = f(y/x)$.
'''
is_special_riccati_mminus = r'''
Your equation has the shape $y' = a x^\alpha + b y^2$ with real numbers $a, b$, and where the exponent of $x$ has the shape $\alpha = -\frac{4m}{2m-1}$.
This is going to be a cascading chain of substitutions, so strap in:

1) First substitute $z = x^2 y + \frac{x}{b}$. This yields 
$$
z' = a x^{\alpha+2}+ \frac{b}{x^2} z^2.
$$
2) Next substitute _both_ the function and the variable: 
$$
u = x^{\alpha+3}\rightarrow x = u^{1/(\alpha+3)}\qquad;\qquad v(u) = \frac{1}{z(x)}.
$$
Now,
$$
\frac{dv}{du} = \frac{dv}{dz}\frac{dz}{dx}\frac{dx}{du} = \left(-v^2\right)\left(a x^{\alpha+2}+\frac{b z^2}{x^2}\right)\left(\frac{u^{-\frac{\alpha+2}{\alpha+3}}}{\alpha+3}\right)=-\frac{b}{\alpha+3}u^{-\frac{\alpha+4}{\alpha+3}}-\frac{a}{\alpha+3}v^2.
$$
3. Given that $\alpha=-\frac{4m}{2m-1}$, we get $-\frac{\alpha+4}{\alpha+3} = -\frac{4(m-1)}{2(m-1)-1}$. This means that we have reduced our original equation to one of the same shape, but with modified coefficients and also $m\rightarrow m-1$. Therefore you can go repeat steps 1 and 2, each time knocking down $m$ by $1$, until you reach $m=0$.
4. The leftover equation is separable. Solve it, and then unravel the daisy chain of substitutions.
'''
is_special_riccati_mplus = r'''
Your equation has the shape $y' = a x^\alpha + b y^2$ with real numbers $a, b$, and where the exponent of $x$ has the shape $\alpha = -\frac{4m}{2m+1}$.
This is going to be a cascading chain of substitutions, so strap in:

1. First substitute _both_ the function and the variable: 
$$
u = x^{-(\alpha+1)}\rightarrow x = u^{-1/(\alpha+1)}\qquad;\qquad z(u) = \frac{1}{y(x)}.
$$
Now,
$$
\frac{dz}{du} = \frac{dz}{dy}\frac{dy}{dx}\frac{dx}{du} = \left(-z^2\right)\left(a u^{-\frac{\alpha}{\alpha+1}}+\frac{b}{z^2}\right)\left(-\frac{u^{-\frac{\alpha+2}{\alpha+1}}}{\alpha+1}\right)=\frac{a}{\alpha+1}\frac{z^2}{u^2} + \frac{b}{\alpha+1}u^{-\frac{\alpha+2}{\alpha+1}}.
$$
2. Now, substitute $v(u) = \frac{z(u)}{u^2}$. This yields
$$
\frac{dv}{du} = \frac{dv}{dz}\frac{dz}{du} = \frac{1}{u^2}\left(\frac{a}{\alpha+1}\frac{v^2u^4}{u^2} + \frac{b}{\alpha+1}u^{-\frac{\alpha+2}{\alpha+1}} \right) = \frac{a}{\alpha+1} v^2 + \frac{b}{\alpha+1}u^{-\frac{3\alpha+4}{\alpha+1}}.
$$
3. Given that $\alpha=-\frac{4m}{2m+1}$, we get $-\frac{3\alpha+4}{\alpha+1} = -\frac{4(m-1)}{2(m-1)+1}$. This means that we have reduced our original equation to one of the same shape, but with modified coefficients and also $m\rightarrow m-1$. Therefore you can go repeat steps 1 and 2, each time knocking down $m$ by $1$, until you reach $m=0$.
4. The leftover equation is separable. Solve it, and then unravel the daisy chain of substitutions.
'''

G.add_node(32, label=is_not_general_riccati)
G.add_node(34, label=is_special_riccati_2)
G.add_node(35, label=is_special_riccati_mminus)
G.add_node(36, label=is_special_riccati_mplus)

G.add_edge(32, 34, label='looks good, tell me more! My exponent is $-2$')
G.add_edge(32, 35, label='looks good, tell me more! My exponent is $-4m/(2m-1)$ for some $m\in\mathbb{N}$')
G.add_edge(32, 36, label='looks good, tell me more! My exponent is $-4m/(2m+1)$ for some $m\in\mathbb{N}$')
G.add_edge(34, 24, label="how do I solve $y' = f(y/x)$ again?")


has_no_substitutions_firstorder = r'''
We have gone through a bunch of possible shapes for $F(x, y)$ and the corresponding substitutions that simplify the ODE. 

If any of the substitutions we just went through was close to your RHS, perhaps fitting except for one term, it is still worth plugging it in. Even if it does not outright crack the equation, you may end up with an equation that's easier to solve. Often enough, solving ODEs is a task where you slowly whittle away through a chain of substitutions until you get an equation simple enough to crack directly.

Once you have juggled the terms of the ODE for long enough, you may have formed an intuition what you would need to do to make some terms vanish. Does any combination of $y$-dependent terms look like a total derivative, such as $y^2 y' = \frac{d}{dx} \left(\frac{y^3}{3}\right)$? Or $\frac{y'}{y} = \frac{d}{dx}\ln y$? Or something adjacent that can be turned into one?

Do not limit yourself to substituting in a new unknown function for $y$ - you can also reparametrise your independent variable $x$ to something else, for example $\tau = \sqrt x$ or $\tau = \ln x$. The next step is to work out the old derivative operator in terms of the new: $\frac{d}{dx} = \frac{d\tau}{dx}\frac{d}{d\tau}$ Have a look at what $x$-dependent terms appear in the equation and see if turning those into a new variable might help simplifying terms. Maybe you recognise a pattern like $\frac{dx}{d\tau}\frac{d}{dx}$ for some well-chosen $\tau$?
'''

needs_voc = r'''
If your equation falls into none of the categories and no substitution gets you anywhere, perhaps we can simplify it and reduce it to one where some may.

Does the $F(x, y)$ in your equation $y' = F(x, y)$ fall apart like this
$$
F(x, y) = f(x, y) + q(x),
$$
where $q(x)$ does not depend on $y$, and the ODE were much simpler if $F(x, y)$ were replaced by $f(x, y)$ instead? For example, we could have $f(x, y)$ of any of these possible shapes
* $f(x, y) = g(x)h(y)$
* $f(x, y) = p(x)y + q(x)y^\nu$ with real $\nu\neq 0, 1$
* $f(x, y) = g(ax+by+c)$
* $f(x, y) = g(y/x)$
* $f(x, y) = g\left(\frac{ax+by+c}{\alpha x+\beta y + \gamma}\right)$
'''

has_no_substitutions_even_dropping_inhomogeneity_firstorder = r'''
Let us try something different: rearrange the ODE in the shape
$$
M(x, y) dx + N(x, y) dy = 0.
$$
You have a lot of freedom in choosing the functions $M$, $N$ because at this point the only constraint is that $F(x, y) = - M(x, y)/N(x, y)$. We want to use this freedom to arrange
$$
\frac{\partial M}{\partial y} = \frac{\partial N}{\partial x}.
$$
This is known as the _integrability condition_. Muster your creativity and try to find $M$, $N$ that fit this.
'''


G.add_node(25, label=has_no_substitutions_firstorder)
G.add_node(14, label=needs_voc)
G.add_node(22, label=has_no_substitutions_even_dropping_inhomogeneity_firstorder)
G.add_edge(32, 25, label='not helpful')
G.add_edge(25, 15, label='can I see the substitutions again?')
G.add_edge(25, 14, label='no progress')
G.add_edge(14, 13, label='that could work!')
G.add_edge(14, 22, label='that will not help')

is_exact = r'''
You have found two functions $M$, $N$ such that your ODE looks like $M dx + N dy = 0$ and $\partial_y M = \partial_x N$ - this is the _integrability condition_, and an ODE that allows for this is called _exact_. One way to create such functions is if they are the gradient of some potential function:
$$
\left[\begin{align*}
M(x, y)\\N(x, y)
\end{align*}\right] = \nabla \Phi(x, y).
$$
In that case the integrability condition works out automatically because the second derivatives of the potential commute: $\partial_y\partial_x\Phi = \partial_x\partial_y\Phi$. There is a neat bit of differential geometry that shows that this works the other way round too: if the integrability condition is satisfied, then you can always find such a potential $\Phi$ via the ansatz
$$
\Phi(x, y) = \int M(x, y) dx + \chi(y)
$$
which automatically satisfies $M = \partial_x\Phi$. To ensure that $N =\partial_y\Phi$, you need to solve the ODE for the rest term $\chi$:
$$
\partial_y\chi(y) = N(x, y) - \int\partial_y M(x, y) dx,
$$
which is first-order and benign. Now insert $\Phi$ into the ODE, keeping in mind we want to solve for a function $y(x)$, a curve in the plane: 
$$
0 = \partial_x\Phi(x, y) dx + \partial_y\Phi(x, y)\frac{dy}{dx}dx = \frac{d}{dx}\Phi(x, y(x)) dx.
$$
If we keep along a constant-potential curve, we get to fulfill our ODE! So if you have an explicit expression for your potential, you can find the ODE solutions $y(x)$ via the implicit equation
$$
\Phi(x, y(x)) = C.
$$
'''

is_not_exact = r'''
You have written your ODE as $M(x, y)dx + N(x, y)dy = 0$. There is one more trick worth trying to find $M$, $N$ that satisfy the integrability condition $\partial_y M = \partial_x N$, namely with a generalisation of the _integrating factor_ method. Here we use it to systematically explore the space of functions $M$, $N$ obeying $M/N=-F$. 

If $M dx + N dy = 0$, then so will $(\mu M) dx + (\mu N) dy=0$ for any function $\mu = \mu(x, y)$. If $\partial_y M \neq \partial_x N$, what condition on $\mu$ would allow us to arrange $\partial_y (\mu M) = \partial_x (\mu N)$? Then we can just use $\mu M$ and $\mu N$ as the coefficient functions of our now-exact equation.

The answer is that $\mu(x, y)$ must obey the _partial differential equation_
$$
M\partial_y\mu - N\partial_x\mu + \left(\partial_yM - \partial_x N\right)\mu = 0
$$
which in general is way too horrendously complicated to solve by analytical means. However - if you are at this point, just write down the corresponding PDE, perhaps there are simplifications and cancellations in your particular case. For example, if $(\partial_y M - \partial_x N)/N$ has all $y$'s drop out, then you may assume that $\mu = \mu(x)$, and the PDE reduces to an ODE which can be cracked with a simple separation of variables.
'''

cant_be_made_exact_with_integrating_factor = r'''
If you made it to here, we need to contemplate the idea that there may not be an exact analytic solution to your problem. This is far from giving up - we just need to look to other, more qualitative techniques of what it means to solve your system. Three important alternative viewpoints are 
1) graphical methods: great for intuition building
2) perturbative methods: find and refine approximate solutions
3) numerical methods: put your ODE in a computer
'''

G.add_node(37, label=is_exact)
G.add_node(38, label=is_not_exact)
G.add_node(39, label=cant_be_made_exact_with_integrating_factor)
G.add_edge(22, 37, label='I found some! What now?')
G.add_edge(38, 37, label='I made it exact with an integrating factor! What now?')
G.add_edge(22, 38, label='I tried everything')
G.add_edge(38, 39, label='nope, nothing works')

needs_graphical = r'''
TBD
'''

needs_perturbative = r'''
TBD
'''

needs_numerical = r'''
TBD
'''

G.add_node(42, label=needs_graphical)
G.add_node(43, label=needs_perturbative)
G.add_node(44, label=needs_numerical)
G.add_edge(39, 42, label='please tell me more about graphical methods')
G.add_edge(39, 43, label='please tell me more about perturbative methods')
G.add_edge(39, 44, label='please tell me more about numerical methods')

# add return edges
for node in G.nodes:
    if node != 0:
        G.add_edge(node, 0, label='return to start')

# helper function that extracts outgoing edge labels and target nodes from node number
def get_desc_node_data(node):
    out_edges = G.out_edges(node, data=True)
    return {edge_data['label']: tail for head, tail, edge_data in out_edges}

# streamlit stuff begins here

# keep track of where in the graph we are
if "current_node" not in st.session_state:
    st.session_state.current_node = 0

if "node_history" not in st.session_state:
    st.session_state.node_history = [st.session_state.current_node]

# this renders the label of the current node, and a button for every outgoing edge
@st.experimental_fragment
def draw_buttons():
    #current_node = st.session_state.current_node
    st.text(f'current node number: {current_node}')
    st.markdown(G.nodes[current_node]['label'])
    node_data = get_desc_node_data(current_node)
    #st.text(f'outgoing data: {node_data}')
    if node_data: # may be empty if terminal node
        container = st.container()
        for (reply, next_node) in node_data.items():
            #st.text(reply + ' : ' + str(next_node))
            # define callback that traverses the clicked edge
            def traverse_graph(next_node):
                st.session_state.current_node = next_node
                st.session_state.node_history.append(next_node)

            # render buttons
            container.button(label=reply, 
                             on_click=traverse_graph, 
                             args=[next_node],
                             use_container_width=True)

        
        # render one extra button for "go back"
        def go_back():
            st.session_state.node_history = st.session_state.node_history[:-1]
            st.session_state.current_node = st.session_state.node_history[-1]
        if len(st.session_state.node_history) > 1:
            container.button(label="go back", 
                             on_click=go_back,
                             use_container_width=True)

# streamlit app rendering begins here
st.header("So you've got this ODE ...", divider='rainbow')
draw_buttons()
st.page_link(label="Comments? Find me and tell me!", page="https://cosmorobb.science")