import matplotlib
# matplotlib.use('Agg')  # desactivado: permite ver gráficos en Spyder
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle
import numpy as np
import os

_here = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = _here if os.path.exists(os.path.join(_here, 'datos')) else os.path.dirname(_here)
GRAF_DIR = os.path.join(BASE_DIR, 'graficos')
os.makedirs(GRAF_DIR, exist_ok=True)

# ── FIGURA ────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(18, 26))
ax.set_xlim(0, 18)
ax.set_ylim(0, 26)
ax.axis('off')

BG = '#0B0F1A'
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

# ── PALETA ────────────────────────────────────────────────────────────────────
P = {
    'dataset' : '#0EA5E9',
    'preproc' : '#818CF8',
    'eda'     : '#C084FC',
    'e1'      : '#F472B6',
    'e2'      : '#E879F9',
    'e3'      : '#A78BFA',
    'feat'    : '#34D399',
    'split'   : '#2DD4BF',
    'rf'      : '#60A5FA',
    'xgb'     : '#FB923C',
    'svr'     : '#F87171',
    'tuning'  : '#94A3B8',
    'met'     : '#FCD34D',
}

ARROW_C = '#475569'
CX      = 9.0
COL_CX  = [3.3, 9.0, 14.7]
COL_W   = 5.0
FULL_X  = 1.5
FULL_W  = 15.0

# ── HELPERS ───────────────────────────────────────────────────────────────────

def darken(hex_color, factor=0.45):
    r = int(hex_color[1:3], 16) / 255
    g = int(hex_color[3:5], 16) / 255
    b = int(hex_color[5:7], 16) / 255
    return (r * factor, g * factor, b * factor)


def card(x, y, w, h, title, color,
         subtitle='', tsize=13, ssize=9.5,
         badge=None, radius=0.22):
    """Caja con color sólido y texto perfectamente centrado."""

    dc = darken(color, 0.40)

    # --- sombra ---
    ax.add_patch(FancyBboxPatch(
        (x + 0.10, y - 0.10), w, h,
        boxstyle=f'round,pad=0,rounding_size={radius}',
        facecolor='black', alpha=0.45, linewidth=0, zorder=2))

    # --- cuerpo: gradiente simulado (dos rectángulos superpuestos) ---
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f'round,pad=0,rounding_size={radius}',
        facecolor=dc, linewidth=0, zorder=3))

    # overlay translúcido del color vivo (da efecto de profundidad)
    r_, g_, b_ = int(color[1:3], 16)/255, int(color[3:5], 16)/255, int(color[5:7], 16)/255
    ax.add_patch(FancyBboxPatch(
        (x, y + h * 0.45), w, h * 0.55,
        boxstyle=f'round,pad=0,rounding_size={radius}',
        facecolor=(r_, g_, b_), alpha=0.28, linewidth=0, zorder=4))

    # --- borde glow ---
    ax.add_patch(FancyBboxPatch(
        (x - 0.025, y - 0.025), w + 0.05, h + 0.05,
        boxstyle=f'round,pad=0,rounding_size={radius + 0.025}',
        facecolor='none', edgecolor=color, linewidth=1.6,
        alpha=0.55, zorder=5))

    # --- badge número (esquina superior izquierda) ---
    if badge is not None:
        bx = x + 0.38
        by = y + h - 0.38
        ax.add_patch(Circle((bx, by), 0.27,
                             facecolor='white', linewidth=0,
                             zorder=7, alpha=0.95))
        ax.text(bx, by, str(badge),
                ha='center', va='center', fontsize=8.5,
                fontweight='bold', color=dc, zorder=8)

    # --- título CENTRADO en la caja ---
    if subtitle:
        # con subtítulo: título un poco arriba del centro
        ax.text(x + w / 2, y + h * 0.62, title,
                ha='center', va='center',
                fontsize=tsize, fontweight='bold',
                color='white', zorder=6)
        ax.text(x + w / 2, y + h * 0.28, subtitle,
                ha='center', va='center',
                fontsize=ssize, color='#E2E8F0',
                zorder=6, fontstyle='italic',
                linespacing=1.6, multialignment='center')
    else:
        # sin subtítulo: perfectamente centrado
        ax.text(x + w / 2, y + h / 2, title,
                ha='center', va='center',
                fontsize=tsize, fontweight='bold',
                color='white', zorder=6)


def arrow_v(x, y_top, y_bot):
    ax.annotate('', xy=(x, y_bot), xytext=(x, y_top),
                arrowprops=dict(
                    arrowstyle='-|>', color=ARROW_C,
                    lw=1.8, mutation_scale=16))


def branch_down(x_from, y_from, col_xs, y_to):
    ym = (y_from + y_to) / 2
    ax.plot([x_from, x_from], [y_from, ym],
            color=ARROW_C, lw=1.8, zorder=3)
    ax.plot([col_xs[0], col_xs[-1]], [ym, ym],
            color=ARROW_C, lw=1.8, zorder=3)
    for cx_ in col_xs:
        ax.annotate('', xy=(cx_, y_to), xytext=(cx_, ym),
                    arrowprops=dict(arrowstyle='-|>', color=ARROW_C,
                                   lw=1.8, mutation_scale=14))


def join_up(col_xs, y_from, x_to, y_to):
    ym = (y_from + y_to) / 2
    for cx_ in col_xs:
        ax.plot([cx_, cx_], [y_from, ym],
                color=ARROW_C, lw=1.8, zorder=3)
    ax.plot([col_xs[0], col_xs[-1]], [ym, ym],
            color=ARROW_C, lw=1.8, zorder=3)
    ax.annotate('', xy=(x_to, y_to), xytext=(x_to, ym),
                arrowprops=dict(arrowstyle='-|>', color=ARROW_C,
                               lw=1.8, mutation_scale=16))


def dot_grid():
    for gx in np.arange(0.5, 18, 0.85):
        for gy in np.arange(0.5, 26, 0.85):
            ax.plot(gx, gy, '.', color='#1E2D40',
                    markersize=1.6, zorder=1)


# ── FONDO ─────────────────────────────────────────────────────────────────────
dot_grid()

# banda decorativa superior
ax.add_patch(Rectangle((0, 24.7), 18, 1.3,
                        facecolor='#0EA5E9', alpha=0.07,
                        linewidth=0, zorder=1))
ax.add_patch(Rectangle((0, 24.7), 18, 0.055,
                        facecolor='#0EA5E9', alpha=0.9,
                        linewidth=0, zorder=2))

# ── TÍTULO PRINCIPAL ──────────────────────────────────────────────────────────
ax.text(CX, 25.45,
        'D I S E Ñ O   M E T O D O L Ó G I C O',
        ha='center', va='center', fontsize=21,
        fontweight='bold', color='white', zorder=5)

ax.text(CX, 24.9,
        'Predicción del consumo energético en hogares inteligentes · Machine Learning',
        ha='center', va='center', fontsize=10.5,
        color='#64748B', zorder=5, fontstyle='italic')

# ── ETIQUETAS DE FASE (barra izquierda) ───────────────────────────────────────
fases = [
    (23.4, 21.7, 'DATOS',        P['dataset']),
    (21.5, 19.4, 'ANÁLISIS',     P['eda']),
    (19.2, 10.6, 'MODELADO',     P['feat']),
    (10.4,  8.7, 'EVALUACIÓN',   P['met']),
]
for yt, yb, lbl, fc in fases:
    ax.add_patch(Rectangle((0.20, yb), 0.30, yt - yb,
                            facecolor=fc, alpha=0.80,
                            linewidth=0, zorder=3, clip_on=False))
    ax.add_patch(Rectangle((0.50, yb), 0.04, yt - yb,
                            facecolor=fc, alpha=0.25,
                            linewidth=0, zorder=3, clip_on=False))
    ax.text(0.35, (yt + yb) / 2, lbl,
            ha='center', va='center', fontsize=7,
            fontweight='bold', color='white', zorder=4,
            rotation=90, clip_on=False)

# ── 1. DATASET ────────────────────────────────────────────────────────────────
DY = 22.15
card(FULL_X, DY, FULL_W, 1.25,
     'Dataset',
     P['dataset'],
     subtitle='UCI — Individual Household Electric Power Consumption\n'
              'Francia 2006 – 2010  ·  2.075.259 registros  ·  Frecuencia: 1 minuto',
     tsize=14.5, ssize=10, badge=1)

arrow_v(CX, DY, DY - 0.38)

# ── 2. PREPROCESAMIENTO ───────────────────────────────────────────────────────
P2Y = 20.65
card(FULL_X, P2Y, FULL_W, 1.0,
     'Preprocesamiento y Limpieza',
     P['preproc'], tsize=13.5, badge=2)

arrow_v(CX, P2Y, P2Y - 0.38)

# ── 3. EDA ────────────────────────────────────────────────────────────────────
EY = 19.15
card(FULL_X, EY, FULL_W, 1.0,
     'Análisis Exploratorio de Datos',
     P['eda'], tsize=13.5, badge=3)

# ── BIFURCACIÓN ───────────────────────────────────────────────────────────────
ESC_Y = 17.45
branch_down(CX, EY, COL_CX, ESC_Y + 1.0)

# ── 4. ESCENARIOS ─────────────────────────────────────────────────────────────
esc_cfg = [
    ('Escenario 1  —  15 Minutos', P['e1']),
    ('Escenario 2  —  1 Hora',     P['e2']),
    ('Escenario 3  —  1 Día',      P['e3']),
]
for cx_, (lbl, col) in zip(COL_CX, esc_cfg):
    card(cx_ - COL_W/2, ESC_Y, COL_W, 1.0,
         lbl, col, tsize=11.5, badge=4)

# ── 5. FEATURE ENGINEERING ───────────────────────────────────────────────────
FEY = 16.05
for cx_, (_, col) in zip(COL_CX, esc_cfg):
    arrow_v(cx_, ESC_Y, FEY + 1.0)
    card(cx_ - COL_W/2, FEY, COL_W, 1.0,
         'Feature Engineering', P['feat'], tsize=12, badge=5)

# ── 6. SPLIT ─────────────────────────────────────────────────────────────────
SPY = 14.65
for cx_ in COL_CX:
    arrow_v(cx_, FEY, SPY + 1.0)
    card(cx_ - COL_W/2, SPY, COL_W, 1.0,
         'Split Cronológico  80 / 20', P['split'], tsize=12, badge=6)

# ── 7. MODELOS ────────────────────────────────────────────────────────────────
MODY = 12.85
MODH = 1.4
MODW = 1.46
MODGAP = 0.11
model_cfg = [
    ('Random Forest', P['rf']),
    ('XGBoost',       P['xgb']),
    ('SVR',           P['svr']),
]
for cx_ in COL_CX:
    arrow_v(cx_, SPY, MODY + MODH)
    total_w = 3 * MODW + 2 * MODGAP
    x0 = cx_ - total_w / 2
    for k, (mlbl, mcol) in enumerate(model_cfg):
        mx = x0 + k * (MODW + MODGAP)
        card(mx, MODY, MODW, MODH,
             mlbl, mcol, tsize=9.5,
             badge=7 if k == 0 else None)

# ── 8. TUNING ────────────────────────────────────────────────────────────────
TUNY = 11.3
for cx_ in COL_CX:
    arrow_v(cx_, MODY, TUNY + 1.0)
    card(cx_ - COL_W/2, TUNY, COL_W, 1.0,
         'Tuning de Hiperparámetros', P['tuning'], tsize=12, badge=8)

# ── CONVERGENCIA ─────────────────────────────────────────────────────────────
METY = 9.5
join_up(COL_CX, TUNY, CX, METY + 1.0)

# ── 9. MÉTRICAS ───────────────────────────────────────────────────────────────
card(FULL_X, METY, FULL_W, 1.1,
     'Evaluación  —  RMSE · MAE · MAPE · R²',
     P['met'], tsize=14, badge=9)

# ── LEYENDA INFERIOR ─────────────────────────────────────────────────────────
LEG_Y = 8.55
for i, (mlbl, mcol) in enumerate(model_cfg):
    bx = 5.0 + i * 3.5
    dc = darken(mcol, 0.38)
    ax.add_patch(FancyBboxPatch(
        (bx - 1.15, LEG_Y - 0.30), 2.3, 0.60,
        boxstyle='round,pad=0,rounding_size=0.15',
        facecolor=dc, linewidth=0, zorder=4))
    ax.add_patch(FancyBboxPatch(
        (bx - 1.17, LEG_Y - 0.32), 2.34, 0.64,
        boxstyle='round,pad=0,rounding_size=0.17',
        facecolor='none', edgecolor=mcol,
        linewidth=1.2, alpha=0.6, zorder=5))
    ax.add_patch(Circle((bx - 0.68, LEG_Y), 0.25,
                         facecolor=mcol, linewidth=0, zorder=6))
    ax.text(bx - 0.25, LEG_Y, mlbl,
            ha='left', va='center', fontsize=10,
            fontweight='bold', color='white', zorder=7)

ax.text(CX, 7.75,
        '3 Escenarios  ×  3 Modelos  ×  2 Etapas (Base / Tuned)  =  18 evaluaciones',
        ha='center', va='center', fontsize=10,
        color='#475569', zorder=4, fontstyle='italic')

# línea arcoíris inferior
colors_line = [P['dataset'], P['preproc'], P['eda'],
               P['feat'], P['split'], P['met']]
seg_w = FULL_W / len(colors_line)
for i, cl in enumerate(colors_line):
    ax.add_patch(Rectangle(
        (FULL_X + i * seg_w, 7.15), seg_w, 0.07,
        facecolor=cl, linewidth=0, zorder=4))

# ── GUARDAR ───────────────────────────────────────────────────────────────────
out = os.path.join(GRAF_DIR, 'diagrama_metodologico.png')
plt.savefig(out, dpi=180, bbox_inches='tight',
            facecolor=fig.get_facecolor())
plt.close()
print(f'Guardado: {out}')
