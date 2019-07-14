class Parser():

    def read(self, fileName):
        
        self.year = []
        self.month = []
        self.day = []
        self.MJD = []

        self.IERSpolar = []
        self.IERSutc = []

        self.aPMx = []
        self.aPMy = []
        self.aUTC = []

        self.bPMx = []
        self.bPMy = []
        self.bUTC = []

        fileLen = 0
        f = open(fileName, "r")
        for line in f:   
            # Считать mjd
            mjd = float(line[7:15].replace(" ", ""))
            self.MJD.append(mjd)
            
            # Год, месяц, день
            yr =  line[0:2].replace(" ", "")
            if len(yr) == 1:
                yr = "0" + yr
            if mjd < 51544.0:
                self.year.append(int("19" + yr))
            else:
                self.year.append(int("20" + yr))        
            self.month.append(int(line[2:4].replace(" ", "")))    
            self.day.append(int(line[4:6].replace(" ", "")))
            
            self.IERSpolar = line[17].replace(" ", "")
            self.IERSutc.append(line[57].replace(" ", ""))    
            
            # A: X, Y, UTC 
            x = line[18:27].replace(" ", "")
            try:
                if x[0] == "-":
                    self.aPMx.append(float("-"+"0"+x[1:]))
                else:
                    self.aPMx.append(float("0"+x))    
            except:
                self.aPMx.append(self.aPMx[-1]) 
                        
            y = line[37:46].replace(" ", "")
            try:
                if y[0] == "-":
                    self.aPMy.append(float("-"+"0"+y[1:]))
                else:
                    self.aPMy.append(float("0"+y))     
            except:
                self.aPMy.append(self.aPMy[-1])                              
            
            u = line[58:68].replace(" ", "")
            try:
                if u[0] == "-":
                    if u[1] == "0":
                        self.aUTC.append(float(u))
                    else:            
                        self.aUTC.append(float("-"+"0"+y[1:]))
                else:
                    if u[0] == "0":
                        self.aUTC.append(float(u))
                    else:
                        self.aUTC.append(float("0"+u))    
            except:
                self.aUTC.append(self.aUTC[-1])    
                    
                    
            # B: X, Y, UTC 
            x = line[134:144].replace(" ", "")
            try:
                if x[0] == "-":
                    self.bPMx.append(float("-"+"0"+x[1:]))
                else:
                    self.bPMx.append(float("0"+x))    
            except:
                self.bPMx.append(self.bPMx[-1]) 
                        
            y = line[144:154].replace(" ", "")
            try:
                if y[0] == "-":
                    self.bPMy.append(float("-"+"0"+y[1:]))
                else:
                    self.bPMy.append(float("0"+y))     
            except:
                self.bPMy.append(self.bPMy[-1])                  
            
            u = line[154:165].replace(" ", "")
            try:
                if u[0] == "-":
                    if u[1] == "0":
                        self.bUTC.append(float(u))
                    else:            
                        self.bUTC.append(float("-"+"0"+y[1:]))
                else:
                    if u[0] == "0":
                        self.bUTC.append(float(u))
                    else:
                        self.bUTC.append(float("0"+u))    
            except:
                self.bUTC.append(self.bUTC[-1])     
            fileLen += 1
        return fileLen 
    
    def getData(self, name):
        """
        Получить необходимые данные
        Возвращает соответствующие данные
        """
        if name == "X (A)":
            return self.aPMx 
        if name == "X (B)":
            return self.bPMx 
            
        if name == "Y (A)":
            return self.aPMy 
        if name == "Y (B)":
            return self.bPMy 

        if name == "UTC-UT1 (A)":
            return self.aUTC 
        if name == "UTC-UT1 (B)":
            return self.bUTC 