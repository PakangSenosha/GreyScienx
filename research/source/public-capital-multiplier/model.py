from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

WORK=Path(__file__).resolve().parent; ASSETS=WORK/"assets"; ASSETS.mkdir(parents=True,exist_ok=True)
STYLE=Path(r"C:\Users\Deriv\Desktop\GreyScienx\skills\greyscienx-editorial-pdf\scripts"); sys.path.insert(0,str(STYLE))
from greyscienx_style import add_figure_header,configure_matplotlib,save_figure,style_axis  # noqa: E402
T=configure_matplotlib(Path(r"C:\Users\Deriv\Desktop\GreyScienx\app\globals.css")); C,K,W,G1,G3,G5,G7=T["coral"],T["black"],T["white"],T["grey-100"],T["grey-300"],T["grey-500"],T["grey-700"]
PUBLIC=225.0
INSTRUMENTS={
 "Public ownership":{"multiple":1.0,"public_loss":.25,"control":1.0,"private":0},
 "Co-investment":{"multiple":1.5,"public_loss":.18,"control":.55,"private":.33},
 "Concessional debt":{"multiple":2.0,"public_loss":.10,"control":.35,"private":.50},
 "Minority public equity":{"multiple":2.5,"public_loss":.22,"control":.30,"private":.60},
 "First-loss layer":{"multiple":3.0,"public_loss":.38,"control":.22,"private":.67},
 "Guarantee reserve":{"multiple":4.0,"public_loss":.55,"control":.12,"private":.75},
}
PORTFOLIO={"Common infrastructure":50,"Concessional debt":55,"Minority equity":45,"First-loss capital":25,"Guarantee reserve":15,"Project preparation":15,"Skills + supplier funds":20}
PORT_MULT={"Common infrastructure":1.2,"Concessional debt":2.0,"Minority equity":2.8,"First-loss capital":4.0,"Guarantee reserve":5.0,"Project preparation":1.0,"Skills + supplier funds":1.0}

def head(fig,title,subtitle): add_figure_header(fig,title,subtitle,field="GREYSCIENCX / PAPER 9",tokens=T)
def done(fig,name,*,top=.77,bottom=.14,left=.10,right=.97): fig.subplots_adjust(top=top,bottom=bottom,left=left,right=right);save_figure(fig,ASSETS/name,dpi=270);plt.close(fig)

def multiples():
 fig,ax=plt.subplots(figsize=(9.4,5.3));head(fig,"Leverage rises as public control falls","R1 of public capital; gross project value is not public profit")
 n=list(INSTRUMENTS);m=[x["multiple"] for x in INSTRUMENTS.values()];x=np.arange(len(n));ax.bar(x,m,color=[K,G7,G5,C,C,K]);ax.set_xticks(x,[s.replace(" ","\n",1) for s in n]);ax.set_ylabel("Gross investment mobilised per R1 public capital");style_axis(ax,grid_axis="y")
 for i,v in enumerate(m):ax.text(i,v+.08,f"{v:.1f}x",ha="center",fontweight="bold")
 done(fig,"multiples.png",bottom=.22)

def stacks():
 fig,ax=plt.subplots(figsize=(9.4,5.3));head(fig,"The multiplier is a capital stack, not money created","Illustrative funding shares; public support changes position and risk")
 names=list(INSTRUMENTS); public=[1/x["multiple"]*100 for x in INSTRUMENTS.values()]; private=[x["private"]*100 for x in INSTRUMENTS.values()]; other=[max(0,100-a-b) for a,b in zip(public,private)];x=np.arange(len(names))
 ax.bar(x,public,label="Public cash / reserve",color=C);ax.bar(x,private,bottom=public,label="Private capital",color=K);ax.bar(x,other,bottom=np.array(public)+private,label="DFI / user / other",color=G5)
 ax.set_xticks(x,[n.replace(" ","\n",1) for n in names]);ax.set_ylabel("Share of gross project capital (%)");ax.legend(frameon=False,ncol=3,loc="upper center",bbox_to_anchor=(.5,-.18));style_axis(ax,grid_axis="y");done(fig,"capital-stacks.png",bottom=.27)

def scenario():
 fig,ax=plt.subplots(figsize=(9.4,5.2));head(fig,"R225 billion can support R225-R900 billion on paper","Simple mobilisation scenarios before defaults, crowding-out and unused facilities")
 mult=np.array([1,1.5,2,3,4]);tot=PUBLIC*mult;x=np.arange(len(mult));ax.bar(x,tot,color=[G5,G5,C,C,K]);ax.set_xticks(x,[f"{v:g}x" for v in mult]);ax.set_ylabel("Gross industrial investment (R billion)");style_axis(ax,grid_axis="y")
 for i,v in enumerate(tot):ax.text(i,v+18,f"R{v:,.0f}bn",ha="center",fontweight="bold")
 done(fig,"scenario.png")

def portfolio():
 fig,ax=plt.subplots(figsize=(9.4,5.3));head(fig,"A mixed portfolio mobilises R506 billion","Illustrative R225bn public envelope; gross project value, not fiscal saving")
 n=list(PORTFOLIO);pub=np.array(list(PORTFOLIO.values()));gross=np.array([PORTFOLIO[k]*PORT_MULT[k] for k in n]);x=np.arange(len(n));w=.36
 ax.bar(x-w/2,pub,w,label="Public capital",color=C);ax.bar(x+w/2,gross,w,label="Gross investment",color=K);ax.set_xticks(x,[s.replace(" ","\n",1) for s in n]);ax.set_ylabel("R billion");ax.legend(frameon=False,ncol=2);style_axis(ax,grid_axis="y");done(fig,"portfolio.png",bottom=.24)

def risk_return():
 fig,ax=plt.subplots(figsize=(9.4,5.3));head(fig,"More mobilisation usually means more hidden tail risk","Expected public loss is illustrative; bubble size shows public control")
 for name,d in INSTRUMENTS.items():
  x=d["multiple"];y=d["public_loss"]*100;ax.scatter(x,y,s=90+650*d["control"],color=C if x>=2.5 else G7,alpha=.9);ax.annotate(name,(x,y),xytext=(5,5),textcoords="offset points",fontsize=8)
 ax.set_xlabel("Gross mobilisation multiple");ax.set_ylabel("Loss of public support in adverse project (%)");style_axis(ax);done(fig,"risk-return.png")

def contingent():
 fig,ax=plt.subplots(figsize=(9.4,5.3));head(fig,"A small guarantee reserve can create a large fiscal surprise","Illustrative 10-year claims on R75bn guaranteed exposure")
 loss_rates=np.array([0,5,10,20,35,50]);prob=np.array([20,25,20,18,12,5]);claims=75*loss_rates/100;x=np.arange(len(loss_rates));ax.bar(x,prob,color=[G5,G5,G5,C,C,K]);ax.set_xticks(x,[f"R{v:.1f}bn" for v in claims]);ax.set_xlabel("Cumulative guarantee claims");ax.set_ylabel("Scenario probability (%)");style_axis(ax,grid_axis="y");done(fig,"contingent.png")

def crowding():
 fig,ax=plt.subplots(figsize=(9.4,5.3));head(fig,"Mobilised capital is not necessarily additional capital","R450bn gross investment at 2x; displacement reduces the net gain")
 crowd=np.array([0,10,25,40,60]);net=450-(450-PUBLIC)*crowd/100;x=np.arange(len(crowd));ax.plot(crowd,net,color=C,marker="o",linewidth=2.5);ax.axhline(PUBLIC,color=K,linestyle="--");ax.text(43,PUBLIC+10,"public-only floor",color=G7)
 ax.set_xlabel("Private investment displaced rather than added (%)");ax.set_ylabel("Net additional investment (R billion)");style_axis(ax);done(fig,"crowding.png")

def returns():
 fig,ax=plt.subplots(figsize=(9.4,5.3));head(fig,"Leverage improves reach but narrows the return buffer","Illustrative public portfolio value after 15 years; initial public capital R225bn")
 rates=np.array([-5,0,3,6,9]);vals={"Direct ownership":PUBLIC*(1+rates/100)**15,"Mixed 2.25x portfolio":PUBLIC*.65*(1+rates/100)**15+PUBLIC*.35,"High leverage":PUBLIC*.35*(1+rates/100)**15+PUBLIC*.65}
 for i,(n,v) in enumerate(vals.items()):ax.plot(rates,v,color=[C,K,G5][i],marker=["o","s","D"][i],linestyle=["-","--",":"][i],label=n)
 ax.axhline(PUBLIC,color=G3);ax.set_xlabel("Real annual return on invested public claims (%)");ax.set_ylabel("Public portfolio value in year 15 (R billion)");ax.legend(frameon=False);style_axis(ax);done(fig,"returns.png")

def waterfall():
 fig,ax=plt.subplots(figsize=(9.4,5.2));head(fig,"The model's R506 billion falls to R383 billion after frictions","Illustrative central reconciliation of gross mobilisation")
 labels=["Gross","Not additional","Unallocated / delayed","Failed projects","Net operating"];changes=[506,-38,-27,-58,383];colors=[K,G5,G5,C,C];
 ax.bar(0,506,color=K);running=506
 for i,ch in enumerate(changes[1:-1],1):ax.bar(i,ch,bottom=running if ch>0 else running+ch,color=colors[i]);running+=ch
 ax.bar(4,383,color=C);ax.set_xticks(range(5),[l.replace(" ","\n",1) for l in labels]);ax.set_ylabel("R billion");style_axis(ax,grid_axis="y");
 for i,v in enumerate(changes):ax.text(i,(506 if i==0 else 383 if i==4 else [468,441,383][i-1])+12,f"{v:+.0f}" if i in (1,2,3) else f"R{v}bn",ha="center",fontweight="bold")
 done(fig,"waterfall.png",bottom=.20)

def governance():
 fig,ax=plt.subplots(figsize=(9.4,5.1));head(fig,"Public capital should pass five gates before it takes risk","Each failed gate returns the project for redesign or closure")
 ax.axis("off");names=["ADDITIONALITY\nWhy public money?","PREPARATION\nCan it be built?","COMMERCIALITY\nWho buys?","RISK PRICE\nWho absorbs loss?","DISCLOSURE\nWhat is reported?"]
 for i,n in enumerate(names):
  x=.02+i*.195;ax.add_patch(Rectangle((x,.4),.17,.28,facecolor=C if i in (0,4) else G7,edgecolor="none"));ax.text(x+.085,.54,n,ha="center",va="center",color=W,fontweight="bold",fontsize=9)
  if i<4:ax.annotate("",xy=(x+.19,.54),xytext=(x+.17,.54),arrowprops=dict(arrowstyle="-|>",color=K))
 done(fig,"governance.png",left=.05,right=.99)

for f in (multiples,stacks,scenario,portfolio,risk_return,contingent,crowding,returns,waterfall,governance):f()

gross=sum(PORTFOLIO[k]*PORT_MULT[k] for k in PORTFOLIO)
results={"public_envelope_r_bn":PUBLIC,"instruments":INSTRUMENTS,"portfolio_public_r_bn":PORTFOLIO,"portfolio_multiples":PORT_MULT,"central":{"gross_mobilised_r_bn":gross,"gross_multiple":gross/PUBLIC,"net_operating_after_frictions_r_bn":383,"net_multiple":383/PUBLIC,"guaranteed_exposure_r_bn":75},"notes":["Scenarios are not forecasts or investment advice.","Gross mobilisation is not fiscal saving, public profit or additional investment.","Guarantees are measured by exposure and claims as well as cash reserve.","All amounts are constant 2026 rand."]}
(WORK/"model_results.json").write_text(json.dumps(results,indent=2),encoding="utf-8")
print(json.dumps(results["central"],indent=2));print(f"Wrote {len(list(ASSETS.glob('*.png')))} figures")
