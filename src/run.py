from src.reader import fetch_data
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from scipy.ndimage import median_filter

PV_LIST = [
    "LabS-MCAG:MC-MCU-06:PTPOffset",
    "LabS-MCAG:MC-MCU-07:PTPOffset",
    "LabS-MCAG:MC-MCU-035:PTPOffset",
]

MEDIAN_FILTER_TIME = 200  # seconds
MIN_ANOMALY_DISTANCE = 120  # seconds
START_TIME = "2024-02-28T12:00:00.000"
END_TIME = "2024-02-29T12:00:00.000"


def reformat_data(data):
    ts = np.array([x["secs"] for x in data["data"]])
    vals = np.array([x["val"] for x in data["data"]])
    return ts, vals


def find_anomalies(ts, vals, vals_filtered, threshold_factor=3):
    """
    Identifies anomalies based on deviations from the median-filtered data.

    Parameters:
    - ts: Timestamps of the data points.
    - vals: Original values.
    - vals_filtered: Median-filtered values.
    - threshold_factor: Factor to multiply by the standard deviation to set the threshold.

    Returns:
    - A list of tuples, each representing the start and end times of detected anomalies.
    """
    # Calculate the absolute difference between original and filtered values
    diffs = np.abs(vals - vals_filtered)

    # Determine the threshold for detecting anomalies
    threshold = np.mean(diffs) + threshold_factor * np.std(diffs)

    # Identify where the difference exceeds the threshold
    anomalies = diffs > threshold

    # Group anomalies
    anomaly_indices = np.where(anomalies)[0]
    groups = np.split(anomaly_indices, np.where(np.diff(anomaly_indices) != 1)[0] + 1)

    # Extract start and end times for each group
    anomaly_periods = [(ts[g[0]], ts[g[-1]]) for g in groups if len(g) > 0]

    # cluster groups that are close together
    final_anomaly_periods = []
    for start, end in anomaly_periods:
        if len(final_anomaly_periods) == 0:
            final_anomaly_periods.append((start, end))
        else:
            last_start, last_end = final_anomaly_periods[-1]
            if start - last_end < MIN_ANOMALY_DISTANCE:
                final_anomaly_periods[-1] = (last_start, end)
            else:
                final_anomaly_periods.append((start, end))

    return final_anomaly_periods


def main():
    all_data = {}
    for pv in PV_LIST:
        data = fetch_data(pv, START_TIME, END_TIME)

        if data is not None:
            ts, vals = reformat_data(data)
            all_data[data["meta"]["name"]] = {}
            all_data[data["meta"]["name"]]["ts"] = ts
            all_data[data["meta"]["name"]]["vals"] = vals
            print(f"Data successfully fetched for {pv}.")
        else:
            print(f"Failed to fetch data for {pv}.")

    for pv, data in all_data.items():
        estimated_sampling_rate = (data["ts"][-1] - data["ts"][0]) / len(data["ts"])
        median_filter_size = int(MEDIAN_FILTER_TIME / estimated_sampling_rate)
        all_data[pv]["ts_dt"] = [datetime.utcfromtimestamp(x) for x in data["ts"]]
        all_data[pv]["vals_filtered"] = median_filter(data["vals"], size=median_filter_size)
        print(f"Data for {pv} has been reformatted with a median filter of size {median_filter_size}.")

    for pv, data in all_data.items():
        anomalies = find_anomalies(data["ts"], data["vals"], data["vals_filtered"])
        all_data[pv]["anomalies"] = anomalies

        print(f"Found {len(anomalies)} anomalies for {pv}.")
        for start, end in anomalies:
            print(f"Anomaly from {datetime.utcfromtimestamp(start)} to {datetime.utcfromtimestamp(end)}. for {pv}")
        plt.plot(data["ts_dt"], data["vals"], label=pv)

    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()

