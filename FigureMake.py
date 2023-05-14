import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# 准备数据
data = {
    'Category': ['A', 'B', 'C', 'A', 'B', 'C'],
    'Type': ['Type1', 'Type1', 'Type1', 'Type2', 'Type2', 'Type2'],
    'Value': [10, 12, 14, 20, 24, 28]
}

df = pd.DataFrame(data)

# 创建一个 1x2 的子图布局
fig, axes = plt.subplots(1, 2, figsize=(8, 4))

# 在第一个子图中绘制柱状图
sns.barplot(x='Category', y='Value', hue='Type', data=df, ax=axes[0])

# 在第二个子图中绘制相同的柱状图
sns.barplot(x='Category', y='Value', hue='Type', data=df, ax=axes[1])

# 显示图形
plt.show()
