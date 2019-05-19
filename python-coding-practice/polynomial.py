#!/usr/local/bin/python3

def poly_add_simple(a, b):
    # "an array represent a0*(x**0) + a1*(x**1) + a2*(x**2) + ..."
    r = [i for i in a]
    for i in range(len(r)):
        r[i] = r[i] + b[i]
    return r

def poly_mul_simple(a, b):
    # "an array represent a0*(x**0) + a1*(x**1) + a2*(x**2) + ..."
    r = [0 for i in range(2*len(a)-1)]
    for i in range(len(a)):
        for j in range(len(b)):
            r[i+j] = r[i+j] + a[i]*b[j]
    return r

class polynomial:
    # "calculate polynomial in case there are huge sparseness between the power of X"
    def __init__(self, arr, isSorted=False):
        # "[ arr is [powerOfX, value], ... ]"
        self._arr = arr
        self._isSorted = isSorted

    def __str__(self):
        return str(self._arr)

    def __eq__(self, another):
        self._sort()
        another._sort()
        return self.__dict__ == another.__dict__

    def _sort(self):
        # "Not thread-safe"
        if not self._isSorted:
            self._arr.sort();
            self._isSorted = True

    def add(self, another):
        def append(r, a, ai):
            for i in range(ai,len(a)):
                r.append(a[i])
            return r
        def merge(r, a, b, ai, bi):
            if ai == len(a):
                return append(r, b, bi)
            if bi == len(b):
                return append(r, a, ai) 
            if a[ai][0] == b[bi][0]:
                r.append([a[ai][0], a[ai][1] + b[bi][1]])
                return merge(r, a, b, ai+1, bi+1)
            if a[ai] < b[bi]:
                r.append(a[ai])
                return merge(r, a, b, ai+1, bi)
            " a[ai] > b[bi]"
            r.append(b[ai])
            return merge(r, a, b, ai, bi+1)

        self._sort()
        another._sort()
        return polynomial(merge([], self._arr, another._arr, 0, 0), True)

    def mul(self, another):
        def ceil(lst, item):
            """
            #sequential search
            for i in range(len(lst)):
                if lst[i][0] >= item[0]:
                    return i
            return len(lst)
            """
            def bsearch(lst, item, start, end):
                if end == start:
                    return len(lst)
                mid = start+int((end-start)/2)
                if lst[mid][0] == item[0]:
                    return mid
                if lst[mid][0] < item[0]:
                    return bsearch(lst,item, mid, end)
                if mid > 0 and lst[mid-1][0] < item[0]:
                    return mid
                if mid == 0:
                    return 0
                return bsearch(lst,item,start,mid)
            if len(lst) == 0 or lst[len(lst)-1][0] < item[0]:
                return len(lst)
            return bsearch(lst, item, 0, len(lst))
        def add(lst, item):
            index = ceil(lst, item)
            if index < len(lst) and lst[index][0] == item[0]:
                lst[index][1] = lst[index][1] + item[1]
                if lst[index][1] == 0:
                    lst.pop(index)
            else:
                lst.insert(index, item)
            return lst
        self._sort()
        another._sort()
        result = []
        for i in self._arr:
            for j in another._arr:
                add(result, [i[0]+j[0], i[1]*j[1]])
        return polynomial(result, True)

def unit_tests():
    for test in [[[1, 2, 3], [3, 4, 5], [4, 6, 8]]]:
        assert test[2] == poly_add_simple(test[0], test[1])
    for test in [ [[ 1, 1], [ 1, 1], [ 1, 2, 1]],
                  [[-1, 1], [-1, 1], [ 1,-2, 1]] ]:
        assert test[2] == poly_mul_simple(test[0], test[1])
    for test in [ [[[1,2],[0,1],[2,3]], [[0,3],[1,4],[2,5]], [[0,4],[1,6],[2,8]]] ]:
        expected = polynomial(test[2])
        result = polynomial(test[0]).add(polynomial(test[1]))
        assert expected == result
    for test in [ [[[0, 1], [1,1]]       , [[0, 1], [1, 1]]       , [[0, 1], [1, 2], [2, 1]]],
                  [[[0,-1], [1,1]]       , [[0,-1], [1, 1]]       , [[0, 1], [1,-2], [2, 1]]],
                  [[[0,-1], [1,1]]       , [[0, 1], [1, 1]]       , [[0,-1],         [2, 1]]],
                  [[[0, 1], [1,2], [2,1]], [[0, 1], [1,-2], [2,1]], [[0, 1], [2,-2], [4, 1]]] ]:
        expected = polynomial(test[2])
        result = polynomial(test[0]).mul(polynomial(test[1]))
        assert expected == result
    return "unit tests pass"

print(unit_tests())
