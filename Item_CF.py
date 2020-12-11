import random

import math
from operator import itemgetter
# 基于物品的协同过滤算法
# 1.读入数据
# 2.构建train-set
# 3.构建movie-popular表  存入每个电影出现的总数量
# 4.构建movie-sim矩阵    存入每两个电影同时出现的次数
# 5.将movie-sim矩阵中的值计算为他们的相似度
# 6.选出排名前十的电影 推荐给用户
class item():
    def set_movie(self):
        self.train_set={}
        self.test_set={}
        self.movie_sim_matrix = {}
        self.movie_popular = {}
        self.movie_count = 0
        print("初始化完成！")
    def get_user_data(self,filename):
        for file in self.load_file(filename):
            user,movie,grade=file.split(',')
            if random.random() < 0.75:
                self.train_set.setdefault(user,{})
                self.train_set[user][movie]=grade
            else:
                self.test_set.setdefault(user,{})
                self.test_set[user][movie]=grade
            self.movie_count+=1
        print("训练集和测试集构建完成！")
    def set_movie_sim(self):
        for user, movies in self.train_set.items():
            for n,movie in enumerate(movies):
                self.movie_popular.setdefault(movie,0)
                self.movie_popular[movie]+=1
        print("流行电影表构建完成！")
        for user,movies in self.train_set.items():
            for m1 in movies:
                for m2 in movies:
                    if m1==m2:
                        continue
                    self.movie_sim_matrix.setdefault(m1,{})
                    self.movie_sim_matrix[m1].setdefault(m2,0)
                    self.movie_sim_matrix[m1][m2]+=1
        print("电影相似度邻接矩阵构建完成！")
        for m1,movies in self.movie_sim_matrix.items():
            for m2 in self.movie_sim_matrix[m1]:
                self.movie_sim_matrix[m1][m2]=self.movie_sim_matrix[m1][m2]/math.sqrt(self.movie_popular[m1]*self.movie_popular[m2])
        print("电影相似度邻接矩阵构建完成！")
    def rec_movie(self,user):
        K=10
        re_movies= {}
        watch_movie=self.train_set[user]
        for movie,grade in watch_movie.items():
            for relate_movie,g in sorted(self.movie_sim_matrix[movie].items(),key=itemgetter(1),reverse=True)[:K]:
                if relate_movie not in watch_movie:
                    re_movies.setdefault(relate_movie,0)
                    re_movies[relate_movie]=float(grade)*g
        print("推荐电影表构建完成！")
        print(re_movies)

    def load_file(self,filename):
        with open(filename,'r') as f:
            for i,line in enumerate(f):
                if i == 0:
                    continue
                yield line.strip('\r\n')
        print("文件录入成功！")





if __name__=="__main__":
    rating_file = 'C:\\Users\\lenovo\\Desktop\\新建文本文档.csv'
    i=item()
    i.set_movie()
    i.get_user_data(rating_file)
    i.set_movie_sim()
    i.rec_movie("A")