def myfunc(x,n):
    sum=0.0
    for i in range(1,n+1):
        sum=sum+(1/(x**i))
    return sum
x=int(input("Enter value of x : "))
n=int(input("Enter value of n : "))
print(myfunc(x,n))
    
