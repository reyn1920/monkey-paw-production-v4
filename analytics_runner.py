import os, glob, pandas as pd, matplotlib.pyplot as plt
os.makedirs('analytics/plots', exist_ok=True)
for csv in glob.glob('data/*.csv'):
    name = os.path.splitext(os.path.basename(csv))[0]
    df = pd.read_csv(csv)
    for col in df.select_dtypes(include='number').columns:
        plt.figure()
        df[col].plot(title=f'{name}:{col}')
        plt.tight_layout()
        plt.savefig(f'analytics/plots/{name}_{col}.png')
        plt.close()
