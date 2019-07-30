import numpy as np
import scipy.stats as stats
import scipy.linalg as linalg

class SSA():
    
    def __init__(self, F, L):        
        self.F = F
        self.N = len(F)
        self.L = L
        self.decompose()
        self.reconstruct()

    def ts(self, Xi):
        """
        Усредняем побочные диоганали элементарной матрицы 
        и переводим в временной ряд
        """
        Xrev = Xi[::-1]
        return np.array([Xrev.diagonal(i).mean() for i in range(-Xi.shape[0]+1, Xi.shape[1])])

    def getContributions(self):
        lambdas = np.power(self.s,2)
        norm = np.linalg.norm(self.X)
        cont = [(lambdas[i]/(norm**2)).round(4) for i in range(len(self.s))]
        cont = {i:cont[i] for i in range(len(cont)) if cont[i]>0}
        return cont

    def decompose(self):
        """
        Создание траекторной матрицы и SVD
        """
        self.K = self.N - self.L + 1

        self.X = np.column_stack([self.F[i:i+self.L] for i in range(0,self.K)])
        self.d = np.linalg.matrix_rank(self.X) 
        self.U, self.s, self.V = np.linalg.svd(self.X)
        self.V = self.V.T 

        self.sContributions = self.getContributions()
        self.r = len(self.sContributions)
        self.orthonormalBase = {i:self.U[:,i] for i in range(self.r)}

    def reconstruct(self, comps = np.arange(10)):
        Xs = np.array([self.ts(self.s[i] * \
            np.outer(self.U[:,i], self.V[:,i])) for i in comps])
        self.tsRec = np.zeros(len(Xs[0]))
        for i in range(len(Xs)):
            self.tsRec += Xs[i]
        
    def getFilt(self):
        return self.tsRec
    
    def getTrend(self):
        self.reconstruct([0])
        return self.tsRec

    def getPeriod(self):
        self.reconstruct(np.arange(1,10))
        return self.tsRec
    
    def forecast(self, steps):
        self.verticalityCoeff = 0
        self.R = np.zeros(self.orthonormalBase[0].shape)[:-1]
        for Pi in self.orthonormalBase.values():
            pi = np.ravel(Pi)[-1]
            self.verticalityCoeff += pi**2
            self.R += pi*Pi[:-1]
        self.R = np.matrix(self.R/(1-self.verticalityCoeff))

        self.tsForecast = self.tsRec
        for i in range(self.N + steps):
            if i >= self.N:
                Z = np.array([self.tsForecast[j] for j in range(i-self.L, i-1)])
                x = self.R @ Z
                self.tsForecast = np.append(self.tsForecast, x)
        return self.tsForecast
