import json

class Valid:
    def __init__(self, json_path):
        self.json_path = json_path

    def has_null(self, key, value, non_target_keys=None):
        if non_target_keys is None:
            non_target_keys = []

        # 1) 값이 dict/list가 아닌 경우 — 실제 null 체크
        if not isinstance(value, (dict, list)):
            if key not in non_target_keys:
                if value is None or value == "":
                    print(f"[파일: {self.json_path}] Null 값 발견: key={key}, value={value}")
                    return True
            return False

        # 2) dict 처리
        if isinstance(value, dict):
            return any(self.has_null(k, v, non_target_keys) for k, v in value.items())

        # 3) list 처리 —★ 여기서 empty 체크 가능
        if isinstance(value, list):
            if key not in non_target_keys and len(value) == 0:
                print(f"[파일: {self.json_path}] Null 리스트 발견: key={key}, value={value}")
                return True

            return any(self.has_null(key, item, non_target_keys) for item in value)

        return False


    def valid_VQA(self):
        # VQA 데이터 검증
        
        pass
    def valid_object(self, data):
        # 객체 데이터 검증
        non_target = ["object_name_en", "object_desciption_kr", "object_desciption_en"]
        if self.has_null(None, data, non_target):
            return False
        pass
    def valid_action(self):
        # 행동 데이터 검증
        pass
    def valid_scene(self):
        # 장면 데이터 검증
        pass

    def check(self):
        with open(self.json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if 'VQA' in self.json_path:
            pass
            #return self.valid_VQA(data)
        elif '객체' in self.json_path:
            return self.valid_object(data)
        elif '행동' in self.json_path:
            pass
            #return self.valid_action(data)
        elif '장면' in self.json_path:
            pass
            #return self.valid_scene(data)
        else:
            return None

if __name__ == "__main__":
    import os

    base_dir = '/home/kim/app/airflow/tmp/gcs_json/CW_OUTPUT/'

    file_list = []

    for root, dirs, files in os.walk(base_dir):
        for f in files:
            file_path = os.path.join(root, f)
            file_list.append(file_path)

    for file in file_list:
        if file.endswith('.json'):
            valid = Valid(file)
            bol = valid.check()
            if bol:
                print(f"{file} : {bol}")