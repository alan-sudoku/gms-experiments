import re,html,sys,glob,os
d=sys.argv[1]
def load(z):
    t=open(f'{d}/z{z}.html',errors='ignore').read()
    t=html.unescape(re.sub(r'<[^>]+>',' ',t))
    rows=[];toks=t.split()
    i=0
    # numbers sequence: energy, mu/rho, muen/rho ; edge labels precede
    nums=[x for x in toks if re.fullmatch(r'[0-9.]+E[+-][0-9]+',x)]
    for j in range(0,len(nums)-2,3):
        rows.append(tuple(float(x) for x in nums[j:j+3]))
    return rows
def at(rows,E):
    r=[x for x in rows if abs(x[0]-E)/E<1e-9]
    if r: return r[-1][1]
    import math
    lo=max([x for x in rows if x[0]<E],key=lambda x:x[0]);hi=min([x for x in rows if x[0]>E],key=lambda x:x[0])
    f=(math.log(E)-math.log(lo[0]))/(math.log(hi[0])-math.log(lo[0]))
    return math.exp(math.log(lo[1])+f*(math.log(hi[1])-math.log(lo[1])))
if __name__=='__main__':
    Z={'C':'06','Al':'13','Fe':'26','Cu':'29','Sn':'50','Gd':'64','W':'74','Pb':'82','Bi':'83','Ba':'56'}
    D={k:load(z) for k,z in Z.items()}
    for E in (0.04,0.06,0.08,0.1,0.5,1,5,10):
        print(E,{k:round(at(v,E),5) for k,v in D.items()})
    for E in (0.1,0.5,1.0,5.0): print('W/C',E,at(D['W'],E)/at(D['C'],E))
    import numpy as np
    g=np.logspace(np.log10(0.03),np.log10(20),4000)
    r=np.array([at(D['W'],e)/at(D['C'],e) for e in g])
    print('min',r.min(),g[r.argmin()]); lt=g[r<2]; print('<2 range',lt.min(),lt.max())
    print('W/C at10',at(D['W'],10)/at(D['C'],10))
    for rc in (1.70,2.26):
        t=np.array([at(D['W'],e)*19.3/(at(D['C'],e)*rc) for e in g]); print('thick min',rc,t.min(),g[t.argmin()])
