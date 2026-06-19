# =============================================================================
# GRÁFICOS COMPARATIVOS — Todos los escenarios y modelos
# Tesis: Modelo predictivo del consumo energético en hogares inteligentes
# Fuente: modelos/tuning_resultados.csv (resultados Base y Tuned)
# =============================================================================

import matplotlib
# matplotlib.use('Agg')  # desactivado: permite ver gráficos en Spyder
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

plt.rcParams.update({'figure.dpi': 150, 'font.size': 10})

_here = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = _here if os.path.exists(os.path.join(_here, 'datos')) else os.path.dirname(_here)
MOD_DIR  = os.path.join(BASE_DIR, 'modelos')
GRAF_DIR = os.path.join(BASE_DIR, 'graficos', 'comparativos')
os.makedirs(GRAF_DIR, exist_ok=True)

COLORES  = {'Random Forest': '#1565C0', 'XGBoost': '#2E7D32', 'SVR': '#B71C1C'}
MODELOS  = ['Random Forest', 'XGBoost', 'SVR']
ESCENARIOS = ['15 Minutos', '1 Hora', '1 Día']
ESC_SHORT  = ['15 min', '1 hora', '1 día']

def savefig(nombre):
    plt.tight_layout()
    plt.savefig(os.path.join(GRAF_DIR, nombre), dpi=150, bbox_inches='tight')
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
# Barras agrupadas por escenario, una barra por modelo
# =============================================================================
print("\n[1] Comparación de métricas (barras agrupadas) ...")

metricas = [
    ('R2',   'R²',        False),   # (col, label, lower_is_better)
    ('RMSE', 'RMSE (kW)', True),
    ('MAE',  'MAE (kW)',  True),
    ('MAPE', 'MAPE (%)',  True),
]

fig, axes = plt.subplots(1, 4, figsize=(20, 6))

x = np.arange(len(ESCENARIOS))
width = 0.25

for ax, (col, ylabel, lower_better) in zip(axes, metricas):
    for i, modelo in enumerate(MODELOS):
        vals = [
            df_tuned[(df_tuned['Escenario']==esc)&(df_tuned['Modelo']==modelo)][col].values[0]
            for esc in ESCENARIOS
        ]
        offset = (i - 1) * width
        bars = ax.bar(x + offset, vals, width,
                      label=modelo, color=COLORES[modelo],
                      edgecolor='black', linewidth=0.5)
        ymax = max(vals)
        for bar, v in zip(bars, vals):
            fmt = f'{v:.2f}' if col == 'MAPE' else f'{v:.4f}'
            ax.text(bar.get_x() + bar.get_width()/2,
                    bar.get_height() + ymax * 0.012,
                    fmt, ha='center', va='bottom', fontsize=6.5, rotation=90)

    ax.set_title(ylabel, fontweight='bold', fontsize=11)
    ax.set_xticks(x)
    ax.set_xticklabels(ESC_SHORT, fontsize=9)
    ax.set_ylabel(ylabel)
    ax.grid(axis='y', alpha=0.3)
    if col == 'R2':
        ax.set_ylim(0, 1.15)
    note = '↓ mejor' if lower_better else '↑ mejor'
    ax.set_xlabel(note, fontsize=8, color='gray')

handles = [mpatches.Patch(color=COLORES[m], label=m) for m in MODELOS]
fig.legend(handles=handles, loc='upper center', ncol=3, fontsize=10,
           bbox_to_anchor=(0.5, 1.02))
plt.suptitle('Comparación de métricas por escenario y modelo (parámetros tuned)',
             fontsize=13, fontweight='bold', y=1.06)
savefig('01_metricas_tuned_barras.png')

# =============================================================================
# GRÁFICO 2 — Heatmaps de las 4 métricas
# Filas = modelos, columnas = escenarios
# =============================================================================
print("[2] Heatmaps de métricas ...")

fig, axes = plt.subplots(1, 4, figsize=(20, 4))

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
                annot_kws={'size': 9, 'weight': 'bold'},
                cbar_kws={'shrink': 0.8})
    note = '(↓ mejor)' if lower_better else '(↑ mejor)'
    ax.set_title(f'{title}\n{note}', fontweight='bold', fontsize=10)
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.tick_params(axis='x', labelsize=9)
    ax.tick_params(axis='y', labelsize=9, rotation=0)

plt.suptitle('Heatmap de métricas — parámetros tuned (GridSearchCV)',
             fontsize=13, fontweight='bold')
savefig('02_heatmap_metricas.png')

# =============================================================================
# GRÁFICO 3 — Comparación Base vs Tuned por escenario (R² y RMSE)
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

    x     = np.arange(len(MODELOS))
    width = 0.35

    for ax, col, ylabel in [(ax_r2, 'R2', 'R²'), (ax_rmse, 'RMSE', 'RMSE (kW)')]:
        base_vals  = [df_esc_base[df_esc_base['Modelo']==m][col].values[0]  for m in MODELOS]
        tuned_vals = [df_esc_tuned[df_esc_tuned['Modelo']==m][col].values[0] for m in MODELOS]

        b1 = ax.bar(x - width/2, base_vals,  width, label='Base',
                    color='#90A4AE', edgecolor='black', linewidth=0.5)
        b2 = ax.bar(x + width/2, tuned_vals, width, label='Tuned',
                    color='#FF8F00', edgecolor='black', linewidth=0.5)

        ymax = max(max(base_vals), max(tuned_vals))
        off  = ymax * 0.012
        for bar, v in zip(b1, base_vals):
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+off,
                    f'{v:.4f}', ha='center', va='bottom', fontsize=7.5)
        for bar, v in zip(b2, tuned_vals):
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+off,
                    f'{v:.4f}', ha='center', va='bottom', fontsize=7.5)

        ax.set_xticks(x)
        ax.set_xticklabels(MODELOS, rotation=12, ha='right', fontsize=9)
        ax.set_ylabel(ylabel)
        ax.grid(axis='y', alpha=0.3)
        ax.legend(fontsize=8)
        if col == 'R2':
            ax.set_title(f'Escenario {ESC_SHORT[col_idx]}', fontweight='bold', fontsize=11)
            ax.set_ylim(0, 1.1)

plt.suptitle('Base vs Tuned — R² y RMSE por escenario (GridSearchCV)',
             fontsize=13, fontweight='bold')
savefig('03_base_vs_tuned_r2_rmse.png')

# =============================================================================
# GRÁFICO 4 — Radar chart: perfil multidimensional por modelo (tuned)
# Un radar por escenario, cada línea = un modelo
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

    # Normalización min-max por métrica (entre los 3 modelos del escenario)
    def norm(col, higher_better=True):
        vals = np.array([df_esc[df_esc['Modelo']==m][col].values[0] for m in MODELOS])
        vmin, vmax = vals.min(), vals.max()
        if vmax == vmin:
            return np.ones(len(MODELOS))
        normed = (vals - vmin) / (vmax - vmin)
        return normed if higher_better else 1 - normed

    r2_n   = norm('R2',   True)
    rmse_n = norm('RMSE', False)
    mae_n  = norm('MAE',  False)
    mape_n = norm('MAPE', False)

    for i, modelo in enumerate(MODELOS):
        values = [r2_n[i], rmse_n[i], mae_n[i], mape_n[i]]
        values += values[:1]
        ax.plot(angles, values, color=COLORES[modelo], linewidth=2, label=modelo)
        ax.fill(angles, values, color=COLORES[modelo], alpha=0.08)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(cats, fontsize=9)
    ax.set_ylim(0, 1)
    ax.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(['0.25', '0.50', '0.75', '1.00'], fontsize=6, color='gray')
    ax.set_title(f'Escenario {ESC_SHORT[ESCENARIOS.index(esc)]}',
                 fontweight='bold', fontsize=11, pad=15)
    ax.grid(color='gray', alpha=0.3)

handles = [mpatches.Patch(color=COLORES[m], label=m) for m in MODELOS]
fig.legend(handles=handles, loc='lower center', ncol=3, fontsize=10,
           bbox_to_anchor=(0.5, -0.02))
plt.suptitle('Perfil multidimensional de modelos por escenario\n'
             '(normalizado: 1 = mejor desempeño relativo)',
             fontsize=12, fontweight='bold')
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
table.set_fontsize(11)

# Estilo encabezado
for j in range(len(cols_tab)):
    table[0, j].set_facecolor('#263238')
    table[0, j].set_text_props(color='white', fontweight='bold')

# Color fondo filas alternado + color modelo
model_colors = {'Random Forest': '#E3F2FD', 'XGBoost': '#E8F5E9', 'SVR': '#FFEBEE'}
for i, row in enumerate(rows):
    modelo = row[1]
    bg = model_colors.get(modelo, '#FAFAFA')
    for j in range(len(cols_tab)):
        table[i+1, j].set_facecolor(bg)
        table[i+1, j].set_height(0.28)

for j in range(len(cols_tab)):
    table[0, j].set_height(0.28)

plt.title('Mejor modelo por escenario (parámetros tuned — GridSearchCV)',
          fontweight='bold', fontsize=12, pad=10)
savefig('05_tabla_mejor_modelo.png')

# =============================================================================
# GRÁFICO 6 — Evolución de R² a través de los escenarios (líneas)
# =============================================================================
print("[6] Evolución de R² por escenario ...")

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

for ax, etapa, title in [(axes[0], 'Base', 'Parámetros Base'),
                          (axes[1], 'Tuned', 'Parámetros Tuned (GridSearchCV)')]:
    df_etapa = df_all[df_all['Etapa'] == etapa]
    for modelo in MODELOS:
        r2_vals = [df_etapa[(df_etapa['Escenario']==e)&
                             (df_etapa['Modelo']==modelo)]['R2'].values[0]
                   for e in ESCENARIOS]
        ax.plot(ESC_SHORT, r2_vals, marker='o', markersize=8, linewidth=2.5,
                color=COLORES[modelo], label=modelo)
        for xi, yi in zip(range(len(ESC_SHORT)), r2_vals):
            ax.annotate(f'{yi:.4f}', (xi, yi),
                        textcoords='offset points', xytext=(0, 10),
                        ha='center', fontsize=8.5)

    ax.set_title(title, fontweight='bold', fontsize=11)
    ax.set_ylabel('R²')
    ax.set_ylim(0.65, 1.0)
    ax.grid(alpha=0.3)
    ax.legend(fontsize=9)

plt.suptitle('Evolución del R² a través de los escenarios temporales',
             fontsize=13, fontweight='bold')
savefig('06_evolucion_r2.png')

# =============================================================================
# RESUMEN
# =============================================================================
print("\n" + "=" * 65)
print("RESUMEN — GRÁFICOS GENERADOS EN graficos/comparativos/")
print("=" * 65)
print("  01_metricas_tuned_barras.png   — 4 métricas, barras agrupadas")
print("  02_heatmap_metricas.png        — heatmaps R²/RMSE/MAE/MAPE")
print("  03_base_vs_tuned_r2_rmse.png   — comparación antes/después tuning")
print("  04_radar_modelos.png           — perfil multidimensional (radar)")
print("  05_tabla_mejor_modelo.png      — tabla resumen mejor modelo")
print("  06_evolucion_r2.png            — R² Base vs Tuned a través de escenarios")
print("\n✓ Gráficos comparativos completados.")
