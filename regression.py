#!/usr/bin/env python
"""
Amaral Group
Northwestern University

regression functions

"""

def linreg(X, Y):
    from math import sqrt
    if len(X) != len(Y): raise ValueError, 'unequal length'
    N = len(X)
    Sx = Sy = Sxx = Syy = Sxy = 0.0
    for x, y in map(None, X, Y):
        Sx = Sx + x
        Sy = Sy + y
        Sxx = Sxx + x*x
        Syy = Syy + y*y
        Sxy = Sxy + x*y
    det = Sxx * N - Sx * Sx
    slope, intercept = (Sxy * N - Sy * Sx)/det, (Sxx * Sy - Sx * Sxy)/det
    
    reg=[]
    for i in range(len(X)):
        reg.append([X[i],(slope*X[i])+intercept])

    top=N*Sxy-Sy*Sx
    bottom=sqrt(N*Sxx-(Sx*Sx))*sqrt(N*Syy-(Sy*Sy))
    R=top/bottom
    
    return slope, intercept, R, reg

def expreg(X, Y):
    from math import exp,log
    if len(X) != len(Y): raise ValueError, 'unequal length'
    N = len(X)
    y2=[]
    for i in range(len(Y)):
        y2.append(log(Y[i]))

    Sx = Sy = Sxx = Syy = Sxy = 0.0
    for x, y in map(None, X, y2):
        Sx = Sx + x
        Sy = Sy + y
        Sxx = Sxx + x*x
        Syy = Syy + y*y
        Sxy = Sxy + x*y
    det = Sxx * N - Sx * Sx
    slope, intercept = (Sxy * N - Sy * Sx)/det, (Sxx * Sy - Sx * Sxy)/det
    
    reg=[]
    for i in range(len(X)):
        reg.append([X[i],exp((slope*X[i])+intercept)])
    
    top=N*Sxy-Sy*Sx
    bottom=sqrt(N*Sxx-(Sx*Sx))*sqrt(N*Syy-(Sy*Sy))
    R=top/bottom
    
    return slope, intercept, R, reg

def pwrreg(X, Y):
    from math import exp,log,sqrt
    if len(X) != len(Y): raise ValueError, 'unequal length'
    N = len(X)
    x2=[]
    y2=[]
    for i in range(len(Y)):
        x2.append(log(X[i]))
        y2.append(log(Y[i]))

    Sx = Sy = Sxx = Syy = Sxy = 0.0
    for x, y in map(None, x2, y2):
        Sx = Sx + x
        Sy = Sy + y
        Sxx = Sxx + x*x
        Syy = Syy + y*y
        Sxy = Sxy + x*y
    det = Sxx * N - Sx * Sx
    slope, intercept = (Sxy * N - Sy * Sx)/det, (Sxx * Sy - Sx * Sxy)/det
    
    reg=[]
    for i in range(len(X)):
        reg.append([X[i],exp((slope*x2[i])+intercept)])
    
    top=N*Sxy-Sy*Sx
    bottom=sqrt(N*Sxx-(Sx*Sx))*sqrt(N*Syy-(Sy*Sy))
    R=top/bottom
    
    return slope, intercept, R, reg
