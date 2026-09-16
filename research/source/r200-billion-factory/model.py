from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, Rectangle

WORK = Path(__file__).resolve().parent
ASSETS = WORK / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)
STYLE = Path(r"C:\Users\Deriv\Desktop\GreyScienx\skills\greyscienx-editorial-pdf\scripts")
sys.path.insert(0, str(STYLE))
from greyscienx_style import add_figure_header, configure_matplotlib, save_figure, style_axis  # noqa: E402

T = configure_matplotlib(Path(r"C:\Users\Deriv\Desktop\GreyScienx\app\globals.css"))
C, K, W, G1, G3, G5, G7 = T["coral"], T["black"], T["white"], T["grey-100"], T["grey-300"], T["grey-500"], T["grey-700"]

ENVELOPE = 225.0
ALLOCATION = {
    "Production plants": 96,
    "Power + grid": 35,
    "Water + effluent": 14,
    "Rail, port + logistics": 18,
    "Parks + common services": 12,
    "Supplier + working capital": 20,
    "Skills, R&D + testing": 8,
    "Worker access + housing": 7,
    "Contingency": 15,
}
CHAINS = {
    "Manganese materials + batteries": {"capital": 45, "sites": 9, "jobs": 4550, "sales": 42, "power_mw": 380},
    "PGM components + hydrogen systems": {"capital": 29, "sites": 10, "jobs": 2900, "sales": 34, "power_mw": 155},
    "Vanadium + long-duration storage": {"capital": 18, "sites": 10, "jobs": 2700, "sales": 25, "power_mw": 120},
    "Shared machinery + recycling": {"capital": 4, "sites": 5, "jobs": 950, "sales": 7, "power_mw": 45},
}
PHASES = [
    ("Prepare", 0, 2, 18), ("Utilities", 1, 5, 61), ("Wave 1 plants", 2, 6, 45),
    ("Wave 2 plants", 4, 8, 51), ("Deep localisation", 6, 10, 35), ("Reserve", 0, 10, 15)
]

def head(fig, title, subtitle): add_figure_header(fig, title, subtitle, field="GREYSCIENCX / PAPER 8", tokens=T)
def done(fig, name, *, top=.77, bottom=.14, left=.10, right=.97):
    fig.subplots_adjust(top=top, bottom=bottom, left=left, right=right); save_figure(fig, ASSETS/name, dpi=270); plt.close(fig)

def allocation():
    fig, ax = plt.subplots(figsize=(9.4, 5.5)); head(fig, "Most of the factory is not a factory", "Illustrative R225bn programme; constant 2026 rand")
    labels=list(ALLOCATION); vals=list(ALLOCATION.values()); y=np.arange(len(labels)); colors=[C if i<2 else G5 for i in range(len(labels))]
    ax.barh(y, vals, color=colors); ax.set_yticks(y, labels); ax.invert_yaxis(); ax.set_xlabel("Capital allocation (R billion)"); style_axis(ax, grid_axis="x")
    for i,v in enumerate(vals): ax.text(v+.7,i,f"R{v}bn",va="center",fontweight="bold")
    done(fig,"allocation.png",left=.25)

def system_map():
    fig,ax=plt.subplots(figsize=(9.4,5.1)); head(fig,"A programme is a system, not a shopping list","Delivery moves from prepared sites to utilities, plants, suppliers and customers")
    ax.axis("off"); boxes=[(.02,.42,.16,.25,"PREPARE\nland + permits"),(.22,.42,.16,.25,"ENABLE\npower + water"),(.42,.42,.16,.25,"BUILD\n34 plant modules"),(.62,.42,.16,.25,"OPERATE\nskills + inputs"),(.82,.42,.16,.25,"SELL\nofftake + exports")]
    for i,(x,y,w,h,s) in enumerate(boxes):
        ax.add_patch(Rectangle((x,y),w,h,facecolor=C if i in (0,4) else G7,edgecolor="none")); ax.text(x+w/2,y+h/2,s,ha="center",va="center",color=W,fontweight="bold")
        if i<len(boxes)-1: ax.add_patch(FancyArrowPatch((x+w+.01,y+h/2),(boxes[i+1][0]-.01,y+h/2),arrowstyle="-|>",mutation_scale=15,color=K))
    ax.text(.5,.22,"A late grid connection can strand an early factory; an absent customer can strand the entire chain.",ha="center",color=G7)
    done(fig,"system-map.png",left=.06,right=.98)

def chain_portfolio():
    fig,ax=plt.subplots(figsize=(9.4,5.4)); head(fig,"The production core contains 34 plant modules","Capital, direct operating jobs and annual sales are independent scenario estimates")
    names=[n.replace(" + "," +\n") for n in CHAINS]; cap=[x["capital"] for x in CHAINS.values()]; jobs=[x["jobs"] for x in CHAINS.values()]
    x=np.arange(len(names)); ax.bar(x,cap,color=[C,G7,G5,K]); ax.set_xticks(x,names); ax.set_ylabel("Production capital (R billion)"); style_axis(ax,grid_axis="y")
    for i,(v,j) in enumerate(zip(cap,jobs)): ax.text(i,v+1,f"R{v}bn\n{j:,} jobs",ha="center",fontweight="bold")
    done(fig,"chain-portfolio.png",bottom=.22)

def timeline():
    fig,ax=plt.subplots(figsize=(9.4,5.2)); head(fig,"R225 billion takes a decade to become an operating system","Illustrative spend waves; reserve is released only through stage gates")
    y=np.arange(len(PHASES));
    for i,(name,start,end,value) in enumerate(PHASES): ax.barh(i,end-start,left=start,color=C if i in (0,2,4) else G5,height=.58); ax.text(start+.12,i,f"R{value}bn",va="center",color=W,fontweight="bold")
    ax.set_yticks(y,[p[0] for p in PHASES]); ax.invert_yaxis(); ax.set_xlabel("Programme year"); ax.set_xticks(range(0,11)); style_axis(ax,grid_axis="x"); done(fig,"timeline.png",left=.18)

def jobs():
    fig,ax=plt.subplots(figsize=(9.4,5.3)); head(fig,"Construction is the employment peak; operation is the test","Direct jobs only; supplier and induced employment shown separately")
    years=np.arange(0,11); construction=np.array([4000,13000,26000,36000,40000,33000,23000,14000,7000,2500,500]); operating=np.array([0,300,1200,3000,5700,8200,10000,10700,11000,11100,11100]); supplier=np.round(operating*.9)
    ax.plot(years,construction,color=C,marker="o",label="Construction"); ax.plot(years,operating,color=K,linestyle="--",marker="s",label="Direct operation"); ax.plot(years,supplier,color=G5,linestyle=":",marker="D",label="Supplier estimate")
    ax.set_xlabel("Programme year"); ax.set_ylabel("Jobs"); ax.legend(frameon=False,ncol=3); style_axis(ax); done(fig,"jobs.png")

def utilities():
    fig,ax=plt.subplots(figsize=(9.4,5.2)); head(fig,"Utilities must arrive before production ramps","Illustrative connected demand from the production core")
    names=[n.split(" + ")[0] for n in CHAINS]; p=[v["power_mw"] for v in CHAINS.values()]; water=[7.5,2.2,1.5,.8]
    x=np.arange(4); ax.bar(x,p,color=C); ax.set_xticks(x,names); ax.set_ylabel("Reliable power demand (MW)"); style_axis(ax,grid_axis="y")
    ax2=ax.twinx(); ax2.plot(x,water,color=K,linestyle="--",marker="s"); ax2.set_ylabel("Industrial water (million m³/year)")
    done(fig,"utilities.png",bottom=.20)

def utilisation():
    fig,ax=plt.subplots(figsize=(9.4,5.3)); head(fig,"A half-used plant can destroy an apparently good plan","Stylised annual local value from R96bn production capital")
    util=np.array([40,55,70,85,95]); gross=101*util/85; fixed=23; local=np.maximum(0,gross*.42-fixed)
    ax.plot(util,local,color=C,marker="o",linewidth=2.5); ax.axhline(0,color=K,linewidth=1); ax.axvline(70,color=G5,linestyle="--"); ax.text(71,2,"minimum portfolio gate",color=G7)
    ax.set_xlabel("Average capacity utilisation (%)"); ax.set_ylabel("Annual local value after fixed operating burden (Rbn)"); style_axis(ax); done(fig,"utilisation.png")

def overrun():
    fig,ax=plt.subplots(figsize=(9.4,5.3)); head(fig,"The reserve absorbs delay; it cannot rescue a broken portfolio","Delivered scope under construction-cost and delay scenarios")
    scenarios=["On plan","10% overrun","20% overrun","20% + 2y delay","35% + 3y delay"]; delivered=[100,94,86,78,64]; reserve=[15,5,0,0,0]
    x=np.arange(len(scenarios)); ax.bar(x,delivered,color=[C,C,G5,G7,K]); ax.set_xticks(x,[s.replace(" ","\n",1) for s in scenarios]); ax.set_ylabel("Share of planned productive capacity delivered (%)"); style_axis(ax,grid_axis="y")
    for i,v in enumerate(delivered): ax.text(i,v+2,f"{v}%",ha="center",fontweight="bold")
    done(fig,"overrun.png",bottom=.21)

def geography():
    fig,ax=plt.subplots(figsize=(9.4,5.2)); head(fig,"Five nodes are more credible than one national megasite","Schematic allocation based on resources, skills, logistics and customers")
    ax.axis("off"); nodes=[(.08,.66,"NORTHERN CAPE","Mn materials\nrail + renewables",45),(.38,.69,"GAUTENG","components\nR&D + finance",52),(.68,.66,"LIMPOPO / NW","PGM systems\nmining customers",43),(.25,.38,"GQEBERHA / COEGA","battery exports\nchemicals + port",48),(.62,.37,"EAST LONDON / DURBAN","VRFB + assembly\nports + auto",37)]
    for x,y,title,sub,val in nodes:
        size=.10+val/1000; ax.scatter([x],[y],s=val*35,color=C if val>=48 else G7,alpha=.95); ax.text(x,y-.12,f"{title}\n{sub}\nR{val}bn",ha="center",va="top",fontweight="bold" if val>=48 else "normal")
    done(fig,"geography.png",left=.05,right=.99)

def outcomes():
    fig,ax=plt.subplots(figsize=(9.4,5.3)); head(fig,"The same budget can produce very different industrial estates","Illustrative programme outcomes after ten years")
    s=["Adverse","Central","High execution"]; operating=[55,86,100]; jobs=[65,111,145]; exports=[24,58,82]
    x=np.arange(3); w=.24; ax.bar(x-w,operating,w,label="Capacity operating (%)",color=G5); ax.bar(x,jobs, w, label="Direct jobs (hundreds)",color=C); ax.bar(x+w,exports,w,label="Annual exports (Rbn)",color=K)
    ax.set_xticks(x,s); ax.set_ylabel("Indexed / stated units"); ax.legend(frameon=False,ncol=3); style_axis(ax,grid_axis="y"); done(fig,"outcomes.png")

for f in (allocation,system_map,chain_portfolio,timeline,jobs,utilities,utilisation,overrun,geography,outcomes): f()

results={"envelope_r_bn":ENVELOPE,"allocation_r_bn":ALLOCATION,"production_chains":CHAINS,"phases":PHASES,"central":{"plant_modules":34,"direct_operating_jobs":11100,"supplier_jobs_estimate":9990,"annual_sales_r_bn":108,"reliable_power_mw":700,"water_million_m3_y":12,"build_years":10},"notes":["Scenario, not forecast or feasibility study.","Plant modules inherit stylised assumptions from GreyScienx Papers 5-7.","Jobs are direct unless labelled supplier estimate.","All amounts are constant 2026 rand."]}
(WORK/"model_results.json").write_text(json.dumps(results,indent=2),encoding="utf-8")
print(json.dumps(results["central"],indent=2)); print(f"Wrote {len(list(ASSETS.glob('*.png')))} figures")
