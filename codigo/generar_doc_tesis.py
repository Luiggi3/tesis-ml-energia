# =============================================================================
# GENERADOR DE DOCUMENTO WORD — DOCUMENTACIÓN DE LA TESIS
# Contenido: Preparación de datos, Horizontes, Feature Engineering, Modelos
# =============================================================================

import os
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

_here    = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = _here if os.path.exists(os.path.join(_here, 'datos')) else os.path.dirname(_here)
OUT_PATH = os.path.join(BASE_DIR, 'Documentacion_Tesis.docx')
GRAF_DIR = os.path.join(BASE_DIR, 'graficos')

doc = Document()

# ── Márgenes ──────────────────────────────────────────────────────────────────
for section in doc.sections:
    section.top_margin    = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin   = Cm(3.0)
    section.right_margin  = Cm(2.5)

doc.styles['Normal'].font.name = 'Times New Roman'
doc.styles['Normal'].font.size = Pt(12)

# ── Helpers ───────────────────────────────────────────────────────────────────
def heading(text, level=1):
    p = doc.add_heading(level=level)
    p.clear()
    r = p.add_run(text)
    r.font.name  = 'Times New Roman'
    r.font.bold  = True
    r.font.color.rgb = RGBColor(0, 0, 0)
    r.font.size  = Pt(16) if level == 1 else Pt(13) if level == 2 else Pt(12)
    p.alignment  = WD_ALIGN_PARAGRAPH.LEFT

def para(text, justify=True, space_after=True):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY if justify else WD_ALIGN_PARAGRAPH.LEFT
    if space_after:
        p.paragraph_format.space_after = Pt(8)
    return p

def add_figure(img_path, caption_num, caption_text, intro_text=None, width=Inches(5.5)):
    if not os.path.exists(img_path):
        print(f'  ⚠ No encontrado: {img_path}')
        return
    if intro_text:
        p = doc.add_paragraph()
        r = p.add_run(intro_text)
        r.font.name = 'Times New Roman'; r.font.size = Pt(12); r.italic = True
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.add_run().add_picture(img_path, width=width)
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cap = p_cap.add_run(f'Figura {caption_num}. {caption_text}')
    r_cap.font.name = 'Times New Roman'; r_cap.font.size = Pt(10); r_cap.italic = True
    doc.add_paragraph()
    print(f'  ✓ Figura {caption_num} agregada')

fig_num = 1

def table_row(table, col1, col2, bold_col1=False):
    row  = table.add_row()
    c1   = row.cells[0].paragraphs[0].add_run(col1)
    c2   = row.cells[1].paragraphs[0].add_run(col2)
    c1.font.name = c2.font.name = 'Times New Roman'
    c1.font.size = c2.font.size = Pt(11)
    c1.bold = bold_col1

def table_row3(table, c1t, c2t, c3t, bold=False):
    row = table.add_row()
    for cell, text in zip(row.cells, [c1t, c2t, c3t]):
        r = cell.paragraphs[0].add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11)
        r.bold = bold

def table_row5(table, vals, bold=False):
    row = table.add_row()
    for cell, text in zip(row.cells, vals):
        r = cell.paragraphs[0].add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11)
        r.bold = bold

# =============================================================================
# PORTADA
# =============================================================================
for _ in range(4):
    doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('DOCUMENTACIÓN DE LA TESIS')
r.font.name = 'Times New Roman'; r.font.size = Pt(20); r.bold = True

doc.add_paragraph()
p2 = doc.add_paragraph()
p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
r2 = p2.add_run('Modelo Predictivo del Consumo Energético en Hogares Inteligentes\nUtilizando Algoritmos de Machine Learning')
r2.font.name = 'Times New Roman'; r2.font.size = Pt(14)

doc.add_page_break()

# =============================================================================
# 1. PREPARACIÓN DE DATOS
# =============================================================================
heading('1. Preparación de Datos', level=1)

para(
    'El proceso de preparación de datos constituye la primera etapa del desarrollo '
    'de los modelos predictivos. A partir del dataset original de consumo eléctrico '
    '(UCI, Francia 2006–2010) con 2.075.259 registros a frecuencia de un minuto, '
    'se realizaron las siguientes etapas: eliminación de valores nulos, detección y '
    'remoción de valores atípicos mediante el método IQR, y exportación del dataset '
    'limpio con 1.739.167 registros.'
)

para(
    'Para adaptar los datos a cada horizonte de predicción, se aplicó un proceso de '
    'remuestreo (resample) calculando el promedio de los valores dentro de cada '
    'intervalo de tiempo. Este procedimiento reduce la resolución temporal pero '
    'elimina el ruido de corto plazo y hace manejable el volumen de datos para '
    'el entrenamiento.'
)

# Variables del dataset
heading('1.1 Variables del Dataset', level=2)

para('El dataset limpio contiene las siguientes variables eléctricas:')

t = doc.add_table(rows=1, cols=3)
t.style = 'Table Grid'
for cell, text in zip(t.rows[0].cells, ['Variable', 'Unidad', 'Descripción']):
    r = cell.paragraphs[0].add_run(text)
    r.font.name = 'Times New Roman'; r.font.size = Pt(11); r.bold = True

for row_data in [
    ('GAP',  'kW',  'Potencia activa global — variable objetivo a predecir'),
    ('GRP',  'kW',  'Potencia reactiva global'),
    ('VOLT', 'V',   'Voltaje de red'),
    ('GI',   'A',   'Intensidad global de corriente'),
    ('SM1',  'Wh',  'Sub-medidor 1 — Cocina'),
    ('SM2',  'Wh',  'Sub-medidor 2 — Lavandería'),
    ('SM3',  'Wh',  'Sub-medidor 3 — Calentador / Aire acondicionado'),
]:
    table_row3(t, *row_data)

doc.add_paragraph()

# Remuestreo por escenario
heading('1.2 Remuestreo por Escenario', level=2)

para(
    'Cada escenario parte del mismo dataset limpio a 1 minuto y lo agrega a una '
    'frecuencia diferente mediante promedio. La siguiente tabla resume el resultado '
    'del proceso de remuestreo:'
)

t2 = doc.add_table(rows=1, cols=4)
t2.style = 'Table Grid'
for cell, text in zip(t2.rows[0].cells, ['Escenario', 'Frecuencia', 'Registros resultantes', 'Observaciones por día']):
    r = cell.paragraphs[0].add_run(text)
    r.font.name = 'Times New Roman'; r.font.size = Pt(11); r.bold = True

for row_data in [
    ('Escenario 1', '15 minutos', '133.489', '96'),
    ('Escenario 2', '1 hora',     '34.007',  '24'),
    ('Escenario 3', '1 día',      '1.433',   '1'),
]:
    table_row5(t2, row_data)

doc.add_paragraph()

para(
    'En todos los escenarios, la división del conjunto de datos se realizó de forma '
    'cronológica: 80% para entrenamiento y 20% para prueba, respetando el orden '
    'temporal de las observaciones para evitar fuga de información futura (data leakage). '
    'La siguiente tabla muestra el desglose exacto por escenario:'
)

t_split = doc.add_table(rows=1, cols=4)
t_split.style = 'Table Grid'
for cell, text in zip(t_split.rows[0].cells, ['Escenario', 'Total registros', 'Entrenamiento (80%)', 'Prueba (20%)']):
    r = cell.paragraphs[0].add_run(text)
    r.font.name = 'Times New Roman'; r.font.size = Pt(11); r.bold = True

for row_data in [
    ('15 minutos', '133.489', '106.791', '26.698'),
    ('1 hora',     '34.007',  '27.205',  '6.802'),
    ('1 día',      '1.433',   '1.146',   '287'),
]:
    table_row5(t_split, row_data)

doc.add_paragraph()

# Preparación específica por escenario
heading('1.3 Preparación Específica por Escenario', level=2)

heading('Escenario 1 — 15 Minutos', level=3)
para(
    'El dataset fue remuestreado a intervalos de 15 minutos, resultando en 133.489 '
    'observaciones para el período completo 2006–2010. De estas, 106.791 corresponden '
    'al conjunto de entrenamiento y 26.698 al conjunto de prueba. Este escenario genera '
    'la mayor cantidad de datos, lo que favorece el aprendizaje de los modelos. '
    'La variable GI (intensidad global) fue eliminada por presentar una correlación de '
    '0.999 con GAP, siendo redundante y fuente de multicolinealidad. Se utilizan las '
    '6 variables eléctricas restantes como predictores base.'
)
add_figure(
    os.path.join(GRAF_DIR, 'escenario1', 'e1_01_serie_resampleada.png'),
    fig_num,
    'Serie temporal de GAP remuestreada a 15 minutos. En azul se muestra el conjunto '
    'de entrenamiento (80%) y en naranja el conjunto de prueba (20%). La línea vertical '
    'indica el corte cronológico entre ambos conjuntos.',
    intro_text='La siguiente figura muestra la serie de consumo (GAP) tras el remuestreo a 15 minutos:'
)
fig_num += 1

heading('Escenario 2 — 1 Hora', level=3)
para(
    'El dataset fue remuestreado a intervalos de una hora, resultando en 34.007 '
    'observaciones para el período completo 2006–2010. De estas, 27.205 corresponden '
    'al conjunto de entrenamiento y 6.802 al conjunto de prueba. Cada observación '
    'captura el promedio de 60 lecturas, lo que reduce las fluctuaciones momentáneas '
    'y produce una serie más estable. Al igual que en el escenario anterior, la '
    'variable GI fue eliminada por multicolinealidad (correlación 0.999 con GAP). '
    'Se utilizan las 6 variables eléctricas restantes como predictores base.'
)
add_figure(
    os.path.join(GRAF_DIR, 'escenario2', 'e2_01_serie_resampleada.png'),
    fig_num,
    'Serie temporal de GAP remuestreada a 1 hora. En azul se muestra el conjunto '
    'de entrenamiento (80%) y en naranja el conjunto de prueba (20%).',
    intro_text='La siguiente figura muestra la serie de consumo (GAP) tras el remuestreo a 1 hora:'
)
fig_num += 1

heading('Escenario 3 — 1 Día', level=3)
para(
    'El dataset fue remuestreado a nivel diario, resultando en 1.433 observaciones '
    'para el período completo 2006–2010. De estas, 1.146 corresponden al conjunto '
    'de entrenamiento y 287 al conjunto de prueba. Es el escenario con menor volumen '
    'de datos. Adicionalmente, se eliminó la variable GI (intensidad global) por '
    'presentar una correlación de 0.999 con GAP, lo que la hace redundante y puede '
    'generar problemas de multicolinealidad.'
)
add_figure(
    os.path.join(GRAF_DIR, 'escenario3', 'e3_01_serie_resampleada.png'),
    fig_num,
    'Serie temporal de GAP remuestreada a 1 día. En azul se muestra el conjunto '
    'de entrenamiento (80%) y en naranja el conjunto de prueba (20%). '
    'Se aprecia claramente el patrón estacional anual del consumo.',
    intro_text='La siguiente figura muestra la serie de consumo (GAP) tras el remuestreo a 1 día:'
)
fig_num += 1

doc.add_page_break()

# =============================================================================
# 2. HORIZONTES DE PREDICCIÓN
# =============================================================================
heading('2. Horizontes de Predicción', level=1)

para(
    'Un horizonte de predicción define cada cuánto tiempo el modelo realiza una '
    'estimación del consumo eléctrico futuro. En esta tesis se evaluaron tres '
    'horizontes distintos, cada uno correspondiente a un escenario de análisis. '
    'La elección de múltiples horizontes permite comparar el desempeño de los '
    'modelos bajo distintas exigencias de resolución temporal.'
)

t3 = doc.add_table(rows=1, cols=3)
t3.style = 'Table Grid'
for cell, text in zip(t3.rows[0].cells, ['Escenario', 'Horizonte', 'Historia utilizada']):
    r = cell.paragraphs[0].add_run(text)
    r.font.name = 'Times New Roman'; r.font.size = Pt(11); r.bold = True

for row_data in [
    ('Escenario 1', '15 minutos', 'Hasta 24 horas hacia atrás (96 períodos)'),
    ('Escenario 2', '1 hora',     'Hasta 1 semana hacia atrás (168 períodos)'),
    ('Escenario 3', '1 día',      'Hasta 1 mes hacia atrás (30 períodos)'),
]:
    table_row3(t3, *row_data)

doc.add_paragraph()

heading('2.1 Escenario 1 — Horizonte de 15 Minutos', level=2)
para(
    'El modelo predice el consumo eléctrico para el próximo cuarto de hora. '
    'Es el horizonte más detallado y preciso del estudio, adecuado para sistemas '
    'de gestión energética en tiempo real. Dispone del mayor volumen de datos para '
    'entrenamiento, con 96 observaciones por día. El rezago más largo utilizado '
    'equivale a 24 horas de historia (96 períodos de 15 minutos).'
)

heading('2.2 Escenario 2 — Horizonte de 1 Hora', level=2)
para(
    'El modelo predice el consumo eléctrico de la próxima hora. Representa un '
    'equilibrio entre detalle y simplicidad, útil para la planificación operativa '
    'del consumo residencial. El rezago más largo utilizado equivale a una semana '
    'completa de historia (168 horas), lo que permite al modelo capturar tanto '
    'patrones diarios como comportamientos semanales.'
)

heading('2.3 Escenario 3 — Horizonte de 1 Día', level=2)
para(
    'El modelo predice el consumo eléctrico total del día siguiente. Es el horizonte '
    'más general del estudio y resulta útil para la planificación energética a '
    'mediano plazo. El rezago más largo utilizado equivale a un mes de historia '
    '(30 días). Al tener menor cantidad de datos disponibles, este escenario '
    'presenta el mayor desafío para los modelos.'
)

doc.add_page_break()

# =============================================================================
# 3. FEATURE ENGINEERING
# =============================================================================
heading('3. Feature Engineering', level=1)

para(
    'El feature engineering es el proceso de construir nuevas variables a partir '
    'de los datos originales, con el objetivo de entregar al modelo información '
    'relevante para la predicción. Los modelos de machine learning no interpretan '
    'el tiempo directamente, por lo que es necesario transformar la dimensión '
    'temporal en columnas numéricas que el modelo pueda utilizar como predictores.'
)

para(
    'En esta tesis se construyeron tres tipos de variables para cada escenario: '
    'variables temporales, rezagos (lags) y medias móviles (rolling windows). '
    'Cada tipo aporta una perspectiva distinta sobre el comportamiento histórico '
    'del consumo.'
)

# Variables base EDA
heading('3.1 Variables Temporales Base (EDA)', level=2)
para(
    'Durante el análisis exploratorio se generaron variables temporales a partir del '
    'índice de fecha y hora, las cuales son reconstruidas en cada escenario tras el '
    'proceso de remuestreo. La tabla siguiente muestra las variables temporales '
    'utilizadas como predictores, indicando en qué escenarios se aplica cada una:'
)

t4 = doc.add_table(rows=1, cols=2)
t4.style = 'Table Grid'
for cell, text in zip(t4.rows[0].cells, ['Variable', 'Descripción']):
    r = cell.paragraphs[0].add_run(text)
    r.font.name = 'Times New Roman'; r.font.size = Pt(11); r.bold = True

for row_data in [
    ('hora',       'Hora del día (0–23) — utilizada en Escenarios 1 y 2'),
    ('dia_semana', 'Día de la semana (0=lunes, 6=domingo) — utilizada en los 3 escenarios'),
    ('mes',        'Mes del año (1–12) — utilizada en los 3 escenarios'),
    ('trimestre',  'Trimestre del año (1–4) — utilizada en Escenario 3'),
    ('dia_anio',   'Día del año (1–365/366) — utilizada en Escenario 3'),
    ('es_finde',   '1 si es sábado o domingo, 0 si es día de semana — utilizada en los 3 escenarios'),
]:
    table_row(t4, *row_data, bold_col1=True)

doc.add_paragraph()

# Por escenario
heading('3.2 Variables por Escenario', level=2)

heading('Escenario 1 — 15 Minutos', level=3)
para('Variables temporales utilizadas: hora, dia_semana, mes, es_finde.')
para('Rezagos de GAP construidos:')

t5 = doc.add_table(rows=1, cols=2)
t5.style = 'Table Grid'
for cell, text in zip(t5.rows[0].cells, ['Variable', 'Equivalencia temporal']):
    r = cell.paragraphs[0].add_run(text); r.font.name='Times New Roman'; r.font.size=Pt(11); r.bold=True
for row_data in [
    ('GAP_lag_1',  'Consumo hace 15 minutos'),
    ('GAP_lag_2',  'Consumo hace 30 minutos'),
    ('GAP_lag_4',  'Consumo hace 1 hora'),
    ('GAP_lag_8',  'Consumo hace 2 horas'),
    ('GAP_lag_12', 'Consumo hace 3 horas'),
    ('GAP_lag_96', 'Consumo hace 24 horas'),
]:
    table_row(t5, *row_data, bold_col1=True)

doc.add_paragraph()
para('Medias y desviaciones móviles construidas:')

t6 = doc.add_table(rows=1, cols=2)
t6.style = 'Table Grid'
for cell, text in zip(t6.rows[0].cells, ['Variable', 'Equivalencia temporal']):
    r = cell.paragraphs[0].add_run(text); r.font.name='Times New Roman'; r.font.size=Pt(11); r.bold=True
for row_data in [
    ('GAP_roll_mean_4  / GAP_roll_std_4',   'Promedio y desviación de la última hora'),
    ('GAP_roll_mean_8  / GAP_roll_std_8',   'Promedio y desviación de las últimas 2 horas'),
    ('GAP_roll_mean_96 / GAP_roll_std_96',  'Promedio y desviación de las últimas 24 horas'),
]:
    table_row(t6, *row_data, bold_col1=True)

doc.add_paragraph()

heading('Escenario 2 — 1 Hora', level=3)
para('Variables temporales utilizadas: hora, dia_semana, mes, es_finde.')
para('Rezagos de GAP construidos:')

t7 = doc.add_table(rows=1, cols=2)
t7.style = 'Table Grid'
for cell, text in zip(t7.rows[0].cells, ['Variable', 'Equivalencia temporal']):
    r = cell.paragraphs[0].add_run(text); r.font.name='Times New Roman'; r.font.size=Pt(11); r.bold=True
for row_data in [
    ('GAP_lag_1',   'Consumo hace 1 hora'),
    ('GAP_lag_2',   'Consumo hace 2 horas'),
    ('GAP_lag_3',   'Consumo hace 3 horas'),
    ('GAP_lag_6',   'Consumo hace 6 horas'),
    ('GAP_lag_12',  'Consumo hace 12 horas'),
    ('GAP_lag_24',  'Consumo hace 1 día'),
    ('GAP_lag_48',  'Consumo hace 2 días'),
    ('GAP_lag_168', 'Consumo hace 1 semana'),
]:
    table_row(t7, *row_data, bold_col1=True)

doc.add_paragraph()
para('Medias y desviaciones móviles construidas:')

t8 = doc.add_table(rows=1, cols=2)
t8.style = 'Table Grid'
for cell, text in zip(t8.rows[0].cells, ['Variable', 'Equivalencia temporal']):
    r = cell.paragraphs[0].add_run(text); r.font.name='Times New Roman'; r.font.size=Pt(11); r.bold=True
for row_data in [
    ('GAP_roll_mean_6   / GAP_roll_std_6',   'Promedio y desviación de las últimas 6 horas'),
    ('GAP_roll_mean_24  / GAP_roll_std_24',  'Promedio y desviación del último día'),
    ('GAP_roll_mean_168 / GAP_roll_std_168', 'Promedio y desviación de la última semana'),
]:
    table_row(t8, *row_data, bold_col1=True)

doc.add_paragraph()

heading('Escenario 3 — 1 Día', level=3)
para('Variables temporales utilizadas: dia_semana, mes, trimestre, dia_anio, es_finde. (No se incluye "hora" porque los datos son diarios.)')
para('Rezagos de GAP construidos:')

t9 = doc.add_table(rows=1, cols=2)
t9.style = 'Table Grid'
for cell, text in zip(t9.rows[0].cells, ['Variable', 'Equivalencia temporal']):
    r = cell.paragraphs[0].add_run(text); r.font.name='Times New Roman'; r.font.size=Pt(11); r.bold=True
for row_data in [
    ('GAP_lag_1',  'Consumo de ayer'),
    ('GAP_lag_2',  'Consumo de hace 2 días'),
    ('GAP_lag_3',  'Consumo de hace 3 días'),
    ('GAP_lag_7',  'Consumo de hace 1 semana'),
    ('GAP_lag_14', 'Consumo de hace 2 semanas'),
    ('GAP_lag_30', 'Consumo de hace ~1 mes'),
]:
    table_row(t9, *row_data, bold_col1=True)

doc.add_paragraph()
para('Medias y desviaciones móviles construidas:')

t10 = doc.add_table(rows=1, cols=2)
t10.style = 'Table Grid'
for cell, text in zip(t10.rows[0].cells, ['Variable', 'Equivalencia temporal']):
    r = cell.paragraphs[0].add_run(text); r.font.name='Times New Roman'; r.font.size=Pt(11); r.bold=True
for row_data in [
    ('GAP_roll_mean_7  / GAP_roll_std_7',  'Promedio y desviación de la última semana'),
    ('GAP_roll_mean_14 / GAP_roll_std_14', 'Promedio y desviación de las últimas 2 semanas'),
    ('GAP_roll_mean_30 / GAP_roll_std_30', 'Promedio y desviación del último mes'),
]:
    table_row(t10, *row_data, bold_col1=True)

doc.add_paragraph()

doc.add_page_break()

# =============================================================================
# 4. MODELOS Y RESULTADOS
# =============================================================================
heading('4. Modelos y Resultados', level=1)

para(
    'Se evaluaron tres algoritmos de machine learning en cada uno de los tres '
    'escenarios: Random Forest, XGBoost y Support Vector Regression (SVR). '
    'La evaluación se realizó sobre el conjunto de prueba (20% cronológico final) '
    'utilizando cuatro métricas: RMSE, MAE, MAPE y R².'
)

# Descripción modelos
heading('4.1 Descripción de los Modelos', level=2)

heading('Random Forest', level=3)
para(
    'Es un modelo de ensamble que construye múltiples árboles de decisión de forma '
    'independiente y promedia sus predicciones. Su fortaleza reside en su robustez '
    'ante datos ruidosos y su capacidad para capturar relaciones no lineales sin '
    'necesidad de escalar los datos.'
)

heading('XGBoost', level=3)
para(
    'Es un modelo de ensamble basado en gradient boosting, donde cada árbol corrige '
    'los errores del árbol anterior. Es conocido por su alta precisión y eficiencia '
    'computacional, siendo uno de los algoritmos más utilizados en competencias de '
    'ciencia de datos.'
)

heading('SVR — Support Vector Regression', level=3)
para(
    'Es una extensión de las máquinas de soporte vectorial para problemas de regresión. '
    'Busca encontrar una función que se ajuste a los datos dentro de un margen de '
    'tolerancia definido. Requiere escalado previo de los datos y puede ser costoso '
    'computacionalmente en datasets grandes.'
)

# Resultados base
heading('4.2 Resultados Base (sin ajuste de hiperparámetros)', level=2)

para('La siguiente tabla presenta los resultados obtenidos con la configuración base de cada modelo:')

t11 = doc.add_table(rows=1, cols=6)
t11.style = 'Table Grid'
for cell, text in zip(t11.rows[0].cells, ['Escenario', 'Modelo', 'RMSE', 'MAE', 'MAPE', 'R²']):
    r = cell.paragraphs[0].add_run(text)
    r.font.name='Times New Roman'; r.font.size=Pt(11); r.bold=True

for row_data in [
    ('15 minutos', 'Random Forest', '0.2013', '0.1194', '14.79%', '0.9144'),
    ('15 minutos', 'XGBoost',       '0.1949', '0.1181', '14.89%', '0.9198'),
    ('15 minutos', 'SVR',           '0.2585', '0.1701', '24.25%', '0.8589'),
    ('1 hora',     'Random Forest', '0.2200', '0.1431', '17.43%', '0.8751'),
    ('1 hora',     'XGBoost',       '0.2146', '0.1385', '16.98%', '0.8812'),
    ('1 hora',     'SVR',           '0.2478', '0.1644', '20.56%', '0.8415'),
    ('1 día',      'Random Forest', '0.1253', '0.0943', '11.48%', '0.7313'),
    ('1 día',      'XGBoost',       '0.1140', '0.0818', '9.69%',  '0.7776'),
    ('1 día',      'SVR',           '0.1238', '0.0865', '10.25%', '0.7374'),
]:
    table_row5(t11, row_data)

doc.add_paragraph()

# Resultados tuning
heading('4.3 Resultados tras Ajuste de Hiperparámetros (GridSearchCV)', level=2)

para(
    'Se aplicó GridSearchCV con validación cruzada temporal (TimeSeriesSplit, 3 folds) '
    'para optimizar los hiperparámetros de cada modelo. La siguiente tabla muestra '
    'la comparación entre el R² base y el R² obtenido tras el ajuste:'
)

t12 = doc.add_table(rows=1, cols=5)
t12.style = 'Table Grid'
for cell, text in zip(t12.rows[0].cells, ['Escenario', 'Modelo', 'R² Base', 'R² Tuned', 'ΔR²']):
    r = cell.paragraphs[0].add_run(text)
    r.font.name='Times New Roman'; r.font.size=Pt(11); r.bold=True

for row_data in [
    ('15 minutos', 'Random Forest', '0.9144', '0.9145', '+0.0001'),
    ('15 minutos', 'XGBoost',       '0.9198', '0.9131', '-0.0067'),
    ('15 minutos', 'SVR',           '0.8589', '0.8801', '+0.0212'),
    ('1 hora',     'Random Forest', '0.8751', '0.8754', '+0.0003'),
    ('1 hora',     'XGBoost',       '0.8812', '0.8812', '+0.0000'),
    ('1 hora',     'SVR',           '0.8415', '0.8580', '+0.0165'),
    ('1 día',      'Random Forest', '0.7313', '0.7276', '-0.0037'),
    ('1 día',      'XGBoost',       '0.7776', '0.7748', '-0.0028'),
    ('1 día',      'SVR',           '0.7374', '0.7848', '+0.0474'),
]:
    table_row5(t12, row_data)

doc.add_paragraph()

# Conclusiones
heading('4.4 Conclusiones por Escenario', level=2)

heading('Escenario 1 — 15 Minutos', level=3)
para(
    'XGBoost y Random Forest obtienen los mejores resultados con R² superior a 0.91, '
    'lo que indica que los modelos explican más del 91% de la variabilidad del consumo. '
    'SVR mejora notablemente tras el ajuste de hiperparámetros (+0.0212 en R²). '
    'El mejor modelo tuned es Random Forest con R²=0.9145.'
)

heading('Escenario 2 — 1 Hora', level=3)
para(
    'XGBoost lidera con R²=0.8812, prácticamente sin cambio tras el tuning, lo que '
    'indica que su configuración base ya era óptima. SVR mejora con el ajuste '
    '(+0.0165). El mejor modelo tuned es XGBoost con R²=0.8812.'
)

heading('Escenario 3 — 1 Día', level=3)
para(
    'SVR es el modelo más beneficiado por el ajuste de hiperparámetros en este '
    'escenario (+0.0474 en R²), convirtiéndose en el mejor modelo tuned con '
    'R²=0.7848. Random Forest y XGBoost disminuyen levemente tras el tuning, '
    'lo que sugiere que ya habían alcanzado su límite con la configuración base.'
)

heading('Conclusión General', level=2)
para(
    'A mayor granularidad temporal (menor horizonte de predicción), los modelos '
    'obtienen mejores resultados. El escenario de 15 minutos alcanza el mejor '
    'desempeño global (R²=0.91), dado que dispone de más datos y patrones más '
    'repetitivos. El escenario diario, si bien con menor R² (0.78), representa '
    'el horizonte de mayor utilidad práctica para la planificación energética. '
    'SVR es el modelo que más se beneficia del ajuste de hiperparámetros en todos '
    'los escenarios, mientras que Random Forest y XGBoost ya presentaban una '
    'configuración base cercana a la óptima.'
)

# =============================================================================
# GUARDAR
# =============================================================================
doc.save(OUT_PATH)
print(f'✓ Documento generado: {OUT_PATH}')
