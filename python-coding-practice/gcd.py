#!/usr/local/bin/python3

def gcd(u, v):
    t = v
    if u < v:
        t = u
    while u % t != 0 or v % t != 0:
        t = t - 1
    return t

def gcd_euclid_recur(u,v):
    if v == 0:
        return u
    else:
        return gcd_euclid_recur(v, u % v)

def gcd_euclid(u,v):
    while v != 0:
        t = u % v
        u = v
        v = t
    return u

def gcdOfThree(u,v,w):
    return gcd_euclid(w, gcd_euclid(u,v))

def unit_tests():
    for uv in [[10, 2, 2], [9, 3, 3], [100, 60, 20], [3, 50, 1]]:
        assert gcd(uv[0],uv[1]) == uv[2]
        assert gcd_euclid_recur(uv[0], uv[1]) == gcd(uv[0],uv[1])
        assert gcd_euclid(uv[0], uv[1]) == gcd_euclid_recur(uv[0],uv[1])
    return "unit_tests pass"

    for uvw in [[10, 20, 5, 5], [9, 18, 27, 9], [100, 60, 10, 10], [5, 3, 50, 1]]:
        assert gcdOfThree(uvw[0],uvw[1],uvw[2]) == uvw[3]

print(unit_tests())
