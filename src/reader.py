from typing import Optional, Dict, Any
import requests


def fetch_data(pv_name: str, start_time: str, end_time: str) -> Optional[Dict[str, Any]]:
    """
    Fetches and returns data for a specified process variable (pv_name) within the given time range.

    Parameters:
    - pv_name: Name of the process variable.
    - start_time: Start of the time range in ISO 8601 format, excluding the 'Z' (e.g., '2024-02-29T13:00:00.000').
    - end_time: End of the time range in ISO 8601 format, excluding the 'Z' (e.g., '2024-02-29T13:20:00.000').

    Returns:
    - A dictionary of the fetched data if successful; None otherwise.
    """
    base_url = "http://172.30.38.34:17668/retrieval/data/getData.json"
    params = {
        'pv': pv_name,
        'from': f"{start_time}Z",
        'to': f"{end_time}Z"
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raises an HTTPError if the response was an error
        return response.json()[0]
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.RequestException as err:
        print(f"An error occurred while fetching the data: {err}")
    return None


if __name__ == "__main__":
    # Example usage
    pv_name = "LabS-MCAG:MC-MCU-035:PTPOffset"
    start_time = "2024-02-29T12:00:00.000"
    end_time = "2024-02-29T13:20:00.000"
    data = fetch_data(pv_name, start_time, end_time)

    if data is not None:
        print("Data successfully fetched. Here's a preview:")
        print(data)  # Adjust based on the structure of 'data'
    else:
        print("Failed to fetch data.")
