# =============================================================================
# TEST DE DIEBOLD-MARIANO — Comparación estadística pareada de pronósticos
# Tesis: Modelo predictivo del consumo energético en hogares inteligentes
# Compara: Random Forest vs XGBoost, y
#          Mejor modelo ML vs Persistencia (¿el aprendizaje es significativo?)
# Fuente: modelos/predicciones_escenarioN.csv (predicciones fila a fila)
# =============================================================================

import os
import pandas as pd
import numpy as np
from scipy.stats import t as t_dist

_here = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = _here if os.path.exists(os.path.join(_here, 'datos')) else os.path.dirname(_here)
MOD_DIR  = os.path.join(BASE_DIR, 'modelos')

# Horizonte de pronóstico (pasos), en las mismas unidades que la frecuencia de
# cada escenario — necesario porque los errores de un pronóstico a h pasos son
# un proceso MA(h-1), y la varianza de largo plazo del test DM debe incluir
# las autocovarianzas hasta el lag h-1 (Diebold & Mariano, 1995).
HORIZONTES = {1: 672, 2: 168, 3: 7}
ESCENARIOS_LABEL = {1: '15 Minutos', 2: '1 Hora', 3: '1 Día'}

MODELOS_ML = {
    'y_pred_rf' : 'Random Forest',
    'y_pred_xgb': 'XGBoost',
    'y_pred_svr': 'SVR',
}


def diebold_mariano(y_true, yhat1, yhat2, h, loss='squared'):
    """
    Test de Diebold-Mariano con ajuste de varianza HAC (autocovarianzas
    hasta el lag h-1) y ajuste de muestra pequeña de Harvey, Leybourne y
    Newbold (1997). Devuelve (estadístico ajustado, p-value bilateral).
    """
    e1 = np.asarray(y_true) - np.asarray(yhat1)
    e2 = np.asarray(y_true) - np.asarray(yhat2)
    d = e1 ** 2 - e2 ** 2 if loss == 'squared' else np.abs(e1) - np.abs(e2)
    n = len(d)
    d_bar = d.mean()

    gamma0 = np.var(d, ddof=0)
    gamma_sum = 0.0
    for k in range(1, min(h, n)):
        gamma_sum += np.mean((d[:-k] - d_bar) * (d[k:] - d_bar))
    var_dbar = (gamma0 + 2 * gamma_sum) / n
    if var_dbar <= 0:
        var_dbar = gamma0 / n  # fallback si el ajuste HAC da varianza negativa

    dm_stat = d_bar / np.sqrt(var_dbar)

    # Ajuste de muestra pequeña (Harvey-Leybourne-Newbold, 1997)
    correction = np.sqrt(max((n + 1 - 2 * h + h * (h - 1) / n) / n, 1e-6))
    dm_adj = dm_stat * correction
    p_value = 2 * (1 - t_dist.cdf(np.abs(dm_adj), df=n - 1))
    return dm_adj, p_value


def concluir(dm_stat, p_value, nombre1, nombre2, alpha=0.05):
    if p_value >= alpha:
        return f'No hay diferencia significativa entre {nombre1} y {nombre2} (p≥{alpha})'
    mejor = nombre1 if dm_stat < 0 else nombre2
    peor  = nombre2 if dm_stat < 0 else nombre1
    return f'{mejor} es significativamente mejor que {peor} (p<{alpha})'


print("=" * 70)
print("TEST DE DIEBOLD-MARIANO — COMPARACIÓN PAREADA DE PRONÓSTICOS")
print("=" * 70)

resultados = []

for num in (1, 2, 3):
    label = ESCENARIOS_LABEL[num]
    h     = HORIZONTES[num]

    pred_csv = os.path.join(MOD_DIR, f'predicciones_escenario{num}.csv')
    met_csv  = os.path.join(MOD_DIR, f'metricas_escenario{num}.csv')
    if not os.path.exists(pred_csv):
        print(f"\n⚠ Escenario {num}: no se encontró {pred_csv} — correr escenario{num}_*.py primero")
        continue

    df_pred = pd.read_csv(pred_csv)
    df_met  = pd.read_csv(met_csv, index_col='Modelo')
    y_real  = df_pred['y_real'].values

    print(f"\n{'='*70}")
    print(f"ESCENARIO {num} — {label}  |  Horizonte: {h} pasos  |  n_test={len(df_pred):,}")
    print(f"{'='*70}")

    # ── 1) Random Forest vs XGBoost (comparación pedida explícitamente) ─────
    dm_stat, p_value = diebold_mariano(
        y_real, df_pred['y_pred_rf'].values, df_pred['y_pred_xgb'].values, h)
    conclusion = concluir(dm_stat, p_value, 'Random Forest', 'XGBoost')
    print(f"\n  Random Forest vs XGBoost:")
    print(f"    DM={dm_stat:+.4f}  p-value={p_value:.4f}  →  {conclusion}")
    resultados.append({'Escenario': label, 'Comparación': 'Random Forest vs XGBoost',
                        'DM_stat': round(dm_stat, 4), 'p_value': round(p_value, 4),
                        'Conclusion': conclusion})

    # ── 2) Mejor modelo ML vs Persistencia (¿el aprendizaje es significativo?) ──
    r2_ml = df_met.loc[list(MODELOS_ML.values()), 'R2']
    mejor_ml_nombre = r2_ml.idxmax()
    mejor_ml_col = [c for c, n in MODELOS_ML.items() if n == mejor_ml_nombre][0]

    dm_stat2, p_value2 = diebold_mariano(
        y_real, df_pred[mejor_ml_col].values, df_pred['y_pred_persistencia'].values, h)
    conclusion2 = concluir(dm_stat2, p_value2, mejor_ml_nombre, 'Persistencia')
    print(f"\n  Mejor modelo ML ({mejor_ml_nombre}, R²={r2_ml.max():.4f}) vs Persistencia:")
    print(f"    DM={dm_stat2:+.4f}  p-value={p_value2:.4f}  →  {conclusion2}")
    resultados.append({'Escenario': label,
                        'Comparación': f'{mejor_ml_nombre} vs Persistencia',
                        'DM_stat': round(dm_stat2, 4), 'p_value': round(p_value2, 4),
                        'Conclusion': conclusion2})

df_dm = pd.DataFrame(resultados)
out_csv = os.path.join(MOD_DIR, 'dm_test_resultados.csv')
df_dm.to_csv(out_csv, index=False)

print(f"\n{'='*70}")
print("TABLA FINAL")
print(f"{'='*70}")
print(df_dm.to_string(index=False))
print(f"\n✓ Resultados guardados → modelos/dm_test_resultados.csv")
