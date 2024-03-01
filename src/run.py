import os
import sys
import matplotlib.pyplot as plt

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(script_dir, '..')
sys.path.append(project_root)

from src.reader import fetch_data
from src.data_processing import process_data_for_pv


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
