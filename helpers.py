import arabic_reshaper
from bidi.algorithm import get_display

def a(txt):
    try:
        x = arabic_reshaper.reshape(txt)
        return get_display(x)
    except:
        return txt

def check_vals(v1, v2, v3, v4):
    try:
        f1 = float(v1)
        f2 = float(v2)
        f3 = float(v3)
        i4 = int(v4)
        if i4 <= 0 or f1 < 0:
            return None
        return (f1, f2, f3, i4)
    except:
        return None
