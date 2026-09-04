# -*- coding: utf-8 -*-
"""Figuras con iconos: pictograma, escalera poblada y medidores de margen."""
import sys
import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch, Rectangle, FancyBboxPatch, Circle

SURF='#fcfcfb';INK='#0b0b0b';SEC='#52514e';MUT='#898781';GRID='#e1e0d9';BASE='#c3c2b7'
CAT=['#c0392b','#eda100','#1baf7a','#2a78d6','#4a3aa7']
TXT=['#a5322a','#8a5d00','#00694a','#2a78d6','#4a3aa7']
ONFILL=['#ffffff','#0b0b0b','#0b0b0b','#ffffff','#ffffff']
RG=['<20','20–35','40–55','60–99','100']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'text.color':INK,
 'axes.facecolor':SURF,'figure.facecolor':SURF,'savefig.facecolor':SURF})

LANG=sys.argv[1] if len(sys.argv)>1 else 'en'
SUF='' if LANG=='en' else '_es'
T={
 'en':{'sh':['Total','Severe','Moderate','Mild','Independent'],'ibl':'BI',
  'p1t':'One figure, one patient: no one is shaded below the column they arrived in',
  'p1s':'78 paired patients grouped by admission category and shaded by discharge category.\nA shade lighter than its own column would be a patient who lost ground; there is none.',
  'p1l':'Barthel category at discharge','adm':'Admission category',
  'p2t':'Who stands on each step of the Barthel staircase',
  'p2s':'One figure per patient admitted in that category. Arcs carry the moves between steps; every arc runs to the right.',
  'p3t':'How much of the recoverable margin each group actually regained',
  'p3s':'The tube is what was available to recover (100 − admission Barthel). The fill is what was regained.',
  'p3cap':'full available margin','p3coh':'cohort 50.2%','pat':'patients'},
 'es':{'sh':['Total','Severa','Moderada','Leve','Independiente'],'ibl':'IB',
  'p1t':'Una figura, un paciente: ninguno queda pintado por debajo de su columna de ingreso',
  'p1s':'78 pacientes pareados, agrupados por categoría de ingreso y pintados según la categoría de egreso.\nUn tono inferior al de su columna sería un paciente que retrocedió; no hay ninguno.',
  'p1l':'Categoría de Barthel al egreso','adm':'Categoría al ingreso',
  'p2t':'Quién está parado en cada escalón de la escalera de Barthel',
  'p2s':'Una figura por paciente ingresado en esa categoría. Los arcos llevan los movimientos entre escalones; todos van hacia la derecha.',
  'p3t':'Cuánto del margen recuperable recobró realmente cada grupo',
  'p3s':'El tubo es lo que había por recuperar (100 − Barthel de ingreso). El relleno es lo que se recobró.',
  'p3cap':'margen disponible completo','p3coh':'cohorte 50,2%','pat':'pacientes'},
}[LANG]
SH=T['sh']

p="/root/.claude/uploads/ebfc8eed-2f56-566b-bc1f-b90c8b916e98/8bf4679e-REGISTRO_ACTUALIZADO_ACV_20242025_POSTER.xlsx"
df=pd.read_excel(p,sheet_name='Planilla Oficial')
df.columns=['id','edad','sexo','dias','tipo','egreso','bi_in','bi_eg','mm_in','mm_eg']
bc=lambda v:0 if v<20 else(1 if v<=35 else(2 if v<=55 else(3 if v<=99 else 4)))
pb=df.dropna(subset=['bi_in','bi_eg']).copy()
pb['ci']=pb.bi_in.map(bc);pb['ce']=pb.bi_eg.map(bc);pb['d']=pb.bi_eg-pb.bi_in
M=np.zeros((5,5),int)
for _,r in pb.iterrows():M[int(r.ci),int(r.ce)]+=1

def person(ax,x,y,h,color,ec=None,lw=0.0,z=4,alpha=1.0):
    """Silueta de trazo: cabeza + torso con muesca de piernas. (x,y) = pie centrado."""
    w=h*0.30
    ax.add_patch(Circle((x,y+h*0.845),h*0.155,facecolor=color,edgecolor=ec or color,
                        lw=lw,zorder=z,alpha=alpha))
    v=[(x-w,y),(x-w,y+h*0.50),(x-w*0.98,y+h*0.62),(x-w*0.55,y+h*0.66),
       (x+w*0.55,y+h*0.66),(x+w*0.98,y+h*0.62),(x+w,y+h*0.50),(x+w,y),
       (x+w*0.26,y),(x+w*0.26,y+h*0.30),(x-w*0.26,y+h*0.30),(x-w*0.26,y),(x-w,y)]
    c=[Path.MOVETO,Path.LINETO,Path.CURVE3,Path.CURVE3,Path.LINETO,Path.CURVE3,Path.CURVE3,
       Path.LINETO,Path.LINETO,Path.LINETO,Path.LINETO,Path.LINETO,Path.CLOSEPOLY]
    ax.add_patch(PathPatch(Path(v,c),facecolor=color,edgecolor=ec or color,lw=lw,zorder=z,alpha=alpha))

def save(fig,n):
    for e in('png','pdf'):fig.savefig(f'figs2/{n}{SUF}.{e}',dpi=300,bbox_inches='tight')
    plt.close(fig);print(' '+n+SUF)

# ================= P1 · PICTOGRAMA =================
PER=5; PX=1.0; PY=1.42; GAP=1.75; H=0.95
fig,ax=plt.subplots(figsize=(12.6,6.8));ax.axis('off')
colw=(PER-1)*PX
RULE=H+0.42                      # regla de columna, por encima de la fila superior
for ci in range(5):
    x0=ci*(colw+GAP)
    dest=[]
    for ce in range(5): dest += [ce]*M[ci,ce]
    for idx,ce in enumerate(dest):
        r,c=divmod(idx,PER)
        person(ax,x0+c*PX,-r*PY,H,CAT[ce])
    ax.plot([x0-PX*0.42,x0+colw+PX*0.42],[RULE,RULE],color=CAT[ci],lw=3.2,solid_capstyle='butt')
    ax.text(x0+colw/2,RULE+0.22,f'n = {M[ci].sum()}',ha='center',va='bottom',fontsize=12.5,
            weight='bold',color=TXT[ci])
    ax.text(x0+colw/2,RULE+1.02,f"{SH[ci]}\n{T['ibl']} {RG[ci]}",ha='center',va='bottom',
            fontsize=11,color=SEC,linespacing=1.3)
TOPH=RULE+2.35
ymin=-(PY*((max(M.sum(1))-1)//PER))-0.35
LP=(5*(colw+GAP)-GAP)/5.0
for ce in range(5):
    hx=ce*LP
    person(ax,hx,ymin-1.75,H*0.84,CAT[ce])
    ax.text(hx+0.40,ymin-1.75+H*0.30,f"{SH[ce]} {RG[ce]} \u00b7 {M[:,ce].sum()}",ha='left',va='center',
            fontsize=10,color=SEC)
ax.text(0,ymin-0.80,T['p1l'],fontsize=10.5,color=MUT,weight='bold')
ax.text(0,TOPH+1.62,T['p1t'],fontsize=16,weight='bold',color=INK)
ax.text(0,TOPH+0.98,T['p1s'],fontsize=10.5,color=SEC,va='top',linespacing=1.5)
ax.set_xlim(-1.1,5*(colw+GAP)-GAP+0.9);ax.set_ylim(ymin-2.9,TOPH+2.9)
save(fig,'P1_pictograma')

# ================= P2 · ESCALERA POBLADA =================
SW=6.0; SH_=2.35; PER2=11; PX2=0.50; PY2=1.05; H2=0.92
fig,ax=plt.subplots(figsize=(13.4,7.6));ax.axis('off')
tread=[]
for k in range(5):
    x0=k*SW; ytop=(k+1)*SH_
    tread.append((x0,x0+SW,ytop))
    ax.add_patch(Rectangle((x0,0),SW,ytop,facecolor=CAT[k],edgecolor=SURF,lw=2.5,zorder=3))
    ax.text(x0+SW/2,ytop-0.42,f"{SH[k]}\n{T['ibl']} {RG[k]}",ha='center',va='top',fontsize=12,
            color=ONFILL[k],weight='bold',linespacing=1.35,zorder=6)
    n=M[k].sum()
    for i in range(n):
        r,c=divmod(i,PER2)
        cnt=min(PER2,n-r*PER2)
        person(ax,x0+SW/2+(c-(cnt-1)/2)*PX2,ytop+0.16+r*PY2,H2,CAT[k],z=7)
    ax.text(x0+SW/2,-0.28,f"{n} {T['pat']}",ha='center',va='top',fontsize=12,color=TXT[k],weight='bold')
# alturas de la multitud sobre cada escalon, para que los arcos pasen por encima
crowd=[]
for k in range(5):
    rows=(M[k].sum()-1)//PER2+1
    crowd.append(tread[k][2]+0.16+rows*PY2+0.28)
BAND=max(crowd)+0.55
MAXW=17.0
for i in range(5):
    for j in range(5):
        n=M[i,j]
        if n==0 or i==j: continue
        x0,_,_=tread[i]; xj,_,_=tread[j]
        xa=x0+SW*0.72; xb=xj+SW*0.28
        h=BAND+0.62*(j-i)
        P0,P1_,P2_,P3=(xa,crowd[i]),(xa,h),(xb,h),(xb,crowd[j])
        v=[P0,P1_,P2_,P3]
        c=[Path.MOVETO,Path.CURVE4,Path.CURVE4,Path.CURVE4]
        ax.add_patch(PathPatch(Path(v,c),fill=False,edgecolor=CAT[i],
                     lw=1.4+MAXW*(n/25)**0.75,alpha=.52,capstyle='round',zorder=5))
        mx=(P0[0]+3*P1_[0]+3*P2_[0]+P3[0])/8.0; my=(P0[1]+3*P1_[1]+3*P2_[1]+P3[1])/8.0
        ax.text(mx,my,str(n),ha='center',va='center',fontsize=11.5,color=TXT[i],weight='bold',zorder=9,
                bbox=dict(boxstyle='round,pad=0.22',fc=SURF,ec='none',alpha=.94))
TOP2=BAND+0.62*4+0.9
ax.text(0,TOP2+1.15,T['p2t'],fontsize=16.5,weight='bold',color=INK)
ax.text(0,TOP2+0.42,T['p2s'],fontsize=10.5,color=SEC)
ax.set_xlim(-0.6,5*SW+0.6);ax.set_ylim(-1.6,TOP2+2.3)
save(fig,'P2_escalera_poblada')

# ================= P3 · MEDIDORES DE MARGEN =================
pct=[100*pb[pb.ci==c].d.sum()/(100-pb[pb.ci==c].bi_in).sum() for c in range(4)]
ns=[len(pb[pb.ci==c]) for c in range(4)]
fig,ax=plt.subplots(figsize=(9.4,6.4));ax.axis('off')
TW,TH,TG=1.30,7.4,1.05
for i in range(4):
    x=i*(TW+TG)
    ax.add_patch(FancyBboxPatch((x,0),TW,TH,boxstyle='round,pad=0,rounding_size=0.30',
                 facecolor='#eeede7',edgecolor=BASE,lw=1.6,zorder=2))
    fh=TH*pct[i]/100
    ax.add_patch(FancyBboxPatch((x+0.10,0.10),TW-0.20,max(fh-0.20,0.30),
                 boxstyle='round,pad=0,rounding_size=0.22',facecolor=CAT[i],edgecolor='none',zorder=3))
    ax.plot([x-0.16,x+TW+0.16],[TH,TH],color=SEC,lw=2,zorder=5)
    ax.text(x+TW/2,fh+0.30,f'{pct[i]:.0f}%',ha='center',va='bottom',fontsize=17,weight='bold',color=INK,zorder=6)
    ax.text(x+TW/2,-0.42,f"{SH[i]}\n{T['ibl']} {RG[i]}",ha='center',va='top',fontsize=11,color=SEC,linespacing=1.3)
    ax.text(x+TW/2,-1.62,f'n = {ns[i]}',ha='center',va='top',fontsize=10.5,color=MUT)
xr=3*(TW+TG)+TW
ax.text(xr+0.30,TH,T['p3cap'],va='center',ha='left',fontsize=10.5,color=SEC)
ax.plot([-0.16,xr+0.16],[TH*0.502,TH*0.502],color=SEC,lw=1.3,ls=(0,(4,3)),zorder=5)
ax.text(xr+0.30,TH*0.502,T['p3coh'],va='center',ha='left',fontsize=10.5,color=SEC)
ax.text(0,TH+1.62,T['p3t'],fontsize=16,weight='bold',color=INK)
ax.text(0,TH+0.92,T['p3s'],fontsize=10.5,color=SEC)
ax.set_xlim(-0.5,xr+3.5);ax.set_ylim(-2.4,TH+2.5)
save(fig,'P3_medidores')
print('done')
