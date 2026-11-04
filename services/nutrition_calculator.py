class NC:
    ACT = {"sedentary":1.2,"light":1.375,"moderate":1.55,"high":1.725,"very_high":1.9}
    GA = {"lose":-0.20,"maintain":0,"gain":0.15}

    @staticmethod
    def bmr(g,w,h,a):
        return 10*w+6.25*h-5*a+(5 if g=="male" else -161)

    @classmethod
    def tdee(cls,g,w,h,a,act):
        return cls.bmr(g,w,h,a)*cls.ACT.get(act,1.55)

    @classmethod
    def cal(cls,g,w,h,a,act,goal):
        return round(cls.tdee(g,w,h,a,act)*(1+cls.GA.get(goal,0)))

    @classmethod
    def macros(cls,c,w,goal):
        pk={"lose":2.2,"maintain":1.8,"gain":2.0}
        p=round(w*pk.get(goal,1.8))
        f=round(c*(0.25 if goal=="lose" else 0.30)/9)
        cb=round(max((c-p*4-f*9)/4,50))
        return {"calories":c,"protein":p,"fats":f,"carbs":cb}

    @classmethod
    def bmi(cls,w,h):
        b=w/(h/100)**2
        c="Дефицит" if b<18.5 else "Норма" if b<25 else "Избыток" if b<30 else "Ожирение"
        return round(b,1),c

    @classmethod
    def report(cls,g,w,h,a,act,goal):
        c=cls.cal(g,w,h,a,act,goal)
        m=cls.macros(c,w,goal)
        bmi,cat=cls.bmi(w,h)
        return {**m,"bmr":round(cls.bmr(g,w,h,a)),"tdee":round(cls.tdee(g,w,h,a,act)),"bmi":bmi,"bmi_cat":cat}
