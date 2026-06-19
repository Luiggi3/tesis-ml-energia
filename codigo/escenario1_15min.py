# =============================================================================
# ESCENARIO 1 — RESAMPLE A 15 MINUTOS + MODELOS ML
# Tesis: Modelo predictivo del consumo energético en hogares inteligentes
# Modelos: Random Forest | XGBoost | SVR
# Métricas: RMSE | MAE | MAPE | R²
# =============================================================================

import matplotlib
# matplotlib.use('Agg')  # desactivado: permite ver gráficos en Spyder
import os, warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from xgboost import XGBRegressor

warnings.filterwarnings('ignore')
plt.rcParams.update({'figure.dpi': 150, 'font.size': 10})

# ── CONFIGURACIÓN ─────────────────────────────────────────────────────────────
ESCENARIO     = 1
FREQ          = '15min'
FREQ_LABEL    = '15 Minutos'
LAGS_GAP      = [1, 2, 4, 8, 12, 96]   # 96 períodos = 24 h hacia atrás
ROLL_WINDOWS  = [4, 8, 96]
TRAIN_RATIO   = 0.80
SVR_MAX_TRAIN = 15_000                  # límite muestras SVR por costo computacional
N_VIZ         = 500                     # puntos del test a mostrar en gráficos

_here = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = _here if os.path.exists(os.path.join(_here, 'datos')) else os.path.dirname(_here)
DATA_CSV = os.path.join(BASE_DIR, 'datos', 'dataset_limpio.csv')
GRAF_DIR = os.path.join(BASE_DIR, 'graficos', f'escenario{ESCENARIO}')
MOD_DIR  = os.path.join(BASE_DIR, 'modelos')
os.makedirs(GRAF_DIR, exist_ok=True)
os.makedirs(MOD_DIR,  exist_ok=True)

COLORES = {'Random Forest': '#1565C0', 'XGBoost': '#2E7D32', 'SVR': '#B71C1C'}

def savefig(nombre):
    plt.tight_layout()
    plt.savefig(os.path.join(GRAF_DIR, nombre), dpi=150, bbox_inches='tight')
    plt.show()
    plt.close()

def calcular_metricas(y_true, y_pred, nombre):
    yt, yp = np.array(y_true), np.array(y_pred)
    rmse = np.sqrt(mean_squared_error(yt, yp))
    mae  = mean_absolute_error(yt, yp)
    mask = yt > 0.01
    mape = np.mean(np.abs((yt[mask] - yp[mask]) / yt[mask])) * 100
    r2   = r2_score(yt, yp)
    return {'Modelo': nombre,
            'RMSE': round(rmse, 4),
            'MAE' : round(mae,  4),
            'MAPE': round(mape, 2),
            'R2'  : round(r2,   4)}

# =============================================================================
# 1. CARGA Y RESAMPLE
# =============================================================================
print("=" * 65)
print(f"ESCENARIO {ESCENARIO} — RESAMPLE A {FREQ_LABEL}")
print("=" * 65)

df_raw = pd.read_csv(DATA_CSV, index_col='datetime', parse_dates=True)
df_raw = df_raw[['GAP', 'GRP', 'VOLT', 'GI', 'SM1', 'SM2', 'SM3']]

print(f"Dataset limpio cargado: {len(df_raw):,} registros a 1 minuto")

df = df_raw.resample(FREQ).mean().dropna()

print(f"Tras resample a {FREQ_LABEL}: {len(df):,} registros")
print(f"Período: {df.index.min()} → {df.index.max()}")
print(f"\nEstadísticas descriptivas:")
print(df.describe().round(3).to_string())

# =============================================================================
# 2. FEATURE ENGINEERING
# =============================================================================
print("\n" + "=" * 65)
print("2. FEATURE ENGINEERING")
print("=" * 65)

df = df.drop(columns=['GI'])  # correlación 0.999 con GAP — multicolinealidad

# Temporales
df['hora']       = df.index.hour
df['dia_semana'] = df.index.dayofweek
df['mes']        = df.index.month
df['es_finde']   = df['dia_semana'].isin([5, 6]).astype(int)

# Lags de GAP
for lag in LAGS_GAP:
    df[f'GAP_lag_{lag}'] = df['GAP'].shift(lag)

# Rolling de GAP (shift(1) evita data leakage con el timestep actual)
for w in ROLL_WINDOWS:
    df[f'GAP_roll_mean_{w}'] = df['GAP'].shift(1).rolling(w).mean()
    df[f'GAP_roll_std_{w}']  = df['GAP'].shift(1).rolling(w).std()

df = df.dropna()

FEATURES = [c for c in df.columns if c != 'GAP']
print(f"Registros tras features: {len(df):,}")
print(f"Features: {len(FEATURES)}")
print(f"  {FEATURES}")

# =============================================================================
# 3. SPLIT CRONOLÓGICO 80 / 20
# =============================================================================
print("\n" + "=" * 65)
print("3. SPLIT CRONOLÓGICO (80 / 20)")
print("=" * 65)

X, y, idx = df[FEATURES].values, df['GAP'].values, df.index
split = int(len(df) * TRAIN_RATIO)

X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]
idx_test        = idx[split:]

print(f"Entrenamiento: {len(X_train):,}  ({idx[0].date()} → {idx[split-1].date()})")
print(f"Prueba:        {len(X_test):,}  ({idx_test[0].date()} → {idx_test[-1].date()})")

# Escalado para SVR
scaler_X = StandardScaler().fit(X_train)
scaler_y = StandardScaler().fit(y_train.reshape(-1, 1))
X_train_sc = scaler_X.transform(X_train)
X_test_sc  = scaler_X.transform(X_test)
y_train_sc = scaler_y.transform(y_train.reshape(-1, 1)).ravel()

# Submuestra para SVR (los más recientes = más representativos)
if len(X_train_sc) > SVR_MAX_TRAIN:
    X_svr = X_train_sc[-SVR_MAX_TRAIN:]
    y_svr = y_train_sc[-SVR_MAX_TRAIN:]
    print(f"\n  [SVR] Entrenamiento limitado a {SVR_MAX_TRAIN:,} muestras")
else:
    X_svr, y_svr = X_train_sc, y_train_sc

# =============================================================================
# 4. ENTRENAMIENTO
# =============================================================================
print("\n" + "=" * 65)
print("4. ENTRENAMIENTO DE MODELOS")
print("=" * 65)

print("  Entrenando Random Forest  ...", end=' ', flush=True)
rf = RandomForestRegressor(n_estimators=200, max_depth=20,
                           min_samples_leaf=5, n_jobs=-1, random_state=42)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)
print("listo")

print("  Entrenando XGBoost        ...", end=' ', flush=True)
xgb = XGBRegressor(n_estimators=200, max_depth=6, learning_rate=0.05,
                   subsample=0.8, colsample_bytree=0.8,
                   tree_method='hist', random_state=42, verbosity=0)
xgb.fit(X_train, y_train)
y_pred_xgb = xgb.predict(X_test)
print("listo")

print("  Entrenando SVR            ...", end=' ', flush=True)
svr = SVR(kernel='rbf', C=10.0, epsilon=0.05, gamma='scale')
svr.fit(X_svr, y_svr)
y_pred_svr = scaler_y.inverse_transform(
    svr.predict(X_test_sc).reshape(-1, 1)
).ravel()
print("listo")

# =============================================================================
# 5. MÉTRICAS
# =============================================================================
print("\n" + "=" * 65)
print("5. MÉTRICAS DE EVALUACIÓN")
print("=" * 65)

resultados = [
    calcular_metricas(y_test, y_pred_rf,  'Random Forest'),
    calcular_metricas(y_test, y_pred_xgb, 'XGBoost'),
    calcular_metricas(y_test, y_pred_svr, 'SVR'),
]
df_met = pd.DataFrame(resultados).set_index('Modelo')
print(f"\n{df_met.to_string()}")

df_met.to_csv(os.path.join(MOD_DIR, f'metricas_escenario{ESCENARIO}.csv'))
print(f"\n✓ Métricas guardadas → modelos/metricas_escenario{ESCENARIO}.csv")

# =============================================================================
# 6. VISUALIZACIONES
# =============================================================================
print("\n" + "=" * 65)
print("6. VISUALIZACIONES")
print("=" * 65)

# 6.1 Serie resampleada completa
fig, ax = plt.subplots(figsize=(15, 4))
serie_d = df['GAP'].resample('D').mean()
ax.plot(serie_d.index, serie_d.values, color='#1565C0', linewidth=0.8, alpha=0.9)
ax.axvline(idx_test[0], color='red', linestyle='--', linewidth=1.5,
           label=f'Inicio test: {idx_test[0].date()}')
ax.set_title(f'Escenario {ESCENARIO} ({FREQ_LABEL}) — GAP Resampleado (promedio diario)',
             fontweight='bold')
ax.set_ylabel('GAP (kW)')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
plt.setp(ax.get_xticklabels(), rotation=30, ha='right', fontsize=8)
ax.legend()
savefig(f'e{ESCENARIO}_01_serie_resampleada.png')
print(f"  ✓ Gráfico 1: serie resampleada")

# 6.2 Predicciones vs real (primeros N_VIZ puntos del test)
fig, ax = plt.subplots(figsize=(15, 5))
ax.plot(idx_test[:N_VIZ], y_test[:N_VIZ],
        color='black', linewidth=1.3, label='Real', zorder=5)
for nombre, y_pred in [('Random Forest', y_pred_rf),
                        ('XGBoost', y_pred_xgb),
                        ('SVR', y_pred_svr)]:
    ax.plot(idx_test[:N_VIZ], y_pred[:N_VIZ],
            color=COLORES[nombre], linewidth=0.8, alpha=0.85, label=nombre)
ax.set_title(f'Escenario {ESCENARIO} — Predicciones vs Real (primeros {N_VIZ} puntos del test)',
             fontweight='bold')
ax.set_ylabel('GAP (kW)')
ax.legend()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
plt.setp(ax.get_xticklabels(), rotation=30, ha='right', fontsize=8)
savefig(f'e{ESCENARIO}_02_predicciones.png')
print(f"  ✓ Gráfico 2: predicciones vs real")

# 6.3 Scatter predicho vs real
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
for ax, (nombre, y_pred) in zip(axes, [('Random Forest', y_pred_rf),
                                         ('XGBoost', y_pred_xgb),
                                         ('SVR', y_pred_svr)]):
    met = df_met.loc[nombre]
    ax.scatter(y_test, y_pred, alpha=0.15, s=2, color=COLORES[nombre])
    lim = [min(y_test.min(), y_pred.min()), max(y_test.max(), y_pred.max())]
    ax.plot(lim, lim, 'k--', linewidth=1.2)
    ax.set_title(f'{nombre}\nR²={met["R2"]:.4f}  RMSE={met["RMSE"]:.4f}',
                 fontweight='bold', fontsize=10)
    ax.set_xlabel('Real (kW)')
    ax.set_ylabel('Predicho (kW)')
plt.suptitle(f'Escenario {ESCENARIO} — Scatter: Predicho vs Real',
             fontsize=12, fontweight='bold')
savefig(f'e{ESCENARIO}_03_scatter.png')
print(f"  ✓ Gráfico 3: scatter")

# 6.4 Comparación de métricas
fig, axes = plt.subplots(1, 4, figsize=(16, 5))
modelos_names = df_met.index.tolist()
bar_colors    = [COLORES[m] for m in modelos_names]
for ax, col in zip(axes, ['RMSE', 'MAE', 'MAPE', 'R2']):
    vals = df_met[col].values
    bars = ax.bar(modelos_names, vals, color=bar_colors, edgecolor='black', linewidth=0.5)
    ax.set_title(col, fontweight='bold')
    ax.tick_params(axis='x', rotation=20)
    for bar, v in zip(bars, vals):
        label = f'{v:.2f}%' if col == 'MAPE' else f'{v:.4f}'
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + max(vals) * 0.015,
                label, ha='center', va='bottom', fontsize=8)
plt.suptitle(f'Escenario {ESCENARIO} ({FREQ_LABEL}) — Comparación de Métricas',
             fontsize=12, fontweight='bold')
savefig(f'e{ESCENARIO}_04_metricas.png')
print(f"  ✓ Gráfico 4: métricas")

# 6.5 Importancia de features (RF y XGBoost)
N_TOP = 15
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
for ax, (nombre, importancias, color) in zip(axes, [
    ('Random Forest', rf.feature_importances_,  '#1565C0'),
    ('XGBoost',       xgb.feature_importances_, '#2E7D32'),
]):
    feat_imp = (pd.Series(importancias, index=FEATURES)
                .sort_values(ascending=True)
                .tail(N_TOP))
    feat_imp.plot(kind='barh', ax=ax, color=color, edgecolor='black', linewidth=0.4)
    ax.set_title(f'Top {N_TOP} Features — {nombre}', fontweight='bold')
    ax.set_xlabel('Importancia')
plt.suptitle(f'Escenario {ESCENARIO} — Importancia de Features',
             fontsize=12, fontweight='bold')
savefig(f'e{ESCENARIO}_05_importancia.png')
print(f"  ✓ Gráfico 5: importancia de features")

# =============================================================================
# RESUMEN FINAL
# =============================================================================
print("\n" + "=" * 65)
print(f"RESUMEN — ESCENARIO {ESCENARIO} ({FREQ_LABEL})")
print("=" * 65)
print(f"  Registros resampleados: {len(df):,}")
print(f"  Features:               {len(FEATURES)}")
print(f"  Train: {len(X_train):,}  |  Test: {len(X_test):,}")
print(f"\n{df_met.to_string()}")
mejor = df_met['R2'].idxmax()
print(f"\n  Mejor modelo (R²): {mejor}  →  R²={df_met.loc[mejor,'R2']:.4f}")
print(f"\n✓ Escenario {ESCENARIO} completado exitosamente.")
