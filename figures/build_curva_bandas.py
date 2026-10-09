# -*- coding: utf-8 -*-
"""V8. El avance contra la categoria de Barthel al ingreso, en crudo y corregido.

No lee el Excel: trabaja sobre los valores agregados por categoria, ya validados
contra la planilla. El eje X es categorico a proposito -- las cuatro bandas son
la unidad en la que habla todo el poster, y evita estimar una posicion continua
que estos valores agregados no contienen.

uso:  python3.13 build_curva_bandas.py [en|es]
"""
import sys, os, textwrap
import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator

HERE=os.path.dirname(os.path.abspath(__file__))
SURF='#fcfcfb';INK='#0b0b0b';SEC='#52514e';MUT='#898781';GRID='#e1e0d9';BASE='#c3c2b7'
CAT=['#c0392b','#eda100','#1baf7a','#2a78d6']
TXT=['#a5322a','#8a5d00','#00694a','#2a78d6']
RG=['<20','20–35','40–55','60–99']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'text.color':INK,
 'axes.facecolor':SURF,'figure.facecolor':SURF,'axes.edgecolor':BASE,'axes.labelcolor':SEC,
 'xtick.color':MUT,'ytick.color':MUT,'axes.linewidth':.8,'xtick.major.size':0,
 'ytick.major.size':0,'axes.spines.top':False,'axes.spines.right':False,'savefig.facecolor':SURF})

LANG=sys.argv[1] if len(sys.argv)>1 else 'en'
SUF='' if LANG=='en' else '_es'
def D(x,dec=1):
    t=f'{x:.{dec}f}'
    return t.replace('.',',') if LANG=='es' else t

# --- valores agregados, verificados contra la planilla ---
N     = [13, 25, 11, 25]      # pacientes pareados por categoria de ingreso
GAIN  = [23.5, 49.4, 28.1, 13.2]   # delta Barthel medio
SHARE = [24.4, 69.0, 49.9, 48.9]   # ganancia / margen disponible, razon de sumas
COH   = 50.2                       # misma razon sobre la cohorte

T={
 'en':{'sh':['Total','Severe','Moderate','Mild'],'ibl':'BI',
  'title':'The gain collapses at the extreme of dependence and peaks in the severe band',
  'sub':'Admission Barthel category against what each group gained, raw and corrected for the ceiling.',
  'pa':'a.  Mean points gained during the stay','yla':'ΔBI (points)',
  'pb':'b.  The same groups, corrected for the ceiling','ylb':'Share of own margin recovered (%)',
  'coh':'cohort {v}%',
  'note':('Panel b divides each group’s total gain by its total available margin, ΣΔBI ÷ Σ(100 − admission BI). '
          'The fall on the right of panel a is the ceiling, not a clinical finding: a patient admitted at 80 cannot gain more than 20 points. '
          'Panel b removes that constraint and the peak in the severe band survives it — so the rise on the left is real and the fall on the right is not. '
          'Independent patients on admission (BI 100, n=4) are left out of both panels: their margin is zero, so the ratio is undefined. '
          'Floor effect and profound deficit are both plausible for the BI <20 group; these data cannot separate them.')},
 'es':{'sh':['Total','Severa','Moderada','Leve'],'ibl':'IB',
  'title':'El avance se desploma en el extremo de dependencia y hace pico en la banda severa',
  'sub':'Categoría de Barthel al ingreso frente a lo que ganó cada grupo, en crudo y corregido por el techo.',
  'pa':'a.  Puntos ganados en promedio durante la estadía','yla':'ΔIB (puntos)',
  'pb':'b.  Los mismos grupos, corregido por el techo','ylb':'Proporción del propio margen recuperada (%)',
  'coh':'cohorte {v}%',
  'note':('El panel b divide la ganancia total de cada grupo por su margen total disponible, ΣΔIB ÷ Σ(100 − IB de ingreso). '
          'La caída a la derecha del panel a es el techo, no un hallazgo clínico: un paciente que ingresa con 80 no puede ganar más de 20 puntos. '
          'El panel b elimina esa restricción y el pico de la banda severa la sobrevive: el ascenso de la izquierda es real, la caída de la derecha no. '
          'Los pacientes independientes al ingreso (IB 100, n=4) quedan fuera de ambos paneles: su margen es cero y la razón no está definida. '
          'Efecto suelo y déficit profundo son ambos plausibles en el grupo IB <20; estos datos no permiten separarlos.')},
}[LANG]
SH=T['sh']

X=np.arange(4)
fig,(a,b)=plt.subplots(2,1,figsize=(9.8,10.0),sharex=True,gridspec_kw={'hspace':.26})

def panel(ax,y,ptitle,ylab,pct,top_pad):
    ax.set_axisbelow(True); ax.yaxis.grid(True,color=GRID,lw=.7)
    for x in X: ax.axvline(x,color=GRID,lw=.7,zorder=0)
    gx=np.linspace(0,3,300)
    ax.plot(gx,PchipInterpolator(X,y)(gx),color='#3d3b36',lw=3.0,zorder=4,
            solid_capstyle='round')
    for c in range(4):
        ax.scatter([c],[y[c]],s=300,color=CAT[c],edgecolor=SURF,lw=2.6,zorder=6)
        v=f'{D(y[c],0)}%' if pct else f'+{D(y[c],0)}'
        ax.annotate(v,(c,y[c]),textcoords='offset points',xytext=(0,20),ha='center',
                    fontsize=16,weight='bold',color=TXT[c],zorder=7)
    ax.set_ylim(0,max(y)*top_pad)
    ax.set_ylabel(ylab,fontsize=11.5)
    ax.set_title(ptitle,fontsize=13,weight='bold',color=INK,loc='left',pad=10)

panel(a,GAIN,T['pa'],T['yla'],False,1.34)
panel(b,SHARE,T['pb'],T['ylb'],True,1.30)

b.axhline(COH,color=SEC,lw=1.3,ls=(0,(4,3)),zorder=3,label=T['coh'].format(v=D(COH,1)))
b.legend(loc='lower right',frameon=False,fontsize=9.6,labelcolor=SEC,
         handlelength=2.4,borderpad=.1,handletextpad=.7)

b.set_xticks(X)
b.set_xticklabels([f"{SH[c]}\n{T['ibl']} {RG[c]}\nn={N[c]}" for c in range(4)],
                  fontsize=11,linespacing=1.5)
for lbl,c in zip(b.get_xticklabels(),range(4)):
    lbl.set_color(TXT[c]); lbl.set_fontweight('bold')
a.set_xlim(-.45,3.45); b.set_xlim(-.45,3.45)

fig.subplots_adjust(top=.845,bottom=.225,left=.085,right=.975)
fig.text(.012,.992,'\n'.join(textwrap.wrap(T['title'],64)),va='top',
         fontsize=15.5,weight='bold',color=INK,linespacing=1.25)
fig.text(.012,.895,'\n'.join(textwrap.wrap(T['sub'],130)),va='top',
         fontsize=10,color=SEC,linespacing=1.45)
fig.text(.012,.105,'\n'.join(textwrap.wrap(T['note'],152)),va='top',
         fontsize=9.0,color=MUT,linespacing=1.55)

for e in ('png','pdf'):
    fig.savefig(os.path.join(HERE,f'V8_curva_bandas{SUF}.{e}'),dpi=300)
print('escrito V8_curva_bandas'+SUF)
