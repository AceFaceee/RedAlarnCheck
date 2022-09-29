import pandas as pd
import os
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


#遍历文件夹里的所有csv
file_dir = r"ZT_20210409101144"
all_file_list=os.listdir(file_dir)
for single_file in all_file_list:
    single_data_frame=pd.read_csv(os.path.join(file_dir,single_file),header=0)
    if single_file ==all_file_list[0]:
        all_data_frame=single_data_frame
    else:
        all_data_frame=pd.concat([all_data_frame,single_data_frame],ignore_index=True)


################# 检查文件读入, 修改，第13行，去掉sep = '\t'；这个遍历文件的方法使用的非常好       
#print(all_data_frame.head(2))
print(all_data_frame.columns[0])
print(all_data_frame['slabId'].unique().shape[0])   # 总共有2086块板坯

#################

def deltav(df):        #输出列表格式，计算速度变化
    deltav = [0]
    for i in range(len(df)-1):
        ############ 如果i到了最后一个值，那么i+1就会超过范围，修改29行：len(df)-1
        ###### 建议下一行使用iloc,直接定位到一行的某一个值
        d = df.iloc[i+1]['B4243_ST1_WATER_castspeed_1']-df.iloc[i]['B4243_ST1_WATER_castspeed_1']
        #print(i)
        deltav.append(d)
    df['deltav'] = deltav
    return df 

def deltat(df):
    deltat = [1]
    for i in range(len(df)-1):
        ############ 如果i到了最后一个值，那么i+1就会超过范围，修改36行：len(df)-1
        t = df.iloc[i+1]['ttime']- df.iloc[i]['ttime']
        deltat.append(t)
    df['deltat'] = deltat
    return df

def acc(df):
    acceleration = []
    for i in range(len(df)):                   ######## 修改： 第47行 加括号  
        acc = df.iloc[i]['deltav'] / df.iloc[i]['deltat']
        acceleration.append(acc)
        df['acceleration'] = acceleration
    return df

################# 检查以上函数

all_data_frame.groupby("slabId").apply(deltav)
all_data_frame.groupby("slabId").apply(deltat)
all_data_frame.groupby("slabId").apply(acc)

print(all_data_framedf.head())


