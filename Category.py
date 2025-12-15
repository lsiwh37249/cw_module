import pandas as pd

#원천 업로드 수량과 납품 완료된 수량 비교
class Category:
    def __init__(self, delivery_path, source_path):
        self.category_count_df = pd.read_csv(delivery_path)
        self.source_df = pd.read_csv(source_path)
        self.merge_df = None
    
    def compare(self):
        self.merge_df = self.source_df.merge(self.category_count_df, on='upload_date', how='inner')
        self.merge_df['남은 수량'] = self.merge_df['총합_x'] - self.merge_df['총합_y']
        self.merge_df['보도'] = self.merge_df['보도_x'] - self.merge_df['보도_y']
        self.merge_df['예능'] = self.merge_df['예능_x'] - self.merge_df['예능_y']
        self.merge_df['드라마'] = self.merge_df['드라마_x'] - self.merge_df['드라마_y']
        self.merge_df['시사교양_l'] = self.merge_df['시사교양'] - self.merge_df['시사,교양']
        print(self.merge_df)
        #print(self.merge_df[['upload_date','남은 수량', '보도', '예능', '드라마', '시사교양']])

if __name__ == "__main__":
    delivery_path = "../data/result/category_count_df.csv" 
    source_path = "../data/source/업로드정보.csv" 
    category = Category(delivery_path, source_path)
    category.compare()

