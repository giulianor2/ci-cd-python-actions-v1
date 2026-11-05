import os

import mysql.connector



def conectar():
    """Abre a conexão usando variáveis de ambiente (nada de senha no código!)."""
    return mysql.connector.connect(
        host=os.environ["MYSQL_HOST"],
        port=int(os.environ.get("MYSQL_PORT", "3306")),
        user=os.environ["MYSQL_USER"],
        password=os.environ["MYSQL_PASSWORD"],
        database=os.environ["MYSQL_DATABASE"],
    )


def criar_tabela(conn):
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS produtos (
            id    INT AUTO_INCREMENT PRIMARY KEY,
            nome  VARCHAR(100) NOT NULL,
            preco DECIMAL(10, 2) NOT NULL,
            CONSTRAINT chk_preco_positivo CHECK (preco >= 0)
        )
        """
    )
    conn.commit()
    cur.close()


def inserir_produto(conn, nome, preco):
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO produtos (nome, preco) VALUES (%s, %s)",
        (nome, preco),
    )
    novo_id = cur.lastrowid  # o MySQL não tem RETURNING: o id gerado vem daqui
    conn.commit()
    cur.close()
    return novo_id


def buscar_produto(conn, produto_id):
    cur = conn.cursor(buffered=True)
    cur.execute("SELECT nome, preco FROM produtos WHERE id = %s", (produto_id,))
    linha = cur.fetchone()
    cur.close()
    return linha