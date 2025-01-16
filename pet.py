import streamlit as st
import mysql.connector
from datetime import datetime
import pandas as pd

# Criando um menu lateral
st.set_page_config(layout="wide")
st.sidebar.image('logo1.png', width=200)
st.sidebar.image('petlove.png', width=100)
st.sidebar.text("Solution Logística - Maceió/Al")
st.sidebar.text('Endereço: R. João Monteiro da Silva, 1600 - Tabuleiro do Martins, Maceió - AL, 57081-780')


# Configuração de conexão com o banco de dados
def connect_to_database():
    return mysql.connector.connect(
        host="solution_bi.mysql.dbaas.com.br",
        user="solution_bi",
        password="J3aQqCZ5j32Eq@",
        database="solution_bi"
    )

# Função para criar tabela no banco de dados
def create_table():
    conn = None
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        # Query para criar a tabela
        query = """
        CREATE TABLE IF NOT EXISTS expedição_petlove (
            id INT AUTO_INCREMENT PRIMARY KEY,
            data_planejamento DATE NOT NULL,
            numero_pedido VARCHAR(50) NOT NULL,
            nome_cliente VARCHAR(100) NOT NULL,
            numero_cliente VARCHAR(50) NOT NULL,
            endereco TEXT NOT NULL,
            bairro VARCHAR(100) NOT NULL,
            cidade VARCHAR(100) NOT NULL,
            uf VARCHAR(2) NOT NULL,
            rota VARCHAR(100),
            tipo_expedicao ENUM('BONIFICAÇÃO', 'VENDA NORMAL') NOT NULL,
            quantidade INT NOT NULL,
            data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(query)
        conn.commit()
        st.info("Aviso: Faça todos os registros com letras maiúsculas e sem acentos.")
    except mysql.connector.Error as err:
        st.error(f"Erro ao criar/verificar a tabela: {err}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# Verificar e criar tabela ao iniciar
create_table()

st.header("Solution Logística - Controle e Registro Logístico", anchor="header")

# Criando abas
tabs = st.tabs(["Página inicial", "Registro Expedição", "Power BI", "Contato", "Tabela de Pedidos"])

# Conteúdo da aba "Página inicial"
with tabs[0]:
    st.write("Bem-vindo ao Controle e Registro Logístico")
    url = "https://www.youtube.com/watch?v=M-X7Z7TT_7M"
    st.video(url)
    st.markdown("""
        **A Solution Log Movidos por ir mais longe!**
        
        Buscar novas oportunidades, ampliar nossos horizontes e abrir novos caminhos está em nossa razão de ser. 
        Começamos a contar a nossa história em 2009, com um olhar para o futuro, focado no presente.
    """)
    col1, col2 = st.columns(2)
    with col1:
        st.image('sol1.png', caption="Conheça nossas Soluções")
    with col2:
        st.image('sol2.png', caption="Nossa Razão de existir")
    st.text("2024 - Aplicação desenvolvida por: Williams Rodrigues - Analista de Dados e Logística")
    st.text("Tel.: (82) 98863-9394")
    st.text("Versão:1.0.0")

# Conteúdo da aba "Registro Expedição"
with tabs[1]:
    st.header("Registre aqui a sua expedição diária por Nº Pedidos")

    # Campos de entrada
    data = st.date_input("Data do Planejamento", key="data")
    praca = st.text_input("Praça", key="praca")
    pedido = st.text_input("Nº Pedido", key="pedido")
    cliente_nome = st.text_input("Nome do Cliente", key="cliente_nome")
    cliente_numero = st.text_input("Nº Cliente", key="cliente_numero")
    endereco = st.text_input("Endereço Completo", key="endereco")
    bairro = st.text_input("Bairro", key="bairro")
    cidade = st.text_input("Cidade", key="cidade")
    uf = st.text_input("UF", key="uf")
    rota = st.text_input("Rota", key="rota")
    tipo_expedicao = st.selectbox("Tipo de Expedição", ["SELECIONE UM TIPO", "BONIFICAÇÃO", "VENDA NORMAL","AMOSTRA"], key="tipo_expedicao")
    quantidade = st.text_input("Quantidade", key="quantidade")

    # Botão de envio com verificação de duplicidade
    if st.button("Enviar", key="enviar", help="Clique para enviar os dados", icon="📨"):
            
        # Garantir que todos os campos obrigatórios estejam preenchidos
        if all([
            data,
            pedido.strip(),
            cliente_nome.strip(),
            cliente_numero.strip(),
            endereco.strip(),
            bairro.strip(),
            cidade.strip(),
            uf.strip(),
            tipo_expedicao != "SELECIONE UM TIPO",
            quantidade.strip().isdigit()
        ]):
            try:
                conn = connect_to_database()
                cursor = conn.cursor()

                # Verificar se o registro já existe
                check_query = """
                SELECT COUNT(*) 
                FROM expedição_petlove 
                WHERE numero_pedido = %s AND data_planejamento = %s AND nome_cliente = %s
                """
                cursor.execute(check_query, (pedido, data, cliente_nome))
                record_exists = cursor.fetchone()[0] > 0

                if record_exists:
                    st.warning("Registro duplicado! Este pedido já foi registrado.")
                else:
                    # Inserir os dados no banco de dados
                    insert_query = """
                    INSERT INTO expedição_petlove (data_planejamento, numero_pedido, nome_cliente, numero_cliente, endereco, bairro, cidade, uf, rota, tipo_expedicao, quantidade)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    values = (data, pedido, cliente_nome, cliente_numero, endereco, bairro, cidade, uf, rota, tipo_expedicao, int(quantidade))
                    cursor.execute(insert_query, values)
                    conn.commit()
                    st.success("Registro inserido com sucesso!")
            except mysql.connector.Error as err:
                st.error(f"Erro ao acessar o banco de dados: {err}")
            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()
    else:
            st.warning("Por favor, preencha todos os campos obrigatórios!")

# Conteúdo da aba "Power BI"
with tabs[2]:
    st.header("Acompanhe a operação em tempo real")
    
    # URL do relatório Power BI 1080 x 1920
    url = "https://app.powerbi.com/view?r=eyJrIjoiZjU2ZTMwZDYtZTU3Ny00Y2U3LTgwOTEtMTExZDgzMTI5MmJlIiwidCI6IjNiNTg1ODA2LWQzNTMtNDQxYy1iNGU2LTM3ZGE3YTM1NzMxNiJ9"
    
    # Incorporar o iframe do Power BI com a resolução 1080x1920
    st.components.v1.iframe(src=url, width=1100, height=600)

# Conteúdo da aba "Contato"
with tabs[3]:
    st.header("Contato")
    st.markdown("**Williams Rodrigues - Analista de Dados e Logística**")
    st.markdown("""
        📱 **WhatsApp:** [Clique aqui](https://wa.me/5582988639394)
        📧 **Email:** logistica4.mcz@solution-log.com
    """)

# Conteúdo da aba "Tabela de Pedidos Expedidos"
with tabs[4]:
    st.header("Tabela de Pedidos Expedidos")

    try:
        # Conectar ao banco de dados
        conn = connect_to_database()
        
        # Consultar dados da tabela
        query = "SELECT * FROM expedição_petlove"
        df = pd.read_sql(query, conn)
        
        # Verificar se o DataFrame contém dados
        if not df.empty:
            st.write("Veja abaixo os registros disponíveis:")

            # Campo de entrada para filtro por "Nº Pedido"
            filtro_pedido = st.text_input("Filtrar por Nº Pedido (Digite parte ou todo o número)", key="filtro_pedido")
            
            # Aplicar filtro
            if filtro_pedido:
                df_filtrado = df[df['numero_pedido'].str.contains(filtro_pedido, case=False, na=False)]
                st.write(f"Exibindo resultados para o filtro: `{filtro_pedido}`")
            else:
                df_filtrado = df

            # Exibir o DataFrame
            st.dataframe(df_filtrado)

            # Campo para deletar registros
            filtro_deletar = st.text_input("Deletar Pedido (Digite o Nº Pedido a ser deletado)", key="filtro_deletar")
            if filtro_deletar:
                try:
                    cursor = conn.cursor()
                    delete_query = "DELETE FROM expedição_petlove WHERE numero_pedido = %s"
                    cursor.execute(delete_query, (filtro_deletar,))
                    conn.commit()
                    st.success(f"Registro com Nº Pedido {filtro_deletar} deletado com sucesso!")
                except mysql.connector.Error as err:
                    st.error(f"Erro ao deletar registro: {err}")
                finally:
                    cursor.close()
        else:
            st.warning("Nenhum registro encontrado no banco de dados!")

    except mysql.connector.Error as err:
        st.error(f"Erro ao acessar o banco de dados: {err}")
    except Exception as ex:
        st.error(f"Erro inesperado: {ex}")
    finally:
        if conn.is_connected():
            conn.close()

    # Total de registros no dataframe
    total_registros = len(df_filtrado) if 'df_filtrado' in locals() else 0
    st.write(f"Total de registros: {total_registros}")
