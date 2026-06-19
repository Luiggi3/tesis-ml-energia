# =============================================================================
# TUNING DE HIPERPARÁMETROS — GridSearchCV + TimeSeriesSplit
# Tesis: Modelo predictivo del consumo energético en hogares inteligentes
# Escenarios: 15 min | 1 hora | 1 día
# Modelos: Random Forest | XGBoost | SVR
# =============================================================================

import matplotlib
# matplotlib.use('Agg')  # desactivado: permite ver gráficos en Spyder
import os, warnings, time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from xgboost import XGBRegressor

warnings.filterwarnings('ignore')
plt.rcParams.update({'figure.dpi': 150, 'font.size': 10})

_here = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = _here if os.path.exists(os.path.join(_here, 'datos')) else os.path.dirname(_here)
DATA_CSV = os.path.join(BASE_DIR, 'datos', 'dataset_limpio.csv')
MOD_DIR  = os.path.join(BASE_DIR, 'modelos')
GRAF_DIR = os.path.join(BASE_DIR, 'graficos', 'tuning')
os.makedirs(MOD_DIR,  exist_ok=True)
os.makedirs(GRAF_DIR, exist_ok=True)

COLORES  = {'Random Forest': '#1565C0', 'XGBoost': '#2E7D32', 'SVR': '#B71C1C'}
CV_FOLDS = 3

# ── Grillas de hiperparámetros ───────────────────────────────────────────────
# Random Forest: 3×3×3 = 27 combinaciones
GRID_RF = {
    'n_estimators':     [100, 200, 300],
    'max_depth':        [10, 20, None],
    'min_samples_leaf': [1, 5, 10],
}

# XGBoost: 2×3×2×2 = 24 combinaciones (colsample_bytree fijo en 0.8)
GRID_XGB = {
    'n_estimators':  [100, 200],
    'max_depth':     [4, 6, 8],
    'learning_rate': [0.05, 0.1],
    'subsample':     [0.8, 1.0],
}

# SVR: 3×3×2 = 18 combinaciones
GRID_SVR = {
    'C':       [1, 10, 100],
    'epsilon': [0.01, 0.05, 0.1],
    'gamma':   ['scale', 0.01],
}

# ── Configuración por escenario ──────────────────────────────────────────────
ESCENARIOS = [
    {
        'num': 1, 'freq': '15min', 'label': '15 Minutos',
        'lags':  [1, 2, 4, 8, 12, 96],
        'rolls': [4, 8, 96],
        'svr_max': 15_000,
        'gs_max':  30_000,   # muestras para CV (últimas = más representativas)
        'rf_base':  dict(n_estimators=200, max_depth=20, min_samples_leaf=5),
        'xgb_base': dict(n_estimators=200, max_depth=6, learning_rate=0.05,
                         subsample=0.8, colsample_bytree=0.8),
        'svr_base': dict(C=10.0, epsilon=0.05, gamma='scale'),
    },
    {
        'num': 2, 'freq': 'h', 'label': '1 Hora',
        'lags':  [1, 2, 3, 6, 12, 24, 48, 168],
        'rolls': [6, 24, 168],
        'svr_max': 10_000,
        'gs_max':  None,
        'rf_base':  dict(n_estimators=200, max_depth=20, min_samples_leaf=5),
        'xgb_base': dict(n_estimators=200, max_depth=6, learning_rate=0.05,
                         subsample=0.8, colsample_bytree=0.8),
        'svr_base': dict(C=10.0, epsilon=0.05, gamma='scale'),
    },
    {
        'num': 3, 'freq': 'D', 'label': '1 Día',
        'lags':  [1, 2, 3, 7, 14, 30],
        'rolls': [7, 14, 30],
        'svr_max': None,
        'gs_max':  None,
        'rf_base':  dict(n_estimators=200, max_depth=15, min_samples_leaf=3),
        'xgb_base': dict(n_estimators=200, max_depth=4, learning_rate=0.05,
                         subsample=0.8, colsample_bytree=0.8),
        'svr_base': dict(C=10.0, epsilon=0.05, gamma='scale'),
    },
]

# =============================================================================
# FUNCIONES AUXILIARES
# =============================================================================

def calcular_metricas(y_true, y_pred):
    yt, yp = np.array(y_true), np.array(y_pred)
    rmse = np.sqrt(mean_squared_error(yt, yp))
    mae  = mean_absolute_error(yt, yp)
    mask = yt > 0.01
    mape = np.mean(np.abs((yt[mask] - yp[mask]) / yt[mask])) * 100
    r2   = r2_score(yt, yp)
    return {'RMSE': round(rmse, 4), 'MAE': round(mae, 4),
            'MAPE': round(mape, 2), 'R2': round(r2, 4)}


def preparar_datos(cfg):
    df_raw = pd.read_csv(DATA_CSV, index_col='datetime', parse_dates=True)
    df = df_raw[['GAP', 'GRP', 'VOLT', 'GI', 'SM1', 'SM2', 'SM3']]
    df = df.resample(cfg['freq']).mean().dropna()
    df = df.drop(columns=['GI'])

    if cfg['freq'] != 'D':
        df['hora'] = df.index.hour
    df['dia_semana'] = df.index.dayofweek
    df['mes']        = df.index.month
    df['es_finde']   = df['dia_semana'].isin([5, 6]).astype(int)
    if cfg['freq'] == 'D':
        df['trimestre'] = df.index.quarter
        df['dia_anio']  = df.index.dayofyear

    for lag in cfg['lags']:
        df[f'GAP_lag_{lag}'] = df['GAP'].shift(lag)
    for w in cfg['rolls']:
        df[f'GAP_roll_mean_{w}'] = df['GAP'].shift(1).rolling(w).mean()
        df[f'GAP_roll_std_{w}']  = df['GAP'].shift(1).rolling(w).std()

    df = df.dropna()
    features = [c for c in df.columns if c != 'GAP']

    X, y = df[features].values, df['GAP'].values
    split = int(len(df) * 0.80)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    scaler_X = StandardScaler().fit(X_train)
    scaler_y = StandardScaler().fit(y_train.reshape(-1, 1))
    X_train_sc = scaler_X.transform(X_train)
    X_test_sc  = scaler_X.transform(X_test)
    y_train_sc = scaler_y.transform(y_train.reshape(-1, 1)).ravel()

    return (X_train, X_test, y_train, y_test,
            X_train_sc, X_test_sc, y_train_sc, scaler_y, features)


def run_gridsearch(estimator, param_grid, X_cv, y_cv, n_combos):
    tscv = TimeSeriesSplit(n_splits=CV_FOLDS)
    gs = GridSearchCV(
        estimator, param_grid,
        cv=tscv, scoring='r2',
        n_jobs=-1, refit=False, verbose=0,
    )
    t0 = time.time()
    gs.fit(X_cv, y_cv)
    elapsed = time.time() - t0
    print(f"      {n_combos} combos × {CV_FOLDS} folds = {n_combos*CV_FOLDS} fits  |  "
          f"{elapsed:.1f}s  |  Mejor CV R²={gs.best_score_:.4f}")
    print(f"      Mejores parámetros: {gs.best_params_}")
    return gs.best_params_, round(gs.best_score_, 4)


# =============================================================================
# LOOP PRINCIPAL
# =============================================================================

print("=" * 70)
print("TUNING DE HIPERPARÁMETROS — GridSearchCV + TimeSeriesSplit")
print(f"CV Folds: {CV_FOLDS}  |  Scoring: R²")
print("=" * 70)
print(f"\nGrids de búsqueda:")
print(f"  Random Forest : {27} combinaciones  {GRID_RF}")
print(f"  XGBoost       : {24} combinaciones  {GRID_XGB}")
print(f"  SVR           : {18} combinaciones  {GRID_SVR}")

todos_resultados = []
t_total = time.time()

for cfg in ESCENARIOS:
    num, label = cfg['num'], cfg['label']

    print(f"\n{'='*70}")
    print(f"ESCENARIO {num} — {label}")
    print(f"{'='*70}")

    (X_train, X_test, y_train, y_test,
     X_train_sc, X_test_sc, y_train_sc, scaler_y,
     features) = preparar_datos(cfg)

    print(f"  Train: {len(X_train):,}  |  Test: {len(X_test):,}  |  Features: {len(features)}")

    # Submuestra para GridSearchCV en RF y XGBoost (E1 sólo)
    gs_max = cfg['gs_max']
    if gs_max and len(X_train) > gs_max:
        X_cv, y_cv = X_train[-gs_max:], y_train[-gs_max:]
        print(f"  [GridSearch RF/XGB] Submuestra CV: últimas {gs_max:,} filas del train")
    else:
        X_cv, y_cv = X_train, y_train

    # Submuestra para SVR
    svr_max = cfg['svr_max']
    if svr_max and len(X_train_sc) > svr_max:
        X_svr = X_train_sc[-svr_max:]
        y_svr = y_train_sc[-svr_max:]
        print(f"  [SVR] Submuestra: últimas {svr_max:,} filas del train (escaladas)")
    else:
        X_svr, y_svr = X_train_sc, y_train_sc

    # ── RANDOM FOREST ───────────────────────────────────────────────────────
    print(f"\n  [Random Forest]  ({len(X_cv):,} muestras en CV)")

    rf_base = RandomForestRegressor(**cfg['rf_base'], n_jobs=-1, random_state=42)
    rf_base.fit(X_train, y_train)
    met_rf_base = calcular_metricas(y_test, rf_base.predict(X_test))
    print(f"    Base  →  R²={met_rf_base['R2']:.4f}  RMSE={met_rf_base['RMSE']:.4f}")

    print(f"    GridSearchCV ...")
    best_rf, cv_r2_rf = run_gridsearch(
        RandomForestRegressor(n_jobs=-1, random_state=42),
        GRID_RF, X_cv, y_cv, 27,
    )

    rf_tuned = RandomForestRegressor(**best_rf, n_jobs=-1, random_state=42)
    rf_tuned.fit(X_train, y_train)
    met_rf_tuned = calcular_metricas(y_test, rf_tuned.predict(X_test))
    delta_r2 = met_rf_tuned['R2'] - met_rf_base['R2']
    print(f"    Tuned →  R²={met_rf_tuned['R2']:.4f}  RMSE={met_rf_tuned['RMSE']:.4f}  "
          f"(ΔR²={delta_r2:+.4f})")

    for etapa, met, params, cv_r2 in [
        ('Base',  met_rf_base,  cfg['rf_base'], None),
        ('Tuned', met_rf_tuned, best_rf,        cv_r2_rf),
    ]:
        todos_resultados.append({
            'Escenario': label, 'Modelo': 'Random Forest', 'Etapa': etapa,
            **met, 'CV_R2': cv_r2, 'Params': str(params),
        })

    # ── XGBOOST ────────────────────────────────────────────────────────────
    print(f"\n  [XGBoost]  ({len(X_cv):,} muestras en CV)")

    xgb_base = XGBRegressor(**cfg['xgb_base'], tree_method='hist',
                            random_state=42, verbosity=0)
    xgb_base.fit(X_train, y_train)
    met_xgb_base = calcular_metricas(y_test, xgb_base.predict(X_test))
    print(f"    Base  →  R²={met_xgb_base['R2']:.4f}  RMSE={met_xgb_base['RMSE']:.4f}")

    print(f"    GridSearchCV ...")
    best_xgb, cv_r2_xgb = run_gridsearch(
        XGBRegressor(colsample_bytree=0.8, tree_method='hist',
                     random_state=42, verbosity=0),
        GRID_XGB, X_cv, y_cv, 24,
    )

    xgb_tuned = XGBRegressor(**best_xgb, colsample_bytree=0.8,
                             tree_method='hist', random_state=42, verbosity=0)
    xgb_tuned.fit(X_train, y_train)
    met_xgb_tuned = calcular_metricas(y_test, xgb_tuned.predict(X_test))
    delta_r2 = met_xgb_tuned['R2'] - met_xgb_base['R2']
    print(f"    Tuned →  R²={met_xgb_tuned['R2']:.4f}  RMSE={met_xgb_tuned['RMSE']:.4f}  "
          f"(ΔR²={delta_r2:+.4f})")

    for etapa, met, params, cv_r2 in [
        ('Base',  met_xgb_base,  cfg['xgb_base'], None),
        ('Tuned', met_xgb_tuned, best_xgb,        cv_r2_xgb),
    ]:
        todos_resultados.append({
            'Escenario': label, 'Modelo': 'XGBoost', 'Etapa': etapa,
            **met, 'CV_R2': cv_r2, 'Params': str(params),
        })

    # ── SVR ────────────────────────────────────────────────────────────────
    print(f"\n  [SVR]  ({len(X_svr):,} muestras en CV, escaladas)")

    svr_base = SVR(kernel='rbf', **cfg['svr_base'])
    svr_base.fit(X_svr, y_svr)
    y_pred_svr_base = scaler_y.inverse_transform(
        svr_base.predict(X_test_sc).reshape(-1, 1)).ravel()
    met_svr_base = calcular_metricas(y_test, y_pred_svr_base)
    print(f"    Base  →  R²={met_svr_base['R2']:.4f}  RMSE={met_svr_base['RMSE']:.4f}")

    # GridSearchCV sobre datos escalados (y también escalado → R² interno en escala norm.)
    print(f"    GridSearchCV ...")
    best_svr, cv_r2_svr = run_gridsearch(
        SVR(kernel='rbf'), GRID_SVR, X_svr, y_svr, 18,
    )

    svr_tuned = SVR(kernel='rbf', **best_svr)
    svr_tuned.fit(X_svr, y_svr)
    y_pred_svr_tuned = scaler_y.inverse_transform(
        svr_tuned.predict(X_test_sc).reshape(-1, 1)).ravel()
    met_svr_tuned = calcular_metricas(y_test, y_pred_svr_tuned)
    delta_r2 = met_svr_tuned['R2'] - met_svr_base['R2']
    print(f"    Tuned →  R²={met_svr_tuned['R2']:.4f}  RMSE={met_svr_tuned['RMSE']:.4f}  "
          f"(ΔR²={delta_r2:+.4f})")

    for etapa, met, params, cv_r2 in [
        ('Base',  met_svr_base,  cfg['svr_base'], None),
        ('Tuned', met_svr_tuned, best_svr,        cv_r2_svr),
    ]:
        todos_resultados.append({
            'Escenario': label, 'Modelo': 'SVR', 'Etapa': etapa,
            **met, 'CV_R2': cv_r2, 'Params': str(params),
        })

print(f"\n{'='*70}")
print(f"Tiempo total: {(time.time()-t_total)/60:.1f} minutos")

# =============================================================================
# GUARDAR RESULTADOS
# =============================================================================

df_res = pd.DataFrame(todos_resultados)
csv_path = os.path.join(MOD_DIR, 'tuning_resultados.csv')
df_res.to_csv(csv_path, index=False)
print(f"\n✓ Resultados guardados → modelos/tuning_resultados.csv")

print("\n" + "="*70)
print("TABLA COMPLETA DE RESULTADOS")
print("="*70)
cols_show = ['Escenario', 'Modelo', 'Etapa', 'RMSE', 'MAE', 'MAPE', 'R2', 'CV_R2']
print(df_res[cols_show].to_string(index=False))

# Tabla de mejora (pivot: Base vs Tuned)
print("\n" + "="*70)
print("MEJORA NETA (Tuned − Base)")
print("="*70)
df_base  = df_res[df_res['Etapa'] == 'Base'].set_index(['Escenario','Modelo'])[['RMSE','R2']]
df_tuned = df_res[df_res['Etapa'] == 'Tuned'].set_index(['Escenario','Modelo'])[['RMSE','R2']]
df_delta = (df_tuned - df_base).rename(columns={'RMSE': 'ΔRMSE', 'R2': 'ΔR2'})
df_delta['ΔRMSE'] = df_delta['ΔRMSE'].round(4)
df_delta['ΔR2']   = df_delta['ΔR2'].round(4)
print(df_delta.to_string())

# =============================================================================
# VISUALIZACIONES
# =============================================================================

escenarios_labels = ['15 Minutos', '1 Hora', '1 Día']
modelos = ['Random Forest', 'XGBoost', 'SVR']

def grafico_comparacion(metrica, ylabel, filename):
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    for ax, esc_label in zip(axes, escenarios_labels):
        df_esc = df_res[df_res['Escenario'] == esc_label]
        x = np.arange(len(modelos))
        width = 0.35

        base_vals  = [df_esc[(df_esc['Modelo']==m)&(df_esc['Etapa']=='Base')][metrica].values[0]
                      for m in modelos]
        tuned_vals = [df_esc[(df_esc['Modelo']==m)&(df_esc['Etapa']=='Tuned')][metrica].values[0]
                      for m in modelos]

        bars1 = ax.bar(x - width/2, base_vals,  width, label='Base',
                       color='#90A4AE', edgecolor='black', linewidth=0.5)
        bars2 = ax.bar(x + width/2, tuned_vals, width, label='Tuned',
                       color='#FF8F00', edgecolor='black', linewidth=0.5)

        ymax = max(max(base_vals), max(tuned_vals))
        offset = ymax * 0.015
        fmt = '.4f'
        for bar, v in zip(bars1, base_vals):
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+offset,
                    f'{v:{fmt}}', ha='center', va='bottom', fontsize=7.5)
        for bar, v in zip(bars2, tuned_vals):
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+offset,
                    f'{v:{fmt}}', ha='center', va='bottom', fontsize=7.5)

        ax.set_title(f'Escenario {esc_label}', fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(modelos, rotation=15, ha='right', fontsize=9)
        ax.set_ylabel(ylabel)
        ax.legend(fontsize=9)
        ax.grid(axis='y', alpha=0.3)
        if metrica == 'R2':
            ax.set_ylim(0, 1.08)

    plt.suptitle(f'{ylabel} — Base vs Tuned (GridSearchCV, TimeSeriesSplit)',
                 fontsize=13, fontweight='bold')
    plt.tight_layout()
    path = os.path.join(GRAF_DIR, filename)
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.show()
    plt.close()
    print(f"✓ Gráfico guardado → graficos/tuning/{filename}")

grafico_comparacion('R2',   'R²',        'comparacion_r2.png')
grafico_comparacion('RMSE', 'RMSE (kW)', 'comparacion_rmse.png')
grafico_comparacion('MAPE', 'MAPE (%)',  'comparacion_mape.png')

# Gráfico de mejora ΔR² por modelo y escenario
fig, ax = plt.subplots(figsize=(12, 5))
df_delta_reset = df_delta.reset_index()
x = np.arange(len(escenarios_labels))
width = 0.25

for i, modelo in enumerate(modelos):
    deltas = [df_delta_reset[(df_delta_reset['Escenario']==e)&
                             (df_delta_reset['Modelo']==modelo)]['ΔR2'].values[0]
              for e in escenarios_labels]
    bars = ax.bar(x + (i-1)*width, deltas, width, label=modelo,
                  color=list(COLORES.values())[i], edgecolor='black', linewidth=0.5)
    for bar, v in zip(bars, deltas):
        ax.text(bar.get_x()+bar.get_width()/2,
                bar.get_height() + (0.0005 if v >= 0 else -0.002),
                f'{v:+.4f}', ha='center',
                va='bottom' if v >= 0 else 'top', fontsize=8)

ax.axhline(0, color='black', linewidth=0.8, linestyle='--')
ax.set_xticks(x)
ax.set_xticklabels(escenarios_labels)
ax.set_ylabel('ΔR² (Tuned − Base)')
ax.set_title('Mejora de R² tras GridSearchCV por escenario y modelo', fontweight='bold')
ax.legend()
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
path = os.path.join(GRAF_DIR, 'mejora_delta_r2.png')
plt.savefig(path, dpi=150, bbox_inches='tight')
plt.show()
plt.close()
print(f"✓ Gráfico guardado → graficos/tuning/mejora_delta_r2.png")

# =============================================================================
# RESUMEN FINAL
# =============================================================================

print("\n" + "="*70)
print("RESUMEN FINAL — MEJORES MODELOS TUNED POR ESCENARIO")
print("="*70)
df_tuned_only = df_res[df_res['Etapa'] == 'Tuned'].copy()
for esc in escenarios_labels:
    sub = df_tuned_only[df_tuned_only['Escenario'] == esc]
    mejor = sub.loc[sub['R2'].idxmax()]
    print(f"\n  {esc}:")
    print(f"    Mejor modelo: {mejor['Modelo']}  →  R²={mejor['R2']:.4f}  "
          f"RMSE={mejor['RMSE']:.4f}  MAPE={mejor['MAPE']:.2f}%")
    print(f"    Params: {mejor['Params']}")

print("\n✓ Tuning completado exitosamente.")
