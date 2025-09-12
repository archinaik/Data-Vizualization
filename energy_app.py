
"""
Energy consumption visualization for 'Lecture Block\\AHU-1'.
Processes CSV data and plots Current, Energy, and Power curves.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class EnergyApp:
    """Class to handle processing and visualizing energy data."""

    def __init__(self, data_path="data/Lecture Block\\AHU-1"):
        """
        Initialize EnergyApp.

        Args:
            data_path (str): Folder containing CSV files for AHU-1.
        """
        self.data_path = data_path
        self.df = None

    def load_ahu1_data(self):
        """Load all CSV files in the folder and merge into one DataFrame."""
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"{self.data_path} does not exist")

        dfs = []
        print("Searching for CSV files...")
        for csv_file in os.listdir(self.data_path):
            if csv_file.endswith(".csv"):
                file_path = os.path.join(self.data_path, csv_file)
                df = pd.read_csv(file_path)
                type_name = csv_file.replace('.csv', '')
                df = df.rename(columns={'value': type_name})
                dfs.append(df)
                print(f"Found {csv_file}, columns: {df.columns.tolist()}")

        if not dfs:
            raise ValueError("No CSV files found in the folder.")

        # Merge all dataframes on timestamp
        merged_df = dfs[0]
        for df in dfs[1:]:
            merged_df = pd.merge(merged_df, df, on='ts')
        self.df = merged_df
        print(f"Processed data rows: {len(self.df)}")

    def process_timestamps(self):
        """Convert timestamp column to datetime and local time."""
        if self.df is None:
            raise ValueError("Data not loaded. Run load_ahu1_data() first.")

        self.df['ts'] = pd.to_datetime(self.df['ts'])
        self.df['ts_local'] = self.df['ts'] + pd.to_timedelta(5.5, unit='h')  # IST offset

    def plot_data(self, save_path="energy_plot.jpeg"):
        """Plot all energy-related columns and save to file."""
        if self.df is None:
            raise ValueError("Data not loaded. Run load_ahu1_data() first.")

        plt.figure(figsize=(12, 6))
        # Plot all columns except timestamps
        for col in self.df.columns:
            if col not in ['ts', 'ts_local']:
                plt.plot(self.df['ts_local'], self.df[col], label=col)

        plt.xlabel("Time")
        plt.ylabel("Value")
        plt.title("AHU-1 Energy Consumption")
        plt.legend()
        plt.tight_layout()
        plt.savefig(save_path)
        print(f"Plot saved as {save_path}")


def main():
    """Main function to run the EnergyApp."""
    app = EnergyApp(data_path="data/Lecture Block\\AHU-1")  # Replace with your local CSV folder
    app.load_ahu1_data()
    app.process_timestamps()
    app.plot_data()


if __name__ == "__main__":
    main()
