
N=2000000
f=open("Status.txt")
f1=open('input2.txt','a+')
for i in range(N):
    line=next(f).strip()
    f1.write(line)
    f1.write("\n")
    print(i)
f.close()
f1.close()


