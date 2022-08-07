a=[2,3,4,5,6,7,1]
s=set(a)
print(s)
counts =[]
r=4
def count(a,s):
    r=6
    for el in s:
        count=0
        for item in a:
            
            if item == el :
                count = count +1
        counts.append(count)
    return(counts)


print(count(a,s))

print(s,r,counts)