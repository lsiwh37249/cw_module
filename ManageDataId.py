## source data : mbc_share_data(납품 데이터 여부, 프로젝트 정보), /home/kim/code/gcs/cache/blobs_cache.pkl(업로드 날짜,차수(인덱스))
## target data : ./result/납품 현황.csv
## 모듈 역할 : 데이터 현황 파악을 위한 기본 테이블 생성
## 활용 방안1 : 업로드 날짜별 데이터 수량 파악
## 활용 방안2 : 프로젝트별 데이터 수량 파악
## 활용 방안3 : 작업 불가 여부 수량 확인 및 데이터 추출
## 목표 : 어떤 데이터를 추가로 업로드 가능한지에 대한 정보 바로 획득득

import pandas as pd
import sys
import os

# Try absolute import first (when used as a module)
try:
    from modules.Gcloud import Gcloud
except ImportError:
    # Fallback: add parent directory to path for direct script execution
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    from modules.Gcloud import Gcloud



class ManageDataId:
    def __init__(self, mbc_path):
        self.mbc_share_data_raw_df = None
        self.mbc_share_data_df = None
        self.blobs_cache_df= None
        self.base_table = None
        self.base_table_grouped_by_date = None
        self.base_table_grouped_by_project = None
        self.problem_df = None
        self.mbc_path = mbc_path

    def l_load_data(self):
        # 납품 데이터 여부, 프로젝트 정보 로드
        self.mbc_share_data_raw_df = pd.read_csv(self.mbc_path)
        self.mbc_share_data_raw_df = self.mbc_share_data_raw_df[~self.mbc_share_data_raw_df['project_id'].isin([27017,26945])]
        
        
        #만약 project_id가 26998인 경우 project_type을 v3_bs로 변경
        self.mbc_share_data_raw_df.loc[self.mbc_share_data_raw_df['project_id'] == 27056, 'project_type'] = 'v3_bs'

        self.mbc_share_data_df = self.mbc_share_data_raw_df[['file_name', 'project_id','is_label_upload','project_type','prog_state_cd','problem_yn']]
        self.blobs_cache = pd.read_pickle('/home/kim/code/gcs/cache/blobs_cache.pkl')

        self.mbc_share_data_df = self.mbc_share_data_df[~self.mbc_share_data_df['project_type'].isin(['v1'])]        
        self.blobs_cache_df = pd.DataFrame(self.blobs_cache, columns=["file_name"]) 
        self.blobs_cache_df['upload_date'] = self.blobs_cache_df['file_name'].str.split('/').str[2]
        self.blobs_cache_df['category'] = self.blobs_cache_df['file_name'].str.split('/').str[1]
        self.blobs_cache_df['file_name'] = self.blobs_cache_df['file_name'].str.split('/').str[-1]
        print(self.blobs_cache_df)
        # 디버깅 -> null 값있으면 해당 file_name 출력
        #self.blobs_cache_df = self.blobs_cache_df.dropna()

    def base_create_table(self):
        # 결과 : 작업불가 포함, 검수 완료된 데이터들만 추출

        self.mbc_share_data_df = self.mbc_share_data_df[self.mbc_share_data_df['prog_state_cd'].isin(['ALL_FINISHED', 'CHECK_END'])]
        ## 기본 테이블 생성 | 원천 | 카테고리 | 업로드 날짜 | 프로젝트 아이디 | 납품 데이터 여부 |
        self.base_table = pd.DataFrame(columns=['file_name', 'category', 'upload_date', 'project_id', 'is_label_upload','problem_yn'])
        ## 데이터 추가 mbc_share_data 의 file_name과 blobs_cache_df와 merge
        self.base_table = pd.merge(self.mbc_share_data_df, self.blobs_cache_df, on='file_name', how='left')

        print(f"base_table")
        print(f" {self.base_table}")

        # 후처리 완료된 것 미리 업데이트
        def turn0to1(base_table):
            
            print(f"후처리 리스트 수량 확인 : {len(base_table[base_table['is_label_upload'] == 1])}")
            df_20251121 = pd.read_csv('../data/source/후처리 리스트V2V3.csv')
            df_20251126 = pd.read_csv('../data/source/20251126_후처리리스트V2V3.csv')
            df_20251127 = pd.read_csv('../data/source/20251127_150517_후처리리스트.csv')
            df_20251203 = pd.read_csv('../data/source/20251203_후처리리스트.csv')
            df_20251204 = pd.read_csv('../data/source/20251204_후처리리스트.csv')
            df_20251204_v3 = pd.read_csv('../data/source/20251204_후처리리스트_v3.csv')
            df_20251205 = pd.read_csv('../data/source/20251205_후처리리스트.csv')
            df_20251205_1 = pd.read_csv('../data/source/20251205_후처리리스트_2차.csv')
            df_20251206 = pd.read_csv('../data/source/20251206_후처리리스트.csv')
            # CSV의 파일명 목록
            # CSV의 file_name 목록 합치기
            #update_list = df_20251121['file_name'].tolist() + df_20251126['file_name'].tolist()
            update_list = df_20251121['file_name'].tolist() + df_20251126['file_name'].tolist() + df_20251127['file_name'].tolist() + df_20251203['file_name'].tolist() + df_20251204['file_name'].tolist() + df_20251204_v3['file_name'].tolist() + df_20251205['file_name'].tolist() +df_20251205_1['file_name'].tolist() + df_20251206['file_name'].tolist()

            # is_label_upload 값을 업데이트 (inplace update)
            base_table.loc[base_table['file_name'].isin(update_list), 'is_label_upload'] = 1
            print(f"후처리 리스트 수량 확인 : {len(base_table[base_table['is_label_upload'] == 1].value_counts())}")

            return base_table

        self.base_table = turn0to1(self.base_table)
        self.base_table.to_csv('../data/result/base_table.csv', index=False)

        self.problem_df = (
            self.base_table
                .groupby('file_name')
                .agg(problem_yn_sum=('problem_yn', 'sum'))
                .reset_index()
        )
        
        self.problem_df.to_csv('../data/result/problem_df.csv', index=False)
        self.problem_df['problem_yn_flag'] = self.problem_df['problem_yn_sum'].apply(lambda x: 1 if x > 0 else 0)
        
    
    # 업로드 날짜별 수량 파악
    def t1_group_by_date(self):
        # 객체 프로젝트만 추출
        object_data = self.base_table[self.base_table['project_type'].isin(['v2_object','v3_object'])]
        object_data = pd.merge(object_data, self.problem_df, on='file_name', how='outer')

        # 업로드 날짜별 데이터 수량 파악 | 원천_업로드 날짜 | 카테고리 | 데이터 수량 |
        base_table_grouped_by_date = object_data.groupby('upload_date').agg(
            total_rows=('file_name','count'),
            problem_yn=('problem_yn_flag', 'sum'),
            category=('category', 'nunique')        # 전체 행 수
        ).reset_index()
        
        print(f"업로드 날짜별 데이터 수량 파악:")
        print(f"{base_table_grouped_by_date}")
        object_data.to_csv('../data/result/object_data.csv', index=False)
        base_table_grouped_by_date.to_csv('../data/result/base_table_grouped_by_date.csv', index=False)

        #피봇 테이블로 카테고리별 수량 파악
        category_count_df = object_data.pivot_table(
            index='upload_date',
            columns='category',
            values='file_name',
            aggfunc='count',
            fill_value=0
        ).reset_index()    #프로젝트별 수량 파악 

        # 보도, 예능 드리마, 시사교양 순으로 칼럼 재배치
        def reorder_columns(category_count_df):
            # 원하는 순서
            desired_cols = ['upload_date', '보도', '예능', '드라마', '시사,교양']

            # 없는 컬럼은 0으로 생성
            for col in desired_cols:
                if col not in category_count_df.columns:
                    category_count_df[col] = 0

            # 순서 재배치
            category_count_df = category_count_df[desired_cols]

            # 두번째 열에 총합 추가
            category_count_df.insert(1, '총합', category_count_df.iloc[:, 1:].sum(axis=1))
            return category_count_df

        category_count_df = reorder_columns(category_count_df)
        category_count_df.to_csv('../data/result/category_count_df.csv', index=False)

    # 3개 프로젝트 완료가 안 된 데이터들    
    def t2_problem(self):
        # base_table : ALl_FINISHED, CHECK_END 조건 적용된 상태
        problem_df = pd.read_csv('../data/result/problem_df.csv')
        problem_df = problem_df[problem_df['problem_yn_sum'] > 0]
        print(len(problem_df)) # 대략 2000개
    
    # 3개 프로젝트의 작업 상태가 All_FINISHED, CHECK_END이 아닌 데이터들 
    def t1_prog_state_v3(self):
        mbc_share_data_raw_df = self.mbc_share_data_raw_df[self.mbc_share_data_raw_df['project_type'].isin(['v3_object','v3_bs','v3_vqa'])]
        mbc_share_data_raw_df_agg = mbc_share_data_raw_df.groupby('prog_state_cd').agg(
            total_rows=('file_name', 'count')
        ).reset_index()
        print(mbc_share_data_raw_df_agg)

        # work_end
        mbc_share_data_raw_df = mbc_share_data_raw_df[self.mbc_share_data_raw_df['prog_state_cd'].isin(['WORK_END'])]
        mbc_share_data_raw_df.to_csv('../data/result/v3_work_end.csv', index=False)
        mbc_share_data_raw_df_agg = mbc_share_data_raw_df.groupby('project_name').agg(
            total_rows=('file_name', 'count')
        ).reset_index()
        print(mbc_share_data_raw_df_agg)

    # 각 파일명 별 프로젝트 할당 리스트 
    def t1_project_list(self):
        mbc_share_data_raw_df = self.mbc_share_data_raw_df[self.mbc_share_data_raw_df['project_type'].isin(['v3_object','v3_bs','v3_vqa'])]
        mbc_share_data_raw_df = (
            mbc_share_data_raw_df
                .groupby('file_name')
                .agg(project_list=('project_name', lambda x: ', '.join(sorted(set(x)))))
                .reset_index()
        )
        mbc_share_data_raw_df['project_list_split'] = mbc_share_data_raw_df['project_list'].apply(lambda x: [p.strip() for p in x.split(',')])

        # project_list 항목 수가 3개가 아닌 경우만 필터링
        mbc_share_data_raw_df_invalid = mbc_share_data_raw_df[mbc_share_data_raw_df['project_list_split'].apply(len) <=3 ]
        mbc_share_data_raw_df_invalid = mbc_share_data_raw_df_invalid.drop('project_list', axis=1)

        print(mbc_share_data_raw_df_invalid.to_csv('../data/result/v3_project_list_invalid.csv', index=False))

if __name__ == "__main__":
    mbc_path = "/mnt/c/Users/김령래/Desktop/cw_app/mbc_share/mbc_share_data_20251205_180518.csv"
    gcloud = Gcloud()
    mbc_path = gcloud.get_mbc_share_data()
    manage_data_id = ManageDataId(mbc_path)
    manage_data_id.l_load_data()
    manage_data_id.base_create_table()
    manage_data_id.t1_group_by_date()
    manage_data_id.t2_problem()
    manage_data_id.t1_prog_state_v3()
    manage_data_id.t1_project_list()
    #manage_data_id.t1_group_by_project()
    #manage_data_id.t1_group_by_project_and_date()
