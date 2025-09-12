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

    def find_csv_files(self):
        print('Searching for relevant CSV files...')
        base_path = os.path.join(self.extract_path, 'iiitd', 'Lecture Block', 'AHU-1')
        all_csv_files = []
        for root, _, files in os.walk(base_path):
            for file in files:
                if file.endswith('.csv'):
                    all_csv_files.append(os.path.join(root, file))
        print(f'Found {len(all_csv_files)} CSV files under AHU-1')
        return all_csv_files

    def load_and_process_data(self):
        csv_files = self.find_csv_files()
        data_frames = []

        for file in csv_files:
            # Properly read header-less CSV files
            df = pd.read_csv(file, header=None, names=['ts', 'value'])

            print(f"Columns in {os.path.basename(file)}: {list(df.columns)}")

            column_type = os.path.basename(file).split('.')[0].lower()  # current/energy/power

            # Rename column for clarity
            df = df.rename(columns={'value': column_type})

            # Convert timestamp from milliseconds to local datetime
            df['ts'] = pd.to_datetime(df['ts'], unit='ms') + timedelta(hours=5, minutes=30)

            data_frames.append(df[['ts', column_type]])

        if not data_frames:
            raise ValueError('No CSV data was processed.')

        # Merge dataframes on timestamp
        merged_df = data_frames[0]
        for df in data_frames[1:]:
            merged_df = pd.merge(merged_df, df, on='ts')

        self.df = merged_df.rename(columns={'ts': 'local_timestamp'})
        print(f'Processed data rows: {len(self.df)}')
        return self.df

    def visualize_data(self):
        print('Plotting data...')
        plt.figure(figsize=(12, 6))
        plt.plot(self.df['local_timestamp'], self.df['current'], label='Current (A)')
        plt.plot(self.df['local_timestamp'], self.df['power'], label='Power (kW)')
        plt.plot(self.df['local_timestamp'], self.df['energy'], label='Energy (kWh)')
        plt.xlabel('Local Timestamp')
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
