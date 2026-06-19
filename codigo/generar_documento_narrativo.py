# =============================================================================
# DOCUMENTO NARRATIVO DE ESTUDIO — Tercera persona, lenguaje simple
# Sin gráficos, sin tablas complejas, solo texto explicativo
# =============================================================================

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

_here = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = _here if os.path.exists(os.path.join(_here, 'datos')) else os.path.dirname(_here)
OUT_FILE = os.path.join(BASE_DIR, 'Documento_Estudio_Narrativo.docx')

# =============================================================================
# HELPERS SIMPLES
# =============================================================================

def titulo_seccion(doc, texto, nivel):
    h = doc.add_heading(texto, level=nivel)
    colores = {
        1: RGBColor(0x1A, 0x23, 0x7E),
        2: RGBColor(0x0D, 0x47, 0xA1),
        3: RGBColor(0x1B, 0x5E, 0x20),
    }
    h.runs[0].font.color.rgb = colores.get(nivel, RGBColor(0x33, 0x33, 0x33))
    return h

def parrafo(doc, texto):
    p = doc.add_paragraph(texto)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.first_line_indent = Cm(0.8)
    return p

def separador(doc):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(6)
    pPr = p._p.get_or_add_pPr()
    pb = OxmlElement('w:pBdr')
    bot = OxmlElement('w:bottom')
    bot.set(qn('w:val'), 'single')
    bot.set(qn('w:sz'), '6')
    bot.set(qn('w:space'), '1')
    bot.set(qn('w:color'), '1A237E')
    pb.append(bot)
    pPr.append(pb)

# =============================================================================
# DOCUMENTO
# =============================================================================

doc = Document()

for section in doc.sections:
    section.top_margin    = Cm(3.0)
    section.bottom_margin = Cm(3.0)
    section.left_margin   = Cm(3.5)
    section.right_margin  = Cm(3.0)

style = doc.styles['Normal']
style.font.name = 'Calibri'
style.font.size = Pt(12)

# =============================================================================
# PORTADA
# =============================================================================
for _ in range(5):
    doc.add_paragraph()

port = doc.add_paragraph()
port.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = port.add_run('DOCUMENTO DE ESTUDIO')
r.font.size = Pt(22)
r.font.bold = True
r.font.color.rgb = RGBColor(0x1A, 0x23, 0x7E)

doc.add_paragraph()

sub = doc.add_paragraph()
sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = sub.add_run(
    '"Modelo predictivo del consumo energético en hogares\n'
    'inteligentes utilizando algoritmos de machine learning"'
)
r.font.size = Pt(14)
r.font.italic = True
r.font.color.rgb = RGBColor(0x42, 0x42, 0x42)

doc.add_paragraph()
doc.add_paragraph()

desc = doc.add_paragraph()
desc.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = desc.add_run('Redactado en tercera persona — lenguaje accesible')
r.font.size = Pt(11)
r.font.color.rgb = RGBColor(0x75, 0x75, 0x75)

doc.add_paragraph()
anio = doc.add_paragraph()
anio.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = anio.add_run('2026')
r.font.size = Pt(12)
r.font.bold = True

doc.add_page_break()

# =============================================================================
# 1. DE QUÉ TRATA EL TRABAJO
# =============================================================================
titulo_seccion(doc, '1. De qué trata el trabajo', 1)
separador(doc)

parrafo(doc,
    'El presente trabajo de tesis tiene como propósito principal comparar el rendimiento '
    'de tres métodos computacionales de predicción sobre el consumo eléctrico de un hogar '
    'residencial. La idea central es que, si se tiene registro de cuánta energía ha '
    'consumido una vivienda en el pasado, es posible construir un sistema que sea capaz '
    'de anticipar cuánta energía consumirá en el futuro próximo.')

parrafo(doc,
    'Para llevar a cabo esta comparación, el estudio utiliza un conjunto de datos real '
    'proveniente de un hogar en Francia, que cuenta con mediciones eléctricas detalladas '
    'durante cuatro años consecutivos. Sobre estos datos se aplicaron tres algoritmos '
    'distintos de aprendizaje automático, conocidos por sus siglas en inglés como '
    'Random Forest, XGBoost y SVR, evaluando cada uno bajo tres escenarios temporales '
    'diferentes: predicción cada quince minutos, predicción cada hora y predicción cada día.')

parrafo(doc,
    'El aporte del trabajo radica en comparar de manera sistemática y con el mismo '
    'protocolo experimental cómo se comporta cada método según el intervalo de tiempo '
    'que se desea predecir. Esto permite responder preguntas concretas como: ¿qué '
    'método funciona mejor a corto plazo?, ¿el rendimiento cambia si se predice para '
    'el día siguiente en lugar de los próximos quince minutos?, y ¿vale la pena dedicar '
    'tiempo a ajustar los parámetros de cada método o los valores predeterminados son '
    'suficientes?')

doc.add_page_break()

# =============================================================================
# 2. EL CONJUNTO DE DATOS
# =============================================================================
titulo_seccion(doc, '2. El conjunto de datos utilizado', 1)
separador(doc)

titulo_seccion(doc, '2.1 Origen y descripción general', 2)

parrafo(doc,
    'El conjunto de datos empleado en este estudio proviene del repositorio público '
    'de machine learning de la Universidad de California en Irvine, conocido '
    'mundialmente como UCI Machine Learning Repository. Fue recopilado durante cuatro '
    'años en una vivienda ubicada en la ciudad de Sceaux, Francia, a unos siete '
    'kilómetros al sur de París.')

parrafo(doc,
    'El medidor eléctrico de ese hogar registró automáticamente el estado del consumo '
    'una vez por minuto, desde el 16 de diciembre de 2006 hasta el 26 de noviembre de '
    '2010. Al cabo de ese período, el archivo acumuló más de dos millones de registros, '
    'específicamente 2.075.259 filas de datos. Cada fila contiene la fecha y hora de '
    'la medición junto con siete variables numéricas que describen el comportamiento '
    'eléctrico del hogar en ese instante.')

titulo_seccion(doc, '2.2 Qué mide cada variable', 2)

parrafo(doc,
    'La variable más importante del conjunto de datos se denomina Potencia Activa '
    'Global, identificada en el estudio con el nombre GAP por sus siglas en inglés. '
    'Esta variable representa la cantidad de electricidad que el hogar está consumiendo '
    'en cada momento para realizar trabajo útil, como encender una lámpara, calentar '
    'agua o hacer funcionar un electrodoméstico. Es, en términos simples, lo que '
    'aparece en la factura eléctrica. Toda la predicción del estudio está orientada '
    'a anticipar el valor futuro de esta variable.')

parrafo(doc,
    'La segunda variable es la Potencia Reactiva Global, llamada GRP en el estudio. '
    'A diferencia de la potencia activa, la reactiva no realiza trabajo útil, sino '
    'que oscila entre la fuente y los dispositivos eléctricos. Aunque no se factura '
    'directamente, complementa la información disponible y el estudio la incluye como '
    'variable de apoyo para los modelos.')

parrafo(doc,
    'La tercera variable es el Voltaje, nombrada VOLT, que indica el nivel de tensión '
    'eléctrica en el hogar en cada momento. Esta variable varía ligeramente según la '
    'demanda general de la red eléctrica y también se utiliza como información de '
    'entrada para los modelos.')

parrafo(doc,
    'La cuarta variable, llamada Intensidad de Corriente Global o GI, representa la '
    'cantidad de corriente eléctrica que fluye por el circuito principal del hogar. '
    'Sin embargo, esta variable fue descartada antes de entrenar los modelos porque '
    'tiene una relación matemática casi perfecta con la potencia activa: el 99,9% de '
    'su comportamiento puede predecirse conociendo únicamente GAP. Incluirla habría '
    'confundido a los algoritmos, que no habrían podido distinguir si la predicción '
    'proviene de una u otra variable.')

parrafo(doc,
    'Las últimas tres variables son los sub-medidores de consumo por zona del hogar. '
    'El primero, SM1, registra el consumo de la cocina, incluyendo el lavavajillas, '
    'el horno y el microondas. El segundo, SM2, corresponde a la zona de lavandería, '
    'donde se ubica la lavadora, la secadora y la heladera. El tercero, SM3, mide '
    'el consumo del sistema de calefacción y aire acondicionado, que en el hogar '
    'estudiado resulta ser el de mayor consumo. Estas tres variables brindan '
    'información desagregada sobre qué parte de la vivienda está consumiendo energía '
    'en cada momento.')

titulo_seccion(doc, '2.3 Por qué se eligió este conjunto de datos', 2)

parrafo(doc,
    'Este conjunto de datos fue seleccionado por varias razones concretas. En primer '
    'lugar, proviene de mediciones reales en un hogar real, no de simulaciones '
    'computacionales ni datos artificiales. En segundo lugar, cubre cuatro años '
    'completos, lo que permite observar patrones que se repiten con el cambio de '
    'estaciones del año, los distintos días de la semana y las diferentes horas del '
    'día. En tercer lugar, incluye información detallada de sub-medidores por zona '
    'del hogar, lo que enriquece el análisis.')

parrafo(doc,
    'Adicionalmente, este es el conjunto de datos de referencia más utilizado en la '
    'comunidad científica internacional para investigar la predicción de consumo '
    'eléctrico residencial con aprendizaje automático. Usarlo permite que los '
    'resultados del presente estudio puedan ser comparados directamente con los de '
    'otros trabajos publicados en revistas y conferencias científicas alrededor del '
    'mundo.')

doc.add_page_break()

# =============================================================================
# 3. PREPARACIÓN DE LOS DATOS
# =============================================================================
titulo_seccion(doc, '3. Cómo se prepararon los datos', 1)
separador(doc)

titulo_seccion(doc, '3.1 Eliminación de registros incompletos', 2)

parrafo(doc,
    'Al revisar el conjunto de datos original se encontró que el 1,25 por ciento de '
    'las filas tiene valores faltantes, es decir, registros donde el medidor no capturó '
    'ninguna medición. Una característica particular de este problema es que cuando '
    'falta información en una fila, todas las variables de esa fila están ausentes al '
    'mismo tiempo. Esto indica que durante ese minuto el medidor estuvo apagado o '
    'sin conexión, por lo tanto el registro completo carece de utilidad.')

parrafo(doc,
    'La solución aplicada fue eliminar directamente todas esas filas incompletas. '
    'Dado que representan apenas el 1,25 por ciento del total, su eliminación no '
    'afecta la representatividad ni la calidad del conjunto de datos resultante. '
    'Tras este proceso quedaron disponibles aproximadamente 2.049.000 registros.')

titulo_seccion(doc, '3.2 Eliminación de valores extremos', 2)

parrafo(doc,
    'Una vez eliminados los registros incompletos, se procedió a identificar y '
    'descartar los valores extremos, también conocidos como valores atípicos o '
    'outliers. Estos son mediciones que se alejan demasiado del comportamiento '
    'habitual del hogar y que, si se dejan en el conjunto de datos, pueden confundir '
    'a los algoritmos y deteriorar la calidad de las predicciones.')

parrafo(doc,
    'Para detectarlos se utilizó el método del rango intercuartílico, conocido como '
    'método IQR. Este método divide los datos en cuatro partes iguales y considera '
    'como extremos todos los valores que quedan por debajo del límite inferior o por '
    'encima del límite superior de un rango definido estadísticamente. Es uno de los '
    'métodos más utilizados en ciencia de datos por su sencillez y robustez.')

parrafo(doc,
    'Tras aplicar ambos pasos de limpieza, el conjunto de datos quedó con 1.739.167 '
    'registros, listos para ser utilizados en el entrenamiento de los modelos.')

titulo_seccion(doc, '3.3 El caso particular del sub-medidor de cocina', 2)

parrafo(doc,
    'Durante el proceso de limpieza se detectó una situación particular con el '
    'sub-medidor de cocina. Esta variable tiene un comportamiento muy irregular: '
    'durante la gran mayoría del tiempo su valor es cero, porque los aparatos de '
    'la cocina se usan solo en momentos específicos del día. Al aplicar el método '
    'IQR, los pocos valores distintos de cero fueron identificados como extremos y '
    'eliminados, dejando la variable completamente en cero.')

parrafo(doc,
    'Esto constituye una limitación del método aplicado: cuando una variable tiene '
    'valores casi siempre en cero con picos esporádicos, el filtro estadístico no '
    'es capaz de distinguir entre un valor atípico real y un consumo legítimo pero '
    'infrecuente. Esta situación fue documentada como una limitación conocida del '
    'estudio.')

doc.add_page_break()

# =============================================================================
# 4. LOS TRES ESCENARIOS TEMPORALES
# =============================================================================
titulo_seccion(doc, '4. Los tres escenarios temporales', 1)
separador(doc)

titulo_seccion(doc, '4.1 Por qué se usaron tres escalas de tiempo', 2)

parrafo(doc,
    'El estudio plantea tres escenarios distintos según la escala de tiempo en que '
    'se realiza la predicción. Esto responde a una pregunta práctica importante: '
    'el comportamiento del consumo eléctrico y la dificultad para predecirlo cambian '
    'según si se quiere anticipar el consumo en los próximos quince minutos, en la '
    'próxima hora o durante el día siguiente.')

parrafo(doc,
    'Comparar los tres escenarios bajo el mismo protocolo experimental es precisamente '
    'la contribución central de este trabajo. La mayoría de estudios similares en la '
    'literatura analizan únicamente una escala de tiempo. Evaluar las tres '
    'simultáneamente permite extraer conclusiones más completas sobre cómo varía el '
    'rendimiento de cada método según el horizonte de predicción.')

titulo_seccion(doc, '4.2 Escenario de quince minutos', 2)

parrafo(doc,
    'En el primer escenario, los más de dos millones de mediciones originales a un '
    'minuto de frecuencia se agrupan en bloques de quince minutos, calculando el '
    'promedio de cada variable dentro de cada bloque. El resultado es un conjunto '
    'de aproximadamente 133.000 registros, donde cada fila representa el consumo '
    'promedio del hogar durante quince minutos.')

parrafo(doc,
    'Este escenario es el de mayor resolución temporal entre los tres y es el más '
    'útil para aplicaciones de gestión energética en tiempo real, como el control '
    'automático de electrodomésticos inteligentes o la respuesta inmediata ante '
    'picos de consumo.')

titulo_seccion(doc, '4.3 Escenario de una hora', 2)

parrafo(doc,
    'En el segundo escenario, las mediciones se agrupan en bloques de una hora, '
    'resultando en aproximadamente 33.800 registros. Este nivel de detalle es el '
    'más frecuente en la literatura científica de predicción energética, ya que '
    'coincide con la resolución de los sistemas de tarifas eléctricas horarias '
    'que existen en muchos países.')

parrafo(doc,
    'Predecir con una hora de anticipación es útil, por ejemplo, para que una '
    'empresa eléctrica planifique cuánta energía necesitará distribuir en cada '
    'tramo horario del día.')

titulo_seccion(doc, '4.4 Escenario de un día', 2)

parrafo(doc,
    'En el tercer escenario, los datos se agrupan por día completo, produciendo '
    'apenas 1.403 registros. Cada fila representa el consumo promedio de toda '
    'una jornada. Este escenario es el de menor resolución pero tiene aplicaciones '
    'importantes en la planificación de la red eléctrica a mediano plazo, en la '
    'estimación anticipada de facturas eléctricas mensuales y en la gestión de '
    'recursos energéticos renovables.')

parrafo(doc,
    'Predecir a nivel diario es, en general, más difícil que predecir a quince '
    'minutos, porque al promediar todo un día en un solo valor se pierde '
    'información sobre los patrones de consumo que ocurren a lo largo de las '
    'horas: el pico de la mañana, la pausa del mediodía y el consumo de la noche '
    'desaparecen en el promedio diario.')

titulo_seccion(doc, '4.5 El horizonte de predicción', 2)

parrafo(doc,
    'En los tres escenarios, los modelos realizan lo que se denomina predicción '
    'de un paso adelante. Esto significa que en cada caso el modelo estima el '
    'valor del próximo período utilizando como referencia todos los valores '
    'reales del pasado. En el escenario de quince minutos, el modelo predice '
    'los próximos quince minutos. En el de una hora, predice la próxima hora. '
    'En el diario, predice el consumo del día siguiente.')

doc.add_page_break()

# =============================================================================
# 5. CONSTRUCCIÓN DE VARIABLES DE ENTRADA
# =============================================================================
titulo_seccion(doc, '5. Cómo se construyeron las variables de entrada', 1)
separador(doc)

parrafo(doc,
    'Los métodos de aprendizaje automático utilizados en este estudio, a diferencia '
    'de los métodos estadísticos clásicos para series de tiempo, no son capaces de '
    'analizar una secuencia de datos en orden temporal de forma automática. Para que '
    'estos algoritmos puedan aprender patrones temporales, es necesario transformar '
    'la serie de consumo en un conjunto de variables que capturen explícitamente la '
    'información del pasado. A este proceso se le denomina ingeniería de características.')

titulo_seccion(doc, '5.1 Variables de retraso temporal', 2)

parrafo(doc,
    'El primer tipo de variables creadas se conoce como retrasos o lags. Consisten '
    'en copiar el valor de consumo de períodos anteriores y ponerlos como variables '
    'de entrada para predecir el período actual. Por ejemplo, para predecir el consumo '
    'a las 14:15 horas, se proporciona al modelo el consumo registrado a las 14:00 '
    '(un período atrás), a las 13:45 (dos períodos atrás), y así sucesivamente hasta '
    'el período más lejano que se considere relevante.')

parrafo(doc,
    'La razón de incluir estas variables es que el consumo eléctrico tiene una '
    'dependencia temporal muy fuerte: lo que el hogar consumió en los últimos '
    'minutos u horas es uno de los mejores indicadores de lo que consumirá a '
    'continuación. En el escenario de quince minutos se incluyen retrasos de hasta '
    'veinticuatro horas hacia atrás, capturando así el patrón del día anterior. '
    'En el escenario horario se llega hasta una semana atrás, y en el diario hasta '
    'un mes atrás.')

titulo_seccion(doc, '5.2 Promedios y variabilidad móviles', 2)

parrafo(doc,
    'El segundo tipo de variables creadas son los promedios y desviaciones estándar '
    'móviles. Estos calculan la media y la dispersión del consumo durante las últimas '
    'ventanas de tiempo, ofreciendo una visión suavizada de la tendencia reciente. '
    'Mientras que los retrasos capturan un valor puntual del pasado, estas ventanas '
    'móviles capturan el comportamiento promedio de los últimos períodos, filtrando '
    'fluctuaciones breves y revelando la dirección general del consumo.')

parrafo(doc,
    'Un cuidado especial que se aplicó en la construcción de estas variables fue '
    'desplazar el cálculo un período hacia atrás antes de calcular el promedio. '
    'Esto evita un error grave conocido como contaminación de datos o data leakage, '
    'que ocurre cuando el modelo accede al valor del período que está intentando '
    'predecir como parte de su información de entrada. Si esto sucediera, las '
    'métricas de rendimiento serían engañosamente buenas pero el modelo fallaría '
    'en una aplicación real.')

titulo_seccion(doc, '5.3 Variables que describen el momento del tiempo', 2)

parrafo(doc,
    'El tercer tipo de variables captura los patrones cíclicos del consumo según '
    'el momento del día, la semana y el año. Para cada registro se extrae la hora '
    'del día, el día de la semana, el mes del año y si ese día es fin de semana o '
    'día laboral. Estas variables son relevantes porque el consumo eléctrico sigue '
    'rutinas humanas muy marcadas: hay más consumo durante la noche que a las tres '
    'de la madrugada, más consumo en invierno que en verano por la calefacción, y '
    'los fines de semana tienen patrones distintos a los días de trabajo.')

parrafo(doc,
    'En el escenario diario se agregan también el trimestre del año y el día '
    'del año para capturar la estacionalidad a una escala más amplia. La variable '
    'de hora del día no se incluye en el escenario diario porque al agregar los '
    'datos a nivel de un día completo esa información deja de existir: todos los '
    'registros diarios tienen una sola entrada sin hora específica.')

doc.add_page_break()

# =============================================================================
# 6. CÓMO SE DIVIDIERON LOS DATOS
# =============================================================================
titulo_seccion(doc, '6. Cómo se dividieron los datos para entrenar y evaluar', 1)
separador(doc)

titulo_seccion(doc, '6.1 La separación entre entrenamiento y evaluación', 2)

parrafo(doc,
    'Antes de entrenar cualquier modelo es necesario separar el conjunto de datos '
    'en dos partes. La primera parte, llamada conjunto de entrenamiento, se utiliza '
    'para que el algoritmo aprenda los patrones del consumo. La segunda parte, '
    'llamada conjunto de prueba o de evaluación, se reserva completamente y el '
    'modelo nunca la ve durante el entrenamiento. Luego, cuando el modelo ya está '
    'entrenado, se le pide que prediga los valores del conjunto de prueba y se '
    'comparan esas predicciones con los valores reales para medir su rendimiento.')

parrafo(doc,
    'Esta separación es fundamental para saber si el modelo aprendió a generalizar '
    'o simplemente memorizó los datos de entrenamiento. Un modelo que memoriza '
    'obtiene resultados perfectos sobre los datos que ya vio, pero falla completamente '
    'con datos nuevos. Evaluar sobre un conjunto separado garantiza que la medición '
    'de rendimiento sea honesta.')

titulo_seccion(doc, '6.2 Por qué la separación respeta el orden del tiempo', 2)

parrafo(doc,
    'En este estudio la separación se realizó de manera estrictamente cronológica: '
    'el 80 por ciento más antiguo de los datos se destinó al entrenamiento y el '
    '20 por ciento más reciente al conjunto de prueba. Esto no es arbitrario. En '
    'series de tiempo, mezclar aleatoriamente los datos antes de separar '
    'entrenamiento y prueba es un error metodológico grave.')

parrafo(doc,
    'Si se mezclaran, podría ocurrir que el modelo aprenda durante el entrenamiento '
    'datos del año 2010 y luego se evalúe con datos del año 2007. En ese caso, el '
    'modelo estaría usando información del futuro para aprender, lo que en la '
    'práctica no es posible. Las métricas de rendimiento serían artificialmente '
    'optimistas y no reflejarían el desempeño real que tendría el sistema en '
    'producción. Al mantener el orden cronológico, el estudio simula exactamente '
    'la situación real: el modelo aprende con el pasado y se evalúa con el futuro.')

parrafo(doc,
    'En los tres escenarios el corte cronológico ocurre aproximadamente en abril '
    'de 2009. Todo lo anterior a esa fecha es entrenamiento y todo lo posterior '
    'es evaluación.')

titulo_seccion(doc, '6.3 El escalado de datos para un modelo específico', 2)

parrafo(doc,
    'Uno de los tres modelos utilizados, el SVR, es sensible a la magnitud de los '
    'valores de las variables de entrada. Si una variable tiene valores en miles y '
    'otra tiene valores entre cero y uno, el modelo podría darle demasiado peso '
    'a la primera solo por su escala numérica, sin que eso corresponda a una '
    'mayor importancia real.')

parrafo(doc,
    'Para corregir esto, se aplicó un proceso de estandarización que transforma '
    'cada variable para que su promedio sea cero y su dispersión sea uniforme. '
    'Este proceso se calculó exclusivamente usando los datos de entrenamiento y '
    'luego se aplicó, sin recalcular, al conjunto de prueba. De esta manera se '
    'evita que la estandarización incorpore información del futuro en el proceso '
    'de preparación de los datos. Los otros dos modelos, Random Forest y XGBoost, '
    'no requieren este paso porque sus mecanismos internos de aprendizaje son '
    'independientes de la escala numérica de las variables.')

doc.add_page_break()

# =============================================================================
# 7. LOS TRES MÉTODOS DE PREDICCIÓN
# =============================================================================
titulo_seccion(doc, '7. Los tres métodos de predicción utilizados', 1)
separador(doc)

titulo_seccion(doc, '7.1 Random Forest', 2)

parrafo(doc,
    'Random Forest, que en español puede traducirse como Bosque Aleatorio, es un '
    'método que construye una gran cantidad de árboles de decisión y combina sus '
    'respuestas para obtener una predicción final más robusta y precisa que la de '
    'cualquier árbol individual. La idea es sencilla: en lugar de confiar en la '
    'opinión de una sola fuente, se consulta a muchas fuentes distintas y se '
    'toma el promedio de sus respuestas.')

parrafo(doc,
    'Cada árbol de decisión dentro del bosque aprende con una muestra diferente '
    'del conjunto de entrenamiento, seleccionada al azar con reposición. Además, '
    'cuando cada árbol toma una decisión interna, solo considera una parte aleatoria '
    'de las variables disponibles. Esto hace que los árboles sean diversos entre sí '
    'y que sus errores individuales no se acumulen en la predicción final.')

parrafo(doc,
    'El método fue configurado con doscientos árboles. Se limitó también la '
    'complejidad de cada árbol mediante dos parámetros: uno que controla cuántas '
    'divisiones puede tener cada árbol antes de detenerse, y otro que exige un '
    'mínimo de cinco observaciones en cada grupo final para que el árbol realice '
    'una predicción. Estas restricciones evitan que cada árbol individual se ajuste '
    'demasiado a los datos de entrenamiento y pierda capacidad de generalización.')

titulo_seccion(doc, '7.2 XGBoost', 2)

parrafo(doc,
    'XGBoost, cuya sigla viene del inglés Extreme Gradient Boosting, es también un '
    'método basado en árboles de decisión, pero con una lógica distinta a la del '
    'bosque aleatorio. En lugar de construir todos los árboles al mismo tiempo y '
    'de forma independiente, XGBoost los construye uno tras otro, de manera secuencial, '
    'donde cada árbol nuevo se especializa en corregir los errores que cometió el '
    'árbol anterior.')

parrafo(doc,
    'El proceso funciona de la siguiente manera: el primer árbol hace una predicción '
    'inicial. Luego se calcula cuánto se equivocó en cada caso. El segundo árbol '
    'aprende a predecir precisamente esos errores. La predicción del conjunto hasta '
    'ese punto se actualiza sumando la corrección del segundo árbol, pero multiplicada '
    'por un factor pequeño llamado tasa de aprendizaje, para que la corrección sea '
    'gradual y cuidadosa. Este ciclo se repite hasta completar el número de árboles '
    'definido, que en este estudio fue de doscientos.')

parrafo(doc,
    'XGBoost incluye mecanismos propios de control del sobreajuste, como la '
    'posibilidad de que cada árbol use solo una fracción aleatoria de los datos '
    'disponibles, lo que introduce variedad en el proceso de aprendizaje. En este '
    'estudio se configuró para usar el ochenta por ciento de los datos en cada árbol '
    'y se eligió una tasa de aprendizaje de 0,05, lo cual implica correcciones '
    'pequeñas y progresivas que suelen generalizar mejor.')

titulo_seccion(doc, '7.3 SVR', 2)

parrafo(doc,
    'SVR proviene del inglés Support Vector Regression y representa un enfoque '
    'completamente distinto a los dos métodos anteriores. En lugar de construir '
    'árboles de decisión, este método busca una función matemática que se ajuste '
    'a los datos de entrenamiento dentro de una banda de tolerancia definida. '
    'Cualquier predicción que quede dentro de esa banda se considera aceptable y '
    'no genera penalización; solo los casos donde el error supera ese margen '
    'son tomados en cuenta para afinar el modelo.')

parrafo(doc,
    'Los puntos del conjunto de entrenamiento que quedan en el borde o fuera de '
    'esa banda de tolerancia son los que definen el modelo y se denominan vectores '
    'de soporte. El resto de los datos no influye directamente en la función de '
    'predicción. Esto hace que el método sea especialmente robusto ante valores '
    'atípicos ocasionales, ya que los puntos dentro de la banda no modifican el '
    'resultado.')

parrafo(doc,
    'Para capturar relaciones complejas y no lineales entre las variables, el '
    'método utiliza una función matemática interna conocida como kernel de función '
    'de base radial. Esta función transforma los datos a un espacio de mayor '
    'complejidad donde las relaciones pueden ser capturadas de manera más efectiva, '
    'sin necesidad de definir explícitamente qué tipo de relación existe entre '
    'las variables.')

parrafo(doc,
    'Una característica importante de este método es su alta demanda computacional: '
    'a medida que crece el número de observaciones de entrenamiento, el tiempo '
    'necesario para ajustar el modelo crece de forma cuadrática o incluso cúbica. '
    'Esto obligó a limitar el número de muestras de entrenamiento para este método '
    'en los escenarios con más datos. En el escenario de quince minutos se usaron '
    'las últimas quince mil observaciones del conjunto de entrenamiento y en el de '
    'una hora las últimas diez mil. En el escenario diario, donde el total de '
    'datos de entrenamiento es de solo 1.122 registros, no fue necesario hacer '
    'ninguna restricción.')

doc.add_page_break()

# =============================================================================
# 8. CÓMO SE MIDIÓ EL RENDIMIENTO
# =============================================================================
titulo_seccion(doc, '8. Cómo se midió el rendimiento de los modelos', 1)
separador(doc)

parrafo(doc,
    'Para evaluar qué tan bien predice cada modelo se utilizaron cuatro métricas '
    'diferentes. Usar varias métricas en lugar de una sola es importante porque '
    'cada una captura un aspecto distinto del error de predicción y ninguna por sí '
    'sola cuenta la historia completa.')

titulo_seccion(doc, '8.1 Error cuadrático medio raíz', 2)

parrafo(doc,
    'La primera métrica se conoce como Error Cuadrático Medio Raíz, o por sus siglas '
    'en inglés RMSE. Se calcula elevando al cuadrado cada error individual, luego '
    'promediando todos esos cuadrados y finalmente sacando la raíz cuadrada del '
    'resultado. Al elevar los errores al cuadrado antes de promediar, los errores '
    'grandes quedan muy amplificados en el cálculo, lo que hace que esta métrica '
    'sea especialmente sensible a los casos donde el modelo se equivoca mucho. '
    'El resultado final está en las mismas unidades que el consumo eléctrico, es '
    'decir, en kilovatios. Un RMSE más pequeño indica mejor rendimiento.')

titulo_seccion(doc, '8.2 Error absoluto medio', 2)

parrafo(doc,
    'La segunda métrica es el Error Absoluto Medio, o MAE por sus siglas en inglés. '
    'Se calcula tomando la diferencia entre cada valor real y cada predicción, '
    'ignorando el signo de esa diferencia, y promediando todos esos valores. '
    'A diferencia del RMSE, esta métrica trata todos los errores por igual, sin '
    'amplificar los grandes. Es más fácil de interpretar: un MAE de 0,11 kilovatios '
    'significa que en promedio el modelo se equivoca en 0,11 kilovatios por '
    'predicción. Al igual que el RMSE, un valor más pequeño indica mejor rendimiento.')

titulo_seccion(doc, '8.3 Error porcentual absoluto medio', 2)

parrafo(doc,
    'La tercera métrica es el Error Porcentual Absoluto Medio, o MAPE. Calcula el '
    'error de cada predicción como un porcentaje del valor real, y luego promedia '
    'todos esos porcentajes. Su ventaja es que el resultado es independiente de las '
    'unidades y permite comparar el rendimiento entre escenarios donde los valores '
    'absolutos son diferentes. Un MAPE del quince por ciento significa que en promedio '
    'el modelo se equivoca en un quince por ciento del valor real de consumo. '
    'Se calcula únicamente en los casos donde el consumo real es mayor a cero para '
    'evitar divisiones por cero.')

titulo_seccion(doc, '8.4 Coeficiente de determinación', 2)

parrafo(doc,
    'La cuarta métrica es el Coeficiente de Determinación, conocido como R cuadrado '
    'o simplemente R². Esta métrica mide qué proporción de la variabilidad del consumo '
    'eléctrico logra explicar el modelo. Un valor de R² igual a uno significa que '
    'el modelo explica perfectamente toda la variabilidad. Un valor igual a cero '
    'significa que el modelo no explica nada más de lo que se podría obtener '
    'simplemente prediciendo siempre el consumo promedio. Valores negativos son '
    'posibles e indican que el modelo es peor que ese predictor trivial.')

parrafo(doc,
    'Esta métrica es particularmente útil porque es fácil de comunicar: un R² de '
    '0,91 significa que el modelo explica el 91 por ciento de la variación en el '
    'consumo eléctrico del hogar. Para predicción de series de tiempo energéticas, '
    'valores superiores a 0,90 se consideran excelentes, valores entre 0,80 y 0,90 '
    'son muy buenos y valores entre 0,70 y 0,80 son buenos y aceptables.')

doc.add_page_break()

# =============================================================================
# 9. AJUSTE DE PARÁMETROS
# =============================================================================
titulo_seccion(doc, '9. Cómo se ajustaron los parámetros de cada modelo', 1)
separador(doc)

titulo_seccion(doc, '9.1 Qué son los parámetros de configuración', 2)

parrafo(doc,
    'Cada uno de los tres métodos de predicción tiene una serie de opciones de '
    'configuración que no se aprenden automáticamente durante el entrenamiento, '
    'sino que deben ser definidas por el investigador antes de comenzar. Estas '
    'opciones se conocen como hiperparámetros y controlan aspectos como cuántos '
    'árboles construir, qué tan complejos pueden ser, cuán rígido es el margen '
    'de tolerancia o qué tan agresivas son las correcciones en cada iteración.')

parrafo(doc,
    'Elegir buenos valores para estos parámetros puede mejorar significativamente '
    'el rendimiento del modelo. Elegir valores inadecuados puede resultar en un '
    'modelo que se sobreajusta a los datos de entrenamiento y falla al predecir '
    'datos nuevos, o en uno que es demasiado simple y no captura los patrones '
    'relevantes. El proceso de encontrar la mejor combinación de estos parámetros '
    'se denomina ajuste o tuning.')

titulo_seccion(doc, '9.2 Búsqueda exhaustiva de parámetros', 2)

parrafo(doc,
    'Para encontrar la mejor combinación de parámetros, el estudio utilizó un '
    'método llamado búsqueda exhaustiva en grilla, conocido en inglés como '
    'GridSearchCV. Este método consiste en definir un conjunto de valores posibles '
    'para cada parámetro y luego probar sistemáticamente todas las combinaciones '
    'posibles, evaluando el rendimiento de cada una. Al final, selecciona la '
    'combinación que obtuvo el mejor resultado promedio.')

parrafo(doc,
    'Para el método Random Forest se definieron tres opciones de número de árboles, '
    'tres opciones de profundidad máxima y tres opciones de tamaño mínimo de grupo, '
    'lo que resultó en 27 combinaciones distintas. Para XGBoost se exploraron '
    '24 combinaciones entre número de árboles, profundidad, tasa de aprendizaje '
    'y porcentaje de datos usados en cada árbol. Para SVR se evaluaron 18 '
    'combinaciones entre los parámetros que controlan la penalización, el margen '
    'de tolerancia y el radio de influencia de cada punto.')

titulo_seccion(doc, '9.3 Validación cruzada con respeto al tiempo', 2)

parrafo(doc,
    'Evaluar cada combinación de parámetros directamente sobre el conjunto de prueba '
    'sería incorrecto, porque equivaldría a usar ese conjunto para tomar decisiones '
    'de diseño y su evaluación final ya no sería imparcial. En cambio, la evaluación '
    'de cada combinación se realizó dentro del propio conjunto de entrenamiento usando '
    'una técnica llamada validación cruzada.')

parrafo(doc,
    'La validación cruzada divide el conjunto de entrenamiento en varias partes '
    'y evalúa el rendimiento alternando cuál parte se usa para validar y cuáles '
    'para entrenar. Sin embargo, dado que los datos son una serie de tiempo, no '
    'es posible mezclarlos aleatoriamente: hacerlo permitiría que datos del futuro '
    'contaminen el entrenamiento. Por eso se utilizó una variante especial llamada '
    'validación cruzada temporal, que garantiza que en cada división la parte de '
    'evaluación sea siempre posterior en el tiempo a la parte de entrenamiento.')

parrafo(doc,
    'Se realizaron tres divisiones de este tipo. La combinación de parámetros que '
    'obtuvo el mejor resultado promedio en esas tres divisiones fue seleccionada '
    'como la configuración óptima. El modelo final fue entonces reentrenado con '
    'esa configuración usando todo el conjunto de entrenamiento completo, y se '
    'evaluó por última vez sobre el conjunto de prueba que había permanecido '
    'apartado durante todo el proceso.')

doc.add_page_break()

# =============================================================================
# 10. RESULTADOS
# =============================================================================
titulo_seccion(doc, '10. Los resultados obtenidos', 1)
separador(doc)

titulo_seccion(doc, '10.1 Resultados en el escenario de quince minutos', 2)

parrafo(doc,
    'En el escenario de quince minutos, el mejor rendimiento fue obtenido por '
    'Random Forest. Tras el ajuste de parámetros, este método logró un coeficiente '
    'de determinación de 0,9145, lo que significa que explica el 91,45 por ciento '
    'de la variabilidad en el consumo eléctrico del hogar. El error promedio por '
    'predicción fue de aproximadamente 0,11 kilovatios, y el error expresado como '
    'porcentaje del valor real fue de 14,76 por ciento.')

parrafo(doc,
    'XGBoost obtuvo resultados muy similares, con un coeficiente de determinación '
    'de 0,9131, a solo 0,0014 puntos del mejor resultado. SVR quedó en tercer '
    'lugar con un coeficiente de 0,8801, lo que sigue siendo un resultado muy '
    'bueno para predicción de series de tiempo. A esta resolución, tanto Random '
    'Forest como XGBoost aprovechan mejor el gran volumen de datos disponible: '
    'más de 106.000 registros de entrenamiento, lo que les permite construir '
    'modelos complejos y robustos.')

titulo_seccion(doc, '10.2 Resultados en el escenario de una hora', 2)

parrafo(doc,
    'En el escenario de una hora, el liderazgo pasó a XGBoost, que alcanzó un '
    'coeficiente de determinación de 0,8812. Este resultado es notable porque '
    'es exactamente igual al que obtenía antes del ajuste de parámetros, lo que '
    'indica que la configuración inicial ya era óptima para este escenario. '
    'Random Forest quedó muy cerca con 0,8754, y SVR obtuvo 0,8580.')

parrafo(doc,
    'Con menos datos disponibles, aproximadamente 27.000 registros de entrenamiento '
    'en lugar de 106.000, el enfoque de corrección progresiva de XGBoost demostró '
    'ser ligeramente más efectivo. La variabilidad entre períodos de una hora es '
    'mayor que entre períodos de quince minutos, y XGBoost captura mejor esas '
    'fluctuaciones mediante su mecanismo iterativo de aprendizaje.')

titulo_seccion(doc, '10.3 Resultados en el escenario de un día', 2)

parrafo(doc,
    'En el escenario diario, SVR logró el mejor resultado con un coeficiente de '
    'determinación de 0,7848 tras el ajuste de parámetros. Este fue también el '
    'escenario donde el ajuste de parámetros tuvo mayor impacto: antes del ajuste, '
    'SVR obtenía 0,7374 y tras él llegó a 0,7848, una mejora de casi cinco '
    'centésimas. XGBoost quedó en segundo lugar con 0,7748 y Random Forest '
    'en tercero con 0,7276.')

parrafo(doc,
    'La razón principal por la que SVR supera a los otros métodos en este escenario '
    'es la escasez de datos. Con apenas 1.122 registros de entrenamiento, los métodos '
    'basados en árboles tienen menos datos para aprender la variedad de patrones '
    'posibles y tienden a ajustarse demasiado a los datos que sí conocen. SVR, '
    'en cambio, está diseñado para funcionar bien con conjuntos pequeños porque '
    'su modelo depende únicamente de los puntos más representativos, ignorando '
    'el resto. El coeficiente de 0,7848 en el escenario diario es un resultado '
    'bueno considerando las limitaciones inherentes de ese escenario.')

titulo_seccion(doc, '10.4 El impacto del ajuste de parámetros', 2)

parrafo(doc,
    'El proceso de ajuste de parámetros tuvo efectos muy distintos según el método. '
    'Random Forest y XGBoost mostraron mejoras marginales o incluso ligeras caídas '
    'en algunos escenarios, lo que indica que sus configuraciones iniciales ya eran '
    'cercanas al óptimo. El ajuste simplemente confirmó que esas configuraciones '
    'eran adecuadas.')

parrafo(doc,
    'SVR fue el gran beneficiado del proceso. En el escenario de quince minutos '
    'mejoró en más de dos centésimas, en el de una hora en casi dos centésimas, '
    'y en el diario en casi cinco centésimas. Esto se explica porque la configuración '
    'inicial de SVR estaba definida con valores genéricos que no habían sido '
    'pensados específicamente para datos de consumo energético, mientras que la '
    'configuración encontrada por la búsqueda fue más conservadora y adecuada '
    'para la estructura particular de estos datos.')

doc.add_page_break()

# =============================================================================
# 11. CONCLUSIONES
# =============================================================================
titulo_seccion(doc, '11. Conclusiones del estudio', 1)
separador(doc)

titulo_seccion(doc, '11.1 Hallazgos principales', 2)

parrafo(doc,
    'El estudio llegó a conclusiones claras sobre qué método conviene usar según '
    'el horizonte temporal de predicción. Para predecir cada quince minutos, el '
    'método más adecuado es Random Forest, que logra explicar más del noventa por '
    'ciento de la variabilidad del consumo con un error relativo inferior al '
    'quince por ciento. Para predecir cada hora, XGBoost ofrece el mejor balance '
    'entre precisión y eficiencia, explicando el 88 por ciento de la variabilidad. '
    'Para predicción diaria, SVR demuestra ser el más efectivo gracias a su '
    'capacidad de generalizar bien con pocos datos.')

parrafo(doc,
    'Un hallazgo relevante del proceso de ajuste de parámetros es que los dos '
    'métodos basados en árboles, Random Forest y XGBoost, prácticamente no '
    'necesitaban ajuste: sus configuraciones iniciales ya producían resultados '
    'cercanos al óptimo. El ajuste sistemático tuvo mayor valor para SVR, cuyo '
    'rendimiento mejoró notablemente en todos los escenarios.')

titulo_seccion(doc, '11.2 Limitaciones del trabajo', 2)

parrafo(doc,
    'El estudio tiene varias limitaciones que es importante reconocer. En primer '
    'lugar, los resultados corresponden exclusivamente a un hogar residencial en '
    'Francia durante un período específico. No es posible garantizar que los mismos '
    'modelos y parámetros funcionen igual en hogares con distintos hábitos de '
    'consumo, distintos climas o distintos sistemas eléctricos.')

parrafo(doc,
    'En segundo lugar, las predicciones son siempre de un solo paso adelante, '
    'usando valores reales del pasado como entrada. En una aplicación real donde '
    'se quisiera predecir varios pasos hacia el futuro, habría que usar las '
    'predicciones anteriores del modelo como entrada para las siguientes, lo que '
    'acumula error progresivamente. Este escenario no fue evaluado en el presente '
    'trabajo.')

parrafo(doc,
    'En tercer lugar, la información del sub-medidor de cocina se perdió durante '
    'el proceso de limpieza de datos, lo que reduce la información disponible '
    'sobre el consumo en esa zona del hogar. Esta limitación está relacionada '
    'con la elección del método de eliminación de valores atípicos, que no es '
    'adecuado para variables con distribuciones muy concentradas en cero.')

titulo_seccion(doc, '11.3 Posibles extensiones del trabajo', 2)

parrafo(doc,
    'Entre las extensiones naturales de este trabajo se encuentra la incorporación '
    'de variables externas como la temperatura ambiente y los días festivos del '
    'calendario, que tienen un impacto conocido en el consumo eléctrico residencial '
    'pero no estaban disponibles en el conjunto de datos utilizado.')

parrafo(doc,
    'Otra extensión relevante sería la comparación con modelos de aprendizaje '
    'profundo, como las redes neuronales recurrentes, que son capaces de capturar '
    'dependencias temporales de forma automática sin necesidad de construir '
    'manualmente las variables de retraso. Esto permitiría evaluar si el mayor '
    'costo computacional de esos modelos se justifica con mejoras sustanciales '
    'en la predicción.')

parrafo(doc,
    'Finalmente, evaluar el rendimiento de los modelos con múltiples horizontes '
    'de predicción, es decir, predecir no solo el siguiente período sino también '
    'los dos, cuatro u ocho siguientes, permitiría entender mejor cómo se degrada '
    'la precisión al aumentar el tiempo de anticipación, lo cual es información '
    'valiosa para decisiones de planificación energética.')

doc.add_page_break()

# =============================================================================
# 12. GLOSARIO SIMPLE
# =============================================================================
titulo_seccion(doc, '12. Glosario de términos en lenguaje simple', 1)
separador(doc)

terminos_simples = [
    ('Algoritmo',
     'Secuencia de pasos matemáticos que sigue un computador para aprender patrones '
     'en los datos y hacer predicciones.'),
    ('Aprendizaje automático (Machine Learning)',
     'Rama de la computación en la que los sistemas aprenden a resolver tareas a '
     'partir de datos, sin ser programados con reglas explícitas.'),
    ('Coeficiente de determinación (R²)',
     'Número entre 0 y 1 que indica qué porcentaje de la variación en el consumo '
     'eléctrico logra explicar el modelo. Un R² de 0,90 significa que el modelo '
     'explica el 90 por ciento de esa variación.'),
    ('Conjunto de entrenamiento',
     'Porción de los datos que se le muestra al modelo para que aprenda patrones. '
     'En este estudio corresponde al 80 por ciento más antiguo de los datos.'),
    ('Conjunto de prueba',
     'Porción de los datos que se reserva y nunca se muestra al modelo durante '
     'el entrenamiento. Se usa solo al final para medir el rendimiento real. '
     'Corresponde al 20 por ciento más reciente de los datos.'),
    ('Contaminación de datos (Data Leakage)',
     'Error metodológico que ocurre cuando el modelo tiene acceso durante el '
     'entrenamiento a información del futuro. Genera resultados artificialmente '
     'buenos que no se reproducen en la práctica real.'),
    ('Estandarización',
     'Proceso de transformar los valores de una variable para que su promedio '
     'sea cero y su dispersión sea uniforme. Se aplica para que ninguna variable '
     'domine sobre otras por tener una escala numérica mayor.'),
    ('Escenario temporal',
     'Configuración del estudio que define cada cuánto tiempo se agrupan los '
     'datos y se realiza la predicción: cada 15 minutos, cada hora o cada día.'),
    ('Granularidad',
     'Nivel de detalle de las mediciones. Mayor granularidad significa intervalos '
     'de tiempo más cortos y más registros disponibles.'),
    ('Hiperparámetro',
     'Valor de configuración del modelo que el investigador define antes de entrenar, '
     'como el número de árboles o el margen de tolerancia. No se aprende de los datos.'),
    ('Ingeniería de características',
     'Proceso de crear nuevas variables de entrada a partir de los datos originales '
     'para ayudar al modelo a aprender patrones relevantes.'),
    ('Kernel de función de base radial',
     'Función matemática usada por SVR que mide la similitud entre puntos de datos '
     'y permite capturar relaciones complejas sin que el investigador deba definirlas '
     'explícitamente.'),
    ('Límite intercuartílico (IQR)',
     'Método estadístico para detectar valores extremos. Define un rango normal '
     'alrededor del centro de los datos y considera atípico todo lo que quede fuera.'),
    ('Overfitting (Sobreajuste)',
     'Problema que ocurre cuando un modelo aprende de memoria los datos de '
     'entrenamiento, incluyendo el ruido, y luego falla al predecir datos nuevos.'),
    ('Período de predicción (horizonte)',
     'Cuánto tiempo hacia el futuro predice el modelo. En este estudio es siempre '
     'de un paso adelante: el próximo período de 15 minutos, la próxima hora o '
     'el próximo día.'),
    ('Potencia activa (GAP)',
     'Cantidad de electricidad que realiza trabajo útil en el hogar. Es lo que '
     'aparece en la factura eléctrica. Es la variable que este estudio busca predecir.'),
    ('Random Forest',
     'Método de predicción que construye muchos árboles de decisión con muestras '
     'aleatorias de los datos y promedia sus resultados para mayor robustez.'),
    ('Resample',
     'Proceso de agrupar mediciones frecuentes (cada minuto) en intervalos más '
     'amplios (15 minutos, 1 hora, 1 día) calculando el promedio de cada grupo.'),
    ('Retraso temporal (Lag)',
     'Variable que representa el valor de consumo de períodos anteriores. '
     'Permite al modelo usar información histórica como base para predecir.'),
    ('SVR',
     'Método de predicción que busca una función ajustada dentro de una banda de '
     'tolerancia, usando solo los puntos más representativos del conjunto de datos.'),
    ('Sub-medidor',
     'Dispositivo que registra el consumo eléctrico de una zona específica del '
     'hogar, como la cocina, la lavandería o la calefacción.'),
    ('Tuning (ajuste de parámetros)',
     'Proceso de encontrar la configuración óptima del modelo probando '
     'sistemáticamente distintas combinaciones de hiperparámetros.'),
    ('Validación cruzada temporal',
     'Técnica que divide el conjunto de entrenamiento en varias partes para '
     'evaluar distintas configuraciones del modelo, garantizando siempre que '
     'los datos de evaluación sean posteriores en el tiempo a los de entrenamiento.'),
    ('Variabilidad',
     'Medida de cuánto varía el consumo eléctrico de un período a otro. Mayor '
     'variabilidad implica mayor dificultad para predecir.'),
    ('Ventana móvil (Rolling Window)',
     'Cálculo del promedio o la dispersión de los últimos N períodos de datos, '
     'actualizado en cada paso temporal para capturar la tendencia reciente.'),
    ('XGBoost',
     'Método de predicción que construye árboles de forma secuencial, donde '
     'cada uno corrige los errores del anterior de manera gradual y controlada.'),
]

for termino, definicion in terminos_simples:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(5)
    r1 = p.add_run(termino + '. ')
    r1.bold = True
    r1.font.color.rgb = RGBColor(0x1A, 0x23, 0x7E)
    p.add_run(definicion)

doc.add_page_break()

# =============================================================================
# 13. SÍNTESIS FINAL
# =============================================================================
titulo_seccion(doc, '13. Síntesis del trabajo en sus puntos esenciales', 1)
separador(doc)

parrafo(doc,
    'El trabajo parte de un conjunto de datos real con más de dos millones de '
    'mediciones eléctricas de un hogar en Francia, recopiladas durante cuatro años '
    'a razón de una medición por minuto. Estos datos fueron limpiados eliminando '
    'registros incompletos y valores extremos, resultando en 1.739.167 observaciones '
    'útiles.')

parrafo(doc,
    'A partir de esos datos se construyeron tres versiones del conjunto, cada una '
    'correspondiente a una escala de tiempo distinta: una con registros cada quince '
    'minutos, otra con registros cada hora y una tercera con registros diarios. '
    'Para cada versión se crearon variables de entrada que capturan el comportamiento '
    'pasado del consumo: valores de períodos anteriores, promedios recientes y '
    'características del momento del día y del año.')

parrafo(doc,
    'Los datos de cada escenario se dividieron en entrenamiento y prueba respetando '
    'el orden cronológico, destinando el 80 por ciento más antiguo a que los modelos '
    'aprendieran y el 20 por ciento más reciente a evaluar su rendimiento de forma '
    'imparcial.')

parrafo(doc,
    'Tres métodos de predicción fueron entrenados en cada escenario: Random Forest, '
    'que construye muchos árboles de decisión independientes y promedia sus '
    'respuestas; XGBoost, que construye árboles de forma secuencial donde cada '
    'uno corrige al anterior; y SVR, que ajusta una función dentro de una banda '
    'de tolerancia usando solo los puntos más representativos.')

parrafo(doc,
    'Los parámetros de configuración de cada método fueron optimizados mediante '
    'una búsqueda exhaustiva que probó todas las combinaciones posibles y los '
    'evaluó mediante validación cruzada con respeto al orden temporal.')

parrafo(doc,
    'Los resultados mostraron que a mayor frecuencia de predicción, mayor es la '
    'precisión alcanzable. En quince minutos, Random Forest explicó el 91,45 por '
    'ciento de la variabilidad del consumo. En una hora, XGBoost alcanzó el 88,12 '
    'por ciento. En predicción diaria, SVR logró el 78,48 por ciento. En todos '
    'los casos, el ajuste de parámetros benefició principalmente al método SVR, '
    'cuyas mejoras fueron las más notorias.')

parrafo(doc,
    'El trabajo concluye que la elección del método de predicción más adecuado '
    'depende del horizonte temporal requerido: los métodos basados en árboles '
    'son superiores cuando hay abundancia de datos y se predice a corto plazo, '
    'mientras que SVR es preferible cuando los datos son escasos y el horizonte '
    'es más amplio. Comparar sistemáticamente los tres métodos bajo las tres '
    'escalas de tiempo con el mismo protocolo experimental es la contribución '
    'metodológica central de este trabajo.')

# =============================================================================
# GUARDAR
# =============================================================================
doc.save(OUT_FILE)
print(f'\n{"="*60}')
print('DOCUMENTO NARRATIVO GENERADO EXITOSAMENTE')
print(f'{"="*60}')
print(f'\nArchivo: {OUT_FILE}')
print('\nSecciones:')
print('   1.  De qué trata el trabajo')
print('   2.  El conjunto de datos utilizado')
print('   3.  Cómo se prepararon los datos')
print('   4.  Los tres escenarios temporales')
print('   5.  Cómo se construyeron las variables de entrada')
print('   6.  Cómo se dividieron los datos')
print('   7.  Los tres métodos de predicción')
print('   8.  Cómo se midió el rendimiento')
print('   9.  Cómo se ajustaron los parámetros')
print('  10.  Los resultados obtenidos')
print('  11.  Conclusiones del estudio')
print('  12.  Glosario en lenguaje simple')
print('  13.  Síntesis final')
