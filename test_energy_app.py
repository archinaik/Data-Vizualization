import unittest
import os
import pandas as pd
from energy_app import EnergyApp

class EnergyAppTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.sample_folder = "test_data"
        os.makedirs(cls.sample_folder, exist_ok=True)

        timestamps = [1000, 2000, 3000]

        pd.DataFrame({'ts': timestamps, 'value': [1, 2, 3]}).to_csv(
            os.path.join(cls.sample_folder, "Current.csv"), index=False, header=False
        )
        pd.DataFrame({'ts': timestamps, 'value': [10, 20, 30]}).to_csv(
            os.path.join(cls.sample_folder, "Energy.csv"), index=False, header=False
        )
        pd.DataFrame({'ts': timestamps, 'value': [100, 200, 300]}).to_csv(
            os.path.join(cls.sample_folder, "Power.csv"), index=False, header=False
        )

    @classmethod
    def tearDownClass(cls):
        import shutil
        shutil.rmtree(cls.sample_folder)

    def test_data_loading_merging(self):
        app = EnergyApp(url="")
        app.extract_path = self.sample_folder
        df = app.load_and_process_data()

        self.assertEqual(df.shape[0], 3, "Expected 3 rows after merging CSVs")
        self.assertEqual(df.shape[1], 4, "Expected 4 columns: timestamp + 3 types")
        for col in ["current", "energy", "power", "local_timestamp"]:
            self.assertIn(col, df.columns, f"Missing expected column: {col}")

    def test_plot_creation(self):
        app = EnergyApp(url="")
        app.extract_path = self.sample_folder
        app.load_and_process_data()
        app.visualize_data()

        plot_file = "energy_plot.jpeg"
        self.assertTrue(os.path.exists(plot_file), f"{plot_file} was not created")
        os.remove(plot_file)


if __name__ == "__main__":
    print("Running EnergyApp tests...")
    unittest.main()
