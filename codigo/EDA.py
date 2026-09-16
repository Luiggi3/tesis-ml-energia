# =============================================================================
# ANÁLISIS EXPLORATORIO DE DATOS (EDA) COMPLETO
# Tesis: Modelo predictivo del consumo energético en hogares inteligentes
# Dataset: Individual Household Electric Power Consumption (UCI)
# Período: Diciembre 2006 – Noviembre 2010 | Frecuencia original: 1 minuto
# =============================================================================

import os
import warnings
import matplotlib
# matplotlib.use('Agg')  # desactivado: permite ver gráficos en Spyder
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

warnings.filterwarnings('ignore')
plt.rcParams.update({'figure.dpi': 200, 'font.size': 15})

# ── Rutas ────────────────────────────────────────────────────────────────────
_here = os.path.dirname(os.path.abspath(__file__))
BASE_DIR   = _here if os.path.exists(os.path.join(_here, 'datos')) else os.path.dirname(_here)
DATA_PATH  = os.path.join(BASE_DIR, 'datos', 'household_power_consumption.txt')
GRAF_DIR   = os.path.join(BASE_DIR, 'graficos', 'eda')
DATOS_DIR  = os.path.join(BASE_DIR, 'datos')
os.makedirs(GRAF_DIR, exist_ok=True)

def savefig(nombre):
    plt.tight_layout()
    plt.savefig(os.path.join(GRAF_DIR, nombre), dpi=200, bbox_inches='tight')
    plt.show()
    plt.close()


# =============================================================================
# 1. CARGA DEL DATASET
# =============================================================================
print("=" * 70)
print("1. CARGA DEL DATASET")
print("=" * 70)

df_raw = pd.read_csv(
    DATA_PATH,
    sep=';',
    low_memory=False,
    na_values='?'
)

print(f"Forma del dataset raw:  {df_raw.shape[0]:,} filas × {df_raw.shape[1]} columnas")
print("\nColumnas y tipos originales:")
print(df_raw.dtypes)
print("\nPrimeras 5 filas:")
print(df_raw.head())
print("\nÚltimas 5 filas:")
print(df_raw.tail())


# =============================================================================
# 2. CONVERSIÓN Y PREPARACIÓN DEL ÍNDICE TEMPORAL
# =============================================================================
print("\n" + "=" * 70)
print("2. PREPARACIÓN DEL ÍNDICE TEMPORAL")
print("=" * 70)

df_raw['datetime'] = pd.to_datetime(
    df_raw['Date'] + ' ' + df_raw['Time'],
    format='%d/%m/%Y %H:%M:%S'
)
df_raw = df_raw.drop(columns=['Date', 'Time']).set_index('datetime')

COLS_ORIG = ['Global_active_power', 'Global_reactive_power', 'Voltage',
             'Global_intensity', 'Sub_metering_1', 'Sub_metering_2', 'Sub_metering_3']
for col in COLS_ORIG:
    df_raw[col] = pd.to_numeric(df_raw[col], errors='coerce')

RENAME = {
    'Global_active_power'   : 'GAP',
    'Global_reactive_power' : 'GRP',
    'Voltage'               : 'VOLT',
    'Global_intensity'      : 'GI',
    'Sub_metering_1'        : 'SM1',
    'Sub_metering_2'        : 'SM2',
    'Sub_metering_3'        : 'SM3',
}
df_raw = df_raw.rename(columns=RENAME)
VARS = list(RENAME.values())

print(f"Rango temporal:")
print(f"  Inicio:   {df_raw.index.min()}")
print(f"  Fin:      {df_raw.index.max()}")
print(f"  Duración: {df_raw.index.max() - df_raw.index.min()}")

idx_esperado   = pd.date_range(start=df_raw.index.min(),
                               end=df_raw.index.max(), freq='min')
faltantes_idx  = len(idx_esperado) - len(df_raw)
print(f"\nRegistros esperados (1 min continuo): {len(idx_esperado):,}")
print(f"Registros presentes:                  {len(df_raw):,}")
print(f"Timestamps faltantes:                 {faltantes_idx:,}")


# =============================================================================
# 3. ANÁLISIS DE CALIDAD DE DATOS Y VALORES NULOS
# =============================================================================
print("\n" + "=" * 70)
print("3. CALIDAD DE DATOS — VALORES NULOS")
print("=" * 70)

nulos     = df_raw[VARS].isnull().sum()
pct_nulos = (nulos / len(df_raw) * 100).round(3)
calidad   = pd.DataFrame({
    'No Nulos': len(df_raw) - nulos,
    'Nulos'   : nulos,
    '% Nulos' : pct_nulos
})
print(calidad.to_string())

# ── Gráfico 01: valores nulos ─────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

axes[0].bar(VARS, pct_nulos.values, color='#E74C3C', edgecolor='black', linewidth=0.7)
axes[0].set_title('% de Valores Nulos por Variable', fontweight='bold')
axes[0].set_ylabel('Porcentaje (%)')
axes[0].set_ylim(0, max(pct_nulos.values) * 1.4 + 0.1)
for i, v in enumerate(pct_nulos.values):
    axes[0].text(i, v + 0.02, f'{v:.2f}%', ha='center', va='bottom', fontsize=12.6)

nulos_mensual = df_raw[VARS].resample('ME').apply(lambda x: x.isnull().sum())
xticklabels   = [str(d)[:7] if i % 4 == 0 else '' for i, d in enumerate(nulos_mensual.index)]
sns.heatmap(nulos_mensual.T, ax=axes[1], cmap='Reds',
            xticklabels=xticklabels, yticklabels=VARS,
            linewidths=0.1, cbar_kws={'label': 'Cantidad de nulos'})
axes[1].set_xticklabels(xticklabels, rotation=45, ha='right', fontsize=11.2)
axes[1].tick_params(axis='y', labelsize=12, rotation=0)
axes[1].set_title('Mapa de Calor de Nulos — Mensual', fontweight='bold')

savefig('01_valores_nulos.png')
print("✓ Gráfico 01 guardado — valores nulos")


# =============================================================================
# 4. ESTADÍSTICAS DESCRIPTIVAS
# =============================================================================
print("\n" + "=" * 70)
print("4. ESTADÍSTICAS DESCRIPTIVAS")
print("=" * 70)

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.float_format', '{:.4f}'.format)

print(df_raw[VARS].describe().round(4))

skurt = pd.DataFrame({
    'Media'    : df_raw[VARS].mean().round(4),
    'Mediana'  : df_raw[VARS].median().round(4),
    'Desv.Est' : df_raw[VARS].std().round(4),
    'Skewness' : df_raw[VARS].skew().round(4),
    'Kurtosis' : df_raw[VARS].kurtosis().round(4),
})
print("\nResumen estadístico ampliado:")
print(skurt.to_string())

# Unidades de las variables
unidades = {
    'GAP' : 'kW  — Potencia activa global',
    'GRP' : 'kW  — Potencia reactiva global',
    'VOLT': 'V   — Voltaje',
    'GI'  : 'A   — Intensidad global',
    'SM1' : 'Wh  — Sub-medidor 1 (cocina)',
    'SM2' : 'Wh  — Sub-medidor 2 (lavandería)',
    'SM3' : 'Wh  — Sub-medidor 3 (calentador/AC)',
}
print("\nDescripción de variables:")
for k, v in unidades.items():
    print(f"  {k}: {v}")


# =============================================================================
# 5. SERIES DE TIEMPO — VARIABLES PRINCIPALES
# =============================================================================
print("\n" + "=" * 70)
print("5. SERIES DE TIEMPO")
print("=" * 70)

# ── Gráfico 02: series diarias de variables eléctricas ────────────────────
fig, axes = plt.subplots(4, 1, figsize=(16, 14))
cfg_series = [
    ('GAP',  'Potencia Activa Global — Promedio Diario (kW)',   '#1565C0'),
    ('GRP',  'Potencia Reactiva Global — Promedio Diario (kW)', '#E65100'),
    ('VOLT', 'Voltaje — Promedio Diario (V)',                   '#2E7D32'),
    ('GI',   'Intensidad Global — Promedio Diario (A)',         '#6A1B9A'),
]
for ax, (col, titulo, color) in zip(axes, cfg_series):
    serie = df_raw[col].resample('D').mean()
    ax.plot(serie.index, serie.values, color=color, linewidth=0.8, alpha=0.9)
    ax.set_title(titulo, fontweight='bold', fontsize=14)
    ax.set_ylabel(titulo.split('(')[1].replace(')', '').strip())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.setp(ax.get_xticklabels(), rotation=30, ha='right', fontsize=11.2)

plt.suptitle('Series Temporales — Variables Eléctricas (Promedio Diario)',
             fontsize=18.2, fontweight='bold', y=1.005)
savefig('02_series_tiempo_principales.png')
print("✓ Gráfico 02 guardado — series variables eléctricas")

# ── Gráfico 03: sub-medidores ─────────────────────────────────────────────
fig, axes = plt.subplots(3, 1, figsize=(16, 10))
cfg_sm = [
    ('SM1', 'Sub-medidor 1 — Cocina (Wh)',          '#E53935'),
    ('SM2', 'Sub-medidor 2 — Lavandería (Wh)',       '#8E24AA'),
    ('SM3', 'Sub-medidor 3 — Calentador / AC (Wh)', '#5D4037'),
]
for ax, (col, titulo, color) in zip(axes, cfg_sm):
    serie = df_raw[col].resample('D').mean()
    ax.fill_between(serie.index, serie.values, alpha=0.5, color=color)
    ax.plot(serie.index, serie.values, color=color, linewidth=0.6)
    ax.set_title(titulo, fontweight='bold', fontsize=14)
    ax.set_ylabel('Wh')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.setp(ax.get_xticklabels(), rotation=30, ha='right', fontsize=11.2)

plt.suptitle('Sub-medidores — Promedio Diario', fontsize=18.2, fontweight='bold')
savefig('03_series_submedidores.png')
print("✓ Gráfico 03 guardado — sub-medidores")


# =============================================================================
# 6. DISTRIBUCIONES — HISTOGRAMAS + KDE
# =============================================================================
print("\n" + "=" * 70)
print("6. DISTRIBUCIONES")
print("=" * 70)

colores_dist = ['#1565C0','#2E7D32','#F57F17','#6A1B9A','#B71C1C','#00695C','#4E342E']

fig, axes = plt.subplots(3, 3, figsize=(19, 15))
axes_flat = axes.flatten()

for i, (col, color) in enumerate(zip(VARS, colores_dist)):
    data = df_raw[col].dropna()
    axes_flat[i].hist(data, bins=120, color=color, alpha=0.6,
                      edgecolor='none', density=True)
    data.plot.kde(ax=axes_flat[i], color='black', linewidth=1.8)
    axes_flat[i].axvline(data.mean(),   color='red',    linestyle='--',
                          linewidth=1.2, label=f'Media: {data.mean():.3f}')
    axes_flat[i].axvline(data.median(), color='orange', linestyle=':',
                          linewidth=1.2, label=f'Mediana: {data.median():.3f}')
    axes_flat[i].set_title(f'{col}  |  Sk={data.skew():.2f}', fontweight='bold')
    axes_flat[i].legend(fontsize=9.8)

axes_flat[-1].set_visible(False)
plt.suptitle('Distribuciones de Variables — Histograma + KDE',
             fontsize=18.2, fontweight='bold')
savefig('04_distribuciones.png')
print("✓ Gráfico 04 guardado — distribuciones")


# =============================================================================
# 7. ANÁLISIS DE CORRELACIÓN
# =============================================================================
print("\n" + "=" * 70)
print("7. CORRELACIÓN")
print("=" * 70)

corr_mat = df_raw[VARS].corr().round(4)
print("Matriz de correlación (Pearson):")
print(corr_mat.to_string())

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

mask = np.triu(np.ones_like(corr_mat, dtype=bool), k=1)
sns.heatmap(corr_mat, ax=axes[0], annot=True, fmt='.3f',
            cmap='RdYlGn', vmin=-1, vmax=1,
            linewidths=0.4, annot_kws={'size': 12.6},
            mask=np.triu(np.ones_like(corr_mat, dtype=bool)))
axes[0].set_title('Matriz de Correlación (Pearson)', fontweight='bold')

corr_gap   = corr_mat['GAP'].drop('GAP').sort_values()
bar_colors = ['#E53935' if v < 0 else '#1E88E5' for v in corr_gap.values]
axes[1].barh(corr_gap.index, corr_gap.values, color=bar_colors, edgecolor='black', linewidth=0.5)
axes[1].axvline(0, color='black', linewidth=0.8)
axes[1].set_xlim(-1.1, 1.1)
axes[1].set_title('Correlación de Variables con GAP', fontweight='bold')
axes[1].set_xlabel('Coeficiente de Pearson')
for i, v in enumerate(corr_gap.values):
    offset = 0.03 if v >= 0 else -0.03
    ha     = 'left' if v >= 0 else 'right'
    axes[1].text(v + offset, i, f'{v:.3f}', va='center', ha=ha, fontsize=12.6)

savefig('05_correlacion.png')
print("✓ Gráfico 05 guardado — correlación")


# =============================================================================
# 8. PATRONES TEMPORALES
# =============================================================================
print("\n" + "=" * 70)
print("8. PATRONES TEMPORALES")
print("=" * 70)

df_temp = df_raw.copy()
df_temp['hora']        = df_temp.index.hour
df_temp['dia_semana']  = df_temp.index.dayofweek
df_temp['mes']         = df_temp.index.month
df_temp['anio']        = df_temp.index.year

DIAS  = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
MESES = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
          'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']

# ── Gráfico 06: patrones hora / día / mes / año ───────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(16, 10))

gap_hora = df_temp.groupby('hora')['GAP'].mean()
axes[0, 0].bar(gap_hora.index, gap_hora.values, color='#1565C0',
               edgecolor='black', linewidth=0.5)
axes[0, 0].set_title('Consumo Promedio por Hora del Día', fontweight='bold')
axes[0, 0].set_xlabel('Hora')
axes[0, 0].set_ylabel('GAP Promedio (kW)')
axes[0, 0].set_xticks(range(0, 24))

gap_dia = df_temp.groupby('dia_semana')['GAP'].mean()
colores_bar = ['#42A5F5'] * 5 + ['#EF5350'] * 2
axes[0, 1].bar(range(7), gap_dia.values, color=colores_bar,
               edgecolor='black', linewidth=0.5)
axes[0, 1].set_title('Consumo Promedio por Día de la Semana', fontweight='bold')
axes[0, 1].set_xlabel('Día')
axes[0, 1].set_ylabel('GAP Promedio (kW)')
axes[0, 1].set_xticks(range(7))
axes[0, 1].set_xticklabels(DIAS)

gap_mes = df_temp.groupby('mes')['GAP'].mean()
axes[1, 0].bar(range(1, 13), gap_mes.values, color='#388E3C',
               edgecolor='black', linewidth=0.5)
axes[1, 0].set_title('Consumo Promedio por Mes', fontweight='bold')
axes[1, 0].set_xlabel('Mes')
axes[1, 0].set_ylabel('GAP Promedio (kW)')
axes[1, 0].set_xticks(range(1, 13))
axes[1, 0].set_xticklabels(MESES, rotation=45)

gap_anio = df_temp.groupby('anio')['GAP'].mean()
axes[1, 1].bar(gap_anio.index, gap_anio.values, color='#7B1FA2',
               edgecolor='black', linewidth=0.5)
axes[1, 1].set_title('Consumo Promedio por Año', fontweight='bold')
axes[1, 1].set_xlabel('Año')
axes[1, 1].set_ylabel('GAP Promedio (kW)')

plt.suptitle('Patrones Temporales del Consumo Energético (GAP)',
             fontsize=18.2, fontweight='bold')
savefig('06_patrones_temporales.png')
print("✓ Gráfico 06 guardado — patrones temporales")

# ── Gráfico 07: heatmap hora × día de la semana ───────────────────────────
pivot_hd = df_temp.groupby(['dia_semana', 'hora'])['GAP'].mean().unstack()
pivot_hd.index = DIAS

fig, ax = plt.subplots(figsize=(14, 5))
sns.heatmap(pivot_hd, ax=ax, cmap='YlOrRd',
            xticklabels=range(24), yticklabels=DIAS,
            linewidths=0.2, cbar_kws={'label': 'GAP Promedio (kW)'})
ax.set_title('Consumo Promedio (GAP) — Hora × Día de la Semana',
             fontweight='bold', fontsize=16.8)
ax.set_xlabel('Hora del Día')
ax.set_ylabel('Día de la Semana')
savefig('07_heatmap_hora_dia.png')
print("✓ Gráfico 07 guardado — heatmap hora vs día")

# ── Gráfico 08: boxplot mensual ───────────────────────────────────────────
fig, ax = plt.subplots(figsize=(14, 6))
df_nonan = df_temp.dropna(subset=['GAP'])
data_mes = [df_nonan[df_nonan['mes'] == m]['GAP'].values for m in range(1, 13)]
bp = ax.boxplot(data_mes, patch_artist=True, notch=False,
                medianprops=dict(color='red', linewidth=2),
                flierprops=dict(marker='.', color='gray', alpha=0.2, markersize=1.5))
cmap_box = plt.cm.Set3(np.linspace(0, 1, 12))
for patch, c in zip(bp['boxes'], cmap_box):
    patch.set_facecolor(c)
    patch.set_alpha(0.8)
ax.set_xticklabels(MESES)
ax.set_title('Distribución de GAP por Mes', fontweight='bold', fontsize=16.8)
ax.set_xlabel('Mes')
ax.set_ylabel('GAP (kW)')
savefig('08_boxplot_mensual.png')
print("✓ Gráfico 08 guardado — boxplot mensual")


# =============================================================================
# 9. DETECCIÓN Y TRATAMIENTO DE OUTLIERS (MÉTODO IQR)
# =============================================================================
print("\n" + "=" * 70)
print("9. DETECCIÓN Y TRATAMIENTO DE OUTLIERS")
print("=" * 70)

df_noNaN = df_raw.dropna().copy()
print(f"Filas tras eliminar NaN: {len(df_noNaN):,}")

# IQR estándar para variables continuas; percentil 99.5 para sub-medidores
# esparcidos (IQR=0 en SM1 haría que el cap fuera 0, eliminando toda actividad)
VARS_CONTINUAS = ['GAP', 'GRP', 'VOLT', 'GI']
VARS_ESPARSAS  = ['SM1', 'SM2', 'SM3']

# Los umbrales IQR se calculan usando solo el 80% inicial (cronológico) de
# los datos, sin estadísticas del período de test, y luego se aplican al
# dataset completo.
split_iqr  = int(len(df_noNaN) * 0.80)
df_iqr_fit = df_noNaN.iloc[:split_iqr]
print(f"\nUmbrales IQR calculados solo con el 80% inicial (train): "
      f"{len(df_iqr_fit):,} de {len(df_noNaN):,} filas "
      f"({df_iqr_fit.index.min()} → {df_iqr_fit.index.max()})")

def calcular_umbrales(df_fuente, col):
    Q1  = df_fuente[col].quantile(0.25)
    Q3  = df_fuente[col].quantile(0.75)
    IQR = Q3 - Q1
    if col in VARS_CONTINUAS:
        li, ls, metodo = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR, '1.5×IQR'
    else:
        # Variables esparsas: solo cap superior en el percentil 99.5
        li, ls, metodo = 0.0, df_fuente[col].quantile(0.995), 'P99.5'
    return Q1, Q3, IQR, li, ls, metodo

fmt_hdr = f"{'Variable':<8} {'Q1':>8} {'Q3':>8} {'IQR':>8} {'Lím Inf':>10} {'Lím Sup':>10} {'N Outliers':>12} {'%':>6}  Método"

print("\n" + "-" * 80)
print("Umbrales IQR (calculados solo con train, aplicados a todo el dataset)")
print(fmt_hdr)
print("-" * 80)

stats_iqr = {}
comparacion_filas = []
for col in VARS:
    Q1, Q3, IQR, li, ls, metodo = calcular_umbrales(df_iqr_fit, col)
    n   = int(((df_noNaN[col] < li) | (df_noNaN[col] > ls)).sum())
    pct = n / len(df_noNaN) * 100
    stats_iqr[col] = (li, ls)
    print(f"{col:<8} {Q1:>8.3f} {Q3:>8.3f} {IQR:>8.3f} {li:>10.3f} {ls:>10.3f} {n:>12,} {pct:>5.1f}%  {metodo}")

    # Umbrales alternativos, calculados con el dataset completo — solo para comparar
    Q1_f, Q3_f, IQR_f, li_f, ls_f, _ = calcular_umbrales(df_noNaN, col)
    n_f   = int(((df_noNaN[col] < li_f) | (df_noNaN[col] > ls_f)).sum())
    pct_f = n_f / len(df_noNaN) * 100
    comparacion_filas.append({
        'Variable': col,
        'Lim_Inf_TodoDataset': round(li_f, 4), 'Lim_Sup_TodoDataset': round(ls_f, 4),
        'N_Outliers_TodoDataset': n_f, 'Pct_TodoDataset': round(pct_f, 3),
        'Lim_Inf_SoloTrain': round(li, 4), 'Lim_Sup_SoloTrain': round(ls, 4),
        'N_Outliers_SoloTrain': n, 'Pct_SoloTrain': round(pct, 3),
        'Diferencia_N_Outliers': n - n_f,
    })

df_comparacion_iqr = pd.DataFrame(comparacion_filas)
print("\n" + "-" * 80)
print("Comparación: umbrales calculados con todo el dataset vs. solo con el "
      "período de entrenamiento")
print(df_comparacion_iqr.to_string(index=False))

comparacion_csv = os.path.join(BASE_DIR, 'modelos', 'iqr_comparacion.csv')
os.makedirs(os.path.dirname(comparacion_csv), exist_ok=True)
df_comparacion_iqr.to_csv(comparacion_csv, index=False)
print(f"\n✓ Comparación de umbrales IQR guardada → modelos/iqr_comparacion.csv")

# ── Gráfico 09: boxplots ANTES ────────────────────────────────────────────
fig, axes = plt.subplots(2, 4, figsize=(21, 11))
axes_flat = axes.flatten()
for i, col in enumerate(VARS):
    axes_flat[i].boxplot(df_noNaN[col].values, patch_artist=True,
                         boxprops=dict(facecolor='#4C72B0', color='navy'),
                         medianprops=dict(color='red', linewidth=2),
                         flierprops=dict(marker='.', color='gray', alpha=0.2, markersize=1.5))
    axes_flat[i].set_title(col, fontweight='bold')
axes_flat[-1].set_visible(False)
plt.suptitle('Boxplots — Antes del Tratamiento de Outliers',
             fontsize=18.2, fontweight='bold')
savefig('09_boxplot_antes.png')
print("✓ Gráfico 09 guardado — boxplots antes")

# Aplicar filtro IQR simultáneo a todas las variables
mascara = pd.Series(True, index=df_noNaN.index)
for col, (li, ls) in stats_iqr.items():
    mascara = mascara & (df_noNaN[col] >= li) & (df_noNaN[col] <= ls)

df_final = df_noNaN[mascara].copy()

print(f"\nRegistros antes del filtro IQR:  {len(df_noNaN):,}")
print(f"Registros después del filtro IQR: {len(df_final):,}")
print(f"Outliers eliminados:              {len(df_noNaN) - len(df_final):,}")
print(f"Porcentaje eliminado:             {(len(df_noNaN) - len(df_final)) / len(df_noNaN) * 100:.2f}%")

# Verificación: ¿el filtro IQR deja periodos completos sin ningún minuto
# válido? Eso crearía huecos temporales artificiales en el resample
# posterior (resample().mean() de un periodo vacío = NaN → se elimina).
print("\nVerificación de huecos temporales inducidos por el filtro IQR:")
for freq_check, freq_label in [('15min', '15 minutos'), ('h', '1 hora'), ('D', '1 día')]:
    periodos_originales = df_noNaN[VARS[0]].resample(freq_check).count()
    periodos_tras_iqr   = df_final[VARS[0]].resample(freq_check).count()
    huecos_nuevos = int(((periodos_originales > 0) & (periodos_tras_iqr == 0)).sum())
    print(f"  Resolución {freq_label:<10}: {huecos_nuevos:,} periodos quedaron "
          f"sin ningún minuto válido tras el filtro IQR "
          f"(de {int((periodos_originales > 0).sum()):,} periodos con datos)")

# ── Gráfico 10: boxplots DESPUÉS ──────────────────────────────────────────
fig, axes = plt.subplots(2, 4, figsize=(21, 11))
axes_flat = axes.flatten()
for i, col in enumerate(VARS):
    axes_flat[i].boxplot(df_final[col].values, patch_artist=True,
                         boxprops=dict(facecolor='#55A868', color='darkgreen'),
                         medianprops=dict(color='red', linewidth=2),
                         flierprops=dict(marker='.', color='gray', alpha=0.2, markersize=1.5))
    axes_flat[i].set_title(col, fontweight='bold')
axes_flat[-1].set_visible(False)
plt.suptitle('Boxplots — Después del Tratamiento de Outliers',
             fontsize=18.2, fontweight='bold')
savefig('10_boxplot_despues.png')
print("✓ Gráfico 10 guardado — boxplots después")


# =============================================================================
# 10. DESCOMPOSICIÓN ESTACIONAL (SERIE DIARIA DE GAP)
# =============================================================================
print("\n" + "=" * 70)
print("10. DESCOMPOSICIÓN ESTACIONAL")
print("=" * 70)

try:
    from statsmodels.tsa.seasonal import seasonal_decompose

    gap_diario = df_raw['GAP'].resample('D').mean().interpolate()
    decomp     = seasonal_decompose(gap_diario, model='additive', period=365)

    fig, axes = plt.subplots(4, 1, figsize=(16, 14))
    componentes = [
        (gap_diario,     'Serie Original (kW)',  '#1565C0'),
        (decomp.trend,   'Tendencia (kW)',        '#E65100'),
        (decomp.seasonal,'Estacionalidad (kW)',   '#2E7D32'),
        (decomp.resid,   'Residual (kW)',         '#6A1B9A'),
    ]
    for ax, (data, titulo, color) in zip(axes, componentes):
        ax.plot(data.index, data.values, color=color, linewidth=0.9)
        ax.set_title(titulo, fontweight='bold')
        ax.set_ylabel('kW')
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
        plt.setp(ax.get_xticklabels(), rotation=30, ha='right', fontsize=11.2)

    plt.suptitle('Descomposición Estacional Aditiva — GAP Diario (Período = 365 días)',
                 fontsize=18.2, fontweight='bold')
    savefig('11_descomposicion_estacional.png')
    print("✓ Gráfico 11 guardado — descomposición estacional")

except ImportError:
    print("⚠ statsmodels no disponible — omitiendo descomposición estacional")
    print("  Instalar con: pip install statsmodels")


# =============================================================================
# 11. AUTOCORRELACIÓN (ACF / PACF) — DATOS HORARIOS
# =============================================================================
print("\n" + "=" * 70)
print("11. AUTOCORRELACIÓN (ACF / PACF)")
print("=" * 70)

try:
    from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

    gap_horario = df_raw['GAP'].resample('h').mean().dropna()
    print(f"Serie horaria: {len(gap_horario):,} puntos")

    fig, axes = plt.subplots(2, 1, figsize=(16, 8))
    plot_acf(gap_horario,  ax=axes[0], lags=168, alpha=0.05,
             title='Función de Autocorrelación (ACF) — GAP Horario (168 lags = 7 días)')
    plot_pacf(gap_horario, ax=axes[1], lags=48,  alpha=0.05,
              title='Función de Autocorrelación Parcial (PACF) — GAP Horario (48 lags = 2 días)')
    axes[0].set_xlabel('Lag (horas)')
    axes[1].set_xlabel('Lag (horas)')

    savefig('12_acf_pacf.png')
    print("✓ Gráfico 12 guardado — ACF / PACF")

except ImportError:
    print("⚠ statsmodels no disponible — omitiendo ACF/PACF")


# =============================================================================
# 12. ANÁLISIS DE SUBMEDIDORES — PARTICIPACIÓN EN EL CONSUMO
# =============================================================================
print("\n" + "=" * 70)
print("12. ANÁLISIS DE SUBMEDIDORES")
print("=" * 70)

df_sm_work = df_noNaN.copy()
df_sm_work['energia_total_wh'] = df_sm_work['GAP'] * 1000 / 60
df_sm_work['energia_otros']    = (
    df_sm_work['energia_total_wh']
    - df_sm_work['SM1']
    - df_sm_work['SM2']
    - df_sm_work['SM3']
).clip(lower=0)

# Consumo anual estimado
consumo_anual = df_sm_work['energia_total_wh'].resample('YE').sum() / 1_000_000
print("\nConsumo anual estimado (MWh):")
for año, mwh in consumo_anual.items():
    print(f"  {año.year}: {mwh:,.2f} MWh")

sm_total_sum  = df_sm_work[['SM1', 'SM2', 'SM3']].sum()
otros_total   = float(df_sm_work['energia_otros'].sum())
total_energia = float(df_sm_work['energia_total_wh'].sum())

labels_pie  = ['SM1 — Cocina', 'SM2 — Lavandería', 'SM3 — Calentador/AC', 'Otros circuitos']
sizes_pie   = list(sm_total_sum.values) + [otros_total]
colors_pie  = ['#E53935', '#8E24AA', '#5D4037', '#78909C']

df_sm_mensual = df_sm_work[['SM1', 'SM2', 'SM3', 'energia_total_wh']].resample('ME').sum()
df_sm_mensual['%SM1'] = (df_sm_mensual['SM1'] / df_sm_mensual['energia_total_wh'] * 100).fillna(0)
df_sm_mensual['%SM2'] = (df_sm_mensual['SM2'] / df_sm_mensual['energia_total_wh'] * 100).fillna(0)
df_sm_mensual['%SM3'] = (df_sm_mensual['SM3'] / df_sm_mensual['energia_total_wh'] * 100).fillna(0)

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

wedges, texts, autotexts = axes[0].pie(
    sizes_pie, labels=labels_pie, colors=colors_pie,
    autopct='%1.1f%%', startangle=90,
    wedgeprops=dict(edgecolor='white', linewidth=1.2)
)
for at in autotexts:
    at.set_fontsize(12.6)
axes[0].set_title('Distribución del Consumo Total por Circuito', fontweight='bold')

df_sm_plot = df_sm_mensual[['%SM1', '%SM2', '%SM3']].dropna()
# stackplot (no pandas .plot) para que el eje X quede en fechas reales de
# matplotlib — pandas .plot(kind='area') usa su propio locator interno que
# rompe el DateFormatter/MonthLocator aplicados después (etiquetas ilegibles).
axes[1].stackplot(df_sm_plot.index,
                   df_sm_plot['%SM1'], df_sm_plot['%SM2'], df_sm_plot['%SM3'],
                   colors=['#E53935', '#8E24AA', '#5D4037'], alpha=0.75)
axes[1].set_title('Distribución Mensual de Sub-medidores (%)', fontweight='bold')
axes[1].set_xlabel('Mes')
axes[1].set_ylabel('% del consumo total medido')
axes[1].legend(['SM1 — Cocina', 'SM2 — Lavandería', 'SM3 — Calentador'],
                loc='upper right', fontsize=11.2)
axes[1].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
axes[1].xaxis.set_major_locator(mdates.MonthLocator(interval=3))
plt.setp(axes[1].get_xticklabels(), rotation=45, ha='right', fontsize=11.2)

savefig('13_submedidores_participacion.png')
print("✓ Gráfico 13 guardado — participación de submedidores")


# =============================================================================
# 13. PREPROCESAMIENTO FINAL + FEATURE ENGINEERING + EXPORTACIÓN
# =============================================================================
print("\n" + "=" * 70)
print("13. PREPROCESAMIENTO FINAL Y EXPORTACIÓN")
print("=" * 70)

df_final['hora']        = df_final.index.hour
df_final['dia_semana']  = df_final.index.dayofweek
df_final['mes']         = df_final.index.month
df_final['anio']        = df_final.index.year
df_final['es_finde']    = df_final['dia_semana'].isin([5, 6]).astype(int)
df_final['semana_anio'] = df_final.index.isocalendar().week.astype(int)
df_final['trimestre']   = df_final.index.quarter

print(f"Dataset final:")
print(f"  Filas:    {len(df_final):,}")
print(f"  Columnas: {list(df_final.columns)}")
print(f"  Período:  {df_final.index.min()} → {df_final.index.max()}")
print(f"  Nulos:    {df_final.isnull().sum().sum()}")

output_csv = os.path.join(DATOS_DIR, 'dataset_limpio.csv')
df_final.to_csv(output_csv)
print(f"\n✓ Dataset limpio exportado → {output_csv}")

# Segunda versión SIN filtro de outliers (solo se eliminan nulos), con las
# mismas columnas derivadas — para poder comparar el efecto del filtro IQR
# sobre el desempeño de los modelos.
df_sin_outliers = df_noNaN.copy()
df_sin_outliers['hora']        = df_sin_outliers.index.hour
df_sin_outliers['dia_semana']  = df_sin_outliers.index.dayofweek
df_sin_outliers['mes']         = df_sin_outliers.index.month
df_sin_outliers['anio']        = df_sin_outliers.index.year
df_sin_outliers['es_finde']    = df_sin_outliers['dia_semana'].isin([5, 6]).astype(int)
df_sin_outliers['semana_anio'] = df_sin_outliers.index.isocalendar().week.astype(int)
df_sin_outliers['trimestre']   = df_sin_outliers.index.quarter

output_csv_sin = os.path.join(DATOS_DIR, 'dataset_sin_outliers.csv')
df_sin_outliers.to_csv(output_csv_sin)
print(f"✓ Dataset SIN filtro de outliers exportado → {output_csv_sin} "
      f"({len(df_sin_outliers):,} filas, solo nulos removidos)")


# =============================================================================
# RESUMEN FINAL DEL EDA
# =============================================================================
print("\n" + "=" * 70)
print("RESUMEN DEL EDA")
print("=" * 70)
print(f"  Registros en raw:              {len(df_raw):,}")
print(f"  Registros tras eliminar NaN:   {len(df_noNaN):,}")
print(f"  Registros tras filtro IQR:     {len(df_final):,}")
print(f"  Porcentaje total eliminado:    {(1 - len(df_final)/len(df_raw))*100:.2f}%")
print(f"  Variables originales:          {len(VARS)}")
print(f"  Variables finales (con feats): {len(df_final.columns)}")
print(f"  Gráficos generados:            13")
print(f"  Directorio de gráficos:        {GRAF_DIR}")
print(f"  Dataset limpio:                {output_csv}")
print("\n✓ EDA completado exitosamente.")
