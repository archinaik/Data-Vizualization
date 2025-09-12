import requests
import zipfile
import os
import pandas as pd
from datetime import timedelta
import matplotlib.pyplot as plt

class EnergyApp:
    def __init__(self, url):
        self.url = url
        self.download_path = 'combed.zip'
        self.extract_path = 'data'
        self.csv_file = os.path.join(self.extract_path, 'combed.csv')
        self.df = None

    def download_and_extract(self):
        print('Downloading data...')
        response = requests.get(self.url)
        response.raise_for_status()
        with open(self.download_path, 'wb') as f:
            f.write(response.content)
        print('Download finished.')

        print('Extracting files...')
        if not os.path.exists(self.extract_path):
            os.makedirs(self.extract_path)
        with zipfile.ZipFile(self.download_path, 'r') as zip_ref:
            zip_ref.extractall(self.extract_path)
        print('Extraction finished.')

    def load_and_process_data(self):
        print('Loading and processing data...')
        self.df = pd.read_csv(self.csv_file)
        self.df['local_timestamp'] = pd.to_datetime(self.df['timestamp'], unit='s') + timedelta(hours=5, minutes=30)
        self.df = self.df[self.df['node'] == 'Lecture Block\\AHU-1']
        print(f'Filtered data rows: {len(self.df)}')
        return self.df

    def visualize_data(self):
        print('Plotting data...')
        plt.figure(figsize=(12, 6))
        plt.plot(self.df['local_timestamp'], self.df['current'], label='Current (A)')
        plt.plot(self.df['local_timestamp'], self.df['power'], label='Power (kW)')
        plt.plot(self.df['local_timestamp'], self.df['energy'], label='Energy (kWh)')
        plt.xlabel('Local Time')
        plt.ylabel('Measurements')
        plt.title('Energy Data for Lecture Block\\AHU-1')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('energy_plot.jpeg')
        print('Plot saved as energy_plot.jpeg')
        plt.close()


def main():
    data_url = 'http://combed.github.io/downloads/combed.zip'
    app = EnergyApp(data_url)

    app.download_and_extract()
    app.load_and_process_data()
    app.visualize_data()


if __name__ == '__main__':
    main()
