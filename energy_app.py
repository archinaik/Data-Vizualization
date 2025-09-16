import requests
import zipfile
import os
import pandas as pd
from datetime import timedelta
import matplotlib.pyplot as plt


class EnergyApp:
    """Class to download, process, and visualize energy data for AHU-1."""

    def __init__(self, url):
        """Initialize with the URL of the ZIP file containing CSVs."""
        self.url = url
        self.download_path = 'combed.zip'
        self.extract_path = 'data'
        self.df = None

    def download_and_extract(self):
        """Download the ZIP file and extract its contents."""
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
        """Find all CSV files under AHU-1 folder."""
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
        """Load CSVs, convert timestamps, rename columns, and merge into one DataFrame."""
        csv_files = self.find_csv_files()
        data_frames = []

        for file in csv_files:
            # Read CSV without headers
            df = pd.read_csv(file, header=None, names=['ts', 'value'])
            print(f"Columns in {os.path.basename(file)}: {list(df.columns)}")

            # Determine type from filename (current/energy/power)
            column_type = os.path.basename(file).split('.')[0].lower()

            # Rename value column
            df = df.rename(columns={'value': column_type})

            # Convert timestamp from ms to datetime + IST offset
            df['ts'] = pd.to_datetime(df['ts'], unit='ms') + timedelta(hours=5, minutes=30)

            # Keep only timestamp and the value column
            data_frames.append(df[['ts', column_type]])

        if not data_frames:
            raise ValueError('No CSV data was processed.')

        # # Merge all dataframes on timestamp
        # merged_df = data_frames[0]
        # for df in data_frames[1:]:
        #     print(df.shape)
        #     merged_df = pd.merge(merged_df, df, on='ts')


        merged_df = pd.DataFrame()  # start with empty DataFrame

        for df in data_frames:
            print(df.shape)
            if merged_df.empty:
                merged_df = df.copy()   # first df becomes the base
            else:
                merged_df = pd.merge(merged_df, df, on='ts')

        self.df = merged_df.rename(columns={'ts': 'local_timestamp'})
        print(merged_df.shape)
        print(f'Processed data rows: {len(self.df)}')
        return self.df

    def visualize_data(self):
        """Plot Current, Power, and Energy over local timestamps."""
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
    """Main function to run the app."""
    data_url = 'http://combed.github.io/downloads/combed.zip'
    app = EnergyApp(data_url)

    app.download_and_extract()
    app.load_and_process_data()
    app.visualize_data()


if __name__ == '__main__':
    main()
