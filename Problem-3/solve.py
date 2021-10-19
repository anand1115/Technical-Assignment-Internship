x,y,a,b=int(input()),int(input()),int(input()),int(input())
neumerator=((x+(1/y))**a)*((x-(1/y))**b)
denominator=((y+(1/x))**a)*((y-(1/x))**b)
print(neumerator/denominator)
