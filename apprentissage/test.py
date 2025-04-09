fruits = ["pomme", "banane", "cerise"]

for f in fruits:
    print(f.upper())

if fruits.count("poire"):
    print("trouvé (if)")
elif fruits.count("cerise"):
    print("trouvé (elif)")
else:
    print("pas trouvé (else)")

fruits.reverse()
print(fruits)

print(len(fruits))

fruits.append("poire")

if fruits.count("poire"):
    print("trouvé (if)")
elif fruits.count("cerise"):
    print("trouvé (elif)")
else:
    print("pas trouvé (else)")