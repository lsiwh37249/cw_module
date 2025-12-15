import pandas as pd

class De:
    def __init__(self, mbc_path):  
        self.mbc_path = mbc_path

    def get_empty_project_type(self):
        mbc_share_data_raw_df = pd.read_csv(self.mbc_path)
        mbc_share_data_raw_df_agg =  mbc_share_data_raw_df.groupby('project_id').agg(
            project_name=("project_name", "first"),
            project_type=("project_type", "first"),
        )
        print(mbc_share_data_raw_df_agg)

        print("is empty:", mbc_share_data_raw_df_agg.empty)
if __name__ == "__main__":
    mbc_path = "/mnt/c/Users/김령래/Desktop/cw_app/mbc_share/mbc_share_data_20251201_090525.csv"

    De = De(mbc_path)
    De.get_empty_project_type()