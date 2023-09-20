import machine
s = machine.unique_id()
for b in s:
    print(hex(b)[2:],end=" ")
print()   