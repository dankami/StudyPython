#coding=utf-8
#上面一句是定义python的编码，必须写在第一句

if __name__ == "__main__":
    seasons = ['Spring', 'Summer', 'Fall', 'Winter']
    print(type(seasons))
    en_seasons = enumerate(seasons)
    print(en_seasons)
    print(type(en_seasons))
    list_en = list(enumerate(seasons, start=1))  # 小标从 1 开始
    print(list_en)
