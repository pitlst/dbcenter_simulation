import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt


matplotlib.rcParams['font.family'] = 'SimHei'  # 或其他支持中文的字体
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号'-'显示为方块的问题

temp_data = np.array(np.load(r"F:\\dbcenter_simulation\\analyze\\temp.npy"))

# print(temp_data[:100 ,3])
# print(temp_data[:100 ,3])

xpoints = np.array([i for i in range(100)])  
plt.rcParams['lines.markersize'] = 1
plt.plot(xpoints, np.array(temp_data[:100 ,0]), label='进车次数')
plt.plot(xpoints, np.array(temp_data[:100 ,1]), label='出车次数')
plt.plot(xpoints, np.array(temp_data[:100 ,2]), label='转运次数')
plt.plot(xpoints, np.array(temp_data[:100 ,3]), label='异常次数')
plt.plot(xpoints, np.array(temp_data[:100 ,4]), label='异常时长')

plt.xticks(xpoints)

plt.xlabel('时间，每步进一个点代表工作10分钟')
plt.legend()

plt.show()

# temp_data = pd.read_csv(r"F:\\dbcenter_simulation\\analyze\\error.csv")
# temp_data['days_start_to_end'] = temp_data.end - temp_data.start

# fig, ax = plt.subplots(1, figsize=(16,6))
# ax.barh(temp_data.task, temp_data.days_start_to_end, left=temp_data.start)

# def color(row):
#     c_dict = {'MKT':'#E64646', 'FIN':'#E69646', 'ENG':'#34D05C', 'PROD':'#34D0C3', 'IT':'#3475D0'}
#     return c_dict[row['task']]
# temp_data['color'] = temp_data.apply(color, axis=1)

# plt.show()
