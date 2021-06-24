import secrets

system_random = secrets.SystemRandom()

s = system_random.randint(1, 60)

print(s)

f = system_random.randint(1, 60)
print(f)
