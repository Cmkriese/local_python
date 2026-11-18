
### Import Statements

import matplotlib.pyplot as plt
import numpy as np
import csv
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
    plt.savefig("provo_streamflow.png", dpi=150, bbox_inches="tight")
    colors = ['red', 'blue', 'green', 'orange', 'purple']
    for flow, site, color in zip(flows.T, sites, colors):
        plt.plot(dates, flow, color=color, label=f'Site {site}')
    plt.xlabel('Date')
    plt.ylabel('Flowrate (cfs)')
    plt.title('Provo River Streamflow Data (2021)')

    plt.gcf().autofmt_xdate()
    plt.legend(title='Site Numbers')
    plt.show()


def summarize(dates, flows, sites):
    #I did get the values of 131 for the max and 57 for the average. 
    """Print and save maximum, minimum, and average flow for each gauge."""
    if flows.shape[1] != len(sites) or len(dates) != flows.shape[0]:
        raise ValueError("The dates, flows, and sites do not have matching dimensions.")

    header = (
        f"{'Gauge':<12}{'Max (cfs)':>12}{'Date of max':>20}"
        f"{'Min (cfs)':>12}{'Avg (cfs)':>12}"
    )
    print(header)
    print("-" * len(header))

    summary_rows = []
    for column, site in enumerate(sites):
        gauge_flows = flows[:, column]
        max_index = int(np.argmax(gauge_flows))
        max_flow = np.max(gauge_flows)
        min_flow = np.min(gauge_flows)
        average_flow = np.mean(gauge_flows)
        max_date = dates[max_index]

        print(
            f"{site:<12}{max_flow:>12.1f}{max_date.strftime('%Y-%m-%d %H:%M'):>20}"
            f"{min_flow:>12.1f}{average_flow:>12.1f}"
        )
        summary_rows.append([
            site,
            f"{max_flow:.1f}",
            max_date.strftime('%Y-%m-%d %H:%M'),
            f"{min_flow:.1f}",
            f"{average_flow:.1f}",
        ])

    summary_file = Path(__file__).with_name("streamflow_summary.csv")
    with summary_file.open("w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Gauge", "Max (cfs)", "Date of max", "Min (cfs)", "Avg (cfs)"])
        writer.writerows(summary_rows)


# Main program
sites = ["10163000", "10155200", "10155500", "10154200", "10155000"]
dates, flows = load_streamflow(data_file)
plot_streamflow(dates, flows, sites)
summarize(dates, flows, sites)