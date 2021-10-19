def myfunc(x,n):
    if(n<=0):
        return 0
    else:
        return (1/(x^n))+myfunc(x,n-1)
    
x=int(input("Enter value of x : "))
n=int(input("Enter value of n : "))
print(myfunc(x,n))
    
