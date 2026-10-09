# -*- coding: utf-8 -*-
"""V8. El avance contra el Barthel de ingreso, en crudo y corregido por techo.

La pregunta que responde: los pacientes con dependencia total avanzan menos que
los severos, y el avance se dispara en la banda severa. El panel de arriba lo
muestra en puntos ganados, que es como lo vive la clínica; el de abajo lo repite
sobre el margen disponible, que es lo que sobrevive a la objeción del techo.

uso:  python3.13 build_curva2.py [en|es] [ruta al .xlsx]
"""
import sys, os
import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator

HERE = os.path.dirname(os.path.abspath(__file__))
SURF='#fcfcfb';INK='#0b0b0b';SEC='#52514e';MUT='#898781';GRID='#e1e0d9';BASE='#c3c2b7'
CAT=['#c0392b','#eda100','#1baf7a','#2a78d6','#4a3aa7']
TXT=['#a5322a','#8a5d00','#00694a','#2a78d6','#4a3aa7']
RG=['<20','20–35','40–55','60–99','100']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'text.color':INK,
 'axes.facecolor':SURF,'figure.facecolor':SURF,'axes.edgecolor':BASE,'axes.labelcolor':SEC,
 'xtick.color':MUT,'ytick.color':MUT,'axes.linewidth':.8,'xtick.major.size':0,
 'ytick.major.size':0,'axes.spines.top':False,'axes.spines.right':False,'savefig.facecolor':SURF})

LANG = sys.argv[1] if len(sys.argv)>1 else 'en'
SUF  = '' if LANG=='en' else '_es'
XLSX = sys.argv[2] if len(sys.argv)>2 else None
def D(x,dec=1):
    t=f'{x:.{dec}f}'
    return t.replace('.',',') if LANG=='es' else t

T={
 'en':{'sh':['Total','Severe','Moderate','Mild','Independent'],'ibl':'BI',
  'title':'The gain collapses at the extreme of dependence and peaks in the severe band',
  'sub':'Each faint dot is one patient; the large markers are the group value with its 95% bootstrap interval.',
  'x':'Barthel Index on admission',
  'pa':'a.  Mean points gained during the stay',  'yla':'\u0394BI (points)',
  'pb':'b.  The same patients, corrected for the ceiling', 'ylb':'Share of own margin recovered (%)',
  'coh':'cohort {v}%',
  'note':('Panel b divides each group\u2019s total gain by its total available margin, \u03a3\u0394BI \u00f7 \u03a3(100 \u2212 admission BI). '
          'The fall on the right of panel a is the ceiling, not a clinical finding: a patient admitted at 80 cannot gain more than 20 points. '
          'Panel b removes that constraint and the peak in the severe band survives it. '
          'Independent patients (BI 100) are excluded from panel b \u2014 their margin is zero, so the ratio is undefined. '
          'Floor effect and profound deficit are both plausible for the BI <20 group; these data cannot separate them.')},
 'es':{'sh':['Total','Severa','Moderada','Leve','Independiente'],'ibl':'IB',
  'title':'El avance se desploma en el extremo de dependencia y hace pico en la banda severa',
  'sub':'Cada punto tenue es un paciente; los marcadores grandes son el valor del grupo con su intervalo bootstrap del 95%.',
  'x':'\u00cdndice de Barthel al ingreso',
  'pa':'a.  Puntos ganados en promedio durante la estad\u00eda', 'yla':'\u0394IB (puntos)',
  'pb':'b.  Los mismos pacientes, corregido por el techo', 'ylb':'Proporci\u00f3n del propio margen recuperada (%)',
  'coh':'cohorte {v}%',
  'note':('El panel b divide la ganancia total de cada grupo por su margen total disponible, \u03a3\u0394IB \u00f7 \u03a3(100 \u2212 IB de ingreso). '
          'La ca\u00edda a la derecha del panel a es el techo, no un hallazgo cl\u00ednico: un paciente que ingresa con 80 no puede ganar m\u00e1s de 20 puntos. '
          'El panel b elimina esa restricci\u00f3n y el pico de la banda severa la sobrevive. '
          'Los pacientes independientes (IB 100) quedan fuera del panel b: su margen es cero y la raz\u00f3n no est\u00e1 definida. '
          'Efecto suelo y d\u00e9ficit profundo son ambos plausibles en el grupo IB <20; estos datos no permiten separarlos.')},
}[LANG]
SH=T['sh']

# ---- datos ----
if XLSX is None:
    raise SystemExit('Falta la ruta al .xlsx. Uso: python3.13 build_curva2.py [en|es] <ruta>')
df=pd.read_excel(XLSX,sheet_name='Planilla Oficial')
df.columns=['id','edad','sexo','dias','tipo','egreso','bi_in','bi_eg','mm_in','mm_eg']
bc=lambda v:0 if v<20 else(1 if v<=35 else(2 if v<=55 else(3 if v<=99 else 4)))
pb=df.dropna(subset=['bi_in','bi_eg']).copy()
pb['ci']=pb.bi_in.map(bc); pb['d']=pb.bi_eg-pb.bi_in; pb['marg']=100-pb.bi_in
q=pb[pb.marg>0].copy(); q['share']=q.d/q.marg*100

rng=np.random.default_rng(20260904)

def boot_mean(x,B=5000):
    x=np.asarray(x,float); n=len(x)
    s=x[rng.integers(0,n,size=(B,n))].mean(axis=1)
    return np.percentile(s,[2.5,97.5])

def boot_ratio(d,m,B=5000):
    d=np.asarray(d,float); m=np.asarray(m,float); n=len(d)
    i=rng.integers(0,n,size=(B,n))
    s=100*d[i].sum(axis=1)/m[i].sum(axis=1)
    return np.percentile(s,[2.5,97.5])

# anclas: x = Barthel de ingreso medio del grupo
xs=[pb[pb.ci==c].bi_in.mean() for c in range(4)]
yA=[pb[pb.ci==c].d.mean() for c in range(4)]
ciA=[boot_mean(pb[pb.ci==c].d.values) for c in range(4)]
xsB=[q[q.ci==c].bi_in.mean() for c in range(4)]
yB=[100*q[q.ci==c].d.sum()/q[q.ci==c].marg.sum() for c in range(4)]
ciB=[boot_ratio(q[q.ci==c].d.values,q[q.ci==c].marg.values) for c in range(4)]
nA=[int((pb.ci==c).sum()) for c in range(4)]
coh=100*q.d.sum()/q.marg.sum()

import textwrap

fig,(a,b)=plt.subplots(2,1,figsize=(9.8,10.0),sharex=True,gridspec_kw={'hspace':.30})

def panel(ax,xa,ya,ci,dotx,doty,dotc,ptitle,ylab,pct):
    ax.set_axisbelow(True); ax.yaxis.grid(True,color=GRID,lw=.7)
    for c in range(5):
        m=dotc==c
        if m.any():
            ax.scatter(dotx[m],doty[m],s=34,color=CAT[c],alpha=.24,edgecolor='none',zorder=2)
    g=PchipInterpolator(xa,ya); gx=np.linspace(min(xa),max(xa),300)
    ax.plot(gx,g(gx),color='#3d3b36',lw=2.6,zorder=4,solid_capstyle='round')
    lo=min(float(np.min(doty)),min(float(c[0]) for c in ci))
    hi=max(float(np.max(doty)),max(float(c[1]) for c in ci))
    span=hi-lo
    for c in range(4):
        ax.vlines(xa[c],ci[c][0],ci[c][1],color=TXT[c],lw=2.4,alpha=.5,zorder=5)
        ax.scatter([xa[c]],[ya[c]],s=250,color=CAT[c],edgecolor=SURF,lw=2.4,zorder=6)
        v=f'{D(ya[c],0)}%' if pct else f'+{D(ya[c],0)}'
        ax.annotate(v,(xa[c],ci[c][1]),textcoords='offset points',xytext=(0,9),
                    ha='center',fontsize=14,weight='bold',color=TXT[c],zorder=7)
        ax.annotate(f"{SH[c]}\n{T['ibl']} {RG[c]} \u00b7 n={nA[c]}",(xa[c],ci[c][0]),
                    textcoords='offset points',xytext=(0,-11),ha='center',va='top',
                    fontsize=9.2,color=TXT[c],weight='bold',linespacing=1.3,zorder=7)
    ax.set_ylim(lo-span*.32, hi+span*.17)
    ax.set_ylabel(ylab,fontsize=11)
    ax.set_title(ptitle,fontsize=12.5,weight='bold',color=INK,loc='left',pad=10)

panel(a,xs,yA,ciA,pb.bi_in.values,pb.d.values,pb.ci.values,T['pa'],T['yla'],False)
panel(b,xsB,yB,ciB,q.bi_in.values,q.share.values,q.ci.values,T['pb'],T['ylb'],True)

b.axhline(coh,color=SEC,lw=1.3,ls=(0,(4,3)),zorder=3,label=T['coh'].format(v=D(coh,1)))
b.legend(loc='lower left',frameon=False,fontsize=9.4,labelcolor=SEC,
         handlelength=2.4,borderpad=.1,handletextpad=.7)

a.set_xlim(-8,110); b.set_xlim(-8,110)
b.set_xlabel(T['x'],fontsize=11.5)

fig.subplots_adjust(top=.845,bottom=.150,left=.088,right=.975)
fig.text(.012,.990,'\n'.join(textwrap.wrap(T['title'],64)),va='top',
         fontsize=15,weight='bold',color=INK,linespacing=1.25)
fig.text(.012,.902,'\n'.join(textwrap.wrap(T['sub'],130)),va='top',
         fontsize=9.8,color=SEC,linespacing=1.45)
fig.text(.012,.112,'\n'.join(textwrap.wrap(T['note'],152)),va='top',
         fontsize=9.0,color=MUT,linespacing=1.55)

for e in ('png','pdf'):
    fig.savefig(os.path.join(HERE,f'V8_curva_avance{SUF}.{e}'),dpi=300)
print('escrito V8_curva_avance'+SUF)
print('anclas x:',[round(float(v),1) for v in xs])
print('panel a (dBI medio):',[round(float(v),1) for v in yA],'IC',[[round(float(z),1) for z in c] for c in ciA])
print('panel b (share %):  ',[round(float(v),1) for v in yB],'IC',[[round(float(z),1) for z in c] for c in ciB])
print('cohorte:',round(float(coh),1),'  n por categoria:',nA)
