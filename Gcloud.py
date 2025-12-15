from math import e
import pandas as pd
import duckdb
import os

class Gcloud:
    def __init__(self):
        self.mbc_share_data_path = None
        
    def get_mbc_share_data(self):
        from google.cloud import storage
        from datetime import datetime

        # GCS 클라이언트 생성
        client = storage.Client(project=os.getenv('GCP_PROJECT_ID'))

        # 버킷 이름과 경로 설정
        bucket_name = os.getenv('GCS_BUCKET_NAME')
        prefix = 'cw/07-mbc-bq/mbc_share_data/'

        bucket = client.bucket(bucket_name)

        # 파일 리스트 가져오기
        blobs = list(bucket.list_blobs(prefix=prefix))

        df = pd.DataFrame()
        if not blobs:
            print("해당 경로에 파일이 없습니다.")
        else:
            # 최신 파일 찾기
            latest_blob = max(blobs, key=lambda b: b.updated)  # b.updated: 최종 수정일
            print("최신 파일 이름:", latest_blob.name)
            print("업데이트 날짜:", latest_blob.updated)

            # df 다운로드: 로컬 저장 경로 생성 후 저장
            local_dir = '/mnt/c/Users/김령래/Desktop/cw_app/mbc_share'
            os.makedirs(local_dir, exist_ok=True)
            local_path = os.path.join(local_dir, os.path.basename(latest_blob.name))
            latest_blob.download_to_filename(local_path)
            print(f"다운로드 완료 : {local_path}")
        return local_path