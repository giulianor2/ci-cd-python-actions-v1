import os
from decimal import Decimal

import mysql.connector
import pytest

from db import buscar_produto, conectar, criar_tabela, inserir_produto

# Se não houver banco configurado (ex.: na sua máquina), os testes são pulados.
pytestmark = pytest.mark.skipif(
    "MYSQL_HOST" not in os.environ, reason="MYSQL_HOST não definida"
)


@pytest.fixture
def conn():
    """Prepara o banco antes de cada teste e limpa tudo depois."""
    conexao = conectar()
    criar_tabela(conexao)
    yield conexao
    conexao.rollback()
    cur = conexao.cursor()
    cur.execute("TRUNCATE TABLE produtos")  # esvazia a tabela e zera o AUTO_INCREMENT
    cur.close()
    conexao.close()


def test_inserir_e_buscar_produto(conn):
    novo_id = inserir_produto(conn, "Teclado", 150.00)
    assert buscar_produto(conn, novo_id) == ("Teclado", Decimal("150.00"))


def test_banco_rejeita_preco_negativo(conn):
    # A constraint CHECK (preco >= 0) deve impedir a inserção
    with pytest.raises(mysql.connector.Error):
        inserir_produto(conn, "Mouse", -10)
      