import ctypes
import os

#import search.so
libPath = os.path.abspath("helper/search.so")
_lib = ctypes.CDLL(libPath)

_lib.arrDist.argtypes = [
    ctypes.POINTER(ctypes.c_double),
    ctypes.POINTER(ctypes.c_double),
    ctypes.c_int,
    ctypes.c_int,
]
_lib.arrDist.restype = ctypes.c_double

_lib.getClosestNeighbors.argtypes = [
    ctypes.POINTER(ctypes.c_double),
    ctypes.POINTER(ctypes.POINTER(ctypes.c_double)),
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_int),
]
_lib.getClosestNeighbors.restype = ctypes.POINTER(ctypes.c_int)

_lib.free.argtypes = [ctypes.c_void_p]
_lib.free.restype = None


def findClosestNeighbors(searchVector, dataset, threshold=5):
    datS = len(dataset)
    lenD = len(searchVector)

    cSearch = (ctypes.c_double * lenD)(*searchVector)

    cPointerArrayType = ctypes.POINTER(ctypes.c_double) * datS
    cDataset = cPointerArrayType()

    rowObjects = []
    for i, row in enumerate(dataset):
        cRow = (ctypes.c_double * lenD)(*row)
        rowObjects.append(cRow)
        cDataset[i] = ctypes.cast(cRow, ctypes.POINTER(ctypes.c_double))

    cOutCount = ctypes.c_int(0)

    cResultsPtr = _lib.getClosestNeighbors(
        cSearch,
        cDataset,
        threshold,
        lenD,
        datS,
        ctypes.byref(cOutCount),
    )

    if not cResultsPtr:
        return []

    count = cOutCount.value
    indices = [cResultsPtr[i] for i in range(count)]

    _lib.free(cResultsPtr)

    return indices