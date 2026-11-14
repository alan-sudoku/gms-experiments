import json,sys,urllib.parse,urllib.request,time
Q={3:"Klein Nishina Über die Streuung von Strahlung durch freie Elektronen nach der neuen relativistischen Quantendynamik von Dirac",
7:"Jensen Sur les fonctions convexes et les inégalités entre les valeurs moyennes Acta Mathematica",
11:"ENDF/B-VIII.0 the 8th major release of the nuclear reaction data library with CIELO-project cross sections",
12:"Japanese evaluated nuclear data library version 5 JENDL-5",
15:"Dowell Effects of eddy currents in transformer windings",
16:"Thomson On the economy of metal in conductors of electricity",
20:"Schmidt Die Wärmeübertragung durch Rippen",
23:"Murray The physiological principle of minimum work I vascular system cost of blood volume",
24:"Hashin Shtrikman A variational approach to the theory of the effective magnetic permeability of multiphase materials",
25:"Newman Tobias Theoretical analysis of current distribution in porous electrodes",
26:"de Levie On porous electrodes in electrolyte solutions",
27:"Trasatti Work function, electronegativity, and electrochemical behaviour of metals III Electrolytic hydrogen evolution in acid solutions",
28:"Sheng Gasteiger Shao-Horn Hydrogen oxidation and evolution reaction kinetics on platinum acid vs alkaline electrolytes",
29:"McCrory Jung Peters Jaramillo Benchmarking heterogeneous electrocatalysts for the oxygen evolution reaction",
30:"Gilliam Graydon Kirk Thorpe A review of specific conductivities of potassium hydroxide solutions for various concentrations and temperatures",
35:"Coey Hard magnetic materials: a perspective",
37:"Skomski Coey Magnetic anisotropy how much is enough for a permanent magnet",
38:"Skomski Coey Giant energy product in nanostructured two-phase magnets",
39:"Kneller Hawig The exchange-spring magnet: a new material principle for permanent magnets",
40:"Stoner Wohlfarth A mechanism of magnetic hysteresis in heterogeneous alloys",
41:"Skomski Liu Shield Hadjipanayis Sellmyer Permanent magnetism of dense-packed nanostructures",
42:"Xia Chen Li Tao Measurement of the quantum capacitance of graphene",
44:"Christen Carlen Theory of Ragone plots",
45:"Augustyn Simon Dunn Pseudocapacitive oxide materials for high-rate electrochemical energy storage",
46:"Haacke New figure of merit for transparent conductors",
47:"Ellmer Past achievements and future challenges in the development of optically transparent electrodes",
32:"Nuss Eckelman Life cycle assessment of metals: a scientific synthesis",
10:"Sears Neutron scattering lengths and cross sections Neutron News",
}
for k,q in Q.items():
    u="https://api.crossref.org/works?rows=2&select=title,author,container-title,volume,issue,page,issued,DOI,type&query.bibliographic="+urllib.parse.quote(q)
    try:
        d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'citecheck/1.0 (mailto:none@example.com)'}),timeout=30))
        for it in d['message']['items'][:2]:
            au=', '.join((a.get('family','?')) for a in it.get('author',[])[:5])
            print(k,'|',it.get('title',['?'])[0][:90],'|',au,'|',(it.get('container-title') or ['?'])[0],it.get('volume'),it.get('issue'),it.get('page'),it['issued']['date-parts'][0][0],it['DOI'])
    except Exception as e: print(k,'ERR',e)
    print('--'); time.sleep(0.3)
