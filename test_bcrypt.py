import bcrypt

password = input("Введите пароль: ").strip()

# переводим в байты
password_bytes = password.encode()

# генерируем соль и хеш
hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

print("\nВаш хеш:")
print(hashed.decode())   # выводим как строку


hashes = [
    b"$2b$12$zFbcmDzDcdhl5XTvhQ8/s.Lg2n3.bacGnZH7gWAUILYbU9Uo87m0K",
    b"$2b$12$Y4SJWDkQ0fxhfHTKqqYbE.NhXVMWl0tlntsOGrH/biaO0Wy1pa.62",
    b"$2b$12$pJdcIX33NPQtLpHIPuzWSec7xQD7eKb.pcB6HzOyUHgSqRCHUkgyO"
]

passwords_to_test = [
    "123456",
    "password",
    "111",
    "TesteR2024",
    "RedBurn",
    "222",
    "333",
    "tester",
]

for h in hashes:
    print("\nHASH:", h.decode())
    for p in passwords_to_test:
        # p → bytes
        pb = p.encode()

        if bcrypt.checkpw(pb, h):
            print(" ✔ MATCH:", p)
        else:
            print("   NO —", p)
