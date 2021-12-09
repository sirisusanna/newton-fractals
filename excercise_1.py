# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 21:45:06 2021

@author: HP
"""
from  numpy import *
from  matplotlib.pyplot import *

class jacobian:
    
    def __init__(self, func):
        self.func=func

        
    def calculate_jacobian(self, x0, y0):
        J=zeros((2,2))
        f_x0y0=self.func(x0, y0)
        eps=1.e-8
        z = [x0, y0]
        for i in range(2):
            z[i] = z[i]+eps
            J[:, i] = subtract(self.func(z[0], z[1]), f_x0y0)/eps
            z[i] = z[i]-eps
        return J
        

class newton:
    
    def __init__(self, func, dfunc=None):
        self.func=func
        self.zerolist=[]
        if dfunc is None:
            J=jacobian(self.func)
            self.dfunc=J.calculate_jacobian
        else:
            self.dfunc=dfunc
        
    def delta_xy(self, x, y, simplify=False):
        if simplify:
            jacobian_fixed = self.dfunc(x, y)
            return linalg.solve(jacobian_fixed, self.func(x, y))
        else:
            return linalg.solve(self.dfunc(x, y), self.func(x,y))
            
        
    def calculate_newton(self, x1, y1, simplify=False):
        z = array([x1, y1])
        tol = 1.e-8
        counter = 0
        for i in range(100):
            s = z
            z = s-self.delta_xy(s[0], s[1], simplify)
            counter = counter +1
            if allclose(s,z, tol):
                return z, counter         
            elif i==99 and allclose(s,z,tol)==False:
                return None, counter
    
    def findzeroes(self, x, y, simplify=False):
        zerolist=self.zerolist
        zero, counter = self.calculate_newton(x, y, simplify)
        tol=1.e-2
        if isinstance(zero, type(None)):
            return -1
        elif ((not isinstance(zero, type(None))) and zerolist==[]):
            zerolist.append(zero)
            return 0
        else:
            for k in range(len(zerolist)):
                if allclose(zerolist[k], zero, tol):
                    return k
                elif k==len(zerolist)-1 and allclose(zerolist[k], zero, tol)==False:
                    zerolist.append(zero)
                    return len(zerolist)-1


class fractalplot:
    
    def __init__(self, func, dfunc=None):
        self.func=func
        self.dfunc=dfunc

    def fractalplot_show(self, a,b,c,d,N, simplify=False, iterations=False):
        i1=linspace(a,b,N)
        i2=linspace(c,d,N)
        xx,yy=meshgrid(i1,i2)
        A=zeros((N,N))
        Newt=newton(self.func, self.dfunc)
        for k in range(N):
            for i in range(N):
                if iterations:
                    A[k,i]=Newt.calculate_newton(xx[k,i],yy[k,i], simplify)[1]
                else: 
                    A[k,i]=Newt.findzeroes(xx[k,i],yy[k,i], simplify)
        pca=pcolor(A)
        colorbar(pca)
        axis("off")
        
        
        

        
x=linspace(-10, 10)
y=x

def g1(x,y):
    return x**3-3*x*y**2-1, 3*x**2*y-y**3

def g2(x,y):
    return x**3-3*x*y**2-2*x-2, 3*x**2*y-y**3-2*y

def g3(x,y):
    return x**8-28*x**6*y**2+70*x**4*y**4+15*x**4-28*x**2*y**6-90*x**2*y**2+y**8+15*y**4-16, 8*x**7*y-56*x**5*y**3+56*x**3*y**5+60*x**3*y-8*x*y**7-60*x*y**3


def h1(x,y):                                        
    return [[3*x**2-3*y**2, -6*x*y], [6*x*y, 3*x**2-3*y**2]]                

def h2(x,y):
    return [[3*x**2-3*y**2-2, -6*x*y], [6*x*y, 3*x**2-3*y**2-2]]

def h3(x,y):
    return[[8*x**7-168*x**5*y**2+280*x**3*y**4+60*x**3-56*x*y**6-180*x*y**2, -56*x**6*y+280*x**4*y**3-168*x**2*y**5-180*x**2*y+8*y**7+60*y**3], [56*x**6*y-280*x**4*y**3+168*x**2*y**5+180*x**2*y-8*y**7-60*y**3, 8*x**7-168*x**5*y**2+280*x**3*y**4+60*x**3-56*x*y**6-180*x*y**2]]


F=fractalplot(g1, h1)   

F.fractalplot_show(-1,1,-1,1,300, False, True)
