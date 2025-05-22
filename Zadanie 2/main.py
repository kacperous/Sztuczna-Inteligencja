import pandas as pd
import numpy as np
from glob import glob
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import matplotlib.pyplot as plt

# ------- 1. Ścieżki do katalogów -------
project_dir = os.path.join(os.getcwd(), "pomiary")
f8_dir = os.path.join(project_dir, "F8")
f10_dir = os.path.join(project_dir, "F10")

# ------- 2. Ładuj pliki statyczne F8 i F10 razem -------
stat_files = glob(os.path.join(f8_dir, "*stat*.xlsx")) + glob(os.path.join(f10_dir, "*stat*.xlsx"))
if not stat_files:
    raise Exception("Nie znaleziono plików statycznych w F8/F10!")
dfs = []
for file in stat_files:
    df = pd.read_excel(file)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    dfs.append(df)
data = pd.concat(dfs, ignore_index=True)

feature_cols = ['data__coordinates__x', 'data__coordinates__y']
target_cols  = ['reference__x', 'reference__y']

data = data.dropna(subset=feature_cols + target_cols)
# Konwersja: przecinek na kropkę i float
for col in feature_cols + target_cols:
    data[col] = data[col].astype(str).str.replace(",", ".").astype(float)

X = data[feature_cols].values
y = data[target_cols].values

# ------- Skalowanie wejścia i wyjścia -------
scaler_X = StandardScaler()
scaler_y = StandardScaler()
X_scaled = scaler_X.fit_transform(X)
y_scaled = scaler_y.fit_transform(y)

# ------- Podział train/test -------
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_scaled, test_size=0.2, random_state=42)

# ------- Sieć -------
# ------- Sieć -------
model = Sequential([
    Dense(32, activation='relu', input_dim=2),
    Dense(16, activation='relu'),
    Dense(8, activation='relu'),
    Dense(4, activation='relu'),
    # Warstwa wyjściowa pozostaje bez zmian:
    Dense(2, activation='linear')
])

model.compile(optimizer='adam', loss='mse', metrics=['mae'])
history = model.fit(X_train, y_train, epochs=20, batch_size=8,
                    validation_data=(X_test, y_test), verbose=2)

# ------- TEST na WSZYSTKICH RANDOM -------
random_files = glob(os.path.join(f8_dir, "*random*.xlsx")) + glob(os.path.join(f10_dir, "*random*.xlsx"))
if not random_files:
    print("Nie znaleziono plików random w katalogach F8/F10!")

for random_file in random_files:
    dyn_df = pd.read_excel(random_file)
    dyn_df = dyn_df.loc[:, ~dyn_df.columns.str.contains('^Unnamed')]
    dyn_df = dyn_df.dropna(subset=feature_cols + target_cols)
    if len(dyn_df) == 0:
        continue
    # Konwersja: przecinek na kropkę i float
    for col in feature_cols + target_cols:
        dyn_df[col] = dyn_df[col].astype(str).str.replace(",", ".").astype(float)
    X_dyn = dyn_df[feature_cols].values
    X_dyn_scaled = scaler_X.transform(X_dyn)
    y_pred_scaled = model.predict(X_dyn_scaled)
    y_pred = scaler_y.inverse_transform(y_pred_scaled)

    # Błąd przed i po
    err_before = np.sqrt((dyn_df[feature_cols[0]] - dyn_df[target_cols[0]]) ** 2 +
                         (dyn_df[feature_cols[1]] - dyn_df[target_cols[1]]) ** 2)
    err_after = np.sqrt((y_pred[:, 0] - dyn_df[target_cols[0]]) ** 2 +
                        (y_pred[:, 1] - dyn_df[target_cols[1]]) ** 2)

    # Dystrybuanta
    sorted_before = np.sort(err_before)
    sorted_after = np.sort(err_after)
    cdf = np.arange(1, len(sorted_before) + 1) / len(sorted_before)

    wyniki_df = pd.DataFrame({
        'err_before': sorted_before,
        'err_after': sorted_after,
        'cdf': cdf
    })
    out_name = os.path.splitext(os.path.basename(random_file))[0]
    wyniki_df.to_excel(f"dystrybuanta_{out_name}.xlsx", index=False)

    plt.figure()
    plt.plot(sorted_before, cdf, label='Przed korekcją')
    plt.plot(sorted_after, cdf, label='Po korekcji')
    plt.xlabel('Błąd [px]')
    plt.ylabel('CDF')
    plt.title(f'Dystrybuanta błędu: {out_name}')
    plt.legend()
    plt.grid()
    plt.savefig(f"dystrybuanta_{out_name}.png")
    plt.close()
    print(f"Zrobiono dystrybuantę i wykres dla: {out_name}")

print("\nSieć działa, wyniki wyeksportowane.")

model.save("model_do_korekcji_wspolny_f8f10.keras")
