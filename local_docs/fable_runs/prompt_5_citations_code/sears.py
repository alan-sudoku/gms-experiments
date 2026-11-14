import re,html,sys
t=open(sys.argv[1],errors='ignore').read()
t=html.unescape(re.sub(r'<[^>]+>','\n',t))
L=[x.strip() for x in t.split('\n') if x.strip()]
i=L.index('Abs xs')+1
want=['H','6Li','Li','10B','B','C','Al','Fe','Ag','113Cd','Cd','In','Sm','Eu','155Gd','157Gd','Gd','Dy','Hf','Cu','Ni','Co','W','Pb','Sn','Ir','Pt']
iso=re.compile(r'^(\d*[A-Z][a-z]?)$')
# find indices of isotope labels followed by conc token
for k in range(i,len(L)):
    if L[k] in want and (L[k+1]=='---' or re.match(r'^[\d.()]+( [a-z])?$',L[k+1])) :
        # abs xs is the token before next label; take next 7 tokens robustly: find the next label
        j=k+1
        while j<len(L) and not (iso.match(L[j]) and (L[j+1]=='---' or re.match(r'^\(?[\d.]+',L[j+1]) ) and re.match(r'^\d*[A-Z][a-z]?$',L[j])): j+=1
        print(L[k],L[k+1:j])
