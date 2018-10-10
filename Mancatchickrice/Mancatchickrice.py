class Mancatchickrice():
    # man=0
    # cat=1
    # chick=2
    # rice=3
    step=0
    maxstep=10
    here=[0,1,1,1]
    there=[1,0,0,0]
    action=[]
    slove=[]
    def go(self,l):
        if(Mancatchickrice.step>Mancatchickrice.step):
            return
        for i in range(4):
            if Mancatchickrice.here[i] and i!=l:
                Mancatchickrice.action.append(i)
                Mancatchickrice.step+=1
                Mancatchickrice.here[i]=0
                Mancatchickrice.there[i]=1
                if Mancatchickrice.there[1] and Mancatchickrice.there[2] and Mancatchickrice.there[3]:
                    Mancatchickrice.slove.append(Mancatchickrice.action)
                    self.printresult()
                if (Mancatchickrice.here[1] and Mancatchickrice.here[2])==0 and(Mancatchickrice.here[2] and Mancatchickrice.here[3])==0:
                    self.back(i)
                Mancatchickrice.there[i]=0
                Mancatchickrice.here[i]=1
                Mancatchickrice.step-=1
                Mancatchickrice.action.pop()
    def back(self,l):
        if Mancatchickrice.step>Mancatchickrice.maxstep:
            return
        for i in range(4):
            if Mancatchickrice.there[i] and i!=l:
                Mancatchickrice.action.append(i)
                Mancatchickrice.step+=1
                if i!=0:
                    Mancatchickrice.there[i]=0
                    Mancatchickrice.here[i]=1
                if (Mancatchickrice.there[1] and Mancatchickrice.there[2])==0 and (Mancatchickrice.there[2] and Mancatchickrice.there[3])==0:
                    self.go(i)
                Mancatchickrice.there[i]=1
                Mancatchickrice.here[i]=0
                Mancatchickrice.step-=1
                Mancatchickrice.action.pop()
    def printresult(self):

        for i in range(len(self.action)):
            if i%2==1:
                print("back:")
            else:
                print("go:")
            if Mancatchickrice.action[i]==0:
                print("人")
            elif Mancatchickrice.action[i]==1:
                print("人和猫")
            elif Mancatchickrice.action[i]==2:
                print("人和鸡")
            else:
                print("人和米")
        print('*'*20)
if __name__ == '__main__':
    m=Mancatchickrice()
    m.go(0)