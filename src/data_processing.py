from scipy.ndimage import median_filter
from datetime import datetime
import numpy as np

from src.anomaly_functions import find_anomalies_std
from src.reader import fetch_data


def apply_median_filter(vals, sampling_rate, filter_time=200):
    filter_size = int(filter_time / sampling_rate)
    return median_filter(vals, size=filter_size)


def convert_timestamps_to_datetime(ts):
    if isinstance(ts, list) or isinstance(ts, np.ndarray):
        return [datetime.utcfromtimestamp(x) for x in ts]
    return datetime.utcfromtimestamp(ts)


def calculate_sampling_rate(ts):
    return (ts[-1] - ts[0]) / len(ts)


def reformat_data(data):
    ts = np.array([x["secs"] for x in data["data"]])
    vals = np.array([x["val"] for x in data["data"]])
    return ts, vals


def process_data_for_pv(pv, data, median_filter_time=60, min_anomaly_distance=60):
    if data is None:
        return None

    ts, vals = reformat_data(data)
    sampling_rate = calculate_sampling_rate(ts)
    vals_filtered = apply_median_filter(vals, sampling_rate, median_filter_time)
    ts_dt = convert_timestamps_to_datetime(ts)
    anomalies = find_anomalies_std(ts, vals, vals_filtered, min_anomaly_distance)

    print(f"Data successfully processed for {pv}. Found {len(anomalies)} anomalies.")
    for start, end in anomalies:
        print(f"Anomaly from {convert_timestamps_to_datetime(start)} to {convert_timestamps_to_datetime(end)}. for {pv}")
    return ts_dt, vals, vals_filtered, anomalies
