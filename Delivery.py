import pandas as pd
import os
class Delivery:
    def __init__(self, file_name):
        self.df = pd.read_csv(file_name)
        self.caption_empty_df = None

    def remove_data(self):
        self.df = self.df[self.df['prog_state_cd'].isin(['CHECK_END', 'ALL_FINISHED'])]
        self.df = self.df[self.df['is_label_upload'] != 1]
        self.df = self.df[self.df['problem_yn'] != 1]
        self.df.loc[self.df['project_id'] == 27056, 'project_type'] = 'v3_bs'

        return self.df
    
    def set_3_type(self):
        # 객체 데이터 파일 리스트 추출 (파일 or GCS)
        df_object = self.df[self.df['project_type'] == 'v3_object']
        df_action = self.df[self.df['project_type'] == 'v3_bs']
        df_vqa = self.df[self.df['project_type'] == 'v3_vqa']
        #df_vqa = self.df[self.df['project_id'].isin([27000, 26999, 26998,26997])]
        return df_object, df_action, df_vqa

    def except_data(self):
        # 원본 데이터 수 저장 (제거 전)
        original_count = len(self.df)

        # 첫 번째 제외 리스트
        done_df1 = pd.read_csv('../data/source/후처리 리스트V2V3.csv')
        removed1 = self.df[self.df['file_name'].isin(done_df1['file_name'])]
        self.df = self.df[~self.df['file_name'].isin(done_df1['file_name'])]

        # 두 번째 제외 리스트
        done_df2 = pd.read_csv('../data/source/20251126_후처리리스트V2V3.csv')
        removed2 = self.df[self.df['file_name'].isin(done_df2['file_name'])]
        self.df = self.df[~self.df['file_name'].isin(done_df2['file_name'])]

        done_df3 = pd.read_csv('../data/source/20251127_150517_후처리리스트.csv')
        removed3 = self.df[self.df['file_name'].isin(done_df3['file_name'])]
        self.df = self.df[~self.df['file_name'].isin(done_df3['file_name'])]

        done_df4 = pd.read_csv('../data/source/20251203_후처리리스트.csv')
        removed4 = self.df[self.df['file_name'].isin(done_df4['file_name'])]
        self.df = self.df[~self.df['file_name'].isin(done_df4['file_name'])]

        done_df5 = pd.read_csv('../data/source/20251204_후처리리스트.csv')
        removed5 = self.df[self.df['file_name'].isin(done_df5['file_name'])]
        self.df = self.df[~self.df['file_name'].isin(done_df5['file_name'])]

        done_df5 = pd.read_csv('../data/source/20251204_후처리리스트_v3.csv')
        removed5 = self.df[self.df['file_name'].isin(done_df5['file_name'])]
        self.df = self.df[~self.df['file_name'].isin(done_df5['file_name'])]
        
        done_df6 = pd.read_csv('../data/source/20251205_후처리리스트.csv')
        removed6 = self.df[self.df['file_name'].isin(done_df6['file_name'])]
        self.df = self.df[~self.df['file_name'].isin(done_df6['file_name'])]

        done_df7 = pd.read_csv('../data/source/20251205_후처리리스트_2차.csv')
        removed7 = self.df[self.df['file_name'].isin(done_df7['file_name'])]
        self.df = self.df[~self.df['file_name'].isin(done_df7['file_name'])]

        done_df8 = pd.read_csv('../data/source/20251206_후처리리스트.csv')
        removed8 = self.df[self.df['file_name'].isin(done_df8['file_name'])]
        self.df = self.df[~self.df['file_name'].isin(done_df8['file_name'])]
        final_count = len(self.df)
        total_removed = original_count - final_count

        print("=== 제거 결과 ===")
        print(f"전체 데이터 수: {original_count}")
        print(f"제외된 파일(1차): {len(removed1)}")
        print(f"제외된 파일(2차): {len(removed2)}")
        print(f"제외된 파일(3차): {len(removed3)}")
        print(f"제외된 파일(4차): {len(removed4)}")
        print(f"제외된 파일(5차): {len(removed5)}")
        print(f"제외된 파일(6차): {len(removed6)}")
        print(f"최종 남은 데이터 수: {final_count}")
        print(f"총 제거된 수: {total_removed}")

        return self.df


    def check_vaild_data(self):
        print("\n검사 시작...\n")
        # ---------- 1) 업로드된 데이터(불가능) ----------
        uploaded_invalid = self.df[self.df['is_label_upload'] == 1]
        if not uploaded_invalid.empty:
            print("❌ 업로드된 데이터가 있습니다. (is_label_upload = 1)")
            print(uploaded_invalid)
            return False
        # ---------- 2) 허용되지 않은 is_label_upload 값 ----------
        allowed = ["CHECK_END", "ALL_FINISHED"]
        invalid_label = self.df[~self.df['prog_state_cd'].isin(allowed)]
        if not invalid_label.empty:
            print(f"❌ 허용되지 않은 is_label_upload 값이 있습니다. (허용값: {allowed})")
            print(invalid_label)
            return False
        # ---------- 3) 문제 있는 데이터(problem_yn = 1) ----------
        problem_invalid = self.df[self.df['problem_yn'] == 1]
        if not problem_invalid.empty:
            print("❌ 문제(problem_yn = 1)가 있는 데이터가 있습니다.")
            print(problem_invalid)
            return False
        # ---------- 성공 ----------
        print("✅ 모든 조건을 통과했습니다.")   
        return True
    
    def get_check_caption_empty(self,result_df):
        # 4개 프로젝트 union
        df1 = pd.read_csv('../data/source/26930.csv')
        df2 = pd.read_csv('../data/source/26932.csv')
        df3 = pd.read_csv('../data/source/26933.csv')
        df4 = pd.read_csv('../data/source/26934.csv')
        union_df = pd.concat([df1, df2, df3, df4])

        # result_df와 union_df를 data_id 기준으로 있는지 확인
        empty_caption_df = union_df[union_df['데이터ID'].isin(result_df['data_id'])]
        self.caption_empty_df = empty_caption_df
        self.caption_empty_df.to_csv(f'../data/result/delivery_result/{date}_caption_empty.csv', index=False)
        return self.caption_empty_df
    
    def filter_object_data(sel, df_object):
        df_object = df_object[
            df_object['project_id'].isin(object_type_2) | df_object['project_id'].isin(object_type_1) &
            df_object['is_mod'] == True
        ]
        return df_object
    
    def save_data(self, object_df, action_df, vqa_df):
        object_df.to_csv('../data/tmp/df_object.csv', index=False)
        action_df.to_csv('../data/tmp/df_action.csv', index=False)
        vqa_df.to_csv('../data/tmp/df_vqa.csv', index=False)
        print("=========================="*10)
        print(f"problem_yn = 0, is_label_upload = 0, prog_state_cd = CHECK_END, ALL_FINISHED 데이터 수:")
        print(f"v3_object 데이터 수: {len(object_df)}")
        print(f"v3_bs 데이터 수: {len(action_df)}")
        print(f"v3_vqa 데이터 수: {len(vqa_df)}")
        print("=========================="*10)

    def get_which_one_empty(self, object_df, action_df, vqa_df):
        union_df = pd.concat([object_df, action_df, vqa_df])
        df = pd.DataFrame(union_df['file_name'].unique(), columns=['file_name'])
        #만약 file_name이 object_df, action_df, vqa_df 에 있는지 확인
        df['object_df'] = df['file_name'].isin(object_df['file_name'])
        df['action_df'] = df['file_name'].isin(action_df['file_name'])
        df['vqa_df'] = df['file_name'].isin(vqa_df['file_name'])
        df = df.sort_values(by='action_df', ascending=False)
        df.to_csv('../data/tmp/df.csv', index=False)
        
        return union_df
    
    def get_problem_data_but_can_delivery(self, file_path):
        df = pd.read_csv(file_path)
        v3_etc = df[df['project_type'].isin(['v3_bs', 'v3_vqa'])]
        v3_etc = v3_etc[v3_etc['problem_yn'] != 1]
        v3_etc = v3_etc[v3_etc['is_label_upload'] != 1]
        v3_etc = v3_etc[v3_etc['prog_state_cd'].isin(['CHECK_END', 'ALL_FINISHED'])]

        v3_object = df[df['project_type'] == 'v3_object']
        v3_object = v3_object[v3_object['project_id'].isin([26932, 26930, 26933, 26934])]
        v3_object = v3_object[v3_object['problem_yn'] == 1]
        v3_object = v3_object[v3_object['is_mod'] == True]
        v3_object = v3_object[v3_object['is_label_upload'] != 1]
        v3_object = v3_object[v3_object['prog_state_cd'].isin(['CHECK_END', 'ALL_FINISHED'])]
        union_df = pd.concat([v3_etc, v3_object])
        result_df = union_df[union_df['file_name'].isin(union_df['file_name'].value_counts()[union_df['file_name'].value_counts() == 3].index)]
        result_df.to_csv(f'../data/result/delivery_result/{date}_problem_data_but_can_delivery.csv', index=False)
        print(f"작업 불가지만 납품 가능한 데이터 수 : {len(result_df)}")


file_name = 'mbc_share_data_20251209_190527.csv'
date = file_name.split('_')[3] + "_" + file_name.split('_')[4].replace('.csv', '')
file_path = '/mnt/c/Users/김령래/Desktop/cw_app/mbc_share/' + file_name

#df_object 중에 project_id가 26932,26930,26933,26934 인 애들 중에 작업 수정이 없는 애들은 제외

### 집계
delivery = Delivery(file_path)

### 데이터 필터링
object_type_1 = [26932, 26930, 26933, 26934]
object_type_2 = [27009, 27010, 27047, 27064]

# 납품한 데이터 제외
df = delivery.except_data()
# 납품 가능한 최소 조건으로 필터링링
df = delivery.remove_data()
# 프로젝트 타입으로 분류
df_object, df_action, df_vqa = delivery.set_3_type()
# df_object 추가 필터링
df_object = delivery.filter_object_data(df_object)

union_df = pd.concat([df_object, df_action, df_vqa])
delivery.save_data(df_object, df_action, df_vqa)
delivery.get_which_one_empty(df_object, df_action, df_vqa)

result_df = union_df[union_df['file_name'].isin(union_df['file_name'].value_counts()[union_df['file_name'].value_counts() == 3].index)]
print(f"최종 데이터 수: {len(result_df)}")
unpacked_df = union_df[~union_df['file_name'].isin(result_df['file_name'])]
unpacked_df.to_csv(f'../data/result/{date}_unpacked_df.csv', index=False)


### 검증
delivery.check_vaild_data()

delivery.get_problem_data_but_can_delivery(file_path)

os.makedirs(f'../data/result/delivery_result', exist_ok=True)
result_df.to_csv(f'../data/result/delivery_result/{date}_후처리리스트.csv', index=False)
print(f" 총 갯수 : {len(result_df.drop_duplicates(subset=['file_name']))}")

### 캡셔닝 확인인
delivery.get_check_caption_empty(result_df)
