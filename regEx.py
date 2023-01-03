import sys; args = sys.argv[1:]
idx = int(args[0])-30

myRegexLst = [
    r"/^0$|^100$|^101$/",
    r"/^[01]*$/",
    r"/0$/",
    r"/[^- \n.,]*[aeiou][^- \n.,]*[aeiou][^- \n.,]*/i",
    r"/^1[01]*0$|^0$/",
    r"/^[01]*110[01]*$/",
    r"/^.{2,4}$/s",
    r"/^\d{3}\s*-?\s*\d{2}\s*-?\s*\d{4}$/",
    r"/^.*\S*d\S*\b/imu",
    r"/^0[01]*0$|^1[10]*1$|^[01]$|^$/",

    r"/^[x\.o]{64}$/i",
    r"/^[xo]*\.[xo]*$/i",
    r"/^(x+o*)?\.|\.(o*x+)?$/i",
    r"/^.(..)*$/si",
    r"/^(0|1[01])([01]{2})*$/",
    r"/\w*([aei][ou]|[ou][aei]|ae|ea|ai|ia|ou|uo|ei|ie)\w*/i",
    r"/^(0|11*$|10)*$/",
    r"/^[bc]+$|^[bc]*a[bc]*$/",
    r"/^(([bc]*a){2}[bc]*)+$|^[bc]+$/",
    r"/^((2|1[02]*1)[02]*)+$/",
]
if idx < len(myRegexLst):
  print(myRegexLst[idx])

# Zachary Baker, Pd. 4, 2024