# =============================================================================
# DOCUMENTO DE EXPOSICIÓN PARA TUTOR
# Narración en primera persona como expositor, basada en Documento_Final_Tesis
# =============================================================================

import os
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

_here    = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = _here if os.path.exists(os.path.join(_here, 'datos')) else os.path.dirname(_here)
OUT_PATH = os.path.join(BASE_DIR, 'Exposicion_Tutor.docx')

doc = Document()

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
    p.paragraph_format.space_after = Pt(8)
    return p

def nota(text):
    p = doc.add_paragraph()
    r = p.add_run('📌 ' + text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    r.italic = True
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.left_indent = Cm(1)
    p.paragraph_format.space_after = Pt(8)
    return p

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
for _ in range(4):
    doc.add_paragraph()

def centered(text, size, bold=True):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(size)
    r.bold = bold
    return p

centered('EXPOSICIÓN DE TESIS PARA EL TUTOR', 18)
doc.add_paragraph()
centered('Modelo Predictivo del Consumo Energético\nen Hogares Inteligentes\nUtilizando Algoritmos de Machine Learning', 14)
doc.add_paragraph()
centered('Narración guiada — Documento de apoyo para la presentación', 11, bold=False)
doc.add_paragraph()
centered('Dataset: Individual Household Electric Power Consumption (UCI)\nFrancia, 2006–2010', 11, bold=False)
doc.add_page_break()


# =============================================================================
# INTRODUCCIÓN — APERTURA DE LA EXPOSICIÓN
# =============================================================================
heading('1. Introducción y Presentación del Tema')

para(
    'Buenos días / buenas tardes. Mi nombre es Luiggi Ubilla y el trabajo de tesis que voy a presentarle '
    'lleva por título "Modelo Predictivo del Consumo Energético en Hogares Inteligentes Utilizando '
    'Algoritmos de Machine Learning". A continuación le voy a explicar, paso a paso, todo lo que '
    'desarrollamos: desde la obtención y análisis de los datos, hasta los resultados finales de los '
    'modelos predictivos y las conclusiones que obtuvimos.'
)

para(
    'El punto de partida de este trabajo es una pregunta práctica y relevante: ¿es posible predecir '
    'con precisión cuánta energía eléctrica va a consumir un hogar en el próximo cuarto de hora, '
    'en la próxima hora o en el próximo día, utilizando únicamente el historial de consumo y '
    'algunas variables temporales? Esta capacidad de predicción tiene aplicaciones directas en la '
    'gestión eficiente de la energía, la optimización de tarifas y la planificación de sistemas '
    'de energías renovables.'
)

para(
    'Para responder esta pregunta, trabajamos con un dataset público y bien documentado del repositorio '
    'UCI Machine Learning Repository, y evaluamos tres algoritmos de machine learning ampliamente '
    'utilizados en la literatura de series temporales: Random Forest, XGBoost y Support Vector '
    'Regression (SVR). Los evaluamos bajo tres escenarios de predicción con distintos horizontes '
    'temporales: cada 15 minutos, cada hora y cada día.'
)

nota('Punto clave para el tutor: El trabajo cubre el ciclo completo de un proyecto de ML — desde '
     'la exploración de datos hasta el ajuste de hiperparámetros y el análisis comparativo de resultados.')

doc.add_page_break()


# =============================================================================
# CAPÍTULO 2 — EL DATASET
# =============================================================================
heading('2. El Dataset: Origen, Estructura y Variables')

para(
    'El dataset que utilizamos se llama "Individual Household Electric Power Consumption" y fue '
    'publicado por el repositorio UCI Machine Learning Repository. Registra el consumo eléctrico '
    'de un único hogar en Francia durante casi cuatro años, desde diciembre de 2006 hasta '
    'noviembre de 2010, con una frecuencia de medición de un minuto. En total, el dataset '
    'original contiene 2.075.259 registros y 7 variables numéricas.'
)

para(
    'Para facilitar el manejo durante el análisis, renombramos las variables originales con '
    'nombres más cortos y descriptivos. La variable más importante es GAP, que representa la '
    'potencia activa global del hogar en kilovatios y es la variable que vamos a predecir '
    'en todos los escenarios. Las demás variables funcionan como predictores:'
)

t = new_table(3, 'Variable', 'Unidad', 'Descripción')
for v in [
    ('GAP',  'kW',  'Potencia activa global — VARIABLE OBJETIVO a predecir'),
    ('GRP',  'kW',  'Potencia reactiva global — predictor'),
    ('VOLT', 'V',   'Voltaje de la red eléctrica — predictor'),
    ('GI',   'A',   'Intensidad global de corriente — predictor (eliminado luego)'),
    ('SM1',  'Wh',  'Sub-medidor 1: Cocina (horno, microondas, lavavajillas)'),
    ('SM2',  'Wh',  'Sub-medidor 2: Lavandería (lavadora, secadora, refrigerador)'),
    ('SM3',  'Wh',  'Sub-medidor 3: Calentador de agua y aire acondicionado'),
]:
    add_row(t, *v)
doc.add_paragraph()

para(
    'Los tres sub-medidores (SM1, SM2, SM3) nos permiten conocer el consumo parcial de los '
    'principales circuitos del hogar, lo cual es útil para entender qué aparatos contribuyen '
    'más al consumo total. El consumo restante, que no está medido por ninguno de los tres '
    'sub-medidores, corresponde a circuitos secundarios como iluminación, televisores y '
    'computadoras.'
)

nota('Si el tutor pregunta por qué este dataset: Es ampliamente usado en la literatura de '
     'predicción energética, está bien documentado, tiene alta granularidad temporal (1 minuto) '
     'y una duración de casi 4 años, lo que permite analizar estacionalidad anual.')

doc.add_page_break()


# =============================================================================
# CAPÍTULO 3 — ANÁLISIS EXPLORATORIO DE DATOS (EDA)
# =============================================================================
heading('3. Análisis Exploratorio de Datos (EDA)')

para(
    'Antes de construir cualquier modelo, realizamos un análisis exploratorio exhaustivo del '
    'dataset. El objetivo de esta etapa es entender la estructura, calidad y comportamiento de '
    'los datos, para tomar decisiones informadas en las etapas posteriores de limpieza, '
    'transformación y modelado. Este análisis está completamente documentado en el archivo '
    'EDA.py y produce 13 gráficos de resultados.'
)

heading('3.1 Calidad de Datos — Valores Nulos', level=2)

para(
    'Lo primero que revisamos fue la calidad de los datos. Encontramos que el 1,252% de '
    'los registros contenían valores nulos, y un hecho importante es que los nulos aparecen '
    'en todas las variables al mismo tiempo. Esto nos indica que no son errores de medición '
    'aislados, sino períodos completos sin registro — por ejemplo, cortes en el sistema de '
    'medición. Por esa razón, decidimos eliminarlos directamente con dropna(), ya que '
    'imputarlos habría introducido información artificial en la serie temporal.'
)

nota('Si el tutor pregunta por qué no se imputaron los nulos: Porque los nulos son bloques '
     'completos de tiempo sin medición, no valores aislados. Imputarlos habría inventado '
     'datos de consumo para períodos que en realidad no fueron registrados.')

heading('3.2 Análisis de las Series Temporales', level=2)

para(
    'A continuación graficamos la evolución temporal de todas las variables. El hallazgo más '
    'relevante es la marcada estacionalidad anual del consumo: la potencia activa (GAP) es '
    'notablemente más alta en los meses de invierno —noviembre a febrero— que en verano. '
    'Esto es completamente coherente con el clima de Francia, donde en invierno se necesita '
    'calefacción eléctrica. También observamos que la variable GI (intensidad) tiene una '
    'trayectoria prácticamente idéntica a GAP, lo que nos anticipó su alta correlación.'
)

para(
    'En cuanto a los sub-medidores, SM3 (calentador/aire acondicionado) muestra la mayor '
    'estacionalidad invernal, lo que confirma que es el principal responsable del aumento '
    'del consumo en invierno. SM2 (lavandería) se mantiene relativamente constante durante '
    'todo el año, y SM1 (cocina) presenta una distribución muy esparsa.'
)

heading('3.3 Distribuciones Estadísticas', level=2)

para(
    'Analizamos la distribución de cada variable con histogramas y curvas de densidad. Las '
    'variables de potencia —GAP y GRP— presentan distribuciones asimétricas hacia la derecha: '
    'la mayor parte del tiempo el consumo es bajo, pero ocasionalmente hay picos de consumo '
    'alto. El voltaje, en cambio, muestra una distribución más simétrica y concentrada, '
    'lo cual es esperable en una red eléctrica estable. Los sub-medidores, especialmente '
    'SM1 y SM2, tienen distribuciones muy esparsas con muchos valores en cero, '
    'correspondientes a los momentos en que esos electrodomésticos no están en uso.'
)

heading('3.4 Análisis de Correlación', level=2)

para(
    'Calculamos la matriz de correlación de Pearson entre todas las variables. El hallazgo '
    'más importante —y que tuvo consecuencias directas en el modelado— es la correlación '
    'de 0,999 entre GI y GAP. Esto significa que la intensidad de corriente y la potencia '
    'activa son prácticamente la misma variable desde el punto de vista estadístico. '
    'Técnicamente esto es esperable: la potencia activa se calcula como el producto del '
    'voltaje por la corriente (con el factor de potencia), y dado que el voltaje es '
    'relativamente constante, la corriente y la potencia evolucionan prácticamente igual.'
)

para(
    'Esta correlación casi perfecta nos llevó a tomar la decisión de eliminar GI de todos '
    'los escenarios de modelado, ya que no aporta información adicional sobre GAP y puede '
    'generar problemas de multicolinealidad en los modelos. También observamos que SM3 '
    'tiene una correlación moderada con GAP (aproximadamente 0,60), confirmando que el '
    'calentador y aire acondicionado es el sub-medidor con mayor influencia en el consumo total.'
)

nota('Si el tutor pregunta por la correlación GI-GAP: Es una correlación física, no estadística '
     'artificial. P = V × I × cos(φ). Como el voltaje es estable (~230V) y cos(φ) es relativamente '
     'constante, GI y GAP son linealmente proporcionales.')

heading('3.5 Patrones Temporales del Consumo', level=2)

para(
    'Un análisis clave para justificar las variables que construimos luego en el feature '
    'engineering fue el estudio de patrones temporales. Analizamos el consumo promedio '
    'según cuatro dimensiones: hora del día, día de la semana, mes del año y año.'
)

para(
    'Por hora del día, el consumo presenta un valle en la madrugada (entre las 2:00 y las '
    '6:00 de la mañana) y dos picos: uno matutino entre las 7:00 y las 9:00, y otro '
    'vespertino/nocturno entre las 17:00 y las 21:00. Por día de la semana, el consumo '
    'es ligeramente mayor los fines de semana, posiblemente por mayor permanencia en el hogar. '
    'A nivel mensual, el patrón estacional es muy claro: máximos en enero-febrero y '
    'mínimos en junio-agosto.'
)

para(
    'Estos patrones justifican directamente la inclusión de variables como la hora del día, '
    'el día de la semana, el mes y una variable binaria de fin de semana en el feature '
    'engineering. Sin esta exploración previa, no habríamos podido justificar con evidencia '
    'empírica qué variables temporales incluir.'
)

heading('3.6 Detección y Tratamiento de Outliers', level=2)

para(
    'Aplicamos el método del rango intercuartílico (IQR) para detectar y eliminar valores '
    'atípicos. Para las variables continuas (GAP, GRP, VOLT, GI) usamos el criterio estándar '
    'de 1,5 veces el IQR como límite. Para los sub-medidores (SM1, SM2, SM3), que tienen '
    'distribuciones muy esparsas con Q1=Q3=0, usamos el percentil 99,5 como límite superior, '
    'ya que aplicar el criterio IQR estándar habría eliminado toda actividad medida.'
)

para(
    'El filtro se aplicó de forma simultánea: un registro se elimina si cualquiera de sus '
    'variables está fuera del rango permitido. Tras este proceso, el dataset quedó con '
    '1.739.167 registros, lo que equivale a eliminar el 16,18% de los registros limpios '
    '(es decir, de los que no tenían nulos). Este dataset limpio fue exportado como '
    'dataset_limpio.csv y es el punto de partida para todos los escenarios de modelado.'
)

nota('Limitación conocida: SM1 (cocina) quedó en cero en todas las filas del dataset limpio. '
     'Su distribución tiene Q1=Q3=0, y aunque usamos el percentil 99,5 para el límite superior, '
     'los valores de consumo de cocina son tan esporádicos que aún así quedaron filtrados. '
     'Esta es una limitación reconocida del método IQR en variables esparsas.')

heading('3.7 Descomposición Estacional y Autocorrelación', level=2)

para(
    'Aplicamos descomposición estacional aditiva sobre la serie diaria de GAP con un período '
    'de 365 días. Este análisis nos permite separar la serie en tres componentes: tendencia, '
    'estacionalidad y residuo. La tendencia muestra un leve descenso del consumo hacia los '
    'años 2009-2010, posiblemente por mejoras en eficiencia energética o cambios en los '
    'hábitos del hogar. La componente estacional confirma el patrón anual que ya habíamos '
    'identificado, y el residuo es de baja magnitud, lo que indica que la mayor parte de la '
    'variación queda bien capturada por tendencia y estacionalidad.'
)

para(
    'También calculamos las funciones de autocorrelación (ACF) y autocorrelación parcial (PACF) '
    'sobre la serie horaria de GAP. La ACF con 168 lags —es decir, 7 días— muestra correlaciones '
    'significativas en múltiplos de 24 horas, confirmando la fuerte estacionalidad diaria. '
    'Estos resultados nos guiaron directamente en la selección de lags para el feature '
    'engineering: si hay correlación significativa en el lag 24, tiene sentido incluir '
    'el consumo de hace 24 horas como predictor.'
)

doc.add_page_break()


# =============================================================================
# CAPÍTULO 4 — PREPARACIÓN DE DATOS Y ESCENARIOS
# =============================================================================
heading('4. Preparación de Datos, Remuestreo y Escenarios de Predicción')

para(
    'Con el dataset limpio listo, el siguiente paso fue prepararlo para el modelado. '
    'Este proceso incluyó el remuestreo a tres frecuencias distintas y la división '
    'cronológica en conjuntos de entrenamiento y prueba.'
)

heading('4.1 Los Tres Escenarios de Predicción', level=2)

para(
    'Una decisión central de diseño de esta tesis fue evaluar tres horizontes de predicción '
    'distintos, que corresponden a tres escenarios de uso práctico diferentes. Cada escenario '
    'parte del mismo dataset limpio (a frecuencia de 1 minuto) y lo agrega a una frecuencia '
    'distinta mediante el promedio de los valores dentro de cada intervalo.'
)

t = new_table(4, 'Escenario', 'Frecuencia', 'Registros disponibles', 'Uso práctico')
for v in [
    ('Escenario 1', '15 minutos', '133.489', 'Control en tiempo casi real del consumo'),
    ('Escenario 2', '1 hora',     '34.007',  'Gestión horaria de cargas y tarifas'),
    ('Escenario 3', '1 día',      '1.433',   'Planificación energética a mediano plazo'),
]:
    add_row(t, *v)
doc.add_paragraph()

para(
    'Es importante notar que los conteos de registros que acabo de mostrar corresponden '
    'al número de observaciones disponibles después del feature engineering — porque '
    'al calcular lags y estadísticas móviles, las primeras filas quedan sin valor '
    'y se eliminan automáticamente.'
)

heading('4.2 División Cronológica Train / Test', level=2)

para(
    'Para dividir los datos en entrenamiento y prueba, utilizamos una división cronológica '
    'estricta: el 80% de las observaciones más antiguas se asignan al entrenamiento y el '
    '20% más reciente a la prueba. Esta decisión es fundamental en series temporales. '
    'Si dividiéramos aleatoriamente, estaríamos permitiendo que el modelo "vea" datos del '
    'futuro durante el entrenamiento, lo que generaría una estimación de rendimiento '
    'artificialmente optimista —conocido como data leakage—. Al dividir cronológicamente, '
    'simulamos el escenario real: el modelo aprende del pasado y predice el futuro.'
)

t = new_table(4, 'Escenario', 'Total registros', 'Entrenamiento (80%)', 'Prueba (20%)')
for v in [
    ('15 minutos', '133.489', '106.791', '26.698'),
    ('1 hora',     '34.007',  '27.205',  '6.802'),
    ('1 día',      '1.433',   '1.146',   '287'),
]:
    add_row(t, *v)
doc.add_paragraph()

nota('Si el tutor pregunta por qué 80/20 y no otra proporción: Es la división estándar en ML. '
     'En el caso del escenario diario, 287 días de prueba representan casi 10 meses de datos '
     'reales, lo cual es suficiente para evaluar el desempeño en distintas estaciones del año.')

doc.add_page_break()


# =============================================================================
# CAPÍTULO 5 — FEATURE ENGINEERING
# =============================================================================
heading('5. Feature Engineering — Construcción de Variables Predictoras')

para(
    'El feature engineering es, en mi opinión, una de las etapas más importantes de este '
    'trabajo. Los modelos de machine learning que utilizamos no procesan el tiempo de forma '
    'nativa: no saben que un dato es de "lunes por la mañana" o que fue medido "24 horas '
    'antes del dato actual". Por eso, necesitamos transformar toda esa información temporal '
    'en columnas numéricas que el modelo pueda utilizar como entrada.'
)

para(
    'Construimos tres tipos de variables para cada escenario: variables temporales, rezagos '
    '(lags) y estadísticas móviles (rolling windows). Antes de construirlas, eliminamos GI '
    'en los tres escenarios por la correlación de 0,999 con GAP que mencioné antes. '
    'Los predictores eléctricos base que quedan son cinco: GRP, VOLT, SM1, SM2 y SM3.'
)

heading('5.1 Variables Temporales', level=2)

para(
    'Las variables temporales extraen información del índice de fecha y hora de cada '
    'observación. No se toman del dataset original sino del índice del dataset ya remuestreado, '
    'porque el remuestreo modifica el índice temporal. Las variables que utilizamos son:'
)

t = new_table(3, 'Variable', 'Descripción', 'Escenarios')
for v in [
    ('hora',       'Hora del día (0 = medianoche, 23 = 23:00)',         'Escenarios 1 y 2'),
    ('dia_semana', 'Día de la semana (0=lunes, 6=domingo)',              'Los 3 escenarios'),
    ('mes',        'Mes del año (1=enero, 12=diciembre)',                'Los 3 escenarios'),
    ('trimestre',  'Trimestre (1–4)',                                    'Solo Escenario 3'),
    ('dia_anio',   'Día del año (1–365)',                                'Solo Escenario 3'),
    ('es_finde',   'Binaria: 1 si sábado o domingo, 0 si no',           'Los 3 escenarios'),
]:
    add_row(t, *v)
doc.add_paragraph()

para(
    'La variable "hora" no se incluye en el Escenario 3 porque los datos son diarios y '
    'no existe una hora específica asociada. En su lugar, incluimos "trimestre" y "dia_anio" '
    'para capturar la estacionalidad a escalas más gruesas. Estas decisiones se basan '
    'directamente en los patrones temporales que identificamos en el EDA.'
)

heading('5.2 Rezagos (Lags)', level=2)

para(
    'Los rezagos son quizás las variables más intuitivas de este trabajo. Un rezago de '
    'orden k para una serie temporal significa "el valor que tenía la serie k períodos '
    'atrás". En términos de consumo eléctrico, GAP_lag_1 en el escenario horario '
    'representa el consumo de hace 1 hora, y GAP_lag_24 representa el consumo de hace '
    'un día completo. Estos rezagos le permiten al modelo aprender que el consumo tiende '
    'a repetir patrones: si ayer a las 20:00 el consumo fue alto, probablemente hoy a '
    'las 20:00 también lo será.'
)

para('Los rezagos utilizados en cada escenario son:')

t = new_table(3, 'Escenario', 'Lags', 'Equivalencia del lag más largo')
for v in [
    ('15 minutos', 'lag 1, 2, 4, 8, 12, 96',        'lag_96 = 24 horas (mismo cuarto de hora del día anterior)'),
    ('1 hora',     'lag 1, 2, 3, 6, 12, 24, 48, 168', 'lag_168 = 1 semana completa'),
    ('1 día',      'lag 1, 2, 3, 7, 14, 30',          'lag_30 ≈ 1 mes de historia'),
]:
    add_row(t, *v)
doc.add_paragraph()

heading('5.3 Estadísticas Móviles (Rolling Windows)', level=2)

para(
    'Las estadísticas móviles calculan el promedio y la desviación estándar del consumo '
    'sobre una ventana de los k períodos anteriores. Son complementarias a los lags: '
    'mientras que un lag captura un valor puntual del pasado, una media móvil captura '
    'la tendencia reciente promedio. Por ejemplo, GAP_roll_mean_96 en el escenario de '
    '15 minutos representa el consumo promedio de las últimas 24 horas.'
)

para(
    'Un detalle técnico importante: aplicamos un shift(1) antes de calcular el rolling, '
    'lo que garantiza que cada cálculo usa únicamente información del pasado y no incluye '
    'el valor del período actual. Esto es fundamental para evitar data leakage en la '
    'construcción de features.'
)

heading('5.4 Resumen de Features por Escenario', level=2)

t = new_table(6, 'Escenario', 'Eléctricas', 'Temporales', 'Lags', 'Rolling', 'TOTAL')
for v in [
    ('15 minutos', '5', '4', '6', '6', '21 features'),
    ('1 hora',     '5', '4', '8', '6', '23 features'),
    ('1 día',      '5', '5', '6', '6', '22 features'),
]:
    add_row(t, *v)
doc.add_paragraph()

nota('Si el tutor pregunta por qué distintos lags por escenario: Porque la información '
     'relevante del pasado depende de la escala temporal. A 15 minutos importa saber '
     'qué pasó hace 24 horas (lag_96). A nivel diario, importa saber qué pasó hace '
     'una semana (lag_7) o un mes (lag_30).')

doc.add_page_break()


# =============================================================================
# CAPÍTULO 6 — LOS MODELOS
# =============================================================================
heading('6. Los Modelos de Machine Learning')

para(
    'Con los datos preparados y las features construidas, aplicamos tres algoritmos de '
    'machine learning supervisado de regresión. La elección de estos tres modelos responde '
    'a que representan enfoques algorítmicos distintos —árboles de decisión por ensamble '
    'paralelo, boosting secuencial y máquinas de soporte vectorial— y están entre los '
    'más utilizados y mejor evaluados en la literatura de predicción de series temporales '
    'de consumo energético.'
)

heading('6.1 Random Forest (RF)', level=2)

para(
    'Random Forest es un modelo de ensamble que construye múltiples árboles de decisión '
    'de forma independiente. Cada árbol se entrena sobre una submuestra aleatoria del '
    'dataset y considera solo un subconjunto aleatorio de las features en cada división. '
    'La predicción final es el promedio de las predicciones de todos los árboles. Este '
    'mecanismo de aleatorización es lo que le da su nombre y su principal ventaja: al '
    'promediar muchos árboles distintos, se reduce el sobreajuste y se obtiene un modelo '
    'robusto ante datos ruidosos.'
)

para(
    'No requiere escalado previo de los datos, ya que los árboles de decisión son '
    'invariantes a las escalas de las variables. Los hiperparámetros principales son '
    'n_estimators (número de árboles), max_depth (profundidad máxima de cada árbol) '
    'y min_samples_leaf (mínimo de muestras requeridas en una hoja).'
)

heading('6.2 XGBoost', level=2)

para(
    'XGBoost es un modelo de ensamble basado en gradient boosting. A diferencia de Random '
    'Forest, donde los árboles se construyen en paralelo de forma independiente, en '
    'XGBoost los árboles se construyen de forma secuencial: cada árbol nuevo se entrena '
    'para corregir los errores del árbol anterior. Este enfoque iterativo le permite a '
    'XGBoost reducir progresivamente el error de predicción.'
)

para(
    'Es conocido por su alta precisión, eficiencia computacional y sus mecanismos de '
    'regularización que evitan el sobreajuste. Tampoco requiere escalado de datos. '
    'Sus hiperparámetros clave son n_estimators, max_depth, learning_rate (qué tan '
    'grande es el paso en cada iteración) y subsample (proporción de datos usados por árbol).'
)

heading('6.3 Support Vector Regression (SVR)', level=2)

para(
    'SVR es la extensión del algoritmo de Máquinas de Soporte Vectorial para tareas de '
    'regresión. A diferencia de los dos modelos anteriores, SVR busca ajustar una función '
    'dentro de un margen de tolerancia epsilon: solo los puntos que caen fuera de ese '
    'margen (los vectores de soporte) contribuyen al error de entrenamiento. Utilizamos '
    'el kernel RBF (radial basis function) para capturar relaciones no lineales en los datos.'
)

para(
    'SVR es el único modelo que requiere escalado previo de los datos, tanto en las '
    'features (X) como en la variable objetivo (y). Aplicamos StandardScaler para '
    'normalizar a media cero y desviación estándar uno. Otra característica de SVR '
    'es su alto costo computacional en datasets grandes: por esta razón, en los '
    'escenarios de mayor volumen limitamos el conjunto de entrenamiento de SVR a las '
    'últimas 15.000 muestras en el Escenario 1 y a las últimas 10.000 en el Escenario 2.'
)

nota('Si el tutor pregunta por qué solo 3 modelos: Estos tres representan enfoques distintos '
     'y son benchmark estándar en la literatura. Un estudio más amplio podría incluir redes '
     'neuronales LSTM, pero eso requeriría infraestructura adicional y escapa al alcance '
     'de esta tesis.')

doc.add_page_break()


# =============================================================================
# CAPÍTULO 7 — MÉTRICAS Y RESULTADOS BASE
# =============================================================================
heading('7. Métricas de Evaluación y Resultados con Configuración Base')

heading('7.1 Métricas de Evaluación', level=2)

para(
    'Para evaluar el desempeño de los modelos utilizamos cuatro métricas complementarias. '
    'Todas se calculan sobre el conjunto de prueba — es decir, sobre el 20% de datos '
    'más recientes que el modelo nunca vio durante el entrenamiento:'
)

t = new_table(3, 'Métrica', 'Unidad', 'Qué mide y por qué es útil')
for v in [
    ('RMSE', 'kW', 'Raíz del Error Cuadrático Medio. Penaliza errores grandes más que los pequeños. Útil para detectar predicciones muy alejadas de la realidad.'),
    ('MAE',  'kW', 'Error Absoluto Medio. Promedio de los errores absolutos. Más interpretable que RMSE ya que está en las mismas unidades que GAP.'),
    ('MAPE', '%',  'Error Porcentual Absoluto Medio. Expresa el error como porcentaje del valor real. Permite comparar entre escenarios con distintas escalas.'),
    ('R²',   '—',  'Coeficiente de determinación. Proporción de la varianza de GAP explicada por el modelo (0 = nulo, 1 = perfecto). Es la métrica principal de comparación.'),
]:
    add_row(t, *v)
doc.add_paragraph()

para(
    'El R² es nuestra métrica principal de comparación porque no depende de la escala '
    'de la variable y permite comparar directamente entre escenarios. El MAPE excluye '
    'los registros donde el valor real es menor a 0,01 kW para evitar divisiones por '
    'valores cercanos a cero que distorsionarían el resultado.'
)

heading('7.2 Resultados con Configuración Base', level=2)

para(
    'Primero evaluamos cada modelo con una configuración de hiperparámetros seleccionada '
    'manualmente —lo que llamamos "configuración base"—, antes de hacer ningún ajuste '
    'automático. Estos son los resultados sobre el conjunto de prueba:'
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

heading('7.3 Análisis de los Resultados Base', level=2)

para(
    'Del Escenario 1 —15 minutos— puedo destacar que Random Forest y XGBoost obtienen '
    'resultados muy similares, ambos por encima del 91% de varianza explicada. Esto es '
    'un resultado sólido: significa que con la información del historial de consumo y '
    'las variables temporales, el modelo puede predecir el consumo del siguiente cuarto '
    'de hora con una precisión del 91%. SVR, en su configuración base, tiene un desempeño '
    'menor con un R² de 0,8589 y un MAPE de 24,25%.'
)

para(
    'En el Escenario 2 —1 hora— el patrón es similar: XGBoost lidera con R²=0,8812, '
    'seguido muy de cerca por Random Forest con R²=0,8751. SVR mantiene el desempeño '
    'más bajo con R²=0,8415. Es destacable que incluso a resolución horaria, con menos '
    'datos y mayor horizonte de predicción, los modelos mantienen un R² superior al 84%.'
)

para(
    'El Escenario 3 —1 día— es el más desafiante por dos razones: tiene solo 1.146 '
    'registros de entrenamiento y la predicción diaria promedia mucho el ruido de corto '
    'plazo. En este escenario XGBoost lidera con R²=0,7776, seguido de SVR con 0,7374 '
    'y Random Forest con 0,7313. El RMSE es más bajo que en los otros escenarios '
    '(~0,11–0,12 kW) porque los valores diarios son promedios de 1.440 minutos y tienen '
    'menor variabilidad que las series de alta frecuencia.'
)

para(
    'Un patrón claro que emerge es que a mayor granularidad temporal —es decir, menor '
    'horizonte de predicción—, los modelos obtienen mejores resultados. Esto tiene '
    'sentido intuitivo: predecir lo que pasará en los próximos 15 minutos es más fácil '
    'que predecir el promedio del día de mañana.'
)

heading('7.4 Importancia de Features', level=2)

para(
    'Random Forest y XGBoost nos permiten calcular la importancia relativa de cada '
    'feature en las predicciones. En los tres escenarios, los rezagos recientes de GAP '
    'son consistentemente las variables más importantes: GAP_lag_1 y GAP_lag_2, junto '
    'con las medias móviles de largo alcance. Esto confirma que el consumo reciente '
    'es el predictor más potente del consumo futuro.'
)

para(
    'Las variables temporales (hora, mes, dia_semana) también contribuyen de forma '
    'relevante, especialmente en el escenario diario donde la estacionalidad anual '
    'es el factor dominante. Las variables eléctricas como GRP y SM3 tienen una '
    'importancia moderada, y SM1 prácticamente nula por estar en cero en todo el dataset.'
)

doc.add_page_break()


# =============================================================================
# CAPÍTULO 8 — AJUSTE DE HIPERPARÁMETROS
# =============================================================================
heading('8. Ajuste de Hiperparámetros con GridSearchCV')

para(
    'Una vez obtenidos los resultados con la configuración base, aplicamos ajuste automático '
    'de hiperparámetros para intentar mejorar el desempeño de cada modelo. La técnica que '
    'utilizamos es GridSearchCV combinada con TimeSeriesSplit como esquema de validación cruzada.'
)

heading('8.1 ¿Qué es GridSearchCV?', level=2)

para(
    'GridSearchCV es una técnica de búsqueda exhaustiva de hiperparámetros. Definimos un '
    '"espacio de búsqueda" que es una cuadrícula (grid) con los valores posibles para cada '
    'hiperparámetro, y el algoritmo prueba todas las combinaciones posibles de esa cuadrícula. '
    'Para cada combinación, evalúa el desempeño mediante validación cruzada y selecciona '
    'la combinación que produce el mejor resultado promedio.'
)

heading('8.2 ¿Por qué TimeSeriesSplit y no K-Fold estándar?', level=2)

para(
    'Esta es una decisión metodológica importante. La validación cruzada estándar (K-Fold) '
    'divide los datos aleatoriamente en k grupos, lo cual es apropiado para datos independientes '
    'pero incorrecto para series temporales: si un fold de validación contiene datos anteriores '
    'al fold de entrenamiento, estaríamos evaluando el modelo con datos del "pasado" que en '
    'realidad ya conocía, generando una estimación optimista. TimeSeriesSplit garantiza que '
    'en cada fold la validación siempre sea posterior al entrenamiento, respetando la '
    'naturaleza temporal de los datos.'
)

para(
    'Usamos 3 folds y la métrica de optimización fue R². Tanto en el Escenario 1 como en el '
    'Escenario 2, para gestionar el tiempo de cómputo, RF y XGBoost se entrenaron sobre las '
    'últimas 30.000 muestras del conjunto de entrenamiento durante el GridSearch. SVR fue '
    'limitado a 15.000 muestras (Esc. 1) y 10.000 (Esc. 2).'
)

heading('8.3 Espacios de Búsqueda Evaluados', level=2)

t = new_table(3, 'Modelo', 'Hiperparámetro', 'Valores evaluados')
for v in [
    ('Random Forest', 'n_estimators',     '100, 200, 300'),
    ('Random Forest', 'max_depth',        '10, 20, None (sin límite)'),
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

para(
    'Esto resulta en 27 combinaciones para Random Forest (3×3×3), 24 para XGBoost (2×3×2×2) '
    'y 18 para SVR (3×3×2). Cada combinación se evalúa con 3 folds de TimeSeriesSplit, '
    'lo que en total significa 207 entrenamientos por escenario y 621 entrenamientos en total.'
)

heading('8.4 Mejores Hiperparámetros Encontrados', level=2)

t = new_table(3, 'Escenario', 'Modelo', 'Mejores hiperparámetros')
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

doc.add_page_break()


# =============================================================================
# CAPÍTULO 9 — RESULTADOS TRAS EL TUNING
# =============================================================================
heading('9. Resultados tras el Ajuste de Hiperparámetros')

heading('9.1 Comparación Base vs Tuned (R²)', level=2)

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

heading('9.2 Métricas Completas tras el Tuning', level=2)

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

heading('9.3 Interpretación de los Resultados del Tuning', level=2)

para(
    'El hallazgo más interesante del proceso de tuning es el comportamiento diferenciado '
    'de los tres modelos. SVR es, con diferencia, el modelo que más se beneficia del '
    'ajuste de hiperparámetros en todos los escenarios: mejora +0,0212 en el Escenario 1, '
    '+0,0165 en el Escenario 2 y +0,0474 en el Escenario 3. Esto indica que SVR es '
    'muy sensible a la configuración de sus parámetros, especialmente de C, epsilon y gamma.'
)

para(
    'Random Forest y XGBoost, en cambio, muestran cambios mínimos o incluso leves '
    'descensos tras el tuning. Esto no es un resultado negativo: significa que su '
    'configuración base ya era cercana a la óptima. XGBoost en el Escenario 1 tiene '
    'una pequeña disminución (−0,0067), lo cual puede atribuirse a que el GridSearch '
    'fue entrenado sobre una submuestra del conjunto de entrenamiento (30.000 muestras) '
    'y los hiperparámetros óptimos sobre esa submuestra no generalizan perfectamente '
    'al conjunto de prueba completo.'
)

nota('Punto clave para explicar al tutor: que el tuning no siempre mejora todos los modelos '
     'no es un fallo metodológico — es un resultado. Nos dice que RF y XGBoost son robustos '
     'y relativamente insensibles a la configuración de hiperparámetros en este problema.')

doc.add_page_break()


# =============================================================================
# CAPÍTULO 10 — ANÁLISIS COMPARATIVO Y CONCLUSIONES
# =============================================================================
heading('10. Análisis Comparativo y Conclusiones')

heading('10.1 Mejor Modelo por Escenario', level=2)

t = new_table(4, 'Escenario', 'Mejor modelo (tuned)', 'R²', 'MAPE')
for v in [
    ('15 minutos', 'Random Forest', '0,9145', '14,76%'),
    ('1 hora',     'XGBoost',       '0,8812', '16,98%'),
    ('1 día',      'SVR',           '0,7848', '9,66%'),
]:
    add_row(t, *v, bold=True)
doc.add_paragraph()

heading('10.2 Patrones Generales Identificados', level=2)

para(
    'A lo largo de los nueve modelos evaluados (3 algoritmos × 3 escenarios), emergen '
    'varios patrones claros que vale la pena destacar:'
)

para(
    'Primero: a mayor granularidad temporal, mejor desempeño. El escenario de 15 minutos '
    'alcanza un R² de 0,91, el horario llega a 0,88 y el diario a 0,78. Esto es intuitivo: '
    'predecir el próximo cuarto de hora es más fácil que predecir el promedio del día '
    'siguiente, y además el escenario de 15 minutos dispone de 106.791 registros de '
    'entrenamiento vs. solo 1.146 del escenario diario.'
)

para(
    'Segundo: XGBoost es el algoritmo más consistente. Lidera en R² base en dos de los '
    'tres escenarios (15 min y 1 hora) y mantiene un desempeño muy competitivo en el '
    'escenario diario. Su robustez y precisión lo posicionan como el algoritmo de '
    'referencia para este tipo de problema.'
)

para(
    'Tercero: SVR es el modelo más sensible a los hiperparámetros. Con su configuración '
    'base es el de menor rendimiento en todos los escenarios, pero tras el tuning se '
    'convierte en el mejor modelo para el escenario diario (R²=0,7848, MAPE=9,66%). '
    'Esto sugiere que SVR tiene potencial pero requiere un proceso de ajuste más cuidadoso.'
)

para(
    'Cuarto: los rezagos de consumo son las variables más importantes. En los tres '
    'escenarios, las features que más contribuyen a la predicción son los valores '
    'recientes de GAP (lags cortos) y las medias móviles. Las variables temporales '
    'son relevantes pero secundarias, y las variables eléctricas adicionales (GRP, '
    'SM3) aportan información complementaria.'
)

heading('10.3 Conclusión Final', level=2)

para(
    'El trabajo demuestra que es perfectamente factible construir modelos predictivos '
    'del consumo energético doméstico utilizando algoritmos de machine learning estándar, '
    'sin recurrir a arquitecturas de deep learning como LSTM. Con el feature engineering '
    'adecuado —especialmente la construcción de rezagos y estadísticas móviles que '
    'capturan la memoria de la serie temporal—, modelos como Random Forest y XGBoost '
    'pueden explicar más del 91% de la variabilidad del consumo a resolución de 15 minutos.'
)

para(
    'Los resultados obtenidos son coherentes con la literatura especializada y los tres '
    'escenarios ofrecen información útil para distintas aplicaciones prácticas: el escenario '
    'de 15 minutos es útil para control en tiempo casi real, el horario para gestión de '
    'tarifas y el diario para planificación energética a mediano plazo. El proceso de '
    'ajuste de hiperparámetros confirma que modelos de ensamble como RF y XGBoost son '
    'robustos a la configuración inicial, mientras que SVR se beneficia significativamente '
    'de un ajuste cuidadoso, especialmente en el escenario de menor volumen de datos.'
)

nota('Cierre sugerido para la exposición: "En resumen, logramos construir un sistema de '
     'predicción completo con tres horizontes temporales, tres algoritmos distintos y '
     'un proceso de optimización riguroso. Los resultados son sólidos, las limitaciones '
     'están identificadas y el trabajo está completamente documentado. Quedo a disposición '
     'para responder cualquier consulta."')

doc.add_page_break()


# =============================================================================
# ANEXO — POSIBLES PREGUNTAS DEL TUTOR
# =============================================================================
heading('Anexo: Posibles Preguntas del Tutor y Respuestas Sugeridas')

para(
    'A continuación se listan las preguntas más probables que el tutor podría hacer '
    'durante la exposición, con respuestas concisas y directas:'
)

preguntas = [
    (
        '¿Por qué eligieron este dataset y no uno de Chile o Latinoamérica?',
        'El dataset UCI es el más utilizado en la literatura de predicción de consumo energético residencial. '
        'Tiene alta calidad, granularidad de 1 minuto, casi 4 años de datos y está ampliamente documentado. '
        'No existen datasets públicos equivalentes para Chile con esas características. El objetivo de la '
        'tesis es metodológico: demostrar que los algoritmos funcionan, no estudiar el consumo francés específicamente.'
    ),
    (
        '¿Por qué eliminaron GI si es una variable del dataset?',
        'GI tiene una correlación de 0,999 con GAP, la variable objetivo. Mantenerla como predictor '
        'introduce multicolinealidad severa sin agregar información útil, lo que puede inestabilizar '
        'los coeficientes del modelo. Además, técnicamente GI y GAP son casi la misma magnitud física: '
        'Potencia = Voltaje × Corriente × cos(φ), y al ser el voltaje relativamente constante, '
        'la corriente y la potencia son prácticamente proporcionales.'
    ),
    (
        '¿Por qué no usaron redes neuronales LSTM?',
        'LSTM es una arquitectura especializada para secuencias temporales y puede ser una extensión '
        'natural de este trabajo. Sin embargo, requiere infraestructura computacional significativamente '
        'mayor y un proceso de ajuste más complejo. El objetivo de esta tesis es demostrar que algoritmos '
        'de ML estándar pueden obtener resultados competitivos con un proceso metodológico riguroso. '
        'Comparar con LSTM sería una extensión interesante para trabajo futuro.'
    ),
    (
        '¿Por qué el R² del escenario diario es más bajo?',
        'Por dos razones principales: primero, el escenario diario tiene solo 1.146 registros de '
        'entrenamiento vs. 106.791 del escenario de 15 minutos. Con menos datos, el modelo tiene menos '
        'información para aprender. Segundo, predecir el promedio diario es inherentemente más difícil '
        'porque hay más factores imprevisibles que afectan el comportamiento de un día completo que el '
        'de los próximos 15 minutos.'
    ),
    (
        '¿Por qué XGBoost a veces empeora con el tuning?',
        'El GridSearch optimiza sobre una submuestra del conjunto de entrenamiento (30.000 muestras) '
        'por razones de tiempo de cómputo, y los hiperparámetros seleccionados no siempre generalizan '
        'perfectamente al conjunto de prueba completo. Además, XGBoost ya tenía una configuración base '
        'muy cercana al óptimo, por lo que las diferencias son mínimas (−0,0067 en el peor caso) y '
        'estadísticamente no son significativas.'
    ),
    (
        '¿Cuál sería el siguiente paso lógico para este trabajo?',
        'Hay varias extensiones naturales: (1) incorporar variables exógenas como temperatura, '
        'calendario de festivos o tarifas eléctricas; (2) comparar con modelos de deep learning como '
        'LSTM; (3) aplicar la metodología a un dataset chileno; (4) evaluar modelos multivariados '
        'que predigan también los sub-medidores; (5) desarrollar un sistema de predicción en línea '
        'con actualización incremental del modelo.'
    ),
]

for i, (pregunta, respuesta) in enumerate(preguntas, 1):
    p = doc.add_paragraph()
    r = p.add_run(f'P{i}: {pregunta}')
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.bold = True
    p.paragraph_format.space_after = Pt(2)

    p2 = doc.add_paragraph()
    r2 = p2.add_run(f'R: {respuesta}')
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(12)
    p2.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p2.paragraph_format.left_indent = Cm(0.5)
    p2.paragraph_format.space_after = Pt(12)


# =============================================================================
# GUARDAR
# =============================================================================
print(f'\nGuardando documento de exposición...')
doc.save(OUT_PATH)
print(f'✓ Documento generado: {OUT_PATH}')
