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
INIT_TEMP_L = 0 # in °C
INIT_TEMP_H = 5 # in °C
ROOM_TEMP_L = 5 # in °C
ROOM_TEMP_H = 21 # in °C

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

def format_func(value, tick_number) -> str:
    """Formats time values into appropriate units (hours, minutes)"""
    hours = int(value // 3600)
    minutes = int((value % 3600) // 60)
    return f'{hours}h {minutes}m'

def sim_temp_change(init_temp: float,
                    room_temp: float,) -> Tuple[float, float, float]:
    """Simulate the time taken to cool to within 1 degree of room temperature
    for the given initial and room temperatures."""
    k_value = CONV_HEAT_TRANS_COEF * SURF_AREA / (MASS * SPEC_HEAT_CAP)
    t = np.linspace(0, SIM_LEN, SIM_STEPS)
    T = odeint(model, init_temp, t, args=(k_value, room_temp))
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
        (init_temp, room_temp)
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
                 time_grid: np.ndarray) -> None:
    """Plot the simulation results."""
    # Create a new figure for display
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(211, 
                         projection='3d',
                         proj_type='ortho',
                         azim=-120,
                         elev=30,
                         box_aspect=(1,1,1))
    # Draw the surface plot
    ax.plot_surface(init_grid,
                    room_grid,
                    time_grid,
                    cmap='coolwarm',
                    linewidth=0,
                    antialiased=True)
    ax.set_xlabel('Initial Temperature (°C)')
    ax.set_ylabel('Room Temperature (°C)')
    ax.set_zlabel('Time to cool to within 1 degree of room temperature')
    ax.zaxis.set_major_formatter(ticker.FuncFormatter(format_func))

    # Save the surface plot
    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111, 
                         projection='3d',
                         proj_type='ortho',
                         azim=-120,
                         elev=30,
                         box_aspect=(1,1,1))
    ax2.plot_surface(init_grid,
                    room_grid,
                    time_grid,
                    cmap='coolwarm',
                    linewidth=0,
                    antialiased=True)
    ax2.set_xlabel('Initial Temperature (°C)')
    ax2.set_ylabel('Room Temperature (°C)')
    ax2.set_zlabel('Time to cool to within 1 degree of room temperature')
    ax2.zaxis.set_major_formatter(ticker.FuncFormatter(format_func))
    fig2.savefig("3d_plot.png")
    plt.close(fig2)

    # Draw the contour plot
    ax3 = fig.add_subplot(212)
    xlim = [INIT_TEMP_L, INIT_TEMP_H]
    ylim = [INIT_TEMP_H, ROOM_TEMP_H]
    ax3.set_xlim(xlim)
    ax3.set_ylim(ylim)
    mask = (init_grid >= xlim[0]) & (init_grid <= xlim[1]) & \
        (room_grid >= ylim[0]) & (room_grid <= ylim[1])
    time_grid_filtered = np.where(mask, time_grid, np.nan)
    contour_levels = np.arange(0, 10000, 500)
    contour_fill = ax3.contourf(init_grid,
                                room_grid,
                                time_grid_filtered,
                                levels=contour_levels,
                                cmap='coolwarm')
    contour_lines = ax3.contour(init_grid,
                                room_grid,
                                time_grid_filtered,
                                levels=contour_levels,
                                colors='k')
    ax3.set_xlabel('Initial Temperature (°C)')
    ax3.set_ylabel('Room Temperature (°C)')
    ax3.clabel(contour_lines,
               inline=1,
               fontsize=10,
               fmt=ticker.FuncFormatter(format_func))
    colorbar = fig.colorbar(contour_fill,
                            ax=ax3,
                            format=ticker.FuncFormatter(format_func))

    # Save the contour plot
    fig4 = plt.figure()
    ax4 = fig4.add_subplot(111)
    ax4.set_xlim(xlim)
    ax4.set_ylim(ylim)
    contour_fill_2 = ax4.contourf(init_grid,
                                room_grid,
                                time_grid_filtered,
                                levels=contour_levels,
                                cmap='coolwarm')
    contour_lines_2 = ax4.contour(init_grid,
                                room_grid,
                                time_grid_filtered,
                                levels=contour_levels,
                                colors='k')
    ax4.set_xlabel('Initial Temperature (°C)')
    ax4.set_ylabel('Room Temperature (°C)')
    ax4.clabel(contour_lines_2,
               inline=1,
               fontsize=10,
               fmt=ticker.FuncFormatter(format_func))
    colorbar_2 = fig4.colorbar(contour_fill_2,
                            ax=ax4,
                            format=ticker.FuncFormatter(format_func))
    fig4.savefig("contour_plot.png")
    plt.close(fig4)

    fig.tight_layout()
    plt.show()


def main() -> None:
    """Main function for the program."""
    # Create a 2D grid of initial and room temperatures
    init_temps = np.linspace(INIT_TEMP_L, INIT_TEMP_H, 100)
    room_temps = np.linspace(ROOM_TEMP_L, ROOM_TEMP_H, 100)
    init_grid, room_grid = np.meshgrid(init_temps, room_temps)

    # Perform the simulation
    time_grid = perform_simulation(init_temps, room_temps)

    # Plot the simulation results
    plot_results(init_grid, room_grid, time_grid)


if __name__ == "__main__":
    main()
