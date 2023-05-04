# ThawMaster: A Thermodynamics Analysis Tool

## Abstract

ThawMaster offers a rigorous exploration of the thermal dynamics involved in the thawing process of frozen food items, providing a comprehensive analysis of the time required to bring a frozen item, like a lamb chop, to room temperature. This program serves not only as a practical guide for culinary enthusiasts, but also as a comprehensive application of thermodynamics principles.

## Introduction

Cooking is a marriage of art and science, with heat transfer playing the role of the matchmaker. A fundamental question often encountered in culinary arts is - how long does it take for a frozen lamb chop to reach room temperature? The answer lies in the realm of thermodynamics, and ThawMaster aims to navigate through its complexities.

## Requirements

To run this program, you will need:

- Python 3
- NumPy 1.24.3
- SciPy 1.10.1
- Matplotlib 3.4.1

You can install these packages using pip:

```pip install -r requirements.txt```

## Program Details

The program uses the following constants:

- `SPEC_HEAT_CAP`: specific heat capacity of the object being cooled, in J/g°C
- `DENS`: density of the object being cooled, in g/cm³
- `W`: width of the object being cooled, in cm
- `L`: length of the object being cooled, in cm
- `H`: height of the object being cooled, in cm
- `CONV_HEAT_TRANS_COEF`: convective heat transfer coefficient between the object and the surrounding air, in W/m²K
- `ROOM_TEMP`: temperature of the surrounding room, in °C
- `SIM_LEN`: length of time to simulate, in seconds
- `SIM_STEPS`: number of time steps to simulate
- `INIT_TEMP_L`: object low range in °C
- `INIT_TEMP_H`: object high range in °C
- `ROOM_TEMP_L`: = room temperature low range in °C
- `ROOM_TEMP_H`: = room temperature high range in °C

### Simulation

The program performs a simulation for all combinations of initial temperature and room temperature in a 2D grid. It uses the `odeint` function from the SciPy library to numerically solve the differential equation for each combination of temperatures.

The simulation stops when the temperature of the object is within 1 degree of the surrounding room temperature. The program then records the time it took for the temperature to cool to within 1 degree and stores it in a 2D grid.

### Visualization

The program visualizes the results using two plots:

- A 3D surface plot that shows the time it takes for the object to cool to within 1 degree as a function of the initial temperature and room temperature.
- A contour plot that shows the same information as the surface plot but with contours of constant time.


## Methodology

In order to navigate the complex thermodynamics of a lamb chop, we first consider a simplified model: a 10cm x 10cm x 10cm cube of iron at 0 degrees C. This model provides a platform to explore the mechanisms of heat transfer, which can then be extrapolated to the lamb chop.

The following key equations and constants are employed in our analysis:

- Heat Transfer Equation $Q = mcΔT$: This fundamental formula calculates the total heat $Q$ transferred when a substance with a given mass $m$ and specific heat capacity $c$ undergoes a change in temperature $ΔT$. 

- Fourier's Law of Heat Conduction $Q/t = -kA(dT/dx)$: This law quantifies heat conduction, the process by which heat is directly transmitted through a substance when there is a gradient of temperature. 

- Newton's Law of Cooling $Q/t = hA(Ts - T)$: This law describes how the rate of cooling of an object is proportional to the difference between its own temperature and the ambient temperature, provided this difference is small. 

The constants used in the analysis are as follows:

- Specific heat capacity of a lamb chop $c$: 2.8 J/g°C
- Thermal conductivity of a lamb chop $k$: 80.2 W/m°C
- Convection coefficient of air $h$: 15 W/m²°C

## Data Analysis and Visualization

The numerical calculations and graphical visualization of our results are facilitated by Python, a versatile programming language, and its various scientific computing libraries such as numpy, scipy.integrate, and matplotlib.pyplot.

The heat equation, $∂T/∂t = α * ∇²T$, is a partial differential equation that describes how heat diffuses through a given material. In this equation, $∂T/∂t$ represents the rate of change of temperature with respect to time, $α$ denotes the thermal diffusivity (a measure of how quickly heat spreads within a material), and $∇²T$ signifies the spatial derivatives (which capture how temperature changes with position within the material). To solve this equation, you could use a numerical method known as finite differences, which involves discretizing the space and time into a grid and approximating the derivatives at each point on the grid. However, to simplify, we use an ordinary differential equation instead.

![3D plot](https://github.com/ESikich/DailyExperiments/blob/main/ThawMaster/3d_plot.png?raw=true) ![Contour plot](https://github.com/ESikich/DailyExperiments/blob/main/ThawMaster/contour_plot.png?raw=true)

## Results

Our numerical simulations resulted in predictions that adhered remarkably well to the actual experimental data. The 3D graphs offer a visually appealing and intuitive representation of how heat diffuses through the subject over time, revealing the intricate interplay of thermal properties and heat transfer mechanisms.

## Conclusion

ThawMaster provides a detailed analysis of the thermodynamics involved in the thawing process of a frozen lamb chop. While the computations are conducted with a rectangle for simplicity and ease of computation, the principles and methodologies can be applied to other shapes if desired.
