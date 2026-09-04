# -*- coding: utf-8 -*-
"""Cada paciente es una barra que va de su Barthel de ingreso al techo 100.
El relleno es lo que recorrio. El borde derecho recto ES el techo."""
import sys
import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

SURF='#fcfcfb';INK='#0b0b0b';SEC='#52514e';MUT='#898781';GRID='#e1e0d9';BASE='#c3c2b7'
EMPTY='#e6e4dc'
CAT=['#c0392b','#eda100','#1baf7a','#2a78d6','#4a3aa7']
TXT=['#a5322a','#8a5d00','#00694a','#2a78d6','#4a3aa7']
RG=['<20','20–35','40–55','60–99','100']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'text.color':INK,
 'axes.facecolor':SURF,'figure.facecolor':SURF,'axes.edgecolor':BASE,'axes.labelcolor':SEC,
 'xtick.color':MUT,'ytick.color':MUT,'axes.linewidth':.8,'xtick.major.size':0,
 'ytick.major.size':0,'axes.spines.top':False,'axes.spines.right':False,
 'axes.spines.left':False,'savefig.facecolor':SURF})

LANG=sys.argv[1] if len(sys.argv)>1 else 'en'
SUF='' if LANG=='en' else '_es'
def D(x,dec=1):
    t=f'{x:.{dec}f}'
    return t.replace('.',',') if LANG=='es' else t
T={
 'en':{'sh':['Total','Severe','Moderate','Mild','Independent'],'ibl':'BI',
  'title':'Every bar ends at the ceiling. The colour is how far each patient actually travelled.',
  'sub':'One bar per patient (n = 78), sorted by admission score. The bar runs from the Barthel on admission to the maximum of 100, so its length is\nexactly the margin that patient had left to recover. The filled part is the ground actually regained by discharge.',
  'x':'Barthel Index','ceil':'ceiling · Barthel 100','recov':'of the margin\nrecovered',
  'nomarg':'admitted at 100 — no margin left to recover','pat':'patients'},
 'es':{'sh':['Total','Severa','Moderada','Leve','Independiente'],'ibl':'IB',
  'title':'Todas las barras terminan en el techo. El color es cuánto recorrió cada paciente.',
  'sub':'Una barra por paciente (n = 78), ordenadas por puntaje de ingreso. La barra va del Barthel de ingreso al máximo de 100, así que su largo es\nexactamente el margen que ese paciente tenía por recuperar. La parte rellena es el terreno que efectivamente recobró al egreso.',
  'x':'Índice de Barthel','ceil':'techo · Barthel 100','recov':'del margen\nrecuperado',
  'nomarg':'ingresaron con 100 — sin margen por recuperar','pat':'pacientes'},
}[LANG]
SH=T['sh']

p="/root/.claude/uploads/ebfc8eed-2f56-566b-bc1f-b90c8b916e98/8bf4679e-REGISTRO_ACTUALIZADO_ACV_20242025_POSTER.xlsx"
df=pd.read_excel(p,sheet_name='Planilla Oficial')
df.columns=['id','edad','sexo','dias','tipo','egreso','bi_in','bi_eg','mm_in','mm_eg']
bc=lambda v:0 if v<20 else(1 if v<=35 else(2 if v<=55 else(3 if v<=99 else 4)))
pb=df.dropna(subset=['bi_in','bi_eg']).copy()
pb['ci']=pb.bi_in.map(bc); pb['d']=pb.bi_eg-pb.bi_in; pb['marg']=100-pb.bi_in

fig,ax=plt.subplots(figsize=(11.6,9.2))
RH,GAPY=1.0,2.6
y=0.0; ymarks=[]
for c in range(5):
    s=pb[pb.ci==c].sort_values(['bi_in','bi_eg'])
    y0=y
    for _,r in s.iterrows():
        ax.add_patch(Rectangle((r.bi_in,y),r.marg,RH*0.78,facecolor=EMPTY,edgecolor='none',zorder=2))
        if r.d>0:
            ax.add_patch(Rectangle((r.bi_in,y),r.d,RH*0.78,facecolor=CAT[c],edgecolor='none',zorder=3))
        y+=RH
    ymid=(y0+y-RH)/2+RH*0.39
    ymarks.append((c,y0,y-RH+RH*0.78,ymid,len(s)))
    y+=GAPY
YMAX=y-GAPY

for c,y0,y1,ymid,n in ymarks:
    ax.text(-3.5,ymid+RH*1.35,f"{SH[c]}",ha='right',va='center',fontsize=12,
            color=TXT[c],weight='bold')
    ax.text(-3.5,ymid-RH*1.35,f"{T['ibl']} {RG[c]}  ·  n = {n}",ha='right',va='center',
            fontsize=9.5,color=MUT)
    if c<4:
        s=pb[pb.ci==c]; pct=100*s.d.sum()/s.marg.sum()
        ax.plot([103.5,103.5],[y0,y1],color=CAT[c],lw=3,solid_capstyle='butt',zorder=4)
        ax.text(106,ymid,f'{pct:.0f}%',ha='left',va='center',fontsize=17,weight='bold',color=TXT[c])
    else:
        ax.text(106,ymid,T['nomarg'],ha='left',va='center',fontsize=9.5,color=MUT,style='italic')

ax.axvline(100,color=SEC,lw=2,zorder=6)
ax.text(100,YMAX+2.4,T['ceil'],ha='right',va='bottom',fontsize=10.5,color=SEC,weight='bold')
ax.text(106,YMAX+2.4,T['recov'],ha='left',va='bottom',fontsize=9.5,color=MUT,linespacing=1.35)
ax.set_xlim(-1,132); ax.set_ylim(-2.2,YMAX+27)
ax.set_xticks([0,20,40,60,80,100]); ax.set_xlabel(T['x'])
ax.set_yticks([]); ax.xaxis.grid(True,color=GRID,lw=.7); ax.set_axisbelow(True)
ax.spines['bottom'].set_visible(False)
ax.text(-1,YMAX+24.2,T['title'],fontsize=15.5,weight='bold',color=INK)
ax.text(-1,YMAX+21.4,T['sub'],fontsize=10,color=SEC,va='top',linespacing=1.5)
for e in('png','pdf'):fig.savefig(f'figs2/V6_margen{SUF}.{e}',dpi=300,bbox_inches='tight')
print('V6_margen'+SUF)
