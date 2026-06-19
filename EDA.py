# =============================================================================
# ANÁLISIS EXPLORATORIO DE DATOS (EDA)
# Tesis: Modelo predictivo del consumo energético en hogares inteligentes
# =============================================================================

# ── 1. LIBRERÍAS ──────────────────────────────────────────────────────────────
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ── 2. CARGA DEL DATASET ──────────────────────────────────────────────────────
df = pd.read_csv(r'C:\Users\USER\Desktop\Tesis_ML_Energia\datos\household_power_consumption.txt',
                 sep=';',
                 low_memory=False)

print("=" * 50)
print("FORMA DEL DATASET:")
print(f"Filas: {df.shape[0]}, Columnas: {df.shape[1]}")
print("\nPRIMERAS 5 FILAS:")
print(df.head())
print("\nTIPO DE DATOS:")
print(df.dtypes)
print("\nVALORES NULOS:")
print(df.isnull().sum())

# ── 3. CONVERSIÓN DE TIEMPO ───────────────────────────────────────────────────
df['datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'],
                                format='%d/%m/%Y %H:%M:%S')
df = df.drop(columns=['Date', 'Time'])
df = df.set_index('datetime')

# Convertir columnas a numérico
cols_numericas = ['Global_active_power', 'Global_reactive_power', 'Voltage',
                  'Global_intensity', 'Sub_metering_1', 'Sub_metering_2',
                  'Sub_metering_3']

for col in cols_numericas:
    df[col] = pd.to_numeric(df[col], errors='coerce')

print("\nFecha inicio:", df.index.min())
print("Fecha fin:", df.index.max())
print("Duración:", df.index.max() - df.index.min())

# ── 4. RENOMBRE DE VARIABLES ──────────────────────────────────────────────────
df = df.rename(columns={
    'Global_active_power'   : 'GAP',
    'Global_reactive_power' : 'GRP',
    'Voltage'               : 'VOLT',
    'Global_intensity'      : 'GI',
    'Sub_metering_1'        : 'SM1',
    'Sub_metering_2'        : 'SM2',
    'Sub_metering_3'        : 'SM3',
})

print("\nColumnas renombradas:")
print(df.columns.tolist())

# ── 5. ESTADÍSTICAS DESCRIPTIVAS ──────────────────────────────────────────────
print("\nESTADÍSTICAS DESCRIPTIVAS:")
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
print(df.describe().round(2))

# ── 6. SERIES DE TIEMPO ───────────────────────────────────────────────────────
fig, axes = plt.subplots(3, 1, figsize=(14, 10))

df['GAP'].resample('D').mean().plot(ax=axes[0], color='blue')
axes[0].set_title('Potencia Activa Global (GAP) - Promedio Diario')
axes[0].set_ylabel('kW')

df['VOLT'].resample('D').mean().plot(ax=axes[1], color='orange')
axes[1].set_title('Voltaje (VOLT) - Promedio Diario')
axes[1].set_ylabel('V')

df['GI'].resample('D').mean().plot(ax=axes[2], color='green')
axes[2].set_title('Intensidad Global (GI) - Promedio Diario')
axes[2].set_ylabel('A')

plt.tight_layout()
plt.savefig(r'C:\Users\USER\Desktop\Tesis_ML_Energia\graficos\series_tiempo.png', dpi=150)
plt.show()

# Sub-medidores
fig, axes = plt.subplots(3, 1, figsize=(14, 10))
colores = ['red', 'purple', 'brown']
labels = ['SM1 - Cocina', 'SM2 - Lavandería', 'SM3 - Calentador/AC']

for i, (col, color, label) in enumerate(zip(['SM1','SM2','SM3'], colores, labels)):
    df[col].resample('D').mean().plot(ax=axes[i], color=color)
    axes[i].set_title(label)
    axes[i].set_ylabel('W')

plt.tight_layout()
plt.savefig(r'C:\Users\USER\Desktop\Tesis_ML_Energia\graficos\sub_medidores.png', dpi=150)
plt.show()

# ── 7. PREPROCESAMIENTO ───────────────────────────────────────────────────────

# 7.1 ELIMINACIÓN DE NULOS
print("=" * 55)
print("ELIMINACIÓN DE VALORES NULOS")
print("=" * 55)
print(f"Filas antes de limpiar:  {len(df)}")
print(f"Valores nulos por columna:\n{df.isnull().sum()}")
df = df.dropna()
print(f"\nFilas después de limpiar: {len(df)}")
print(f"Valores nulos restantes:  {df.isnull().sum().sum()}")
print("Limpieza completada")

# 7.2 DETECCIÓN DE OUTLIERS (IQR)
variables_numericas = ['GAP', 'GRP', 'VOLT', 'GI', 'SM1', 'SM2', 'SM3']

print("\n" + "=" * 75)
print(f"{'Variable':<10} {'Q1':>8} {'Q3':>8} {'IQR':>8} {'Lím Inf':>10} {'Lím Sup':>10} {'Outliers':>10}")
print("=" * 75)

for col in variables_numericas:
    Q1  = df[col].quantile(0.25)
    Q3  = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lim_inf    = Q1 - 1.5 * IQR
    lim_sup    = Q3 + 1.5 * IQR
    n_outliers = ((df[col] < lim_inf) | (df[col] > lim_sup)).sum()
    pct        = (n_outliers / len(df)) * 100
    print(f"{col:<10} {Q1:>8.3f} {Q3:>8.3f} {IQR:>8.3f} {lim_inf:>10.3f} {lim_sup:>10.3f} {n_outliers:>8} ({pct:.1f}%)")

print("=" * 75)

# 7.3 BOXPLOT ANTES DE OUTLIERS
fig, axes = plt.subplots(2, 4, figsize=(16, 8))
axes = axes.flatten()

for i, col in enumerate(variables_numericas):
    axes[i].boxplot(df[col].dropna(), patch_artist=True,
                    boxprops=dict(facecolor='#4C72B0', color='navy'),
                    medianprops=dict(color='red', linewidth=2),
                    whiskerprops=dict(color='navy'),
                    capprops=dict(color='navy'),
                    flierprops=dict(marker='o', color='gray', alpha=0.3, markersize=2))
    axes[i].set_title(col, fontsize=10, fontweight='bold')

axes[-1].set_visible(False)
plt.suptitle('Boxplots - Antes del tratamiento de outliers',
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(r'C:\Users\USER\Desktop\Tesis_ML_Energia\graficos\boxplot_antes.png',
            dpi=150, bbox_inches='tight')
plt.show()
print("Boxplot antes guardado")

# 7.4 ELIMINACIÓN DE OUTLIERS - VARIABLE OBJETIVO GAP
mascara = pd.Series([True] * len(df), index=df.index)

for col in variables_numericas:
    Q1  = df[col].quantile(0.25)
    Q3  = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lim_inf = Q1 - 1.5 * IQR
    lim_sup = Q3 + 1.5 * IQR
    mascara = mascara & (df[col] >= lim_inf) & (df[col] <= lim_sup)

df_limpio = df[mascara]

print(f"Filas antes de outliers:   {len(df)}")
print(f"Filas después de outliers: {len(df_limpio)}")
print(f"Outliers eliminados:       {len(df) - len(df_limpio)}")
print(f"Porcentaje eliminado:      {((len(df) - len(df_limpio))/len(df))*100:.1f}%")

# 7.5 BOXPLOT DESPUÉS DE OUTLIERS
fig, axes = plt.subplots(2, 4, figsize=(16, 8))
axes = axes.flatten()

for i, col in enumerate(variables_numericas):
    axes[i].boxplot(df_limpio[col].dropna(), patch_artist=True,
                    boxprops=dict(facecolor='#55A868', color='darkgreen'),
                    medianprops=dict(color='red', linewidth=2),
                    whiskerprops=dict(color='darkgreen'),
                    capprops=dict(color='darkgreen'),
                    flierprops=dict(marker='o', color='gray', alpha=0.3, markersize=2))
    axes[i].set_title(col, fontsize=10, fontweight='bold')

axes[-1].set_visible(False)
plt.suptitle('Boxplots - Después del tratamiento de outliers',
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(r'C:\Users\USER\Desktop\Tesis_ML_Energia\graficos\boxplot_despues.png',
            dpi=150, bbox_inches='tight')
plt.show()
print("Boxplot después guardado")

# ── 8. SELECCIÓN DE VARIABLES ─────────────────────────────────────────────────
variables_independientes = ['GRP', 'VOLT', 'GI', 'SM1', 'SM2', 'SM3']
variable_dependiente     = 'GAP'

X = df_limpio[variables_independientes]
y = df_limpio[variable_dependiente]

print(f"\nVariable dependiente: {variable_dependiente}")
print(f"Variables independientes: {variables_independientes}")
print(f"X shape: {X.shape}")
print(f"y shape: {y.shape}")