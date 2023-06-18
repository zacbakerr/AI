## Regex 4

### Recognize all base 3 (non-negative) strings that are even

Given n,
- n even => 3n even
- n odd => 3n odd

There exists two states
- Z(even)
    - Adding a 0|2 keeps it even
    - Adding a 1 makes it odd
    - 1(0|2)*1 keeps it even
- W(odd)
    - Adding a 0|2 keeps it odd
    - Adding a 1 makes it even

/^(0|2|1(0|2)*1)+$/
State diagram

MyRegexLst = [
    r"/(?!.*')(?=.*a)(?=.*e)(?=.*i)(?=.*o)(?=.*u)\b[a-z]+\b/",
    r"/(?!.*')\b([qwrtypsdfghjklzxcvbnm]*[aeiou][qwrtypsdfghjklzxcvbnm]*){5}\b/",
    r"/(?=^[qrtypsdfghjklzxcvbnmaeuo]*?(?!i)([qrtypsdfghjklzxcvbnm])w(?!.[aeiou])[qrtypsdfghjklzxcvbnm])^[a-z]+$/m",
    r"/^(?=([a-z])([a-z])([a-z])?)(?=.*\3\2\1$)[a-z]*$|^([a-z])\4$|^a$/m",
    r"/(?=.*(bt|tb))^[qweryuiopasdfghjklzxcvnm]*?\1[qweryuiopasdfghjklzxcvnm]*$/m",
    r"/(?!.*')^[a-z]*([a-z])\1[a-z]*$/m",
    r"/^[a-z]*([a-z])(?=((.*\1){5,}))[a-z]+$/m",
    r"/(?=[a-z]*(([a-z])\2){3})^[a-z]+$/m",
    r"/(?=(.*[qwrtypsdfghjklzxcvbnm].*){13})^[a-z]+$/m",
    r"/^(?!.*')(([a-z])(?![a-z]*\2[a-z]*\2))+$/m",
]