# =============================================================================
# GRÁFICOS COMPARATIVOS — Todos los escenarios y modelos
# Tesis: Modelo predictivo del consumo energético en hogares inteligentes
# Fuente: modelos/tuning_resultados.csv (resultados Base y Tuned, incl. baselines)
#         modelos/dm_test_resultados.csv (test de Diebold-Mariano)
# =============================================================================

import matplotlib
# matplotlib.use('Agg')  # desactivado: permite ver gráficos en Spyder
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

plt.rcParams.update({'figure.dpi': 200, 'font.size': 15})

_here = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = _here if os.path.exists(os.path.join(_here, 'datos')) else os.path.dirname(_here)
MOD_DIR  = os.path.join(BASE_DIR, 'modelos')
GRAF_DIR = os.path.join(BASE_DIR, 'graficos', 'comparativos')
os.makedirs(GRAF_DIR, exist_ok=True)

COLORES  = {'Random Forest': '#1565C0', 'XGBoost': '#2E7D32', 'SVR': '#B71C1C',
            'Persistencia': '#757575', 'Regresión Lineal': '#F9A825'}
ABREV    = {'Random Forest': 'RF', 'XGBoost': 'XGB', 'SVR': 'SVR',
            'Persistencia': 'Persist.', 'Regresión Lineal': 'Reg. Lineal'}
MODELOS_ML  = ['Random Forest', 'XGBoost', 'SVR']            # solo modelos entrenados (para radar)
MODELOS     = ['Random Forest', 'XGBoost', 'SVR', 'Persistencia', 'Regresión Lineal']
ESCENARIOS = ['15 Minutos', '1 Hora', '1 Día']
ESC_SHORT  = ['15 min', '1 hora', '1 día']

def savefig(nombre):
    plt.tight_layout()
    plt.savefig(os.path.join(GRAF_DIR, nombre), dpi=200, bbox_inches='tight')
    plt.show()
    plt.close()
    print(f"  ✓ {nombre}")

# =============================================================================
# CARGA DE DATOS
# =============================================================================
df_all = pd.read_csv(os.path.join(MOD_DIR, 'tuning_resultados.csv'))
df_base  = df_all[df_all['Etapa'] == 'Base'].copy()
df_tuned = df_all[df_all['Etapa'] == 'Tuned'].copy()

print("=" * 65)
print("GRÁFICOS COMPARATIVOS — ESCENARIOS Y MODELOS")
print("=" * 65)
print(f"Registros cargados: {len(df_all)}  (Base: {len(df_base)}, Tuned: {len(df_tuned)})")

# =============================================================================
# GRÁFICO 1 — Comparación de 4 métricas (modelos × escenarios) — Tuned
# Barras agrupadas por escenario, una barra por modelo (incl. baselines)
# =============================================================================
print("\n[1] Comparación de métricas (barras agrupadas) ...")

metricas = [
    ('R2',   'R²',        False),   # (col, label, lower_is_better)
    ('RMSE', 'RMSE (kW)', True),
    ('MAE',  'MAE (kW)',  True),
    ('MAPE', 'MAPE (%)',  True),
]

fig, axes = plt.subplots(1, 4, figsize=(22, 6))

x = np.arange(len(ESCENARIOS))
n_mod = len(MODELOS)
width = 0.8 / n_mod

for ax, (col, ylabel, lower_better) in zip(axes, metricas):
    vals_por_modelo = {
        modelo: [
            df_tuned[(df_tuned['Escenario']==esc)&(df_tuned['Modelo']==modelo)][col].values[0]
            for esc in ESCENARIOS
        ]
        for modelo in MODELOS
    }
    ymax_col = max(v for vals in vals_por_modelo.values() for v in vals)
    ymin_col = min(0, min(v for vals in vals_por_modelo.values() for v in vals))

    for i, modelo in enumerate(MODELOS):
        vals = vals_por_modelo[modelo]
        offset = (i - (n_mod - 1) / 2) * width
        bars = ax.bar(x + offset, vals, width,
                      label=modelo, color=COLORES[modelo],
                      edgecolor='black', linewidth=0.5)
        for bar, v in zip(bars, vals):
            fmt = f'{v:.2f}' if col == 'MAPE' else f'{v:.4f}'
            signo = 1 if v >= 0 else -1
            ax.text(bar.get_x() + bar.get_width()/2,
                    bar.get_height() + signo * ymax_col * 0.02,
                    fmt, ha='center', va='bottom' if v >= 0 else 'top',
                    fontsize=7.5, rotation=90)

    ax.set_title(ylabel, fontweight='bold', fontsize=15.4)
    ax.set_xticks(x)
    ax.set_xticklabels(ESC_SHORT, fontsize=12.6)
    ax.set_ylabel(ylabel)
    ax.grid(axis='y', alpha=0.3)
    # Deja espacio de sobra arriba para las etiquetas rotadas, y espacio abajo
    # cuando hay valores negativos (R² puede ser negativo) para que las
    # etiquetas de las barras negativas no se corten contra el eje X.
    rango = ymax_col - ymin_col
    ax.set_ylim(ymin_col - rango * 0.15, ymax_col + rango * 0.35)
    if ymin_col < 0:
        ax.axhline(0, color='black', linewidth=0.7)
    note = '↓ mejor' if lower_better else '↑ mejor'
    ax.set_xlabel(note, fontsize=11.2, color='gray')

handles = [mpatches.Patch(color=COLORES[m], label=m) for m in MODELOS]
fig.legend(handles=handles, loc='upper center', ncol=5, fontsize=12,
           bbox_to_anchor=(0.5, 1.04))
plt.suptitle('Comparación de métricas por escenario y modelo (parámetros tuned + baselines)',
             fontsize=18.2, fontweight='bold', y=1.08)
savefig('01_metricas_tuned_barras.png')

# =============================================================================
# GRÁFICO 2 — Heatmaps de las 4 métricas
# Filas = modelos (incl. baselines), columnas = escenarios
# =============================================================================
print("[2] Heatmaps de métricas ...")

fig, axes = plt.subplots(1, 4, figsize=(22, 6.5))

heatmap_cfg = [
    ('R2',   'R²',        'YlGn',    False),
    ('RMSE', 'RMSE (kW)', 'YlOrRd',  True),
    ('MAE',  'MAE (kW)',  'YlOrRd',  True),
    ('MAPE', 'MAPE (%)',  'YlOrRd',  True),
]

for ax, (col, title, cmap, lower_better) in zip(axes, heatmap_cfg):
    mat = np.zeros((len(MODELOS), len(ESCENARIOS)))
    for i, mod in enumerate(MODELOS):
        for j, esc in enumerate(ESCENARIOS):
            mat[i, j] = df_tuned[(df_tuned['Modelo']==mod)&
                                  (df_tuned['Escenario']==esc)][col].values[0]

    df_mat = pd.DataFrame(mat, index=MODELOS, columns=ESC_SHORT)
    annot_fmt = '.2f' if col == 'MAPE' else '.4f'
    sns.heatmap(df_mat, ax=ax, cmap=cmap, annot=True, fmt=annot_fmt,
                linewidths=0.5, linecolor='white',
                annot_kws={'size': 11, 'weight': 'bold'},
                cbar_kws={'shrink': 0.8})
    note = '(↓ mejor)' if lower_better else '(↑ mejor)'
    ax.set_title(f'{title}\n{note}', fontweight='bold', fontsize=14)
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.tick_params(axis='x', labelsize=12.6)
    ax.tick_params(axis='y', labelsize=11, rotation=0)

plt.suptitle('Heatmap de métricas — parámetros tuned (GridSearchCV) + baselines',
             fontsize=18.2, fontweight='bold')
savefig('02_heatmap_metricas.png')

# =============================================================================
# GRÁFICO 3 — Comparación Base vs Tuned por escenario (R² y RMSE)
# Solo modelos con hiperparámetros tuneados (los baselines no cambian)
# =============================================================================
print("[3] Base vs Tuned — R² y RMSE ...")

fig, axes = plt.subplots(2, 3, figsize=(18, 10))

for col_idx, esc in enumerate(ESCENARIOS):
    # Fila 0: R²
    ax_r2   = axes[0][col_idx]
    # Fila 1: RMSE
    ax_rmse = axes[1][col_idx]

    df_esc_base  = df_base[df_base['Escenario'] == esc]
    df_esc_tuned = df_tuned[df_tuned['Escenario'] == esc]

    x     = np.arange(len(MODELOS_ML))
    width = 0.35

    for ax, col, ylabel in [(ax_r2, 'R2', 'R²'), (ax_rmse, 'RMSE', 'RMSE (kW)')]:
        base_vals  = [df_esc_base[df_esc_base['Modelo']==m][col].values[0]  for m in MODELOS_ML]
        tuned_vals = [df_esc_tuned[df_esc_tuned['Modelo']==m][col].values[0] for m in MODELOS_ML]

        b1 = ax.bar(x - width/2, base_vals,  width, label='Base',
                    color='#90A4AE', edgecolor='black', linewidth=0.5)
        b2 = ax.bar(x + width/2, tuned_vals, width, label='Tuned',
                    color='#FF8F00', edgecolor='black', linewidth=0.5)

        # R2 puede ser negativo — el eje y las etiquetas deben acomodar eso
        # (si no, las barras/etiquetas quedan fuera del rango visible).
        ymin = min(0, min(base_vals), min(tuned_vals))
        ymax = max(0, max(base_vals), max(tuned_vals))
        rango = ymax - ymin
        off  = rango * 0.02
        for bar, v in zip(b1, base_vals):
            signo = 1 if v >= 0 else -1
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+signo*off,
                    f'{v:.4f}', ha='center', va='bottom' if v >= 0 else 'top', fontsize=10.5)
        for bar, v in zip(b2, tuned_vals):
            signo = 1 if v >= 0 else -1
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+signo*off,
                    f'{v:.4f}', ha='center', va='bottom' if v >= 0 else 'top', fontsize=10.5)

        ax.set_xticks(x)
        ax.set_xticklabels([ABREV[m] for m in MODELOS_ML], rotation=0, fontsize=12.6)
        ax.set_ylabel(ylabel)
        ax.grid(axis='y', alpha=0.3)
        ax.legend(fontsize=11.2)
        if col == 'R2':
            ax.set_title(f'Escenario {ESC_SHORT[col_idx]}', fontweight='bold', fontsize=15.4)
            if ymin >= 0:
                ax.set_ylim(0, 1.1)
            else:
                ax.set_ylim(ymin - rango * 0.15, ymax + rango * 0.15)
                ax.axhline(0, color='black', linewidth=0.6)

plt.suptitle('Base vs Tuned — R² y RMSE por escenario (GridSearchCV)',
             fontsize=18.2, fontweight='bold')
savefig('03_base_vs_tuned_r2_rmse.png')

# =============================================================================
# GRÁFICO 4 — Radar chart: perfil multidimensional por modelo (tuned)
# Un radar por escenario, cada línea = un modelo ML (sin baselines, para
# no saturar el gráfico con series triviales)
# =============================================================================
print("[4] Radar charts por escenario ...")

# Para radar: normalizar métricas (0=peor, 1=mejor)
# R² → mayor es mejor; RMSE/MAE/MAPE → menor es mejor
cats = ['R²', 'RMSE\n(inv)', 'MAE\n(inv)', 'MAPE\n(inv)']
N    = len(cats)
angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
angles += angles[:1]

fig, axes = plt.subplots(1, 3, figsize=(18, 6),
                         subplot_kw=dict(polar=True))

for ax, esc in zip(axes, ESCENARIOS):
    df_esc = df_tuned[df_tuned['Escenario'] == esc]

    # Normalización min-max por métrica (entre los modelos ML del escenario)
    def norm(col, higher_better=True):
        vals = np.array([df_esc[df_esc['Modelo']==m][col].values[0] for m in MODELOS_ML])
        vmin, vmax = vals.min(), vals.max()
        if vmax == vmin:
            return np.ones(len(MODELOS_ML))
        normed = (vals - vmin) / (vmax - vmin)
        return normed if higher_better else 1 - normed

    r2_n   = norm('R2',   True)
    rmse_n = norm('RMSE', False)
    mae_n  = norm('MAE',  False)
    mape_n = norm('MAPE', False)

    for i, modelo in enumerate(MODELOS_ML):
        values = [r2_n[i], rmse_n[i], mae_n[i], mape_n[i]]
        values += values[:1]
        ax.plot(angles, values, color=COLORES[modelo], linewidth=2, label=modelo)
        ax.fill(angles, values, color=COLORES[modelo], alpha=0.08)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(cats, fontsize=12.6)
    ax.set_ylim(0, 1)
    ax.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(['0.25', '0.50', '0.75', '1.00'], fontsize=9, color='gray')
    ax.set_title(f'Escenario {ESC_SHORT[ESCENARIOS.index(esc)]}',
                 fontweight='bold', fontsize=15.4, pad=15)
    ax.grid(color='gray', alpha=0.3)

handles = [mpatches.Patch(color=COLORES[m], label=m) for m in MODELOS_ML]
fig.legend(handles=handles, loc='lower center', ncol=3, fontsize=14,
           bbox_to_anchor=(0.5, -0.1))
plt.suptitle('Perfil multidimensional de modelos ML por escenario\n'
             '(normalizado: 1 = mejor desempeño relativo)',
             fontsize=16.8, fontweight='bold')
savefig('04_radar_modelos.png')

# =============================================================================
# GRÁFICO 5 — Tabla resumen visual (mejor modelo por escenario)
# =============================================================================
print("[5] Tabla resumen visual ...")

fig, ax = plt.subplots(figsize=(14, 4))
ax.axis('off')

cols_tab = ['Escenario', 'Mejor Modelo', 'R²', 'RMSE (kW)', 'MAE (kW)', 'MAPE (%)']
rows = []
for esc, esc_s in zip(ESCENARIOS, ESC_SHORT):
    sub = df_tuned[df_tuned['Escenario'] == esc]
    best_row = sub.loc[sub['R2'].idxmax()]
    rows.append([
        esc_s,
        best_row['Modelo'],
        f"{best_row['R2']:.4f}",
        f"{best_row['RMSE']:.4f}",
        f"{best_row['MAE']:.4f}",
        f"{best_row['MAPE']:.2f}%",
    ])

table = ax.table(
    cellText=rows,
    colLabels=cols_tab,
    cellLoc='center',
    loc='center',
    bbox=[0, 0, 1, 1],
)
table.auto_set_font_size(False)
table.set_fontsize(15.4)

# Estilo encabezado
for j in range(len(cols_tab)):
    table[0, j].set_facecolor('#263238')
    table[0, j].set_text_props(color='white', fontweight='bold')

# Color fondo filas alternado + color modelo
model_colors = {'Random Forest': '#E3F2FD', 'XGBoost': '#E8F5E9', 'SVR': '#FFEBEE',
                 'Persistencia': '#EEEEEE', 'Regresión Lineal': '#FFF8E1'}
for i, row in enumerate(rows):
    modelo = row[1]
    bg = model_colors.get(modelo, '#FAFAFA')
    for j in range(len(cols_tab)):
        table[i+1, j].set_facecolor(bg)
        table[i+1, j].set_height(0.28)

for j in range(len(cols_tab)):
    table[0, j].set_height(0.28)

plt.title('Mejor modelo por escenario (parámetros tuned — GridSearchCV)',
          fontweight='bold', fontsize=16.8, pad=10)
savefig('05_tabla_mejor_modelo.png')

# =============================================================================
# GRÁFICO 6 — Evolución de R² a través de los escenarios (líneas)
# =============================================================================
print("[6] Evolución de R² por escenario ...")

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

r2_min, r2_max = df_all['R2'].min(), df_all['R2'].max()
pad = (r2_max - r2_min) * 0.20
ylim_r2 = (r2_min - pad, r2_max + pad)

for ax, etapa, title in [(axes[0], 'Base', 'Parámetros Base'),
                          (axes[1], 'Tuned', 'Parámetros Tuned (GridSearchCV)')]:
    df_etapa = df_all[df_all['Etapa'] == etapa]
    valores = {
        modelo: [df_etapa[(df_etapa['Escenario']==e)&
                           (df_etapa['Modelo']==modelo)]['R2'].values[0]
                 for e in ESCENARIOS]
        for modelo in MODELOS
    }
    for modelo in MODELOS:
        estilo = dict(linestyle='--', alpha=0.6) if modelo in ('Persistencia', 'Regresión Lineal') else {}
        ax.plot(ESC_SHORT, valores[modelo], marker='o', markersize=7, linewidth=2,
                color=COLORES[modelo], label=modelo, **estilo)

    ax.axhline(0, color='black', linewidth=0.6, alpha=0.5)
    ax.set_title(title, fontweight='bold', fontsize=15.4)
    ax.set_ylabel('R²')
    ax.set_ylim(*ylim_r2)
    ax.grid(alpha=0.3)
    ax.legend(fontsize=10.5, ncol=2)

plt.suptitle('Evolución del R² a través de los escenarios temporales (modelos ML y baselines)',
             fontsize=18.2, fontweight='bold')
savefig('06_evolucion_r2.png')

# =============================================================================
# GRÁFICO 7 — Métricas normalizadas (sMAPE / WAPE / MASE / nRMSE) — Tuned
# =============================================================================
print("[7] Métricas normalizadas (barras agrupadas) ...")

metricas_norm = [
    ('sMAPE', 'sMAPE (%)', True),
    ('WAPE',  'WAPE (%)',  True),
    ('MASE',  'MASE',      True),
    ('nRMSE', 'nRMSE (%)', True),
]

fig, axes = plt.subplots(1, 4, figsize=(22, 6))
for ax, (col, ylabel, lower_better) in zip(axes, metricas_norm):
    vals_por_modelo = {
        modelo: [
            df_tuned[(df_tuned['Escenario']==esc)&(df_tuned['Modelo']==modelo)][col].values[0]
            for esc in ESCENARIOS
        ]
        for modelo in MODELOS
    }
    # MASE de Persistencia queda NaN por definición (no se compara consigo misma)
    valores_validos = [v for vals in vals_por_modelo.values() for v in vals if pd.notna(v)]
    ymax_col = max(valores_validos) if valores_validos else 1

    for i, modelo in enumerate(MODELOS):
        vals = [0 if pd.isna(v) else v for v in vals_por_modelo[modelo]]
        offset = (i - (n_mod - 1) / 2) * width
        bars = ax.bar(x + offset, vals, width,
                      label=modelo, color=COLORES[modelo],
                      edgecolor='black', linewidth=0.5)
        for bar, v in zip(bars, vals_por_modelo[modelo]):
            if pd.isna(v):
                continue
            ax.text(bar.get_x() + bar.get_width()/2,
                    bar.get_height() + ymax_col * 0.02,
                    f'{v:.2f}', ha='center', va='bottom', fontsize=7.5, rotation=90)

    ax.set_title(ylabel, fontweight='bold', fontsize=15.4)
    ax.set_xticks(x)
    ax.set_xticklabels(ESC_SHORT, fontsize=12.6)
    ax.set_ylabel(ylabel)
    ax.grid(axis='y', alpha=0.3)
    ax.set_ylim(0, ymax_col * 1.45)
    ax.set_xlabel('↓ mejor' if lower_better else '↑ mejor', fontsize=11.2, color='gray')

handles = [mpatches.Patch(color=COLORES[m], label=m) for m in MODELOS]
fig.legend(handles=handles, loc='upper center', ncol=5, fontsize=12,
           bbox_to_anchor=(0.5, 1.04))
plt.suptitle('Métricas normalizadas — Base vs baselines (parámetros tuned)\n'
             '(MASE se calcula respecto al MAE de Persistencia; MASE<1 = supera al naive)',
             fontsize=16.8, fontweight='bold', y=1.1)
savefig('07_metricas_normalizadas_barras.png')

# =============================================================================
# GRÁFICO 8 — Heatmap de métricas normalizadas
# =============================================================================
print("[8] Heatmap de métricas normalizadas ...")

fig, axes = plt.subplots(1, 4, figsize=(22, 6.5))
for ax, (col, title, lower_better) in zip(axes, metricas_norm):
    mat = np.zeros((len(MODELOS), len(ESCENARIOS)))
    for i, mod in enumerate(MODELOS):
        for j, esc in enumerate(ESCENARIOS):
            v = df_tuned[(df_tuned['Modelo']==mod)&(df_tuned['Escenario']==esc)][col].values[0]
            mat[i, j] = v if pd.notna(v) else np.nan

    df_mat = pd.DataFrame(mat, index=MODELOS, columns=ESC_SHORT)
    sns.heatmap(df_mat, ax=ax, cmap='YlOrRd', annot=True, fmt='.2f',
                linewidths=0.5, linecolor='white',
                annot_kws={'size': 11, 'weight': 'bold'},
                cbar_kws={'shrink': 0.8}, mask=df_mat.isna())
    ax.set_title(f'{title}\n(↓ mejor)', fontweight='bold', fontsize=14)
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.tick_params(axis='x', labelsize=12.6)
    ax.tick_params(axis='y', labelsize=11, rotation=0)

plt.suptitle('Heatmap de métricas normalizadas (sMAPE, WAPE, MASE, nRMSE) — tuned',
             fontsize=18.2, fontweight='bold')
savefig('08_heatmap_metricas_normalizadas.png')

# =============================================================================
# GRÁFICO 9 — Tabla del test de Diebold-Mariano
# =============================================================================
dm_csv = os.path.join(MOD_DIR, 'dm_test_resultados.csv')
if os.path.exists(dm_csv):
    print("[9] Tabla del test de Diebold-Mariano ...")
    df_dm = pd.read_csv(dm_csv)

    fig, ax = plt.subplots(figsize=(16, 4.5))
    ax.axis('off')

    cols_dm = ['Escenario', 'Comparación', 'DM_stat', 'p_value', 'Conclusion']
    rows_dm = [
        [r['Escenario'], r['Comparación'], f"{r['DM_stat']:+.4f}",
         f"{r['p_value']:.4f}", r['Conclusion']]
        for _, r in df_dm.iterrows()
    ]

    table = ax.table(cellText=rows_dm, colLabels=cols_dm, cellLoc='center',
                      loc='center', bbox=[0, 0, 1, 1],
                      colWidths=[0.1, 0.22, 0.1, 0.1, 0.48])
    table.auto_set_font_size(False)
    table.set_fontsize(11.5)
    for j in range(len(cols_dm)):
        table[0, j].set_facecolor('#263238')
        table[0, j].set_text_props(color='white', fontweight='bold')
        table[0, j].set_height(0.14)
    for i in range(len(rows_dm)):
        bg = '#FAFAFA' if i % 2 == 0 else '#EEEEEE'
        for j in range(len(cols_dm)):
            table[i+1, j].set_facecolor(bg)
            table[i+1, j].set_height(0.14)

    plt.title('Test de Diebold-Mariano — comparación pareada de pronósticos',
              fontweight='bold', fontsize=16.8, pad=10)
    savefig('09_tabla_dm_test.png')
else:
    print("\n⚠ [9] No se encontró modelos/dm_test_resultados.csv — "
          "correr test_diebold_mariano.py primero. Se omite el gráfico 9.")

# =============================================================================
# RESUMEN
# =============================================================================
print("\n" + "=" * 65)
print("RESUMEN — GRÁFICOS GENERADOS EN graficos/comparativos/")
print("=" * 65)
print("  01_metricas_tuned_barras.png            — 4 métricas, barras agrupadas")
print("  02_heatmap_metricas.png                 — heatmaps R²/RMSE/MAE/MAPE")
print("  03_base_vs_tuned_r2_rmse.png            — comparación antes/después tuning")
print("  04_radar_modelos.png                    — perfil multidimensional (radar, ML)")
print("  05_tabla_mejor_modelo.png                — tabla resumen mejor modelo")
print("  06_evolucion_r2.png                      — R² Base vs Tuned a través de escenarios")
print("  07_metricas_normalizadas_barras.png      — sMAPE/WAPE/MASE/nRMSE, barras")
print("  08_heatmap_metricas_normalizadas.png     — heatmap sMAPE/WAPE/MASE/nRMSE")
print("  09_tabla_dm_test.png                     — resultados del test de Diebold-Mariano")
print("\n✓ Gráficos comparativos completados.")
