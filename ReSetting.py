import pandas as pd
from datetime import datetime

class ReSetting:
    def __init__(self, path):
        self.df = pd.read_csv(path)
        self.output_df = None
        self.object_df = None

    def remove_resset_object_data(self):
        self.object_df = pd.read_csv('/home/kim/app/airflow/data/source/resetted/251211_객체_재세팅_파일리스트.csv')
        print(self.output_df[self.output_df['file_name'].isin(self.object_df['file_name'])])
        self.output_df = self.output_df[~self.output_df['file_name'].isin(self.object_df['file_name'])]

    def set_project_id(self, project_id_list, project_id, project_type, organization_id):
        self.output_df = self.df[self.df['project_id'].isin(project_id_list)]
        self.output_df = self.output_df[self.output_df['is_label_upload'] == 1]
        self.output_df = self.output_df[['file_name','project_id']].copy()
        
        self.remove_resset_object_data()
        self.agg_data()
        # project_id를 project_id_old로 rename
        self.output_df.rename(columns={'project_id': 'project_id_old'}, inplace=True)
        # 새로운 컬럼들 추가
        self.output_df['project_type'] = project_type
        self.output_df['project_id'] = project_id
        self.output_df['organization_id'] = organization_id

    def agg_data(self):
        df = self.output_df
        print(df.groupby('project_id').size())


if __name__ == "__main__":
    project_id_list = [26668, 26669, 26579] + [26982, 27009, 27010, 27047, 27064]
    project_type = 'object'
    project_id = 27108
    organization_id =1070
    path = "/mnt/c/Users/김령래/Desktop/cw_app/mbc_share/mbc_share_data_20251209_190527.csv"
    re_setting = ReSetting(path)
    re_setting.set_project_id(project_id_list, project_id, project_type, organization_id)
    re_setting.output_df.to_csv(f'../data/result/{datetime.now().strftime("%Y%m%d")}_resettingoutput.csv', index=False)