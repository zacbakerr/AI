import sys; args = sys.argv[1:]
# import re
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

    r"/\b\w*(\w)\w*\1\w*\b/i",
    r"/\b\w*(\w)(\w*\1\w*){3}\b/i",
    r"/^0[01]*0$|^1[10]*1$|^[01]$|^$/",
    r"/\b(?=\w*cat)\w{6}\b/i",
    r"/\b(?=\w*bri)(?=\w*ing)\w{5,9}\b/i",
    r"/\b(?!\w*cat)\w{6}\b/i",
    r"/\b(\w)(?!\w*\1)\w*\b/",
    r"/^(?!.*10011.*)[01]*$/",
    r"/\b\w*([aeiou])(?!\1)[aeiou]\w*\b/i",
    r"/^(?!.*101)(?!.*111)[10]*$/",

    r"/^(?![01]*010)[01]*$/",
    r"/^(?![01]*010)(?![01]*101)[01]*$/",
    r"/^0[01]*0$|^1[10]*1$|^[01]$|^$/",
    r"/(\b((\w)(?!\w*\3\b))+\b)/i",
    r"/((?=\w*?(\w)\w*\2)(?=\w*(?!\2)(\w)\w*\3)\w*|(?=\w*?(\w)(\w*\4){3})\w*)/i",
    r"/\b((\w)(?!\w*\2))*(\w)((\w)(?!\w*\5))*(\3((\w)(?!\w*\8))*){2}\b/i",
    r"/\b[^aeiou ]*(([aeiou])[^aeiou ]*(?!\w*\2)){5}\b/",
    r"/^(?=^(0*(10*1)?)*$)(?=^1*0(1*01*0)*1*$).*$/",
    r"/^(?=^0?((1(01*0)*1)*0*)*$)(0(1[01]*)*|(1[01]*)+)$/",
    r"/^(?!^0?((1(01*0)*1)*0*)*$)(0(1[01]*)*|(1[01]*)+)$/",

    r"/^(?=.*a)(?=.*e)(?=.*i)(?=.*o)(?=.*u)[a-z]*$/m",
    r"/^([b-df-hj-np-tv-z]*([aeiou])[b-df-hj-np-tv-z]*){5}$/m",
    r"/(?=^[a-vx-z]*?(?!i)([b-df-hj-np-tvx-z])w(?!.[aeiou])[b-df-hj-np-tvx-z])^[a-z]+$/m",
    r"/^(?=([a-z])([a-z])([a-z])?)(?=.*\3\2\1$)[a-z]*$|^([a-z])\4$|^a$/m",
    r"/^(?=[ac-su-z]*(bt|tb)[ac-su-z]*$)\w*$/m",
    r"/^[a-z]*([a-z])\1[a-z]*$/m",
    r"/^[a-z]*([a-z])(?=(([a-z]*\1){5}))[a-z]+$/m",
    r"/^[a-z]*(([a-z])\2){3}[a-z]*$/m",
    r"/(?=(\w*[b-df-hj-np-tv-z]\w*){13})^\w+$/m",
    r"/^(([a-z])(?!\w*\2\w*\2))+$/m",
]

if idx < len(myRegexLst):
  # print(re.findall(myRegexLst[idx], 'Alabama and Mississippi are next to each other.', re.IGNORECASE))
  print(myRegexLst[idx])

# Zachary Baker, Pd. 4, 2024