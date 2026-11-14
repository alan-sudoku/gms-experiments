import math
NA=6.02214076e23; F=96485.332; e=1.602176634e-19
# N3 Sigma_a (cm^-1), sigma from Sears/INDC (b)
print('Cd',8.65*NA/112.414*2520e-24)
print('B4C',2.52*NA*4/55.255*767e-24)
print('Gd',7.90*NA/157.25*49700e-24)
print('steel1wtB',7.8*0.01/10.811*NA*767e-24)
# water
NH=2*0.998*NA/18.015; print('SigmaH2O',NH*0.3326e-24, NH*0.3326e-24*math.sqrt(math.pi)/2)
# collisions
def xi(A): return 1 if A==1 else 1+((A-1)**2/(2*A))*math.log((A-1)/(A+1))
for A in (1,2,12,56): print('A',A,'xi',xi(A),'collisions',math.log(2e6/0.0253)/xi(A))
print('1/v gain 1MeV',math.sqrt(1e6/0.0253))
# ratios G3.7
print('B10/C',3835/0.0035,'Cd/Al',2520/0.231)
# H1 Li/SOCl2
M=4*6.94+2*(32.06+15.999+2*35.45)
print('Li/SOCl2 Wh/kg',4*F*3.65/(M/1000)/3600)
# SSA graphene
a=0.142e-9; apa=3*math.sqrt(3)/4*a*a
print('SSA m2/g',2*apa*NA/12.011/1000, 'C_sp F/g',21e-6*1e4*2*apa*NA/12.011/1000*1000/1000)
# Ag natural RI from isotopes (INDC)
print('Ag RI nat',0.5184*100+0.4816*1400)
# Gd,Cd isotopic checks Sears
print('natGd',0.148*61100+0.1565*259000,'natCd',0.1222*20600,'natB',0.199*3835)
