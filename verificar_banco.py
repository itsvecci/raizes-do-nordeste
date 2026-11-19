import sqlite3

conexao = sqlite3.connect("raizes.db")

resultado = conexao.execute(
    "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
).fetchall()

print("Tabelas encontradas:")

for tabela in resultado:
    print("-", tabela[0])

conexao.close()