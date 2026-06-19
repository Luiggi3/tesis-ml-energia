# =============================================================================
# DOCUMENTO FINAL DE TESIS — GENERADOR COMPLETO
# Incluye: EDA, preparación de datos, feature engineering, modelos y resultados
# Todos los números verificados contra los CSV reales del proyecto
# =============================================================================

import os
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

_here    = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = _here if os.path.exists(os.path.join(_here, 'datos')) else os.path.dirname(_here)
OUT_PATH = os.path.join(BASE_DIR, 'Documento_Final_Tesis.docx')
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
    sizes = {1: Pt(16), 2: Pt(13), 3: Pt(12)}
    p = doc.add_heading(level=level)
    p.clear()
    r = p.add_run(text)
    r.font.name  = 'Times New Roman'
    r.font.bold  = True
    r.font.color.rgb = RGBColor(0, 0, 0)
    r.font.size  = sizes.get(level, Pt(12))
    p.alignment  = WD_ALIGN_PARAGRAPH.LEFT
    return p

def para(text, justify=True):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY if justify else WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_after = Pt(6)
    return p

def italic_para(text):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.italic = True
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_after = Pt(4)

fig_counter = [1]

def add_fig(img_subpath, caption_text, intro=None, width=Inches(5.8)):
    img_path = os.path.join(GRAF_DIR, img_subpath)
    if not os.path.exists(img_path):
        print(f'  ⚠ No encontrado: {img_path}')
        return
    if intro:
        italic_para(intro)
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.add_run().add_picture(img_path, width=width)
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cap = p_cap.add_run(f'Figura {fig_counter[0]}. {caption_text}')
    r_cap.font.name = 'Times New Roman'
    r_cap.font.size = Pt(10)
    r_cap.italic = True
    doc.add_paragraph()
    print(f'  ✓ Figura {fig_counter[0]}: {caption_text[:60]}')
    fig_counter[0] += 1

def header_row(table, *cols):
    row = table.rows[0]
    for cell, text in zip(row.cells, cols):
        r = cell.paragraphs[0].add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11)
        r.bold = True

def add_row(table, *vals, bold=False):
    row = table.add_row()
    for cell, text in zip(row.cells, vals):
        r = cell.paragraphs[0].add_run(str(text))
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11)
        r.bold = bold

def new_table(cols, *header_vals):
    t = doc.add_table(rows=1, cols=cols)
    t.style = 'Table Grid'
    header_row(t, *header_vals)
    return t


# =============================================================================
# PORTADA
# =============================================================================
for _ in range(5):
    doc.add_paragraph()

def centered_bold(text, size):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(size)
    r.bold = True
    return p

centered_bold('DOCUMENTO FINAL DE TESIS', 20)
doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('Modelo Predictivo del Consumo Energético en Hogares Inteligentes\nUtilizando Algoritmos de Machine Learning')
r.font.name = 'Times New Roman'; r.font.size = Pt(14)
doc.add_paragraph()
doc.add_paragraph()
p2 = doc.add_paragraph()
p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
r2 = p2.add_run('Dataset: Individual Household Electric Power Consumption (UCI)\nFrancia, 2006–2010 | Random Forest · XGBoost · SVR')
r2.font.name = 'Times New Roman'; r2.font.size = Pt(12)
doc.add_page_break()

# =============================================================================
# CAPÍTULO 1: ANÁLISIS EXPLORATORIO DE DATOS
# =============================================================================
print('\n[1] Análisis Exploratorio de Datos')
heading('1. Análisis Exploratorio de Datos (EDA)', level=1)

para(
    'El análisis exploratorio de datos constituye la primera etapa del proceso de '
    'modelado. Su propósito es entender la estructura, calidad y comportamiento del '
    'dataset antes de aplicar cualquier transformación o modelo predictivo. En esta '
    'tesis se utilizó el dataset Individual Household Electric Power Consumption '
    '(UCI), que registra el consumo eléctrico de un hogar en Francia entre diciembre '
    'de 2006 y noviembre de 2010, con una frecuencia de medición de un minuto.'
)
para(
    'El EDA incluyó análisis de calidad de datos, series temporales, distribuciones '
    'estadísticas, correlaciones, patrones temporales, tratamiento de outliers, '
    'descomposición estacional, autocorrelación y participación de sub-medidores. '
    'A continuación se describe cada análisis junto con sus resultados.'
)

# 1.1 Descripción del Dataset
heading('1.1 Descripción del Dataset', level=2)
para(
    'El dataset original contiene 2.075.259 registros a frecuencia de un minuto, '
    'distribuidos entre el 16 de diciembre de 2006 y el 26 de noviembre de 2010. '
    'Cada registro incluye siete variables eléctricas correspondientes al consumo '
    'del hogar y de sus tres sub-medidores. Las variables fueron renombradas para '
    'facilitar su manejo durante el análisis:'
)
t = new_table(3, 'Variable', 'Unidad', 'Descripción')
for v in [
    ('GAP',  'kW',  'Potencia activa global — variable objetivo a predecir'),
    ('GRP',  'kW',  'Potencia reactiva global'),
    ('VOLT', 'V',   'Voltaje de la red eléctrica'),
    ('GI',   'A',   'Intensidad global de corriente'),
    ('SM1',  'Wh',  'Sub-medidor 1 — Cocina (horno, microondas, lavavajillas)'),
    ('SM2',  'Wh',  'Sub-medidor 2 — Lavandería (lavadora, secadora, refrigerador)'),
    ('SM3',  'Wh',  'Sub-medidor 3 — Calentador de agua y aire acondicionado'),
]:
    add_row(t, *v)
doc.add_paragraph()

# 1.2 Calidad de datos
heading('1.2 Calidad de Datos — Valores Nulos', level=2)
para(
    'Se detectó un 1,252% de valores nulos en el dataset, afectando a todas las '
    'variables de forma simultánea. Esto indica que los nulos corresponden a '
    'períodos completos sin registro (por ejemplo, cortes de medición), no a '
    'errores aislados por variable. Se optó por eliminar directamente las filas '
    'con valores nulos mediante el método dropna(), dado que representan un '
    'porcentaje bajo del total y su imputación introduciría información artificial '
    'en la serie temporal.'
)
add_fig(
    'eda/01_valores_nulos.png',
    'Análisis de valores nulos. Izquierda: porcentaje de nulos por variable (todas '
    'presentan el mismo 1,252%). Derecha: mapa de calor mensual que muestra los '
    'períodos con mayor concentración de datos faltantes.',
    intro='La figura siguiente muestra la distribución de los valores nulos por variable y por período:'
)

# 1.3 Series temporales
heading('1.3 Series Temporales de Variables Eléctricas', level=2)
para(
    'Se graficaron las series temporales de las cuatro variables eléctricas principales '
    '(GAP, GRP, VOLT, GI) y de los tres sub-medidores, promediadas a nivel diario para '
    'facilitar la visualización del comportamiento a largo plazo. Las series revelan '
    'una marcada estacionalidad anual: el consumo de potencia activa (GAP) es '
    'notablemente más alto en invierno (noviembre–febrero) que en verano, lo que es '
    'consistente con el clima de Francia. La variable GI (intensidad) presenta una '
    'trayectoria prácticamente idéntica a GAP, lo que anticipa su alta correlación.'
)
add_fig(
    'eda/02_series_tiempo_principales.png',
    'Series temporales de las variables eléctricas principales (GAP, GRP, VOLT, GI) '
    'expresadas como promedios diarios para el período 2006–2010. Se aprecia claramente '
    'la estacionalidad anual del consumo y la similitud entre GAP y GI.',
    intro='La figura siguiente muestra la evolución temporal de las cuatro variables eléctricas principales:'
)
para(
    'Los tres sub-medidores presentan patrones distintos entre sí. SM3 (calentador/AC) '
    'muestra la mayor estacionalidad invernal, coherente con el uso de calefacción. '
    'SM2 (lavandería) mantiene un nivel relativamente constante durante todo el año. '
    'SM1 (cocina) fue afectado por el tratamiento de outliers, quedando en cero '
    'tras el filtro IQR por tener una distribución muy esparsa (Q1=Q3=0).'
)
add_fig(
    'eda/03_series_submedidores.png',
    'Series temporales de los sub-medidores SM1 (cocina), SM2 (lavandería) y SM3 '
    '(calentador/AC) como promedios diarios. SM3 exhibe la estacionalidad más marcada, '
    'con picos en los meses de invierno.',
    intro='La figura siguiente muestra la evolución de los tres sub-medidores:'
)

# 1.4 Distribuciones
heading('1.4 Distribuciones Estadísticas', level=2)
para(
    'Se analizaron las distribuciones de las siete variables mediante histogramas y '
    'estimación de densidad (KDE). Las variables de potencia (GAP y GRP) presentan '
    'distribuciones asimétricas positivas (sesgo a la derecha), con la mayoría de '
    'los valores concentrados en consumos bajos y una cola extendida hacia consumos '
    'altos. El voltaje (VOLT) muestra una distribución más simétrica y concentrada, '
    'lo cual es esperable en una red eléctrica estable. Los sub-medidores, '
    'especialmente SM1 y SM2, presentan distribuciones muy esparsas con gran '
    'proporción de valores en cero, correspondientes a períodos sin uso de los '
    'electrodomésticos conectados.'
)
add_fig(
    'eda/04_distribuciones.png',
    'Distribuciones de las siete variables eléctricas mediante histograma y curva KDE. '
    'Las líneas verticales indican la media (rojo) y la mediana (naranja). Las variables '
    'de potencia presentan sesgo positivo, mientras que el voltaje muestra una '
    'distribución más simétrica.',
    intro='La figura siguiente muestra la distribución estadística de cada variable:'
)

# 1.5 Correlación
heading('1.5 Análisis de Correlación', level=2)
para(
    'Se calculó la matriz de correlación de Pearson entre todas las variables. '
    'El hallazgo más relevante es la correlación de 0,999 entre GI (intensidad global) '
    'y GAP (potencia activa), lo que indica una relación prácticamente lineal perfecta. '
    'Esto es técnicamente esperable, ya que la potencia activa es el producto del '
    'voltaje por la corriente (con el factor de potencia), y el voltaje es relativamente '
    'constante. Dado que GI no aporta información adicional sobre GAP y puede generar '
    'problemas de multicolinealidad en los modelos, fue eliminada durante el feature '
    'engineering en los tres escenarios. SM3 también presenta correlación moderada con '
    'GAP (≈0,60), lo que indica que el calentador/AC es el sub-medidor con mayor '
    'influencia en el consumo total.'
)
add_fig(
    'eda/05_correlacion.png',
    'Matriz de correlación de Pearson (izquierda) y correlaciones individuales con GAP '
    '(derecha). Destaca la correlación casi perfecta de GI con GAP (0,999), que motivó '
    'su eliminación como predictor en todos los escenarios.',
    intro='La figura siguiente muestra la matriz de correlación y las correlaciones individuales con GAP:'
)

# 1.6 Patrones temporales
heading('1.6 Patrones Temporales del Consumo', level=2)
para(
    'El análisis de patrones temporales permite identificar regularidades en el '
    'comportamiento del consumo eléctrico según la hora del día, el día de la semana, '
    'el mes del año y el año. Estos patrones son la base que justifica la inclusión '
    'de variables temporales en el feature engineering.'
)
para(
    'Por hora del día, el consumo presenta un valle durante la madrugada (2:00–6:00) '
    'y dos picos: uno matutino (7:00–9:00) y uno vespertino/nocturno (17:00–21:00), '
    'que corresponden a los momentos de mayor actividad del hogar. Por día de la '
    'semana, el consumo es ligeramente mayor los fines de semana que durante la '
    'semana laboral, posiblemente por mayor permanencia en el hogar. A nivel mensual, '
    'el consumo es claramente más alto en los meses de invierno (noviembre–febrero) '
    'y más bajo en verano (junio–agosto).'
)
add_fig(
    'eda/06_patrones_temporales.png',
    'Patrones del consumo promedio (GAP) según cuatro dimensiones temporales: hora del '
    'día, día de la semana, mes del año y año. Los días de fin de semana (sábado y '
    'domingo) se destacan en naranja/rojo para facilitar su identificación.',
    intro='La figura siguiente resume los patrones de consumo en las cuatro dimensiones temporales:'
)
add_fig(
    'eda/07_heatmap_hora_dia.png',
    'Mapa de calor del consumo promedio de GAP cruzando hora del día (eje X) con día '
    'de la semana (eje Y). Los colores más intensos indican mayor consumo. Se observa '
    'que las noches de viernes y sábado tienen consumo más elevado y sostenido.',
    intro='El mapa de calor siguiente muestra la interacción entre hora del día y día de la semana:'
)
add_fig(
    'eda/08_boxplot_mensual.png',
    'Distribución mensual del consumo de GAP mediante diagramas de caja. La mediana '
    '(línea roja) y el rango intercuartílico muestran claramente la estacionalidad: '
    'mayor consumo y mayor variabilidad en los meses de invierno.',
    intro='Los boxplots mensuales muestran la distribución del consumo para cada mes del año:'
)

# 1.7 Outliers
heading('1.7 Detección y Tratamiento de Valores Atípicos', level=2)
para(
    'Se aplicó el método IQR (rango intercuartílico) para detectar y eliminar '
    'valores atípicos. Para las variables continuas (GAP, GRP, VOLT, GI) se usó '
    'el criterio estándar de 1,5×IQR. Para las variables esparsas (SM1, SM2, SM3) '
    'se usó el percentil 99,5 como límite superior, ya que su Q1=Q3=0 haría que '
    'el filtro IQR eliminara toda actividad medida. El filtro se aplicó de forma '
    'simultánea a todas las variables: un registro se elimina si cualquiera de sus '
    'valores está fuera del rango permitido. Tras el filtrado, el dataset quedó con '
    '1.739.167 registros (de un total de 2.075.259 originales tras eliminar nulos, '
    'equivalente a eliminar el 16,18% de los registros).'
)
para(
    'Nota metodológica: La variable SM1 (cocina) quedó con valor cero en todas las '
    'filas del dataset limpio. Esto ocurre porque su distribución es extremadamente '
    'esparsa (Q1=Q3=0), y el criterio IQR fija el límite superior en el percentil '
    '99,5. Aunque SM1 permanece en el dataset como variable, no aporta información '
    'discriminante. Esta es una limitación conocida del método IQR en variables '
    'esparsas y se reconoce como tal en el análisis.'
)
add_fig(
    'eda/09_boxplot_antes.png',
    'Diagramas de caja de las siete variables eléctricas antes del tratamiento de '
    'outliers. Se observan valores extremos (puntos grises) en todas las variables, '
    'especialmente en GAP, GRP y GI.',
    intro='La figura siguiente muestra la distribución de cada variable antes del filtro IQR:'
)
add_fig(
    'eda/10_boxplot_despues.png',
    'Diagramas de caja de las siete variables después del tratamiento de outliers con '
    'el método IQR. Los valores extremos fueron eliminados, resultando en distribuciones '
    'más compactas y representativas del comportamiento típico del hogar.',
    intro='La figura siguiente muestra el resultado después de aplicar el filtro IQR:'
)

# 1.8 Descomposición estacional
heading('1.8 Descomposición Estacional', level=2)
para(
    'Se aplicó descomposición estacional aditiva sobre la serie diaria de GAP con '
    'un período de 365 días, utilizando el método de medias móviles de statsmodels. '
    'La descomposición separa la serie en tres componentes: tendencia, estacionalidad '
    'y residuo. La tendencia muestra un leve descenso del consumo hacia los años '
    '2009–2010, posiblemente por cambios en los hábitos del hogar o eficiencia '
    'energética. La componente estacional confirma el patrón anual descrito anteriormente, '
    'con amplitudes de aproximadamente ±0,3 kW respecto a la tendencia. El residuo '
    'es de baja magnitud y sin estructura aparente, lo que sugiere que la mayor '
    'parte de la variación queda capturada por tendencia y estacionalidad.'
)
add_fig(
    'eda/11_descomposicion_estacional.png',
    'Descomposición estacional aditiva de la serie diaria de GAP con período de 365 días. '
    'De arriba hacia abajo: serie original, componente de tendencia, componente estacional '
    'y residuo. La tendencia muestra un descenso gradual del consumo en el período analizado.',
    intro='La figura siguiente presenta la descomposición de la serie temporal en sus componentes:'
)

# 1.9 Autocorrelación
heading('1.9 Análisis de Autocorrelación (ACF y PACF)', level=2)
para(
    'Se calcularon las funciones de autocorrelación (ACF) y autocorrelación parcial '
    '(PACF) sobre la serie horaria de GAP. La ACF con 168 lags (7 días) muestra '
    'correlaciones significativas en múltiplos de 24 horas, lo que confirma una '
    'fuerte estacionalidad diaria. Las correlaciones decaen lentamente, indicando '
    'que el consumo actual depende de valores recientes de forma persistente. La PACF '
    'con 48 lags (2 días) muestra las correlaciones directas descontando el efecto '
    'de los lags intermedios. Estos resultados justifican la selección de lags de '
    '1h, 24h y 168h (1 semana) en el feature engineering del escenario de 1 hora.'
)
add_fig(
    'eda/12_acf_pacf.png',
    'Función de Autocorrelación (ACF, arriba) con 168 lags y Función de Autocorrelación '
    'Parcial (PACF, abajo) con 48 lags, calculadas sobre la serie horaria de GAP. '
    'Las líneas azules punteadas indican los intervalos de confianza al 95%.',
    intro='La figura siguiente muestra las funciones de autocorrelación de la serie horaria de GAP:'
)

# 1.10 Participación sub-medidores
heading('1.10 Participación de Sub-medidores en el Consumo Total', level=2)
para(
    'Se analizó la contribución de cada sub-medidor al consumo energético total del '
    'hogar. SM3 (calentador/AC) es el circuito medido con mayor participación, seguido '
    'de SM2 (lavandería) y SM1 (cocina). Sin embargo, una proporción significativa del '
    'consumo corresponde a "otros circuitos" no monitorizados directamente (iluminación, '
    'televisores, computadoras, etc.). La participación de SM3 varía notablemente a lo '
    'largo del año, siendo mayor en invierno por el uso de calefacción eléctrica.'
)
add_fig(
    'eda/13_submedidores_participacion.png',
    'Participación de los sub-medidores en el consumo total. Izquierda: gráfico de '
    'torta con la distribución porcentual acumulada del período. Derecha: evolución '
    'mensual de la participación relativa de cada sub-medidor, donde se aprecia la '
    'mayor contribución de SM3 en los meses de invierno.',
    intro='La figura siguiente muestra la distribución del consumo por circuito medido:'
)

doc.add_page_break()

# =============================================================================
# CAPÍTULO 2: PREPARACIÓN DE DATOS
# =============================================================================
print('\n[2] Preparación de Datos')
heading('2. Preparación de Datos y Remuestreo', level=1)

para(
    'Tras el análisis exploratorio, se prepararon los datos para el modelado predictivo. '
    'Este proceso incluyó la selección y descripción de variables, el remuestreo a tres '
    'frecuencias temporales distintas (correspondientes a los tres escenarios de predicción) '
    'y la división cronológica del dataset en conjuntos de entrenamiento y prueba.'
)

# 2.1 Variables
heading('2.1 Variables del Dataset Limpio', level=2)
para(
    'El dataset limpio resultante del EDA contiene 1.739.167 registros a frecuencia '
    'de un minuto, con las siguientes siete variables eléctricas. La variable objetivo '
    'a predecir en todos los escenarios es GAP (potencia activa global):'
)
t = new_table(3, 'Variable', 'Unidad', 'Descripción')
for v in [
    ('GAP',  'kW',  'Potencia activa global — variable objetivo'),
    ('GRP',  'kW',  'Potencia reactiva global — variable predictora'),
    ('VOLT', 'V',   'Voltaje de la red — variable predictora'),
    ('GI',   'A',   'Intensidad global — eliminada en los 3 escenarios (correlación 0,999 con GAP)'),
    ('SM1',  'Wh',  'Sub-medidor 1 (cocina) — variable predictora'),
    ('SM2',  'Wh',  'Sub-medidor 2 (lavandería) — variable predictora'),
    ('SM3',  'Wh',  'Sub-medidor 3 (calentador/AC) — variable predictora'),
]:
    add_row(t, *v)
doc.add_paragraph()
para(
    'La variable GI es eliminada en los tres escenarios durante el proceso de feature '
    'engineering, por presentar una correlación de 0,999 con GAP que introduce '
    'multicolinealidad sin agregar información predictiva adicional. Los predictores '
    'base resultantes son: GRP, VOLT, SM1, SM2 y SM3 (5 variables eléctricas).'
)

# 2.2 Remuestreo
heading('2.2 Remuestreo por Escenario', level=2)
para(
    'Cada escenario parte del mismo dataset limpio (1 minuto) y lo agrega a una '
    'frecuencia diferente mediante el promedio de los valores dentro de cada intervalo. '
    'Los registros faltantes dentro del período de integración se propagan como NaN '
    'y se eliminan tras el remuestreo. Los conteos a continuación corresponden '
    'al número de registros disponibles después del feature engineering (lags y '
    'rolling windows introducen NaN en las primeras filas, que luego son eliminadas):'
)
t = new_table(4, 'Escenario', 'Frecuencia', 'Registros (post FE)', 'Observaciones / día')
for v in [
    ('Escenario 1', '15 minutos', '133.489', '96'),
    ('Escenario 2', '1 hora',     '34.007',  '24'),
    ('Escenario 3', '1 día',      '1.433',   '1'),
]:
    add_row(t, *v)
doc.add_paragraph()

# 2.3 División train/test
heading('2.3 División Cronológica Train / Test', level=2)
para(
    'La división del dataset se realizó de forma cronológica en todos los escenarios, '
    'asignando el 80% de las observaciones más antiguas al conjunto de entrenamiento '
    'y el 20% más reciente al conjunto de prueba. Este enfoque respeta la estructura '
    'temporal de los datos y evita la fuga de información futura (data leakage), '
    'que ocurriría si se dividiera aleatoriamente. La siguiente tabla muestra el '
    'desglose exacto por escenario:'
)
t = new_table(4, 'Escenario', 'Total registros', 'Entrenamiento (80%)', 'Prueba (20%)')
for v in [
    ('15 minutos', '133.489', '106.791', '26.698'),
    ('1 hora',     '34.007',  '27.205',  '6.802'),
    ('1 día',      '1.433',   '1.146',   '287'),
]:
    add_row(t, *v)
doc.add_paragraph()

# 2.4 Series por escenario
heading('2.4 Series Temporales por Escenario', level=2)

heading('Escenario 1 — 15 Minutos', level=3)
para(
    'Con 133.489 observaciones en el período completo 2006–2010, el escenario de '
    '15 minutos ofrece la mayor resolución temporal y la mayor cantidad de datos '
    'para el entrenamiento. El conjunto de entrenamiento comprende desde el inicio '
    'del dataset hasta el 80% cronológico, y el conjunto de prueba corresponde al '
    '20% final. La línea vertical roja en la figura indica el corte entre ambos conjuntos.'
)
add_fig(
    'escenario1/e1_01_serie_resampleada.png',
    'Serie temporal de GAP remuestreada a 15 minutos, visualizada como promedio diario '
    'para mejorar la legibilidad. La línea vertical roja indica el inicio del conjunto '
    'de prueba. Se aprecian los patrones estacionales anuales y la separación cronológica '
    'entre entrenamiento (izquierda) y prueba (derecha).',
    intro='La siguiente figura muestra la serie de consumo tras el remuestreo a 15 minutos:'
)

heading('Escenario 2 — 1 Hora', level=3)
para(
    'Con 34.007 observaciones, el escenario horario captura el promedio de 60 '
    'lecturas por período, reduciendo el ruido de corto plazo y produciendo una '
    'serie más estable. Es el escenario con resolución intermedia y equilibra '
    'detalle temporal con volumen de datos manejable.'
)
add_fig(
    'escenario2/e2_01_serie_resampleada.png',
    'Serie temporal de GAP remuestreada a 1 hora, visualizada como promedio diario. '
    'La línea vertical roja indica el inicio del conjunto de prueba. La estacionalidad '
    'anual es claramente visible con mayor suavidad que en el escenario de 15 minutos.',
    intro='La siguiente figura muestra la serie de consumo tras el remuestreo a 1 hora:'
)

heading('Escenario 3 — 1 Día', level=3)
para(
    'Con 1.433 observaciones, el escenario diario es el de menor resolución y menor '
    'volumen de datos. Cada observación representa el promedio de los 1.440 minutos '
    'del día. Este escenario es el más desafiante para los modelos por la escasez '
    'de datos de entrenamiento (1.146 días), pero el de mayor utilidad para '
    'planificación energética a mediano plazo.'
)
add_fig(
    'escenario3/e3_01_serie_resampleada.png',
    'Serie temporal de GAP remuestreada a nivel diario. La línea vertical roja indica '
    'el inicio del conjunto de prueba (últimos 287 días). La estacionalidad anual se '
    'aprecia con mayor claridad en esta resolución, con valores más altos en invierno '
    'y más bajos en verano.',
    intro='La siguiente figura muestra la serie de consumo tras el remuestreo a 1 día:'
)

doc.add_page_break()

# =============================================================================
# CAPÍTULO 3: HORIZONTES DE PREDICCIÓN
# =============================================================================
print('\n[3] Horizontes de Predicción')
heading('3. Horizontes de Predicción', level=1)

para(
    'El horizonte de predicción define la unidad de tiempo para la que el modelo '
    'estima el consumo eléctrico futuro. En esta tesis se evaluaron tres horizontes '
    'distintos, cada uno asociado a un escenario de análisis. La elección de múltiples '
    'horizontes permite evaluar cómo varía el desempeño de los modelos en función '
    'de la resolución temporal requerida y la cantidad de historia disponible.'
)
t = new_table(3, 'Escenario', 'Horizonte de predicción', 'Historia máxima utilizada')
for v in [
    ('Escenario 1', '15 minutos', 'Hasta 24 horas hacia atrás (96 períodos de 15 min)'),
    ('Escenario 2', '1 hora',     'Hasta 1 semana hacia atrás (168 horas)'),
    ('Escenario 3', '1 día',      'Hasta 30 días hacia atrás (~1 mes)'),
]:
    add_row(t, *v)
doc.add_paragraph()

heading('3.1 Escenario 1 — Horizonte de 15 Minutos', level=2)
para(
    'El modelo predice el consumo eléctrico (GAP) para el siguiente cuarto de hora. '
    'Es el horizonte más detallado y preciso de este estudio. Con 96 observaciones '
    'por día, dispone del mayor volumen de datos de entrenamiento y puede capturar '
    'patrones intra-diarios con alta resolución. El rezago más largo utilizado '
    '(GAP_lag_96) equivale a 24 horas de historia, permitiendo al modelo reconocer '
    'el comportamiento del hogar a la misma hora del día anterior.'
)

heading('3.2 Escenario 2 — Horizonte de 1 Hora', level=2)
para(
    'El modelo predice el consumo eléctrico de la próxima hora. Representa un '
    'equilibrio entre detalle temporal y volumen de datos. El rezago más largo '
    '(GAP_lag_168) equivale a una semana completa de historia, lo que permite al '
    'modelo capturar tanto el patrón diario como el comportamiento semanal del hogar '
    '(por ejemplo, distinguir un lunes de un domingo a la misma hora).'
)

heading('3.3 Escenario 3 — Horizonte de 1 Día', level=2)
para(
    'El modelo predice el consumo eléctrico total promedio del día siguiente. Es el '
    'horizonte más general del estudio y el de mayor utilidad práctica para la '
    'planificación energética a mediano plazo (gestión de tarifas, programación de '
    'equipos, etc.). El rezago más largo (GAP_lag_30) equivale a aproximadamente '
    'un mes de historia. Al tener solo 1.146 registros de entrenamiento, este '
    'escenario presenta el mayor desafío estadístico para los modelos.'
)

doc.add_page_break()

# =============================================================================
# CAPÍTULO 4: FEATURE ENGINEERING
# =============================================================================
print('\n[4] Feature Engineering')
heading('4. Feature Engineering', level=1)

para(
    'El feature engineering es el proceso de construir nuevas variables a partir de '
    'los datos originales con el objetivo de entregar al modelo información relevante '
    'para la predicción. Los modelos de machine learning no procesan el tiempo de '
    'forma nativa, por lo que es necesario transformar la dimensión temporal en '
    'columnas numéricas. En esta tesis se construyeron tres tipos de variables para '
    'cada escenario: variables temporales, rezagos (lags) y estadísticas móviles '
    '(rolling windows).'
)
para(
    'La variable GI fue eliminada antes de construir las features en los tres '
    'escenarios, por presentar una correlación de 0,999 con GAP. Los predictores '
    'eléctricos base son GRP, VOLT, SM1, SM2 y SM3 (5 variables). Sobre ellos '
    'se añaden las variables construidas descritas a continuación.'
)

# 4.1 Variables temporales
heading('4.1 Variables Temporales', level=2)
para(
    'Las variables temporales codifican numéricamente la posición de cada observación '
    'en el tiempo. Se construyen a partir del índice de fecha y hora de cada escenario '
    'tras el remuestreo. No se toman del dataset limpio directamente porque el '
    'remuestreo cambia el índice temporal. La tabla siguiente indica qué variables '
    'temporales se usan en cada escenario:'
)
t = new_table(3, 'Variable', 'Descripción', 'Escenarios donde se aplica')
for v in [
    ('hora',       'Hora del día (0 = medianoche, 23 = 23:00)',    'Escenarios 1 y 2'),
    ('dia_semana', 'Día de la semana (0=lunes, 6=domingo)',         'Los 3 escenarios'),
    ('mes',        'Mes del año (1=enero, 12=diciembre)',           'Los 3 escenarios'),
    ('trimestre',  'Trimestre del año (1–4)',                       'Solo Escenario 3'),
    ('dia_anio',   'Día del año (1–365 o 366)',                     'Solo Escenario 3'),
    ('es_finde',   'Variable binaria: 1 si sábado o domingo, 0 si no', 'Los 3 escenarios'),
]:
    add_row(t, *v)
doc.add_paragraph()
para(
    'La variable "hora" no se incluye en el Escenario 3 porque los datos son diarios '
    'y no existe una hora asociada a cada registro. En su lugar se añaden "trimestre" '
    'y "dia_anio" para capturar la estacionalidad a escala mensual y anual.'
)

# 4.2 Escenario 1
heading('4.2 Features del Escenario 1 — 15 Minutos', level=2)
para('Variables temporales: hora, dia_semana, mes, es_finde.')
para('Rezagos de GAP construidos (total: 6 lags):')
t = new_table(2, 'Variable', 'Equivalencia temporal')
for v in [
    ('GAP_lag_1',  'Consumo hace 15 minutos (período inmediatamente anterior)'),
    ('GAP_lag_2',  'Consumo hace 30 minutos'),
    ('GAP_lag_4',  'Consumo hace 1 hora'),
    ('GAP_lag_8',  'Consumo hace 2 horas'),
    ('GAP_lag_12', 'Consumo hace 3 horas'),
    ('GAP_lag_96', 'Consumo hace 24 horas (mismo cuarto de hora del día anterior)'),
]:
    add_row(t, *v)
doc.add_paragraph()
para('Estadísticas móviles de GAP construidas (6 variables: media + desviación para 3 ventanas):')
t = new_table(2, 'Variable', 'Equivalencia temporal')
for v in [
    ('GAP_roll_mean_4  /  GAP_roll_std_4',   'Promedio y desviación de la última hora (4 períodos)'),
    ('GAP_roll_mean_8  /  GAP_roll_std_8',   'Promedio y desviación de las últimas 2 horas'),
    ('GAP_roll_mean_96 /  GAP_roll_std_96',  'Promedio y desviación de las últimas 24 horas'),
]:
    add_row(t, *v)
doc.add_paragraph()
para('Total de features en Escenario 1: 5 eléctricas + 4 temporales + 6 lags + 6 rolling = 21 features.')

# 4.3 Escenario 2
heading('4.3 Features del Escenario 2 — 1 Hora', level=2)
para('Variables temporales: hora, dia_semana, mes, es_finde.')
para('Rezagos de GAP construidos (total: 8 lags):')
t = new_table(2, 'Variable', 'Equivalencia temporal')
for v in [
    ('GAP_lag_1',   'Consumo hace 1 hora'),
    ('GAP_lag_2',   'Consumo hace 2 horas'),
    ('GAP_lag_3',   'Consumo hace 3 horas'),
    ('GAP_lag_6',   'Consumo hace 6 horas'),
    ('GAP_lag_12',  'Consumo hace 12 horas'),
    ('GAP_lag_24',  'Consumo hace 1 día (misma hora del día anterior)'),
    ('GAP_lag_48',  'Consumo hace 2 días'),
    ('GAP_lag_168', 'Consumo hace 1 semana (mismo día y hora de la semana anterior)'),
]:
    add_row(t, *v)
doc.add_paragraph()
para('Estadísticas móviles de GAP construidas (6 variables):')
t = new_table(2, 'Variable', 'Equivalencia temporal')
for v in [
    ('GAP_roll_mean_6   /  GAP_roll_std_6',   'Promedio y desviación de las últimas 6 horas'),
    ('GAP_roll_mean_24  /  GAP_roll_std_24',  'Promedio y desviación del último día'),
    ('GAP_roll_mean_168 /  GAP_roll_std_168', 'Promedio y desviación de la última semana'),
]:
    add_row(t, *v)
doc.add_paragraph()
para('Total de features en Escenario 2: 5 eléctricas + 4 temporales + 8 lags + 6 rolling = 23 features.')

# 4.4 Escenario 3
heading('4.4 Features del Escenario 3 — 1 Día', level=2)
para('Variables temporales: dia_semana, mes, trimestre, dia_anio, es_finde. (Sin "hora" porque los datos son diarios.)')
para('Rezagos de GAP construidos (total: 6 lags):')
t = new_table(2, 'Variable', 'Equivalencia temporal')
for v in [
    ('GAP_lag_1',  'Consumo de ayer'),
    ('GAP_lag_2',  'Consumo de hace 2 días'),
    ('GAP_lag_3',  'Consumo de hace 3 días'),
    ('GAP_lag_7',  'Consumo de hace 1 semana (mismo día de la semana anterior)'),
    ('GAP_lag_14', 'Consumo de hace 2 semanas'),
    ('GAP_lag_30', 'Consumo de hace aproximadamente 1 mes'),
]:
    add_row(t, *v)
doc.add_paragraph()
para('Estadísticas móviles de GAP construidas (6 variables):')
t = new_table(2, 'Variable', 'Equivalencia temporal')
for v in [
    ('GAP_roll_mean_7  /  GAP_roll_std_7',  'Promedio y desviación de la última semana'),
    ('GAP_roll_mean_14 /  GAP_roll_std_14', 'Promedio y desviación de las últimas 2 semanas'),
    ('GAP_roll_mean_30 /  GAP_roll_std_30', 'Promedio y desviación del último mes'),
]:
    add_row(t, *v)
doc.add_paragraph()
para('Total de features en Escenario 3: 5 eléctricas + 5 temporales + 6 lags + 6 rolling = 22 features.')
para(
    'Nota técnica: Las estadísticas móviles se calculan con shift(1) previo al rolling, '
    'lo que garantiza que cada cálculo usa únicamente información del pasado y no incluye '
    'el valor del período actual. Esto evita el data leakage en la construcción de features.'
)

doc.add_page_break()

# =============================================================================
# CAPÍTULO 5: MODELOS Y RESULTADOS
# =============================================================================
print('\n[5] Modelos y Resultados')
heading('5. Modelos y Resultados', level=1)

para(
    'Se evaluaron tres algoritmos de machine learning en cada uno de los tres escenarios: '
    'Random Forest (RF), XGBoost y Support Vector Regression (SVR). Para cada modelo '
    'se realizó primero una evaluación con configuración base (hiperparámetros seleccionados '
    'manualmente) y luego una optimización mediante GridSearchCV con validación cruzada '
    'temporal (TimeSeriesSplit, 3 folds). Todas las evaluaciones se realizaron sobre el '
    'conjunto de prueba (20% cronológico final).'
)

# 5.1 Métricas
heading('5.1 Métricas de Evaluación', level=2)
para('Se utilizaron cuatro métricas para evaluar el desempeño de los modelos:')
t = new_table(2, 'Métrica', 'Descripción')
for v in [
    ('RMSE', 'Raíz del Error Cuadrático Medio — penaliza errores grandes. En kW.'),
    ('MAE',  'Error Absoluto Medio — promedio de los errores absolutos. En kW.'),
    ('MAPE', 'Error Porcentual Absoluto Medio — error relativo al valor real. En %.'),
    ('R²',   'Coeficiente de determinación — proporción de varianza explicada (0 a 1).'),
]:
    add_row(t, *v)
doc.add_paragraph()
para(
    'El cálculo del MAPE excluye registros donde el valor real es menor a 0,01 kW '
    'para evitar divisiones por valores cercanos a cero que distorsionarían el '
    'resultado. El R² es la métrica principal de comparación entre modelos.'
)

# 5.2 Descripción modelos
heading('5.2 Descripción de los Modelos', level=2)

heading('Random Forest (RF)', level=3)
para(
    'Random Forest es un modelo de ensamble que construye múltiples árboles de '
    'decisión de forma independiente sobre submuestras aleatorias del dataset y '
    'promedia sus predicciones. Su fortaleza reside en la robustez ante datos '
    'ruidosos, la capacidad para capturar relaciones no lineales y la resistencia '
    'al sobreajuste. No requiere escalado previo de los datos. Los hiperparámetros '
    'principales son el número de árboles (n_estimators), la profundidad máxima '
    '(max_depth) y el mínimo de muestras por hoja (min_samples_leaf).'
)

heading('XGBoost', level=3)
para(
    'XGBoost es un modelo de ensamble basado en gradient boosting, donde cada árbol '
    'se construye para corregir los errores del árbol anterior. Es conocido por su '
    'alta precisión, eficiencia computacional y capacidad de regularización. No '
    'requiere escalado de datos. Los hiperparámetros clave son el número de árboles, '
    'la profundidad máxima, la tasa de aprendizaje (learning_rate) y la proporción '
    'de muestras por árbol (subsample).'
)

heading('Support Vector Regression (SVR)', level=3)
para(
    'SVR es una extensión de las máquinas de soporte vectorial para regresión. Busca '
    'una función que se ajuste a los datos dentro de un margen de tolerancia epsilon, '
    'maximizando el margen entre la función y los puntos de soporte. Utiliza el '
    'kernel RBF (radial basis function) para capturar relaciones no lineales. '
    'Requiere escalado previo de los datos (StandardScaler aplicado a X e y). '
    'Por su alto costo computacional en datasets grandes, se limitó el conjunto '
    'de entrenamiento de SVR a las últimas 15.000 muestras en el Escenario 1 y '
    'a las últimas 10.000 en el Escenario 2.'
)

# 5.3 Resultados base
heading('5.3 Resultados con Configuración Base', level=2)
para(
    'La siguiente tabla presenta los resultados obtenidos con la configuración base '
    'de cada modelo (hiperparámetros seleccionados manualmente, previo al tuning). '
    'Todos los valores provienen del conjunto de prueba (20% cronológico final):'
)
t = new_table(6, 'Escenario', 'Modelo', 'RMSE', 'MAE', 'MAPE', 'R²')
for v in [
    ('15 minutos', 'Random Forest', '0,2013', '0,1194', '14,79%', '0,9144'),
    ('15 minutos', 'XGBoost',       '0,1949', '0,1181', '14,89%', '0,9198'),
    ('15 minutos', 'SVR',           '0,2585', '0,1701', '24,25%', '0,8589'),
    ('1 hora',     'Random Forest', '0,2200', '0,1431', '17,43%', '0,8751'),
    ('1 hora',     'XGBoost',       '0,2146', '0,1385', '16,98%', '0,8812'),
    ('1 hora',     'SVR',           '0,2478', '0,1644', '20,56%', '0,8415'),
    ('1 día',      'Random Forest', '0,1253', '0,0943', '11,48%', '0,7313'),
    ('1 día',      'XGBoost',       '0,1140', '0,0818', '9,69%',  '0,7776'),
    ('1 día',      'SVR',           '0,1238', '0,0865', '10,25%', '0,7374'),
]:
    add_row(t, *v)
doc.add_paragraph()

# Resultados y gráficos por escenario
heading('Escenario 1 — 15 Minutos', level=3)
para(
    'En el escenario de 15 minutos, Random Forest (R²=0,9144) y XGBoost (R²=0,9198) '
    'obtienen resultados muy similares y superiores al 91% de varianza explicada. '
    'SVR muestra un desempeño menor (R²=0,8589) en su configuración base, con un '
    'MAPE de 24,25% que es considerablemente más alto que los otros dos modelos.'
)
add_fig(
    'escenario1/e1_02_predicciones.png',
    'Predicciones vs valores reales de GAP para los primeros 500 puntos del conjunto '
    'de prueba (Escenario 1, 15 minutos). Los tres modelos siguen de cerca la serie '
    'real, siendo XGBoost y Random Forest los que menor desviación presentan.',
    intro='La figura siguiente compara las predicciones de los tres modelos contra los valores reales:'
)
add_fig(
    'escenario1/e1_03_scatter.png',
    'Gráficos de dispersión (predicho vs real) para los tres modelos en el Escenario 1. '
    'Un modelo perfecto mostraría todos los puntos sobre la línea diagonal. XGBoost '
    'y Random Forest muestran la nube de puntos más concentrada alrededor de la '
    'diagonal, mientras SVR presenta mayor dispersión.',
    intro='Los gráficos de dispersión siguientes muestran la relación entre valores predichos y reales:'
)
add_fig(
    'escenario1/e1_04_metricas.png',
    'Comparación de las cuatro métricas (RMSE, MAE, MAPE, R²) para los tres modelos '
    'en el Escenario 1. XGBoost lidera en RMSE y R², mientras Random Forest es muy '
    'competitivo. SVR queda rezagado especialmente en MAPE.',
    intro='La figura siguiente muestra la comparación de métricas entre los tres modelos:'
)
add_fig(
    'escenario1/e1_05_importancia.png',
    'Importancia de las 15 features principales para Random Forest y XGBoost en el '
    'Escenario 1. Los rezagos recientes de GAP (lag_1, lag_2) y las medias móviles '
    '(roll_mean_96) dominan en ambos modelos, confirmando que el consumo reciente '
    'es el predictor más potente.',
    intro='La figura siguiente muestra las 15 features más importantes según Random Forest y XGBoost:'
)

heading('Escenario 2 — 1 Hora', level=3)
para(
    'En el escenario de 1 hora, XGBoost lidera con R²=0,8812 y MAPE de 16,98%. '
    'Random Forest obtiene R²=0,8751, muy cercano. SVR mejora relativamente frente '
    'al escenario anterior (R²=0,8415), aunque mantiene el mayor error relativo '
    'entre los tres modelos con un MAPE de 20,56%.'
)
add_fig(
    'escenario2/e2_02_predicciones.png',
    'Predicciones vs valores reales de GAP para los primeros 500 puntos del conjunto '
    'de prueba (Escenario 2, 1 hora). Los modelos capturan bien los picos y valles '
    'del consumo horario, con mayor suavidad que en el escenario de 15 minutos.',
    intro='La figura siguiente compara las predicciones de los tres modelos en el Escenario 2:'
)
add_fig(
    'escenario2/e2_03_scatter.png',
    'Gráficos de dispersión (predicho vs real) para los tres modelos en el Escenario 2. '
    'Los tres modelos muestran buena concentración alrededor de la diagonal, con '
    'XGBoost y Random Forest presentando menor dispersión que SVR.',
    intro='Los gráficos de dispersión siguientes corresponden al Escenario 2:'
)
add_fig(
    'escenario2/e2_04_metricas.png',
    'Comparación de métricas para los tres modelos en el Escenario 2. XGBoost lidera '
    'en R² y RMSE, mientras Random Forest y XGBoost presentan valores muy similares. '
    'SVR muestra el mayor MAPE (20,56%).',
    intro='La figura siguiente compara las métricas entre los tres modelos en el Escenario 2:'
)
add_fig(
    'escenario2/e2_05_importancia.png',
    'Importancia de las 15 features principales para Random Forest y XGBoost en el '
    'Escenario 2. El rezago de 1 hora (GAP_lag_1) y el rezago de 24 horas (GAP_lag_24) '
    'son los más relevantes, lo que confirma la importancia del valor reciente y '
    'del patrón diario.',
    intro='La figura siguiente muestra la importancia de features en el Escenario 2:'
)

heading('Escenario 3 — 1 Día', level=3)
para(
    'En el escenario diario, XGBoost obtiene el mejor R² base (0,7776) seguido de '
    'SVR (0,7374) y Random Forest (0,7313). Los tres modelos presentan MAPE por '
    'debajo del 12%, con XGBoost alcanzando 9,69%. El menor R² respecto a los otros '
    'escenarios refleja la mayor dificultad de predecir el consumo diario con solo '
    '1.146 registros de entrenamiento.'
)
add_fig(
    'escenario3/e3_02_predicciones.png',
    'Predicciones vs valores reales de GAP para el conjunto de prueba completo '
    '(287 días) en el Escenario 3. Los tres modelos siguen la tendencia general, '
    'aunque con mayor error absoluto en los picos de consumo invernal.',
    intro='La figura siguiente muestra las predicciones sobre el conjunto de prueba completo:'
)
add_fig(
    'escenario3/e3_03_scatter.png',
    'Gráficos de dispersión (predicho vs real) para los tres modelos en el Escenario 3. '
    'La menor concentración alrededor de la diagonal (respecto a los escenarios anteriores) '
    'refleja la mayor dificultad de la predicción diaria con datos limitados.',
    intro='Los gráficos de dispersión siguientes corresponden al Escenario 3:'
)
add_fig(
    'escenario3/e3_04_metricas.png',
    'Comparación de métricas para los tres modelos en el Escenario 3. XGBoost lidera '
    'en todas las métricas en la configuración base. El RMSE más bajo de este escenario '
    '(~0,11–0,12 kW) se explica porque los valores diarios son promedios y tienen '
    'menor variabilidad que las series de mayor frecuencia.',
    intro='La figura siguiente compara las métricas entre los tres modelos en el Escenario 3:'
)
add_fig(
    'escenario3/e3_05_importancia.png',
    'Importancia de las features para Random Forest y XGBoost en el Escenario 3. '
    'El rezago de 1 día (GAP_lag_1) domina ampliamente, seguido de las medias '
    'móviles de 7 y 14 días. Las variables temporales (mes, dia_anio) también '
    'contribuyen de forma relevante, capturando la estacionalidad anual.',
    intro='La figura siguiente muestra la importancia de features en el Escenario 3:'
)

doc.add_page_break()

# =============================================================================
# CAPÍTULO 6: AJUSTE DE HIPERPARÁMETROS
# =============================================================================
print('\n[6] Ajuste de Hiperparámetros')
heading('6. Ajuste de Hiperparámetros (GridSearchCV)', level=1)

para(
    'Para optimizar el desempeño de los modelos se aplicó GridSearchCV con validación '
    'cruzada temporal (TimeSeriesSplit, 3 folds) sobre el conjunto de entrenamiento. '
    'El uso de TimeSeriesSplit garantiza que en cada fold la validación siempre sea '
    'posterior al entrenamiento, respetando la naturaleza temporal de los datos. '
    'La métrica de optimización fue R².'
)
para(
    'Para los Escenarios 1 y 2, donde el volumen de datos es grande, RF y XGBoost '
    'fueron entrenados durante el GridSearch sobre las últimas 30.000 y todas las '
    'muestras del train respectivamente. SVR se limitó a 15.000 muestras (Esc. 1) '
    'y 10.000 (Esc. 2) por costo computacional.'
)

heading('6.1 Espacios de Búsqueda', level=2)
t = new_table(3, 'Modelo', 'Hiperparámetro', 'Valores evaluados')
for v in [
    ('Random Forest', 'n_estimators',     '100, 200, 300'),
    ('Random Forest', 'max_depth',        '10, 20, None'),
    ('Random Forest', 'min_samples_leaf', '1, 5, 10'),
    ('XGBoost',       'n_estimators',     '100, 200'),
    ('XGBoost',       'max_depth',        '4, 6, 8'),
    ('XGBoost',       'learning_rate',    '0,05, 0,10'),
    ('XGBoost',       'subsample',        '0,8, 1,0'),
    ('SVR',           'C',                '1, 10, 100'),
    ('SVR',           'epsilon',          '0,01, 0,05, 0,10'),
    ('SVR',           'gamma',            'scale, 0,01'),
]:
    add_row(t, *v)
doc.add_paragraph()

heading('6.2 Mejores Hiperparámetros por Escenario', level=2)
t = new_table(3, 'Escenario', 'Modelo', 'Mejores hiperparámetros (tuned)')
for v in [
    ('15 min', 'Random Forest', 'n_estimators=200, max_depth=None, min_samples_leaf=5'),
    ('15 min', 'XGBoost',       'n_estimators=100, max_depth=6, lr=0,05, subsample=1,0'),
    ('15 min', 'SVR',           'C=1, epsilon=0,05, gamma=scale'),
    ('1 hora', 'Random Forest', 'n_estimators=300, max_depth=20, min_samples_leaf=1'),
    ('1 hora', 'XGBoost',       'n_estimators=200, max_depth=6, lr=0,05, subsample=0,8'),
    ('1 hora', 'SVR',           'C=1, epsilon=0,05, gamma=0,01'),
    ('1 día',  'Random Forest', 'n_estimators=200, max_depth=20, min_samples_leaf=5'),
    ('1 día',  'XGBoost',       'n_estimators=100, max_depth=4, lr=0,05, subsample=0,8'),
    ('1 día',  'SVR',           'C=1, epsilon=0,05, gamma=0,01'),
]:
    add_row(t, *v)
doc.add_paragraph()

heading('6.3 Resultados tras el Ajuste de Hiperparámetros', level=2)
para('La siguiente tabla compara el R² base y el R² tras el tuning para cada modelo y escenario:')
t = new_table(5, 'Escenario', 'Modelo', 'R² Base', 'R² Tuned', 'ΔR²')
for v in [
    ('15 min', 'Random Forest', '0,9144', '0,9145', '+0,0001'),
    ('15 min', 'XGBoost',       '0,9198', '0,9131', '−0,0067'),
    ('15 min', 'SVR',           '0,8589', '0,8801', '+0,0212'),
    ('1 hora', 'Random Forest', '0,8751', '0,8754', '+0,0003'),
    ('1 hora', 'XGBoost',       '0,8812', '0,8812', '+0,0000'),
    ('1 hora', 'SVR',           '0,8415', '0,8580', '+0,0165'),
    ('1 día',  'Random Forest', '0,7313', '0,7276', '−0,0037'),
    ('1 día',  'XGBoost',       '0,7776', '0,7748', '−0,0028'),
    ('1 día',  'SVR',           '0,7374', '0,7848', '+0,0474'),
]:
    add_row(t, *v)
doc.add_paragraph()

para('La siguiente tabla presenta las métricas completas tras el tuning:')
t = new_table(6, 'Escenario', 'Modelo', 'RMSE', 'MAE', 'MAPE', 'R²')
for v in [
    ('15 min', 'Random Forest', '0,2012', '0,1193', '14,76%', '0,9145'),
    ('15 min', 'XGBoost',       '0,2028', '0,1233', '16,04%', '0,9131'),
    ('15 min', 'SVR',           '0,2383', '0,1554', '22,25%', '0,8801'),
    ('1 hora', 'Random Forest', '0,2197', '0,1434', '17,61%', '0,8754'),
    ('1 hora', 'XGBoost',       '0,2146', '0,1385', '16,98%', '0,8812'),
    ('1 hora', 'SVR',           '0,2346', '0,1501', '17,75%', '0,8580'),
    ('1 día',  'Random Forest', '0,1261', '0,0950', '11,61%', '0,7276'),
    ('1 día',  'XGBoost',       '0,1147', '0,0832', '9,90%',  '0,7748'),
    ('1 día',  'SVR',           '0,1121', '0,0804', '9,66%',  '0,7848'),
]:
    add_row(t, *v)
doc.add_paragraph()

add_fig(
    'tuning/comparacion_r2.png',
    'Comparación de R² antes (Base) y después (Tuned) del ajuste de hiperparámetros, '
    'para los tres escenarios. Se observa que RF y XGBoost muestran cambios mínimos '
    'tras el tuning, mientras SVR presenta las mejoras más importantes.',
    intro='La figura siguiente compara el R² base vs tuned para cada escenario y modelo:'
)
add_fig(
    'tuning/comparacion_rmse.png',
    'Comparación de RMSE antes y después del tuning. SVR reduce su RMSE de forma '
    'notable en los tres escenarios, mientras RF y XGBoost presentan cambios marginales.',
    intro='La figura siguiente compara el RMSE base vs tuned:'
)
add_fig(
    'tuning/comparacion_mape.png',
    'Comparación de MAPE antes y después del tuning. SVR es el modelo que más reduce '
    'su error porcentual, especialmente en el Escenario 2 (de 20,56% a 17,75%).',
    intro='La figura siguiente compara el MAPE base vs tuned:'
)
add_fig(
    'tuning/mejora_delta_r2.png',
    'Mejora neta de R² (ΔR² = Tuned − Base) por modelo y escenario. Las barras '
    'positivas indican mejora tras el tuning y las negativas una leve degradación. '
    'SVR es el modelo más beneficiado en todos los escenarios. RF y XGBoost, que '
    'ya tenían una configuración base cercana a la óptima, presentan cambios mínimos.',
    intro='La figura siguiente muestra la mejora neta de R² atribuible al ajuste de hiperparámetros:'
)

doc.add_page_break()

# =============================================================================
# CAPÍTULO 7: ANÁLISIS COMPARATIVO
# =============================================================================
print('\n[7] Análisis Comparativo')
heading('7. Análisis Comparativo entre Escenarios y Modelos', level=1)

para(
    'En este capítulo se comparan de forma conjunta los resultados de los nueve '
    'modelos (3 algoritmos × 3 escenarios) en su configuración tuned, con el objetivo '
    'de identificar patrones generales, determinar el mejor modelo por escenario y '
    'extraer conclusiones sobre el efecto del horizonte de predicción en el desempeño.'
)

add_fig(
    'comparativos/01_metricas_tuned_barras.png',
    'Comparación de las cuatro métricas (RMSE, MAE, MAPE, R²) en su versión tuned '
    'para los nueve modelos evaluados, agrupados por escenario. Permite visualizar '
    'qué modelo destaca en cada métrica y escenario simultáneamente.',
    intro='La figura siguiente compara todas las métricas tuned de forma conjunta para los tres escenarios:'
)
add_fig(
    'comparativos/02_heatmap_metricas.png',
    'Mapa de calor de las métricas tuned por modelo y escenario. Los colores permiten '
    'identificar rápidamente qué combinación escenario-modelo produce los mejores '
    'resultados en cada métrica. El Escenario 1 (15 min) domina en R², mientras '
    'el Escenario 3 (1 día) presenta los RMSE y MAE más bajos en valor absoluto.',
    intro='El mapa de calor siguiente facilita la comparación visual de todas las métricas:'
)
add_fig(
    'comparativos/03_base_vs_tuned_r2_rmse.png',
    'Comparación directa de R² y RMSE antes y después del tuning para los nueve modelos. '
    'Permite evaluar el impacto real del ajuste de hiperparámetros en cada combinación '
    'modelo-escenario.',
    intro='La figura siguiente muestra el cambio de R² y RMSE atribuible al tuning:'
)
add_fig(
    'comparativos/04_radar_modelos.png',
    'Gráfico de radar (araña) que compara los tres modelos en su configuración tuned '
    'sobre múltiples métricas de forma simultánea. Facilita la identificación de '
    'fortalezas y debilidades relativas de cada algoritmo.',
    intro='El gráfico radar siguiente compara los tres modelos en múltiples dimensiones:'
)
add_fig(
    'comparativos/05_tabla_mejor_modelo.png',
    'Resumen visual del mejor modelo por escenario y por métrica. Permite identificar '
    'de forma rápida cuál algoritmo lidera en cada combinación.',
    intro='La figura siguiente resume el mejor modelo identificado por escenario y métrica:'
)
add_fig(
    'comparativos/06_evolucion_r2.png',
    'Evolución del R² a través de los tres escenarios para cada modelo. Se observa '
    'la degradación del desempeño al aumentar el horizonte de predicción (de 15 min '
    'a 1 día), y cómo los tres modelos siguen tendencias similares aunque con '
    'magnitudes distintas.',
    intro='La figura siguiente muestra cómo varía el R² de cada modelo a través de los tres escenarios:'
)

doc.add_page_break()

# =============================================================================
# CAPÍTULO 8: CONCLUSIONES
# =============================================================================
print('\n[8] Conclusiones')
heading('8. Conclusiones', level=1)

heading('8.1 Conclusiones por Escenario', level=2)

heading('Escenario 1 — 15 Minutos', level=3)
para(
    'XGBoost y Random Forest obtienen los mejores resultados con R² superior a 0,91 '
    'en la configuración base, explicando más del 91% de la variabilidad del consumo. '
    'Tras el ajuste de hiperparámetros, Random Forest es el mejor modelo tuned con '
    'R²=0,9145. SVR mejora notablemente con el tuning (+0,0212 en R²), pasando de '
    'R²=0,8589 a R²=0,8801. La alta disponibilidad de datos (106.791 registros de '
    'entrenamiento) y los patrones repetitivos a nivel de cuarto de hora favorecen '
    'el aprendizaje de los modelos.'
)

heading('Escenario 2 — 1 Hora', level=3)
para(
    'XGBoost lidera con R²=0,8812, sin cambio perceptible tras el tuning (ΔR²=0,0000), '
    'lo que indica que su configuración base ya era óptima. Random Forest obtiene '
    'R²=0,8754 tuned, muy cercano a XGBoost. SVR mejora con el ajuste de '
    'hiperparámetros (+0,0165 en R²). El mejor modelo tuned es XGBoost con R²=0,8812.'
)

heading('Escenario 3 — 1 Día', level=3)
para(
    'SVR es el modelo más beneficiado por el ajuste de hiperparámetros en este '
    'escenario (+0,0474 en R²), convirtiéndose en el mejor modelo tuned con '
    'R²=0,7848 y MAPE de 9,66%. Random Forest y XGBoost disminuyen levemente '
    'tras el tuning (−0,0037 y −0,0028 respectivamente), lo que sugiere que ya '
    'habían alcanzado su límite con la configuración base. El menor desempeño '
    'general de este escenario refleja la dificultad de predecir con solo 1.146 '
    'registros de entrenamiento.'
)

heading('8.2 Conclusión General', level=2)
para(
    'A mayor granularidad temporal (menor horizonte de predicción), los modelos '
    'obtienen mejores resultados. El escenario de 15 minutos alcanza el mejor '
    'desempeño global (R²≈0,91), gracias a su mayor volumen de datos y a los '
    'patrones más repetitivos y predecibles que presenta el consumo a esa escala. '
    'El escenario diario, con R²≈0,78, representa el horizonte de mayor utilidad '
    'práctica para la planificación energética a mediano plazo, a pesar de ser el '
    'más desafiante por la escasez de datos de entrenamiento.'
)
para(
    'SVR es el modelo que más se beneficia del ajuste de hiperparámetros en todos '
    'los escenarios, mientras que Random Forest y XGBoost ya presentaban una '
    'configuración base cercana a la óptima. XGBoost destaca como el algoritmo '
    'más consistente, liderando en los escenarios de 15 minutos (base) y 1 hora '
    '(base y tuned). Para el escenario diario, SVR tuned es la mejor opción.'
)

t = new_table(3, 'Escenario', 'Mejor modelo (tuned)', 'R² tuned')
for v in [
    ('15 minutos', 'Random Forest', '0,9145'),
    ('1 hora',     'XGBoost',       '0,8812'),
    ('1 día',      'SVR',           '0,7848'),
]:
    add_row(t, *v)
doc.add_paragraph()

# =============================================================================
# GUARDAR
# =============================================================================
print(f'\nGuardando documento...')
doc.save(OUT_PATH)
print(f'✓ Documento final generado: {OUT_PATH}')
print(f'  Figuras incluidas: {fig_counter[0] - 1}')
