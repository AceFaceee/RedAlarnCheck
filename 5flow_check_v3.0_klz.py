import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt
import os

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 设置函数
def x_theory(a, b, vc, t):  # x理论的计算
    res = 0.0186 * (a * b * vc) / (math.sqrt(0.0006 * t * t - 0.0522 * t + 1.1452))
    return res

def x_prac(x):  # x实际的计算
    res = 1000 * (x - 0.03)
    return res

def dif(theory, prac):  ###type(theory) = type(prac) = list 偏差的计算
    temp = 0
    for e in range(5):
        temp += (theory[e] - prac[e])
    res = temp / 5
    return res

def deter(t, p, e):  # 大E的计算
    res = (p / (t - e)) - 1
    return res

def graph(df):  # 做出折线图，并保存在电脑上
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    x = range(0, len(df))
    y = list(df['upper_e_value'])
    plt.plot(x, y)
    plt.title('结瘤模型运算结果图表')  # 设置图体，plt.title
    plt.xlabel('时刻，单位s')  # 设置x轴名称,plt.xlabel
    plt.ylabel('结瘤指数E')  # 设置y轴名称,plt.ylabel
    plt.xlim(0, 180)  # 设置横轴范围，会覆盖上面的横坐标,plt.xlim
    plt.ylim(-0.5, 0.5)  # 设置纵轴范围，会覆盖上面的纵坐标,plt.ylim
    plt.tick_params(axis='both', which='major', labelsize=14)
    plt.show()
    save_loc = r'作图测试.png'
    plt.savefig(save_loc)

def slope_graph(name, slope_list):
    xlist = []
    ylist = []
    for slopes in range(len(slope_list)):
        if slopes % 20 == 0 and slopes != 0 and slopes != 20 and slopes != 40 and slopes != 60:
            xlist.append(slopes)
            ylist.append(slope_list[slopes])
    x1 = xlist
    y1 = ylist
    plt.figure(figsize=(20, 10))
    plt.plot(x1, y1)
    plt.xticks(np.arange(80, xlist[-1], 20))
    plt.xlabel("单位：s")
    plt.ylabel("每20s斜率")
    save_loc = str(name) + "斜率图.png"
    plt.savefig(save_loc)

def judge(start_time, t_alarm, e_min, e_max, listx):
    time = 0
    check_list = []
    judgement = '无结瘤发生'
    for t in range(start_time, len(listx)):
        if listx[t] >= e_min:
            time += 10
            check_list.append(listx[t])
            if time == t_alarm:
                check_start = int(-0.04 * t_alarm)
                check_value = np.mean(check_list[check_start:])
                if check_value >= e_max:
                    judgement = '有结瘤发生'
                else:
                    judgement = '无结瘤发生'
            else:
                continue
        else:
            continue
    return judgement

def main(df):  # 主函数，取值并计算
    # 这五个列表用于存放每10s选取过后的数据
    a_list = []
    b_list = []
    vc_list = []
    t_list = []
    x_list = []
    # 这两个列表是零时用的，用于计算小e
    x_theory_list = []
    x_prac_list = []

    # 每10s取一次数据，最后放在selected_df当中
    for loop in range(0, len(df), 10):
        a = df['B4243_ST1_PLC_mdbotwidth_1'].iloc[loop]
        a_list.append(a)
        b = df['B4243_ST1_WATER_slabthick_1'].loc[loop]
        b_list.append(b)
        vc = df['B4243_ST1_WATER_castspeed_1'].loc[loop]
        vc_list.append(vc)
        t = df['B4243_GEN_PLC_tdsteelweight'].loc[loop]
        t_list.append(t)
        x = df['B4243_ST1_StopperPosition_1'].loc[loop]
        x_list.append(x)
    selected_data = {
        'a_value': a_list,
        'b_value': b_list,
        'vc_value': vc_list,
        't_value': t_list,
        'x_value': x_list
    }
    selected_df = pd.DataFrame(selected_data)
    # 先单独计算小e
    for each in range(55, 60):
        a = selected_df['a_value'][each]
        b = selected_df['b_value'][each]
        vc = selected_df['vc_value'][each]
        t = selected_df['t_value'][each]
        x = selected_df['x_value'][each]
        res_1 = x_theory(a, b, vc, t)
        x_theory_list.append(res_1)
        res_2 = x_prac(x)
        x_prac_list.append(res_2)
    res_3 = dif(x_theory_list, x_prac_list)
    e_value = res_3

    # 清理变量，把两个用于计算小e的列表清空,并添加60个0
    x_theory_list = []
    for zero in range(60):
        x_theory_list.append(0)
    x_prac_list = []
    for zero in range(60):
        x_prac_list.append(0)
    # 用于存放大E计算结果的列表,并添加60个0
    upper_e_list = []
    for zero in range(60):
        upper_e_list.append(0)
    slope_list = []
    for zero in range(60):
        slope_list.append(0)

    # 从610s开始计算
    for every in range(60, len(selected_df)):
        a = selected_df['a_value'][every]
        b = selected_df['b_value'][every]
        vc = selected_df['vc_value'][every]
        t = selected_df['t_value'][every]
        x = selected_df['x_value'][every]
        temp_x_theory_value = x_theory(a, b, vc, t)
        x_theory_list.append(temp_x_theory_value)
        temp_x_prac_value = x_prac(x)
        x_prac_list.append(temp_x_prac_value)
        temp_upper_e_value = deter(t=temp_x_theory_value, p=temp_x_prac_value, e=e_value)
        upper_e_list.append(temp_upper_e_value)

    # 存放进表格
    selected_df['x_theory_value'] = x_theory_list
    selected_df['x_prac_value'] = x_prac_list
    selected_df['upper_e_value'] = upper_e_list
    selected_df = selected_df.fillna(0)
    res_ele = judge(t_alarm=600, e_min=0.42, e_max=0.53, listx=selected_df['upper_e_value'], start_time=200)
    print(single_file + '判定结果为：' + res_ele)
    selected_df.to_excel('E值结算结果'+single_file)
    # save_df_loc = str(name) + '运行结果.xlsx'
    # save_df(selected_df)

if __name__ == '__main__':
    global file_dir
    global single_file
    file_dir = r'C:\Users\User\Desktop\jieliu_model\结瘤模型\5流'
    all_file_list = os.listdir(file_dir)
    for single_file in all_file_list:
        single_data_frame = pd.read_excel(os.path.join(file_dir, single_file), header=0)
        main(df=single_data_frame)
