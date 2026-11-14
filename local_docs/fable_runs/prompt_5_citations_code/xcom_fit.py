import re,html,sys,math
import numpy as np
d=sys.argv[1]
def load(z):
    t=open(f'{d}/x{z}.html',errors='ignore').read()
    t=html.unescape(re.sub(r'<[^>]+>',' ',t))
    n=[float(x) for x in re.findall(r'[0-9]\.[0-9]+E[+-][0-9]+',t)]
    return [n[i:i+8] for i in range(0,len(n)-7,8)]
def row(z,E):
    r=[x for x in load(z) if abs(x[0]-E)/E<1e-6]; return r[-1] if r else None
Zs=[6,13,26,29,50,74,82]
A={6:12.011,13:26.98,26:55.845,29:63.546,50:118.71,74:183.84,82:207.2}
pe=[];
for z in Zs:
    r=row(z,0.1); pe.append(r[3]); print(z,'E=0.1: coh %.4g incoh %.4g photo %.4g tot_w %.4g'%(r[1],r[2],r[3],r[6]),'compton frac of total(w coh)=%.3f'%(r[2]/r[6]))
sl=np.polyfit(np.log(Zs),np.log(pe),1)[0]; print('Z exponent per mass, all 7:',sl)
sl2=np.polyfit(np.log(Zs[1:]),np.log(pe[1:]),1)[0]; print('excluding C:',sl2)
# W energy exponent 0.1-0.5 MeV
w=load(74)
def ph(E): return row(74,E)[3]
print('W photo 0.1,0.15,0.2,0.3,0.4,0.5:',[ph(E) for E in (0.1,0.15,0.2,0.3,0.4,0.5)])
Es=[0.1,0.15,0.2,0.3,0.4,0.5]; print('W energy exponent:',np.polyfit(np.log(Es),np.log([ph(E) for E in Es]),1)[0], 'endpoints:',math.log(ph(0.5)/ph(0.1))/math.log(5))
# KN check
re_=2.8179403e-15;NA=6.02214076e23
def skn(E):
    k=E/0.51099895
    return 2*math.pi*re_**2*((1+k)/k**2*(2*(1+k)/(1+2*k)-math.log(1+2*k)/k)+math.log(1+2*k)/(2*k)-(1+3*k)/(1+2*k)**2)
for E in (0.5,1.0):
    s=skn(E); print('KN',E,'sigma b',s/1e-28,'mu/rho C',NA*6/12.011*s*1e4)
    r=row(6,E); print(' table C incoh',r[2],'total w/o coh',r[7])
