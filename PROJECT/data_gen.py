import random

# Parameters
d = 50
m = 10000
coordinate_range = (-1000, 1000)

# Generate m random points and save to database.txt
with open("database.txt", "w") as f:
    for _ in range(m):
        point = [random.randint(*coordinate_range) for _ in range(d)]
        f.write(",".join(map(str, point)) + "\n")

print(f"{m} random points generated and saved to database.txt.")
