from typing import Tuple
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import multiprocessing


# Constants
SPEC_HEAT_CAP = 4.0  # in J/g°C
DENS = 1.04  # in g/cm³
W = 4.0  # in cm
L = 6.0  # in cm
H = 3.0  # in cm
CONV_HEAT_TRANS_COEF = 10.0  # in W/m²K
ROOM_TEMP = 20.0  # in °C
SIM_LEN = 10000.0  # in seconds
SIM_STEPS = 1000

# Derived constants
VOLUME = W * L * H  # in cm³
MASS = VOLUME * DENS  # in g
SURF_AREA = 2 * ((W * L + W * H + L * H) / 10000)  # in m², converted from cm²


def model(T: float, t: float, k: float, room_temp: float) -> float:
    """
    Model for Newton's law of cooling.

    :param T: Current temperature.
    :param t: Time.
    :param k: Cooling constant.
    :param room_temp: Room temperature.
    :return: Rate of change of temperature.
    """
    return -k * (T - room_temp)

def format_func(value, tick_number):
    """Formats time values into appropriate units (hours, minutes)"""
    hours = int(value // 3600)
    minutes = int((value % 3600) // 60)
    return f'{hours}h {minutes}m'


def sim_temp_change(init_temp: float,
                    room_temp: float,
                    room_temp_target: float) -> Tuple[float, float, float]:
    """Simulate the time taken to cool to within 1 degree of room temperature
    for the given initial and room temperatures."""
    k_value = CONV_HEAT_TRANS_COEF * SURF_AREA / (MASS * SPEC_HEAT_CAP)
    t = np.linspace(0, SIM_LEN, SIM_STEPS)
    T = odeint(model, init_temp, t, args=(k_value, room_temp_target))
    time_to_cool = None
    for i in range(T.shape[0]):
        if abs(T[i] - room_temp) < 1:
            time_to_cool = t[i]
            break
    return init_temp, room_temp, time_to_cool


def perform_simulation(init_temps: np.ndarray,
                       room_temps: np.ndarray) -> np.ndarray:
    """Perform the simulation for the given initial and room temperatures."""
    # Create a 2D grid of initial and room temperatures
    # Use multiprocessing to simulate the time taken to cool to within 1 degree
    # of room temperature for each combination of initial and room temperature
    init_grid, room_grid = np.meshgrid(init_temps, room_temps)
    pool = multiprocessing.Pool(processes=(multiprocessing.cpu_count() - 1))
    # Create a list of tuples containing initial temps and room temps
    temp_tuples = [
        (init_temp, room_temp, ROOM_TEMP)
        for init_temp, room_temp in zip(init_grid.ravel(), room_grid.ravel())
    ]

    # Use starmap to apply the sim_temp_change function to each tuple in
    # parallel using the pool
    results = pool.starmap(sim_temp_change, temp_tuples)

    time_grid = np.zeros_like(init_grid)
    for i, (init_temp, room_temp, time_to_cool) in enumerate(results):
        row, col = np.unravel_index(i, init_grid.shape)
        time_grid[row, col] = time_to_cool
    return time_grid

def plot_results(init_grid: np.ndarray,
                 room_grid: np.ndarray,
                 time_grid: np.ndarray):
    """Plot the simulation results."""
    # Create a new figure with a 3D subplot and a 2D subplot
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(211, 
                         projection='3d',
                         proj_type='ortho',
                         azim=-120,
                         elev=30,
                         box_aspect=(1,1,1))
    # Draw the surface plot
    surf = ax.plot_surface(init_grid,
                           room_grid,
                           time_grid,
                           cmap='coolwarm',
                           linewidth=0,
                           antialiased=True)
    ax.set_xlabel('Initial Temperature (°C)')
    ax.set_ylabel('Room Temperature (°C)')
    ax.set_zlabel('Time to cool to within 1 degree of room temperature')
    ax.zaxis.set_major_formatter(ticker.FuncFormatter(format_func))

    # Draw the contour plot
    ax2 = fig.add_subplot(212)
    contour_levels = np.arange(0, 10000, 500)
    contour_fill = ax2.contourf(init_grid,
                                room_grid,
                                time_grid,
                                levels=contour_levels,
                                cmap='coolwarm')
    contour_lines = ax2.contour(init_grid,
                                room_grid,
                                time_grid,
                                levels=contour_levels,
                                colors='k')
    ax2.set_xlabel('Initial Temperature (°C)')
    ax2.set_ylabel('Room Temperature (°C)')
    ax2.clabel(contour_lines,
               inline=1,
               fontsize=10,
               fmt=ticker.FuncFormatter(format_func))
    
    # Add a colorbar to the contour plot
    colorbar = fig.colorbar(contour_fill,
                            ax=ax2,
                            format=ticker.FuncFormatter(format_func))

    fig.tight_layout()
    plt.show()

def main() -> None:
    """Main function for the program."""
    # Create a 2D grid of initial and room temperatures
    init_temps = np.linspace(0, 10, 100)
    room_temps = np.linspace(15, 25, 100)
    init_grid, room_grid = np.meshgrid(init_temps, room_temps)

    # Perform the simulation
    time_grid = perform_simulation(init_temps, room_temps)

    # Plot the simulation results
    plot_results(init_grid, room_grid, time_grid)


if __name__ == "__main__":
    main()
