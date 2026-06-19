# =============================================================================
# GUÍA DE ESTUDIO PARA DEFENSA DE TESIS
# Genera un documento Word completo para preparar la sustentación
# =============================================================================

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

_here = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = _here if os.path.exists(os.path.join(_here, 'datos')) else os.path.dirname(_here)
OUT_FILE = os.path.join(BASE_DIR, 'Guia_Estudio_Defensa.docx')

# =============================================================================
# HELPERS
# =============================================================================

def set_cell_bg(cell, hex_color):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)
    tcPr.append(shd)

def heading(doc, text, level, color=None):
    h = doc.add_heading(text, level=level)
    if color:
        h.runs[0].font.color.rgb = color
    else:
        colors = {
            1: RGBColor(0x1A, 0x23, 0x7E),
            2: RGBColor(0x0D, 0x47, 0xA1),
            3: RGBColor(0x1B, 0x5E, 0x20),
            4: RGBColor(0x4A, 0x14, 0x8C),
        }
        h.runs[0].font.color.rgb = colors.get(level, RGBColor(0x33, 0x33, 0x33))
    return h

def body(doc, text, bold_prefix=None):
    p = doc.add_paragraph()
    if bold_prefix:
        run_b = p.add_run(bold_prefix)
        run_b.bold = True
    p.add_run(text)
    p.paragraph_format.space_after = Pt(5)
    return p

def bullet(doc, text, bold_prefix=None):
    p = doc.add_paragraph(style='List Bullet')
    if bold_prefix:
        r = p.add_run(bold_prefix)
        r.bold = True
    p.add_run(text)
    p.paragraph_format.space_after = Pt(3)
    return p

def nota(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.8)
    p.paragraph_format.space_after = Pt(5)
    run = p.add_run('NOTA: ')
    run.bold = True
    run.font.color.rgb = RGBColor(0xB7, 0x1C, 0x1C)
    r2 = p.add_run(text)
    r2.italic = True
    r2.font.color.rgb = RGBColor(0x4E, 0x34, 0x2E)
    return p

def pregunta_jurado(doc, pregunta, respuesta):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.5)
    p.paragraph_format.space_before = Pt(8)
    r = p.add_run('P: ' + pregunta)
    r.bold = True
    r.font.color.rgb = RGBColor(0xB7, 0x1C, 0x1C)
    r.font.size = Pt(11)

    p2 = doc.add_paragraph()
    p2.paragraph_format.left_indent = Cm(0.8)
    p2.paragraph_format.space_after = Pt(6)
    r2 = p2.add_run('R: ')
    r2.bold = True
    r2.font.color.rgb = RGBColor(0x1B, 0x5E, 0x20)
    p2.add_run(respuesta)

def formula(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(text)
    run.font.name = 'Courier New'
    run.font.size = Pt(11)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0x1A, 0x23, 0x7E)
    return p

def add_hr(doc):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(6)
    pPr = p._p.get_or_add_pPr()
    pb = OxmlElement('w:pBdr')
    bot = OxmlElement('w:bottom')
    bot.set(qn('w:val'), 'single')
    bot.set(qn('w:sz'), '8')
    bot.set(qn('w:space'), '1')
    bot.set(qn('w:color'), '1A237E')
    pb.append(bot)
    pPr.append(pb)

def seccion_alerta(doc, texto):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.6)
    p.paragraph_format.space_after = Pt(6)
    shading = OxmlElement('w:shd')
    shading.set(qn('w:val'), 'clear')
    shading.set(qn('w:fill'), 'FFF8E1')
    p._p.get_or_add_pPr().append(shading)
    r = p.add_run('★  ' + texto)
    r.font.color.rgb = RGBColor(0xE6, 0x5C, 0x00)
    r.bold = True

# =============================================================================
# CREAR DOCUMENTO
# =============================================================================
doc = Document()

for section in doc.sections:
    section.top_margin = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin = Cm(3.0)
    section.right_margin = Cm(2.5)

style = doc.styles['Normal']
style.font.name = 'Calibri'
style.font.size = Pt(11)

# =============================================================================
# PORTADA
# =============================================================================
for _ in range(4):
    doc.add_paragraph()

title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = title.add_run('GUÍA DE ESTUDIO PARA LA DEFENSA DE TESIS')
run.font.size = Pt(22)
run.font.bold = True
run.font.color.rgb = RGBColor(0x1A, 0x23, 0x7E)

doc.add_paragraph()
sub = doc.add_paragraph()
sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = sub.add_run('"Modelo predictivo del consumo energético en hogares\ninteligentes utilizando algoritmos de machine learning"')
r.font.size = Pt(14)
r.font.italic = True
r.font.color.rgb = RGBColor(0x42, 0x42, 0x42)

doc.add_paragraph()
doc.add_paragraph()
desc = doc.add_paragraph()
desc.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = desc.add_run(
    'Contiene: Dataset · Preprocesamiento · Feature Engineering · Modelos ML\n'
    'Métricas · Tuning · Análisis de Resultados · Preguntas del Jurado · Glosario'
)
r.font.size = Pt(11)
r.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

doc.add_paragraph()
anio = doc.add_paragraph()
anio.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = anio.add_run('2026')
r.font.size = Pt(12)
r.font.bold = True

doc.add_page_break()

# =============================================================================
# SECCIÓN 1 — EL DATASET
# =============================================================================
heading(doc, '1. EL DATASET', 1)
add_hr(doc)

heading(doc, '1.1 ¿Qué es el dataset?', 2)
body(doc,
    'Se utilizó el dataset "Individual Household Electric Power Consumption" del '
    'repositorio UCI Machine Learning Repository (University of California, Irvine). '
    'Es uno de los datasets más utilizados en el mundo para investigación de machine '
    'learning aplicado a energía residencial.')
body(doc,
    'Contiene mediciones de consumo eléctrico de UN hogar residencial ubicado en '
    'Sceaux, Francia (7 km al sur de París), recolectadas entre el 16 de diciembre '
    'de 2006 y el 26 de noviembre de 2010, a una frecuencia de UN MINUTO.')

heading(doc, '1.2 Estadísticas clave del dataset', 2)

t = doc.add_table(rows=6, cols=2)
t.style = 'Table Grid'
t.alignment = WD_TABLE_ALIGNMENT.CENTER
datos_stat = [
    ('Total de registros', '2,075,259 filas × 9 columnas'),
    ('Frecuencia de muestreo', '1 medición por minuto'),
    ('Período cubierto', '16/12/2006 → 26/11/2010 (≈ 4 años)'),
    ('Valores nulos', '1.252% de las filas (todos simultáneos)'),
    ('Registros tras limpieza', '1,739,167 (después de dropna + IQR)'),
    ('País / Contexto', 'Francia — hogar residencial europeo'),
]
for i, (k, v) in enumerate(datos_stat):
    bg = 'E8EAF6' if i % 2 == 0 else 'FFFFFF'
    t.rows[i].cells[0].text = k
    t.rows[i].cells[1].text = v
    t.rows[i].cells[0].paragraphs[0].runs[0].font.bold = True
    for cell in t.rows[i].cells:
        set_cell_bg(cell, bg)

doc.add_paragraph()

heading(doc, '1.3 Variables del dataset — explicadas', 2)
body(doc, 'El dataset tiene 7 variables numéricas (más Date y Time que se unen en el índice datetime):')

t2 = doc.add_table(rows=9, cols=4)
t2.style = 'Table Grid'
t2.alignment = WD_TABLE_ALIGNMENT.CENTER
for j, h in enumerate(['Variable original', 'Alias', 'Unidad', 'Descripción y rol en la tesis']):
    t2.rows[0].cells[j].text = h
    t2.rows[0].cells[j].paragraphs[0].runs[0].font.bold = True
    t2.rows[0].cells[j].paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    set_cell_bg(t2.rows[0].cells[j], '1A237E')

vars_info = [
    ('Global_active_power', 'GAP', 'kW',
     'VARIABLE OBJETIVO. Potencia activa total consumida por el hogar. '
     'Es la energía "real" que realiza trabajo útil (calefacción, iluminación, electrodomésticos).'),
    ('Global_reactive_power', 'GRP', 'kW',
     'Feature del modelo. Potencia reactiva (energía que oscila entre fuente y carga, '
     'no realiza trabajo útil). Complementa la información de GAP.'),
    ('Voltage', 'VOLT', 'V',
     'Feature del modelo. Voltaje promedio en el hogar. Varía según la demanda '
     'de la red eléctrica.'),
    ('Global_intensity', 'GI', 'A',
     'DESCARTADA. Intensidad de corriente. Correlación de Pearson = 0.999 con GAP '
     '(por la ley de Ohm: P = V·I). Su inclusión causaría multicolinealidad severa.'),
    ('Sub_metering_1', 'SM1', 'Wh',
     'Sub-medidor cocina (lavavajillas, horno, microondas). NOTA: quedó en 0 tras '
     'el filtro IQR por distribución esparsa. Limitación conocida.'),
    ('Sub_metering_2', 'SM2', 'Wh',
     'Sub-medidor lavandería (lavadora, secadora, heladera). Feature del modelo.'),
    ('Sub_metering_3', 'SM3', 'Wh',
     'Sub-medidor calefacción y aire acondicionado. Feature del modelo. '
     'Suele ser la variable de mayor consumo en el hogar estudiado.'),
    ('Date + Time', 'datetime (índice)', '—',
     'Marca temporal combinada. Se usa como índice de la serie de tiempo '
     'y para extraer features temporales (hora, día, mes).'),
]
for i, (orig, alias, unidad, desc) in enumerate(vars_info):
    bg = 'F5F5F5' if i % 2 == 0 else 'FFFFFF'
    if orig == 'Global_intensity':
        bg = 'FFEBEE'
    elif orig == 'Global_active_power':
        bg = 'E8F5E9'
    row = t2.rows[i+1]
    row.cells[0].text = orig
    row.cells[1].text = alias
    row.cells[2].text = unidad
    row.cells[3].text = desc
    for cell in row.cells:
        cell.paragraphs[0].runs[0].font.size = Pt(9.5)
        set_cell_bg(cell, bg)

doc.add_paragraph()

heading(doc, '1.4 ¿Por qué se eligió este dataset?', 2)
bullet(doc, 'Es un dataset REAL de un hogar real, no simulado.')
bullet(doc, 'Cubre 4 años completos, capturando estacionalidad anual, semanal y diaria.')
bullet(doc, 'Tiene múltiples variables (sub-medidores) que enriquecen el análisis.')
bullet(doc, 'Es el dataset estándar de referencia en la literatura de ML energético, '
       'lo que permite comparar resultados con otros trabajos.')
bullet(doc, 'Está disponible públicamente y es reproducible.')

nota(doc, 'Si el jurado pregunta "¿por qué este dataset y no uno chileno?", la respuesta es: '
     'no existe un dataset público de hogares chilenos con estas características (4 años, '
     '1 minuto de resolución, múltiples sub-medidores). La metodología es transferible a '
     'cualquier dataset con estructura similar.')

doc.add_page_break()

# =============================================================================
# SECCIÓN 2 — LIMPIEZA DE DATOS
# =============================================================================
heading(doc, '2. LIMPIEZA DE DATOS', 1)
add_hr(doc)

heading(doc, '2.1 Valores nulos — ¿qué son y cómo se trataron?', 2)
body(doc,
    'Un valor nulo (missing value) ocurre cuando el medidor no registró datos en ese '
    'minuto. En este dataset, el 1.252% de las filas tiene valores faltantes, y cuando '
    'una fila tiene un nulo, TODAS las columnas de esa fila son nulas simultáneamente.')
body(doc,
    'Esto indica que hubo períodos sin medición (corte de luz, mantenimiento del medidor, etc.). '
    'Al ser simultáneos, todo el registro es inválido y se eliminó con:')
formula(doc, 'df = df.dropna()')
body(doc,
    'Resultado: se eliminaron 25,979 filas (1.252%), quedando 2,049,280 registros. '
    'Esta tasa es suficientemente baja como para no afectar la representatividad del dataset.')

heading(doc, '2.2 Filtro de outliers — Método IQR', 2)
body(doc,
    'Los outliers son valores extremos que distorsionan el entrenamiento del modelo. '
    'El método IQR (Interquartile Range) identifica y elimina valores anómalos:')
formula(doc, 'Q1 = percentil 25     Q3 = percentil 75     IQR = Q3 - Q1')
formula(doc, 'Límite inferior = Q1 - 1.5 × IQR')
formula(doc, 'Límite superior = Q3 + 1.5 × IQR')
body(doc,
    'Se eliminan las filas donde CUALQUIER variable numérica cae fuera de estos límites. '
    'Tras aplicar dropna + IQR, el dataset quedó con 1,739,167 registros.')

heading(doc, '2.3 El problema de SM1 (Sub-medidor de cocina)', 2)
body(doc,
    'La variable SM1 quedó en cero en todo el dataset limpio. Esto ocurre porque '
    'su distribución es muy esparsa: el 75% de las mediciones valen 0 (Q1=Q3=0). '
    'Al calcular IQR=0, el límite superior también es 0, y el filtro elimina todos '
    'los valores no-nulos como si fueran outliers.')
nota(doc,
    'Si el jurado pregunta sobre SM1: es una LIMITACIÓN conocida del método IQR en variables '
    'con distribuciones esparsas. Una alternativa sería usar un umbral mínimo o aplicar '
    'el filtro solo a variables con IQR > 0. Sin embargo, como SM1 representa el consumo '
    'de cocina (que es intermitente), su impacto en la predicción de GAP es menor.')

heading(doc, '2.4 Eliminación de GI — Multicolinealidad', 2)
body(doc,
    'Global Intensity (GI) tiene una correlación de Pearson de 0.999 con GAP. '
    'Esto se debe a la Ley de Ohm: la potencia activa es proporcional a la intensidad '
    'de corriente (P ≈ V × I). Incluir GI como feature causaría multicolinealidad:')
bullet(doc, 'Los modelos no podrían distinguir el efecto de GAP_lag vs GI_lag.')
bullet(doc, 'Aumentaría la varianza de los coeficientes (inestabilidad).')
bullet(doc, 'Generaría redundancia sin aportar información nueva.')
body(doc, 'Solución: se elimina GI en todos los escenarios antes del entrenamiento.')

doc.add_page_break()

# =============================================================================
# SECCIÓN 3 — GRANULARIDADES Y RESAMPLE
# =============================================================================
heading(doc, '3. GRANULARIDADES TEMPORALES Y RESAMPLE', 1)
add_hr(doc)

heading(doc, '3.1 ¿Qué es el resample?', 2)
body(doc,
    'El dataset original tiene frecuencia de 1 minuto. Para crear los tres escenarios '
    'se aplica un resample: se agrupan los registros por ventana de tiempo y se '
    'calcula el promedio de cada variable en esa ventana.')
formula(doc, "df_15min = df.resample('15min').mean()")
formula(doc, "df_1hora = df.resample('h').mean()")
formula(doc, "df_1dia  = df.resample('D').mean()")
body(doc,
    'Se usa la media porque las variables son potencias promedias '
    '(no sumas de energía), así el promedio es la operación físicamente correcta.')

heading(doc, '3.2 Los tres escenarios y su justificación', 2)

t3 = doc.add_table(rows=4, cols=5)
t3.style = 'Table Grid'
t3.alignment = WD_TABLE_ALIGNMENT.CENTER
for j, h in enumerate(['Escenario', 'Frecuencia', 'Registros train', 'Registros test', 'Uso práctico']):
    t3.rows[0].cells[j].text = h
    t3.rows[0].cells[j].paragraphs[0].runs[0].font.bold = True
    t3.rows[0].cells[j].paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    set_cell_bg(t3.rows[0].cells[j], '0D47A1')

esc_rows = [
    ('E1 — 15 minutos', '15 min', '106,714', '26,679',
     'Gestión en tiempo real. Control de carga en el hogar. Smart plugs.'),
    ('E2 — 1 hora', '1 hora', '27,071', '6,768',
     'Planificación horaria. Tarificación horaria de electricidad.'),
    ('E3 — 1 día', '1 día', '1,122', '281',
     'Planificación de red eléctrica. Estimación de factura mensual.'),
]
for i, row_vals in enumerate(esc_rows):
    bg = 'E3F2FD' if i % 2 == 0 else 'FFFFFF'
    for j, val in enumerate(row_vals):
        t3.rows[i+1].cells[j].text = val
        t3.rows[i+1].cells[j].paragraphs[0].runs[0].font.size = Pt(9.5)
        set_cell_bg(t3.rows[i+1].cells[j], bg)

doc.add_paragraph()

heading(doc, '3.3 ¿Por qué comparar tres granularidades?', 2)
body(doc,
    'La granularidad temporal afecta directamente la dificultad de predicción y la '
    'utilidad práctica del modelo. Comparar las tres permite responder:')
bullet(doc, '¿Qué modelo funciona mejor a corto plazo vs largo plazo?')
bullet(doc, '¿Cómo cambia el error al agregar datos temporalmente?')
bullet(doc, '¿Qué escenario justifica mejor el costo computacional del modelo?')
body(doc,
    'Esta comparación sistemática es la contribución principal de la tesis. La mayoría '
    'de estudios similares analizan solo una granularidad.')

heading(doc, '3.4 El horizonte de pronóstico', 2)
body(doc,
    'En los tres escenarios se usa pronóstico de UN PASO ADELANTE (h=1): el modelo '
    'predice el valor del siguiente período usando los valores reales pasados como entrada.')
bullet(doc, 'E1: predice el consumo de los próximos 15 minutos.')
bullet(doc, 'E2: predice el consumo de la próxima hora.')
bullet(doc, 'E3: predice el consumo del día siguiente.')
nota(doc,
    'Durante la evaluación se usan valores REALES pasados (no predicciones anteriores) '
    'como input. En producción real, si se quisiera predecir 2 pasos adelante habría '
    'que usar la predicción del paso 1 como input, acumulando error. Esto es una '
    'limitación declarada en la tesis.')

doc.add_page_break()

# =============================================================================
# SECCIÓN 4 — FEATURE ENGINEERING
# =============================================================================
heading(doc, '4. FEATURE ENGINEERING (INGENIERÍA DE CARACTERÍSTICAS)', 1)
add_hr(doc)

body(doc,
    'Feature engineering es el proceso de crear variables de entrada (features) que '
    'ayuden al modelo a aprender los patrones de la serie temporal. Los modelos de ML '
    'clásicos (RF, XGBoost, SVR) NO son modelos de series de tiempo nativos: necesitan '
    'que la información temporal se les entregue explícitamente como features.')

heading(doc, '4.1 Features de LAGS (rezagos)', 2)
body(doc,
    'Un lag es el valor de la variable objetivo en un período anterior. Si el modelo '
    'quiere predecir GAP en el tiempo t, le entregamos GAP en t-1, t-2, t-3, etc.')
formula(doc, 'GAP_lag_1 = GAP(t-1)    GAP_lag_2 = GAP(t-2)    ...')
body(doc,
    'JUSTIFICACIÓN: El consumo eléctrico tiene fuerte autocorrelación. Lo que el hogar '
    'consumió hace 15 minutos es un excelente predictor de lo que consumirá ahora. '
    'El análisis ACF/PACF en el EDA confirmó esta dependencia temporal.')

t_lags = doc.add_table(rows=4, cols=3)
t_lags.style = 'Table Grid'
t_lags.alignment = WD_TABLE_ALIGNMENT.CENTER
for j, h in enumerate(['Escenario', 'Lags usados', 'Lag máximo equivale a...']):
    t_lags.rows[0].cells[j].text = h
    t_lags.rows[0].cells[j].paragraphs[0].runs[0].font.bold = True
    t_lags.rows[0].cells[j].paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    set_cell_bg(t_lags.rows[0].cells[j], '1B5E20')
lags_rows = [
    ('15 minutos', '[1, 2, 4, 8, 12, 96]', 'lag 96 = 24 horas atrás'),
    ('1 hora', '[1, 2, 3, 6, 12, 24, 48, 168]', 'lag 168 = 1 semana atrás'),
    ('1 día', '[1, 2, 3, 7, 14, 30]', 'lag 30 = 1 mes atrás'),
]
for i, row_vals in enumerate(lags_rows):
    bg = 'F1F8E9' if i % 2 == 0 else 'FFFFFF'
    for j, val in enumerate(row_vals):
        t_lags.rows[i+1].cells[j].text = val
        t_lags.rows[i+1].cells[j].paragraphs[0].runs[0].font.size = Pt(9.5)
        set_cell_bg(t_lags.rows[i+1].cells[j], bg)

doc.add_paragraph()

heading(doc, '4.2 Rolling Windows (ventanas móviles)', 2)
body(doc,
    'Una ventana móvil calcula la media o desviación estándar de los últimos N períodos. '
    'Captura la TENDENCIA RECIENTE del consumo, suavizando fluctuaciones.')
formula(doc, 'GAP_roll_mean_4 = promedio(GAP[t-4], GAP[t-3], GAP[t-2], GAP[t-1])')
formula(doc, 'GAP_roll_std_4  = desv.std(GAP[t-4], ..., GAP[t-1])')
body(doc,
    'Se usa shift(1) ANTES de calcular el rolling para evitar data leakage: si no se '
    'desplazara, la ventana incluiría el valor actual t en el promedio, lo cual es '
    'información que el modelo no debería ver al predecir t.')
nota(doc,
    'DATA LEAKAGE: ocurre cuando el modelo accede durante entrenamiento a información '
    'del futuro (o del propio instante a predecir). Si existiera leakage, las métricas '
    'en test serían irrealmente buenas pero el modelo fallaría en producción real.')

heading(doc, '4.3 Features temporales', 2)
body(doc, 'Se extraen del índice datetime para capturar patrones cíclicos:')

t_temp = doc.add_table(rows=7, cols=3)
t_temp.style = 'Table Grid'
t_temp.alignment = WD_TABLE_ALIGNMENT.CENTER
for j, h in enumerate(['Feature', 'Valores posibles', 'Patrón que captura']):
    t_temp.rows[0].cells[j].text = h
    t_temp.rows[0].cells[j].paragraphs[0].runs[0].font.bold = True
    t_temp.rows[0].cells[j].paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    set_cell_bg(t_temp.rows[0].cells[j], '4A148C')
temp_rows = [
    ('hora', '0 a 23', 'Mayor consumo en horas nocturnas (18-22h). Menor en madrugada.'),
    ('dia_semana', '0=Lun a 6=Dom', 'Fines de semana vs días laborales tienen patrones distintos.'),
    ('mes', '1 a 12', 'Variación estacional: más consumo en invierno (calefacción).'),
    ('es_finde', '0 ó 1', 'Indicador binario de fin de semana. Simplifica la captura del patrón.'),
    ('trimestre', '1 a 4', 'Solo en E3 (diario). Captura estacionalidad trimestral.'),
    ('dia_anio', '1 a 365', 'Solo en E3 (diario). Captura tendencia a lo largo del año.'),
]
for i, row_vals in enumerate(temp_rows):
    bg = 'F3E5F5' if i % 2 == 0 else 'FFFFFF'
    for j, val in enumerate(row_vals):
        t_temp.rows[i+1].cells[j].text = val
        t_temp.rows[i+1].cells[j].paragraphs[0].runs[0].font.size = Pt(9.5)
        set_cell_bg(t_temp.rows[i+1].cells[j], bg)

doc.add_paragraph()
body(doc,
    'NOTA: en E3 (diario) NO se incluye la feature "hora" porque al agregar por día '
    'se pierde la información intradiaria — todos los registros diarios tienen una '
    'sola entrada sin hora específica.')

doc.add_page_break()

# =============================================================================
# SECCIÓN 5 — SPLIT CRONOLÓGICO
# =============================================================================
heading(doc, '5. SPLIT CRONOLÓGICO TRAIN/TEST', 1)
add_hr(doc)

heading(doc, '5.1 ¿Por qué NO se usa split aleatorio en series de tiempo?', 2)
body(doc,
    'En machine learning convencional (datos tabulares sin dependencia temporal) '
    'el split aleatorio es correcto. Pero en series de tiempo es un ERROR GRAVE '
    'porque causa DATA LEAKAGE:')
bullet(doc, 'Si una muestra del año 2010 queda en train y otra del 2008 en test, '
       'el modelo "aprende del futuro" durante el entrenamiento.')
bullet(doc, 'Las métricas serían artificialmente buenas (el modelo ya "vio" esos datos).')
bullet(doc, 'En producción el modelo fallaría porque no puede ver el futuro.')

heading(doc, '5.2 Split cronológico 80/20', 2)
body(doc,
    'Se mantiene el orden temporal estricto: los primeros 80% de los datos son '
    'entrenamiento y los últimos 20% son prueba. El modelo solo aprende con datos '
    'pasados y se evalúa con datos futuros, simulando el escenario real.')
formula(doc, 'split = int(len(df) * 0.80)')
formula(doc, 'X_train = X[:split]    X_test = X[split:]')

t_split = doc.add_table(rows=4, cols=4)
t_split.style = 'Table Grid'
t_split.alignment = WD_TABLE_ALIGNMENT.CENTER
for j, h in enumerate(['Escenario', 'Train (80%)', 'Test (20%)', 'Corte temporal']):
    t_split.rows[0].cells[j].text = h
    t_split.rows[0].cells[j].paragraphs[0].runs[0].font.bold = True
    t_split.rows[0].cells[j].paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    set_cell_bg(t_split.rows[0].cells[j], '37474F')
split_rows = [
    ('15 minutos', '106,714 registros', '26,679 registros', 'Corte ≈ Abril 2009'),
    ('1 hora', '27,071 registros', '6,768 registros', 'Corte ≈ Abril 2009'),
    ('1 día', '1,122 registros', '281 registros', 'Corte ≈ Abril 2009'),
]
for i, row_vals in enumerate(split_rows):
    bg = 'ECEFF1' if i % 2 == 0 else 'FFFFFF'
    for j, val in enumerate(row_vals):
        t_split.rows[i+1].cells[j].text = val
        t_split.rows[i+1].cells[j].paragraphs[0].runs[0].font.size = Pt(9.5)
        set_cell_bg(t_split.rows[i+1].cells[j], bg)

doc.add_paragraph()

heading(doc, '5.3 Escalado para SVR', 2)
body(doc,
    'SVR es sensible a la magnitud de las variables (a diferencia de RF y XGBoost '
    'que usan reglas de división basadas en rangos). Se aplica StandardScaler '
    'que transforma cada variable para tener media=0 y desviación estándar=1:')
formula(doc, 'X_escalado = (X - media(X_train)) / desv_std(X_train)')
body(doc,
    'IMPORTANTE: el scaler se ajusta SOLO con los datos de train y luego se aplica '
    '(sin re-ajustar) al test. Si se ajustara también con test, estaría usando '
    'información del futuro para normalizar (data leakage).')
body(doc,
    'También se escala el target (y) de SVR para que el epsilon sea equivalente '
    'en todas las escalas. Las predicciones se invierten con inverse_transform '
    'antes de calcular las métricas.')

nota(doc,
    'RF y XGBoost NO necesitan escalado porque sus divisiones son comparaciones '
    '(¿GAP_lag_1 > umbral?) que son invariantes al escalado de las features.')

doc.add_page_break()

# =============================================================================
# SECCIÓN 6 — MODELOS DE MACHINE LEARNING
# =============================================================================
heading(doc, '6. MODELOS DE MACHINE LEARNING', 1)
add_hr(doc)

# Random Forest
heading(doc, '6.1 Random Forest (Bosque Aleatorio)', 2)
body(doc,
    'Random Forest es un algoritmo de ENSEMBLE LEARNING basado en árboles de decisión. '
    'La idea central es que muchos árboles "mediocres" juntos predicen mejor que un '
    'solo árbol "perfecto" (principio de la sabiduría colectiva).')

heading(doc, 'Cómo funciona:', 3)
bullet(doc, 'Se construyen N árboles de decisión (n_estimators).')
bullet(doc, 'Cada árbol se entrena con una MUESTRA BOOTSTRAP: subconjunto aleatorio '
       'con reemplazo de los datos de entrenamiento (técnica de bagging).')
bullet(doc, 'En cada nodo de cada árbol se selecciona aleatoriamente un subconjunto '
       'de features para encontrar la mejor división.')
bullet(doc, 'La predicción final es el PROMEDIO de las predicciones de todos los árboles.')

heading(doc, 'Hiperparámetros del modelo:', 3)
t_rf = doc.add_table(rows=4, cols=4)
t_rf.style = 'Table Grid'
t_rf.alignment = WD_TABLE_ALIGNMENT.CENTER
for j, h in enumerate(['Parámetro', 'Qué controla', 'Valor base', 'Valor tuned (E1)']):
    t_rf.rows[0].cells[j].text = h
    t_rf.rows[0].cells[j].paragraphs[0].runs[0].font.bold = True
    t_rf.rows[0].cells[j].paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    set_cell_bg(t_rf.rows[0].cells[j], '1565C0')
rf_params = [
    ('n_estimators', 'Número de árboles. Más árboles = más estable, pero más lento. '
     'Después de cierto número la mejora es marginal.', '200', '200'),
    ('max_depth', 'Profundidad máxima de cada árbol. None = sin límite (árboles profundos '
     'pueden sobreajustarse). Limitar reduce overfitting.', '20', 'None'),
    ('min_samples_leaf', 'Mínimo de muestras que debe tener una hoja terminal. '
     'Mayor valor = árbol más simple = menos overfitting.', '5', '5'),
]
for i, row_vals in enumerate(rf_params):
    bg = 'E3F2FD' if i % 2 == 0 else 'FFFFFF'
    for j, val in enumerate(row_vals):
        t_rf.rows[i+1].cells[j].text = val
        t_rf.rows[i+1].cells[j].paragraphs[0].runs[0].font.size = Pt(9.5)
        set_cell_bg(t_rf.rows[i+1].cells[j], bg)

doc.add_paragraph()
heading(doc, 'Ventajas y limitaciones:', 3)
bullet(doc, 'VENTAJA: No necesita escalado de datos.')
bullet(doc, 'VENTAJA: Maneja relaciones no lineales y features redundantes.')
bullet(doc, 'VENTAJA: Proporciona importancia de features (feature_importances_).')
bullet(doc, 'VENTAJA: Robusto ante outliers.')
bullet(doc, 'LIMITACIÓN: Alto uso de memoria con muchos árboles y datos grandes.')
bullet(doc, 'LIMITACIÓN: No extrapola bien fuera del rango de entrenamiento.')

doc.add_paragraph()

# XGBoost
heading(doc, '6.2 XGBoost (eXtreme Gradient Boosting)', 2)
body(doc,
    'XGBoost es un algoritmo de BOOSTING: construye árboles de forma SECUENCIAL, '
    'donde cada árbol nuevo intenta corregir los errores del árbol anterior. '
    'Es actualmente uno de los algoritmos más competitivos para datos tabulares.')

heading(doc, 'Cómo funciona:', 3)
bullet(doc, 'El primer árbol predice con el valor promedio.')
bullet(doc, 'Se calculan los RESIDUOS (errores) de esa predicción.')
bullet(doc, 'El segundo árbol aprende a predecir esos residuos.')
bullet(doc, 'La predicción se actualiza: nueva_predicción = anterior + learning_rate × corrección.')
bullet(doc, 'Este proceso se repite n_estimators veces.')

heading(doc, 'Hiperparámetros del modelo:', 3)
t_xgb = doc.add_table(rows=5, cols=4)
t_xgb.style = 'Table Grid'
t_xgb.alignment = WD_TABLE_ALIGNMENT.CENTER
for j, h in enumerate(['Parámetro', 'Qué controla', 'Valor base', 'Valor tuned (E2)']):
    t_xgb.rows[0].cells[j].text = h
    t_xgb.rows[0].cells[j].paragraphs[0].runs[0].font.bold = True
    t_xgb.rows[0].cells[j].paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    set_cell_bg(t_xgb.rows[0].cells[j], '2E7D32')
xgb_params = [
    ('n_estimators', 'Número de árboles (iteraciones de boosting). '
     'Más iteraciones = modelo más complejo.', '200', '200'),
    ('max_depth', 'Profundidad de cada árbol. Árboles poco profundos (4-6) '
     'generalmente funcionan mejor en boosting.', '6', '6'),
    ('learning_rate', 'Tamaño del paso de corrección. Valores pequeños (0.05) '
     'requieren más árboles pero generalizan mejor.', '0.05', '0.05'),
    ('subsample', 'Fracción de datos usada para cada árbol. < 1.0 introduce '
     'aleatoriedad y reduce overfitting (similar a bagging).', '0.8', '0.8'),
]
for i, row_vals in enumerate(xgb_params):
    bg = 'E8F5E9' if i % 2 == 0 else 'FFFFFF'
    for j, val in enumerate(row_vals):
        t_xgb.rows[i+1].cells[j].text = val
        t_xgb.rows[i+1].cells[j].paragraphs[0].runs[0].font.size = Pt(9.5)
        set_cell_bg(t_xgb.rows[i+1].cells[j], bg)

doc.add_paragraph()
heading(doc, 'Ventajas y limitaciones:', 3)
bullet(doc, 'VENTAJA: Incluye regularización L1/L2 que previene overfitting.')
bullet(doc, 'VENTAJA: tree_method="hist" lo hace muy eficiente computacionalmente.')
bullet(doc, 'VENTAJA: Generalmente supera a Random Forest en datos tabulares medianos.')
bullet(doc, 'LIMITACIÓN: Más hiperparámetros que afinar que RF.')
bullet(doc, 'LIMITACIÓN: Sensible al learning_rate: si es muy grande, no converge.')

doc.add_paragraph()

# SVR
heading(doc, '6.3 Support Vector Regression (SVR)', 2)
body(doc,
    'SVR es una extensión de las Support Vector Machines (SVM) para problemas de '
    'regresión. En lugar de clasificar, busca encontrar una función que se ajuste '
    'a los datos dentro de un margen de tolerancia ε (epsilon).')

heading(doc, 'Cómo funciona:', 3)
bullet(doc, 'Busca el hiperplano de regresión que deja el mayor número de puntos '
       'DENTRO del "tubo" de tolerancia ε.')
bullet(doc, 'Solo los puntos FUERA del tubo (llamados Support Vectors) contribuyen '
       'a definir el modelo.')
bullet(doc, 'El kernel RBF (Radial Basis Function) transforma los datos a un espacio '
       'de mayor dimensión, permitiendo capturar relaciones no lineales.')
bullet(doc, 'Matemáticamente: K(x_i, x_j) = exp(-gamma × ||x_i - x_j||²)')

heading(doc, 'Hiperparámetros del modelo:', 3)
t_svr = doc.add_table(rows=4, cols=4)
t_svr.style = 'Table Grid'
t_svr.alignment = WD_TABLE_ALIGNMENT.CENTER
for j, h in enumerate(['Parámetro', 'Qué controla', 'Valor base', 'Valor tuned (E3)']):
    t_svr.rows[0].cells[j].text = h
    t_svr.rows[0].cells[j].paragraphs[0].runs[0].font.bold = True
    t_svr.rows[0].cells[j].paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    set_cell_bg(t_svr.rows[0].cells[j], 'B71C1C')
svr_params = [
    ('C', 'Penalización por errores fuera del tubo ε. '
     'C alto = ajuste más estricto = más riesgo de overfitting. '
     'C bajo = más tolerante = modelo más simple.', '10.0', '1'),
    ('epsilon (ε)', 'Ancho del tubo de tolerancia. Los puntos dentro no generan error. '
     'Mayor ε = modelo más simple y menos sensible al ruido.', '0.05', '0.05'),
    ('gamma', 'Radio de influencia de cada punto de entrenamiento. '
     '"scale" = 1/n_features. Valor pequeño (0.01) = influencia más amplia.', 'scale', '0.01'),
]
for i, row_vals in enumerate(svr_params):
    bg = 'FFEBEE' if i % 2 == 0 else 'FFFFFF'
    for j, val in enumerate(row_vals):
        t_svr.rows[i+1].cells[j].text = val
        t_svr.rows[i+1].cells[j].paragraphs[0].runs[0].font.size = Pt(9.5)
        set_cell_bg(t_svr.rows[i+1].cells[j], bg)

doc.add_paragraph()
heading(doc, 'Ventajas y limitaciones:', 3)
bullet(doc, 'VENTAJA: Efectivo con datasets pequeños (como E3 con ~1,100 filas train).')
bullet(doc, 'VENTAJA: Robusto ante outliers (solo depende de los support vectors).')
bullet(doc, 'VENTAJA: El kernel RBF captura relaciones complejas.')
bullet(doc, 'LIMITACIÓN: O(n² a n³) en tiempo y memoria → muy lento con datasets grandes.')
bullet(doc, 'LIMITACIÓN: Por eso en E1 se limita a 15,000 muestras y en E2 a 10,000.')
bullet(doc, 'LIMITACIÓN: Requiere escalado obligatorio de features y target.')

nota(doc,
    'El tuning benefició más a SVR porque su configuración base (C=10, gamma=scale) '
    'estaba lejos del óptimo para datos energéticos. La configuración tuned '
    '(C=1, gamma=0.01) es más simple y generaliza mejor.')

doc.add_page_break()

# =============================================================================
# SECCIÓN 7 — MÉTRICAS DE EVALUACIÓN
# =============================================================================
heading(doc, '7. MÉTRICAS DE EVALUACIÓN', 1)
add_hr(doc)

body(doc,
    'Las métricas se calculan SIEMPRE sobre el conjunto de TEST (datos que el modelo '
    'nunca vio durante el entrenamiento). Usar métricas sobre train solo mediría '
    'cuánto memorizó el modelo, no cuánto aprendió a generalizar.')

heading(doc, '7.1 RMSE — Root Mean Squared Error', 2)
formula(doc, 'RMSE = √( (1/n) × Σ(y_real - y_pred)² )')
body(doc,
    'El RMSE eleva al cuadrado los errores antes de promediarlos, lo que PENALIZA '
    'fuertemente los errores grandes. Es sensible a outliers. '
    'Está en las mismas unidades que la variable objetivo (kW).')
body(doc, 'INTERPRETACIÓN: Un RMSE=0.19 significa que el modelo se equivoca en promedio '
     '0.19 kW, pero los errores grandes pesan más en este cálculo.')
bullet(doc, 'RMSE bajo = mejor predicción.')
bullet(doc, 'Valor de referencia: comparar con la desviación estándar de y_test.')

heading(doc, '7.2 MAE — Mean Absolute Error', 2)
formula(doc, 'MAE = (1/n) × Σ|y_real - y_pred|')
body(doc,
    'El MAE promedia los errores en valor absoluto, sin penalizar los grandes. '
    'Es más ROBUSTO que el RMSE ante outliers y más fácil de interpretar.')
body(doc, 'INTERPRETACIÓN: Un MAE=0.11 significa que en promedio el modelo se equivoca '
     '0.11 kW por predicción.')
bullet(doc, 'MAE bajo = mejor predicción.')
bullet(doc, 'Siempre MAE ≤ RMSE. Si la diferencia es grande, hay errores muy grandes ocasionalmente.')

heading(doc, '7.3 MAPE — Mean Absolute Percentage Error', 2)
formula(doc, 'MAPE = (100/n) × Σ|( y_real - y_pred ) / y_real|')
body(doc,
    'El MAPE expresa el error como PORCENTAJE del valor real. Es independiente '
    'de las unidades y permite comparar entre escenarios con diferentes escalas.')
body(doc, 'INTERPRETACIÓN: MAPE=14.76% significa que en promedio el modelo se equivoca '
     'en un 14.76% del valor real.')
bullet(doc, 'Se calcula solo donde y_real > 0.01 kW para evitar divisiones por cero.')
bullet(doc, 'Referencia general: <10% excelente, 10-20% bueno, 20-50% aceptable, >50% pobre.')

heading(doc, '7.4 R² — Coeficiente de Determinación', 2)
formula(doc, 'R² = 1 - SS_res / SS_tot')
formula(doc, 'SS_res = Σ(y_real - y_pred)²    SS_tot = Σ(y_real - ȳ)²')
body(doc,
    'R² mide qué proporción de la VARIANZA de los datos explica el modelo. '
    'Un modelo que siempre predice el promedio (ȳ) tiene R²=0. '
    'Un modelo perfecto tiene R²=1.')
body(doc, 'INTERPRETACIÓN: R²=0.9145 significa que el modelo explica el 91.45% '
     'de la variabilidad del consumo eléctrico.')
bullet(doc, 'R² > 0.90: excelente.')
bullet(doc, 'R² entre 0.80-0.90: muy bueno.')
bullet(doc, 'R² entre 0.70-0.80: bueno (aceptable para datos diarios con alta variabilidad).')
bullet(doc, 'R² < 0: el modelo es peor que predecir siempre el promedio.')

nota(doc,
    'En el escenario diario (E3), el R² máximo es 0.7848. Esto es esperado: '
    'al agregar los datos a nivel diario se pierde información intradiaria '
    'relevante para la predicción, y los 1,122 registros de train son pocos '
    'para capturar toda la variabilidad.')

heading(doc, '7.5 ¿Cuándo usar cada métrica?', 2)
t_met = doc.add_table(rows=5, cols=3)
t_met.style = 'Table Grid'
t_met.alignment = WD_TABLE_ALIGNMENT.CENTER
for j, h in enumerate(['Métrica', 'Cuándo priorizarla', 'Cuándo NO usarla sola']):
    t_met.rows[0].cells[j].text = h
    t_met.rows[0].cells[j].paragraphs[0].runs[0].font.bold = True
    t_met.rows[0].cells[j].paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    set_cell_bg(t_met.rows[0].cells[j], 'B71C1C')
met_rows = [
    ('RMSE', 'Cuando los errores grandes son costosos (ej: sobrecargar la red eléctrica).', 'Cuando hay muchos outliers que distorsionen el promedio.'),
    ('MAE', 'Cuando se quiere una métrica robusta e interpretable en las unidades de GAP.', 'Cuando los errores grandes merecen mayor penalización.'),
    ('MAPE', 'Para comparar entre escenarios con diferentes escalas de valores.', 'Cuando y_real puede ser cero o muy pequeño.'),
    ('R²', 'Para tener una medida relativa de la calidad del modelo vs. el promedio basal.', 'Con datos no estacionarios donde el promedio no es una buena referencia.'),
]
for i, row_vals in enumerate(met_rows):
    bg = 'FFF3E0' if i % 2 == 0 else 'FFFFFF'
    for j, val in enumerate(row_vals):
        t_met.rows[i+1].cells[j].text = val
        t_met.rows[i+1].cells[j].paragraphs[0].runs[0].font.size = Pt(9.5)
        set_cell_bg(t_met.rows[i+1].cells[j], bg)

doc.add_page_break()

# =============================================================================
# SECCIÓN 8 — TUNING DE HIPERPARÁMETROS
# =============================================================================
heading(doc, '8. OPTIMIZACIÓN DE HIPERPARÁMETROS (TUNING)', 1)
add_hr(doc)

heading(doc, '8.1 ¿Qué es el tuning y por qué es necesario?', 2)
body(doc,
    'Los hiperparámetros son configuraciones del modelo que NO se aprenden durante '
    'el entrenamiento: deben ser definidos ANTES de entrenar. El tuning es el proceso '
    'de encontrar la combinación de hiperparámetros que maximiza el rendimiento.')
body(doc,
    'Sin tuning, los valores por defecto o "base" pueden estar lejos del óptimo, '
    'dejando rendimiento sin aprovechar. Pero tampoco se puede buscar en el conjunto '
    'de test: eso sería usar información del futuro para optimizar el modelo.')

heading(doc, '8.2 GridSearchCV — Búsqueda exhaustiva', 2)
body(doc,
    'GridSearchCV prueba TODAS las combinaciones posibles de hiperparámetros definidas '
    'en una grilla. Para cada combinación, evalúa el rendimiento mediante '
    'validación cruzada y selecciona la combinación con mejor score promedio.')

t_grids = doc.add_table(rows=4, cols=4)
t_grids.style = 'Table Grid'
t_grids.alignment = WD_TABLE_ALIGNMENT.CENTER
for j, h in enumerate(['Modelo', 'Grilla de búsqueda', 'Combinaciones', 'Total de fits']):
    t_grids.rows[0].cells[j].text = h
    t_grids.rows[0].cells[j].paragraphs[0].runs[0].font.bold = True
    t_grids.rows[0].cells[j].paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    set_cell_bg(t_grids.rows[0].cells[j], '4E342E')
grids_rows = [
    ('Random Forest',
     'n_estimators: [100,200,300]\nmax_depth: [10,20,None]\nmin_samples_leaf: [1,5,10]',
     '3×3×3 = 27', '27 × 3 folds = 81 fits'),
    ('XGBoost',
     'n_estimators: [100,200]\nmax_depth: [4,6,8]\nlearning_rate: [0.05,0.1]\nsubsample: [0.8,1.0]',
     '2×3×2×2 = 24', '24 × 3 folds = 72 fits'),
    ('SVR',
     'C: [1,10,100]\nepsilon: [0.01,0.05,0.1]\ngamma: [scale, 0.01]',
     '3×3×2 = 18', '18 × 3 folds = 54 fits'),
]
for i, row_vals in enumerate(grids_rows):
    bg = 'EFEBE9' if i % 2 == 0 else 'FFFFFF'
    for j, val in enumerate(row_vals):
        t_grids.rows[i+1].cells[j].text = val
        t_grids.rows[i+1].cells[j].paragraphs[0].runs[0].font.size = Pt(9.5)
        set_cell_bg(t_grids.rows[i+1].cells[j], bg)

doc.add_paragraph()

heading(doc, '8.3 TimeSeriesSplit — Validación cruzada temporal', 2)
body(doc,
    'El KFold estándar divide aleatoriamente los datos en folds. En series de tiempo '
    'esto causa data leakage. TimeSeriesSplit resuelve esto garantizando que el '
    'conjunto de validación SIEMPRE sea temporalmente posterior al de entrenamiento:')
formula(doc, 'Fold 1: Train [1..n/4]       Val [n/4..n/2]')
formula(doc, 'Fold 2: Train [1..n/2]       Val [n/2..3n/4]')
formula(doc, 'Fold 3: Train [1..3n/4]      Val [3n/4..n]')
body(doc,
    'Se usaron 3 folds (n_splits=3) con scoring=R². El score de CV es el promedio '
    'de R² en los 3 folds de validación.')

nota(doc,
    'Con n_splits=3, los 3 escenarios × 3 modelos × (27+24+18) combinaciones '
    '= más de 600 entrenamientos. Por eso el script de tuning puede tardar '
    '20-60 minutos dependiendo del computador.')

heading(doc, '8.4 Proceso completo del tuning', 2)
bullet(doc, 'PASO 1: Definir grillas de hiperparámetros a explorar.')
bullet(doc, 'PASO 2: Ejecutar GridSearchCV con TimeSeriesSplit sobre el conjunto de TRAIN.')
bullet(doc, 'PASO 3: Identificar los mejores parámetros según CV R².')
bullet(doc, 'PASO 4: Re-entrenar el modelo con los mejores parámetros sobre TODO el train.')
bullet(doc, 'PASO 5: Evaluar el modelo re-entrenado sobre el conjunto de TEST.')
body(doc,
    'NOTA IMPORTANTE: el re-entrenamiento (paso 4) es sobre todo el train, no solo '
    'sobre el subconjunto usado en CV. Esto es estándar: se usa más data para el '
    'modelo final.')

doc.add_page_break()

# =============================================================================
# SECCIÓN 9 — RESULTADOS Y ANÁLISIS
# =============================================================================
heading(doc, '9. RESULTADOS Y ANÁLISIS', 1)
add_hr(doc)

heading(doc, '9.1 Tabla completa de resultados (modelos tuned)', 2)

t_res = doc.add_table(rows=10, cols=6)
t_res.style = 'Table Grid'
t_res.alignment = WD_TABLE_ALIGNMENT.CENTER
for j, h in enumerate(['Escenario', 'Modelo', 'RMSE (kW)', 'MAE (kW)', 'MAPE (%)', 'R²']):
    t_res.rows[0].cells[j].text = h
    t_res.rows[0].cells[j].paragraphs[0].runs[0].font.bold = True
    t_res.rows[0].cells[j].paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    set_cell_bg(t_res.rows[0].cells[j], '1A237E')

resultados = [
    ('15 min', 'Random Forest', '0.1898', '0.1107', '14.76', '0.9145', True),
    ('15 min', 'XGBoost',       '0.1876', '0.1111', '14.87', '0.9131', False),
    ('15 min', 'SVR',           '0.2397', '0.1491', '20.08', '0.8801', False),
    ('1 hora', 'Random Forest', '0.2211', '0.1416', '18.54', '0.8754', False),
    ('1 hora', 'XGBoost',       '0.2160', '0.1382', '18.42', '0.8812', True),
    ('1 hora', 'SVR',           '0.2580', '0.1711', '23.26', '0.8580', False),
    ('1 día',  'Random Forest', '0.1255', '0.0971', '12.50', '0.7276', False),
    ('1 día',  'XGBoost',       '0.1206', '0.0884', '11.37', '0.7748', False),
    ('1 día',  'SVR',           '0.1186', '0.0867', '10.96', '0.7848', True),
]
model_bg = {'Random Forest': 'E3F2FD', 'XGBoost': 'E8F5E9', 'SVR': 'FFEBEE'}
for i, (esc, mod, rmse, mae, mape, r2, es_mejor) in enumerate(resultados):
    bg = model_bg[mod]
    vals = [esc, mod, rmse, mae, mape, r2]
    for j, val in enumerate(vals):
        cell = t_res.rows[i+1].cells[j]
        cell.text = val
        run = cell.paragraphs[0].runs[0]
        run.font.size = Pt(9.5)
        if es_mejor and j >= 2:
            run.font.bold = True
            run.font.color.rgb = RGBColor(0x1B, 0x5E, 0x20)
        set_cell_bg(cell, bg)

doc.add_paragraph()
body(doc, 'Los valores en NEGRITA VERDE corresponden al mejor modelo de cada escenario.')

heading(doc, '9.2 ¿Por qué cada modelo gana en su escenario?', 2)

heading(doc, 'Escenario 15 min → Random Forest (R²=0.9145):', 3)
bullet(doc, 'Con 106,714 registros de train, RF tiene suficientes datos para construir '
       'árboles profundos y robustos.')
bullet(doc, 'Los patrones a 15 min son altamente autocorrelacionados: el lag_1 predice '
       'muy bien el siguiente período. RF captura esto eficientemente.')
bullet(doc, 'XGBoost es muy cercano (R²=0.9131) — la diferencia es mínima.')

heading(doc, 'Escenario 1 hora → XGBoost (R²=0.8812):', 3)
bullet(doc, 'Con menor resolución, la variabilidad entre períodos aumenta, '
       'requiriendo un modelo que corrija errores iterativamente (boosting).')
bullet(doc, 'XGBoost captura mejor los residuos de predicciones previas mediante '
       'su mecanismo de gradiente descendente.')
bullet(doc, 'El tuning confirmó que los parámetros base ya eran óptimos (ΔR²=0.0000).')

heading(doc, 'Escenario 1 día → SVR (R²=0.7848):', 3)
bullet(doc, 'Con solo 1,122 registros de train, RF y XGBoost tienen menos datos '
       'para construir modelos complejos y estables.')
bullet(doc, 'SVR con kernel RBF y C=1 (regularización fuerte) generaliza mejor '
       'con pocos datos: no sobreajusta.')
bullet(doc, 'SVR fue el mayor beneficiado por el tuning: ΔR²=+0.0474 (de 0.7374 a 0.7848).')
bullet(doc, 'A nivel diario, las tendencias de largo plazo son más suaves, '
       'lo que favorece al kernel RBF de SVR.')

heading(doc, '9.3 Impacto del tuning por modelo', 2)
t_delta = doc.add_table(rows=4, cols=4)
t_delta.style = 'Table Grid'
t_delta.alignment = WD_TABLE_ALIGNMENT.CENTER
for j, h in enumerate(['Modelo', 'Beneficio en E1', 'Beneficio en E2', 'Beneficio en E3']):
    t_delta.rows[0].cells[j].text = h
    t_delta.rows[0].cells[j].paragraphs[0].runs[0].font.bold = True
    t_delta.rows[0].cells[j].paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    set_cell_bg(t_delta.rows[0].cells[j], '37474F')
delta_rows = [
    ('Random Forest', 'ΔR²=+0.0001 (mínimo)', 'ΔR²=+0.0003 (mínimo)', 'ΔR²=-0.0037 (ligera caída)'),
    ('XGBoost', 'ΔR²=-0.0067 (ligera caída)', 'ΔR²=+0.0000 (sin cambio)', 'ΔR²=-0.0028 (ligera caída)'),
    ('SVR', 'ΔR²=+0.0212 (mejora clara)', 'ΔR²=+0.0165 (mejora clara)', 'ΔR²=+0.0474 (gran mejora)'),
]
for i, row_vals in enumerate(delta_rows):
    bg = model_bg[row_vals[0]]
    for j, val in enumerate(row_vals):
        t_delta.rows[i+1].cells[j].text = val
        run = t_delta.rows[i+1].cells[j].paragraphs[0].runs[0]
        run.font.size = Pt(9.5)
        if 'gran mejora' in val or 'mejora clara' in val:
            run.font.bold = True
            run.font.color.rgb = RGBColor(0x1B, 0x5E, 0x20)
        set_cell_bg(t_delta.rows[i+1].cells[j], bg)

doc.add_paragraph()
body(doc,
    'CONCLUSIÓN DEL TUNING: RF y XGBoost ya estaban bien calibrados con sus parámetros '
    'base (el GridSearchCV confirmó que estaban cerca del óptimo). SVR fue el mayor '
    'beneficiado porque sus parámetros base estaban más alejados del óptimo para '
    'datos de series temporales energéticas.')

doc.add_page_break()

# =============================================================================
# SECCIÓN 10 — PREGUNTAS DEL JURADO
# =============================================================================
heading(doc, '10. PREGUNTAS PROBABLES DEL JURADO', 1)
add_hr(doc)

seccion_alerta(doc, 'Estudia estas respuestas hasta poder darlas con confianza y '
               'sin leer. Son las preguntas más frecuentes en defensas de tesis de ML.')

doc.add_paragraph()

heading(doc, '10.1 Sobre el Dataset', 2)
pregunta_jurado(doc,
    '¿Por qué usaste el dataset de Francia si tu tesis es sobre hogares inteligentes en general?',
    'El dataset UCI de Francia es el estándar de referencia en la literatura de predicción '
    'energética residencial. No existe un dataset público comparable de Chile o Latinoamérica '
    'con 4 años de datos a resolución de 1 minuto. La metodología aplicada es completamente '
    'transferible a cualquier dataset con estructura similar. Además, usar un dataset de '
    'referencia internacional permite comparar mis resultados con estudios previos.')

pregunta_jurado(doc,
    '¿Por qué se eliminaron el 1.25% de los datos?',
    'Los valores nulos aparecen de forma simultánea en todas las columnas, lo que indica '
    'períodos sin medición del medidor (cortes de luz o mantenimiento), no errores aleatorios. '
    'Al no tener ninguna variable válida en esas filas, el registro completo es inútil para '
    'el entrenamiento. El 1.25% es una tasa suficientemente baja para no afectar la '
    'representatividad del dataset.')

pregunta_jurado(doc,
    '¿Por qué eliminaste la variable GI?',
    'Global Intensity tiene una correlación de Pearson de 0.999 con Global Active Power, '
    'la variable objetivo. Esto se explica por la Ley de Ohm: P = V × I. Incluir GI '
    'causaría multicolinealidad severa, donde el modelo no puede distinguir el efecto '
    'de cada variable y los coeficientes se vuelven inestables. Al eliminarla, '
    'se mantiene la información sin la redundancia.')

heading(doc, '10.2 Sobre la Metodología', 2)
pregunta_jurado(doc,
    '¿Qué es el data leakage y cómo lo evitaste?',
    'Data leakage ocurre cuando el modelo accede durante el entrenamiento a información '
    'del futuro, generando métricas artificialmente buenas que no se reproducen en producción. '
    'Lo evité de tres formas: (1) split cronológico sin mezcla aleatoria, (2) shift(1) '
    'en los rolling windows para que no incluyan el valor actual del período a predecir, '
    'y (3) el StandardScaler se ajusta solo con datos de train y se aplica sin re-ajustar '
    'al conjunto de test.')

pregunta_jurado(doc,
    '¿Por qué usaste split 80/20 cronológico y no validación cruzada estándar?',
    'En series de tiempo, el KFold estándar mezcla datos de diferentes períodos temporales, '
    'permitiendo que el modelo "aprenda del futuro". El split cronológico 80/20 respeta la '
    'dirección del tiempo: el modelo se entrena con el pasado y se evalúa con el futuro, '
    'que es exactamente cómo se usaría en producción. Para el tuning sí usé validación '
    'cruzada, pero con TimeSeriesSplit que también respeta el orden temporal.')

pregunta_jurado(doc,
    '¿Qué es el feature engineering y por qué es necesario?',
    'Los modelos de ML clásicos como RF, XGBoost y SVR no pueden capturar la dependencia '
    'temporal automáticamente: necesitan que esa información se les entregue explícitamente. '
    'El feature engineering transforma la serie temporal en un conjunto de features '
    'tabulares: lags (valores pasados), rolling windows (tendencias recientes) y '
    'features temporales (hora, día, mes). Sin esto, los modelos no tendrían información '
    'del comportamiento histórico para predecir.')

pregunta_jurado(doc,
    '¿Por qué usaste TimeSeriesSplit y no KFold en el tuning?',
    'KFold estándar asigna datos aleatoriamente a los folds, lo que significa que en '
    'algunos folds el conjunto de validación puede ser ANTERIOR temporalmente al de '
    'entrenamiento — el modelo "ve el futuro". TimeSeriesSplit garantiza que el fold '
    'de validación siempre sea posterior al de entrenamiento, preservando la integridad '
    'temporal del experimento de tuning.')

heading(doc, '10.3 Sobre los Modelos', 2)
pregunta_jurado(doc,
    '¿Por qué elegiste estos tres modelos y no otros (como LSTM o redes neuronales)?',
    'Se eligieron Random Forest, XGBoost y SVR porque son los modelos más utilizados '
    'en la literatura de predicción energética con ML clásico, permiten comparación '
    'directa con otros estudios, y tienen diferentes principios de funcionamiento '
    '(ensemble de árboles, boosting, margen de tolerancia) que enriquece el análisis '
    'comparativo. Los modelos de deep learning como LSTM son una extensión natural '
    'para trabajo futuro, pero requieren mayor volumen de datos y ajuste de '
    'arquitectura que excede el alcance de esta tesis.')

pregunta_jurado(doc,
    '¿Por qué SVR necesita escalado y Random Forest no?',
    'Random Forest y XGBoost usan árboles de decisión: sus divisiones son comparaciones '
    'del tipo "¿GAP_lag_1 > 1.5?" que son invariantes al escalado — si multiplicas '
    'todos los valores por 100, el umbral también se ajusta. SVR en cambio calcula '
    'distancias entre puntos en el espacio de features mediante el kernel RBF. Si una '
    'variable tiene valores en miles y otra en décimas, dominaría el cálculo de '
    'distancias. El escalado iguala la contribución de cada variable.')

pregunta_jurado(doc,
    '¿Por qué SVR se entrenó con menos datos que RF y XGBoost?',
    'SVR tiene complejidad computacional O(n²) a O(n³) en número de muestras. Con los '
    '106,714 registros de entrenamiento del escenario de 15 minutos, SVR tardaría '
    'horas o días en entrenarse. Se usaron las 15,000 muestras más recientes del train, '
    'que son las más representativas del comportamiento actual del hogar, ya que '
    'reflejan patrones recientes en lugar de comportamientos de años anteriores.')

heading(doc, '10.4 Sobre los Resultados', 2)
pregunta_jurado(doc,
    '¿Qué significa que el modelo tenga R²=0.9145?',
    'Un R² de 0.9145 significa que el modelo explica el 91.45% de la variabilidad del '
    'consumo eléctrico en el conjunto de prueba. Dicho de otra forma, el modelo comete '
    'un 91.45% menos de error (en términos de varianza) que un modelo naive que siempre '
    'predice el promedio histórico. Para predicción de series de tiempo energéticas, '
    'R² > 0.90 se considera un resultado excelente.')

pregunta_jurado(doc,
    '¿Por qué el R² del escenario diario (0.78) es menor que el de 15 minutos (0.91)?',
    'Hay dos razones principales. Primera: al agregar datos de 15 minutos a valores '
    'diarios, se pierde información intradiaria relevante (picos de mañana, tarde y '
    'noche se promedian en un solo valor). Segunda: el escenario diario tiene solo '
    '1,122 registros de entrenamiento versus 106,714 del de 15 minutos — con menos '
    'datos los modelos tienen más dificultad para aprender todos los patrones. '
    'Un R² de 0.78 sigue siendo un resultado bueno para predicción diaria.')

pregunta_jurado(doc,
    '¿El tuning mejoró mucho los resultados?',
    'El impacto del tuning fue diferente por modelo. RF y XGBoost estaban ya bien '
    'calibrados: la mejora fue marginal (ΔR² < 0.001 en la mayoría de casos). '
    'SVR fue el gran beneficiado: mejoró hasta +0.0474 en el escenario diario, '
    'pasando de R²=0.7374 a R²=0.7848. Esto indica que los parámetros base de SVR '
    'estaban más alejados del óptimo para este tipo de datos. El tuning fue valioso '
    'para confirmar que RF y XGBoost ya estaban bien configurados y para optimizar SVR.')

pregunta_jurado(doc,
    '¿Cuál es la limitación más importante de tu trabajo?',
    'La limitación principal es que los resultados son específicos de UN hogar en '
    'Francia durante 2006-2010. No se puede garantizar que los mismos modelos y '
    'parámetros funcionen igual de bien en otros hogares con diferentes hábitos de '
    'consumo, clima o sistema eléctrico. Además, el pronóstico es de un paso adelante '
    '(h=1): no se evaluó la degradación del rendimiento al predecir múltiples pasos '
    'en el futuro. Finalmente, la variable SM1 (cocina) quedó en cero por el filtro '
    'IQR, perdiendo información de ese sub-medidor.')

pregunta_jurado(doc,
    '¿Cómo se comparan tus resultados con la literatura?',
    'Los resultados son comparables o superiores a estudios similares. En el escenario '
    'de 15 minutos, R²=0.9145 es un resultado excelente. En predicción horaria, '
    'R²=0.8812 está dentro del rango reportado en estudios con el mismo dataset. '
    'El escenario diario con R²=0.7848 es adecuado considerando el tamaño del dataset. '
    'La principal contribución metodológica es la comparación sistemática de los '
    'tres modelos bajo las tres granularidades con el mismo protocolo experimental.')

heading(doc, '10.5 Preguntas adicionales', 2)
pregunta_jurado(doc,
    '¿Qué es el overfitting y cómo lo controlaste?',
    'Overfitting ocurre cuando el modelo aprende demasiado bien los datos de '
    'entrenamiento (incluyendo el ruido) y no generaliza a datos nuevos. Se controla '
    'de varias formas en esta tesis: (1) en RF, con min_samples_leaf que limita la '
    'profundidad de los árboles; (2) en XGBoost, con subsample=0.8 y regularización '
    'L1/L2 incorporada; (3) en SVR, con el parámetro C que controla la penalización; '
    '(4) en todos los modelos, evaluando sobre el conjunto de test que nunca fue visto '
    'durante el entrenamiento.')

pregunta_jurado(doc,
    '¿Por qué usaste la media y no la suma en el resample?',
    'Las variables del dataset son POTENCIAS (kW) — representan la tasa de consumo '
    'en un instante. Al agregar múltiples mediciones en un período, la operación '
    'correcta es el promedio (potencia promedio del período). Si fueran ENERGÍAS '
    '(kWh — ya integradas en el tiempo), se usaría la suma. Los sub-medidores SM1, '
    'SM2 y SM3 sí están en Wh, pero al hacer resample para usarlos como features '
    'también se promedian para mantener consistencia.')

pregunta_jurado(doc,
    '¿Qué harías diferente si tuvieras más tiempo?',
    'Incluiría variables exógenas como temperatura y calendario de festivos, que '
    'tienen gran impacto en el consumo eléctrico. También implementaría modelos de '
    'deep learning (LSTM) para comparación. Revisaría la estrategia de limpieza de '
    'SM1 para preservar esa información. Finalmente, evaluaría el rendimiento con '
    'múltiples horizontes de pronóstico (h=1, h=4, h=8) para entender cómo se '
    'degrada la precisión al predecir más pasos al futuro.')

doc.add_page_break()

# =============================================================================
# SECCIÓN 11 — GLOSARIO
# =============================================================================
heading(doc, '11. GLOSARIO DE TÉRMINOS CLAVE', 1)
add_hr(doc)

terminos = [
    ('Algoritmo de ML', 'Procedimiento matemático que aprende patrones en los datos sin ser '
     'explícitamente programado con reglas. Ejemplos: RF, XGBoost, SVR.'),
    ('Autocorrelación', 'Correlación de una serie temporal consigo misma en diferentes retardos. '
     'Alta autocorrelación significa que el pasado predice bien el futuro.'),
    ('Bagging', 'Bootstrap Aggregating. Técnica de ensemble que entrena múltiples modelos '
     'con submuestras aleatorias con reemplazo. Reduce la varianza.'),
    ('Boosting', 'Técnica de ensemble donde cada modelo corrige los errores del anterior, '
     'construyendo modelos secuencialmente. Reduce el sesgo.'),
    ('Cross-validation', 'Técnica de evaluación que divide los datos en múltiples folds '
     'para obtener una estimación más robusta del rendimiento.'),
    ('Data Leakage', 'Contaminación del entrenamiento con información del futuro. Produce '
     'modelos optimistas que fallan en producción.'),
    ('Ensemble', 'Combinación de múltiples modelos para obtener mejores predicciones que '
     'cualquier modelo individual.'),
    ('Feature', 'Variable de entrada del modelo. También llamada "característica" o "atributo".'),
    ('Feature Engineering', 'Proceso de crear o transformar features para mejorar el '
     'rendimiento del modelo.'),
    ('Feature Importance', 'Medida de cuánto contribuye cada feature a las predicciones '
     'del modelo. En RF: basada en la reducción de impureza. En XGBoost: basada en '
     'la ganancia de los splits.'),
    ('GAP', 'Global Active Power. Potencia activa total del hogar en kW. Variable objetivo.'),
    ('GridSearchCV', 'Búsqueda exhaustiva de hiperparámetros probando todas las combinaciones '
     'posibles, evaluadas por validación cruzada.'),
    ('Hiperparámetro', 'Parámetro de configuración del modelo que no se aprende durante '
     'el entrenamiento (ej: n_estimators, C, epsilon).'),
    ('Horizonte de pronóstico (h)', 'Número de pasos al futuro que predice el modelo. '
     'En esta tesis h=1 en todos los escenarios.'),
    ('IQR', 'Interquartile Range. Diferencia entre Q3 (percentil 75) y Q1 (percentil 25). '
     'Mide la dispersión central de los datos.'),
    ('Kernel RBF', 'Radial Basis Function. Función matemática que transforma datos a '
     'un espacio de mayor dimensión para capturar relaciones no lineales en SVR.'),
    ('Lag', 'Valor retardado de una variable. GAP_lag_3 = GAP de 3 períodos atrás.'),
    ('MAE', 'Mean Absolute Error. Error medio absoluto. Robusto ante outliers.'),
    ('MAPE', 'Mean Absolute Percentage Error. Error relativo expresado en porcentaje.'),
    ('Multicolinealidad', 'Correlación muy alta entre dos o más features. Causa inestabilidad '
     'en los modelos y dificulta interpretar la importancia individual de cada variable.'),
    ('Overfitting', 'Sobreajuste. El modelo aprende el ruido del entrenamiento y no '
     'generaliza a datos nuevos.'),
    ('R²', 'Coeficiente de determinación. Proporción de varianza explicada por el modelo. '
     'Rango teórico: -∞ a 1. Para modelos útiles: 0 a 1.'),
    ('Resample', 'Reagrupación de datos temporales a una frecuencia diferente. En esta '
     'tesis: agregación de 1 minuto a 15min/1h/1día usando la media.'),
    ('RMSE', 'Root Mean Squared Error. Raíz del error cuadrático medio. Penaliza errores grandes.'),
    ('Rolling Window', 'Ventana móvil. Cálculo de estadísticas (media, desviación) sobre '
     'los últimos N períodos.'),
    ('Serie temporal', 'Secuencia de observaciones ordenadas en el tiempo.'),
    ('Split cronológico', 'División train/test que respeta el orden temporal. Los datos '
     'más antiguos son train y los más recientes son test.'),
    ('StandardScaler', 'Escalador que transforma variables para tener media=0 y desviación '
     'estándar=1. Requerido por SVR.'),
    ('Support Vectors', 'Puntos de datos que están en el borde o fuera del margen ε en SVR. '
     'Son los únicos que definen el modelo.'),
    ('SVR', 'Support Vector Regression. Extensión de SVM para regresión. Busca el '
     'hiperplano que deja los errores dentro de un margen ε.'),
    ('TimeSeriesSplit', 'Variante de KFold para series de tiempo. Garantiza que el fold '
     'de validación siempre sea posterior temporalmente al de entrenamiento.'),
    ('Tuning', 'Optimización de hiperparámetros. Proceso de encontrar la mejor configuración '
     'del modelo mediante búsqueda sistemática.'),
    ('XGBoost', 'eXtreme Gradient Boosting. Algoritmo de boosting eficiente con '
     'regularización incorporada. Muy competitivo en datos tabulares.'),
]

for i, (termino, definicion) in enumerate(terminos):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(3)
    if i % 2 == 0:
        shd = OxmlElement('w:shd')
        shd.set(qn('w:val'), 'clear')
        shd.set(qn('w:fill'), 'F5F5F5')
        p._p.get_or_add_pPr().append(shd)
    r1 = p.add_run(termino + ': ')
    r1.bold = True
    r1.font.color.rgb = RGBColor(0x1A, 0x23, 0x7E)
    p.add_run(definicion)

doc.add_page_break()

# =============================================================================
# SECCIÓN 12 — RESUMEN EJECUTIVO PARA LA DEFENSA
# =============================================================================
heading(doc, '12. RESUMEN EJECUTIVO PARA LA DEFENSA', 1)
add_hr(doc)

seccion_alerta(doc, 'Lee este resumen la noche antes de la defensa para refrescar los puntos clave.')

doc.add_paragraph()
heading(doc, 'En una oración: ¿de qué trata tu tesis?', 2)
p = doc.add_paragraph()
p.paragraph_format.left_indent = Cm(0.8)
run = p.add_run(
    '"Se comparan tres algoritmos de machine learning — Random Forest, XGBoost y SVR — '
    'para predecir el consumo eléctrico de un hogar inteligente, evaluando su desempeño '
    'bajo tres granularidades temporales: 15 minutos, 1 hora y 1 día."'
)
run.font.size = Pt(12)
run.font.italic = True
run.font.color.rgb = RGBColor(0x1A, 0x23, 0x7E)

heading(doc, '5 conclusiones que debes saber de memoria:', 2)
conclusiones = [
    'A 15 minutos, Random Forest es el mejor modelo (R²=0.9145, MAPE=14.76%).',
    'A 1 hora, XGBoost es el mejor modelo (R²=0.8812, MAPE=18.42%).',
    'A 1 día, SVR es el mejor modelo (R²=0.7848, MAPE=10.96%).',
    'El tuning benefició principalmente a SVR (hasta +0.0474 en R²). '
    'RF y XGBoost ya estaban bien calibrados.',
    'A mayor granularidad (más datos por período), mayor dificultad de predicción '
    'y menor R². Esto es esperado y consistente con la literatura.',
]
for i, c in enumerate(conclusiones):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.5)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(f'{i+1}. ' + c)
    r.font.size = Pt(11)
    if i < 3:
        r.font.bold = True

heading(doc, '3 decisiones metodológicas que debes poder defender:', 2)
decisiones = [
    ('Split cronológico (no aleatorio)',
     'Para evitar data leakage: el modelo solo aprende del pasado.'),
    ('TimeSeriesSplit en el tuning',
     'Para que la validación cruzada también respete el orden temporal.'),
    ('Submuestreo de SVR',
     'SVR es O(n²~n³): con 106K muestras tardaría horas. Las 15K más recientes '
     'son representativas del comportamiento actual.'),
]
for titulo, explicacion in decisiones:
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.5)
    p.paragraph_format.space_after = Pt(5)
    r1 = p.add_run('• ' + titulo + ': ')
    r1.bold = True
    r1.font.color.rgb = RGBColor(0x1A, 0x23, 0x7E)
    p.add_run(explicacion)

# =============================================================================
# GUARDAR
# =============================================================================
doc.save(OUT_FILE)
print(f'\n{"="*60}')
print('GUÍA DE ESTUDIO GENERADA EXITOSAMENTE')
print(f'{"="*60}')
print(f'\nArchivo: {OUT_FILE}')
print('\nContenido:')
print('  1.  El Dataset (UCI, variables, estadísticas)')
print('  2.  Limpieza de datos (nulos, IQR, GI)')
print('  3.  Granularidades temporales y resample')
print('  4.  Feature Engineering (lags, rolling, temporales)')
print('  5.  Split cronológico train/test')
print('  6.  Modelos ML (RF, XGBoost, SVR) con hiperparámetros')
print('  7.  Métricas de evaluación (RMSE, MAE, MAPE, R²)')
print('  8.  Tuning de hiperparámetros (GridSearchCV + TimeSeriesSplit)')
print('  9.  Resultados y análisis')
print(' 10.  Preguntas probables del jurado con respuestas')
print(' 11.  Glosario de términos clave')
print(' 12.  Resumen ejecutivo para la defensa')
