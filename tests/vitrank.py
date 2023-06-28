import math
import random

salary: int = int(input("salary: "))
marks: int = int(input("expected marks:"))

total = 400000 # candidates

if salary>1000000:
    print(random.choice(range(0, int((marks * salary)/1000))))
elif salary < 1000000:
    print(random.choice(range(0,int((marks * salary)/100))))
