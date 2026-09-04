import pandas as pd,numpy as np,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch,Rectangle,FancyArrowPatch
SURF='#fcfcfb';INK='#0b0b0b';SEC='#52514e';MUT='#898781';GRID='#e1e0d9';BASE='#c3c2b7'
CAT=['#c0392b','#eda100','#1baf7a','#2a78d6','#4a3aa7']
RG=['<20','20–35','40–55','60–99','100']
import sys
STR={
 'en':{'sh':['Total','Severe','Moderate','Mild','Independent'],'ibl':'BI','in':'in','out':'out',
   'axis':'greater independence',
   'title':'Patients climb the Barthel staircase \u2014 none stepped down',
   'sub':'78 paired patients \u00b7 median stay 5 days \u00b7 every arc runs to the right; a leftward arc would mean deterioration, and there is none',
   'foot':'Arc thickness is proportional to the number of patients making that move. Loops on a step are patients who stayed in their category.',
   'suffix':'','footy':-0.95,'y0':-1.35},
 'es':{'sh':['Total','Severa','Moderada','Leve','Independiente'],'ibl':'IB','in':'ingresan','out':'egresan',
   'axis':'mayor independencia',
   'title':'Los pacientes suben la escalera de Barthel \u2014 ninguno baj\u00f3 un escal\u00f3n',
   'sub':'78 pacientes pareados \u00b7 estad\u00eda mediana 5 d\u00edas\nTodos los arcos van hacia la derecha; un arco hacia la izquierda significar\u00eda deterioro, y no hay ninguno',
   'foot':'El grosor del arco es proporcional al n\u00famero de pacientes que hace ese movimiento.\nLos lazos sobre un escal\u00f3n son los pacientes que se mantuvieron en su categor\u00eda.',
   'suffix':'_es','footy':-0.98,'y0':-1.95},
}
LANG=sys.argv[1] if len(sys.argv)>1 else 'en'
T=STR[LANG]; SH=T['sh']
plt.rcParams.update({'font.family':'DejaVu Sans','text.color':INK,'axes.facecolor':SURF,'figure.facecolor':SURF,'savefig.facecolor':SURF})
p="/root/.claude/uploads/ebfc8eed-2f56-566b-bc1f-b90c8b916e98/8bf4679e-REGISTRO_ACTUALIZADO_ACV_20242025_POSTER.xlsx"
df=pd.read_excel(p,sheet_name='Planilla Oficial')
df.columns=['id','edad','sexo','dias','tipo','egreso','bi_in','bi_eg','mm_in','mm_eg']
bc=lambda v:0 if v<20 else(1 if v<=35 else(2 if v<=55 else(3 if v<=99 else 4)))
pb=df.dropna(subset=['bi_in','bi_eg']).copy();pb['ci']=pb.bi_in.map(bc);pb['ce']=pb.bi_eg.map(bc)
M=np.zeros((5,5),int)
for _,r in pb.iterrows():M[int(r.ci),int(r.ce)]+=1

fig,ax=plt.subplots(figsize=(11.4,7.2));ax.axis('off')
SW=1.0; SH_=1.0   # ancho y alto de cada escalón
tread=[]          # (x0,x1,ytop) de cada huella
for k in range(5):
    x0=k*SW; ytop=(k+1)*SH_
    tread.append((x0,x0+SW,ytop))
    ax.add_patch(Rectangle((x0,0),SW,ytop,facecolor=CAT[k],edgecolor=SURF,lw=2.5,zorder=3))
    ax.text(x0+SW/2,ytop-0.30,f"{SH[k]}\n{T['ibl']} {RG[k]}",ha='center',va='top',fontsize=11.5,
            color='#ffffff',weight='bold',linespacing=1.35,zorder=6)
    ax.text(x0+SW/2,-0.20,f"{M[k].sum()} {T['in']}",ha='center',va='top',fontsize=12,color=SEC,weight='bold')
    ax.text(x0+SW/2,-0.52,f"{M[:,k].sum()} {T['out']}",ha='center',va='top',fontsize=12,color=CAT[k],weight='bold')

MAXW=26.0
for i in range(5):
    for j in range(5):
        n=M[i,j]
        if n==0:continue
        x0,x1,y0=tread[i]; _,_,y1=tread[j]
        lw=1.6+MAXW*(n/25)**0.75
        if i==j:   # permanencia: lazo corto sobre la propia huella
            xa,xb=x0+SW*0.30,x0+SW*0.70; h=0.30
            v=[(xa,y0),(xa,y0+h),(xb,y0+h),(xb,y0)]
            c=[Path.MOVETO,Path.CURVE4,Path.CURVE4,Path.CURVE4]
            ax.add_patch(PathPatch(Path(v,c),fill=False,edgecolor=CAT[i],lw=lw*0.55,alpha=.75,capstyle='round',zorder=5))
            ax.text((xa+xb)/2,y0+h+0.06,str(n),ha='center',fontsize=10.5,color=CAT[i],weight='bold',zorder=6)
        else:      # ascenso: arco hacia la derecha
            xa=x0+SW*0.62; xb=x1+ (j-i-1)*SW + SW*0.38
            xb=tread[j][0]+SW*0.38
            rise=max(y1-y0,0.5); h=0.42+0.30*(j-i)
            v=[(xa,y0),(xa,y0+rise*0.55+h),(xb,y1+h*0.85),(xb,y1)]
            c=[Path.MOVETO,Path.CURVE4,Path.CURVE4,Path.CURVE4]
            ax.add_patch(PathPatch(Path(v,c),fill=False,edgecolor=CAT[i],lw=lw,alpha=.62,capstyle='round',zorder=4))
            if n>=2:
                P0=(xa,y0);P1=(xa,y0+rise*0.55+h);P2=(xb,y1+h*0.85);P3=(xb,y1)
                mx=(P0[0]+3*P1[0]+3*P2[0]+P3[0])/8.0
                my=(P0[1]+3*P1[1]+3*P2[1]+P3[1])/8.0
                ax.text(mx,my,str(n),ha='center',va='center',
                        fontsize=11.5,color=CAT[i],weight='bold',zorder=7,
                        bbox=dict(boxstyle='round,pad=0.22',fc=SURF,ec='none',alpha=.92))

ax.annotate('',xy=(5.16,5.05),xytext=(5.16,0.30),arrowprops=dict(arrowstyle='-|>',color=BASE,lw=1.6))
ax.text(5.34,2.6,T['axis'],rotation=90,va='center',ha='center',fontsize=10.5,color=MUT)
ax.text(2.5,6.62,T['title'],
        ha='center',fontsize=16,weight='bold',color=INK)
ax.text(2.5,6.10,T['sub'],
        ha='center',va='top',fontsize=10.5,color=SEC,linespacing=1.45)
ax.text(0.02,T['footy'],T['foot'],fontsize=10,color=MUT,va='top',linespacing=1.5)
ax.set_xlim(-0.30,5.62);ax.set_ylim(T['y0'],6.95)
for e in('png','pdf'):fig.savefig(f"figs2/V5_escalera{T['suffix']}.{e}",dpi=300,bbox_inches='tight')
print('ok')
