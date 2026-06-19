# =============================================================================
# GUÍA DE GRÁFICOS — EXPLICACIÓN COMPLETA DE LAS 38 FIGURAS
# Para la exposición al tutor
# =============================================================================

import os
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

_here    = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = _here if os.path.exists(os.path.join(_here, 'datos')) else os.path.dirname(_here)
OUT_PATH = os.path.join(BASE_DIR, 'Guia_Graficos.docx')
GRAF_DIR = os.path.join(BASE_DIR, 'graficos')

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
    sizes = {1: Pt(16), 2: Pt(14), 3: Pt(12)}
    p = doc.add_heading(level=level)
    p.clear()
    r = p.add_run(text)
    r.font.name  = 'Times New Roman'
    r.font.bold  = True
    r.font.color.rgb = RGBColor(0, 0, 0)
    r.font.size  = sizes.get(level, Pt(12))
    p.alignment  = WD_ALIGN_PARAGRAPH.LEFT
    return p

def para(text, justify=True, size=12):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(size)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY if justify else WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_after = Pt(6)
    return p

def etiqueta(texto, color_rgb=(0, 70, 127)):
    p = doc.add_paragraph()
    r = p.add_run(texto)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    r.bold = True
    r.font.color.rgb = RGBColor(*color_rgb)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.space_before = Pt(6)
    return p

def cuerpo(text):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.left_indent = Cm(0.5)
    p.paragraph_format.space_after = Pt(4)
    return p

fig_num = [1]

def grafico(img_subpath, titulo_fig, que_muestra, como_leerlo, conclusion, que_decir, width=Inches(5.5)):
    img_path = os.path.join(GRAF_DIR, img_subpath)

    # Número y título
    heading(f'Figura {fig_num[0]} — {titulo_fig}', level=2)

    # Imagen
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(img_path, width=width)
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run(f'Figura {fig_num[0]}. {titulo_fig}')
        r_cap.font.name = 'Times New Roman'
        r_cap.font.size = Pt(10)
        r_cap.italic = True
        print(f'  ✓ Fig {fig_num[0]}: {titulo_fig[:55]}')
    else:
        p = doc.add_paragraph()
        r = p.add_run(f'[Imagen no encontrada: {img_path}]')
        r.font.color.rgb = RGBColor(200, 0, 0)
        r.font.size = Pt(10)
        print(f'  ⚠ Fig {fig_num[0]}: NO ENCONTRADA — {img_path}')

    doc.add_paragraph()

    etiqueta('¿Qué muestra este gráfico?')
    cuerpo(que_muestra)

    etiqueta('¿Cómo se lee?')
    cuerpo(como_leerlo)

    etiqueta('¿Qué conclusión se saca?')
    cuerpo(conclusion)

    etiqueta('¿Qué decirle al tutor?', color_rgb=(0, 100, 0))
    cuerpo(que_decir)

    doc.add_paragraph()
    fig_num[0] += 1


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

centered('GUÍA COMPLETA DE GRÁFICOS', 18)
doc.add_paragraph()
centered('Explicación de las 38 Figuras del Documento Final de Tesis', 14)
doc.add_paragraph()
centered('Modelo Predictivo del Consumo Energético en Hogares Inteligentes\nUsando Algoritmos de Machine Learning', 12, bold=False)
doc.add_paragraph()
centered('Documento de apoyo para la exposición al tutor', 11, bold=False)
doc.add_page_break()


# =============================================================================
# INTRODUCCIÓN
# =============================================================================
heading('Cómo usar esta guía')
para(
    'Este documento contiene los 38 gráficos del documento final de tesis, organizados '
    'en el mismo orden en que aparecen. Para cada gráfico se incluye: (1) qué muestra, '
    '(2) cómo se lee correctamente, (3) la conclusión que se extrae y (4) una sugerencia '
    'de qué decirle al tutor durante la exposición. Úsalo para estudiar cada figura '
    'antes de la presentación.'
)
doc.add_page_break()


# =============================================================================
# CAPÍTULO 1: EDA (Figuras 1–13)
# =============================================================================
print('\n[Capítulo 1] EDA — Figuras 1 a 13')
heading('Capítulo 1: Análisis Exploratorio de Datos (Figuras 1–13)')
doc.add_paragraph()

# ── Fig 1 ──
grafico(
    'eda/01_valores_nulos.png',
    'Análisis de Valores Nulos',
    que_muestra=(
        'Muestra cuántos valores nulos tiene cada variable del dataset original y en qué '
        'períodos del tiempo se concentran. El panel izquierdo muestra el porcentaje de '
        'nulos por variable. El panel derecho es un mapa de calor mensual que indica '
        'en qué meses hubo más datos faltantes.'
    ),
    como_leerlo=(
        'En el panel izquierdo, todas las barras llegan al mismo valor (1,252%), lo que '
        'significa que todas las variables tienen exactamente el mismo porcentaje de nulos. '
        'En el mapa de calor del panel derecho, los colores más oscuros indican más nulos '
        'en ese mes. Cada fila es una variable y cada columna es un mes del período 2006-2010.'
    ),
    conclusion=(
        'El hecho de que todas las variables tengan exactamente el mismo 1,252% de nulos '
        'confirma que los valores faltantes son bloques completos de tiempo sin medición '
        '(por ejemplo, apagones del medidor), no errores aislados por variable. Esto '
        'justifica usar dropna() para eliminarlos en lugar de imputarlos.'
    ),
    que_decir=(
        '"Como pueden observar en este gráfico, el porcentaje de nulos es idéntico en '
        'todas las variables —exactamente 1,252%—. Esto nos indica que los nulos no '
        'son errores aleatorios de medición sino períodos completos sin registro. Por '
        'esa razón decidimos eliminarlos directamente, ya que imputarlos habría '
        'significado inventar datos de consumo para períodos que en realidad no fueron medidos."'
    )
)

# ── Fig 2 ──
grafico(
    'eda/02_series_tiempo_principales.png',
    'Series Temporales de Variables Eléctricas Principales (GAP, GRP, VOLT, GI)',
    que_muestra=(
        'La evolución temporal de las cuatro variables eléctricas principales a lo largo '
        'de los cuatro años del dataset (2006-2010), promediadas a nivel diario para '
        'facilitar la visualización. Cada variable tiene su propio panel.'
    ),
    como_leerlo=(
        'El eje X es el tiempo (años). El eje Y es el valor promedio diario de cada '
        'variable en sus respectivas unidades (kW para GAP y GRP, V para VOLT, A para GI). '
        'Los picos hacia arriba indican períodos de mayor consumo o mayor voltaje.'
    ),
    conclusion=(
        'GAP muestra una clara estacionalidad anual: consumo alto en invierno '
        '(noviembre-febrero) y bajo en verano (junio-agosto), coherente con el clima '
        'francés. GI sigue una trayectoria prácticamente idéntica a GAP, anticipando '
        'la correlación casi perfecta que encontramos después (0,999). VOLT es relativamente '
        'estable durante todo el período, con pequeñas fluctuaciones.'
    ),
    que_decir=(
        '"Este gráfico nos muestra lo primero que observamos al explorar los datos: '
        'una estacionalidad anual muy marcada en el consumo. Los picos de GAP coinciden '
        'con los inviernos franceses. También noten cómo GI —la intensidad— sigue '
        'exactamente el mismo patrón que GAP, lo que nos llevó a decidir eliminarla '
        'como predictor porque ambas variables son prácticamente la misma información."'
    )
)

# ── Fig 3 ──
grafico(
    'eda/03_series_submedidores.png',
    'Series Temporales de Sub-medidores (SM1, SM2, SM3)',
    que_muestra=(
        'La evolución temporal de los tres sub-medidores del hogar: SM1 (cocina), '
        'SM2 (lavandería) y SM3 (calentador/aire acondicionado), promediados a nivel diario. '
        'Muestra qué circuitos del hogar contribuyen más al consumo y en qué épocas.'
    ),
    como_leerlo=(
        'Cada panel corresponde a un sub-medidor. El eje X es el tiempo y el eje Y '
        'es el consumo promedio diario en Wh. Los valores altos indican mayor uso '
        'de los electrodomésticos conectados a ese circuito.'
    ),
    conclusion=(
        'SM3 (calentador/AC) es el sub-medidor con mayor consumo y la estacionalidad '
        'invernal más pronunciada, lo que confirma que la calefacción eléctrica es el '
        'principal responsable del aumento de consumo en invierno. SM2 (lavandería) se '
        'mantiene relativamente constante. SM1 (cocina) quedó en cero tras el filtro IQR, '
        'lo cual es una limitación conocida del método.'
    ),
    que_decir=(
        '"Los sub-medidores nos cuentan una historia interesante. SM3, que corresponde '
        'al calentador de agua y aire acondicionado, tiene picos muy marcados en invierno, '
        'lo que confirma que la calefacción es el mayor consumidor estacional. SM1 '
        'aparece en cero porque su distribución es tan esparsa que el filtro IQR eliminó '
        'todos sus valores no-nulos — reconocemos esto como una limitación del método."'
    )
)

# ── Fig 4 ──
grafico(
    'eda/04_distribuciones.png',
    'Distribuciones Estadísticas de las Variables (Histogramas + KDE)',
    que_muestra=(
        'La distribución de frecuencias de cada una de las siete variables eléctricas. '
        'Cada panel contiene un histograma (barras) y una curva de densidad KDE (línea '
        'suave), más líneas verticales que marcan la media (rojo) y la mediana (naranja).'
    ),
    como_leerlo=(
        'El eje X es el valor de la variable y el eje Y es la frecuencia (cuántas veces '
        'aparece ese valor). Una distribución simétrica tiene media y mediana muy juntas. '
        'Cuando la cola derecha es más larga, la distribución es asimétrica positiva '
        '(sesgo a la derecha). KDE es una versión suavizada del histograma.'
    ),
    conclusion=(
        'GAP y GRP tienen distribuciones asimétricas hacia la derecha: la mayor parte '
        'del tiempo el consumo es bajo, pero ocasionalmente hay picos altos. VOLT tiene '
        'una distribución más simétrica y concentrada, propia de una red estable. Los '
        'sub-medidores tienen distribuciones muy esparsas con masa concentrada en cero, '
        'lo que refleja que la mayoría del tiempo esos electrodomésticos no están en uso.'
    ),
    que_decir=(
        '"Este gráfico nos muestra cómo se distribuyen los valores de cada variable. '
        'Lo más relevante es que GAP tiene una distribución con sesgo a la derecha: '
        'el hogar pasa la mayor parte del tiempo con consumo bajo, pero hay momentos '
        'picos de consumo alto. Esto es típico del consumo residencial. También vemos '
        'que el voltaje es muy estable —la distribución es estrecha y simétrica—, '
        'lo cual es esperable en una red eléctrica normal."'
    )
)

# ── Fig 5 ──
grafico(
    'eda/05_correlacion.png',
    'Matriz de Correlación de Pearson',
    que_muestra=(
        'Las correlaciones lineales entre todas las variables del dataset. El panel '
        'izquierdo es la matriz de correlación completa (todas las variables entre sí). '
        'El panel derecho muestra específicamente las correlaciones de cada variable con GAP.'
    ),
    como_leerlo=(
        'En la matriz, los colores van de azul intenso (correlación +1, perfectamente positiva) '
        'a rojo intenso (correlación −1, perfectamente negativa). El blanco indica correlación '
        'cercana a 0. Los números dentro de cada celda son el coeficiente de correlación de '
        'Pearson. En el panel derecho, las barras más largas indican mayor correlación con GAP.'
    ),
    conclusion=(
        'El hallazgo más importante es la correlación de 0,999 entre GI y GAP, '
        'prácticamente perfecta. SM3 tiene una correlación moderada con GAP (~0,60), '
        'siendo el sub-medidor más relacionado con el consumo total. GRP y VOLT tienen '
        'correlaciones moderadas-bajas con GAP. Esta información determinó qué variables '
        'conservar y cuáles eliminar en el modelado.'
    ),
    que_decir=(
        '"La matriz de correlación reveló algo fundamental para el diseño del modelo: '
        'GI y GAP tienen una correlación de 0,999, prácticamente 1. Eso significa que '
        'son la misma variable con distintas unidades de medida —una en amperios y la '
        'otra en kilovatios—. Mantener ambas en el modelo habría generado multicolinealidad '
        'severa sin agregar información, por eso GI fue eliminada en los tres escenarios."'
    )
)

# ── Fig 6 ──
grafico(
    'eda/06_patrones_temporales.png',
    'Patrones Temporales del Consumo (Hora, Día, Mes, Año)',
    que_muestra=(
        'El consumo promedio de GAP desagregado por cuatro dimensiones temporales: hora del '
        'día, día de la semana, mes del año y año. Cada panel muestra cómo varía el consumo '
        'promedio según esa dimensión temporal.'
    ),
    como_leerlo=(
        'Cada panel es un gráfico de barras o línea donde el eje X es la categoría temporal '
        '(hora 0-23, día 0=lunes a 6=domingo, mes 1-12, año) y el eje Y es el consumo '
        'promedio de GAP en kW. Los fines de semana aparecen resaltados en color distinto.'
    ),
    conclusion=(
        'Por hora: valle en madrugada (2-6h) y dos picos (7-9h matutino y 17-21h vespertino). '
        'Por día: consumo levemente mayor en fines de semana. Por mes: pico invernal claro '
        '(enero-febrero) y mínimo en verano (julio-agosto). Estos patrones justifican '
        'directamente las variables temporales que se construyen en el feature engineering.'
    ),
    que_decir=(
        '"Este gráfico es fundamental porque justifica las variables que construimos luego. '
        'Si el consumo no variara según la hora del día o el mes del año, no tendría sentido '
        'incluir esas variables como predictores. Pero aquí vemos claramente que sí varían: '
        'hay picos vespertinos, mayor consumo en fines de semana y una estacionalidad invernal '
        'muy marcada. Esto nos dice exactamente qué información temporal le debemos dar al modelo."'
    )
)

# ── Fig 7 ──
grafico(
    'eda/07_heatmap_hora_dia.png',
    'Mapa de Calor: Consumo por Hora del Día y Día de la Semana',
    que_muestra=(
        'Un mapa de calor que cruza dos dimensiones: la hora del día (eje horizontal, 0-23) '
        'y el día de la semana (eje vertical, lunes a domingo). Cada celda muestra el '
        'consumo promedio de GAP para esa combinación específica de hora y día.'
    ),
    como_leerlo=(
        'Los colores más intensos (más oscuros o más cálidos según la paleta) indican mayor '
        'consumo. Los más claros indican consumo bajo. Leyendo por filas se ve el patrón diario '
        'de consumo para un día específico. Leyendo por columnas se ve qué días de la semana '
        'tienen mayor consumo en una hora específica.'
    ),
    conclusion=(
        'Las noches del viernes y sábado tienen consumo más elevado y más sostenido hasta '
        'altas horas. Los horarios de madrugada (2-6h) son consistentemente los de menor '
        'consumo en todos los días. El patrón vespertino (17-21h) es más pronunciado entre '
        'semana que los fines de semana.'
    ),
    que_decir=(
        '"Este mapa de calor nos permite ver simultáneamente el efecto de la hora y el día '
        'de la semana. Lo más interesante es que el patrón no es igual para todos los días: '
        'los viernes y sábados tienen consumo nocturno más alto que los lunes. Esto confirma '
        'que la variable "es_finde" que incluimos en el feature engineering captura una '
        'diferencia real en el comportamiento del hogar."'
    )
)

# ── Fig 8 ──
grafico(
    'eda/08_boxplot_mensual.png',
    'Distribución Mensual del Consumo (Boxplots por Mes)',
    que_muestra=(
        'La distribución estadística del consumo de GAP para cada mes del año, representada '
        'mediante diagramas de caja (boxplots). Permite ver no solo el promedio mensual sino '
        'también la variabilidad y los valores extremos de cada mes.'
    ),
    como_leerlo=(
        'Cada caja representa el 50% central de los datos (entre el percentil 25 y 75). '
        'La línea horizontal dentro de la caja es la mediana. Los "bigotes" se extienden '
        'hasta 1,5 veces el IQR. Los puntos fuera de los bigotes son valores atípicos. '
        'Cuanto más alta la caja, mayor el consumo típico de ese mes.'
    ),
    conclusion=(
        'La estacionalidad anual es muy evidente: enero y febrero tienen las medianas más '
        'altas y también la mayor variabilidad (cajas más anchas). Julio y agosto tienen las '
        'medianas más bajas. También se observa que los meses de invierno tienen más valores '
        'atípicos hacia arriba, indicando que los picos de consumo son más frecuentes en esa época.'
    ),
    que_decir=(
        '"Los boxplots mensuales complementan al gráfico anterior mostrando no solo el '
        'promedio sino también la dispersión del consumo. Enero y febrero no solo tienen '
        'mayor consumo promedio sino también mayor variabilidad: algunos días de invierno '
        'el hogar consume muchísimo y otros días menos. Esto refleja el comportamiento '
        'real de la calefacción, que se usa más en los días más fríos."'
    )
)

# ── Fig 9 ──
grafico(
    'eda/09_boxplot_antes.png',
    'Distribución de Variables ANTES del Tratamiento de Outliers',
    que_muestra=(
        'Diagramas de caja de las siete variables eléctricas en su estado original, antes '
        'de aplicar el filtro IQR. Muestra la presencia de valores atípicos (outliers) '
        'en cada variable.'
    ),
    como_leerlo=(
        'Los puntos dispersos que aparecen por encima o por debajo de los bigotes de cada '
        'caja son los valores atípicos. Cuantos más puntos haya y más alejados estén de la '
        'caja, más problemáticos son los outliers. Los bigotes muy largos también indican '
        'presencia de valores extremos.'
    ),
    conclusion=(
        'Se observan valores extremos en todas las variables, especialmente en GAP, GRP y GI. '
        'Estos valores pueden corresponder a mediciones erróneas, picos de consumo muy inusuales '
        'o artefactos del sistema de medición. Su presencia justifica aplicar un filtro de '
        'outliers antes del modelado.'
    ),
    que_decir=(
        '"Este gráfico muestra por qué necesitábamos tratar los outliers. Pueden verse puntos '
        'muy alejados de las cajas, especialmente en GAP. Esos valores extremos podrían '
        'sesgar el entrenamiento de los modelos, haciendo que el algoritmo aprenda a predecir '
        'esos casos raros en lugar de aprender el comportamiento típico del hogar."'
    )
)

# ── Fig 10 ──
grafico(
    'eda/10_boxplot_despues.png',
    'Distribución de Variables DESPUÉS del Tratamiento de Outliers',
    que_muestra=(
        'Los mismos diagramas de caja que la figura anterior pero después de aplicar el '
        'filtro IQR. Permite comparar directamente el efecto del tratamiento de outliers '
        'sobre la distribución de cada variable.'
    ),
    como_leerlo=(
        'La comparación directa con la figura anterior es lo más importante. Si las cajas '
        'son más compactas y hay menos puntos extremos, el filtro funcionó correctamente. '
        'Las distribuciones deberían ser más "limpias" y representativas del comportamiento típico.'
    ),
    conclusion=(
        'Tras el filtro IQR, las distribuciones son notablemente más compactas y los valores '
        'extremos han sido eliminados. El dataset resultante tiene 1.739.167 registros, '
        'habiendo eliminado el 16,18% de los registros originales (post-dropna). Las '
        'distribuciones ahora representan mejor el comportamiento típico del hogar.'
    ),
    que_decir=(
        '"Después del filtro IQR, las distribuciones son mucho más compactas. Eliminamos '
        'el 16,18% de los registros, quedando con 1.739.167 observaciones. Este es nuestro '
        'dataset limpio, que exportamos como dataset_limpio.csv y que es el punto de partida '
        'para todos los modelos. La mejora en la calidad de los datos justifica el costo '
        'de reducir el tamaño del dataset."'
    )
)

# ── Fig 11 ──
grafico(
    'eda/11_descomposicion_estacional.png',
    'Descomposición Estacional Aditiva de GAP (Período 365 días)',
    que_muestra=(
        'La descomposición de la serie diaria de GAP en tres componentes separados: '
        'tendencia (trend), estacionalidad (seasonal) y residuo (residual). Permite '
        'entender cuánto de la variación del consumo se debe a cada componente.'
    ),
    como_leerlo=(
        'El gráfico tiene cuatro paneles de arriba hacia abajo: (1) la serie original, '
        '(2) la tendencia (variación de largo plazo suavizada), (3) la componente estacional '
        '(patrón repetitivo anual) y (4) el residuo (lo que no explican tendencia ni estacionalidad). '
        'Cada panel tiene su propia escala en el eje Y.'
    ),
    conclusion=(
        'La tendencia muestra un leve descenso del consumo promedio hacia 2009-2010. '
        'La componente estacional confirma el patrón anual con amplitudes de ±0,3 kW. '
        'El residuo es de baja magnitud y sin estructura aparente, lo que indica que '
        'tendencia y estacionalidad explican la mayor parte de la variación.'
    ),
    que_decir=(
        '"La descomposición estacional nos permite separar "capas" de la serie temporal. '
        'La tendencia nos muestra que el consumo disminuye levemente a lo largo de los años, '
        'posiblemente por eficiencia energética. La componente estacional confirma el patrón '
        'anual con una amplitud de aproximadamente 0,3 kW. Y el residuo es pequeño, lo que '
        'es buena señal: significa que la serie tiene estructura predecible, no es puro ruido."'
    )
)

# ── Fig 12 ──
grafico(
    'eda/12_acf_pacf.png',
    'Funciones de Autocorrelación (ACF y PACF) de la Serie Horaria de GAP',
    que_muestra=(
        'La ACF (Autocorrelation Function) y la PACF (Partial Autocorrelation Function) '
        'de la serie horaria de GAP. Muestran con qué fuerza se correlaciona el consumo '
        'actual con los consumos pasados en distintos horizontes de tiempo.'
    ),
    como_leerlo=(
        'El eje X son los lags (períodos hacia atrás). El eje Y es el coeficiente de '
        'correlación (-1 a 1). Las líneas azules punteadas son los intervalos de confianza '
        'al 95%: una barra que supera esas líneas indica una correlación estadísticamente '
        'significativa. La ACF muestra correlaciones totales; la PACF muestra correlaciones '
        'directas descontando los efectos intermedios.'
    ),
    conclusion=(
        'La ACF muestra correlaciones significativas en múltiplos de 24 lags (24 horas), '
        'confirmando la fuerte estacionalidad diaria. Las correlaciones decaen lentamente, '
        'indicando memoria de largo plazo. La PACF muestra que los lags más cercanos (1, 2, 3h) '
        'son los que tienen mayor correlación directa. Estos resultados guiaron directamente '
        'la selección de lags en el feature engineering.'
    ),
    que_decir=(
        '"La ACF y PACF son el fundamento matemático detrás de la selección de lags. '
        'Cuando vemos una barra en lag 24 que supera las líneas de confianza, eso nos dice '
        'que el consumo de hace 24 horas tiene correlación estadísticamente significativa '
        'con el consumo actual. Eso justifica incluir GAP_lag_24 como predictor. '
        'Sin este análisis, la selección de lags habría sido arbitraria."'
    )
)

# ── Fig 13 ──
grafico(
    'eda/13_submedidores_participacion.png',
    'Participación de Sub-medidores en el Consumo Total',
    que_muestra=(
        'La contribución porcentual de cada sub-medidor al consumo total del hogar. '
        'El panel izquierdo es un gráfico de torta con la distribución acumulada del '
        'período completo. El panel derecho muestra cómo evoluciona la participación '
        'relativa de cada sub-medidor mes a mes.'
    ),
    como_leerlo=(
        'En la torta, cada sector es la proporción del consumo total atribuida a ese '
        'sub-medidor (y "otros circuitos" es lo que no está monitorizado). En el gráfico '
        'de líneas del panel derecho, cada línea es un sub-medidor y el eje Y es el '
        'porcentaje de participación en ese mes.'
    ),
    conclusion=(
        'Una proporción importante del consumo corresponde a "otros circuitos" no monitorizados '
        '(iluminación, electrónica, etc.). SM3 es el circuito medido con mayor participación '
        'y esta participación aumenta marcadamente en invierno por la calefacción. SM2 se '
        'mantiene más constante durante el año. SM1 tiene participación mínima.'
    ),
    que_decir=(
        '"Este gráfico nos muestra que los sub-medidores no cubren todo el consumo del hogar: '
        'una porción importante corresponde a circuitos no monitorizados como iluminación y '
        'electrónica. Entre los sub-medidores, SM3 es el más relevante y su participación '
        'aumenta mucho en invierno —hasta casi duplicarse— lo que confirma que la calefacción '
        'eléctrica es el principal driver del patrón estacional."'
    )
)

doc.add_page_break()


# =============================================================================
# CAPÍTULO 2: REMUESTREO (Figuras 14–16)
# =============================================================================
print('\n[Capítulo 2] Remuestreo — Figuras 14 a 16')
heading('Capítulo 2: Series Temporales por Escenario (Figuras 14–16)')
doc.add_paragraph()

# ── Fig 14 ──
grafico(
    'escenario1/e1_01_serie_resampleada.png',
    'Serie GAP Remuestreada a 15 Minutos',
    que_muestra=(
        'La serie temporal de GAP después de agregar los datos de 1 minuto a intervalos '
        'de 15 minutos, visualizada como promedio diario para mejorar la legibilidad. '
        'Muestra el conjunto de entrenamiento y el de prueba separados por una línea vertical.'
    ),
    como_leerlo=(
        'El eje X es el tiempo (2006-2010) y el eje Y es el consumo promedio de GAP en kW. '
        'La línea vertical roja (o de otro color destacado) marca el inicio del conjunto de '
        'prueba: todo lo que está a la izquierda es el 80% de entrenamiento y todo lo que '
        'está a la derecha es el 20% de prueba.'
    ),
    conclusion=(
        'El Escenario 1 tiene 133.489 observaciones después del feature engineering. '
        'El conjunto de entrenamiento tiene 106.791 registros y el de prueba 26.698. '
        'La estacionalidad anual es visible incluso a esta resolución. La división '
        'cronológica garantiza que el modelo aprende del pasado y predice el futuro.'
    ),
    que_decir=(
        '"Esta figura muestra la serie del Escenario 1 ya remuestreada a 15 minutos. '
        'La línea vertical separa entrenamiento y prueba. El modelo aprende todo lo que '
        'está a la izquierda de esa línea —los primeros cuatro años de datos— y luego '
        'se evalúa en lo que está a la derecha, que son los últimos meses del período. '
        'Nunca ve los datos de prueba durante el entrenamiento."'
    )
)

# ── Fig 15 ──
grafico(
    'escenario2/e2_01_serie_resampleada.png',
    'Serie GAP Remuestreada a 1 Hora',
    que_muestra=(
        'La serie temporal de GAP después de agregar los datos a intervalos de 1 hora, '
        'visualizada como promedio diario. Tiene 34.007 observaciones totales y la '
        'misma división cronológica 80/20.'
    ),
    como_leerlo=(
        'Igual que la figura anterior pero con menor número de puntos (24 por día en lugar '
        'de 96). La serie aparece más suavizada porque cada valor es el promedio de 60 '
        'minutos de mediciones. Los patrones estacionales anuales son aún más visibles '
        'por el efecto de suavizado.'
    ),
    conclusion=(
        'El Escenario 2 tiene 27.205 registros de entrenamiento y 6.802 de prueba. '
        'La menor resolución temporal hace que la serie sea más suave que en el Escenario 1, '
        'lo que puede facilitar o dificultar la predicción dependiendo del modelo. '
        'Es el escenario intermedio entre detalle y volumen de datos.'
    ),
    que_decir=(
        '"La serie horaria es visualmente más suave que la de 15 minutos porque cada '
        'punto agrega 60 lecturas del sensor. Con 34.007 observaciones, tenemos suficiente '
        'volumen para entrenar los modelos, pero menos que en el Escenario 1. La '
        'estacionalidad anual se aprecia aún con más claridad en esta resolución."'
    )
)

# ── Fig 16 ──
grafico(
    'escenario3/e3_01_serie_resampleada.png',
    'Serie GAP Remuestreada a 1 Día',
    que_muestra=(
        'La serie temporal de GAP agregada a nivel diario, con solo 1.433 observaciones '
        'totales (una por día). Es la representación más compacta del consumo, donde '
        'cada punto es el promedio de los 1.440 minutos del día.'
    ),
    como_leerlo=(
        'El eje X es el tiempo y el eje Y es el consumo promedio diario en kW. '
        'Con solo 1.433 puntos, cada punto visible en el gráfico es un día real. '
        'La estacionalidad anual se aprecia con gran claridad a esta escala. '
        'La línea vertical indica el inicio de los 287 días de prueba.'
    ),
    conclusion=(
        'El Escenario 3 tiene solo 1.146 días de entrenamiento y 287 de prueba. '
        'Esta es la principal limitación de este escenario: los modelos tienen mucho '
        'menos historia para aprender. Sin embargo, la estacionalidad anual es muy '
        'clara y los patrones son más regulares y predecibles a escala diaria.'
    ),
    que_decir=(
        '"El escenario diario es el más desafiante precisamente porque tiene muy pocos datos. '
        'Con 1.146 días de entrenamiento —menos de 4 años— el modelo tiene que aprender '
        'a predecir el consumo diario con escasa información. Eso explica el R² más bajo '
        'que obtenemos en este escenario comparado con los otros dos. A cambio, tiene '
        'la mayor utilidad práctica para planificación energética a mediano plazo."'
    )
)

doc.add_page_break()


# =============================================================================
# CAPÍTULO 5: RESULTADOS POR ESCENARIO (Figuras 17–28)
# =============================================================================
print('\n[Capítulo 5] Resultados por Escenario — Figuras 17 a 28')
heading('Capítulo 5: Modelos y Resultados por Escenario (Figuras 17–28)')
doc.add_paragraph()

heading('Escenario 1 — 15 Minutos', level=2)
doc.add_paragraph()

# ── Fig 17 ──
grafico(
    'escenario1/e1_02_predicciones.png',
    'Predicciones vs Valores Reales — Escenario 1 (15 min)',
    que_muestra=(
        'Una comparación visual entre los valores reales de GAP (línea de un color) y '
        'las predicciones de los tres modelos (líneas de colores distintos) para los '
        'primeros 500 puntos del conjunto de prueba. Permite ver qué tan bien siguen '
        'los modelos la serie real.'
    ),
    como_leerlo=(
        'El eje X son los primeros 500 períodos de 15 minutos del conjunto de prueba '
        '(equivale a aproximadamente 5 días). El eje Y es el valor de GAP en kW. '
        'Cuanto más cerca estén las líneas de predicción de la línea real, mejor es el modelo. '
        'Las desviaciones visibles son los errores de predicción.'
    ),
    conclusion=(
        'RF y XGBoost siguen de cerca la serie real, capturando tanto los picos como '
        'los valles del consumo. SVR muestra mayor desviación, especialmente en los picos. '
        'Los tres modelos capturan bien el patrón general del consumo, aunque con diferencias '
        'en la precisión de los picos más extremos.'
    ),
    que_decir=(
        '"Este gráfico es una de las formas más intuitivas de visualizar el rendimiento del '
        'modelo. Cuando la línea de predicción sigue de cerca a la línea real, el modelo '
        'está funcionando bien. Pueden ver que RF y XGBoost prácticamente se superponen '
        'a la serie real, mientras que SVR tiende a suavizar los picos. Esto es coherente '
        'con los R² que obtuvimos: 0,91 para RF y XGB, y 0,86 para SVR."'
    )
)

# ── Fig 18 ──
grafico(
    'escenario1/e1_03_scatter.png',
    'Gráfico de Dispersión Predicho vs Real — Escenario 1 (15 min)',
    que_muestra=(
        'Gráficos de dispersión donde cada punto representa una observación del conjunto '
        'de prueba. El eje X es el valor real de GAP y el eje Y es el valor predicho por '
        'el modelo. Hay un panel por modelo (RF, XGBoost, SVR).'
    ),
    como_leerlo=(
        'La línea diagonal punteada representa la predicción perfecta (predicho = real). '
        'Cuanto más concentrada esté la nube de puntos alrededor de esa diagonal, mejor '
        'es el modelo. Los puntos alejados de la diagonal son errores grandes. '
        'Si los puntos están por encima de la diagonal, el modelo sobreestima; si están '
        'por debajo, subestima.'
    ),
    conclusion=(
        'RF y XGBoost muestran nubes de puntos muy concentradas alrededor de la diagonal, '
        'con R² de 0,9144 y 0,9198 respectivamente. SVR tiene mayor dispersión, especialmente '
        'para valores altos de GAP donde tiende a subestimar los picos. Este gráfico confirma '
        'visualmente los coeficientes R² calculados.'
    ),
    que_decir=(
        '"El scatter plot es otra forma de validar los resultados. Un modelo perfecto tendría '
        'todos los puntos exactamente sobre la diagonal. En RF y XGBoost la nube está muy '
        'concentrada alrededor de esa línea. SVR tiene más dispersión, especialmente para '
        'valores altos de consumo —el modelo tiende a subestimar los picos, que son los '
        'momentos más difíciles de predecir."'
    )
)

# ── Fig 19 ──
grafico(
    'escenario1/e1_04_metricas.png',
    'Comparación de Métricas — Escenario 1 (15 min)',
    que_muestra=(
        'Un gráfico de barras que compara las cuatro métricas de evaluación (RMSE, MAE, '
        'MAPE y R²) entre los tres modelos en el Escenario 1. Permite comparar de un '
        'vistazo el rendimiento relativo de cada algoritmo.'
    ),
    como_leerlo=(
        'Cada grupo de barras corresponde a una métrica. Dentro de cada grupo hay tres '
        'barras, una por modelo (RF, XGBoost, SVR). Para RMSE, MAE y MAPE, las barras '
        'más cortas son mejores (menos error). Para R², las barras más largas son mejores '
        '(mayor proporción de varianza explicada).'
    ),
    conclusion=(
        'XGBoost lidera en RMSE (0,1949) y R² (0,9198). RF es muy competitivo. SVR '
        'queda rezagado, especialmente en MAPE (24,25% vs ~15% de RF y XGB). La diferencia '
        'entre RF y XGB es pequeña, pero entre ambos y SVR es significativa en la configuración base.'
    ),
    que_decir=(
        '"Este gráfico de métricas nos permite comparar los tres modelos de forma objetiva. '
        'En todas las métricas, RF y XGBoost son superiores a SVR en su configuración base. '
        'El MAPE de SVR del 24% en el Escenario 1 es el resultado más preocupante —significa '
        'que en promedio el error es del 24% del valor real—. Esto motiva el ajuste de '
        'hiperparámetros que hacemos después."'
    )
)

# ── Fig 20 ──
grafico(
    'escenario1/e1_05_importancia.png',
    'Importancia de Features — Escenario 1 (15 min)',
    que_muestra=(
        'Las 15 features más importantes según Random Forest y XGBoost en el Escenario 1. '
        'Muestra qué variables tienen mayor influencia en las predicciones de cada modelo. '
        'Hay un panel por modelo.'
    ),
    como_leerlo=(
        'Las barras horizontales representan la importancia relativa de cada feature. '
        'Las barras más largas corresponden a las variables que más peso tienen en las '
        'predicciones. La suma de todas las importancias es 1 (o 100%). Las variables '
        'están ordenadas de mayor a menor importancia.'
    ),
    conclusion=(
        'Los rezagos recientes de GAP (GAP_lag_1, GAP_lag_2) y las medias móviles de '
        'largo alcance (GAP_roll_mean_96, equivalente a 24 horas) dominan en ambos modelos. '
        'Las variables temporales (hora, dia_semana) tienen importancia moderada. '
        'Las variables eléctricas (GRP, SM3) contribuyen pero de forma secundaria.'
    ),
    que_decir=(
        '"La importancia de features nos dice qué variables son las más útiles para '
        'predecir el consumo. El resultado más claro es que el consumo reciente —lo que '
        'pasó en los últimos 15 minutos o en las últimas horas— es el predictor más '
        'potente. Esto tiene mucho sentido: si el consumo fue alto en los últimos 15 '
        'minutos, probablemente seguirá siendo alto en el siguiente cuarto de hora."'
    )
)

doc.add_paragraph()
heading('Escenario 2 — 1 Hora', level=2)
doc.add_paragraph()

# ── Fig 21 ──
grafico(
    'escenario2/e2_02_predicciones.png',
    'Predicciones vs Valores Reales — Escenario 2 (1 hora)',
    que_muestra=(
        'Comparación entre valores reales y predicciones de los tres modelos para los '
        'primeros 500 puntos del conjunto de prueba del Escenario 2. A resolución horaria, '
        'cada punto representa el consumo promedio de una hora completa.'
    ),
    como_leerlo=(
        'El eje X son los primeros 500 períodos horarios del conjunto de prueba '
        '(equivale a aproximadamente 20 días). El eje Y es GAP en kW. La serie horaria '
        'es más suave que la de 15 minutos, por lo que los picos y valles son menos abruptos.'
    ),
    conclusion=(
        'Los tres modelos siguen bien la tendencia general. RF y XGBoost capturan con '
        'precisión los picos y valles diarios. SVR muestra mayor suavizado, especialmente '
        'en los picos de consumo. La mayor suavidad de la serie horaria facilita la '
        'predicción respecto a los 15 minutos.'
    ),
    que_decir=(
        '"La serie horaria es más suave y los modelos la siguen bien. Noten que los picos '
        'y valles son menos abruptos que en el escenario de 15 minutos: esto es porque '
        'cada punto agrega 60 lecturas y el promedio suaviza el ruido de corto plazo. '
        'XGBoost y RF capturan incluso los ciclos diarios con bastante fidelidad."'
    )
)

# ── Fig 22 ──
grafico(
    'escenario2/e2_03_scatter.png',
    'Gráfico de Dispersión Predicho vs Real — Escenario 2 (1 hora)',
    que_muestra=(
        'Gráficos de dispersión del conjunto de prueba del Escenario 2, con los valores '
        'reales en el eje X y los predichos en el eje Y. Uno por modelo.'
    ),
    como_leerlo=(
        'Igual que el scatter plot del Escenario 1. La diagonal es la predicción perfecta. '
        'Concentración alrededor de la diagonal = buen modelo. Puntos alejados = errores grandes. '
        'Patrones sistemáticos (curvatura) indicarían sesgo del modelo.'
    ),
    conclusion=(
        'Los tres modelos muestran buena concentración alrededor de la diagonal. XGBoost '
        'y RF tienen la mayor concentración. SVR también muestra buen ajuste en este '
        'escenario aunque con algo más de dispersión que los otros dos. No se observan '
        'patrones sistemáticos que indiquen sesgo significativo.'
    ),
    que_decir=(
        '"En el escenario horario los tres modelos muestran scatter plots más concentrados '
        'que en el de 15 minutos. Esto tiene sentido porque la serie es más suave y '
        'predecible. SVR también mejora su dispersión respecto al escenario anterior, '
        'lo que adelanta que el modelo se adapta mejor a resoluciones más gruesas."'
    )
)

# ── Fig 23 ──
grafico(
    'escenario2/e2_04_metricas.png',
    'Comparación de Métricas — Escenario 2 (1 hora)',
    que_muestra=(
        'Comparación de las cuatro métricas de evaluación entre los tres modelos para '
        'el Escenario 2. Permite ver quién lidera en cada métrica a resolución horaria.'
    ),
    como_leerlo=(
        'Mismo esquema que el gráfico de métricas del Escenario 1: barras más cortas '
        'son mejores para RMSE/MAE/MAPE y barras más largas son mejores para R².'
    ),
    conclusion=(
        'XGBoost lidera con R²=0,8812 y MAPE de 16,98%. RF obtiene R²=0,8751 con '
        'MAPE de 17,43%, muy competitivo. SVR mejora considerablemente respecto al '
        'Escenario 1 en términos relativos, con R²=0,8415, pero aún es el de menor '
        'rendimiento entre los tres.'
    ),
    que_decir=(
        '"A resolución horaria, XGBoost lidera con R²=0,8812. La diferencia con RF '
        'es pequeña (solo 0,006 de R²), pero SVR queda algo más atrás con 0,8415. '
        'Un resultado interesante es que SVR reduce su MAPE de 24,25% en el Escenario 1 '
        'a 20,56% aquí, mostrando que el modelo se desempeña relativamente mejor '
        'en resoluciones temporales más gruesas."'
    )
)

# ── Fig 24 ──
grafico(
    'escenario2/e2_05_importancia.png',
    'Importancia de Features — Escenario 2 (1 hora)',
    que_muestra=(
        'Las 15 features más importantes para RF y XGBoost en el Escenario 2. '
        'Permite ver qué información del pasado es más útil para predecir el consumo '
        'de la próxima hora.'
    ),
    como_leerlo=(
        'Mismo esquema que la figura de importancia del Escenario 1. Las barras '
        'horizontales indican la importancia relativa de cada variable.'
    ),
    conclusion=(
        'GAP_lag_1 (consumo de hace 1 hora) es la feature más importante en ambos modelos, '
        'seguida de GAP_lag_24 (consumo de hace 24 horas, mismo período del día anterior). '
        'Las medias móviles de 24 y 168 horas también son relevantes. Las variables '
        'temporales tienen importancia moderada pero consistente.'
    ),
    que_decir=(
        '"En el escenario horario, el lag de 1 hora domina claramente: lo más útil para '
        'predecir el consumo de la próxima hora es saber qué pasó en la última hora. '
        'El segundo lag más importante es el de 24 horas —lo que pasó exactamente a '
        'esta hora del día anterior—, lo que refleja el patrón diario repetitivo '
        'del comportamiento del hogar."'
    )
)

doc.add_paragraph()
heading('Escenario 3 — 1 Día', level=2)
doc.add_paragraph()

# ── Fig 25 ──
grafico(
    'escenario3/e3_02_predicciones.png',
    'Predicciones vs Valores Reales — Escenario 3 (1 día)',
    que_muestra=(
        'Comparación entre valores reales y predicciones de los tres modelos para '
        'el conjunto de prueba completo del Escenario 3 (287 días). A diferencia '
        'de los escenarios anteriores, se muestra el conjunto de prueba completo '
        'porque es manejable en tamaño.'
    ),
    como_leerlo=(
        'El eje X son los 287 días del conjunto de prueba y el eje Y es el consumo '
        'promedio diario en kW. Cada punto en el eje X es un día. Se pueden observar '
        'los picos invernales y los valles estivales dentro del período de prueba.'
    ),
    conclusion=(
        'Los tres modelos siguen la tendencia general correctamente. La estacionalidad '
        'anual es visible en el conjunto de prueba. Los errores más grandes ocurren en '
        'los picos de consumo invernal, donde los modelos tienden a subestimar los valores '
        'extremos. SVR y XGBoost muestran el mejor seguimiento global.'
    ),
    que_decir=(
        '"Para el escenario diario mostramos el conjunto de prueba completo —287 días— '
        'porque es manejable. Pueden verse claramente los picos de consumo invernal '
        'y los valles de verano. Los modelos capturan bien la tendencia general, aunque '
        'los picos extremos tienden a ser subestimados, lo cual es un comportamiento '
        'típico de los modelos de ML basados en árboles."'
    )
)

# ── Fig 26 ──
grafico(
    'escenario3/e3_03_scatter.png',
    'Gráfico de Dispersión Predicho vs Real — Escenario 3 (1 día)',
    que_muestra=(
        'Gráficos de dispersión del conjunto de prueba del Escenario 3. Muestra la '
        'relación entre los valores diarios reales y los predichos por cada modelo.'
    ),
    como_leerlo=(
        'Igual que los scatter plots anteriores. La diferencia visible respecto a los '
        'escenarios anteriores es que la nube de puntos puede estar más dispersa, '
        'reflejando el menor R² de este escenario.'
    ),
    conclusion=(
        'La dispersión es mayor que en los escenarios anteriores, coherente con los R² '
        'de 0,73-0,78. Los modelos no subestiman sistemáticamente, pero hay más varianza '
        'en el error. El escenario diario es intrínsecamente más difícil de predecir '
        'con solo 1.146 registros de entrenamiento.'
    ),
    que_decir=(
        '"Noten que la nube de puntos está más dispersa respecto a los escenarios anteriores. '
        'Esto es consistente con los R² más bajos que obtenemos (0,73-0,78 vs 0,91 del '
        'Escenario 1). No es que los modelos fallen —siguen explicando el 73-78% de la '
        'varianza— sino que el problema de predicción diaria con pocos datos es '
        'intrínsecamente más difícil."'
    )
)

# ── Fig 27 ──
grafico(
    'escenario3/e3_04_metricas.png',
    'Comparación de Métricas — Escenario 3 (1 día)',
    que_muestra=(
        'Comparación de las cuatro métricas entre los tres modelos para el Escenario 3. '
        'Permite identificar qué modelo es mejor para la predicción del consumo diario.'
    ),
    como_leerlo=(
        'Mismo esquema que los gráficos de métricas anteriores. El RMSE y MAE serán '
        'numéricamente más pequeños que en los escenarios anteriores porque los valores '
        'diarios tienen menor variabilidad (son promedios de 1.440 lecturas).'
    ),
    conclusion=(
        'XGBoost lidera en configuración base con R²=0,7776 y MAPE=9,69%. SVR obtiene '
        'R²=0,7374 y RF R²=0,7313. El RMSE es ~0,11-0,12 kW, inferior al de los '
        'escenarios anteriores por la menor variabilidad de los promedios diarios. '
        'Este es el escenario donde el tuning de SVR tendrá mayor impacto.'
    ),
    que_decir=(
        '"En el escenario diario XGBoost lidera con R²=0,7776 y un MAPE de 9,69%. '
        'El RMSE de 0,11-0,12 kW es numéricamente menor que en los escenarios de '
        '15 minutos y 1 hora, pero hay que tener cuidado con esa comparación: los '
        'valores diarios son promedios y tienen menos variabilidad por naturaleza, '
        'lo cual hace que el error absoluto sea más pequeño en unidades de kW."'
    )
)

# ── Fig 28 ──
grafico(
    'escenario3/e3_05_importancia.png',
    'Importancia de Features — Escenario 3 (1 día)',
    que_muestra=(
        'Las features más importantes para RF y XGBoost en el Escenario 3. '
        'A resolución diaria, el conjunto de features es diferente: no hay "hora" '
        'y se incluyen lag_7 (semana) y lag_30 (mes), además de dia_anio y trimestre.'
    ),
    como_leerlo=(
        'Igual que los gráficos de importancia anteriores. En este caso es interesante '
        'observar si las variables temporales de largo plazo (dia_anio, trimestre) '
        'tienen mayor importancia que en los escenarios anteriores.'
    ),
    conclusion=(
        'GAP_lag_1 (consumo de ayer) domina con gran diferencia. Las medias móviles '
        'de 7 y 14 días también son muy relevantes. Las variables temporales como "mes" '
        'y "dia_anio" tienen mayor importancia relativa que en los escenarios de mayor '
        'frecuencia, reflejando el mayor peso de la estacionalidad anual en la predicción diaria.'
    ),
    que_decir=(
        '"En el escenario diario, el consumo de ayer (GAP_lag_1) es el predictor más '
        'potente con diferencia. Esto tiene mucho sentido: si ayer fue un día frío '
        'con alto consumo, hoy probablemente también lo sea. También es notable que '
        'el mes del año tiene mayor importancia aquí que en los otros escenarios, '
        'porque la estacionalidad anual es el patrón dominante a escala diaria."'
    )
)

doc.add_page_break()


# =============================================================================
# CAPÍTULO 6: TUNING (Figuras 29–32)
# =============================================================================
print('\n[Capítulo 6] Tuning — Figuras 29 a 32')
heading('Capítulo 6: Ajuste de Hiperparámetros (Figuras 29–32)')
doc.add_paragraph()

# ── Fig 29 ──
grafico(
    'tuning/comparacion_r2.png',
    'Comparación de R² Antes y Después del Tuning',
    que_muestra=(
        'Gráfico de barras agrupadas que compara el R² de la configuración base vs el '
        'R² tuned para los tres modelos en cada uno de los tres escenarios. Permite ver '
        'de un vistazo cuánto mejora (o no) cada modelo tras el GridSearchCV.'
    ),
    como_leerlo=(
        'Hay dos barras por modelo en cada escenario: una para Base y otra para Tuned. '
        'Si la barra Tuned es más larga que la Base, el tuning mejoró el modelo. '
        'Si son iguales o la Tuned es más corta, el tuning no ayudó o incluso empeoró levemente.'
    ),
    conclusion=(
        'SVR es el modelo que más mejora en todos los escenarios: +0,0212 en 15 min, '
        '+0,0165 en 1h y +0,0474 en 1 día. RF y XGBoost muestran cambios mínimos o '
        'leves descensos, lo que indica que ya estaban bien configurados. El mayor '
        'impacto del tuning es en el Escenario 3 para SVR.'
    ),
    que_decir=(
        '"Este gráfico resume el impacto del ajuste de hiperparámetros. El resultado más '
        'relevante es que SVR es el modelo que más se beneficia del tuning en los tres '
        'escenarios. RF y XGBoost prácticamente no cambian —las barras Base y Tuned son '
        'casi del mismo tamaño—, lo que indica que su configuración manual inicial ya '
        'era muy cercana a la óptima."'
    )
)

# ── Fig 30 ──
grafico(
    'tuning/comparacion_rmse.png',
    'Comparación de RMSE Antes y Después del Tuning',
    que_muestra=(
        'Mismo tipo de gráfico que el anterior pero para la métrica RMSE. Compara '
        'el error cuadrático medio raíz antes y después del tuning para los tres '
        'modelos y los tres escenarios.'
    ),
    como_leerlo=(
        'Para RMSE, las barras más cortas son mejores. Si la barra Tuned es más corta '
        'que la Base, el tuning redujo el error. Hay que prestar atención a la escala: '
        'los tres escenarios tienen distintos rangos de RMSE.'
    ),
    conclusion=(
        'SVR reduce su RMSE de forma notable en todos los escenarios, especialmente en '
        'el Escenario 3 (de 0,1238 a 0,1121 kW). RF y XGBoost mantienen su RMSE prácticamente '
        'sin cambios. Este gráfico confirma desde otra métrica lo que ya mostraba el R².'
    ),
    que_decir=(
        '"Desde el punto de vista del RMSE, el patrón es el mismo: SVR reduce su error '
        'significativamente con el tuning. En el escenario diario pasa de 0,1238 a '
        '0,1121 kW de RMSE, lo que es una mejora de aproximadamente 10% en términos '
        'absolutos. RF y XGBoost se mantienen prácticamente igual."'
    )
)

# ── Fig 31 ──
grafico(
    'tuning/comparacion_mape.png',
    'Comparación de MAPE Antes y Después del Tuning',
    que_muestra=(
        'Comparación del error porcentual (MAPE) antes y después del tuning. El MAPE '
        'es especialmente útil porque expresa el error como porcentaje del valor real, '
        'facilitando la interpretación independientemente de la escala.'
    ),
    como_leerlo=(
        'Para MAPE, barras más cortas son mejores. Un MAPE de 10% significa que en promedio '
        'el modelo se equivoca en un 10% del valor real. Barras que bajan del Base al Tuned '
        'indican que el ajuste redujo el error porcentual.'
    ),
    conclusion=(
        'SVR es el que más reduce su MAPE en todos los escenarios, especialmente '
        'en el Escenario 2 (de 20,56% a 17,75%) y en el Escenario 3 (de 10,25% a 9,66%). '
        'El mejor MAPE final obtenido es el de SVR en el Escenario 3 (9,66%), seguido '
        'de XGBoost en el Escenario 3 (9,90%).'
    ),
    que_decir=(
        '"El MAPE es la métrica más fácil de interpretar para alguien ajeno al modelo: '
        '"el modelo se equivoca en promedio un X% del valor real". SVR pasa de un MAPE '
        'de 20,56% a 17,75% en el escenario horario con el tuning —una mejora de casi '
        '3 puntos porcentuales. El escenario diario tiene los MAPE más bajos en general, '
        'lo que puede sonar contradictorio pero se explica por la menor variabilidad '
        'de los promedios diarios."'
    )
)

# ── Fig 32 ──
grafico(
    'tuning/mejora_delta_r2.png',
    'Mejora Neta de R² por Tuning (ΔR² = Tuned − Base)',
    que_muestra=(
        'Un gráfico de barras que muestra directamente la diferencia entre R² tuned '
        'y R² base para cada combinación modelo-escenario. Visualiza la ganancia neta '
        'atribuible al proceso de ajuste de hiperparámetros.'
    ),
    como_leerlo=(
        'Las barras positivas (hacia arriba) indican mejora tras el tuning. Las barras '
        'negativas (hacia abajo) indican una leve degradación. La altura de la barra '
        'es la magnitud del cambio. Las barras muy pequeñas (positivas o negativas) '
        'indican que el tuning tuvo impacto mínimo.'
    ),
    conclusion=(
        'SVR muestra las barras positivas más grandes en los tres escenarios, con la '
        'mayor ganancia en el Escenario 3 (+0,0474). RF y XGBoost tienen barras '
        'prácticamente en cero o levemente negativas, lo que confirma que no se '
        'benefician significativamente del GridSearchCV porque su configuración base '
        'ya era óptima.'
    ),
    que_decir=(
        '"Este gráfico de delta R² es quizás el más directo para responder la pregunta: '
        '"¿valió la pena el GridSearchCV?". La respuesta es: sí para SVR, marginalmente '
        'para RF, y prácticamente no para XGBoost. Las barras negativas de RF y XGBoost '
        'son muy pequeñas y se explican por la submuestra usada en el GridSearch, no '
        'son degradaciones reales del modelo."'
    )
)

doc.add_page_break()


# =============================================================================
# CAPÍTULO 7: ANÁLISIS COMPARATIVO (Figuras 33–38)
# =============================================================================
print('\n[Capítulo 7] Comparativo — Figuras 33 a 38')
heading('Capítulo 7: Análisis Comparativo entre Modelos y Escenarios (Figuras 33–38)')
doc.add_paragraph()

# ── Fig 33 ──
grafico(
    'comparativos/01_metricas_tuned_barras.png',
    'Comparación General de Métricas Tuned (Todos los Modelos y Escenarios)',
    que_muestra=(
        'Un panel de gráficos de barras que muestra simultáneamente las cuatro métricas '
        'en su versión tuned para los nueve modelos evaluados (3 algoritmos × 3 escenarios). '
        'Es la vista más completa de todos los resultados finales.'
    ),
    como_leerlo=(
        'Hay cuatro subgráficos, uno por métrica. En cada subgráfico, las barras están '
        'agrupadas por escenario y coloreadas por modelo. Esta disposición permite comparar '
        'simultáneamente cómo varía cada métrica entre escenarios y entre modelos.'
    ),
    conclusion=(
        'El Escenario 1 domina en R² (todos los modelos superan 0,88). El Escenario 3 '
        'tiene los RMSE y MAE más bajos en valor absoluto (por menor variabilidad de '
        'los datos). SVR tuned es el mejor en el Escenario 3. RF y XGBoost son más '
        'estables entre escenarios.'
    ),
    que_decir=(
        '"Este gráfico de resumen nos permite ver todos los resultados de un vistazo. '
        'Dos patrones emergen claramente: primero, el R² disminuye al aumentar el '
        'horizonte de predicción (de 15 min a 1 día). Segundo, dentro de cada escenario, '
        'RF y XGBoost siempre son competitivos entre sí, mientras SVR tuned es el mejor '
        'solo en el escenario diario."'
    )
)

# ── Fig 34 ──
grafico(
    'comparativos/02_heatmap_metricas.png',
    'Mapa de Calor de Métricas Tuned por Modelo y Escenario',
    que_muestra=(
        'Un mapa de calor donde las filas son los modelos, las columnas son los escenarios '
        'y el color de cada celda representa el valor de la métrica. Hay un mapa de calor '
        'por cada métrica (RMSE, MAE, MAPE, R²).'
    ),
    como_leerlo=(
        'Para R², los colores más intensos/cálidos indican mejor desempeño. Para RMSE, '
        'MAE y MAPE, los colores más claros/fríos indican menor error y por lo tanto '
        'mejor desempeño. Las celdas con el mejor valor en cada columna se pueden '
        'identificar visualmente por ser las más destacadas.'
    ),
    conclusion=(
        'El mapa permite identificar rápidamente: XGBoost-15min y RF-15min como las '
        'combinaciones con mayor R². SVR-1día como la combinación con mejor MAPE '
        'después del tuning. La degradación diagonal del R² al aumentar el escenario '
        'es visible de forma inmediata.'
    ),
    que_decir=(
        '"El mapa de calor es una forma muy eficiente de presentar todos los resultados. '
        'De un vistazo podemos ver qué combinación modelo-escenario produce los mejores '
        'resultados en cada métrica. Los colores más intensos en la columna de 15 minutos '
        'para R² confirman que es el escenario con mejor desempeño general."'
    )
)

# ── Fig 35 ──
grafico(
    'comparativos/03_base_vs_tuned_r2_rmse.png',
    'Comparación Directa R² y RMSE: Base vs Tuned (Todos los Modelos)',
    que_muestra=(
        'Un gráfico de dispersión o barras pareadas que muestra directamente el cambio de '
        'R² y RMSE desde la configuración base hasta la tuned, para los nueve modelos. '
        'Permite evaluar el impacto total del ajuste de hiperparámetros.'
    ),
    como_leerlo=(
        'Cada punto o barra representa un modelo en un escenario. Los ejes muestran '
        'el valor base vs el valor tuned. Los modelos sobre la diagonal (o con barras '
        'positivas) mejoraron con el tuning. Los que están debajo empeoraron levemente.'
    ),
    conclusion=(
        'SVR en todos los escenarios mejora su R² y reduce su RMSE con el tuning. '
        'RF y XGBoost se mantienen prácticamente sin cambios, confirmando su robustez. '
        'El mayor impacto positivo es SVR-1día (+0,0474 R²). El impacto negativo mayor '
        'es XGBoost-15min (−0,0067), pero es muy pequeño en términos absolutos.'
    ),
    que_decir=(
        '"Este gráfico complementa los anteriores mostrando explícitamente qué modelos '
        'mejoraron y cuáles no con el tuning. La conclusión es clara: el GridSearchCV '
        'fue muy útil para SVR, que era el modelo con más margen de mejora. RF y '
        'XGBoost ya estaban bien configurados desde el inicio, lo que también es '
        'un buen resultado: significa que son modelos robustos."'
    )
)

# ── Fig 36 ──
grafico(
    'comparativos/04_radar_modelos.png',
    'Gráfico Radar: Comparación Multidimensional de los Tres Modelos',
    que_muestra=(
        'Un gráfico de radar (o araña) que compara los tres modelos en su versión tuned '
        'sobre múltiples métricas simultáneamente, promediadas sobre los tres escenarios. '
        'Cada eje del radar corresponde a una métrica.'
    ),
    como_leerlo=(
        'Cada modelo forma un polígono dentro del radar. Un polígono más grande y regular '
        'indica mejor desempeño general. Los vértices del polígono en cada eje indican '
        'el valor de esa métrica para ese modelo. Las métricas de error (RMSE, MAE, MAPE) '
        'se invierten para que "más afuera" siempre sea mejor.'
    ),
    conclusion=(
        'RF y XGBoost forman polígonos similares y más amplios que SVR en la mayoría de '
        'las dimensiones. Sin embargo, SVR tuned es competitivo especialmente en las '
        'métricas del Escenario 3. Este gráfico permite identificar rápidamente '
        'las fortalezas y debilidades relativas de cada algoritmo.'
    ),
    que_decir=(
        '"El gráfico radar es una visualización poderosa para comparar múltiples modelos '
        'en múltiples métricas a la vez. Visualmente se puede ver que RF y XGBoost tienen '
        'polígonos más grandes —mejor desempeño general—, mientras que SVR tuned cierra '
        'la brecha especialmente en el escenario diario. Este tipo de gráfico es muy '
        'útil en papers y presentaciones para mostrar la comparación global."'
    )
)

# ── Fig 37 ──
grafico(
    'comparativos/05_tabla_mejor_modelo.png',
    'Resumen Visual: Mejor Modelo por Escenario y Métrica',
    que_muestra=(
        'Una tabla visual o gráfico de resumen que identifica qué modelo gana en cada '
        'combinación de escenario y métrica. Es un cuadro de honor que sintetiza todos '
        'los resultados comparativos.'
    ),
    como_leerlo=(
        'Cada celda indica qué modelo obtuvo el mejor resultado para esa combinación '
        'de escenario y métrica. Los colores pueden indicar el modelo ganador. '
        'Este gráfico no muestra valores numéricos sino el ganador relativo.'
    ),
    conclusion=(
        'RF es el mejor en el Escenario 1 (tuned). XGBoost es el mejor en el Escenario 2 '
        'y también lidera en algunos aspectos del Escenario 3 (base). SVR tuned domina '
        'en el Escenario 3. XGBoost es el algoritmo más consistente entre escenarios.'
    ),
    que_decir=(
        '"Este gráfico de resumen responde la pregunta que probablemente tiene el tutor: '
        '"¿cuál es el mejor modelo?". La respuesta es que depende del escenario: para '
        '15 minutos, Random Forest tuned; para 1 hora, XGBoost; y para 1 día, SVR tuned. '
        'No hay un ganador universal, lo que es un resultado realista y honesto."'
    )
)

# ── Fig 38 ──
grafico(
    'comparativos/06_evolucion_r2.png',
    'Evolución del R² a través de los Tres Escenarios',
    que_muestra=(
        'Un gráfico de líneas que muestra cómo varía el R² de cada modelo al pasar '
        'del Escenario 1 (15 min) al Escenario 2 (1 hora) y al Escenario 3 (1 día). '
        'Permite ver la tendencia de degradación del desempeño con el horizonte temporal.'
    ),
    como_leerlo=(
        'El eje X son los tres escenarios (de izquierda a derecha: 15 min, 1h, 1 día). '
        'El eje Y es el R². Cada línea corresponde a un modelo. Una línea decreciente '
        'de izquierda a derecha indica que el modelo se desempeña peor a mayor horizonte. '
        'Líneas paralelas indicarían que todos los modelos se degradan igual.'
    ),
    conclusion=(
        'Los tres modelos siguen una tendencia decreciente de R² al aumentar el horizonte '
        'de predicción, lo que confirma que mayor horizonte = mayor dificultad. XGBoost '
        'mantiene el R² más alto en los Escenarios 1 y 2, pero SVR tuned lo supera en '
        'el Escenario 3. La caída de R² entre el Escenario 2 y el 3 es más pronunciada '
        'que entre el 1 y el 2.'
    ),
    que_decir=(
        '"Este es probablemente el gráfico más importante del análisis comparativo porque '
        'muestra una tendencia fundamental: a mayor horizonte de predicción, menor R². '
        'Esto no es un fallo de los modelos, es una propiedad intrínseca del problema: '
        'predecir más lejos en el futuro siempre es más incierto. Lo que sí es interesante '
        'es que la caída entre 1 hora y 1 día es más pronunciada que entre 15 minutos y '
        '1 hora, lo que sugiere que el mayor problema es la escasez de datos del escenario '
        'diario más que la dificultad intrínseca del horizonte."'
    )
)

doc.add_page_break()


# =============================================================================
# RESUMEN FINAL
# =============================================================================
heading('Resumen: Los 38 Gráficos de un Vistazo')

para(
    'A continuación se presenta un resumen compacto de todos los gráficos para '
    'repaso rápido antes de la exposición:'
)

t = doc.add_table(rows=1, cols=3)
t.style = 'Table Grid'
for cell, txt in zip(t.rows[0].cells, ['Figura', 'Título', 'Mensaje clave']):
    r = cell.paragraphs[0].add_run(txt)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(10)
    r.bold = True

resumen = [
    ('1',  'Valores nulos',                    'Todos tienen 1,252% de nulos → son bloques de tiempo sin medición → usar dropna()'),
    ('2',  'Series temporales principales',    'Estacionalidad invernal clara. GI ≈ GAP → GI se elimina'),
    ('3',  'Series sub-medidores',             'SM3 tiene mayor estacionalidad. SM1 queda en cero por IQR'),
    ('4',  'Distribuciones',                   'GAP tiene sesgo derecho. VOLT es estable. Sub-medidores son esparsas'),
    ('5',  'Correlación',                      'GI-GAP = 0,999 → GI se elimina. SM3 correlaciona moderado con GAP'),
    ('6',  'Patrones temporales',              'Picos a 7-9h y 17-21h. Mayor consumo en invierno → justifica features temporales'),
    ('7',  'Heatmap hora × día',               'Noches de viernes/sábado tienen mayor consumo → justifica es_finde'),
    ('8',  'Boxplots mensuales',               'Enero-febrero = mayor consumo y variabilidad. Julio-agosto = mínimos'),
    ('9',  'Boxplots ANTES de outliers',       'Valores extremos visibles en todas las variables → justifica filtro IQR'),
    ('10', 'Boxplots DESPUÉS de outliers',     'Distribuciones más compactas. Dataset limpio: 1.739.167 registros'),
    ('11', 'Descomposición estacional',        'Tendencia decreciente leve. Estacionalidad anual clara. Residuo pequeño'),
    ('12', 'ACF y PACF',                       'Correlación significativa en lags 24h → justifica lag_24 en features'),
    ('13', 'Participación sub-medidores',      'SM3 domina en invierno. Gran parte es "otros circuitos" no medidos'),
    ('14', 'Serie 15 minutos',                 '133.489 obs. Split: 106.791 train / 26.698 test'),
    ('15', 'Serie 1 hora',                     '34.007 obs. Split: 27.205 train / 6.802 test'),
    ('16', 'Serie 1 día',                      '1.433 obs. Split: 1.146 train / 287 test'),
    ('17', 'Predicciones E1',                  'RF y XGB siguen bien la serie real. SVR suaviza los picos'),
    ('18', 'Scatter E1',                       'Nube concentrada en diagonal para RF/XGB. SVR más dispersa'),
    ('19', 'Métricas E1',                      'XGB líder: R²=0,9198, MAPE=14,89%. SVR: MAPE=24,25%'),
    ('20', 'Importancia E1',                   'lag_1 y lag_2 dominan. Variables temporales: importancia moderada'),
    ('21', 'Predicciones E2',                  'Serie más suave. RF/XGB siguen bien los ciclos diarios'),
    ('22', 'Scatter E2',                       'Los tres modelos bien concentrados en diagonal'),
    ('23', 'Métricas E2',                      'XGB líder: R²=0,8812, MAPE=16,98%. SVR mejora vs E1'),
    ('24', 'Importancia E2',                   'lag_1 (1h) y lag_24 (1 día anterior) dominan'),
    ('25', 'Predicciones E3',                  'Se muestra todo el test. Modelos capturan tendencia general'),
    ('26', 'Scatter E3',                       'Más disperso que E1/E2. Coherente con R² más bajos (0,73-0,78)'),
    ('27', 'Métricas E3',                      'XGB base: R²=0,7776, MAPE=9,69%. RF y SVR base similares'),
    ('28', 'Importancia E3',                   'lag_1 (ayer) domina. "mes" y "dia_anio" más importantes que en E1/E2'),
    ('29', 'Tuning: R² base vs tuned',         'SVR mejora mucho. RF y XGB prácticamente sin cambio'),
    ('30', 'Tuning: RMSE base vs tuned',       'SVR reduce RMSE notablemente. RF/XGB estables'),
    ('31', 'Tuning: MAPE base vs tuned',       'SVR reduce MAPE especialmente en E2 y E3'),
    ('32', 'Delta R² del tuning',              'SVR: barras positivas grandes. RF/XGB: barras casi en cero'),
    ('33', 'Métricas tuned general',           'R² decrece de E1 a E3. SVR tuned es mejor en E3'),
    ('34', 'Heatmap de métricas',              'XGB-15min y RF-15min = mejores R². SVR-1día = mejor MAPE'),
    ('35', 'Base vs tuned R² y RMSE',          'SVR mejora, RF/XGB se mantienen. Mayor impacto: SVR-1día'),
    ('36', 'Radar de modelos',                 'RF y XGB con polígonos más grandes. SVR cierra brecha en E3'),
    ('37', 'Tabla mejor modelo',               'E1→RF, E2→XGB, E3→SVR. No hay ganador universal'),
    ('38', 'Evolución R² por escenario',       'R² decrece al aumentar horizonte. Caída mayor entre E2 y E3'),
]

for fig, titulo, mensaje in resumen:
    row = t.add_row()
    for cell, text in zip(row.cells, [fig, titulo, mensaje]):
        r = cell.paragraphs[0].add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(9)


# =============================================================================
# GUARDAR
# =============================================================================
print(f'\nGuardando documento...')
doc.save(OUT_PATH)
print(f'✓ Documento generado: {OUT_PATH}')
print(f'  Figuras procesadas: {fig_num[0] - 1} / 38')
