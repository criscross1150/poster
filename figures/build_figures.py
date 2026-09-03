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
SH=['Total','Severe','Moderate','Mild','Independent'];RG=['<20','20–35','40–55','60–99','100']
M=np.zeros((5,5),int)
for _,r in pb.iterrows():M[int(r.ci),int(r.ce)]+=1
def save(f,n):
    for e in('png','pdf'):f.savefig(f'figs2/{n}.{e}',dpi=300,bbox_inches='tight')
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
ax.text(-0.196,TOT/2,'greater independence',rotation=90,va='center',ha='center',fontsize=9,color=MUT)
ax.text(X0+BW/2,TOT+3.0,'ADMISSION',ha='center',fontsize=10.5,weight='bold',color=INK)
ax.text(X1-BW/2,TOT+3.0,'DISCHARGE',ha='center',fontsize=10.5,weight='bold',color=INK)
ax.text(0.5,TOT+10.6,'Every ribbon rises: not one patient lost a Barthel category',ha='center',fontsize=15,weight='bold',color=INK)
ax.text(0.5,TOT+6.6,'78 paired patients · median stay 5 days · 43 (55.1%) gained ≥1 category · 0 (0%) declined',ha='center',fontsize=10,color=SEC)
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
        a.text(.5,-17,f'+{s.d.mean():.0f} pts',ha='center',fontsize=13,weight='bold',color=TXT[k])
    a.set_title(f'{SH[k]}  {RG[k]}\nn={len(s)}',fontsize=10.5,weight='bold',color=INK,pad=10,linespacing=1.35)
    a.set_xlim(-.22,1.22);a.set_ylim(-6,106);a.set_xticks([0,1]);a.set_xticklabels(['adm','disch'],fontsize=9,color=MUT)
    a.spines['bottom'].set_visible(False)
    if k:a.spines['left'].set_visible(False)
axs[0].set_ylabel('Barthel Index (points)')
fig.text(.5,1.10,'The lower the admission category, the steeper the individual climb',ha='center',fontsize=15,weight='bold',color=INK)
fig.text(.5,1.015,'Each thin line is one patient; the thick line is the group mean. Every group mean rises — and no patient changed category downward.',ha='center',fontsize=10,color=SEC)
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
a.text(15,101,'mathematically impossible',color='#c0332f',fontsize=9.5,ha='left')
a.text(40,52,'ceiling = 100 − admission BI',color='#c0332f',fontsize=9,ha='center',rotation=-30)
a.set_xlabel('Admission Barthel Index');a.set_ylabel('ADL gain  ΔBI (points)')
a.set_xlim(-4,104);a.set_ylim(-12,112)
a.set_title('a. The ceiling caps every gain',fontsize=12,weight='bold',color=INK,loc='left',pad=12)
b=axs[1];b.set_axisbelow(True);b.yaxis.grid(True,color=GRID,lw=.7)
pct=[100*pb[pb.ci==c].d.sum()/(100-pb[pb.ci==c].bi_in).sum() for c in range(4)]
ns=[len(pb[pb.ci==c]) for c in range(4)]
b.bar(range(4),pct,width=.6,color=[RAMP[c] for c in range(4)],edgecolor=SURF,lw=2,zorder=3)
for i,(v,n) in enumerate(zip(pct,ns)):
    b.text(i,v+2.4,f'{v:.0f}%',ha='center',fontsize=13,weight='bold',color=INK)
    b.text(i,3.2,f'n={n}',ha='center',fontsize=9.5,color=ONFILL[i])
b.axhline(50.2,color=SEC,lw=1.2,ls=(0,(4,3)),zorder=4)
b.text(3.46,50.2,'cohort\n50.2%',fontsize=8.5,color=SEC,va='center',linespacing=1.3)
b.set_xticks(range(4));b.set_xticklabels([f'{SH[c]}\n{RG[c]}' for c in range(4)],fontsize=9.5,color=SEC,linespacing=1.35)
b.set_ylabel('Share of available headroom recovered (%)');b.set_ylim(0,84);b.set_xlim(-.6,3.95)
b.set_title('b. Corrected, severe patients recover most',fontsize=12,weight='bold',color=INK,loc='left',pad=12)
fig.text(.5,-.10,'Headroom = 100 − admission BI. Normalising by it removes the ceiling artefact and answers the regression-to-the-mean objection: the\nadvantage of the severe group (BI 20–35) is not explained by simply having had more room to improve. Independent patients (BI 100, n=4) are\nexcluded from panel b — their headroom is zero, so the ratio is undefined.',ha='center',fontsize=9.2,color=MUT,linespacing=1.6)
save(fig,'V3_techo_headroom')

# ===== V4 ESQUEMA =====
fig,ax=plt.subplots(figsize=(11,5.4));ax.axis('off')
rows=[(0,13,23.5,24,'Highest daily frequency,\nplus caregiver training'),
      (1,25,49.4,69,'Highest daily frequency —\nlargest achievable return'),
      (2,11,28.1,50,'Standard daily frequency'),
      (3,25,13.2,49,'Task-specific,\ndischarge-oriented')]
CX={'cat':.60,'n':1.62,'d':2.34,'bar':3.90,'pct':5.02,'dose':5.66}
BARL,BARW=2.90,1.85
top=4.30
for k,(c,n,dbi,hr,rec) in enumerate(rows):
    y=top-k*1.02
    ax.add_patch(Rectangle((0,y-.34),1.20,.68,color=RAMP[c],zorder=3))
    ax.text(CX['cat'],y+.11,SH[c],ha='center',va='center',fontsize=10.5,weight='bold',color=ONFILL[c])
    ax.text(CX['cat'],y-.14,'BI '+RG[c],ha='center',va='center',fontsize=8.8,color=ONFILL[c])
    ax.text(CX['n'],y,str(n),ha='center',va='center',fontsize=11,color=SEC)
    ax.text(CX['d'],y,f'+{dbi:.0f}',ha='center',va='center',fontsize=14,weight='bold',color=INK)
    ax.add_patch(Rectangle((BARL,y-.14),BARW,.28,color=GRID,zorder=2))
    ax.add_patch(Rectangle((BARL,y-.14),BARW*hr/100,.28,color=RAMP[c],zorder=3))
    ax.text(CX['pct'],y,f'{hr}%',va='center',ha='center',fontsize=11,weight='bold',color=INK)
    ax.add_patch(FancyArrowPatch((5.28,y),(5.56,y),arrowstyle='-|>',mutation_scale=12,color=BASE,lw=1.1))
    ax.text(CX['dose'],y,rec,va='center',fontsize=9.5,color=SEC,linespacing=1.35)
for x,t in ((CX['cat'],'Admission\ncategory'),(CX['n'],'Patients'),(CX['d'],'Mean\nΔBI'),(BARL+BARW/2,'Headroom recovered'),(CX['dose']+.55,'Indicated OT dose')):
    ax.text(x,top+.80,t,ha='center',va='center',fontsize=9,weight='bold',color=MUT,linespacing=1.3)
ax.plot([-.02,8.15],[top+.50,top+.50],color=BASE,lw=1)
ax.text(-.02,top+1.72,'Admission Barthel category as an occupational therapy dosing rule',fontsize=15,weight='bold',color=INK)
ax.text(-.02,top+1.30,'Recovery peaks in the severe group in both absolute points and share of what was recoverable — that is where dose should concentrate.',fontsize=9.8,color=SEC)
ax.set_xlim(-.10,8.25);ax.set_ylim(.75,top+2.05)
save(fig,'V4_esquema_dosificacion')
print('done')
