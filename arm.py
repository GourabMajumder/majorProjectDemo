def armstrong(n):
    s = 0
    order = len(str(n))
    copy_n = n
    while(n>0):
        digit = n%10
        s += digit **order
        n = n//10
    
    if(s == copy_n):
        print(f"{copy_n} is armstrong number")
        result = {
            "Number" : copy_n,
            "Armstrong" : True,
            "Server IP" : "123.154.1234.00"
        }
    else:
        print(f"{copy_n} is not armstrong number")
        result = {
            "Number" : copy_n,
            "Armstrong" : False,
            "Server IP" : "123.154.1234.00"
        }
    