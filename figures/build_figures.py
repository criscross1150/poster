import pandas as pd,numpy as np,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch,Rectangle,FancyArrowPatch
SURF='#fcfcfb';INK='#0b0b0b';SEC='#52514e';MUT='#898781';GRID='#e1e0d9';BASE='#c3c2b7'
RAMP=['#c0392b','#eda100','#1baf7a','#2a78d6','#4a3aa7']
# variantes oscuras para TEXTO: ambar y aqua no alcanzan 3:1 sobre fondo claro
TXT=['#a5322a','#8a5d00','#00694a','#2a78d6','#4a3aa7']
# texto sobre bloque relleno: claro sobre los oscuros, tinta sobre ambar y aqua
ONFILL=['#ffffff','#0b0b0b','#0b0b0b','#ffffff','#ffffff']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'text.color':INK,'axes.facecolor':SURF,
 'figure.facecolor':SURF,'axes.edgecolor':BASE,'axes.labelcolor':SEC,'xtick.color':MUT,'ytick.color':MUT,
 'axes.linewidth':.8,'xtick.major.size':0,'ytick.major.size':0,'axes.spines.top':False,
 'axes.spines.right':False,'savefig.facecolor':SURF})
p="/root/.claude/uploads/ebfc8eed-2f56-566b-bc1f-b90c8b916e98/8bf4679e-REGISTRO_ACTUALIZADO_ACV_20242025_POSTER.xlsx"
df=pd.read_excel(p,sheet_name='Planilla Oficial')
df.columns=['id','edad','sexo','dias','tipo','egreso','bi_in','bi_eg','mm_in','mm_eg']
bc=lambda v:0 if v<20 else(1 if v<=35 else(2 if v<=55 else(3 if v<=99 else 4)))
pb=df.dropna(subset=['bi_in','bi_eg']).copy();pb['ci']=pb.bi_in.map(bc);pb['ce']=pb.bi_eg.map(bc);pb['d']=pb.bi_eg-pb.bi_in
RG=['<20','20–35','40–55','60–99','100']
import sys
LANG=sys.argv[1] if len(sys.argv)>1 else 'en'
SUF='' if LANG=='en' else '_es'
def D(x,dec=1):
    """Numero formateado; coma decimal en espanol."""
    t=f'{x:.{dec}f}'
    return t.replace('.',',') if LANG=='es' else t
T={
 'en':{'sh':['Total','Severe','Moderate','Mild','Independent'],
  'ibl':'BI','adm':'ADMISSION','dis':'DISCHARGE','axis':'greater independence',
  'v1t':'Every ribbon rises: not one patient lost a Barthel category',
  'v1s':'78 paired patients \u00b7 median stay 5 days \u00b7 43 (55.1%) gained \u22651 category \u00b7 0 (0%) declined',
  'ylab':'Barthel Index (points)','admS':'adm','disS':'disch','pts':'pts',
  'v2t':'The lower the admission category, the steeper the individual climb',
  'v2s':'Each thin line is one patient; the thick line is the group mean. Every group mean rises \u2014 and no patient changed category downward.',
  'v3at':'a. The ceiling caps every gain','v3bt':'b. Corrected, severe patients recover most',
  'imp':'mathematically impossible','impxy':(15,101),'ceil':'ceiling = 100 \u2212 admission BI',
  'xlab':'Admission Barthel Index','ygain':'ADL gain  \u0394BI (points)',
  'yshare':'Share of available headroom recovered (%)','coh':'cohort',
  'v3f':'Headroom = 100 \u2212 admission BI. Normalising by it removes the ceiling artefact and answers the regression-to-the-mean objection: the\nadvantage of the severe group (BI 20\u201335) is not explained by simply having had more room to improve. Independent patients (BI 100, n=4) are\nexcluded from panel b \u2014 their headroom is zero, so the ratio is undefined.',
  'v4t':'Recovery by admission Barthel category',
  'v4s':'Recovery peaks in the severe group, in both absolute points and in share of what was recoverable.',
  'h1':'Admission\ncategory','h2':'Patients','h3':'Mean\n\u0394BI','h4':'Headroom recovered','h5':'Proposed dose\nAUTHORS\u2019 INFERENCE,\nNOT A RESULT',
  'dose':['\u2014','Priority for the highest\ndaily session frequency','\u2014','\u2014'],'v4f':'This cohort did not measure occupational therapy dose: every patient received what the unit provided, with no variation to compare. The single\nproposal above rests on the recovery pattern observed here together with external dose evidence, and is an inference by the authors, not a finding\nof this study. No differentiated recommendation is made for the other categories, and none is supported by these data.'},
 'es':{'sh':['Total','Severa','Moderada','Leve','Independiente'],
  'ibl':'IB','adm':'INGRESO','dis':'EGRESO','axis':'mayor independencia',
  'v1t':'Todas las cintas ascienden: ning\u00fan paciente perdi\u00f3 una categor\u00eda de Barthel',
  'v1s':'78 pacientes pareados \u00b7 estad\u00eda mediana 5 d\u00edas \u00b7 43 (55,1%) mejor\u00f3 \u22651 categor\u00eda \u00b7 0 (0%) descendi\u00f3',
  'ylab':'\u00cdndice de Barthel (puntos)','admS':'ingr.','disS':'egr.','pts':'pts',
  'v2t':'Cuanto m\u00e1s baja la categor\u00eda de ingreso, m\u00e1s empinado el ascenso',
  'v2s':'Cada l\u00ednea fina es un paciente; la l\u00ednea gruesa es la media del grupo. Todas las medias suben, y ning\u00fan paciente descendi\u00f3 de categor\u00eda.',
  'v3at':'a. El techo limita toda ganancia','v3bt':'b. Corregido, los severos recuperan m\u00e1s',
  'imp':'matem\u00e1ticamente imposible','impxy':(4,104),'ceil':'techo = 100 \u2212 Barthel de ingreso',
  'xlab':'\u00cdndice de Barthel al ingreso','ygain':'Ganancia en AVD  \u0394IB (puntos)',
  'yshare':'Margen disponible recuperado (%)','coh':'cohorte',
  'v3f':'Margen disponible = 100 \u2212 Barthel de ingreso. Normalizar por \u00e9l elimina el artefacto del techo y responde a la objeci\u00f3n de regresi\u00f3n a la media:\nla ventaja del grupo severo (IB 20\u201335) no se explica por haber tenido simplemente m\u00e1s espacio para mejorar. Los pacientes independientes al\ningreso (IB 100, n=4) quedan excluidos del panel b: su margen es cero y el cociente resulta indefinido.',
  'v4t':'Recuperaci\u00f3n seg\u00fan la categor\u00eda de Barthel al ingreso',
  'v4s':'La recuperaci\u00f3n es m\u00e1xima en el grupo severo, tanto en puntos absolutos como en proporci\u00f3n de lo recuperable.',
  'h1':'Categor\u00eda\nal ingreso','h2':'Pacientes','h3':'\u0394IB\nmedio','h4':'Margen recuperado','h5':'Dosis propuesta\nINFERENCIA DE LOS AUTORES,\nNO UN RESULTADO',
  'dose':['\u2014','Prioridad para la mayor\nfrecuencia diaria de sesiones','\u2014','\u2014'],'v4f':'Esta cohorte no midi\u00f3 la dosis de terapia ocupacional: todos los pacientes recibieron lo que la unidad entregaba, sin variaci\u00f3n que comparar.\nLa \u00fanica propuesta anterior se apoya en el patr\u00f3n de recuperaci\u00f3n observado aqu\u00ed junto con evidencia externa de dosis, y es una inferencia de los\nautores, no un hallazgo de este estudio. No se formula recomendaci\u00f3n diferenciada para las dem\u00e1s categor\u00edas, ni estos datos la respaldan.'},
}[LANG]
SH=T['sh']
M=np.zeros((5,5),int)
for _,r in pb.iterrows():M[int(r.ci),int(r.ce)]+=1
def save(f,n):
    for e in('png','pdf'):f.savefig(f'figs2/{n}{SUF}.{e}',dpi=300,bbox_inches='tight')
    plt.close(f);print(' '+n)

# ===== V1 ALLUVIAL (mejor arriba: la mejoría ASCIENDE) =====
ORD=[4,3,2,1,0]
fig,ax=plt.subplots(figsize=(9.6,6.6));ax.axis('off')
GAP=1.8;TOT=78+4*GAP;X0,X1,BW=0.0,1.0,0.05
li={};ry={};y=TOT
for k in ORD:
    h=M[k].sum();li[k]=(y-h,y);y-=h+GAP
y=TOT
for k in ORD:
    h=M[:,k].sum();ry[k]=(y-h,y);y-=h+GAP
for k in ORD:
    for arr,x in ((li,X0),(ry,X1-BW)):
        a,b=arr[k]
        if b-a>0:ax.add_patch(Rectangle((x,a),BW,b-a,color=RAMP[k],zorder=6))
cl={k:li[k][0] for k in ORD};cr={k:ry[k][0] for k in ORD}   # llenar de abajo hacia arriba
for i in ORD[::-1]:
    for j in ORD[::-1]:
        n=M[i,j]
        if n==0:continue
        l0,l1=cl[i],cl[i]+n;cl[i]=l1
        r0,r1=cr[j],cr[j]+n;cr[j]=r1
        xa,xb=X0+BW,X1-BW;xm=(xa+xb)/2
        v=[(xa,l1),(xm,l1),(xm,r1),(xb,r1),(xb,r0),(xm,r0),(xm,l0),(xa,l0),(xa,l1)]
        c=[Path.MOVETO,Path.CURVE4,Path.CURVE4,Path.CURVE4,Path.LINETO,Path.CURVE4,Path.CURVE4,Path.CURVE4,Path.CLOSEPOLY]
        ax.add_patch(PathPatch(Path(v,c),facecolor=RAMP[i],edgecolor=SURF,lw=.7,alpha=.60 if i!=j else .26,zorder=3))
for k in ORD:
    a,b=li[k]
    if b-a>0:
        ax.text(X0-0.016,(a+b)/2,f'{SH[k]}\n{RG[k]}',ha='right',va='center',fontsize=9.5,color=SEC,linespacing=1.3)
        ax.text(X0+BW/2,(a+b)/2,str(M[k].sum()),ha='center',va='center',fontsize=10,weight='bold',color=ONFILL[k],zorder=7)
    a,b=ry[k]
    if b-a>0:
        ax.text(X1+0.016,(a+b)/2,f'{SH[k]}\n{RG[k]}',ha='left',va='center',fontsize=9.5,color=SEC,linespacing=1.3)
        ax.text(X1-BW/2,(a+b)/2,str(M[:,k].sum()),ha='center',va='center',fontsize=10,weight='bold',color=ONFILL[k],zorder=7)
ax.annotate('',xy=(-0.175,TOT),xytext=(-0.175,0),arrowprops=dict(arrowstyle='-|>',color=BASE,lw=1.4))
ax.text(-0.196,TOT/2,T['axis'],rotation=90,va='center',ha='center',fontsize=9,color=MUT)
ax.text(X0+BW/2,TOT+3.0,T['adm'],ha='center',fontsize=10.5,weight='bold',color=INK)
ax.text(X1-BW/2,TOT+3.0,T['dis'],ha='center',fontsize=10.5,weight='bold',color=INK)
ax.text(0.5,TOT+10.6,T['v1t'],ha='center',fontsize=15,weight='bold',color=INK)
ax.text(0.5,TOT+6.6,T['v1s'],ha='center',fontsize=10,color=SEC)
ax.set_xlim(-0.30,1.24);ax.set_ylim(-3,TOT+13)
save(fig,'V1_alluvial_categorias')

# ===== V2 SMALL MULTIPLES =====
fig,axs=plt.subplots(1,5,figsize=(12.4,3.9),sharey=True,gridspec_kw={'wspace':.14})
for k in range(5):
    a=axs[k];s=pb[pb.ci==k]
    a.set_axisbelow(True);a.yaxis.grid(True,color=GRID,lw=.7)
    for _,r in s.iterrows():
        a.plot([0,1],[r.bi_in,r.bi_eg],color=RAMP[k],lw=1.4,alpha=.42,solid_capstyle='round',zorder=3)
    if len(s):
        a.plot([0,1],[s.bi_in.mean(),s.bi_eg.mean()],color=RAMP[k],lw=4,zorder=5,solid_capstyle='round')
        a.text(.5,-17,f"+{s.d.mean():.0f} {T['pts']}",ha='center',fontsize=13,weight='bold',color=TXT[k])
    a.set_title(f'{SH[k]}  {RG[k]}\nn={len(s)}',fontsize=10.5,weight='bold',color=INK,pad=10,linespacing=1.35)
    a.set_xlim(-.22,1.22);a.set_ylim(-6,106);a.set_xticks([0,1]);a.set_xticklabels([T['admS'],T['disS']],fontsize=9,color=MUT)
    a.spines['bottom'].set_visible(False)
    if k:a.spines['left'].set_visible(False)
axs[0].set_ylabel(T['ylab'])
fig.text(.5,1.10,T['v2t'],ha='center',fontsize=15,weight='bold',color=INK)
fig.text(.5,1.015,T['v2s'],ha='center',fontsize=10,color=SEC)
save(fig,'V2_small_multiples')

# ===== V3 TECHO =====
fig,axs=plt.subplots(1,2,figsize=(11.4,5.0),gridspec_kw={'wspace':.30})
a=axs[0];a.set_axisbelow(True);a.yaxis.grid(True,color=GRID,lw=.7)
xs=np.linspace(0,100,50)
a.fill_between(xs,100-xs,112,color='#e34948',alpha=.055,zorder=1)
a.plot(xs,100-xs,color='#e34948',lw=2,ls=(0,(5,3)),zorder=4)
for c in range(5):
    sub=pb[pb.ci==c]
    if len(sub): a.scatter(sub.bi_in,sub.d,s=52,color=RAMP[c],alpha=.80,edgecolor=SURF,lw=1.6,zorder=3,label=f'{SH[c]} {RG[c]}')
leg=a.legend(loc='upper right',bbox_to_anchor=(1.0,0.99),frameon=False,fontsize=8.6,labelcolor=SEC,handletextpad=.5,borderpad=.2,labelspacing=.35)
a.text(T['impxy'][0],T['impxy'][1],T['imp'],color='#c0332f',fontsize=9.5,ha='left')
a.text(40,52,T['ceil'],color='#c0332f',fontsize=9,ha='center',rotation=-30)
a.set_xlabel(T['xlab']);a.set_ylabel(T['ygain'])
a.set_xlim(-4,104);a.set_ylim(-12,112)
a.set_title(T['v3at'],fontsize=12,weight='bold',color=INK,loc='left',pad=12)
b=axs[1];b.set_axisbelow(True);b.yaxis.grid(True,color=GRID,lw=.7)
pct=[100*pb[pb.ci==c].d.sum()/(100-pb[pb.ci==c].bi_in).sum() for c in range(4)]
ns=[len(pb[pb.ci==c]) for c in range(4)]
b.bar(range(4),pct,width=.6,color=[RAMP[c] for c in range(4)],edgecolor=SURF,lw=2,zorder=3)
for i,(v,n) in enumerate(zip(pct,ns)):
    b.text(i,v+2.4,f'{v:.0f}%',ha='center',fontsize=13,weight='bold',color=INK)
    b.text(i,3.2,f'n={n}',ha='center',fontsize=9.5,color=ONFILL[i])
b.axhline(50.2,color=SEC,lw=1.2,ls=(0,(4,3)),zorder=4)
b.text(3.46,50.2,T['coh']+'\n'+D(50.2)+'%',fontsize=8.5,color=SEC,va='center',linespacing=1.3)
b.set_xticks(range(4));b.set_xticklabels([f'{SH[c]}\n{RG[c]}' for c in range(4)],fontsize=9.5,color=SEC,linespacing=1.35)
b.set_ylabel(T['yshare']);b.set_ylim(0,84);b.set_xlim(-.6,3.95)
b.set_title(T['v3bt'],fontsize=12,weight='bold',color=INK,loc='left',pad=12)
fig.text(.5,-.10,T['v3f'],ha='center',fontsize=9.2,color=MUT,linespacing=1.6)
save(fig,'V3_techo_headroom')

# ===== V4 ESQUEMA =====
fig,ax=plt.subplots(figsize=(11,5.4));ax.axis('off')
rows=[(0,13,23.5,24,T['dose'][0]),
      (1,25,49.4,69,T['dose'][1]),
      (2,11,28.1,50,T['dose'][2]),
      (3,25,13.2,49,T['dose'][3])]
CX={'cat':.60,'n':1.62,'d':2.34,'bar':3.90,'pct':5.02,'dose':5.66}
BARL,BARW=2.90,1.85
top=4.30
for k,(c,n,dbi,hr,rec) in enumerate(rows):
    y=top-k*1.02
    ax.add_patch(Rectangle((0,y-.34),1.20,.68,color=RAMP[c],zorder=3))
    ax.text(CX['cat'],y+.11,SH[c],ha='center',va='center',fontsize=10.5,weight='bold',color=ONFILL[c])
    ax.text(CX['cat'],y-.14,T['ibl']+' '+RG[c],ha='center',va='center',fontsize=8.8,color=ONFILL[c])
    ax.text(CX['n'],y,str(n),ha='center',va='center',fontsize=11,color=SEC)
    ax.text(CX['d'],y,f'+{dbi:.0f}',ha='center',va='center',fontsize=14,weight='bold',color=INK)
    ax.add_patch(Rectangle((BARL,y-.14),BARW,.28,color=GRID,zorder=2))
    ax.add_patch(Rectangle((BARL,y-.14),BARW*hr/100,.28,color=RAMP[c],zorder=3))
    ax.text(CX['pct'],y,f'{hr}%',va='center',ha='center',fontsize=11,weight='bold',color=INK)
    if rec=='\u2014':
        ax.text(CX['dose']+.55,y,rec,va='center',ha='center',fontsize=13,color=BASE)
    else:
        ax.text(CX['dose'],y,rec,va='center',fontsize=9.8,color=INK,weight='bold',linespacing=1.35)
for x,t in ((CX['cat'],T['h1']),(CX['n'],T['h2']),(CX['d'],T['h3']),(BARL+BARW/2,T['h4'])):
    ax.text(x,top+.80,t,ha='center',va='center',fontsize=9,weight='bold',color=MUT,linespacing=1.3)
ax.text(CX['dose']+.55,top+1.12,T['h5'],ha='center',va='center',fontsize=8.4,weight='bold',
        color=MUT,style='italic',linespacing=1.5)
ax.plot([-.02,5.34],[top+.50,top+.50],color=BASE,lw=1)
ax.plot([5.50,8.15],[top+.50,top+.50],color=BASE,lw=1,ls=(0,(3,2)))
SEPX=5.42
ax.plot([SEPX,SEPX],[top-3.62,top+1.02],color=BASE,lw=1,ls=(0,(3,2)))
ax.text(-.02,top+2.56,T['v4t'],fontsize=15,weight='bold',color=INK)
ax.text(-.02,top+2.00,T['v4s'],fontsize=9.8,color=SEC)
ax.text(-.02,.34,T['v4f'],fontsize=8.2,color=MUT,va='top',linespacing=1.55)
ax.set_xlim(-.10,8.25);ax.set_ylim(-.72,top+3.17)
save(fig,'V4_esquema_dosificacion')
print('done')
