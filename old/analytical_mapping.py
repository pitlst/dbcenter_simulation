import numpy as np
import matplotlib
import matplotlib.pyplot as plt


matplotlib.rcParams['font.family'] = 'SimHei'  # 或其他支持中文的字体
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号'-'显示为方块的问题

temp_data = np.array(np.load("temp_data.npy"))


xpoints = np.array([i for i in range(100)])  
plt.rcParams['lines.markersize'] = 1
plt.plot(xpoints, np.array(temp_data[:100 ,0]), label='进车次数')
plt.plot(xpoints, np.array(temp_data[:100 ,1]), label='出车次数')
plt.plot(xpoints, np.array(temp_data[:100 ,-1]), label='转运次数')

plt.xticks(xpoints)

plt.xlabel('时间，每步进一个点代表工作10分钟')
plt.legend()

plt.show()
