# app.py
import streamlit as st
import pandas as pd
import os
import numpy as np
from datetime import datetime, date, timedelta
import altair as alt

# -----------------------------------------
# CONFIGURAÇÕES
# -----------------------------------------
st.set_page_config(
    page_title="Controle Financeiro", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Estilo limpo
st.markdown("""
<style>
            

    .st-emotion-cache-155jwzh{
    background: black !important;
    }
      /* ===== BASE CYBERPUNK ===== */
    .main {
        background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #16213e 100%);
        color: white !important;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #16213e 100%);
    }
    
     /* ===== TEXTO CYBERPUNK ===== */
    * {
        color: white !important;
    }
    
    h1 {
        color: white !important;
        font-weight: 900 !important;
        font-size: 3rem !important;
        text-align: center;
        font-family: Avantgarde, TeX Gyre Adventor, URW Gothic L, sans-serif !important;
        letter-spacing: 2px;
    }
    
    h2 {
        color: white !important;
        font-weight: 800 !important;
        font-size: 2rem !important;
        border-left: 4px solid black;
        padding-left: 15px;
        font-family: 'Courier New', monospace !important;
    }
    
    h3 {
        color: white !important;
        font-weight: 700 !important;
        font-size: 1.5rem !important;
        font-family: 'Courier New', monospace !important;
    }
    
     /* ===== SIDEBAR CYBERPUNK ===== */
    .css-1d391kg {
        background: rgba(10, 10, 15, 0.9) !important;
        backdrop-filter: blur(15px);
        border-right: 1px solid #00ff88;
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.3);
    }
    
    .sidebar .sidebar-content {
        background: rgba(10, 10, 15, 0.9) !important;
    }
    
    
    /* ===== BOTÕES CYBERPUNK ===== */
    .stButton>button {
        background: linear-gradient(135deg, #0a0a0f 0%, #1a1a5e 50%, #16213e 100%) !important;
        color: #0a0a0f !important;
        border: 2px solid white !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-weight: 800 !important;
        font-size: 14px !important;
        font-family: 'Courier New', monospace !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        background: linear-gradient(135deg, #10f298 0%, #00cc6a 100%) !important;
    }
    
    /* Botão de exclusão cyberpunk */
    .delete-btn>button {
        background: linear-gradient(135deg, #ff00ff 0%, #cc00cc 100%) !important;
        border: 2px solid #ff00ff !important;
        box-shadow: 0 0 15px rgba(255, 0, 255, 0.5) !important;
        color: #0a0a0f !important;
    }
    
    .delete-btn>button:hover {
        box-shadow: 0 0 25px rgba(255, 0, 255, 0.8) !important;
    }
    
    /* ===== CARDS E CONTAINERS ===== */
    .stMetric {
        background: linear-gradient(135deg, #0a0a0f 0%, #1a1a5e 50%, #16213e 100%) !important;
        backdrop-filter: blur(10px);
        border-radius: 16px !important;
        padding: 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1) !important;
    }
    
     /* ===== FORMULÁRIOS CYBERPUNK ===== */
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div>select, .stDateInput>div>div>input {
        background: rgba(0,0,0,0.2)!important;
        border: 2px solid #1a1a5e !important;
        border-radius: 8px !important;
        color: black !important;
        padding: 12px 16px !important;
        font-size: 14px !important;
        font-family: 'Courier New', monospace !important;
        transition: all 0.3s ease !important;
    }
            
    .stTextInput>div>div>input:focus, 
    .stNumberInput>div>div>input:focus,
    .stSelectbox>div>div>select:focus,
    .stDateInput>div>div>input:focus {
        border: 2px solid #ff00ff !important;
        box-shadow: 0 0 15px rgba(255, 0, 255, 0.5) !important;
        background: rgba(255, 0, 255, 0.1) !important;
    }
    
    /* Placeholder neon */
    .stTextInput>div>div>input::placeholder {
        color: black !important;
    }
                    
      /* ===== DATAFRAME CYBER ===== */
    .stDataFrame {
        border-radius: 12px !important;
        background: rgba(0, 255, 136, 0.05) !important;
        border: 1px solid #00ff88 !important;
        overflow: hidden;
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.2) !important;
    }
    
     /* ===== ABAS CYBERPUNK ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(0, 255, 136, 0.1);
        border-radius: 12px;
        padding: 6px;
        border: 1px solid #00ff88;
    }
            
     .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 10px 20px;
        background: transparent;
        color: #00ff88 !important;
        font-weight: 700;
        font-family: 'Courier New', monospace;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00ff88 0%, #007a44 100%) !important;
        color: #0a0a0f !important;
        box-shadow: 0 0 15px rgba(0, 255, 136, 0.5);
    }
    
    /* ===== MENSAGENS NEON ===== */
    .stSuccess {
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.2) 0%, rgba(0, 255, 136, 0.1) 100%) !important;
        color: #00ff88 !important;
        border-radius: 12px !important;
        border: 1px solid #00ff88 !important;
        box-shadow: 0 0 15px rgba(0, 255, 136, 0.3) !important;
    }
    
    .stError {
        background: linear-gradient(135deg, rgba(255, 0, 255, 0.2) 0%, rgba(255, 0, 255, 0.1) 100%) !important;
        color: #ff00ff !important;
        border-radius: 12px !important;
        border: 1px solid #ff00ff !important;
        box-shadow: 0 0 15px rgba(255, 0, 255, 0.3) !important;
    }
    
    .stInfo {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.2) 0%, rgba(0, 255, 255, 0.1) 100%) !important;
        color: #00ffff !important;
        border-radius: 12px !important;
        border: 1px solid #00ffff !important;
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.3) !important;
    }
    
    .stWarning {
        background: linear-gradient(135deg, rgba(255, 255, 0, 0.2) 0%, rgba(255, 255, 0, 0.1) 100%) !important;
        color: #ffff00 !important;
        border-radius: 12px !important;
        border: 1px solid #ffff00 !important;
        box-shadow: 0 0 15px rgba(255, 255, 0, 0.3) !important;
    }
    
    /* ===== DIVISÓRIAS NEON ===== */
    hr {
        margin: 2rem 0 !important;
        border: none !important;
        height: 2px !important;
        background: linear-gradient(90deg, transparent, #00ff88, #ff00ff, #00ffff, transparent) !important;
        box-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
    }
    
    /* ===== SCROLLBAR CYBER ===== */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(0, 255, 136, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #00ff88 0%, #ff00ff 100%);
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #ff00ff 0%, #00ffff 100%);
    }
            
      /* ===== MÉTRICAS CYBER ===== */
    div[data-testid="metric-container"] {
        background: rgba(0, 255, 136, 0.1) !important;
        backdrop-filter: blur(10px);
        border: 1px solid #00ff88 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.2) !important;
    }
    
     /* ===== RODAPÉ CYBER ===== */
    .stCaption {
        color: #00ff88 !important;
        text-align: center !important;
        font-size: 12px !important;
        margin-top: 3rem !important;
        text-shadow: 0 0 5px #00ff88;
        font-family: 'Courier New', monospace !important;
    }
    
    /* ===== ANIMAÇÕES CYBERPUNK ===== */
    @keyframes glitch {
        0% { transform: translate(0); }
        20% { transform: translate(-2px, 2px); }
        40% { transform: translate(-2px, -2px); }
        60% { transform: translate(2px, 2px); }
        80% { transform: translate(2px, -2px); }
        100% { transform: translate(0); }
    }
    
    @keyframes neonPulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    h1 {
        animation: neonPulse 2s infinite;
    }
    
    .stButton>button:hover {
        animation: glitch 0.3s;
    }
    
    .main::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(rgba(0, 255, 136, 0.03) 50%, transparent 50%);
        background-size: 100% 4px;
        pointer-events: none;
        z-index: 9999;
    }
</style>
""", unsafe_allow_html=True)

DATA_FOLDER = "data"
os.makedirs(DATA_FOLDER, exist_ok=True)

# Esquema fixo
REQUIRED_COLUMNS = [
    "id", "nome_pessoa", "Categoria", "Descricao", "Tipo", 
    "Conta", "FormaPagamento", "Status", "Data", "Valor", "Subtotal"
]

# Opções pré-definidas - AGORA COM FUNÇÃO DE GERENCIAR
BANK_OPTIONS = ["Itau", "Caixa", "PagBank", "Bradesco", "Mercado Pago", "Paypal", "Ifinit Pay", "Nubank", "PicPay", "Inter", "Pan", "Carteira"]
ACCOUNT_TYPES = ["Corrente", "Poupanca"]
CATEGORY_OPTIONS = ["Cuidado Pessoal", "Moradia", "Alimentacao", "Saude", "Carro", "Pet", "Lazer", "Outros"]
TIPO_OPTIONS = ["entrada", "saida", "transferencia", "investimento"]
FORMA_PGTO = ["pix", "dinheiro", "QR", "boleto", "debito", "credito"]
STATUS_OPTIONS = ["pago", "pendente", "atrasado"]

# -----------------------------------------
# FUNÇÕES UTILITÁRIAS
# -----------------------------------------
def list_data_files():
    """Lista todos os arquivos .xlsx na pasta data"""
    files = [f for f in os.listdir(DATA_FOLDER) if f.endswith(".xlsx")]
    return files

def create_new_file(filename):
    """Cria um novo arquivo com o esquema padrão"""
    if not filename.strip():
        return None, "Nome do arquivo não pode estar vazio"
    
    if not filename.endswith(".xlsx"):
        filename += ".xlsx"
    
    filepath = os.path.join(DATA_FOLDER, filename)
    
    if os.path.exists(filepath):
        return None, "Já existe um arquivo com este nome"
    
    # Cria DataFrame vazio com colunas padrão
    df = pd.DataFrame(columns=REQUIRED_COLUMNS)
    df['Valor'] = df['Valor'].astype(float)
    df['Subtotal'] = df['Subtotal'].astype(float)
    
    try:
        df.to_excel(filepath, index=False)
        return filename, "Arquivo criado com sucesso!"
    except Exception as e:
        return None, f"Erro ao criar arquivo: {e}"

def load_file(filename):
    """Carrega e valida um arquivo existente"""
    filepath = os.path.join(DATA_FOLDER, filename)
    
    if not os.path.exists(filepath):
        return None, "Arquivo não encontrado"
    
    try:
        df = pd.read_excel(filepath)
        
        # Verifica se tem todas as colunas necessárias
        missing_cols = set(REQUIRED_COLUMNS) - set(df.columns)
        if missing_cols:
            return None, f"Arquivo não segue o padrão. Colunas faltantes: {missing_cols}"
        
        # Garante os tipos corretos - CONVERTE TODAS AS DATAS PARA TIMESTAMP
        df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
        df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce')
        df['Subtotal'] = pd.to_numeric(df['Subtotal'], errors='coerce')
        
        # Preenche IDs se necessário
        if df['id'].isna().any() or df.empty:
            df['id'] = range(1, len(df) + 1)
        
        return df, "Arquivo carregado com sucesso!"
    
    except Exception as e:
        return None, f"Erro ao carregar arquivo: {e}"

def save_file(df, filename):
    """Salva o DataFrame no arquivo"""
    filepath = os.path.join(DATA_FOLDER, filename)
    # Converte datas para formato string antes de salvar
    df_save = df.copy()
    df_save['Data'] = pd.to_datetime(df_save['Data']).dt.strftime('%Y-%m-%d')
    df_save.to_excel(filepath, index=False)
    return True

def calculate_subtotal(df):
    """Recalcula o subtotal baseado na ordem de data"""
    if df.empty:
        return df
    
    # Garante que todas as datas são Timestamp
    df['Data'] = pd.to_datetime(df['Data'])
    df = df.sort_values('Data').reset_index(drop=True)
    df['Subtotal'] = df['Valor'].cumsum()
    return df

def get_transfer_accounts():
    """Gera combinações para transferências entre bancos"""
    transfer_accounts = []
    for bank1 in st.session_state.bank_options:
        for bank2 in st.session_state.bank_options:
            if bank1 != bank2:
                transfer_accounts.append(f"{bank1}/{bank2}")
    return transfer_accounts

# -----------------------------------------
# PÁGINA PRINCIPAL
# -----------------------------------------
def main_page():
    st.title("💰 Controle Financeiro Pessoal")
    st.markdown("---")

    # -----------------------------------------
    # SIDEBAR - GERENCIAMENTO DE ARQUIVOS E BANCOS
    # -----------------------------------------
    st.sidebar.header("📁 Gerenciar Arquivos")

    # Criar novo arquivo
    st.sidebar.subheader("Criar Novo Arquivo")
    new_file_name = st.sidebar.text_input("Nome do arquivo:")
    if st.sidebar.button("Criar Arquivo"):
        if new_file_name:
            filename, message = create_new_file(new_file_name)
            if filename:
                st.sidebar.success(message)
                st.rerun()
            else:
                st.sidebar.error(message)
        else:
            st.sidebar.error("Digite um nome para o arquivo")

    st.sidebar.markdown("---")

    # Abrir arquivo existente
    st.sidebar.subheader("Abrir Arquivo Existente")
    files = list_data_files()
    if files:
        selected_file = st.sidebar.selectbox("Selecione um arquivo:", ["-- Selecione --"] + files)
    else:
        selected_file = "-- Selecione --"
        st.sidebar.info("Nenhum arquivo encontrado. Crie um novo arquivo.")

    st.sidebar.markdown("---")

    # GERENCIAR BANCOS - AGORA COM EDITAR/EXCLUIR
    st.sidebar.header("🏦 Gerenciar Bancos")

    # Inicializar session state para bancos
    if 'bank_options' not in st.session_state:
        st.session_state.bank_options = BANK_OPTIONS.copy()
    
    # Mostrar bancos atuais com opções de exclusão
    st.sidebar.write("**Bancos cadastrados:**")
    
    for i, bank in enumerate(st.session_state.bank_options):
        col1, col2 = st.sidebar.columns([3, 1])
        with col1:
            st.sidebar.write(f"• {bank}")
        with col2:
            if st.sidebar.button("🗑️", key=f"del_{bank}"):
                if bank in st.session_state.bank_options:
                    st.session_state.bank_options.remove(bank)
                st.rerun()

    # Adicionar novo banco
    st.sidebar.markdown("---")
    st.sidebar.subheader("Adicionar Novo Banco")
    novo_banco = st.sidebar.text_input("Nome do novo banco:")

    if st.sidebar.button("➕ Adicionar Banco"):
        if novo_banco and novo_banco.strip():
            if novo_banco.strip() not in st.session_state.bank_options:
                st.session_state.bank_options.append(novo_banco.strip())
                st.sidebar.success(f"Banco '{novo_banco}' adicionado!")
                st.rerun()
            else:
                st.sidebar.error("Este banco já existe!")
        else:
            st.sidebar.error("Digite um nome para o banco")

    # Botão para Dashboard
    st.sidebar.markdown("---")
    if st.sidebar.button("📈 Ir para Dashboard"):
        st.session_state.current_page = "dashboard"
        st.rerun()

    # Carregar dados
    df = pd.DataFrame()
    active_filename = None

    if selected_file and selected_file != "-- Selecione --":
        df, message = load_file(selected_file)
        if df is not None:
            active_filename = selected_file
            st.sidebar.success(f"✅ {message}")
        else:
            st.sidebar.error(f"❌ {message}")

    # -----------------------------------------
    # ÁREA PRINCIPAL - APENAS SE ARQUIVO ESTIVER ABERTO
    # -----------------------------------------
    if active_filename:
        st.header(f"📊 Arquivo: {active_filename}")
        
        # Botões de ação rápida
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💾 Salvar Alterações"):
                if save_file(df, active_filename):
                    st.success("Arquivo salvo com sucesso!")
        
        with col2:
            if st.button("🔄 Recalcular Subtotais"):
                df = calculate_subtotal(df)
                st.success("Subtotais recalculados!")
        
        with col3:
            if st.button("📤 Exportar Backup"):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                export_name = f"backup_{active_filename.split('.')[0]}_{timestamp}.xlsx"
                if save_file(df, export_name):
                    st.success(f"Exportado como: {export_name}")
        
        st.markdown("---")
        
        # -----------------------------------------
        # BARRA DE PESQUISA E FILTROS
        # -----------------------------------------
        st.subheader("🔍 Pesquisar e Filtrar")
        
        search_col1, search_col2, search_col3 = st.columns(3)
        
        with search_col1:
            search_term = st.text_input("Pesquisar (qualquer campo):")
        
        with search_col2:
            filter_category = st.selectbox("Filtrar por categoria:", ["Todas"] + CATEGORY_OPTIONS)
        
        with search_col3:
            filter_tipo = st.selectbox("Filtrar por tipo:", ["Todos"] + TIPO_OPTIONS)
        
        # Aplicar filtros
        filtered_df = df.copy()
        
        if search_term:
            mask = (
                filtered_df['id'].astype(str).str.contains(search_term, case=False, na=False) |
                filtered_df['nome_pessoa'].str.contains(search_term, case=False, na=False) |
                filtered_df['Descricao'].str.contains(search_term, case=False, na=False) |
                filtered_df['Categoria'].str.contains(search_term, case=False, na=False) |
                filtered_df['Conta'].str.contains(search_term, case=False, na=False)
            )
            filtered_df = filtered_df[mask]
        
        if filter_category != "Todas":
            filtered_df = filtered_df[filtered_df['Categoria'] == filter_category]
        
        if filter_tipo != "Todos":
            filtered_df = filtered_df[filtered_df['Tipo'] == filter_tipo]
        
        # -----------------------------------------
        # ADICIONAR NOVA LINHA
        # -----------------------------------------
        st.subheader("➕ Adicionar Nova Transação")
        
        with st.form("nova_transacao", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                nome_pessoa = st.text_input("Nome da Pessoa:", placeholder="Ex: João Silva")
                categoria = st.selectbox("Categoria:", CATEGORY_OPTIONS)
                descricao = st.text_input("Descrição:", placeholder="Ex: Pagamento de conta")
                tipo = st.selectbox("Tipo:", TIPO_OPTIONS)
                
            with col2:
                # Banco e tipo de conta - AGORA COM TRANSFERÊNCIAS
                if tipo == "transferencia":
                    # Para transferências: mostrar combinação entre bancos
                    transfer_options = get_transfer_accounts()
                    conta_completa = st.selectbox("Transferência entre:", transfer_options)
                else:
                    # Para outros tipos: banco normal
                    banco = st.selectbox("Banco:", st.session_state.bank_options)
                    conta_tipo = st.selectbox("Tipo de Conta:", ACCOUNT_TYPES)
                    conta_completa = f"{banco} - {conta_tipo}"
                
                forma_pagamento = st.selectbox("Forma de Pagamento:", FORMA_PGTO)
                status = st.selectbox("Status:", STATUS_OPTIONS)
                data_transacao = st.date_input("Data:", value=date.today())
                valor = st.number_input("Valor (R$):", min_value=0.0, format="%.2f", step=0.01)
            
            submitted = st.form_submit_button("💾 Adicionar Transação")
            
            if submitted:
                if not nome_pessoa.strip():
                    st.error("Nome da pessoa é obrigatório!")
                else:
                    # Criar nova linha - CONVERTE date para Timestamp
                    new_id = df['id'].max() + 1 if not df.empty else 1
                    new_row = {
                        'id': new_id,
                        'nome_pessoa': nome_pessoa.strip(),
                        'Categoria': categoria,
                        'Descricao': descricao.strip(),
                        'Tipo': tipo,
                        'Conta': conta_completa,
                        'FormaPagamento': forma_pagamento,
                        'Status': status,
                        'Data': pd.to_datetime(data_transacao),  # CONVERTE para Timestamp
                        'Valor': valor,
                        'Subtotal': 0.0
                    }
                    
                    # Adicionar ao DataFrame
                    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                    df = calculate_subtotal(df)
                    
                    # Salvar automaticamente
                    save_file(df, active_filename)
                    st.success("✅ Transação adicionada com sucesso!")
                    st.rerun()
        
        # -----------------------------------------
        # TABELA DE DADOS
        # -----------------------------------------
        st.subheader("📋 Transações")
        
        if not filtered_df.empty:
            # Formatar a tabela para exibição
            display_df = filtered_df.copy()
            display_df['Data'] = pd.to_datetime(display_df['Data']).dt.strftime('%d/%m/%Y')
            display_df['Valor'] = display_df['Valor'].map('R$ {:,.2f}'.format)
            display_df['Subtotal'] = display_df['Subtotal'].map('R$ {:,.2f}'.format)
            
            st.dataframe(display_df, use_container_width=True, height=400)
            
            # -----------------------------------------
            # EDITAR/EXCLUIR TRANSAÇÃO
            # -----------------------------------------
            st.subheader("✏️ Gerenciar Transação")
            
            transacao_id = st.selectbox(
                "Selecione o ID da transação para editar/excluir:",
                options=["-- Selecione --"] + filtered_df['id'].astype(int).astype(str).tolist()
            )
            
            if transacao_id != "-- Selecione --":
                transacao_id = int(transacao_id)
                transacao_data = df[df['id'] == transacao_id].iloc[0]
                
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write("**Dados atuais:**")
                    info_data = {
                        "ID": transacao_data['id'],
                        "Nome": transacao_data['nome_pessoa'],
                        "Categoria": transacao_data['Categoria'],
                        "Descrição": transacao_data['Descricao'],
                        "Tipo": transacao_data['Tipo'],
                        "Conta": transacao_data['Conta'],
                        "Forma Pagamento": transacao_data['FormaPagamento'],
                        "Status": transacao_data['Status'],
                        "Data": transacao_data['Data'].strftime('%d/%m/%Y'),
                        "Valor": f"R$ {transacao_data['Valor']:,.2f}"
                    }
                    
                    for key, value in info_data.items():
                        st.write(f"**{key}:** {value}")
                
                with col2:
                    if st.button("🗑️ Excluir", key="delete_transaction"):
                        df = df[df['id'] != transacao_id]
                        df = calculate_subtotal(df)
                        save_file(df, active_filename)
                        st.success("✅ Transação excluída!")
                        st.rerun()
                
                # Formulário de edição
                with st.form("editar_transacao"):
                    st.write("**Editar transação:**")
                    
                    edit_col1, edit_col2 = st.columns(2)
                    
                    with edit_col1:
                        edit_nome = st.text_input("Nome:", value=transacao_data['nome_pessoa'])
                        edit_categoria = st.selectbox("Categoria:", CATEGORY_OPTIONS, 
                                                   index=CATEGORY_OPTIONS.index(transacao_data['Categoria']))
                        edit_descricao = st.text_input("Descrição:", value=transacao_data['Descricao'])
                        edit_tipo = st.selectbox("Tipo:", TIPO_OPTIONS, 
                                               index=TIPO_OPTIONS.index(transacao_data['Tipo']))
                    
                    with edit_col2:
                        # Para transferências
                        if edit_tipo == "transferencia":
                            transfer_options = get_transfer_accounts()
                            try:
                                current_index = transfer_options.index(transacao_data['Conta'])
                            except:
                                current_index = 0
                            edit_conta = st.selectbox("Transferência entre:", transfer_options, index=current_index)
                        else:
                            # Para outros tipos
                            try:
                                if " - " in transacao_data['Conta']:
                                    banco_atual, tipo_conta_atual = transacao_data['Conta'].split(" - ")
                                else:
                                    banco_atual, tipo_conta_atual = st.session_state.bank_options[0], ACCOUNT_TYPES[0]
                            except:
                                banco_atual, tipo_conta_atual = st.session_state.bank_options[0], ACCOUNT_TYPES[0]
                            
                            edit_banco = st.selectbox("Banco:", st.session_state.bank_options, 
                                                    index=st.session_state.bank_options.index(banco_atual) if banco_atual in st.session_state.bank_options else 0)
                            edit_conta_tipo = st.selectbox("Tipo Conta:", ACCOUNT_TYPES, 
                                                         index=ACCOUNT_TYPES.index(tipo_conta_atual) if tipo_conta_atual in ACCOUNT_TYPES else 0)
                            edit_conta = f"{edit_banco} - {edit_conta_tipo}"
                        
                        edit_forma_pagamento = st.selectbox("Forma Pagamento:", FORMA_PGTO, 
                                                          index=FORMA_PGTO.index(transacao_data['FormaPagamento']))
                        edit_status = st.selectbox("Status:", STATUS_OPTIONS, 
                                                index=STATUS_OPTIONS.index(transacao_data['Status']))
                        edit_data = st.date_input("Data:", value=transacao_data['Data'].date())
                        edit_valor = st.number_input("Valor:", value=float(transacao_data['Valor']), 
                                                   format="%.2f", step=0.01)
                    
                    if st.form_submit_button("💾 Salvar Alterações"):
                        # Atualizar dados - CONVERTE date para Timestamp
                        df.loc[df['id'] == transacao_id, 'nome_pessoa'] = edit_nome
                        df.loc[df['id'] == transacao_id, 'Categoria'] = edit_categoria
                        df.loc[df['id'] == transacao_id, 'Descricao'] = edit_descricao
                        df.loc[df['id'] == transacao_id, 'Tipo'] = edit_tipo
                        df.loc[df['id'] == transacao_id, 'Conta'] = edit_conta
                        df.loc[df['id'] == transacao_id, 'FormaPagamento'] = edit_forma_pagamento
                        df.loc[df['id'] == transacao_id, 'Status'] = edit_status
                        df.loc[df['id'] == transacao_id, 'Data'] = pd.to_datetime(edit_data)  # CONVERTE
                        df.loc[df['id'] == transacao_id, 'Valor'] = edit_valor
                        
                        # Recalcular subtotais
                        df = calculate_subtotal(df)
                        save_file(df, active_filename)
                        
                        st.success("✅ Transação atualizada com sucesso!")
                        st.rerun()
        
        else:
            st.info("📝 Nenhuma transação encontrada com os filtros aplicados.")
        
        # -----------------------------------------
        # TOTAIS POR CONTA
        # -----------------------------------------
        st.subheader("🏦 Totais por Conta/Banco")
        
        if not df.empty:
            totais_contas = df.groupby('Conta')['Valor'].sum().reset_index()
            totais_contas = totais_contas.sort_values('Valor', ascending=False)
            
            # Mostrar métricas individuais
            cols = st.columns(min(4, len(totais_contas)))
            for idx, (_, row) in enumerate(totais_contas.iterrows()):
                if idx < 4:  # Mostrar apenas os 4 primeiros
                    with cols[idx]:
                        st.metric(
                            label=row['Conta'],
                            value=f"R$ {row['Valor']:,.2f}"
                        )
            
            # Tabela completa
            st.dataframe(totais_contas.style.format({'Valor': 'R$ {:.2f}'}), use_container_width=True)

    else:
        # Tela inicial quando nenhum arquivo está aberto
        st.info("""
        **Bem-vindo ao Controle Financeiro!**
        
        Para começar:
        1. **Crie um novo arquivo** usando o menu lateral, OU
        2. **Abra um arquivo existente** se você já tiver dados
        
        💡 **Dica:** Você pode adicionar e excluir bancos no menu lateral!
        """)

# -----------------------------------------
# PÁGINA DO DASHBOARD
# -----------------------------------------
def dashboard_page():
    st.title("📊 Dashboard Financeiro")
    st.markdown("---")
    
    # Botão para voltar
    if st.button("⬅️ Voltar para Controle"):
        st.session_state.current_page = "main"
        st.rerun()
    
    # Carregar dados do arquivo ativo
    df = pd.DataFrame()
    active_filename = None
    
    files = list_data_files()
    if files:
        # Tentar carregar o primeiro arquivo disponível
        for file in files:
            df_temp, message = load_file(file)
            if df_temp is not None:
                df = df_temp
                active_filename = file
                break
    
    if active_filename:
        st.success(f"📁 Visualizando dados de: {active_filename}")
    else:
        st.warning("⚠️ Nenhum arquivo válido encontrado para mostrar no dashboard")
        # Criar dados de exemplo para demonstração
        df = pd.DataFrame(columns=REQUIRED_COLUMNS)
    
    st.markdown("---")
    
    # Métricas principais
    if not df.empty:
        pendentes = len(df[df['Status'] == 'pendente'])
        pagas = len(df[df['Status'] == 'pago'])
        atrasadas = len(df[df['Status'] == 'atrasado'])
        total_entradas = df[df['Tipo'] == 'entrada']['Valor'].sum()
        total_saidas = df[df['Tipo'] == 'saida']['Valor'].sum()
        saldo = total_entradas - total_saidas
    else:
        pendentes = pagas = atrasadas = total_entradas = total_saidas = saldo = 0
    
    # Métricas em cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Contas Pendentes", pendentes)
    with col2:
        st.metric("Contas Pagas", pagas)
    with col3:
        st.metric("Contas Atrasadas", atrasadas)
    with col4:
        st.metric("Saldo", f"R$ {saldo:,.2f}")
    
    st.markdown("---")
    
    # Gráficos EM ROSCA (DONUT)
    if not df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🍩 Gastos por Categoria")
            gastos_categoria = df[df['Tipo'] == 'saida'].groupby('Categoria')['Valor'].sum().reset_index()
            if not gastos_categoria.empty:
                # Gráfico de rosca para categorias
                base = alt.Chart(gastos_categoria).encode(
                    theta=alt.Theta("Valor:Q", stack=True),
                    radius=alt.Radius("Valor:Q", scale=alt.Scale(type="sqrt", zero=True, rangeMin=20)),
                    color=alt.Color("Categoria:N", scale=alt.Scale(scheme="category10")),
                    tooltip=["Categoria", "Valor"]
                )
                
                donut_chart_categoria = base.mark_arc(innerRadius=50, stroke="#fff") + base.mark_text(radiusOffset=15).encode(
                    text=alt.Text("Categoria:N")
                )
                
                st.altair_chart(donut_chart_categoria.properties(
                    height=400,
                    title="Distribuição de Gastos por Categoria"
                ), use_container_width=True)
            else:
                st.info("Sem dados de gastos por categoria")
        
        with col2:
            st.subheader("🏦 Gastos por Banco")
            gastos_banco = df[df['Tipo'] == 'saida'].groupby('Conta')['Valor'].sum().reset_index()
            if not gastos_banco.empty:
                # Gráfico de rosca para bancos
                base_banco = alt.Chart(gastos_banco).encode(
                    theta=alt.Theta("Valor:Q", stack=True),
                    radius=alt.Radius("Valor:Q", scale=alt.Scale(type="sqrt", zero=True, rangeMin=20)),
                    color=alt.Color("Conta:N", scale=alt.Scale(scheme="set3")),
                    tooltip=["Conta", "Valor"]
                )
                
                donut_chart_banco = base_banco.mark_arc(innerRadius=50, stroke="#fff") + base_banco.mark_text(radiusOffset=15).encode(
                    text=alt.Text("Conta:N")
                )
                
                st.altair_chart(donut_chart_banco.properties(
                    height=400,
                    title="Distribuição de Gastos por Banco"
                ), use_container_width=True)
            else:
                st.info("Sem dados de gastos por banco")
        
        # Linha do tempo (mantido como linha)
        st.subheader("📅 Evolução de Gastos ao Longo do Tempo")
        df_timeline = df.copy()
        df_timeline['Data'] = pd.to_datetime(df_timeline['Data'])
        timeline_data = df_timeline.groupby(df_timeline['Data'].dt.to_period('D'))['Valor'].sum().reset_index()
        timeline_data['Data'] = timeline_data['Data'].dt.to_timestamp()
        
        if not timeline_data.empty:
            chart_timeline = alt.Chart(timeline_data).mark_line(point=True, color='purple').encode(
                x='Data:T',
                y='Valor:Q',
                tooltip=['Data', 'Valor']
            ).properties(height=300, title="Evolução Diária")
            st.altair_chart(chart_timeline, use_container_width=True)
        
        # Humor de gastos - CORRIGIDO: usa .dt.date para comparar com date objects
        st.subheader("😊 Análise de Tendência de Gastos")
        hoje = datetime.now().date()
        ultimos_7_dias = hoje - timedelta(days=6)
        anteriores_7_dias = ultimos_7_dias - timedelta(days=7)
        
        # CORREÇÃO: usa .dt.date para comparar Timestamp com date
        gastos_ultimos_7 = df[
            (df['Data'].dt.date >= ultimos_7_dias) & 
            (df['Data'].dt.date <= hoje) &
            (df['Tipo'] == 'saida')
        ]['Valor'].sum()
        
        gastos_anteriores_7 = df[
            (df['Data'].dt.date >= anteriores_7_dias) & 
            (df['Data'].dt.date < ultimos_7_dias) &
            (df['Tipo'] == 'saida')
        ]['Valor'].sum()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Últimos 7 dias", f"R$ {gastos_ultimos_7:,.2f}")
        with col2:
            st.metric("7 dias anteriores", f"R$ {gastos_anteriores_7:,.2f}")
        
        # Humor
        st.markdown("---")
        if gastos_ultimos_7 > gastos_anteriores_7:
            st.error("😡 **Você está gastando MAIS que o período anterior**")
        elif gastos_ultimos_7 < gastos_anteriores_7:
            st.success("😊 **Você está gastando MENOS que o período anterior**")
        else:
            st.info("😐 **Seus gastos estão estáveis**")
    
    else:
        st.info("📊 O dashboard mostrará gráficos e métricas quando houver dados nos arquivos.")

# -----------------------------------------
# CONTROLE DE NAVEGAÇÃO
# -----------------------------------------
if 'current_page' not in st.session_state:
    st.session_state.current_page = "main"

if st.session_state.current_page == "dashboard":
    dashboard_page()
else:
    main_page()

# -----------------------------------------
# RODAPÉ
# -----------------------------------------
st.markdown("---")
st.caption("Controle Financeiro Pessoal | Desenvolvido para organização financeira")