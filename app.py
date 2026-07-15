import importlib

import pandas as pd
import streamlit as st

import database

importlib.reload(database)

from database import (
    CATEGORIAS,
    CONTATO,
    EMPRESA,
    FORMAS_PAGAMENTO,
    FRASE_INSPIRACIONAL,
    SOBRE_ARQUITETA,
    SOBRE_GESTOR,
    formatar_moeda,
    listar_todas_variantes,
    url_portfolio_embed,
)

st.set_page_config(
    page_title="RF Arquitetura — Dashboard de Vendas",
    layout="wide",
    initial_sidebar_state="expanded",
)

NAV_MIGRACAO = {
    "🏠 Início": "Início",
    "📋 Catálogo": "Catálogo",
    "🛒 Carrinho": "Carrinho",
    "💳 Contratar": "Contratar",
    "🛒 Contratar": "Contratar",
    "📊 Dashboard": "Dashboard",
}

CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=Montserrat:wght@300;400;500;600&display=swap');

    :root {
        --rf-escuro: #1f1810;
        --rf-marrom: #5c4a32;
        --rf-dourado: #a67c52;
        --rf-dourado-claro: #c9a06c;
        --rf-creme: #faf6f0;
        --rf-creme-medio: #ede4d6;
    }

    .stApp {
        background: linear-gradient(160deg, #faf6f0 0%, #e8dcc8 100%);
    }

    h1, h2, h3 {
        font-family: 'Cormorant Garamond', serif !important;
        color: var(--rf-escuro) !important;
        font-weight: 700 !important;
    }

    h2, h3 {
        color: var(--rf-marrom) !important;
    }

    p, li, label, .stMarkdown {
        font-family: 'Montserrat', sans-serif !important;
        color: #3d3428;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1f1810 0%, #3d3225 55%, #5c4a32 100%) !important;
        border-right: 3px solid var(--rf-dourado) !important;
    }

    [data-testid="stSidebar"] * {
        color: #faf6f0 !important;
    }

    [data-testid="stSidebar"] .stRadio label {
        font-size: 0.95rem;
        padding: 0.5rem 0.75rem;
        border-radius: 8px;
        transition: background 0.2s;
    }

    [data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(166, 124, 82, 0.35) !important;
    }

    [data-testid="stSidebar"] .stRadio label[data-checked="true"],
    [data-testid="stSidebar"] label:has(input:checked) {
        background: var(--rf-dourado) !important;
        color: #1f1810 !important;
        font-weight: 700 !important;
    }

    .hero-banner {
        background: linear-gradient(120deg, #1f1810 0%, #4a3b28 40%, #8b6340 75%, #c9a06c 100%);
        border-radius: 16px;
        padding: 2.5rem 2rem;
        color: #faf6f0;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(31, 24, 16, 0.35);
        border: 2px solid var(--rf-dourado-claro);
    }

    .hero-banner h1 {
        color: #fff8f0 !important;
        font-size: 2.8rem !important;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 8px rgba(0,0,0,0.25);
    }

    .hero-banner p {
        color: #f0e4d4 !important;
        font-size: 1.1rem;
        margin: 0;
    }

    .card-preco {
        background: linear-gradient(180deg, #ffffff 0%, #faf6f0 100%);
        border-radius: 12px;
        padding: 1.5rem;
        border: 2px solid var(--rf-dourado-claro);
        border-top: 4px solid var(--rf-dourado);
        box-shadow: 0 6px 20px rgba(92, 74, 50, 0.15);
        margin-bottom: 1rem;
        transition: transform 0.2s, box-shadow 0.2s;
    }

    .card-preco:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 28px rgba(166, 124, 82, 0.28);
        border-color: var(--rf-dourado);
    }

    .preco-destaque {
        font-family: 'Cormorant Garamond', serif;
        font-size: 2rem;
        font-weight: 700;
        color: var(--rf-dourado);
    }

    .badge-completo {
        background: linear-gradient(135deg, #1f1810, #5c4a32);
        color: #f5e6d0;
        padding: 0.35rem 0.85rem;
        border-radius: 20px;
        font-size: 0.8rem;
        display: inline-block;
        margin-top: 0.5rem;
        border: 1px solid var(--rf-dourado-claro);
    }

    .metric-box {
        background: linear-gradient(180deg, #ffffff 0%, #f5ebe0 100%);
        border-radius: 12px;
        padding: 1.25rem;
        text-align: center;
        border: 2px solid var(--rf-dourado-claro);
        border-bottom: 4px solid var(--rf-dourado);
        box-shadow: 0 4px 14px rgba(92, 74, 50, 0.12);
    }

    .metric-box .valor {
        font-family: 'Cormorant Garamond', serif;
        font-size: 2rem;
        font-weight: 700;
        color: var(--rf-dourado);
    }

    .metric-box .label {
        font-size: 0.85rem;
        color: var(--rf-marrom);
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }

    .sobre-card {
        background: linear-gradient(135deg, #ffffff 0%, #faf6f0 100%);
        border-radius: 12px;
        padding: 2rem;
        border-left: 5px solid var(--rf-dourado);
        border: 2px solid var(--rf-creme-medio);
        border-left: 5px solid var(--rf-dourado);
        box-shadow: 0 6px 20px rgba(92, 74, 50, 0.12);
        margin-bottom: 1.5rem;
    }

    .sobre-card h3 {
        color: var(--rf-marrom) !important;
    }

    .equipe-bloco {
        display: flex;
        flex-direction: column;
        align-items: center;
        height: 100%;
    }

    .equipe-foto {
        width: 280px;
        height: 350px;
        object-fit: cover;
        object-position: center top;
        border-radius: 12px;
        border: 4px solid var(--rf-dourado);
        box-shadow: 0 8px 24px rgba(166, 124, 82, 0.35);
        display: block;
        margin: 0 auto 0.75rem auto;
    }

    .equipe-legenda {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.9rem;
        color: var(--rf-dourado);
        font-weight: 700;
        text-align: center;
        margin: 0 0 1rem 0;
        line-height: 1.4;
    }

    .equipe-bloco .sobre-card {
        width: 100%;
        text-align: left;
        margin-bottom: 0;
    }

    .frase-inspiracao {
        background: linear-gradient(135deg, #5c4a32 0%, #8b6340 50%, #a67c52 100%);
        border-radius: 12px;
        padding: 2rem 2.5rem;
        box-shadow: 0 8px 28px rgba(92, 74, 50, 0.3);
        margin: 2rem 0;
        text-align: center;
        border: 2px solid var(--rf-dourado-claro);
    }

    .frase-inspiracao p {
        font-family: 'Cormorant Garamond', serif !important;
        font-size: 1.5rem !important;
        font-style: italic;
        color: #fff8f0 !important;
        margin: 0;
        line-height: 1.6;
    }

    .contato-info-card {
        background: linear-gradient(180deg, #ffffff 0%, #faf6f0 100%);
        border-radius: 12px;
        padding: 1.5rem;
        border: 2px solid var(--rf-dourado-claro);
        border-top: 4px solid var(--rf-dourado);
        box-shadow: 0 6px 18px rgba(92, 74, 50, 0.14);
        height: 100%;
    }

    .contato-info-card h4 {
        color: var(--rf-dourado) !important;
        margin-top: 0 !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        border-bottom: 2px solid var(--rf-creme-medio);
        padding-bottom: 0.5rem;
    }

    .contato-info-card a {
        color: var(--rf-marrom);
        text-decoration: none;
        font-weight: 600;
    }

    .contato-info-card a:hover {
        color: var(--rf-dourado);
    }

    .pagamento-card {
        background: linear-gradient(180deg, #ffffff 0%, #f5ebe0 100%);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        border: 2px solid var(--rf-dourado-claro);
        border-bottom: 4px solid var(--rf-dourado);
        height: 100%;
    }

    .pagamento-card h4 {
        color: var(--rf-marrom) !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #a67c52, #7d5e3a) !important;
        color: #fff8f0 !important;
        border: 2px solid #c9a06c !important;
        border-radius: 8px !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700 !important;
        padding: 0.6rem 2rem !important;
        transition: all 0.2s !important;
        box-shadow: 0 4px 14px rgba(125, 94, 58, 0.35) !important;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #c9a06c, #a67c52) !important;
        color: #1f1810 !important;
        box-shadow: 0 6px 18px rgba(166, 124, 82, 0.45) !important;
        transform: translateY(-1px);
    }

    .stButton > button:disabled {
        background: #d4c9b8 !important;
        border-color: #c4b8a8 !important;
        color: #6b5d4d !important;
        box-shadow: none !important;
    }

    a[data-testid="stBaseLinkButton-secondary"] {
        background: linear-gradient(135deg, #5c4a32, #3d3225) !important;
        color: #faf6f0 !important;
        border: 2px solid var(--rf-dourado-claro) !important;
        font-weight: 600 !important;
    }

    .item-lista {
        font-size: 0.9rem;
        color: #4a4035;
        padding: 0.2rem 0;
    }

    .item-lista::before {
        content: "■ ";
        color: var(--rf-dourado);
        font-weight: bold;
        font-size: 0.65rem;
        vertical-align: middle;
    }

    .stTabs [data-baseweb="tab-list"] {
        border-bottom: 3px solid var(--rf-dourado) !important;
        gap: 0.35rem;
    }

    .stTabs [data-baseweb="tab"] {
        background: var(--rf-creme-medio) !important;
        color: var(--rf-marrom) !important;
        border-radius: 8px 8px 0 0 !important;
        font-weight: 600 !important;
        border: 1px solid #d4c9b8 !important;
        border-bottom: none !important;
    }

    .stTabs [aria-selected="true"] {
        background: var(--rf-dourado) !important;
        color: #1f1810 !important;
        border-color: var(--rf-dourado) !important;
    }

    div[data-testid="stMetric"] {
        background: linear-gradient(180deg, #fff 0%, #f5ebe0 100%);
        border: 2px solid var(--rf-dourado-claro);
        border-left: 4px solid var(--rf-dourado);
        border-radius: 10px;
        padding: 0.75rem 1rem;
    }

    div[data-testid="stMetricLabel"] {
        color: var(--rf-marrom) !important;
        font-weight: 600 !important;
    }

    div[data-testid="stMetricValue"] {
        font-family: 'Cormorant Garamond', serif !important;
        color: var(--rf-dourado) !important;
        font-weight: 700 !important;
    }

    [data-testid="stDataFrame"] {
        border: 2px solid var(--rf-dourado);
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 16px rgba(92, 74, 50, 0.12);
    }

    [data-testid="stDataFrame"] div[data-testid="stTable"] {
        font-family: 'Montserrat', sans-serif !important;
    }

    [data-testid="stDataFrame"] div[data-testid="stTable"] th {
        background: linear-gradient(180deg, #3d3225 0%, #5c4a32 100%) !important;
        color: #faf6f0 !important;
        font-weight: 700 !important;
        border-bottom: 3px solid var(--rf-dourado-claro) !important;
    }

    [data-testid="stDataFrame"] div[data-testid="stTable"] td {
        border-bottom: 1px solid var(--rf-creme-medio) !important;
        color: var(--rf-escuro) !important;
    }

    [data-testid="stDataFrame"] div[data-testid="stTable"] tr:nth-child(even) td {
        background-color: #faf6f0 !important;
    }

    [data-testid="stDataFrame"] div[data-testid="stTable"] tr:hover td {
        background-color: #ede4d6 !important;
    }

    [data-testid="stAlert"] {
        border-radius: 10px !important;
        border-left-width: 5px !important;
    }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


def formatar_colunas_moeda(df: pd.DataFrame, colunas: list[str]) -> pd.DataFrame:
    exibicao = df.copy()
    for coluna in colunas:
        if coluna in exibicao.columns:
            exibicao[coluna] = exibicao[coluna].apply(formatar_moeda)
    return exibicao


def criar_df_precos() -> pd.DataFrame:
    dados = []
    for v in listar_todas_variantes():
        dados.append(
            {
                "Categoria": v["categoria"],
                "Pacote": v["nome"],
                "Área": v["area"],
                "Valor Base": v["valor"],
                "Extra Completo": v.get("completo_extra", 0),
                "Valor Completo": v["valor"] + v.get("completo_extra", 0),
                "Personalizado": "Sim" if v.get("personalizado") else "Não",
            }
        )
    return pd.DataFrame(dados)


def exibir_tabela(df: pd.DataFrame):
    st.dataframe(df, use_container_width=True, hide_index=True)


def df_carrinho(carrinho: list) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Categoria": item["categoria"],
                "Pacote": item["variante"],
                "Área": item["area"],
                "Tipo": "Completo" if item.get("projeto_completo") else "Base",
                "Valor": formatar_moeda(valor_item(item)),
            }
            for item in carrinho
        ]
    )


def df_resumo_pedido(carrinho: list) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "#": i,
                "Categoria": proj["categoria"],
                "Pacote": proj["variante"],
                "Área": proj["area"],
                "Tipo": "Completo" if proj.get("projeto_completo") else "Base",
                "Valor": formatar_moeda(valor_item(proj)),
            }
            for i, proj in enumerate(carrinho, 1)
        ]
    )


def init_session():
    defaults = {
        "pagamento_confirmado": False,
        "carrinho": [],
        "forma_pagamento": None,
        "cliente_nome": "",
        "cliente_email": "",
        "cliente_telefone": "",
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

    # migração de versão anterior (carrinho único)
    if st.session_state.get("projeto_selecionado"):
        proj = st.session_state.projeto_selecionado
        proj["projeto_completo"] = st.session_state.get("projeto_completo", False)
        proj["id"] = f"{proj['categoria_id']}_{proj['variante']}_{'comp' if proj['projeto_completo'] else 'base'}"
        if not any(i["id"] == proj["id"] for i in st.session_state.carrinho):
            st.session_state.carrinho.append(proj)
        del st.session_state["projeto_selecionado"]
        if "projeto_completo" in st.session_state:
            del st.session_state["projeto_completo"]


def item_carrinho_id(cat_id: str, idx: int, completo: bool) -> str:
    tipo = "comp" if completo else "base"
    return f"{cat_id}_{idx}_{tipo}"


def valor_item(item: dict) -> float:
    extra = item["completo_extra"] if item.get("projeto_completo") else 0
    return item["valor_base"] + extra


def total_carrinho() -> float:
    return sum(valor_item(i) for i in st.session_state.carrinho)


def adicionar_ao_carrinho(item: dict):
    if not any(i["id"] == item["id"] for i in st.session_state.carrinho):
        st.session_state.carrinho.append(item)
        st.session_state.pagamento_confirmado = False
        return True
    return False


def remover_do_carrinho(item_id: str):
    st.session_state.carrinho = [
        i for i in st.session_state.carrinho if i["id"] != item_id
    ]
    st.session_state.pagamento_confirmado = False


def limpar_carrinho():
    st.session_state.carrinho = []
    st.session_state.pagamento_confirmado = False


def item_no_carrinho(cat_id: str, idx: int, completo: bool) -> bool:
    item_id = item_carrinho_id(cat_id, idx, completo)
    return any(i["id"] == item_id for i in st.session_state.carrinho)


def hero(titulo: str, subtitulo: str = ""):
    html = f"""
    <div class="hero-banner">
        <h1>{titulo}</h1>
        {"<p>" + subtitulo + "</p>" if subtitulo else ""}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def card_preco(variante: dict, categoria: dict, cat_id: str, idx: int):
    valor_total = variante["valor"]
    if variante.get("completo_extra"):
        valor_completo = valor_total + variante["completo_extra"]
    else:
        valor_completo = valor_total

    personalizado = variante.get("personalizado", False)
    nota = variante.get("nota", "")

    st.markdown(
        f"""
        <div class="card-preco">
            <h3 style="margin-top:0;">{variante['nome']}</h3>
            <p style="color:#8b7355; font-weight:600; margin-bottom:0.5rem;">{variante['area']}</p>
            <div class="preco-destaque">{formatar_moeda(valor_total)}</div>
            <p style="font-size:0.85rem; color:#6b5d4d; margin:0.25rem 0;">
                Projeto base com todos os itens inclusos
            </p>
            {f'<span class="badge-completo">Projeto completo: + {formatar_moeda(variante["completo_extra"])} = {formatar_moeda(valor_completo)}</span>' if variante.get("completo_extra") else ""}
            {f'<p style="margin-top:0.75rem; font-style:italic; color:#8b7355;">{nota}</p>' if nota else ""}
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    no_carrinho_base = item_no_carrinho(cat_id, idx, False)
    no_carrinho_comp = item_no_carrinho(cat_id, idx, True)

    with col1:
        label_base = "No carrinho" if no_carrinho_base else "Adicionar ao Carrinho"
        if st.button(label_base, key=f"sel_{cat_id}_{idx}", use_container_width=True, disabled=no_carrinho_base):
            item = {
                "id": item_carrinho_id(cat_id, idx, False),
                "categoria_id": cat_id,
                "categoria": categoria["titulo"],
                "variante": variante["nome"],
                "area": variante["area"],
                "valor_base": variante["valor"],
                "completo_extra": variante.get("completo_extra", 0),
                "projeto_completo": False,
                "personalizado": personalizado,
            }
            if adicionar_ao_carrinho(item):
                st.toast(f"{variante['nome']} adicionado ao carrinho!")
                st.rerun()
    with col2:
        label_comp = "No carrinho" if no_carrinho_comp else "Adicionar Completo"
        if st.button(label_comp, key=f"comp_{cat_id}_{idx}", use_container_width=True, disabled=no_carrinho_comp):
            item = {
                "id": item_carrinho_id(cat_id, idx, True),
                "categoria_id": cat_id,
                "categoria": categoria["titulo"],
                "variante": variante["nome"],
                "area": variante["area"],
                "valor_base": variante["valor"],
                "completo_extra": variante.get("completo_extra", 0),
                "projeto_completo": True,
                "personalizado": personalizado,
            }
            if adicionar_ao_carrinho(item):
                st.toast(f"{variante['nome']} (completo) adicionado!")
                st.rerun()


def conteudo_sobre():
    col1, col2, col3, col4 = st.columns(4)
    variantes = listar_todas_variantes()
    valores = [v["valor"] for v in variantes]

    with col1:
        st.markdown(
            f'<div class="metric-box"><div class="valor">{len(CATEGORIAS)}</div><div class="label">Categorias</div></div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f'<div class="metric-box"><div class="valor">{len(variantes)}</div><div class="label">Pacotes</div></div>',
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f'<div class="metric-box"><div class="valor">{formatar_moeda(min(valores))}</div><div class="label">A partir de</div></div>',
            unsafe_allow_html=True,
        )
    with col4:
        st.markdown(
            '<div class="metric-box"><div class="valor">13+</div><div class="label">Anos de experiência</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    col_esq, col_dir = st.columns(2, gap="large")

    with col_esq:
        st.markdown(
            f"""
            <div class="equipe-bloco">
                <img src="{EMPRESA['foto_arquiteta']}" class="equipe-foto"
                     alt="{EMPRESA['arquiteta']}"/>
                <p class="equipe-legenda">{EMPRESA['arquiteta']}<br>Arquiteta &amp; Urbanista</p>
                <div class="sobre-card">
                    <h3>{EMPRESA['arquiteta']}</h3>
                    <p>{SOBRE_ARQUITETA.strip()}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_dir:
        st.markdown(
            f"""
            <div class="equipe-bloco">
                <img src="{EMPRESA['foto_gestor']}" class="equipe-foto"
                     alt="{EMPRESA['gestor']}"/>
                <p class="equipe-legenda">{EMPRESA['gestor']}<br>Gestão &amp; Acompanhamento de Obras</p>
                <div class="sobre-card">
                    <h3>{EMPRESA['gestor']}</h3>
                    <p>{SOBRE_GESTOR.strip()}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### O que está incluso em cada projeto")
    cols = st.columns(4)
    for i, (cat_id, cat) in enumerate(CATEGORIAS.items()):
        with cols[i]:
            st.markdown(f"**{cat['titulo']}**")
            for item in cat["itens"]:
                st.markdown(f'<p class="item-lista">{item}</p>', unsafe_allow_html=True)

    st.markdown(
        f'<div class="frase-inspiracao"><p>&ldquo;{FRASE_INSPIRACIONAL}&rdquo;</p></div>',
        unsafe_allow_html=True,
    )


def conteudo_contato():
    st.markdown("## Contato")
    st.markdown(
        "Entre em contato com a **RF Arquitetura & Interiores**. "
        "Teremos prazer em transformar seus sonhos em realidade."
    )

    col_logo, col_info = st.columns([1, 3])
    with col_logo:
        st.image(EMPRESA["logo"], width=140)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
            <div class="contato-info-card">
                <h4>Telefones</h4>
                <p><a href="tel:+{CONTATO['telefone_1_raw']}">{CONTATO['telefone_1']}</a></p>
                <p><a href="tel:+{CONTATO['telefone_2_raw']}">{CONTATO['telefone_2']}</a></p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="contato-info-card">
                <h4>E-mail</h4>
                <p><a href="mailto:{CONTATO['email']}">{CONTATO['email']}</a></p>
                <p style="margin-top:0.75rem;"><a href="https://wa.me/{EMPRESA['whatsapp']}" target="_blank">WhatsApp</a></p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    st.markdown("### Envie sua mensagem")

    with st.form("form_contato", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            nome = st.text_input("Nome", placeholder="Seu nome")
        with c2:
            sobrenome = st.text_input("Sobrenome", placeholder="Seu sobrenome")
        email = st.text_input("E-mail", placeholder="seu@email.com")
        mensagem = st.text_area("Mensagem", placeholder="Como podemos ajudar?", height=150)
        enviado = st.form_submit_button("Enviar", use_container_width=True)

    if enviado:
        if nome.strip() and email.strip() and mensagem.strip():
            nome_completo = f"{nome} {sobrenome}".strip()
            assunto = f"Contato pelo site - {nome_completo}"
            corpo = (
                f"Nome: {nome_completo}%0A"
                f"E-mail: {email}%0A%0A"
                f"Mensagem:%0A{mensagem.replace(chr(10), '%0A')}"
            )
            mailto = (
                f"mailto:{CONTATO['email']}?subject={assunto.replace(' ', '%20')}&body={corpo}"
            )
            st.success("Obrigada pelo envio! Clique abaixo para enviar pelo seu e-mail.")
            st.link_button("Abrir e-mail para enviar", mailto, use_container_width=True)

            whatsapp_msg = (
                f"Olá! Meu nome é {nome_completo}.%0A%0A{mensagem.replace(chr(10), '%0A')}"
            )
            st.link_button(
                "Enviar pelo WhatsApp",
                f"https://wa.me/{EMPRESA['whatsapp']}?text={whatsapp_msg}",
                use_container_width=True,
            )
        else:
            st.error("Preencha nome, e-mail e mensagem para enviar.")

    st.markdown("---")
    st.link_button(
        "Visitar página de contato no site",
        EMPRESA["contato_url"],
        use_container_width=True,
    )


def conteudo_portfolio():
    st.markdown(
        """
        **Portfólio Rachel Fernandes** — projetos residenciais, comerciais e de interiores.
        Navegue pelas páginas abaixo para conhecer nossos trabalhos.
        """
    )

    col1, col2 = st.columns([3, 1])
    with col2:
        st.link_button(
            "Abrir no Canva",
            EMPRESA["portfolio"],
            use_container_width=True,
        )
        st.link_button(
            "Visitar Site",
            EMPRESA["site"],
            use_container_width=True,
        )

    st.markdown("---")

    embed_url = url_portfolio_embed()

    if hasattr(st, "iframe"):
        st.iframe(embed_url, height=750)
    else:
        st.components.v1.iframe(
            src=embed_url,
            height=750,
            scrolling=True,
        )

    st.info(
        "Use as setas do portfólio para ver todas as imagens. "
        "Se não carregar, clique em **Abrir no Canva**."
    )


def pagina_inicio():
    hero(
        "RF Arquitetura & Interiores",
        "Projetos 100% personalizados — do conceito à execução",
    )

    tab_sobre, tab_portfolio, tab_contato = st.tabs(
        ["Sobre", "Portfólio", "Contato"]
    )

    with tab_sobre:
        conteudo_sobre()

    with tab_portfolio:
        conteudo_portfolio()

    with tab_contato:
        conteudo_contato()


def pagina_catalogo():
    hero("Catálogo de Projetos", "Escolha um ou mais pacotes e adicione ao carrinho")

    qtd = len(st.session_state.carrinho)
    if qtd > 0:
        col_info, col_btn = st.columns([3, 1])
        with col_info:
            st.success(f"Você tem **{qtd}** projeto(s) no carrinho — Total: **{formatar_moeda(total_carrinho())}**")
        with col_btn:
            if st.button("Ver Carrinho", use_container_width=True, key="catalogo_ver_carrinho"):
                st.session_state.nav_page = "Carrinho"
                st.rerun()

    tabs = st.tabs([cat["titulo"] for cat in CATEGORIAS.values()])

    for tab, (cat_id, cat) in zip(tabs, CATEGORIAS.items()):
        with tab:
            st.markdown(f"*{cat['descricao']}*")
            st.markdown("**Itens inclusos:**")
            cols_itens = st.columns(2)
            metade = len(cat["itens"]) // 2 + len(cat["itens"]) % 2
            with cols_itens[0]:
                for item in cat["itens"][:metade]:
                    st.markdown(f'<p class="item-lista">{item}</p>', unsafe_allow_html=True)
            with cols_itens[1]:
                for item in cat["itens"][metade:]:
                    st.markdown(f'<p class="item-lista">{item}</p>', unsafe_allow_html=True)

            st.markdown("---")
            cols = st.columns(min(len(cat["variantes"]), 3))
            for idx, var in enumerate(cat["variantes"]):
                with cols[idx % len(cols)]:
                    card_preco(var, cat, cat_id, idx)


def pagina_carrinho():
    hero("Carrinho", "Revise os projetos selecionados antes de finalizar")

    if not st.session_state.carrinho:
        st.warning("Seu carrinho está vazio. Vá ao **Catálogo** e adicione um ou mais projetos.")
        if st.button("Ir para o Catálogo", use_container_width=True, key="carrinho_ir_catalogo_vazio"):
            st.session_state.nav_page = "Catálogo"
            st.rerun()
        return

    st.markdown(f"### {len(st.session_state.carrinho)} projeto(s) selecionado(s)")

    exibir_tabela(df_carrinho(st.session_state.carrinho))

    st.markdown("**Remover projeto do carrinho:**")
    opcoes = {
        f"{item['categoria']} — {item['variante']} ({formatar_moeda(valor_item(item))})": item["id"]
        for item in st.session_state.carrinho
    }
    col_rm, col_btn = st.columns([3, 1])
    with col_rm:
        item_remover = st.selectbox(
            "Selecione o projeto",
            options=list(opcoes.keys()),
            label_visibility="collapsed",
        )
    with col_btn:
        if st.button("Remover", use_container_width=True, key="carrinho_remover"):
            remover_do_carrinho(opcoes[item_remover])
            st.toast("Projeto removido do carrinho")
            st.rerun()

    st.markdown("---")

    col_total, col_acoes = st.columns([2, 1])
    total = total_carrinho()

    with col_total:
        st.markdown(f"### Total: {formatar_moeda(total)}")
        st.caption(f"Parcelamento em 12x: {formatar_moeda(total / 12)}/mês no cartão")

    with col_acoes:
        if st.button("Finalizar Pedido", use_container_width=True, type="primary", key="carrinho_finalizar"):
            st.session_state.nav_page = "Contratar"
            st.rerun()
        if st.button("Limpar Carrinho", use_container_width=True, key="carrinho_limpar"):
            limpar_carrinho()
            st.rerun()
        if st.button("Adicionar mais", use_container_width=True, key="carrinho_adicionar"):
            st.session_state.nav_page = "Catálogo"
            st.rerun()


def pagina_vendas():
    hero("Contratar Projeto", "Finalize o pagamento dos projetos do seu carrinho")

    if not st.session_state.carrinho:
        st.warning("Nenhum projeto no carrinho. Vá ao **Catálogo** e escolha os pacotes.")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Ir para o Catálogo", use_container_width=True, key="vendas_ir_catalogo"):
                st.session_state.nav_page = "Catálogo"
                st.rerun()
        with c2:
            if st.button("Ver Carrinho", use_container_width=True, key="vendas_ver_carrinho"):
                st.session_state.nav_page = "Carrinho"
                st.rerun()
        return

    valor_total = total_carrinho()

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### Resumo do Pedido")
        exibir_tabela(df_resumo_pedido(st.session_state.carrinho))

        if st.button("Editar carrinho", key="vendas_editar_carrinho"):
            st.session_state.nav_page = "Carrinho"
            st.rerun()

    with col2:
        st.markdown("### Valores")
        for proj in st.session_state.carrinho:
            st.metric(
                f"{proj['variante']}",
                formatar_moeda(valor_item(proj)),
            )
        st.metric("TOTAL", formatar_moeda(valor_total))

        st.markdown("---")
        st.markdown("**Parcelamento (cartão 12x):**")
        parcela = valor_total / 12
        st.markdown(f"### {formatar_moeda(parcela)}/mês")

    st.markdown("---")
    st.markdown("### Seus Dados")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.session_state.cliente_nome = st.text_input(
            "Nome completo", value=st.session_state.cliente_nome
        )
    with c2:
        st.session_state.cliente_email = st.text_input(
            "E-mail", value=st.session_state.cliente_email
        )
    with c3:
        st.session_state.cliente_telefone = st.text_input(
            "Telefone / WhatsApp", value=st.session_state.cliente_telefone
        )

    st.markdown("---")
    st.markdown("### Forma de Pagamento")

    cols_pag = st.columns(3)
    for i, fp in enumerate(FORMAS_PAGAMENTO):
        with cols_pag[i]:
            st.markdown(
                f"""
                <div class="pagamento-card">
                    <h4 style="margin:0.5rem 0;">{fp['nome']}</h4>
                    <p style="font-size:0.85rem; color:#6b5d4d;">{fp['descricao']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    forma = st.radio(
        "Selecione a forma de pagamento:",
        [fp["nome"] for fp in FORMAS_PAGAMENTO],
        horizontal=True,
        key="forma_pag_radio",
    )
    st.session_state.forma_pagamento = forma

    st.markdown("---")

    dados_ok = (
        st.session_state.cliente_nome.strip()
        and st.session_state.cliente_email.strip()
        and st.session_state.cliente_telefone.strip()
    )

    if st.button(
        f"Confirmar Pagamento — {formatar_moeda(valor_total)}",
        use_container_width=True,
        disabled=not dados_ok,
        key="vendas_confirmar_pagamento",
    ):
        st.session_state.pagamento_confirmado = True
        st.balloons()
        st.rerun()

    if not dados_ok:
        st.caption("Preencha todos os dados para confirmar o pagamento.")

    if st.session_state.pagamento_confirmado:
        st.success("Pagamento confirmado com sucesso!")
        st.markdown(
            f"""
            ### Próximo passo: fale com nosso time de arquitetura!

            Agora que seu pagamento foi confirmado, entre em contato com a **{EMPRESA['arquiteta']}**
            pelo WhatsApp para iniciar o briefing do seu projeto personalizado.
            """
        )

        projetos_msg = "%0A".join(
            f"• {p['categoria']} — {p['variante']} ({p['area']}) — "
            f"{'Completo' if p.get('projeto_completo') else 'Base'} — {formatar_moeda(valor_item(p))}"
            for p in st.session_state.carrinho
        )
        whatsapp_msg = (
            f"Olá! Acabei de contratar projeto(s) pela plataforma.%0A%0A"
            f"*Nome:* {st.session_state.cliente_nome}%0A"
            f"*Projetos:*%0A{projetos_msg}%0A%0A"
            f"*Total:* {formatar_moeda(valor_total)}%0A"
            f"*Pagamento:* {st.session_state.forma_pagamento}"
        )
        whatsapp_url = f"https://wa.me/{EMPRESA['whatsapp']}?text={whatsapp_msg}"

        st.link_button(
            "Conversar no WhatsApp",
            whatsapp_url,
            use_container_width=True,
        )

        st.info(
            "**Importante:** O WhatsApp só é disponibilizado após a confirmação do pagamento, "
            "conforme nossa política de atendimento."
        )


def pagina_dashboard():
    hero("Dashboard de Vendas", "Visão geral dos pacotes e valores")

    df = criar_df_precos()
    df_exibicao = formatar_colunas_moeda(
        df, ["Valor Base", "Extra Completo", "Valor Completo"]
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Pacotes", len(df))
    with col2:
        st.metric("Ticket Médio (Base)", formatar_moeda(df["Valor Base"].mean()))
    with col3:
        st.metric("Ticket Médio (Completo)", formatar_moeda(df["Valor Completo"].mean()))

    st.markdown("### Tabela de Preços Completa")
    exibir_tabela(df_exibicao)

    st.markdown("### Valores por Categoria")
    chart_data = df.groupby("Categoria")[["Valor Base", "Valor Completo"]].mean()
    chart_data.columns = ["Valor Base (médio)", "Valor Completo (médio)"]
    st.bar_chart(chart_data)

    st.markdown("### Exportar")
    csv = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "Baixar tabela CSV",
        csv,
        "rf_arquitetura_precos.csv",
        "text/csv",
        use_container_width=True,
    )


def main():
    init_session()

    with st.sidebar:
        st.markdown("## RF Arquitetura")
        st.markdown("*Interiores & Projetos*")
        st.markdown("---")

        paginas = {
            "Início": pagina_inicio,
            "Catálogo": pagina_catalogo,
            "Carrinho": pagina_carrinho,
            "Contratar": pagina_vendas,
            "Dashboard": pagina_dashboard,
        }

        if "nav_page" not in st.session_state:
            st.session_state.nav_page = "Início"

        pagina_keys = list(paginas.keys())
        if st.session_state.nav_page not in pagina_keys:
            st.session_state.nav_page = NAV_MIGRACAO.get(
                st.session_state.nav_page, "Início"
            )
        if st.session_state.nav_page not in pagina_keys:
            st.session_state.nav_page = "Início"

        pagina = st.radio(
            "Navegação",
            pagina_keys,
            index=pagina_keys.index(st.session_state.nav_page),
            label_visibility="collapsed",
        )
        st.session_state.nav_page = pagina

        st.markdown("---")

        qtd = len(st.session_state.carrinho)
        if qtd > 0:
            st.markdown(f"**Carrinho ({qtd})**")
            for item in st.session_state.carrinho:
                st.markdown(
                    f"· {item['categoria']} — {item['variante']}  \n"
                    f"&nbsp;&nbsp;{formatar_moeda(valor_item(item))}"
                )
            st.markdown(f"**Total: {formatar_moeda(total_carrinho())}**")
            if st.button("Ver Carrinho", use_container_width=True, key="sidebar_ver_carrinho"):
                st.session_state.nav_page = "Carrinho"
                st.rerun()
            if st.button("Finalizar Pedido", use_container_width=True, key="sidebar_finalizar"):
                st.session_state.nav_page = "Contratar"
                st.rerun()
        else:
            st.caption("Carrinho vazio")

        st.markdown("---")
        st.caption(f"© 2026 {EMPRESA['nome']}")

    paginas[st.session_state.nav_page]()


if __name__ == "__main__":
    main()
