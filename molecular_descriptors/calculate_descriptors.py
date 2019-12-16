import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split

data = pd.read_csv('/Users/mlugowska/PhD/residence_time/molecular_descriptors/md_rt.csv', delimiter=",",
                   decimal=",", index_col=0).astype(np.float)

# NaN replacing
data.isnull().values.any()
data.fillna(0, inplace=True)

# feature names as a list
col = data.columns  # .columns gives columns names in data
col_labels = col.to_numpy()

# 1) Feature filtering (correlation)
correlation = data.corr()
f, ax = plt.subplots(figsize=(18, 18))
sns.heatmap(correlation, annot=True, linewidths=.5, fmt='.1f', ax=ax)
plt.savefig(f'/Users/mlugowska/PhD/residence_time/molecular_descriptors/correlation_with_rt.png')
plt.show()

# Correlation with output variable
cor_target = abs(correlation['Residence Time'])
# Selecting highly correlated features
relevant_features = cor_target[cor_target > 0.5]

len(col)  # 1614 descriptors

## output
# Residence Time    1.000000
# SddssS            0.522943 SddssS(sulfate)count: This descriptor defines the total number of sulphate group connected with two single and two double bonds.
# MAXddssS          0.522943 max of ddssS
# MINddssS          0.522943 min of ddssS
# n5AHRing          0.501549 5-membered aliphatic hetero ring count
# n8FRing           0.701413 8-membered fused ring count
# n8FHRing          0.701413 8-membered fused hetero ring count
# n8FARing          0.701413 8-membered aromatic fused ring count
# n8FAHRing         0.701413 8-membered aromatic fused hetero ring count


# 2) Train test split
np.random.seed(1)

X = data.drop(['Residence Time'], axis=1)
y = data['Residence Time']
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
