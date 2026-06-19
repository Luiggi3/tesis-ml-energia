# =============================================================================
# GENERADOR DE INFORME WORD — Documentación completa del proyecto de tesis
# =============================================================================

import os
import pandas as pd
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

_here = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = _here if os.path.exists(os.path.join(_here, 'datos')) else os.path.dirname(_here)
MOD_DIR  = os.path.join(BASE_DIR, 'modelos')
GRAF_EDA = os.path.join(BASE_DIR, 'graficos', 'eda')
GRAF_E1  = os.path.join(BASE_DIR, 'graficos', 'escenario1')
GRAF_E2  = os.path.join(BASE_DIR, 'graficos', 'escenario2')
GRAF_E3  = os.path.join(BASE_DIR, 'graficos', 'escenario3')
GRAF_TUN = os.path.join(BASE_DIR, 'graficos', 'tuning')
GRAF_CMP = os.path.join(BASE_DIR, 'graficos', 'comparativos')
OUT_FILE = os.path.join(BASE_DIR, 'Informe_Tesis_ML_Energia.docx')

# ── Datos de métricas ────────────────────────────────────────────────────────
df_res = pd.read_csv(os.path.join(MOD_DIR, 'tuning_resultados.csv'))
df_base  = df_res[df_res['Etapa'] == 'Base'].copy()
df_tuned = df_res[df_res['Etapa'] == 'Tuned'].copy()

ESCENARIOS = ['15 Minutos', '1 Hora', '1 Día']
ESC_SHORT  = ['15 min', '1 hora', '1 día']
MODELOS    = ['Random Forest', 'XGBoost', 'SVR']

# =============================================================================
# HELPERS
# =============================================================================

def set_cell_bg(cell, hex_color):
    tc   = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd  = OxmlElement('w:shd')
    shd.set(qn('w:val'),   'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'),  hex_color)
    tcPr.append(shd)

def add_image_safe(doc, path, width=Inches(6.0), caption=None):
    if os.path.exists(path):
        p = doc.add_picture(path, width=width)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if caption:
            c = doc.add_paragraph(caption)
            c.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = c.runs[0]
            run.font.size = Pt(9)
            run.font.italic = True
            run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
    else:
        doc.add_paragraph(f'[Gráfico no encontrado: {os.path.basename(path)}]')

def heading(doc, text, level):
    h = doc.add_heading(text, level=level)
    h.runs[0].font.color.rgb = RGBColor(0x1A, 0x23, 0x7E) if level == 1 else RGBColor(0x1B, 0x5E, 0x20) if level == 2 else RGBColor(0x33, 0x33, 0x33)
    return h

def body(doc, text):
    p = doc.add_paragraph(text)
    p.paragraph_format.space_after = Pt(6)
    return p

def metrics_table(doc, df_data, escenario, caption=None):
    rows_data = []
    for mod in MODELOS:
        row = df_data[(df_data['Escenario']==escenario)&(df_data['Modelo']==mod)]
        if not row.empty:
            r = row.iloc[0]
            rows_data.append([mod, f"{r['RMSE']:.4f}", f"{r['MAE']:.4f}",
                              f"{r['MAPE']:.2f}%", f"{r['R2']:.4f}"])

    t = doc.add_table(rows=1 + len(rows_data), cols=5)
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER

    # Encabezado
    headers = ['Modelo', 'RMSE (kW)', 'MAE (kW)', 'MAPE (%)', 'R²']
    for j, h in enumerate(headers):
        cell = t.rows[0].cells[j]
        cell.text = h
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(10)
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        set_cell_bg(cell, '1A237E')

    # Datos
    model_colors = {'Random Forest': 'E3F2FD', 'XGBoost': 'E8F5E9', 'SVR': 'FFEBEE'}
    for i, row_vals in enumerate(rows_data):
        bg = model_colors.get(row_vals[0], 'FFFFFF')
        # Encontrar mejor R² para marcar en negrita
        r2_vals = [float(r[4]) for r in rows_data]
        best_r2 = max(r2_vals)
        for j, val in enumerate(row_vals):
            cell = t.rows[i+1].cells[j]
            cell.text = val
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER if j > 0 else WD_ALIGN_PARAGRAPH.LEFT
            run = cell.paragraphs[0].runs[0]
            run.font.size = Pt(10)
            set_cell_bg(cell, bg)
            # Negrita al mejor R²
            if j == 4 and float(val) == best_r2:
                run.font.bold = True

    if caption:
        c = doc.add_paragraph(caption)
        c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        c.runs[0].font.size = Pt(9)
        c.runs[0].font.italic = True
        c.runs[0].font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    return t

def add_hr(doc):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after  = Pt(2)
    pPr = p._p.get_or_add_pPr()
    pb  = OxmlElement('w:pBdr')
    bot = OxmlElement('w:bottom')
    bot.set(qn('w:val'),  'single')
    bot.set(qn('w:sz'),   '6')
    bot.set(qn('w:space'),'1')
    bot.set(qn('w:color'),'AAAAAA')
    pb.append(bot)
    pPr.append(pb)

# =============================================================================
# CREAR DOCUMENTO
# =============================================================================

doc = Document()

# Márgenes: 2.5 cm
for section in doc.sections:
    section.top_margin    = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin   = Cm(3.0)
    section.right_margin  = Cm(2.5)

# Estilo base
style = doc.styles['Normal']
style.font.name = 'Calibri'
style.font.size = Pt(11)

# =============================================================================
# PORTADA
# =============================================================================

doc.add_paragraph()
doc.add_paragraph()
doc.add_paragraph()

title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = title.add_run('MODELO PREDICTIVO DEL CONSUMO ENERGÉTICO\nEN HOGARES INTELIGENTES UTILIZANDO\nALGORITMOS DE MACHINE LEARNING')
run.font.size = Pt(20)
run.font.bold = True
run.font.color.rgb = RGBColor(0x1A, 0x23, 0x7E)

doc.add_paragraph()

sub = doc.add_paragraph()
sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = sub.add_run('Documentación Técnica del Proyecto de Tesis')
r.font.size = Pt(14)
r.font.italic = True
r.font.color.rgb = RGBColor(0x42, 0x42, 0x42)

doc.add_paragraph()
doc.add_paragraph()

info = doc.add_paragraph()
info.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = info.add_run('Dataset: UCI Household Electric Power Consumption\n'
                  'Período: 2006 – 2010  |  País: Francia\n'
                  'Modelos: Random Forest · XGBoost · SVR\n'
                  'Escenarios: 15 minutos · 1 hora · 1 día')
r.font.size = Pt(12)
r.font.color.rgb = RGBColor(0x33, 0x33, 0x33)

doc.add_paragraph()

fecha = doc.add_paragraph()
fecha.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = fecha.add_run('2026')
r.font.size = Pt(12)
r.font.bold = True

doc.add_page_break()

# =============================================================================
# RESUMEN EJECUTIVO
# =============================================================================

heading(doc, '1. Resumen Ejecutivo', 1)
add_hr(doc)

body(doc,
    'Este documento presenta la documentación técnica completa del proyecto de tesis '
    '"Modelo predictivo del consumo energético en hogares inteligentes utilizando '
    'algoritmos de machine learning". Se describen en detalle todas las etapas del '
    'proceso: carga y limpieza de datos, análisis exploratorio, preparación de '
    'características, entrenamiento de modelos, tuning de hiperparámetros y análisis '
    'comparativo de resultados.')

body(doc,
    'El estudio emplea el dataset público UCI Household Electric Power Consumption, '
    'que contiene 2,075,259 registros de consumo eléctrico residencial a frecuencia '
    'de 1 minuto, recolectados en Francia entre 2006 y 2010. Se evaluaron tres '
    'algoritmos de machine learning — Random Forest, XGBoost y Support Vector '
    'Regression (SVR) — bajo tres horizontes temporales de predicción: 15 minutos, '
    '1 hora y 1 día.')

body(doc,
    'Los mejores resultados tras optimización de hiperparámetros con GridSearchCV '
    'fueron: R²=0.9145 para el escenario de 15 minutos (Random Forest), R²=0.8812 '
    'para 1 hora (XGBoost) y R²=0.7848 para 1 día (SVR). El tuning resultó '
    'especialmente beneficioso para SVR, modelo que mostró las mayores mejoras en '
    'todos los escenarios.')

doc.add_page_break()

# =============================================================================
# INTRODUCCIÓN
# =============================================================================

heading(doc, '2. Introducción y Contexto', 1)
add_hr(doc)

body(doc,
    'La predicción del consumo energético en hogares inteligentes es un problema '
    'central en el diseño de redes eléctricas eficientes (smart grids). Anticipar '
    'la demanda con precisión permite optimizar la distribución de energía, reducir '
    'costos operativos y facilitar la integración de fuentes de energía renovable.')

body(doc,
    'El objetivo de este trabajo es comparar el desempeño de tres algoritmos de '
    'machine learning ampliamente utilizados en tareas de regresión de series de '
    'tiempo (Random Forest, XGBoost y SVR) para predecir el consumo eléctrico '
    'global activo (GAP) en diferentes horizontes de tiempo.')

heading(doc, '2.1 Variable objetivo', 2)
body(doc,
    'La variable a predecir es el Global Active Power (GAP), medida en kilowatts (kW), '
    'que representa la potencia activa promedio consumida por el hogar en cada '
    'intervalo de tiempo. Esta variable captura el comportamiento general de consumo '
    'del hogar y es la más informativa para fines de predicción.')

doc.add_page_break()

# =============================================================================
# DATASET
# =============================================================================

heading(doc, '3. Dataset', 1)
add_hr(doc)

heading(doc, '3.1 Descripción general', 2)
body(doc,
    'Se utilizó el dataset "Individual Household Electric Power Consumption" '
    'disponible en el repositorio UCI Machine Learning Repository. Este dataset '
    'contiene mediciones de consumo eléctrico de un hogar residencial ubicado en '
    'Sceaux, Francia, recolectadas entre el 16 de diciembre de 2006 y el 26 de '
    'noviembre de 2010, a una frecuencia de un minuto.')

# Tabla de variables
heading(doc, '3.2 Variables del dataset', 2)

t_vars = doc.add_table(rows=9, cols=3)
t_vars.style = 'Table Grid'
t_vars.alignment = WD_TABLE_ALIGNMENT.CENTER

headers_v = ['Variable original', 'Alias usado', 'Descripción']
col_widths = [Inches(1.6), Inches(1.0), Inches(3.6)]
for j, (h, w) in enumerate(zip(headers_v, col_widths)):
    cell = t_vars.rows[0].cells[j]
    cell.text = h
    cell.width = w
    cell.paragraphs[0].runs[0].font.bold = True
    cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    set_cell_bg(cell, '1A237E')

vars_data = [
    ('Date / Time',                     'datetime (índice)', 'Marca de tiempo (minuto a minuto)'),
    ('Global_active_power',             'GAP',  'Potencia activa global del hogar (kW) — variable objetivo'),
    ('Global_reactive_power',           'GRP',  'Potencia reactiva global (kW)'),
    ('Voltage',                         'VOLT', 'Voltaje promedio (V)'),
    ('Global_intensity',                'GI',   'Intensidad de corriente global (A) — descartada por colinealidad'),
    ('Sub_metering_1',                  'SM1',  'Cocina: lavavajillas, horno, microondas (Wh)'),
    ('Sub_metering_2',                  'SM2',  'Lavandería: lavadora, secadora, heladera (Wh)'),
    ('Sub_metering_3',                  'SM3',  'Calefacción y aire acondicionado (Wh)'),
]
for i, (orig, alias, desc) in enumerate(vars_data):
    row = t_vars.rows[i+1]
    row.cells[0].text = orig
    row.cells[1].text = alias
    row.cells[2].text = desc
    bg = 'F5F5F5' if i % 2 == 0 else 'FFFFFF'
    for cell in row.cells:
        cell.paragraphs[0].runs[0].font.size = Pt(9.5)
        set_cell_bg(cell, bg)

c = doc.add_paragraph('Tabla 1. Variables del dataset UCI Household Electric Power Consumption.')
c.alignment = WD_ALIGN_PARAGRAPH.CENTER
c.runs[0].font.size = Pt(9); c.runs[0].font.italic = True

heading(doc, '3.3 Estadísticas generales', 2)

t_stat = doc.add_table(rows=5, cols=2)
t_stat.style = 'Table Grid'
t_stat.alignment = WD_TABLE_ALIGNMENT.CENTER
stats_data = [
    ('Total de registros originales', '2,075,259'),
    ('Frecuencia de muestreo', '1 minuto'),
    ('Período cubierto', '16/12/2006 – 26/11/2010 (≈ 4 años)'),
    ('Porcentaje de valores nulos', '1.252 % (simultáneos en todas las columnas)'),
    ('Registros tras limpieza (dropna + IQR)', '1,739,167'),
]
for i, (k, v) in enumerate(stats_data):
    row = t_stat.rows[i]
    row.cells[0].text = k
    row.cells[1].text = v
    row.cells[0].paragraphs[0].runs[0].font.bold = True
    row.cells[0].paragraphs[0].runs[0].font.size = Pt(10)
    row.cells[1].paragraphs[0].runs[0].font.size = Pt(10)
    bg = 'EDE7F6' if i % 2 == 0 else 'FFFFFF'
    set_cell_bg(row.cells[0], bg)
    set_cell_bg(row.cells[1], bg)

c = doc.add_paragraph('Tabla 2. Estadísticas generales del dataset.')
c.alignment = WD_ALIGN_PARAGRAPH.CENTER
c.runs[0].font.size = Pt(9); c.runs[0].font.italic = True

heading(doc, '3.4 Limpieza de datos', 2)
body(doc,
    'El proceso de limpieza consistió en dos pasos:')
p = doc.add_paragraph(style='List Number')
p.add_run('Eliminación de nulos (dropna): ').bold = True
p.add_run('Los registros con valores faltantes representan el 1.252% del total '
          'y aparecen de forma simultánea en todas las columnas, lo que indica '
          'períodos sin medición. Se eliminaron directamente.')
p = doc.add_paragraph(style='List Number')
p.add_run('Filtro de outliers (IQR): ').bold = True
p.add_run('Se aplicó el método del rango intercuartílico (IQR) por columna. Los valores '
          'fuera del rango [Q1 − 1.5·IQR, Q3 + 1.5·IQR] fueron eliminados. '
          'Nota: la variable SM1 (cocina) quedó en cero en el dataset limpio porque '
          'su distribución es muy esparsa (Q1=Q3=0), y el filtro IQR eliminó todos '
          'sus valores no-nulos como outliers. Esta es una limitación conocida del '
          'método en variables de distribución asimétrica.')

body(doc,
    'La variable GI (Global Intensity) fue descartada en todos los escenarios por '
    'presentar una correlación de Pearson de 0.999 con GAP, lo que introduce '
    'multicolinealidad severa en los modelos.')

doc.add_page_break()

# =============================================================================
# EDA
# =============================================================================

heading(doc, '4. Análisis Exploratorio de Datos (EDA)', 1)
add_hr(doc)

body(doc,
    'El EDA se realizó sobre el dataset limpio (1,739,167 registros) e incluyó '
    'análisis de series temporales, distribuciones, patrones estacionales, '
    'correlaciones y descomposición estacional. Se generaron 13 gráficos '
    'documentados en la carpeta graficos/eda/.')

heading(doc, '4.1 Series de tiempo — variables principales', 2)
add_image_safe(doc,
    os.path.join(GRAF_EDA, '02_series_tiempo_principales.png'),
    width=Inches(6.0),
    caption='Figura 1. Series de tiempo de las variables principales (GAP, GRP, VOLT).')

heading(doc, '4.2 Correlación entre variables', 2)
body(doc,
    'El mapa de calor de correlaciones confirmó la alta colinealidad entre GAP y GI '
    '(r=0.999), justificando la exclusión de GI como feature. Las demás variables '
    'presentan correlaciones moderadas con GAP.')
add_image_safe(doc,
    os.path.join(GRAF_EDA, '05_correlacion.png'),
    width=Inches(5.0),
    caption='Figura 2. Mapa de calor de correlaciones entre variables.')

heading(doc, '4.3 Patrones temporales', 2)
body(doc,
    'El análisis de patrones por hora del día y día de la semana revela '
    'comportamientos recurrentes: mayor consumo en horas de la noche (18–22 h) '
    'y diferencias entre días de semana y fin de semana. Estas regularidades '
    'motivaron la creación de features temporales (hora, día de la semana, '
    'fin de semana).')
add_image_safe(doc,
    os.path.join(GRAF_EDA, '06_patrones_temporales.png'),
    width=Inches(6.0),
    caption='Figura 3. Patrones de consumo por hora del día y día de la semana.')
add_image_safe(doc,
    os.path.join(GRAF_EDA, '07_heatmap_hora_dia.png'),
    width=Inches(5.5),
    caption='Figura 4. Heatmap de consumo promedio por hora y día de la semana.')

heading(doc, '4.4 Distribuciones y outliers', 2)
body(doc,
    'Las distribuciones de GAP muestran asimetría positiva con valores extremos '
    'en períodos de alta demanda. Las cajas antes y después del filtro IQR '
    'ilustran el efecto de la limpieza.')
add_image_safe(doc,
    os.path.join(GRAF_EDA, '04_distribuciones.png'),
    width=Inches(6.0),
    caption='Figura 5. Distribuciones de las variables numéricas.')

heading(doc, '4.5 Descomposición estacional y autocorrelación', 2)
body(doc,
    'La descomposición estacional de GAP mediante STL revela componentes de '
    'tendencia, estacionalidad y residuo. El análisis ACF/PACF confirma la '
    'dependencia temporal y guió la selección de los lags para el feature engineering.')
add_image_safe(doc,
    os.path.join(GRAF_EDA, '11_descomposicion_estacional.png'),
    width=Inches(6.0),
    caption='Figura 6. Descomposición estacional de GAP.')
add_image_safe(doc,
    os.path.join(GRAF_EDA, '12_acf_pacf.png'),
    width=Inches(6.0),
    caption='Figura 7. Funciones de autocorrelación (ACF) y autocorrelación parcial (PACF).')

doc.add_page_break()

# =============================================================================
# PREPARACIÓN DE DATOS
# =============================================================================

heading(doc, '5. Preparación de Datos por Escenario', 1)
add_hr(doc)

body(doc,
    'A partir del dataset limpio (dataset_limpio.csv) se generaron tres versiones '
    'del conjunto de datos mediante remuestreo temporal (resample), cada una '
    'correspondiente a un escenario de predicción diferente.')

heading(doc, '5.1 Remuestreo temporal (resample)', 2)

t_res = doc.add_table(rows=4, cols=4)
t_res.style = 'Table Grid'
t_res.alignment = WD_TABLE_ALIGNMENT.CENTER
res_headers = ['Escenario', 'Frecuencia', 'Registros resultantes', 'Función pandas']
for j, h in enumerate(res_headers):
    cell = t_res.rows[0].cells[j]
    cell.text = h
    cell.paragraphs[0].runs[0].font.bold = True
    cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    set_cell_bg(cell, '1B5E20')
res_rows = [
    ('Escenario 1', '15 minutos', '133,393', "df.resample('15min').mean()"),
    ('Escenario 2', '1 hora',    '33,839',  "df.resample('h').mean()"),
    ('Escenario 3', '1 día',     '1,403',   "df.resample('D').mean()"),
]
for i, row_vals in enumerate(res_rows):
    bg = 'F1F8E9' if i % 2 == 0 else 'FFFFFF'
    for j, val in enumerate(res_rows[i]):
        cell = t_res.rows[i+1].cells[j]
        cell.text = val
        cell.paragraphs[0].runs[0].font.size = Pt(10)
        set_cell_bg(cell, bg)
c = doc.add_paragraph('Tabla 3. Resumen del remuestreo por escenario.')
c.alignment = WD_ALIGN_PARAGRAPH.CENTER
c.runs[0].font.size = Pt(9); c.runs[0].font.italic = True

heading(doc, '5.2 Feature Engineering', 2)
body(doc,
    'Para cada escenario se construyeron las siguientes categorías de features:')

p = doc.add_paragraph(style='List Bullet')
p.add_run('Features temporales: ').bold = True
p.add_run('hora del día, día de la semana, mes, indicador de fin de semana. '
          'Para el escenario diario se añaden trimestre y día del año.')

p = doc.add_paragraph(style='List Bullet')
p.add_run('Lags de GAP: ').bold = True
p.add_run('valores retardados de la variable objetivo. '
          'E1: lags [1, 2, 4, 8, 12, 96] períodos. '
          'E2: lags [1, 2, 3, 6, 12, 24, 48, 168] horas. '
          'E3: lags [1, 2, 3, 7, 14, 30] días.')

p = doc.add_paragraph(style='List Bullet')
p.add_run('Rolling windows de GAP: ').bold = True
p.add_run('media y desviación estándar móvil con shift(1) para evitar data leakage. '
          'E1: ventanas [4, 8, 96]. E2: [6, 24, 168]. E3: [7, 14, 30].')

p = doc.add_paragraph(style='List Bullet')
p.add_run('Variables del dataset resampleado: ').bold = True
p.add_run('GRP, VOLT, SM1, SM2, SM3 (promedios por período).')

body(doc,
    'El total de features varía por escenario: 21 para E1, 23 para E2 y 22 para E3.')

heading(doc, '5.3 División train/test cronológica', 2)
body(doc,
    'El conjunto de datos se dividió en 80% entrenamiento y 20% prueba siguiendo '
    'el orden cronológico estricto, sin mezcla aleatoria. Esta estrategia respeta '
    'la naturaleza temporal de los datos y simula el escenario real de predicción, '
    'donde el modelo sólo puede entrenarse con datos pasados.')

t_split = doc.add_table(rows=4, cols=5)
t_split.style = 'Table Grid'
t_split.alignment = WD_TABLE_ALIGNMENT.CENTER
split_headers = ['Escenario', 'Train (80%)', 'Test (20%)', 'Inicio test', 'Fin test']
for j, h in enumerate(split_headers):
    cell = t_split.rows[0].cells[j]
    cell.text = h
    cell.paragraphs[0].runs[0].font.bold = True
    cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    set_cell_bg(cell, '4A148C')
split_rows = [
    ('15 minutos', '106,714', '26,679', 'Apr 2009', 'Nov 2010'),
    ('1 hora',     '27,071',  '6,768',  'Apr 2009', 'Nov 2010'),
    ('1 día',      '1,122',   '281',    'Apr 2009', 'Nov 2010'),
]
for i, row_vals in enumerate(split_rows):
    bg = 'F3E5F5' if i % 2 == 0 else 'FFFFFF'
    for j, val in enumerate(row_vals):
        cell = t_split.rows[i+1].cells[j]
        cell.text = val
        cell.paragraphs[0].runs[0].font.size = Pt(10)
        set_cell_bg(cell, bg)
c = doc.add_paragraph('Tabla 4. División cronológica train/test por escenario.')
c.alignment = WD_ALIGN_PARAGRAPH.CENTER
c.runs[0].font.size = Pt(9); c.runs[0].font.italic = True

doc.add_page_break()

# =============================================================================
# MODELOS ML
# =============================================================================

heading(doc, '6. Modelos de Machine Learning', 1)
add_hr(doc)

body(doc,
    'Se implementaron tres algoritmos de machine learning supervisado para regresión, '
    'evaluados con las mismas métricas y bajo el mismo protocolo de validación en '
    'cada escenario.')

heading(doc, '6.1 Random Forest', 2)
body(doc,
    'Random Forest es un método de ensamble basado en árboles de decisión. Construye '
    'múltiples árboles sobre submuestras aleatorias del dataset (bagging) y promedia '
    'sus predicciones. Su fortaleza principal es la capacidad para capturar relaciones '
    'no lineales y su robustez ante outliers. No requiere escalado de features.')
p = doc.add_paragraph()
p.add_run('Parámetros base: ').bold = True
p.add_run('n_estimators=200, max_depth=20 (E1/E2) / 15 (E3), '
          'min_samples_leaf=5 (E1/E2) / 3 (E3), random_state=42, n_jobs=−1.')

heading(doc, '6.2 XGBoost', 2)
body(doc,
    'XGBoost (eXtreme Gradient Boosting) es un algoritmo de boosting que construye '
    'árboles de forma secuencial, donde cada árbol corrige los errores del anterior. '
    'Incorpora regularización L1/L2 y es especialmente eficiente gracias a su '
    'implementación con tree_method="hist". Suele ser el modelo con mejor rendimiento '
    'en datos tabulares estructurados.')
p = doc.add_paragraph()
p.add_run('Parámetros base: ').bold = True
p.add_run('n_estimators=200, max_depth=6 (E1/E2) / 4 (E3), learning_rate=0.05, '
          'subsample=0.8, colsample_bytree=0.8, tree_method="hist", random_state=42.')

heading(doc, '6.3 Support Vector Regression (SVR)', 2)
body(doc,
    'SVR busca el hiperplano de regresión que minimiza el error dentro de un margen ε, '
    'usando un kernel RBF (Radial Basis Function) para mapear los datos a un espacio '
    'de mayor dimensión. Requiere escalado previo de features y target. Por su alto '
    'costo computacional (O(n²) a O(n³)), se limitó el conjunto de entrenamiento a '
    '15,000 muestras (E1) y 10,000 (E2), usando las más recientes por ser más '
    'representativas del comportamiento actual.')
p = doc.add_paragraph()
p.add_run('Parámetros base: ').bold = True
p.add_run('kernel="rbf", C=10.0, epsilon=0.05, gamma="scale".')
p = doc.add_paragraph()
p.add_run('Escalado: ').bold = True
p.add_run('StandardScaler aplicado a X e y por separado; las predicciones se '
          'invierten con inverse_transform antes de calcular métricas.')

heading(doc, '6.4 Métricas de evaluación', 2)
body(doc, 'Se emplearon cuatro métricas calculadas sobre el conjunto de prueba:')
metrics_desc = [
    ('RMSE', 'Root Mean Squared Error', 'Penaliza errores grandes. Mismas unidades que GAP (kW).'),
    ('MAE',  'Mean Absolute Error',     'Error promedio absoluto. Más robusto ante outliers que RMSE.'),
    ('MAPE', 'Mean Absolute Percentage Error', 'Error relativo en porcentaje. Calculado sólo sobre valores GAP > 0.01 kW.'),
    ('R²',   'Coeficiente de determinación', 'Proporción de varianza explicada. Rango [0, 1]; mayor es mejor.'),
]
t_met = doc.add_table(rows=5, cols=3)
t_met.style = 'Table Grid'
t_met.alignment = WD_TABLE_ALIGNMENT.CENTER
for j, h in enumerate(['Sigla', 'Nombre completo', 'Interpretación']):
    cell = t_met.rows[0].cells[j]
    cell.text = h
    cell.paragraphs[0].runs[0].font.bold = True
    cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    set_cell_bg(cell, 'B71C1C')
for i, (sigla, nombre, desc) in enumerate(metrics_desc):
    bg = 'FFF3E0' if i % 2 == 0 else 'FFFFFF'
    for j, val in enumerate([sigla, nombre, desc]):
        cell = t_met.rows[i+1].cells[j]
        cell.text = val
        cell.paragraphs[0].runs[0].font.size = Pt(10)
        if j == 0: cell.paragraphs[0].runs[0].font.bold = True
        set_cell_bg(cell, bg)
c = doc.add_paragraph('Tabla 5. Métricas de evaluación utilizadas.')
c.alignment = WD_ALIGN_PARAGRAPH.CENTER
c.runs[0].font.size = Pt(9); c.runs[0].font.italic = True

doc.add_page_break()

# =============================================================================
# RESULTADOS POR ESCENARIO
# =============================================================================

heading(doc, '7. Resultados por Escenario', 1)
add_hr(doc)

body(doc,
    'A continuación se presentan los resultados obtenidos con los parámetros base '
    '(antes del tuning) y tuned (tras GridSearchCV) para cada escenario, junto '
    'con las visualizaciones de predicciones y scatter plots.')

# ── Escenario 1 ──────────────────────────────────────────────────────────────
heading(doc, '7.1 Escenario 1 — 15 Minutos', 2)
body(doc,
    'Resolución de 15 minutos. Es el escenario de mayor granularidad y presenta '
    'los datasets más grandes: 106,714 registros para entrenamiento y 26,679 para '
    'prueba. Los lags incluyen hasta 96 períodos (equivalente a 24 horas hacia atrás) '
    'para capturar la estacionalidad diaria.')

add_image_safe(doc,
    os.path.join(GRAF_E1, 'e1_01_serie_resampleada.png'),
    caption='Figura 8. Serie GAP resampleada a 15 minutos con corte train/test.')
add_image_safe(doc,
    os.path.join(GRAF_E1, 'e1_02_predicciones.png'),
    caption='Figura 9. Predicciones vs valores reales — primeros 500 puntos del test (15 min).')
add_image_safe(doc,
    os.path.join(GRAF_E1, 'e1_03_scatter.png'),
    caption='Figura 10. Scatter plot predicho vs real — Escenario 15 minutos.')

heading(doc, 'Métricas — Escenario 15 minutos (parámetros base)', 3)
metrics_table(doc, df_base, '15 Minutos',
              'Tabla 6. Métricas con parámetros base — Escenario 15 minutos.')

heading(doc, 'Métricas — Escenario 15 minutos (tuned)', 3)
metrics_table(doc, df_tuned, '15 Minutos',
              'Tabla 7. Métricas con parámetros tuned — Escenario 15 minutos.')

add_image_safe(doc,
    os.path.join(GRAF_E1, 'e1_05_importancia.png'),
    caption='Figura 11. Importancia de features — RF y XGBoost (Escenario 15 min).')

# ── Escenario 2 ──────────────────────────────────────────────────────────────
doc.add_page_break()
heading(doc, '7.2 Escenario 2 — 1 Hora', 2)
body(doc,
    'Resolución de 1 hora. El conjunto de entrenamiento contiene 27,071 registros '
    'y el de prueba 6,768. Los lags incluyen hasta 168 horas (1 semana) para '
    'capturar la estacionalidad semanal.')

add_image_safe(doc,
    os.path.join(GRAF_E2, 'e2_02_predicciones.png'),
    caption='Figura 12. Predicciones vs valores reales — primeros 500 puntos del test (1 hora).')
add_image_safe(doc,
    os.path.join(GRAF_E2, 'e2_03_scatter.png'),
    caption='Figura 13. Scatter plot predicho vs real — Escenario 1 hora.')

heading(doc, 'Métricas — Escenario 1 hora (parámetros base)', 3)
metrics_table(doc, df_base, '1 Hora',
              'Tabla 8. Métricas con parámetros base — Escenario 1 hora.')
heading(doc, 'Métricas — Escenario 1 hora (tuned)', 3)
metrics_table(doc, df_tuned, '1 Hora',
              'Tabla 9. Métricas con parámetros tuned — Escenario 1 hora.')

add_image_safe(doc,
    os.path.join(GRAF_E2, 'e2_05_importancia.png'),
    caption='Figura 14. Importancia de features — RF y XGBoost (Escenario 1 hora).')

# ── Escenario 3 ──────────────────────────────────────────────────────────────
doc.add_page_break()
heading(doc, '7.3 Escenario 3 — 1 Día', 2)
body(doc,
    'Resolución diaria. Es el dataset más pequeño: 1,122 registros para '
    'entrenamiento y 281 para prueba. Los lags incluyen hasta 30 días para '
    'capturar tendencias mensuales. Al ser un dataset pequeño, SVR no requiere '
    'submuestreo y es entrenado sobre todos los datos disponibles.')

add_image_safe(doc,
    os.path.join(GRAF_E3, 'e3_02_predicciones.png'),
    caption='Figura 15. Predicciones vs valores reales — conjunto de prueba completo (1 día).')
add_image_safe(doc,
    os.path.join(GRAF_E3, 'e3_03_scatter.png'),
    caption='Figura 16. Scatter plot predicho vs real — Escenario 1 día.')

heading(doc, 'Métricas — Escenario 1 día (parámetros base)', 3)
metrics_table(doc, df_base, '1 Día',
              'Tabla 10. Métricas con parámetros base — Escenario 1 día.')
heading(doc, 'Métricas — Escenario 1 día (tuned)', 3)
metrics_table(doc, df_tuned, '1 Día',
              'Tabla 11. Métricas con parámetros tuned — Escenario 1 día.')

add_image_safe(doc,
    os.path.join(GRAF_E3, 'e3_05_importancia.png'),
    caption='Figura 17. Importancia de features — RF y XGBoost (Escenario 1 día).')

doc.add_page_break()

# =============================================================================
# TUNING
# =============================================================================

heading(doc, '8. Optimización de Hiperparámetros (GridSearchCV)', 1)
add_hr(doc)

heading(doc, '8.1 Metodología', 2)
body(doc,
    'Se implementó una búsqueda exhaustiva de hiperparámetros mediante GridSearchCV '
    'de scikit-learn, con validación cruzada temporal usando TimeSeriesSplit '
    '(n_splits=3) y scoring=R². TimeSeriesSplit garantiza que en cada fold '
    'el conjunto de validación siempre sea posterior al de entrenamiento, '
    'preservando la integridad temporal del experimento.')

body(doc,
    'Para los escenarios con datasets grandes (E1 y E2), la búsqueda de CV se '
    'realizó sobre las últimas 30,000 muestras del train (E1) o sobre el train '
    'completo (E2). En todos los casos, el modelo final se reentrenó con los '
    'mejores parámetros sobre el conjunto de entrenamiento completo.')

heading(doc, '8.2 Grids de búsqueda', 2)

t_grids = doc.add_table(rows=4, cols=3)
t_grids.style = 'Table Grid'
t_grids.alignment = WD_TABLE_ALIGNMENT.CENTER
for j, h in enumerate(['Modelo', 'Hiperparámetros', 'Valores explorados']):
    cell = t_grids.rows[0].cells[j]
    cell.text = h
    cell.paragraphs[0].runs[0].font.bold = True
    cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    set_cell_bg(cell, '4E342E')
grid_data = [
    ('Random Forest', 'n_estimators\nmax_depth\nmin_samples_leaf',
     '[100, 200, 300]\n[10, 20, None]\n[1, 5, 10]\n→ 27 combinaciones'),
    ('XGBoost', 'n_estimators\nmax_depth\nlearning_rate\nsubsample',
     '[100, 200]\n[4, 6, 8]\n[0.05, 0.1]\n[0.8, 1.0]\n→ 24 combinaciones'),
    ('SVR', 'C\nepsilon\ngamma',
     '[1, 10, 100]\n[0.01, 0.05, 0.1]\n["scale", 0.01]\n→ 18 combinaciones'),
]
for i, (mod, params, vals) in enumerate(grid_data):
    bg = 'EFEBE9' if i % 2 == 0 else 'FFFFFF'
    for j, val in enumerate([mod, params, vals]):
        cell = t_grids.rows[i+1].cells[j]
        cell.text = val
        cell.paragraphs[0].runs[0].font.size = Pt(9.5)
        if j == 0: cell.paragraphs[0].runs[0].font.bold = True
        set_cell_bg(cell, bg)
c = doc.add_paragraph('Tabla 12. Grids de hiperparámetros explorados por modelo.')
c.alignment = WD_ALIGN_PARAGRAPH.CENTER
c.runs[0].font.size = Pt(9); c.runs[0].font.italic = True

heading(doc, '8.3 Mejores parámetros encontrados', 2)

t_best = doc.add_table(rows=10, cols=4)
t_best.style = 'Table Grid'
t_best.alignment = WD_TABLE_ALIGNMENT.CENTER
for j, h in enumerate(['Escenario', 'Modelo', 'CV R²', 'Mejores parámetros']):
    cell = t_best.rows[0].cells[j]
    cell.text = h
    cell.paragraphs[0].runs[0].font.bold = True
    cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    set_cell_bg(cell, '1A237E')

best_params_data = [
    ('15 min', 'Random Forest', '0.8772', 'max_depth=None, min_samples_leaf=5, n_estimators=200'),
    ('15 min', 'XGBoost',       '0.8776', 'learning_rate=0.05, max_depth=6, n_estimators=100, subsample=1.0'),
    ('15 min', 'SVR',           '0.8166', 'C=1, epsilon=0.05, gamma=scale'),
    ('1 hora', 'Random Forest', '0.8465', 'max_depth=20, min_samples_leaf=1, n_estimators=300'),
    ('1 hora', 'XGBoost',       '0.8671', 'learning_rate=0.05, max_depth=6, n_estimators=200, subsample=0.8'),
    ('1 hora', 'SVR',           '0.8244', 'C=1, epsilon=0.05, gamma=0.01'),
    ('1 día',  'Random Forest', '0.7233', 'max_depth=20, min_samples_leaf=5, n_estimators=200'),
    ('1 día',  'XGBoost',       '0.7226', 'learning_rate=0.05, max_depth=4, n_estimators=100, subsample=0.8'),
    ('1 día',  'SVR',           '0.7691', 'C=1, epsilon=0.05, gamma=0.01'),
]
model_colors_hex = {'Random Forest': 'E3F2FD', 'XGBoost': 'E8F5E9', 'SVR': 'FFEBEE'}
for i, row_vals in enumerate(best_params_data):
    bg = model_colors_hex.get(row_vals[1], 'FFFFFF')
    for j, val in enumerate(row_vals):
        cell = t_best.rows[i+1].cells[j]
        cell.text = val
        cell.paragraphs[0].runs[0].font.size = Pt(9.5)
        set_cell_bg(cell, bg)
c = doc.add_paragraph('Tabla 13. Mejores hiperparámetros encontrados por GridSearchCV.')
c.alignment = WD_ALIGN_PARAGRAPH.CENTER
c.runs[0].font.size = Pt(9); c.runs[0].font.italic = True

heading(doc, '8.4 Impacto del tuning', 2)
body(doc,
    'La siguiente tabla muestra la variación neta en R² y RMSE tras el tuning '
    'respecto a los parámetros base:')

t_delta = doc.add_table(rows=10, cols=5)
t_delta.style = 'Table Grid'
t_delta.alignment = WD_TABLE_ALIGNMENT.CENTER
for j, h in enumerate(['Escenario', 'Modelo', 'R² Base', 'R² Tuned', 'ΔR²']):
    cell = t_delta.rows[0].cells[j]
    cell.text = h
    cell.paragraphs[0].runs[0].font.bold = True
    cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    set_cell_bg(cell, '37474F')

delta_data = [
    ('15 min', 'Random Forest', '0.9144', '0.9145', '+0.0001'),
    ('15 min', 'XGBoost',       '0.9198', '0.9131', '−0.0067'),
    ('15 min', 'SVR',           '0.8589', '0.8801', '+0.0212'),
    ('1 hora', 'Random Forest', '0.8751', '0.8754', '+0.0003'),
    ('1 hora', 'XGBoost',       '0.8812', '0.8812', '+0.0000'),
    ('1 hora', 'SVR',           '0.8415', '0.8580', '+0.0165'),
    ('1 día',  'Random Forest', '0.7313', '0.7276', '−0.0037'),
    ('1 día',  'XGBoost',       '0.7776', '0.7748', '−0.0028'),
    ('1 día',  'SVR',           '0.7374', '0.7848', '+0.0474'),
]
for i, row_vals in enumerate(delta_data):
    bg = model_colors_hex.get(row_vals[1], 'FFFFFF')
    for j, val in enumerate(row_vals):
        cell = t_delta.rows[i+1].cells[j]
        cell.text = val
        run = cell.paragraphs[0].runs[0]
        run.font.size = Pt(9.5)
        if j == 4:
            if val.startswith('+') and val != '+0.0000':
                run.font.color.rgb = RGBColor(0x1B, 0x5E, 0x20)
                run.font.bold = True
            elif val.startswith('−'):
                run.font.color.rgb = RGBColor(0xB7, 0x1C, 0x1C)
        set_cell_bg(cell, bg)
c = doc.add_paragraph('Tabla 14. Variación de R² tras el tuning (verde = mejora, rojo = ligera caída).')
c.alignment = WD_ALIGN_PARAGRAPH.CENTER
c.runs[0].font.size = Pt(9); c.runs[0].font.italic = True

add_image_safe(doc,
    os.path.join(GRAF_TUN, 'comparacion_r2.png'),
    caption='Figura 18. R² Base vs Tuned por escenario y modelo.')
add_image_safe(doc,
    os.path.join(GRAF_TUN, 'mejora_delta_r2.png'),
    caption='Figura 19. Mejora neta de R² tras GridSearchCV (ΔR² = Tuned − Base).')

doc.add_page_break()

# =============================================================================
# ANÁLISIS COMPARATIVO
# =============================================================================

heading(doc, '9. Análisis Comparativo', 1)
add_hr(doc)

body(doc,
    'Esta sección presenta una visión unificada del desempeño de todos los '
    'modelos a través de los tres escenarios, utilizando los resultados con '
    'parámetros tuned.')

heading(doc, '9.1 Heatmap de métricas', 2)
body(doc,
    'El mapa de calor permite identificar de un vistazo los modelos y escenarios '
    'con mejor desempeño. Colores más intensos en R² indican mejor predicción; '
    'en RMSE, MAE y MAPE indican mayor error.')
add_image_safe(doc,
    os.path.join(GRAF_CMP, '02_heatmap_metricas.png'),
    caption='Figura 20. Heatmap de las cuatro métricas — modelos × escenarios (tuned).')

heading(doc, '9.2 Comparación completa de métricas', 2)
add_image_safe(doc,
    os.path.join(GRAF_CMP, '01_metricas_tuned_barras.png'),
    caption='Figura 21. Comparación de R², RMSE, MAE y MAPE por escenario y modelo.')

heading(doc, '9.3 Evolución del R² a través de escenarios', 2)
body(doc,
    'El gráfico de evolución muestra cómo varía el R² de cada modelo al aumentar '
    'el horizonte temporal de predicción. En general, predecir a mayor horizonte '
    '(1 día) resulta más difícil que a corto plazo (15 min), lo cual se refleja '
    'en la caída de R² en todos los modelos.')
add_image_safe(doc,
    os.path.join(GRAF_CMP, '06_evolucion_r2.png'),
    caption='Figura 22. Evolución del R² por escenario — Base vs Tuned.')

heading(doc, '9.4 Perfil multidimensional (Radar)', 2)
body(doc,
    'Los radar charts muestran el perfil normalizado de cada modelo en las '
    'cuatro métricas. Un modelo ideal ocuparía toda el área del radar. '
    'Los valores están normalizados entre 0 y 1 dentro de cada escenario '
    '(1 = mejor desempeño relativo).')
add_image_safe(doc,
    os.path.join(GRAF_CMP, '04_radar_modelos.png'),
    caption='Figura 23. Perfil multidimensional normalizado por escenario.')

heading(doc, '9.5 Resumen — mejor modelo por escenario', 2)
add_image_safe(doc,
    os.path.join(GRAF_CMP, '05_tabla_mejor_modelo.png'),
    width=Inches(5.5),
    caption='Figura 24. Tabla resumen del mejor modelo por escenario (parámetros tuned).')

doc.add_page_break()

# =============================================================================
# CONCLUSIONES
# =============================================================================

heading(doc, '10. Conclusiones', 1)
add_hr(doc)

heading(doc, '10.1 Resultados principales', 2)
concls = [
    ('Escenario 15 minutos (corto plazo):',
     'Random Forest logra el mejor R² tuned (0.9145), seguido muy de cerca por '
     'XGBoost (0.9131). Ambos modelos basados en árboles muestran rendimiento '
     'superior en este escenario de alta resolución. MAPE ≈ 14.8%, lo que indica '
     'un error relativo bajo para predicción intradía.'),
    ('Escenario 1 hora (mediano plazo):',
     'XGBoost mantiene el primer lugar con R²=0.8812, con los mismos parámetros '
     'que los de base, lo que demuestra que el tuning confirmó que la '
     'configuración inicial ya era óptima. MAPE ≈ 17.0%.'),
    ('Escenario 1 día (largo plazo):',
     'SVR emerge como el mejor modelo tras tuning con R²=0.7848 y MAPE=9.66%, '
     'mostrando la mayor mejora absoluta por el tuning (ΔR²=+0.0474). '
     'A resolución diaria, el SVR captura mejor la tendencia de largo plazo '
     'que los modelos de árboles.'),
]
for titulo, texto in concls:
    p = doc.add_paragraph()
    p.add_run(titulo + ' ').bold = True
    p.add_run(texto)
    p.paragraph_format.space_after = Pt(6)

heading(doc, '10.2 Hallazgos del tuning', 2)
hallazgos = [
    'SVR se beneficia significativamente del tuning en todos los escenarios, con mejoras de hasta +0.0474 en R² (E3).',
    'Random Forest y XGBoost ya estaban bien calibrados con los parámetros base; el GridSearchCV confirmó que estaban cerca del óptimo.',
    'Para los escenarios de mayor resolución (15 min, 1 hora), el impacto del tuning en RF y XGBoost es marginal, mientras que SVR mejora notablemente.',
    'El uso de TimeSeriesSplit en lugar de KFold estándar garantiza que la validación cruzada respete la naturaleza temporal de los datos.',
]
for h in hallazgos:
    p = doc.add_paragraph(h, style='List Bullet')
    p.paragraph_format.space_after = Pt(4)

heading(doc, '10.3 Limitaciones', 2)
lims = [
    'La variable SM1 (sub-medidor de cocina) quedó en cero en el dataset limpio por efecto del filtro IQR en distribuciones esparsas. Esto limita la información disponible sobre el consumo de cocina.',
    'SVR fue entrenado sobre submuestras por restricciones computacionales. Con el dataset completo podría obtener resultados aún mejores.',
    'Los resultados son específicos del hogar y período estudiados. La generalización a otros contextos requiere validación adicional.',
    'El R² del escenario diario (0.78 máximo) sugiere que la resolución diaria pierde información intradiaria relevante para la predicción.',
]
for lim in lims:
    p = doc.add_paragraph(lim, style='List Bullet')
    p.paragraph_format.space_after = Pt(4)

heading(doc, '10.4 Trabajo futuro', 2)
futuros = [
    'Implementar modelos de deep learning (LSTM, Transformer) para comparar con los modelos clásicos.',
    'Explorar RandomizedSearchCV o Optuna (Bayesian optimization) para espacios de búsqueda más amplios.',
    'Revisar la estrategia de limpieza de SM1 para preservar el sub-medidor de cocina.',
    'Incorporar variables exógenas (temperatura, calendario de festivos) para mejorar la predicción en el escenario diario.',
]
for fut in futuros:
    p = doc.add_paragraph(fut, style='List Bullet')
    p.paragraph_format.space_after = Pt(4)

doc.add_page_break()

# =============================================================================
# APÉNDICE — ESTRUCTURA DEL PROYECTO
# =============================================================================

heading(doc, 'Apéndice — Estructura del proyecto', 1)
add_hr(doc)

body(doc, 'Árbol de directorios del proyecto:')
code = doc.add_paragraph()
code.paragraph_format.left_indent = Cm(1.0)
run = code.add_run(
    'Tesis_ML_Energia/\n'
    '  codigo/\n'
    '    EDA.py                    ← Análisis exploratorio completo\n'
    '    escenario1_15min.py       ← Modelo base E1 (15 min)\n'
    '    escenario2_1hora.py       ← Modelo base E2 (1 hora)\n'
    '    escenario3_1dia.py        ← Modelo base E3 (1 día)\n'
    '    tuning_gridsearch.py      ← GridSearchCV (3 escenarios × 3 modelos)\n'
    '    graficos_comparativos.py  ← Gráficos unificados\n'
    '    generar_informe.py        ← Este script (genera el informe Word)\n'
    '  datos/\n'
    '    household_power_consumption.txt  ← Dataset original UCI\n'
    '    dataset_limpio.csv               ← Dataset limpio (1,739,167 registros)\n'
    '  graficos/\n'
    '    eda/           ← 13 gráficos del EDA\n'
    '    escenario1/    ← 5 gráficos (15 min)\n'
    '    escenario2/    ← 5 gráficos (1 hora)\n'
    '    escenario3/    ← 5 gráficos (1 día)\n'
    '    tuning/        ← 4 gráficos del tuning\n'
    '    comparativos/  ← 6 gráficos comparativos\n'
    '  modelos/\n'
    '    tuning_resultados.csv   ← Métricas Base y Tuned (todos los modelos)\n'
    '  Informe_Tesis_ML_Energia.docx  ← Este informe'
)
run.font.name = 'Courier New'
run.font.size = Pt(9)
run.font.color.rgb = RGBColor(0x1A, 0x23, 0x7E)

# =============================================================================
# GUARDAR
# =============================================================================

doc.save(OUT_FILE)
print(f"\n✓ Informe generado exitosamente:")
print(f"  {OUT_FILE}")
print(f"\n  Secciones incluidas:")
print(f"    1. Resumen ejecutivo")
print(f"    2. Introducción y contexto")
print(f"    3. Dataset (tablas de variables y estadísticas)")
print(f"    4. EDA (7 gráficos embebidos)")
print(f"    5. Preparación de datos (resample, feature engineering, split)")
print(f"    6. Modelos ML (RF, XGBoost, SVR + métricas)")
print(f"    7. Resultados por escenario (tablas + gráficos)")
print(f"    8. Tuning GridSearchCV (grids, mejores params, impacto)")
print(f"    9. Análisis comparativo (heatmap, radar, evolución R²)")
print(f"   10. Conclusiones y trabajo futuro")
print(f"    A. Apéndice — estructura del proyecto")
