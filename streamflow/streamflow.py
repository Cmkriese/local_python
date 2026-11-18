
### Import Statements

import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from pathlib import Path

data_file = Path(__file__).with_name('June-2021-Provo-River-Streamflow-Rates (1).csv')


def load_streamflow(filename):
    """Read the streamflow CSV. Return the dates and a 2D array of flows (cfs), one column per gauge."""
    data_path = Path(filename)
    if not data_path.is_absolute():
        data_path = Path(__file__).with_name(filename)

    array2 = np.genfromtxt(data_path, delimiter=',', dtype=str, skip_header=1)
    dates = [
        datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        for date in array2[:, 0]
    ]
    flows = array2[:, 1:].astype(float)
    return dates, flows


def plot_streamflow(dates, flows, sites):
    """Plot the flow at each gauge, with the same title, labels, and formatting as the Matplotlib HW."""
    colors = ['red', 'blue', 'green', 'orange', 'purple']
    for flow, site, color in zip(flows.T, sites, colors):
        plt.plot(dates, flow, color=color, label=f'Site {site}')
    plt.xlabel('Date')
    plt.ylabel('Flowrate (cfs)')
    plt.title('Provo River Streamflow Data (2021)')

    plt.gcf().autofmt_xdate()
    plt.legend(title='Site Numbers')
    plt.show()


# Main program
sites = ["10163000", "10155200", "10155500", "10154200", "10155000"]
dates, flows = load_streamflow(data_file)
plot_streamflow(dates, flows, sites)