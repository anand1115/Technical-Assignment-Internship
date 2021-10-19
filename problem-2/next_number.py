def get_number(n):
    if(n&1):
        return (n**2)+1
    else:
        return (n**2)-1
n=int(input("Enter the number :"))
print(get_number(n))
