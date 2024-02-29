from src.reader import fetch_data
from src.data_processing import apply_median_filter, convert_timestamps_to_datetime, calculate_sampling_rate, \
    reformat_data, process_data_for_pv
from src.anomaly_functions import find_anomalies_std
import matplotlib.pyplot as plt

PV_LIST = [
    "LabS-MCAG:MC-MCU-06:PTPOffset",
    "LabS-MCAG:MC-MCU-07:PTPOffset",
    "LabS-MCAG:MC-MCU-035:PTPOffset",
]

MEDIAN_FILTER_TIME = 200  # seconds
MIN_ANOMALY_DISTANCE = 120  # seconds
START_TIME = "2024-02-28T12:00:00.000"
END_TIME = "2024-02-29T12:00:00.000"


def main():
    plt.figure(figsize=(10, 6))  # Optional: Adjust figure size
    for pv in PV_LIST:
        data = fetch_data(pv, START_TIME, END_TIME)
        result = process_data_for_pv(pv, data, MEDIAN_FILTER_TIME, MIN_ANOMALY_DISTANCE)
        if result:
            ts_dt, vals, vals_filtered, anomalies = result
            plt.plot(ts_dt, vals, label=pv)
            # Optionally, plot anomalies or filtered values

    plt.legend()
    plt.title("PV Values Over Time")
    plt.xlabel("Time")
    plt.ylabel("Values")
    plt.show()


if __name__ == "__main__":
    main()
