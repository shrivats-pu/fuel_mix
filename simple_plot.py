
import os
import sys

from gridstatusio import GridStatusClient
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, UTC
API_KEY = os.getenv("MY_API_KEY")
if not API_KEY:
    sys.exit("ERROR: MY_API_KEY not set")
    DATE = "2025-01-01"

# this is a simple little script to grab data via gridstatusio and make an image of it, which I host on a GitHub Page
# and allow my TRMNL screen to ping. This is functionally useless, as this same info exists elsewhere. This is basically
# a 'hello world' for me to learn a little bit more about various self-hosting options and use cases for my TRMNL device
def main():
    client = GridStatusClient(api_key=API_KEY)
    dataset = client.get_dataset(dataset="pjm_fuel_mix_hourly", start=DATE)

    end_date = datetime.now(tz=UTC)
    start_date = end_date - timedelta(hours=24)
    relevant_dataset = dataset[dataset['interval_end_utc'].lt(end_date) & 
                            dataset['interval_start_utc'].gt(start_date)]

    plt.figure(figsize=(10, 6))
    markers = ['o', 's', '^', 'D', 'v', 'p']
    for fuel in ['coal', 'gas', 'hydro', 'nuclear', 'solar', 'wind']:
        i = ['coal', 'gas', 'hydro', 'nuclear', 'solar', 'wind'].index(fuel)
        plt.plot(relevant_dataset['interval_start_utc'], relevant_dataset[fuel],
                linestyle='',
                marker=markers[i],
                markersize=5,
                label=fuel.capitalize())
    plt.xlabel('Time')
    plt.ylabel('Fuel Mix Value')
    plt.title('PJM Fuel Mix Over Last 24 Hours ')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.gcf().set_size_inches(8, 4.8)
    plt.savefig("docs/fuel_mix.png", dpi=100)

if __name__ == '__main__':
    main()
