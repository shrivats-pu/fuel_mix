#%%
from gridstatusio import GridStatusClient
import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, UTC
import time

client = GridStatusClient(api_key="dadb3f841dd24920a1394b78aa2b713d")
while True:
    dataset = client.get_dataset(dataset="pjm_fuel_mix_hourly", start="2025-01-01")

    end_date = datetime.now(tz=UTC)
    start_date = end_date - timedelta(hours=24)
    relevant_dataset = dataset[dataset['interval_end_utc'].lt(end_date) & 
                            dataset['interval_start_utc'].gt(start_date)]

    plt.figure(figsize=(10, 6))
    linestyles = ['', '--', '-.', ':',]
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
    plt.title('PJM Fuel Mix Over Last 24 Hours')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('docs/pjm_fuel_mix.png', dpi=300)
    time.sleep(3600)

#%%
