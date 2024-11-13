import csv
from collections import defaultdict

# 文件名
input_file = '../benchmark_results.csv'

# 用于存储各个指标的总和和计数
sums = defaultdict(float)
counts = defaultdict(int)

# 打开并读取 CSV 文件
with open(input_file, mode='r') as infile:
    reader = csv.reader(infile)
    next(reader)  # 跳过标题行

    for row in reader:
        benchmark, run, result = row[0], row[1], float(row[2])
        
        # 将结果加到相应的指标中
        sums[run] += result
        counts[run] += 1

# 计算平均值
averages = {run: sums[run] / counts[run] for run in sums}

# 输出平均值
for run, avg in averages.items():
    print(f"{run}: {avg:.2f}")
