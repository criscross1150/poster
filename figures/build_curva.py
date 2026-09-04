# -*- coding: utf-8 -*-
"""La recuperación proporcional NO es monótona: hace pico en la banda severa."""
import sys
import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
SURF='#fcfcfb';INK='#0b0b0b';SEC='#52514e';MUT='#898781';GRID='#e1e0d9';BASE='#c3c2b7'
CAT=['#c0392b','#eda100','#1baf7a','#2a78d6','#4a3aa7']
TXT=['#a5322a','#8a5d00','#00694a','#2a78d6','#4a3aa7']
RG=['<20','20–35','40–55','60–99','100']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'text.color':INK,
 'axes.facecolor':SURF,'figure.facecolor':SURF,'axes.edgecolor':BASE,'axes.labelcolor':SEC,
 'xtick.color':MUT,'ytick.color':MUT,'axes.linewidth':.8,'xtick.major.size':0,
 'ytick.major.size':0,'axes.spines.top':False,'axes.spines.right':False,'savefig.facecolor':SURF})
LANG=sys.argv[1] if len(sys.argv)>1 else 'en'
SUF='' if LANG=='en' else '_es'
def D(x,dec=1):
    t=f'{x:.{dec}f}'
    return t.replace('.',',') if LANG=='es' else t
T={
 'en':{'sh':['Total','Severe','Moderate','Mild','Independent'],'ibl':'BI',
  'title':'Proportional recovery peaks in the severe band — not at the extreme of impairment',
  'sub':'Share of each patient’s available margin that was regained, against the Barthel on admission. Faint dots are patients; the large markers are the\npooled value per category. The most impaired group recovers the smallest share of its own margin, so the relationship is a peak, not a straight line.',
  'x':'Barthel Index on admission','y':'Share of available margin recovered (%)',
  'coh':'cohort 50.2%','peak':'peak: 69%','low':'lowest of all: 24%',
  'note':'Floor effect and profound deficit both plausible in the BI <20 group; these data cannot separate them.'},
 'es':{'sh':['Total','Severa','Moderada','Leve','Independiente'],'ibl':'IB',
  'title':'La recuperación proporcional hace pico en la banda severa, no en el extremo de gravedad',
  'sub':'Proporción del margen disponible de cada paciente que fue recuperada, según el Barthel de ingreso. Los puntos tenues son pacientes; los marcadores\ngrandes, el valor agrupado por categoría. El grupo más comprometido recupera la menor proporción de su margen: la relación es un pico, no una recta.',
  'x':'Índice de Barthel al ingreso','y':'Proporción del margen disponible recuperada (%)',
  'coh':'cohorte 50,2%','peak':'pico: 69%','low':'el más bajo: 24%',
  'note':'Efecto suelo y déficit profundo son ambos plausibles en el grupo IB <20; estos datos no permiten separarlos.'},
}[LANG]
SH=T['sh']
p="/root/.claude/uploads/ebfc8eed-2f56-566b-bc1f-b90c8b916e98/8bf4679e-REGISTRO_ACTUALIZADO_ACV_20242025_POSTER.xlsx"
df=pd.read_excel(p,sheet_name='Planilla Oficial')
df.columns=['id','edad','sexo','dias','tipo','egreso','bi_in','bi_eg','mm_in','mm_eg']
bc=lambda v:0 if v<20 else(1 if v<=35 else(2 if v<=55 else(3 if v<=99 else 4)))
pb=df.dropna(subset=['bi_in','bi_eg']).copy()
pb['ci']=pb.bi_in.map(bc); pb['d']=pb.bi_eg-pb.bi_in; pb['marg']=100-pb.bi_in
sub=pb[pb.ci<=3].copy(); sub['share']=100*sub.d/sub.marg

fig,ax=plt.subplots(figsize=(11.2,6.4))
ax.set_axisbelow(True); ax.yaxis.grid(True,color=GRID,lw=.7)
for c in range(4):
    s=sub[sub.ci==c]
    ax.scatter(s.bi_in,s.share,s=42,color=CAT[c],alpha=.28,edgecolor='none',zorder=2)
xs=[];ys=[]
for c in range(4):
    s=sub[sub.ci==c]
    x=s.bi_in.mean(); y=100*s.d.sum()/s.marg.sum(); xs.append(x); ys.append(y)
ax.plot(xs,ys,color=SEC,lw=2,zorder=4,solid_capstyle='round')
for c in range(4):
    ax.scatter([xs[c]],[ys[c]],s=340,color=CAT[c],edgecolor=SURF,lw=3,zorder=6)
    if c==1:   # el rotulo del pico esquiva la linea descendente
        ax.text(xs[c]-9,ys[c]-4,f"{SH[c]}\n{T['ibl']} {RG[c]}",ha='right',va='top',fontsize=10,
                color=TXT[c],weight='bold',linespacing=1.3)
    else:
        ax.text(xs[c],ys[c]-11,f"{SH[c]}\n{T['ibl']} {RG[c]}",ha='center',va='top',fontsize=10,
                color=TXT[c],weight='bold',linespacing=1.3)
    ax.text(xs[c],ys[c]+8.5,f'{ys[c]:.0f}%',ha='center',va='bottom',fontsize=14,weight='bold',color=TXT[c])
ax.axhline(50.2,color=SEC,lw=1.2,ls=(0,(4,3)),zorder=3)
ax.text(99,51.6,T['coh'],ha='right',va='bottom',fontsize=10,color=SEC)
ax.annotate(T['peak'],xy=(xs[1],ys[1]+3),xytext=(xs[1]+16,ys[1]+26),fontsize=11,color=TXT[1],
            weight='bold',arrowprops=dict(arrowstyle='-|>',color=TXT[1],lw=1.4,
            connectionstyle='arc3,rad=-0.25'))
ax.annotate(T['low'],xy=(xs[0],ys[0]-3),xytext=(xs[0]+7,ys[0]-30),fontsize=11,color=TXT[0],
            weight='bold',arrowprops=dict(arrowstyle='-|>',color=TXT[0],lw=1.4,
            connectionstyle='arc3,rad=0.25'))
ax.set_xlabel(T['x']); ax.set_ylabel(T['y'])
ax.set_xlim(-4,104); ax.set_ylim(-32,124); ax.set_xticks([0,20,40,60,80,100])
ax.set_yticks([0,25,50,75,100])
ax.text(-4,138,T['title'],fontsize=15,weight='bold',color=INK)
ax.text(-4,132,T['sub'],fontsize=9.8,color=SEC,va='top',linespacing=1.5)
fig.text(0.012,-0.035,T['note'],fontsize=9.2,color=MUT)
for e in('png','pdf'):fig.savefig(f'figs2/V7_curva{SUF}.{e}',dpi=300,bbox_inches='tight')
print('V7_curva'+SUF)
