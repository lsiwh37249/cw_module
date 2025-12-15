# Modules Documentation

이 디렉토리는 데이터 처리 및 검증을 위한 모듈들을 포함합니다.

## 📁 파일 목록

### 1. Valid.py
**JSON 데이터 검증 모듈**

JSON 파일에서 null 값이나 빈 값을 검증하는 클래스입니다.

#### 주요 기능
- `has_null()`: JSON 데이터에서 null 값이나 빈 문자열을 재귀적으로 검색
- `valid_object()`: 객체 데이터셋 검증 (특정 key 제외 가능)
- `valid_VQA()`, `valid_action()`, `valid_scene()`: 각 데이터셋 타입별 검증

#### 사용 예시
```python
from modules.Valid import Valid

# JSON 파일 검증
valid = Valid('/path/to/file.json')
result = valid.check()

# 전체 디렉토리 검증
for file in json_files:
    valid = Valid(file)
    bol = valid.check()
```

#### 특징
- 재귀적으로 dict/list 구조 탐색
- 특정 key를 검증 대상에서 제외 가능 (`non_target_keys`)
- 빈 리스트도 검증 가능
- 파일명과 함께 null 값 위치 출력

---

### 2. ReSetting.py
**프로젝트 재세팅 모듈**

기존 프로젝트의 데이터를 새로운 프로젝트로 재세팅하는 클래스입니다.

#### 주요 기능
- `set_project_id()`: 프로젝트 ID 리스트를 필터링하고 새로운 프로젝트 정보로 재세팅
- `remove_resset_object_data()`: 이미 재세팅된 데이터 제외
- `agg_data()`: 프로젝트별 데이터 집계

#### 사용 예시
```python
from modules.ReSetting import ReSetting

re_setting = ReSetting('/path/to/mbc_share_data.csv')
re_setting.set_project_id(
    project_id_list=[26668, 26669, 26579],
    project_id=27108,
    project_type='object',
    organization_id=1070
)
re_setting.output_df.to_csv('output.csv', index=False)
```

#### 출력 컬럼
- `file_name`: 파일명
- `project_id_old`: 기존 프로젝트 ID
- `project_id`: 새로운 프로젝트 ID
- `project_type`: 프로젝트 타입
- `organization_id`: 조직 ID

---

### 3. Delivery.py
**납품 데이터 처리 모듈**

납품 가능한 데이터를 필터링하고 분류하는 클래스입니다.

#### 주요 기능
- `remove_data()`: 납품 가능한 최소 조건으로 필터링
- `except_data()`: 이미 납품된 데이터 제외
- `set_3_type()`: 프로젝트 타입별로 분류 (v3_object, v3_bs, v3_vqa)
- `check_vaild_data()`: 납품 가능 여부 검증
- `get_check_caption_empty()`: 캡셔닝 빈 데이터 확인
- `get_problem_data_but_can_delivery()`: 문제가 있지만 납품 가능한 데이터 추출

#### 사용 예시
```python
from modules.Delivery import Delivery

delivery = Delivery('/path/to/mbc_share_data.csv')

# 납품한 데이터 제외
df = delivery.except_data()

# 납품 가능한 최소 조건으로 필터링
df = delivery.remove_data()

# 프로젝트 타입으로 분류
df_object, df_action, df_vqa = delivery.set_3_type()

# 검증
delivery.check_vaild_data()
```

#### 필터링 조건
- `prog_state_cd`: 'CHECK_END', 'ALL_FINISHED'
- `is_label_upload`: 1이 아닌 경우
- `problem_yn`: 1이 아닌 경우

---

### 4. ManageDataId.py
**데이터 현황 관리 모듈**

데이터 현황 파악을 위한 기본 테이블을 생성하고 분석하는 클래스입니다.

#### 주요 기능
- `l_load_data()`: mbc_share_data와 blobs_cache 데이터 로드
- `base_create_table()`: 기본 테이블 생성 및 후처리 리스트 업데이트
- `t1_group_by_date()`: 업로드 날짜별 데이터 수량 파악
- `t2_problem()`: 문제가 있는 데이터 추출
- `t1_prog_state_v3()`: v3 프로젝트의 작업 상태 분석
- `t1_project_list()`: 파일명별 프로젝트 할당 리스트 생성

#### 사용 예시
```python
from modules.ManageDataId import ManageDataId
from modules.Gcloud import Gcloud

gcloud = Gcloud()
mbc_path = gcloud.get_mbc_share_data()

manage_data_id = ManageDataId(mbc_path)
manage_data_id.l_load_data()
manage_data_id.base_create_table()
manage_data_id.t1_group_by_date()
manage_data_id.t2_problem()
```

#### 출력 파일
- `base_table.csv`: 기본 테이블
- `problem_df.csv`: 문제 데이터
- `object_data.csv`: 객체 데이터
- `base_table_grouped_by_date.csv`: 날짜별 집계
- `category_count_df.csv`: 카테고리별 수량

---

### 5. Category.py
**카테고리 비교 모듈**

원천 업로드 수량과 납품 완료된 수량을 비교하는 클래스입니다.

#### 주요 기능
- `compare()`: 납품 데이터와 원천 데이터를 비교하여 남은 수량 계산

#### 사용 예시
```python
from modules.Category import Category

category = Category(
    delivery_path='../data/result/category_count_df.csv',
    source_path='../data/source/업로드정보.csv'
)
category.compare()
```

#### 비교 항목
- 총합
- 보도
- 예능
- 드라마
- 시사교양

---

### 6. Gcloud.py
**Google Cloud Storage 연동 모듈**

GCS에서 최신 mbc_share_data 파일을 다운로드하는 클래스입니다.

#### 주요 기능
- `get_mbc_share_data()`: GCS에서 최신 mbc_share_data 파일 다운로드

#### 사용 예시
```python
from modules.Gcloud import Gcloud

gcloud = Gcloud()
mbc_path = gcloud.get_mbc_share_data()
```

#### 환경 변수
- `GCP_PROJECT_ID`: GCP 프로젝트 ID
- `GCS_BUCKET_NAME`: GCS 버킷 이름

#### 다운로드 경로
- `/mnt/c/Users/김령래/Desktop/cw_app/mbc_share/`

---

### 7. gchat.py
**Google Chat 메시지 전송 모듈**

Google Chat에 메시지를 전송하는 스크립트입니다.

#### 기능
- 서비스 계정을 사용하여 Google Chat에 메시지 전송

#### 설정
- `SERVICE_ACCOUNT_FILE`: 서비스 계정 키 파일 경로
- `SPACE_ID`: Google Chat 스페이스 ID

---

### 8. De.py
**데이터 분석 유틸리티**

프로젝트 타입이 비어있는 프로젝트를 확인하는 클래스입니다.

#### 주요 기능
- `get_empty_project_type()`: 프로젝트별 집계 및 빈 프로젝트 타입 확인

#### 사용 예시
```python
from modules.De import De

de = De('/path/to/mbc_share_data.csv')
de.get_empty_project_type()
```

---

## 🔧 공통 의존성

- `pandas`: 데이터 처리
- `json`: JSON 파일 처리
- `datetime`: 날짜/시간 처리
- `google-cloud-storage`: GCS 연동 (Gcloud.py)
- `google.oauth2`: 인증 (gchat.py)

---

## 📝 사용 시 주의사항

1. **경로 설정**: 각 모듈에서 사용하는 파일 경로가 환경에 맞게 설정되어 있는지 확인
2. **환경 변수**: Gcloud.py 사용 시 GCP 관련 환경 변수 설정 필요
3. **데이터 형식**: 입력 데이터의 형식이 각 모듈의 기대 형식과 일치하는지 확인
4. **권한**: GCS 접근 및 파일 읽기/쓰기 권한 확인

---

## 🔄 모듈 간 연동

일반적인 워크플로우:

1. **Gcloud.py**: 최신 mbc_share_data 다운로드
2. **ManageDataId.py**: 데이터 현황 분석 및 기본 테이블 생성
3. **Delivery.py**: 납품 가능 데이터 필터링 및 분류
4. **Valid.py**: JSON 데이터 검증
5. **ReSetting.py**: 프로젝트 재세팅
6. **Category.py**: 납품 수량 비교

---

## 📅 최종 업데이트

2025-12-15

