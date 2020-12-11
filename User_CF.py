import random

import math

from operator import itemgetter
# 基于用户的协同过滤算法
# 1.读入数据
# 2.构建trainset
# 3.构建movie-user矩阵
# 4.构建sim-user矩阵
# 5.计算sim-user矩阵的值，计算出排名前几的用户
# 6.找出要推荐给user的电影
class user():
    def set(self):
        self.trainset={}
        self.testset={}
        self.sim_user={}
        self.movie_user={}
        print("初始化成功！")

    def file_load(self,filename):
        with open(filename,'r') as f:
            for i,line in enumerate(f):
                if i == 0:
                    continue
                yield line.strip('\r\n')
            print("文件读取成功！")

    def get_dataset(self,filename):
        for line in self.file_load(filename):
            user,movie,grade=line.split(',')
            if random.random() <0.75:
                self.trainset.setdefault(user,{})
                self.trainset[user][movie]=grade
            else:
                self.testset.setdefault(user,{})
                self.testset[user][movie]=grade
        print("训练集和数据集构建完成！")
        for user,movies in self.trainset.items():
            for movie in movies:
                self.movie_user.setdefault(movie,set())
                self.movie_user[movie].add(user)
        print("用户-电影表构建完成！")
        for movie,users in self.movie_user.items():
            for u1 in users:
                for u2 in users:
                    if u1==u2:
                        continue
                    self.sim_user.setdefault(u1,{})
                    self.sim_user[u1].setdefault(u2,0)
                    self.sim_user[u1][u2]+=1
        for u1,users in self.sim_user.items():
            for u2,v in users.items():
                self.sim_user[u1][u2]=v/math.sqrt(len(self.trainset[u1])*len(self.trainset[u2]))
        print("相似性用户表构建完成！")
    def recommend(self,user):
        rec_movies={}
        for sim_u,u in sorted(self.sim_user[user].items(),key=itemgetter(1),reverse=True)[0:20]:
            for rec_m,grade in self.trainset[sim_u].items():
                if rec_m in self.trainset[user]:
                    continue
                rec_movies[rec_m]=float(grade)*u
        rec_movies=sorted(rec_movies.items(),key=itemgetter(1),reverse=True)[0:10]
        print("推荐电影列表：")
        print(rec_movies)

if __name__=="__main__":
    u1=user()
    u1.set()
    u1.get_dataset('C:\\Users\\lenovo\\Desktop\\新建文本文档.csv')
    u1.recommend('A')









