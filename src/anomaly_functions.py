import numpy as np


def find_anomalies_std(ts, vals, vals_filtered, min_anomaly_distance=60, threshold_factor=3):
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
            if start - last_end < min_anomaly_distance:
                final_anomaly_periods[-1] = (last_start, end)
            else:
                final_anomaly_periods.append((start, end))

    return final_anomaly_periods