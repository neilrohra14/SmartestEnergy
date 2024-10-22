import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for rendering
import matplotlib.pyplot as plt
from src.utils.utils import save_cleaned_data_to_excel
from src.logger import logging  
from src.exception import CustomException

class AnalyseData:
    def __init__(self, cleaned_df):
        self.cleaned_df = cleaned_df

    def generate_time_series_chart(self):
        try:
            self.cleaned_df.set_index('startTime', inplace=True)

            plt.figure(figsize=(10, 6))
            plt.plot(self.cleaned_df.index, self.cleaned_df['systemSellPrice'], label='System Sell Price', color='blue')
            plt.plot(self.cleaned_df.index, self.cleaned_df['systemBuyPrice'], label='System Buy Price', color='green')
            plt.plot(self.cleaned_df.index, self.cleaned_df['netImbalanceVolume'], label='Net Imbalance Volume', color='red')

            plt.title('Time Series of Prices and Imbalance Volume')
            plt.xlabel('Time (Half-hourly)')
            plt.ylabel('Value')
            plt.legend(loc='upper left')
            plt.xticks(rotation=45)
            plt.tight_layout()

            combined_image_path = 'timeseries_combined.png'
            plt.savefig(combined_image_path)
            plt.close()

            system_sell_image_path = self._generate_individual_time_series('systemSellPrice', 'System Sell Price', 'blue')
            system_buy_image_path = self._generate_individual_time_series('systemBuyPrice', 'System Buy Price', 'green')
            imbalance_volume_image_path = self._generate_individual_time_series('netImbalanceVolume', 'Net Imbalance Volume', 'red')

            logging.info(f"Time series charts saved at {combined_image_path}, {system_sell_image_path}, {system_buy_image_path}, and {imbalance_volume_image_path}.")
            return combined_image_path, system_sell_image_path, system_buy_image_path, imbalance_volume_image_path

        except Exception as e:
            logging.error(f"Failed to generate time series chart: {str(e)}")
            raise CustomException(f"Error generating time series chart: {str(e)}")

    def _generate_individual_time_series(self, column_name, title, color):
        plt.figure(figsize=(10, 6))
        plt.plot(self.cleaned_df.index, self.cleaned_df[column_name], label=title, color=color)

        plt.title(f'Time Series of {title}')
        plt.xlabel('Time (Half-hourly)')
        plt.ylabel('Value')
        plt.xticks(rotation=45)
        plt.tight_layout()

        image_path = f'timeseries_{column_name}.png'
        plt.savefig(image_path)
        plt.close()

        return image_path

    def save_chart_to_excel(self, target_date):
        try:
            combined_image_path, system_sell_image_path, system_buy_image_path, imbalance_volume_image_path = self.generate_time_series_chart()

            df_for_chart = pd.DataFrame({'Chart': ['Time series charts are added here. See the images below.']})

            save_cleaned_data_to_excel(df_for_chart, target_date, sheet_name='timeseries', image_paths=[
                combined_image_path, system_sell_image_path, system_buy_image_path, imbalance_volume_image_path
            ])

            logging.info(f"Time series charts for {target_date} saved in Excel.")
        except CustomException as e:
            logging.error(f"Failed to save chart to Excel: {str(e)}")
            raise CustomException(f"Error saving chart to Excel: {str(e)}")
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            raise CustomException(f"Unexpected error occurred: {str(e)}")

    def generate_imbalance_summary(self):
        try:

            self.cleaned_df['imbalance_cost'] = self.cleaned_df.apply(
                lambda row: abs(row['netImbalanceVolume']) * (row['systemSellPrice'] if row['netImbalanceVolume'] > 0 else row['systemBuyPrice']),
                axis=1
            )

            total_imbalance_cost = self.cleaned_df['imbalance_cost'].sum()
            total_volume = self.cleaned_df['netImbalanceVolume'].abs().sum()

            daily_unit_rate = total_imbalance_cost / total_volume if total_volume != 0 else 0

            self.cleaned_df['hour'] = self.cleaned_df.index.hour
            hourly_imbalance_volume = self.cleaned_df.groupby('hour')['netImbalanceVolume'].sum().abs()
            highest_imbalance_hour = hourly_imbalance_volume.idxmax()
            highest_imbalance_volume = hourly_imbalance_volume.max()

            summary_data = {
                'Total Daily Imbalance Cost': [total_imbalance_cost],
                'Daily Imbalance Unit Rate': [daily_unit_rate],
                'Hour with Highest Imbalance Volume': [highest_imbalance_hour],
                'Highest Imbalance Volume': [highest_imbalance_volume]
            }

            summary_df = pd.DataFrame(summary_data)

            return summary_df

        except Exception as e:
            logging.error(f"Failed to generate imbalance summary: {str(e)}")
            raise CustomException(f"Error generating imbalance summary: {str(e)}")

    def save_summary_to_excel(self, target_date):
        try:
            summary_df = self.generate_imbalance_summary()

            save_cleaned_data_to_excel(summary_df, target_date, sheet_name='imbalance_summary')

            logging.info(f"Imbalance summary for {target_date} saved in Excel.")
        except CustomException as e:
            logging.error(f"Failed to save imbalance summary to Excel: {str(e)}")
            raise CustomException(f"Error saving imbalance summary to Excel: {str(e)}")
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            raise CustomException(f"Unexpected error occurred: {str(e)}")
