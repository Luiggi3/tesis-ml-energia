# =============================================================================
# ESCENARIO 3 — RESAMPLE A 1 DÍA + MODELOS ML
# Tesis: Modelo predictivo del consumo energético en hogares inteligentes
# Modelos: Random Forest | XGBoost | SVR  +  Baselines: Persistencia | Reg. Lineal
# Métricas: RMSE | MAE | MAPE | sMAPE | WAPE | nRMSE | MASE | R²
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
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.compose import TransformedTargetRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from xgboost import XGBRegressor

warnings.filterwarnings('ignore')
plt.rcParams.update({'figure.dpi': 200, 'font.size': 15})

# ── CONFIGURACIÓN ─────────────────────────────────────────────────────────────
ESCENARIO     = 3
FREQ          = 'D'
FREQ_LABEL    = '1 Día'
LAG_LABEL     = '1 Day'                 # equivalencia de 1 lag, para gráficos en eje 'Time Lag'
HORIZON       = 7                       # pasos hacia adelante = 7 días (1 semana) a resolución diaria
HORIZON_LABEL = '7 Días (1 Semana)'
LAGS_GAP      = [1, 2, 3, 7, 14, 30]   # 30 días = ~1 mes
ROLL_WINDOWS  = [7, 14, 30]
TRAIN_RATIO   = 0.80
TRAIN_WINDOW  = None                    # sin límite: dataset pequeño (~1 400 filas)
N_VIZ         = None                    # mostrar todo el test set

_here = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = _here if os.path.exists(os.path.join(_here, 'datos')) else os.path.dirname(_here)
DATA_CSV = os.path.join(BASE_DIR, 'datos', 'dataset_limpio.csv')
GRAF_DIR = os.path.join(BASE_DIR, 'graficos', f'escenario{ESCENARIO}')
MOD_DIR  = os.path.join(BASE_DIR, 'modelos')
os.makedirs(GRAF_DIR, exist_ok=True)
os.makedirs(MOD_DIR,  exist_ok=True)

COLORES = {'Random Forest': '#1565C0', 'XGBoost': '#2E7D32', 'SVR': '#B71C1C',
           'Persistencia': '#757575', 'Regresión Lineal': '#F9A825'}
ABREV   = {'Random Forest': 'RF', 'XGBoost': 'XGB', 'SVR': 'SVR',
           'Persistencia': 'Persist.', 'Regresión Lineal': 'Reg. Lineal'}

def savefig(nombre):
    plt.tight_layout()
    plt.savefig(os.path.join(GRAF_DIR, nombre), dpi=200, bbox_inches='tight')
    plt.show()
    plt.close()

def calcular_metricas(y_true, y_pred, nombre, mae_naive=None):
    yt, yp = np.array(y_true), np.array(y_pred)
    rmse = np.sqrt(mean_squared_error(yt, yp))
    mae  = mean_absolute_error(yt, yp)
    mask = yt > 0.01
    mape  = np.mean(np.abs((yt[mask] - yp[mask]) / yt[mask])) * 100
    smape = np.mean(2 * np.abs(yt - yp) / (np.abs(yt) + np.abs(yp) + 1e-6)) * 100
    wape  = np.sum(np.abs(yt - yp)) / np.sum(np.abs(yt)) * 100
    nrmse = rmse / np.mean(yt) * 100
    mase  = mae / mae_naive if mae_naive else np.nan
    r2    = r2_score(yt, yp)
    return {'Modelo': nombre,
            'RMSE' : round(rmse,  4),
            'MAE'  : round(mae,   4),
            'MAPE' : round(mape,  2),
            'sMAPE': round(smape, 2),
            'WAPE' : round(wape,  2),
            'nRMSE': round(nrmse, 2),
            'MASE' : round(mase,  4) if mae_naive else np.nan,
            'R2'   : round(r2,    4)}

# =============================================================================
# 1. CARGA Y RESAMPLE
# =============================================================================
print("=" * 65)
print(f"ESCENARIO {ESCENARIO} — RESAMPLE A {FREQ_LABEL}")
print(f"HORIZONTE DE PREDICCIÓN: {HORIZON} pasos → {HORIZON_LABEL}")
print("=" * 65)

df_raw = pd.read_csv(DATA_CSV, index_col='datetime', parse_dates=True)
df_raw = df_raw[['GAP', 'GRP', 'VOLT', 'GI', 'SM1', 'SM2', 'SM3']]

print(f"Dataset limpio cargado: {len(df_raw):,} registros a 1 minuto")

df = df_raw.resample(FREQ).mean().dropna()

print(f"Tras resample a {FREQ_LABEL}: {len(df):,} registros")
print(f"Período: {df.index.min().date()} → {df.index.max().date()}")
print(f"\nEstadísticas descriptivas:")
print(df.describe().round(3).to_string())

# =============================================================================
# 2. FEATURE ENGINEERING
# =============================================================================
print("\n" + "=" * 65)
print("2. FEATURE ENGINEERING")
print("=" * 65)

df = df.drop(columns=['GI'])  # correlación 0.999 con GAP

# Temporales — para datos diarios no se incluye 'hora'
df['dia_semana'] = df.index.dayofweek
df['mes']        = df.index.month
df['trimestre']  = df.index.quarter
df['dia_anio']   = df.index.dayofyear
df['es_finde']   = df['dia_semana'].isin([5, 6]).astype(int)

# Lags de GAP
for lag in LAGS_GAP:
    df[f'GAP_lag_{lag}'] = df['GAP'].shift(lag)

# Rolling de GAP
for w in ROLL_WINDOWS:
    df[f'GAP_roll_mean_{w}'] = df['GAP'].shift(1).rolling(w).mean()
    df[f'GAP_roll_std_{w}']  = df['GAP'].shift(1).rolling(w).std()

# Target: GAP desplazado HORIZON pasos hacia el futuro (predicción real, no nowcasting)
df['GAP_lag_0'] = df['GAP']                    # valor actual — antes excluido por ser el target
df['target']    = df['GAP'].shift(-HORIZON)
df = df.dropna()

FEATURES = [c for c in df.columns if c not in ('GAP', 'target')]
IDX_LAG0 = FEATURES.index('GAP_lag_0')
print(f"Registros tras features: {len(df):,}")
print(f"Features: {len(FEATURES)}")
print(f"  {FEATURES}")

# =============================================================================
# 3. SPLIT CRONOLÓGICO 80 / 20
# =============================================================================
print("\n" + "=" * 65)
print("3. SPLIT CRONOLÓGICO (80 / 20)")
print("=" * 65)

X, y, idx = df[FEATURES].values, df['target'].values, df.index
idx_target = df.index.shift(HORIZON, freq=FREQ)   # timestamp real de lo que se predice
split = int(len(df) * TRAIN_RATIO)

X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]
idx_test          = idx[split:]
idx_target_test   = idx_target[split:]

print(f"Entrenamiento: {len(X_train):,} días  ({idx[0].date()} → {idx[split-1].date()})")
print(f"Prueba:        {len(X_test):,} días  ({idx_test[0].date()} → {idx_test[-1].date()})")

# Ventana de entrenamiento unificada: los 3 modelos (RF, XGB, SVR) y la
# Regresión Lineal ven exactamente los mismos datos, para una comparación justa.
if TRAIN_WINDOW and len(X_train) > TRAIN_WINDOW:
    X_train_used = X_train[-TRAIN_WINDOW:]
    y_train_used = y_train[-TRAIN_WINDOW:]
    print(f"\n  Ventana de entrenamiento unificada: últimas {TRAIN_WINDOW:,} filas "
          f"(de {len(X_train):,}) para RF, XGBoost, SVR y Regresión Lineal")
else:
    X_train_used, y_train_used = X_train, y_train  # dataset pequeño, sin límite

# =============================================================================
# 4. ENTRENAMIENTO
# =============================================================================
print("\n" + "=" * 65)
print("4. ENTRENAMIENTO DE MODELOS")
print("=" * 65)

print("  Entrenando Random Forest  ...", end=' ', flush=True)
rf = RandomForestRegressor(n_estimators=200, max_depth=15,
                           min_samples_leaf=3, n_jobs=-1, random_state=42)
rf.fit(X_train_used, y_train_used)
y_pred_rf = rf.predict(X_test)
print("listo")

print("  Entrenando XGBoost        ...", end=' ', flush=True)
xgb = XGBRegressor(n_estimators=200, max_depth=4, learning_rate=0.05,
                   subsample=0.8, colsample_bytree=0.8,
                   tree_method='hist', random_state=42, verbosity=0)
xgb.fit(X_train_used, y_train_used)
y_pred_xgb = xgb.predict(X_test)
print("listo")

print("  Entrenando SVR            ...", end=' ', flush=True)
svr = TransformedTargetRegressor(
    regressor=Pipeline([('scaler', StandardScaler()),
                         ('svr', SVR(kernel='rbf', C=10.0, epsilon=0.05, gamma='scale'))]),
    transformer=StandardScaler(),
)
svr.fit(X_train_used, y_train_used)
y_pred_svr = svr.predict(X_test)
print("listo")

print("  Baseline: Persistencia    ...", end=' ', flush=True)
y_pred_persist = X_test[:, IDX_LAG0]   # ŷ(t+H) = y(t) — el valor actual de GAP
print("listo")

print("  Baseline: Regresión Lineal...", end=' ', flush=True)
lr = Pipeline([('scaler', StandardScaler()), ('linreg', LinearRegression())])
lr.fit(X_train_used, y_train_used)
y_pred_lr = lr.predict(X_test)
print("listo")

# =============================================================================
# 5. MÉTRICAS
# =============================================================================
print("\n" + "=" * 65)
print("5. MÉTRICAS DE EVALUACIÓN")
print("=" * 65)

met_persist  = calcular_metricas(y_test, y_pred_persist, 'Persistencia')
mae_naive    = met_persist['MAE']

resultados = [
    calcular_metricas(y_test, y_pred_rf,     'Random Forest',    mae_naive),
    calcular_metricas(y_test, y_pred_xgb,    'XGBoost',          mae_naive),
    calcular_metricas(y_test, y_pred_svr,    'SVR',              mae_naive),
    met_persist,
    calcular_metricas(y_test, y_pred_lr,     'Regresión Lineal', mae_naive),
]
df_met = pd.DataFrame(resultados).set_index('Modelo')
print(f"\n{df_met.to_string()}")

df_met.to_csv(os.path.join(MOD_DIR, f'metricas_escenario{ESCENARIO}.csv'))
print(f"\n✓ Métricas guardadas → modelos/metricas_escenario{ESCENARIO}.csv")

# Exportar predicciones fila a fila (para el test de Diebold-Mariano)
df_pred = pd.DataFrame({
    'datetime'           : idx_target_test,
    'y_real'             : y_test,
    'y_pred_rf'          : y_pred_rf,
    'y_pred_xgb'         : y_pred_xgb,
    'y_pred_svr'         : y_pred_svr,
    'y_pred_persistencia': y_pred_persist,
    'y_pred_lr'          : y_pred_lr,
})
df_pred.to_csv(os.path.join(MOD_DIR, f'predicciones_escenario{ESCENARIO}.csv'), index=False)
print(f"✓ Predicciones guardadas → modelos/predicciones_escenario{ESCENARIO}.csv")

# =============================================================================
# 6. VISUALIZACIONES
# =============================================================================
print("\n" + "=" * 65)
print("6. VISUALIZACIONES")
print("=" * 65)

N_plot = len(idx_test) if N_VIZ is None else min(N_VIZ, len(idx_test))

# 6.1 Curva de carga eléctrica por Time Lag (train en negro, test en rojo)
lags_idx = np.arange(len(df))
fig, ax = plt.subplots(figsize=(15, 4))
ax.plot(lags_idx[:split], df['GAP'].values[:split],
        color='black', linewidth=0.6, label='Train')
ax.plot(lags_idx[split:], df['GAP'].values[split:],
        color='red', linewidth=0.6, label='Test')
ax.set_title(f'Escenario {ESCENARIO} ({FREQ_LABEL}) — Curva de Carga Eléctrica (GAP)',
             fontweight='bold')
ax.set_xlabel(f'Time Lag (1 lag = {LAG_LABEL})')
ax.set_ylabel('GAP (kW)')
ax.legend(framealpha=1)
savefig(f'e{ESCENARIO}_01_time_lag_train_test.png')
print(f"  ✓ Gráfico 1: curva de carga por time lag (train/test)")

# 6.2 Predicciones vs real (todo el test set)
fig, ax = plt.subplots(figsize=(15, 5))
ax.plot(idx_target_test[:N_plot], y_test[:N_plot],
        color='black', linewidth=1.5, label='Real', zorder=5)
for nombre, y_pred in [('Random Forest', y_pred_rf),
                        ('XGBoost', y_pred_xgb),
                        ('SVR', y_pred_svr),
                        ('Persistencia', y_pred_persist),
                        ('Regresión Lineal', y_pred_lr)]:
    estilo = dict(linewidth=1.0, alpha=0.85)
    if nombre in ('Persistencia', 'Regresión Lineal'):
        estilo = dict(linewidth=1.1, alpha=0.7, linestyle='--')
    ax.plot(idx_target_test[:N_plot], y_pred[:N_plot],
            color=COLORES[nombre], label=nombre, **estilo)
ax.set_title(f'Escenario {ESCENARIO} ({FREQ_LABEL}) — Predicciones vs Real '
             f'(horizonte: {HORIZON_LABEL}, conjunto de prueba completo)',
             fontweight='bold')
ax.set_ylabel('GAP (kW)')
ax.legend(framealpha=1)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
plt.setp(ax.get_xticklabels(), rotation=30, ha='right', fontsize=11.2)
savefig(f'e{ESCENARIO}_02_predicciones.png')
print(f"  ✓ Gráfico 2: predicciones vs real")

# 6.3 Scatter predicho vs real (modelos ML)
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
for ax, (nombre, y_pred) in zip(axes, [('Random Forest', y_pred_rf),
                                         ('XGBoost', y_pred_xgb),
                                         ('SVR', y_pred_svr)]):
    met = df_met.loc[nombre]
    ax.scatter(y_test, y_pred, alpha=0.6, s=30, color=COLORES[nombre],
               edgecolors='black', linewidths=0.3)
    lim = [min(y_test.min(), y_pred.min()), max(y_test.max(), y_pred.max())]
    ax.plot(lim, lim, 'k--', linewidth=1.2)
    ax.set_title(f'{nombre}\nR²={met["R2"]:.4f}  RMSE={met["RMSE"]:.4f}',
                 fontweight='bold', fontsize=14)
    ax.set_xlabel('Real (kW)')
    ax.set_ylabel('Predicho (kW)')
plt.suptitle(f'Escenario {ESCENARIO} — Scatter: Predicho vs Real',
             fontsize=16.8, fontweight='bold')
savefig(f'e{ESCENARIO}_03_scatter.png')
print(f"  ✓ Gráfico 3: scatter")

# 6.4 Comparación de métricas (todos los modelos + baselines)
fig, axes = plt.subplots(1, 4, figsize=(18, 5))
modelos_names  = df_met.index.tolist()
modelos_abrev  = [ABREV[m] for m in modelos_names]
bar_colors     = [COLORES[m] for m in modelos_names]
for ax, col in zip(axes, ['RMSE', 'MAE', 'MAPE', 'R2']):
    vals = df_met[col].values
    ymin_col = min(0, vals.min())
    ymax_col = max(0, vals.max())
    rango = ymax_col - ymin_col
    bars = ax.bar(modelos_abrev, vals, color=bar_colors, edgecolor='black', linewidth=0.5)
    ax.set_title(col, fontweight='bold')
    ax.tick_params(axis='x', rotation=0, labelsize=11.5)
    for bar, v in zip(bars, vals):
        label = f'{v:.2f}%' if col == 'MAPE' else f'{v:.4f}'
        signo = 1 if v >= 0 else -1
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + signo * rango * 0.02,
                label, ha='center', va='bottom' if v >= 0 else 'top', fontsize=10)
    # Deja espacio de sobra arriba, y espacio abajo cuando hay valores
    # negativos (R² puede serlo), para que ni las barras ni sus etiquetas
    # queden cortadas o choquen con el eje X.
    ax.set_ylim(ymin_col - rango * 0.15, ymax_col + rango * 0.25)
    if ymin_col < 0:
        ax.axhline(0, color='black', linewidth=0.6)
plt.suptitle(f'Escenario {ESCENARIO} ({FREQ_LABEL}) — Comparación de Métricas '
             f'(modelos ML y baselines)',
             fontsize=16.8, fontweight='bold')
savefig(f'e{ESCENARIO}_04_metricas.png')
print(f"  ✓ Gráfico 4: métricas")

# 6.5 Importancia de features (RF, XGBoost) + coeficientes (Regresión Lineal)
N_TOP = min(15, len(FEATURES))
fig, axes = plt.subplots(1, 3, figsize=(20, 6))
for ax, (nombre, importancias, color) in zip(axes, [
    ('Random Forest',    rf.feature_importances_,               '#1565C0'),
    ('XGBoost',          xgb.feature_importances_,              '#2E7D32'),
    ('Regresión Lineal', np.abs(lr.named_steps['linreg'].coef_), '#F9A825'),
]):
    etiqueta = 'Importancia' if nombre != 'Regresión Lineal' else '|Coeficiente| (estandarizado)'
    feat_imp = (pd.Series(importancias, index=FEATURES)
                .sort_values(ascending=True)
                .tail(N_TOP))
    feat_imp.plot(kind='barh', ax=ax, color=color, edgecolor='black', linewidth=0.4)
    ax.set_title(f'Top {N_TOP} Features — {nombre}', fontweight='bold')
    ax.set_xlabel(etiqueta)
plt.suptitle(f'Escenario {ESCENARIO} — Importancia de Features',
             fontsize=16.8, fontweight='bold')
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
print(f"  Train: {len(X_train):,}  |  Train usado: {len(X_train_used):,}  |  Test: {len(X_test):,}")
print(f"\n{df_met.to_string()}")
mejor = df_met['R2'].idxmax()
print(f"\n  Mejor modelo (R²): {mejor}  →  R²={df_met.loc[mejor,'R2']:.4f}")
print(f"\n✓ Escenario {ESCENARIO} completado exitosamente.")
