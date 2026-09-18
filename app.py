import importlib
import json
import os
import random
import re
import uuid
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

import pandas as pd
import streamlit as st

import database

importlib.reload(database)

_BASE_DIR_APP = Path(__file__).parent

from database import (
    ITENS_PROJETO_COMPLETO_EXTRA,
    ITENS_PROJETO_INTERIORES,
    PROJETOS_PRONTOS_IMG_DIR,
    carregar_compras,
    carregar_projetos_prontos,
    formatar_moeda,
    foto_src,
    get_categorias,
    get_empresa,
    get_frase_inspiracional,
    get_sobre_arquiteta,
    get_sobre_gestor,
    get_sobre_rita,
    itens_projeto_simples,
    listar_todas_variantes,
    registrar_compra,
    salvar_categoria_texto,
    salvar_empresa_overrides,
    salvar_projetos_prontos,
    salvar_textos_overrides,
    salvar_variante_override,
    url_portfolio_embed,
)

CATEGORIAS = get_categorias()
EMPRESA = get_empresa()
FRASE_INSPIRACIONAL = get_frase_inspiracional()
SOBRE_ARQUITETA = get_sobre_arquiteta()
SOBRE_GESTOR = get_sobre_gestor()
SOBRE_RITA = get_sobre_rita()


def senha_admin() -> str:
    try:
        valor = st.secrets.get("ADMIN_PASSWORD")
    except Exception:
        valor = None
    return valor or os.environ.get("ADMIN_PASSWORD") or "1234"


def eh_arquiteta() -> bool:
    return st.session_state.get("papel") == "arquiteta"


st.set_page_config(
    page_title="RF Arquitetura & Interiores",
    page_icon=EMPRESA["logo"],
    layout="wide",
    initial_sidebar_state="auto",
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

    /* Área principal: texto escuro em fundo claro */
    [data-testid="stAppViewContainer"] [data-testid="stMain"],
    [data-testid="stAppViewContainer"] [data-testid="stMain"] p,
    [data-testid="stAppViewContainer"] [data-testid="stMain"] li,
    [data-testid="stAppViewContainer"] [data-testid="stMain"] label,
    [data-testid="stAppViewContainer"] [data-testid="stMain"] .stMarkdown,
    [data-testid="stAppViewContainer"] [data-testid="stMain"] [data-testid="stCaptionContainer"] {
        color: #3d3428 !important;
    }

    /* Botões e links: texto claro no fundo escuro/dourado */
    [data-testid="stAppViewContainer"] [data-testid="stMain"] .stButton > button,
    [data-testid="stAppViewContainer"] [data-testid="stMain"] .stButton > button p,
    [data-testid="stAppViewContainer"] [data-testid="stMain"] .stButton > button span,
    [data-testid="stAppViewContainer"] [data-testid="stMain"] a[data-testid="stBaseLinkButton-secondary"],
    [data-testid="stAppViewContainer"] [data-testid="stMain"] a[data-testid="stBaseLinkButton-secondary"] p,
    [data-testid="stAppViewContainer"] [data-testid="stMain"] a[data-testid="stBaseLinkButton-secondary"] span {
        color: #fff8f0 !important;
    }

    [data-testid="stAppViewContainer"] [data-testid="stMain"] .stButton > button:hover,
    [data-testid="stAppViewContainer"] [data-testid="stMain"] .stButton > button:hover p,
    [data-testid="stAppViewContainer"] [data-testid="stMain"] .stButton > button:hover span {
        color: #1f1810 !important;
    }

    [data-testid="stAppViewContainer"] [data-testid="stMain"] .stButton > button:disabled,
    [data-testid="stAppViewContainer"] [data-testid="stMain"] .stButton > button:disabled p,
    [data-testid="stAppViewContainer"] [data-testid="stMain"] .stButton > button:disabled span {
        color: #6b5d4d !important;
    }

    [data-testid="stAppViewContainer"] [data-testid="stMain"] h1,
    [data-testid="stAppViewContainer"] [data-testid="stMain"] h2,
    [data-testid="stAppViewContainer"] [data-testid="stMain"] h3 {
        color: var(--rf-escuro) !important;
    }

    [data-testid="stAppViewContainer"] [data-testid="stMain"] h2,
    [data-testid="stAppViewContainer"] [data-testid="stMain"] h3 {
        color: var(--rf-marrom) !important;
    }

    [data-testid="stAppViewContainer"] [data-testid="stMain"] .hero-banner h1,
    [data-testid="stAppViewContainer"] [data-testid="stMain"] .hero-banner p,
    [data-testid="stAppViewContainer"] [data-testid="stMain"] .frase-inspiracao p,
    [data-testid="stAppViewContainer"] [data-testid="stMain"] .badge-completo {
        color: #fff8f0 !important;
    }

    [data-testid="stAppViewContainer"] [data-testid="stMain"] .hero-banner p {
        color: #f0e4d4 !important;
    }

    [data-testid="stAppViewContainer"] [data-testid="stMain"] input,
    [data-testid="stAppViewContainer"] [data-testid="stMain"] textarea,
    [data-testid="stAppViewContainer"] [data-testid="stMain"] [data-baseweb="select"] {
        color: #1f1810 !important;
    }

    /* Sidebar: fundo escuro → texto claro (exceto itens com fundo claro/dourado) */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1f1810 0%, #3d3225 55%, #5c4a32 100%) !important;
        border-right: 3px solid var(--rf-dourado) !important;
        color: #faf6f0 !important;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"],
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
        color: #faf6f0 !important;
    }

    [data-testid="stSidebar"] .stRadio label {
        font-size: 0.95rem;
        padding: 0.5rem 0.75rem;
        border-radius: 8px;
        transition: background 0.2s;
        color: #faf6f0 !important;
    }

    [data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(166, 124, 82, 0.35) !important;
        color: #faf6f0 !important;
    }

    [data-testid="stSidebar"] .stRadio label[data-checked="true"],
    [data-testid="stSidebar"] .stRadio label:has(input:checked) {
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
        padding: 1.25rem 1.5rem;
        border: 2px solid var(--rf-dourado-claro);
        border-top: 4px solid var(--rf-dourado);
        box-shadow: 0 6px 20px rgba(92, 74, 50, 0.15);
        margin-bottom: 0.5rem;
        transition: transform 0.2s, box-shadow 0.2s;
        color: #3d3428;
        min-height: 9.5rem;
        display: flex;
        flex-direction: column;
        justify-content: center;
        text-align: center;
    }

    .card-preco h3 {
        color: var(--rf-marrom) !important;
        margin-bottom: 0.35rem !important;
    }

    .card-preco .card-area {
        color: #8b7355 !important;
        font-weight: 600;
        margin: 0 0 0.5rem 0;
        font-size: 0.95rem;
    }

    .card-preco .card-subtitulo {
        font-size: 0.85rem;
        color: #6b5d4d !important;
        margin: 0.35rem 0 0 0;
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

    .card-preco-botoes {
        margin-top: 0.25rem;
        margin-bottom: 1.25rem;
    }

    div[data-testid="stMarkdownContainer"]:has(.card-preco) ~ div .stButton > button {
        min-height: 2.85rem;
        font-size: 0.9rem !important;
        line-height: 1.3 !important;
        white-space: normal !important;
        margin-bottom: 0.35rem;
    }

    div[data-testid="stMarkdownContainer"]:has(.btn-completo-wrap) + div .stButton > button,
    div[data-testid="stMarkdownContainer"]:has(.btn-completo-wrap) + div .stButton > button p,
    div[data-testid="stMarkdownContainer"]:has(.btn-completo-wrap) + div .stButton > button span {
        background: linear-gradient(135deg, #1f1810, #5c4a32) !important;
        color: #fff8f0 !important;
        border: 2px solid var(--rf-dourado-claro) !important;
        box-shadow: 0 4px 14px rgba(31, 24, 16, 0.35) !important;
    }

    div[data-testid="stMarkdownContainer"]:has(.btn-completo-wrap) + div .stButton > button:hover,
    div[data-testid="stMarkdownContainer"]:has(.btn-completo-wrap) + div .stButton > button:hover p,
    div[data-testid="stMarkdownContainer"]:has(.btn-completo-wrap) + div .stButton > button:hover span {
        background: linear-gradient(135deg, #5c4a32, #8b6340) !important;
        color: #fff8f0 !important;
    }

    div[data-testid="stMarkdownContainer"]:has(.btn-completo-wrap) + div .stButton > button:disabled,
    div[data-testid="stMarkdownContainer"]:has(.btn-completo-wrap) + div .stButton > button:disabled p,
    div[data-testid="stMarkdownContainer"]:has(.btn-completo-wrap) + div .stButton > button:disabled span {
        background: #8b7355 !important;
        color: #f5ebe0 !important;
        border-color: #a67c52 !important;
        opacity: 0.85;
    }

    div[data-testid="stMarkdownContainer"]:has(.btn-interiores-wrap) + div .stButton > button,
    div[data-testid="stMarkdownContainer"]:has(.btn-interiores-wrap) + div .stButton > button p,
    div[data-testid="stMarkdownContainer"]:has(.btn-interiores-wrap) + div .stButton > button span {
        background: linear-gradient(135deg, #7d5e3a, #a67c52) !important;
        color: #fff8f0 !important;
        border: 2px solid #c9a06c !important;
        box-shadow: 0 4px 14px rgba(125, 94, 58, 0.3) !important;
    }

    div[data-testid="stMarkdownContainer"]:has(.btn-interiores-wrap) + div .stButton > button:hover,
    div[data-testid="stMarkdownContainer"]:has(.btn-interiores-wrap) + div .stButton > button:hover p,
    div[data-testid="stMarkdownContainer"]:has(.btn-interiores-wrap) + div .stButton > button:hover span {
        background: linear-gradient(135deg, #a67c52, #c9a06c) !important;
        color: #1f1810 !important;
    }

    div[data-testid="stMarkdownContainer"]:has(.btn-interiores-wrap) + div .stButton > button:disabled,
    div[data-testid="stMarkdownContainer"]:has(.btn-interiores-wrap) + div .stButton > button:disabled p,
    div[data-testid="stMarkdownContainer"]:has(.btn-interiores-wrap) + div .stButton > button:disabled span {
        background: #c4b8a8 !important;
        color: #6b5d4d !important;
        border-color: #b8aa98 !important;
        opacity: 0.9;
    }

    .btn-completo-wrap,
    .btn-interiores-wrap {
        display: none;
    }

    div[data-testid="stTabs"] div[data-testid="stHorizontalBlock"] {
        align-items: flex-start !important;
        gap: 1.25rem !important;
    }

    div[data-testid="stTabs"] div[data-testid="column"] {
        display: flex;
        flex-direction: column;
    }

    .catalogo-pacote-botoes {
        width: 100%;
        margin-bottom: 1.5rem;
    }

    .metric-box {
        background: linear-gradient(180deg, #ffffff 0%, #f5ebe0 100%);
        border-radius: 12px;
        padding: 1.25rem;
        text-align: center;
        border: 2px solid var(--rf-dourado-claro);
        border-bottom: 4px solid var(--rf-dourado);
        box-shadow: 0 4px 14px rgba(92, 74, 50, 0.12);
        color: #3d3428;
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
        color: #3d3428;
    }

    .sobre-card h3 {
        color: var(--rf-marrom) !important;
    }

    .sobre-card p {
        color: #4a4035 !important;
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

    .badge-papel {
        padding: 0.6rem 0.75rem;
        border-radius: 8px;
        font-weight: 700;
        font-size: 0.85rem;
        text-align: center;
        margin-bottom: 0.75rem;
    }

    .badge-papel-arquiteta {
        background: linear-gradient(135deg, #1f1810, #5c4a32);
        color: #f5e6d0;
        border: 1px solid var(--rf-dourado);
        box-shadow: 0 4px 14px rgba(31, 24, 16, 0.3);
    }

    .badge-papel-cliente {
        background: var(--rf-creme-medio);
        color: var(--rf-marrom);
        border: 1px solid var(--rf-dourado-claro);
    }

    .card-projeto-pronto {
        background: linear-gradient(180deg, #ffffff 0%, #faf6f0 100%);
        border-radius: 12px;
        overflow: hidden;
        border: 2px solid var(--rf-dourado-claro);
        box-shadow: 0 6px 20px rgba(92, 74, 50, 0.15);
        margin-bottom: 1.25rem;
        transition: transform 0.2s, box-shadow 0.2s;
    }

    .card-projeto-pronto:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 28px rgba(166, 124, 82, 0.28);
    }

    .pix-box {
        background: linear-gradient(180deg, #ffffff 0%, #f5ebe0 100%);
        border: 2px dashed var(--rf-dourado);
        border-radius: 10px;
        padding: 1rem 1.25rem;
        margin: 0.75rem 0;
        text-align: center;
    }

    .pix-box p {
        margin: 0.2rem 0;
        color: #6b5d4d !important;
    }

    .pix-chave {
        font-family: 'Courier New', monospace;
        font-size: 1.1rem !important;
        font-weight: 700;
        color: var(--rf-marrom) !important;
        word-break: break-all;
    }

    .card-projeto-pronto img {
        width: 100%;
        aspect-ratio: 4 / 3;
        object-fit: cover;
        display: block;
    }

    .card-projeto-pronto .corpo {
        padding: 1rem 1.25rem 1.25rem;
    }

    .card-projeto-pronto h3 {
        margin: 0 0 0.4rem 0 !important;
        color: var(--rf-marrom) !important;
    }

    .card-projeto-pronto p {
        color: #4a4035 !important;
        font-size: 0.92rem;
        margin: 0;
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
        color: #fff8f0;
    }

    .frase-inspiracao p {
        font-family: 'Cormorant Garamond', serif !important;
        font-size: 1.5rem !important;
        font-style: italic;
        color: #fff8f0 !important;
        margin: 0;
        line-height: 1.6;
    }

    .pagamento-card {
        background: linear-gradient(180deg, #ffffff 0%, #f5ebe0 100%);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        border: 2px solid var(--rf-dourado-claro);
        border-bottom: 4px solid var(--rf-dourado);
        height: 100%;
        color: #3d3428;
    }

    .pagamento-card h4 {
        color: var(--rf-marrom) !important;
    }

    .pagamento-card p {
        color: #6b5d4d !important;
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

    .balao-projetos {
        position: relative;
        background: linear-gradient(135deg, #ffffff 0%, #faf6f0 100%);
        border: 2px solid var(--rf-dourado-claro);
        border-left: 5px solid var(--rf-dourado);
        border-radius: 16px;
        padding: 1.5rem 1.75rem 1.25rem;
        margin-bottom: 1.75rem;
        box-shadow: 0 8px 24px rgba(92, 74, 50, 0.14);
    }

    .balao-projetos::after {
        content: "";
        position: absolute;
        bottom: -12px;
        left: 48px;
        width: 22px;
        height: 22px;
        background: #faf6f0;
        border-right: 2px solid var(--rf-dourado-claro);
        border-bottom: 2px solid var(--rf-dourado-claro);
        transform: rotate(45deg);
    }

    .balao-projetos-titulo {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.35rem;
        font-weight: 700;
        color: var(--rf-marrom);
        margin: 0 0 1rem 0;
    }

    .balao-projetos-colunas {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 1.25rem;
    }

    @media (max-width: 992px) {
        .balao-projetos-colunas {
            grid-template-columns: 1fr;
        }
    }

    .balao-coluna h4 {
        font-family: 'Cormorant Garamond', serif !important;
        color: var(--rf-dourado) !important;
        font-size: 1.15rem !important;
        margin: 0 0 0.5rem 0 !important;
    }

    .balao-coluna p {
        font-size: 0.85rem;
        color: #8b7355 !important;
        margin: 0 0 0.5rem 0 !important;
        font-style: italic;
    }

    .balao-coluna ul {
        margin: 0;
        padding-left: 1.1rem;
        list-style: none;
    }

    .balao-coluna li {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.88rem;
        color: #4a4035 !important;
        padding: 0.2rem 0;
        line-height: 1.45;
    }

    .balao-coluna li::before {
        content: "✓ ";
        color: var(--rf-dourado);
        font-weight: 700;
    }

    .balao-coluna-extra li::before {
        content: "+ ";
        color: var(--rf-dourado);
        font-weight: 700;
    }

    .balao-coluna-interiores li::before {
        content: "◆ ";
        color: var(--rf-dourado);
        font-weight: 700;
    }

    .balao-nota-3d {
        font-size: 0.8rem;
        color: #8b7355 !important;
        margin-top: 0.75rem !important;
        font-style: italic;
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

    .stTabs [aria-selected="true"] p,
    .stTabs [aria-selected="true"] span {
        color: #1f1810 !important;
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

    /* Página Contratar Projeto */
    [data-testid="stAppViewContainer"] [data-testid="stMain"] .secao-contratar h3,
    [data-testid="stAppViewContainer"] [data-testid="stMain"] .secao-contratar h4 {
        color: var(--rf-marrom) !important;
        font-weight: 600 !important;
    }

    [data-testid="stAppViewContainer"] [data-testid="stMain"] .secao-contratar p,
    [data-testid="stAppViewContainer"] [data-testid="stMain"] .secao-contratar label,
    [data-testid="stAppViewContainer"] [data-testid="stMain"] .secao-contratar .stMarkdown p {
        color: #6b5d4d !important;
    }

    [data-testid="stAppViewContainer"] [data-testid="stMain"] .bloco-valores-contratar [data-testid="stMetric"] {
        background: linear-gradient(180deg, #fff 0%, #f5ebe0 100%);
    }

    [data-testid="stAppViewContainer"] [data-testid="stMain"] .bloco-valores-contratar [data-testid="stMetricLabel"],
    [data-testid="stAppViewContainer"] [data-testid="stMain"] .bloco-valores-contratar [data-testid="stMetricLabel"] p,
    [data-testid="stAppViewContainer"] [data-testid="stMain"] .bloco-valores-contratar [data-testid="stMetricLabel"] span {
        color: #8b7355 !important;
        font-weight: 600 !important;
    }

    [data-testid="stAppViewContainer"] [data-testid="stMain"] .bloco-valores-contratar [data-testid="stMetricValue"],
    [data-testid="stAppViewContainer"] [data-testid="stMain"] .bloco-valores-contratar [data-testid="stMetricValue"] p,
    [data-testid="stAppViewContainer"] [data-testid="stMain"] .bloco-valores-contratar [data-testid="stMetricValue"] span {
        color: var(--rf-dourado) !important;
        font-weight: 700 !important;
    }

    [data-testid="stAppViewContainer"] [data-testid="stMain"] .parcela-destaque {
        font-family: 'Cormorant Garamond', serif !important;
        font-size: 1.75rem !important;
        font-weight: 700 !important;
        color: var(--rf-dourado) !important;
        margin: 0.25rem 0 0 0 !important;
    }

    [data-testid="stAppViewContainer"] [data-testid="stMain"] .bloco-pagamento-contratar .pagamento-card h4 {
        color: var(--rf-dourado) !important;
    }

    [data-testid="stAppViewContainer"] [data-testid="stMain"] .bloco-pagamento-contratar .pagamento-card p {
        color: #8b7355 !important;
    }

    [data-testid="stAppViewContainer"] [data-testid="stMain"] .bloco-pagamento-contratar .stRadio > label {
        color: var(--rf-marrom) !important;
        font-weight: 600 !important;
    }

    [data-testid="stAppViewContainer"] [data-testid="stMain"] .bloco-pagamento-contratar .stRadio [data-baseweb="radio"] label,
    [data-testid="stAppViewContainer"] [data-testid="stMain"] .bloco-pagamento-contratar .stRadio label {
        color: #6b5d4d !important;
        background: #faf6f0 !important;
        border: 1px solid var(--rf-creme-medio) !important;
        border-radius: 8px !important;
        padding: 0.45rem 0.85rem !important;
        margin-right: 0.35rem !important;
    }

    [data-testid="stAppViewContainer"] [data-testid="stMain"] .bloco-pagamento-contratar .stRadio label:has(input:checked) {
        background: var(--rf-dourado) !important;
        color: #fff8f0 !important;
        border-color: var(--rf-dourado-claro) !important;
        font-weight: 700 !important;
    }

    [data-testid="stAppViewContainer"] [data-testid="stMain"] .bloco-dados-contratar label {
        color: #8b7355 !important;
        font-weight: 500 !important;
    }

    [data-testid="stAppViewContainer"] [data-testid="stMain"] .bloco-dados-contratar input {
        color: #4a4035 !important;
        background-color: #fff !important;
    }

    /* Android e iOS — layout responsivo */
    @media (max-width: 768px) {
        [data-testid="stMain"] .block-container {
            padding-left: 0.85rem !important;
            padding-right: 0.85rem !important;
            padding-top: 1rem !important;
            max-width: 100% !important;
        }

        [data-testid="stHorizontalBlock"] {
            flex-direction: column !important;
            gap: 0.5rem !important;
        }

        [data-testid="column"] {
            width: 100% !important;
            min-width: 100% !important;
            flex: 1 1 100% !important;
        }

        .hero-banner {
            padding: 1.35rem 1rem !important;
            margin-bottom: 1.25rem !important;
        }

        .hero-banner h1 {
            font-size: 1.75rem !important;
            line-height: 1.15 !important;
        }

        .hero-banner p {
            font-size: 0.95rem !important;
        }

        .balao-projetos {
            padding: 1.1rem 1rem !important;
            margin-bottom: 1.25rem !important;
        }

        .balao-projetos-titulo {
            font-size: 1.15rem !important;
        }

        .balao-projetos-colunas {
            grid-template-columns: 1fr !important;
        }

        .card-preco {
            min-height: auto !important;
            padding: 1rem !important;
        }

        .preco-destaque {
            font-size: 1.55rem !important;
        }

        .stButton > button,
        div[data-testid="stMarkdownContainer"]:has(.card-preco) ~ div .stButton > button {
            min-height: 3.1rem !important;
            font-size: 0.82rem !important;
            padding: 0.65rem 0.75rem !important;
        }

        .stTabs [data-baseweb="tab-list"] {
            flex-wrap: nowrap !important;
            overflow-x: auto !important;
            -webkit-overflow-scrolling: touch;
        }

        .stTabs [data-baseweb="tab"] {
            min-width: max-content !important;
            font-size: 0.82rem !important;
        }

        [data-testid="stSidebar"] {
            min-width: min(18rem, 88vw) !important;
        }

        [data-testid="stSidebar"] .stRadio label {
            min-height: 2.75rem !important;
            display: flex !important;
            align-items: center !important;
        }

        .equipe-foto {
            width: min(100%, 260px) !important;
            height: auto !important;
            min-height: 300px !important;
        }

        .metric-box .valor {
            font-size: 1.55rem !important;
        }

        .frase-inspiracao p {
            font-size: 1.15rem !important;
        }

        .pagamento-card {
            margin-bottom: 0.5rem;
        }

        [data-testid="stAppViewContainer"] [data-testid="stMain"] .bloco-pagamento-contratar .stRadio [data-baseweb="radio"] label,
        [data-testid="stAppViewContainer"] [data-testid="stMain"] .bloco-pagamento-contratar .stRadio label {
            width: 100% !important;
            margin: 0 0 0.4rem 0 !important;
            text-align: center !important;
        }

        [data-testid="stAppViewContainer"] [data-testid="stMain"] .parcela-destaque {
            font-size: 1.4rem !important;
        }

        iframe {
            max-width: 100% !important;
        }

        .dica-instalar-app {
            display: block !important;
        }
    }

    @media (max-width: 480px) {
        .hero-banner h1 {
            font-size: 1.5rem !important;
        }

        .stButton > button {
            font-size: 0.78rem !important;
        }
    }

    .dica-instalar-app {
        display: none;
        background: rgba(166, 124, 82, 0.15);
        border: 1px solid var(--rf-dourado-claro);
        border-radius: 10px;
        padding: 0.65rem 0.85rem;
        font-size: 0.78rem;
        color: #f0e4d4 !important;
        line-height: 1.45;
        margin-top: 0.5rem;
    }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


def inject_mobile_meta():
    manifest = {
        "name": "RF Arquitetura & Interiores",
        "short_name": "RF Arquitetura",
        "description": "Catálogo e contratação de projetos de arquitetura e interiores",
        "start_url": "/",
        "scope": "/",
        "display": "standalone",
        "orientation": "any",
        "background_color": "#faf6f0",
        "theme_color": "#a67c52",
        "lang": "pt-BR",
        "icons": [
            {
                "src": EMPRESA["logo"],
                "sizes": "192x192",
                "type": "image/png",
                "purpose": "any",
            },
            {
                "src": EMPRESA["logo"],
                "sizes": "512x512",
                "type": "image/png",
                "purpose": "maskable",
            },
        ],
    }
    manifest_uri = "data:application/manifest+json," + quote(
        json.dumps(manifest, ensure_ascii=False)
    )
    logo = EMPRESA["logo"]

    st.markdown(
        f"""
        <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
        <meta name="mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="default">
        <meta name="apple-mobile-web-app-title" content="RF Arquitetura">
        <meta name="theme-color" content="#a67c52">
        <meta name="format-detection" content="telephone=yes">
        <link rel="manifest" href="{manifest_uri}">
        <link rel="apple-touch-icon" href="{logo}">
        """,
        unsafe_allow_html=True,
    )


inject_mobile_meta()


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
                "Arquitetura Simples": v["valor"],
                "Arquitetura Completo": v["valor"] + v.get("completo_extra", 0),
                "Interiores": v.get("valor_interiores", 0),
                "Personalizado": "Sim" if v.get("personalizado") else "Não",
            }
        )
    return pd.DataFrame(dados)


def exibir_tabela(df: pd.DataFrame):
    st.dataframe(df, use_container_width=True, hide_index=True)


def tipo_projeto_item(item: dict) -> str:
    if item.get("tipo_projeto"):
        return item["tipo_projeto"]
    if item.get("projeto_completo"):
        return "completo"
    return "simples"


def label_tipo_projeto(item: dict) -> str:
    return {
        "simples": "Simples de Arquitetura",
        "completo": "Completo de Arquitetura",
        "interiores": "Interiores",
    }.get(tipo_projeto_item(item), "Simples de Arquitetura")


def df_carrinho(carrinho: list) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Categoria": item["categoria"],
                "Pacote": item["variante"],
                "Área": item["area"],
                "Tipo": label_tipo_projeto(item),
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
                "Tipo": label_tipo_projeto(proj),
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


def item_carrinho_id(cat_id: str, idx: int, tipo: str) -> str:
    return f"{cat_id}_{idx}_{tipo}"


def valor_item(item: dict) -> float:
    tipo = tipo_projeto_item(item)
    if tipo == "interiores":
        return item.get("valor_interiores", item["valor_base"])
    if tipo == "completo":
        return item["valor_base"] + item.get("completo_extra", 0)
    return item["valor_base"]


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


def item_no_carrinho(cat_id: str, idx: int, tipo: str) -> bool:
    item_id = item_carrinho_id(cat_id, idx, tipo)
    return any(i["id"] == item_id for i in st.session_state.carrinho)


def hero(titulo: str, subtitulo: str = ""):
    html = f"""
    <div class="hero-banner">
        <h1>{titulo}</h1>
        {"<p>" + subtitulo + "</p>" if subtitulo else ""}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def _lista_html_itens(itens: list[str]) -> str:
    return "".join(f"<li>{item}</li>" for item in itens)


def balao_tipos_projeto(cat_id: str | None = None):
    if cat_id is None:
        simples = itens_projeto_simples("casas")
        nota_3d = (
            '<p class="balao-nota-3d">Em Studios, Apartamentos e Comercial, '
            "o item 3D fachada é substituído por <strong>3D — 1 ambiente escolhido por você</strong>.</p>"
        )
    else:
        simples = itens_projeto_simples(cat_id)
        nota_3d = ""

    extras = ITENS_PROJETO_COMPLETO_EXTRA
    interiores = ITENS_PROJETO_INTERIORES
    completo_intro = (
        "Tudo do <strong>projeto simples</strong>, mais:"
        if cat_id
        else "Tudo do <strong>projeto simples</strong> (conforme a categoria), mais:"
    )

    st.markdown(
        f"""
        <div class="balao-projetos">
            <p class="balao-projetos-titulo">O que cada projeto inclui</p>
            <div class="balao-projetos-colunas">
                <div class="balao-coluna">
                    <h4>Projeto Simples de Arquitetura</h4>
                    <ul>{_lista_html_itens(simples)}</ul>
                    {nota_3d}
                </div>
                <div class="balao-coluna balao-coluna-extra">
                    <h4>Projeto Completo de Arquitetura</h4>
                    <p>{completo_intro}</p>
                    <ul>{_lista_html_itens(extras)}</ul>
                </div>
                <div class="balao-coluna balao-coluna-interiores">
                    <h4>Projeto de Interiores</h4>
                    <ul>{_lista_html_itens(interiores)}</ul>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def card_preco(variante: dict, categoria: dict, cat_id: str, idx: int):
    valor_total = variante["valor"]
    if variante.get("completo_extra"):
        valor_completo = valor_total + variante["completo_extra"]
    else:
        valor_completo = valor_total

    personalizado = variante.get("personalizado", False)

    st.markdown(
        f"""
        <div class="card-preco">
            <h3>{variante['nome']}</h3>
            <p class="card-area">{variante['area']}</p>
            <div class="preco-destaque">{formatar_moeda(valor_total)}</div>
            <p class="card-subtitulo">Escolha o tipo de projeto abaixo</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if eh_arquiteta():
        with st.expander("✏️ Editar valores"):
            with st.form(f"form_editar_variante_{cat_id}_{idx}"):
                novo_valor = st.number_input(
                    "Projeto Simples (R$)", min_value=0.0, step=100.0, value=float(variante["valor"])
                )
                novo_extra = st.number_input(
                    "Adicional Projeto Completo (R$)",
                    min_value=0.0,
                    step=100.0,
                    value=float(variante.get("completo_extra", 0)),
                )
                novo_interiores = st.number_input(
                    "Projeto de Interiores (R$)",
                    min_value=0.0,
                    step=100.0,
                    value=float(variante.get("valor_interiores", 0)),
                )
                if st.form_submit_button("Salvar valores"):
                    salvar_variante_override(
                        cat_id,
                        idx,
                        {
                            "valor": novo_valor,
                            "completo_extra": novo_extra,
                            "valor_interiores": novo_interiores,
                        },
                    )
                    st.toast("Valores atualizados!")
                    st.rerun()

    st.markdown('<div class="catalogo-pacote-botoes">', unsafe_allow_html=True)

    no_carrinho_simples = item_no_carrinho(cat_id, idx, "simples")
    no_carrinho_comp = item_no_carrinho(cat_id, idx, "completo")
    no_carrinho_interiores = item_no_carrinho(cat_id, idx, "interiores")
    valor_interiores = variante.get("valor_interiores", 0)

    label_base = (
        f"✓ Projeto Simples de Arquitetura — {formatar_moeda(valor_total)} (no carrinho)"
        if no_carrinho_simples
        else f"Projeto Simples de Arquitetura — {formatar_moeda(valor_total)}"
    )
    if st.button(
        label_base,
        key=f"sel_{cat_id}_{idx}",
        use_container_width=True,
        disabled=no_carrinho_simples,
    ):
        item = {
            "id": item_carrinho_id(cat_id, idx, "simples"),
            "categoria_id": cat_id,
            "categoria": categoria["titulo"],
            "variante": variante["nome"],
            "area": variante["area"],
            "valor_base": variante["valor"],
            "completo_extra": variante.get("completo_extra", 0),
            "valor_interiores": valor_interiores,
            "tipo_projeto": "simples",
            "projeto_completo": False,
            "personalizado": personalizado,
        }
        if adicionar_ao_carrinho(item):
            st.toast(f"{variante['nome']} (simples) adicionado ao carrinho!")
            st.rerun()

    if variante.get("completo_extra"):
        st.markdown('<div class="btn-completo-wrap"></div>', unsafe_allow_html=True)
        label_comp = (
            f"✓ Projeto Completo de Arquitetura — {formatar_moeda(valor_completo)} (no carrinho)"
            if no_carrinho_comp
            else f"Projeto Completo de Arquitetura — {formatar_moeda(valor_completo)}"
        )
        if st.button(
            label_comp,
            key=f"comp_{cat_id}_{idx}",
            use_container_width=True,
            disabled=no_carrinho_comp,
        ):
            item = {
                "id": item_carrinho_id(cat_id, idx, "completo"),
                "categoria_id": cat_id,
                "categoria": categoria["titulo"],
                "variante": variante["nome"],
                "area": variante["area"],
                "valor_base": variante["valor"],
                "completo_extra": variante.get("completo_extra", 0),
                "valor_interiores": valor_interiores,
                "tipo_projeto": "completo",
                "projeto_completo": True,
                "personalizado": personalizado,
            }
            if adicionar_ao_carrinho(item):
                st.toast(f"{variante['nome']} (completo) adicionado!")
                st.rerun()

    if valor_interiores:
        st.markdown('<div class="btn-interiores-wrap"></div>', unsafe_allow_html=True)
        label_int = (
            f"✓ Projeto de Interiores — {formatar_moeda(valor_interiores)} (no carrinho)"
            if no_carrinho_interiores
            else f"Projeto de Interiores — {formatar_moeda(valor_interiores)}"
        )
        if st.button(
            label_int,
            key=f"int_{cat_id}_{idx}",
            use_container_width=True,
            disabled=no_carrinho_interiores,
        ):
            item = {
                "id": item_carrinho_id(cat_id, idx, "interiores"),
                "categoria_id": cat_id,
                "categoria": categoria["titulo"],
                "variante": variante["nome"],
                "area": variante["area"],
                "valor_base": variante["valor"],
                "completo_extra": variante.get("completo_extra", 0),
                "valor_interiores": valor_interiores,
                "tipo_projeto": "interiores",
                "projeto_completo": False,
                "personalizado": personalizado,
            }
            if adicionar_ao_carrinho(item):
                st.toast(f"{variante['nome']} (interiores) adicionado!")
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def conteudo_sobre():
    if eh_arquiteta():
        with st.expander("✏️ Editar textos e contatos do site"):
            with st.form("form_editar_textos"):
                st.markdown("**Textos institucionais**")
                nova_frase = st.text_area("Frase inspiracional", value=FRASE_INSPIRACIONAL)
                novo_sobre_arquiteta = st.text_area(
                    f"Sobre {EMPRESA['arquiteta']}", value=SOBRE_ARQUITETA.strip(), height=150
                )
                novo_sobre_gestor = st.text_area(
                    f"Sobre {EMPRESA['gestor']}", value=SOBRE_GESTOR.strip(), height=150
                )
                novo_sobre_rita = st.text_area(
                    f"Sobre {EMPRESA['rita_cassia']}", value=SOBRE_RITA.strip(), height=150
                )

                st.markdown("---")
                st.markdown("**Contato**")
                novo_whatsapp = st.text_input(
                    "WhatsApp (só números, com DDI e DDD)", value=EMPRESA["whatsapp"]
                )
                novo_site = st.text_input("Site", value=EMPRESA["site"])
                novo_portfolio = st.text_input("Link do portfólio (Canva)", value=EMPRESA["portfolio"])
                nova_chave_pix = st.text_input(
                    "Chave Pix para recebimento", value=EMPRESA.get("chave_pix", "")
                )

                if st.form_submit_button("Salvar alterações"):
                    salvar_textos_overrides(
                        {
                            "frase_inspiracional": nova_frase.strip(),
                            "sobre_arquiteta": novo_sobre_arquiteta.strip(),
                            "sobre_gestor": novo_sobre_gestor.strip(),
                            "sobre_rita": novo_sobre_rita.strip(),
                        }
                    )
                    salvar_empresa_overrides(
                        {
                            "whatsapp": novo_whatsapp.strip(),
                            "site": novo_site.strip(),
                            "portfolio": novo_portfolio.strip(),
                            "portfolio_embed": f"{novo_portfolio.strip()}?embed",
                            "chave_pix": nova_chave_pix.strip(),
                        }
                    )
                    st.toast("Alterações salvas!")
                    st.rerun()

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

    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
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

    with col2:
        st.markdown(
            f"""
            <div class="equipe-bloco">
                <img src="{EMPRESA['foto_gestor']}" class="equipe-foto"
                     alt="{EMPRESA['gestor']}"/>
                <p class="equipe-legenda">{EMPRESA['gestor']}<br>Profissional responsável</p>
                <div class="sobre-card">
                    <h3>{EMPRESA['gestor']}</h3>
                    <p>{SOBRE_GESTOR.strip()}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div class="equipe-bloco">
                <img src="{foto_src(EMPRESA['foto_rita_cassia'], EMPRESA['logo'])}" class="equipe-foto"
                     alt="{EMPRESA['rita_cassia']}"/>
                <p class="equipe-legenda">{EMPRESA['rita_cassia']}<br>Arquiteta &amp; Urbanista</p>
                <div class="sobre-card">
                    <h3>{EMPRESA['rita_cassia']}</h3>
                    <p>{SOBRE_RITA.strip()}</p>
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

    tab_sobre, tab_portfolio = st.tabs(["Sobre", "Portfólio"])

    with tab_sobre:
        conteudo_sobre()

    with tab_portfolio:
        conteudo_portfolio()


def pagina_catalogo():
    hero("Catálogo de Projetos", "Escolha um ou mais pacotes e adicione ao carrinho")

    balao_tipos_projeto()

    qtd = len(st.session_state.carrinho)
    if qtd > 0:
        col_info, col_btn = st.columns([3, 1])
        with col_info:
            st.success(f"Você tem **{qtd}** projeto(s) no carrinho — Total: **{formatar_moeda(total_carrinho())}**")
        with col_btn:
            if st.button("Ver Carrinho", use_container_width=True, key="catalogo_ver_carrinho"):
                st.session_state.nav_page = "Carrinho"
                st.rerun()

    titulos_tabs = [cat["titulo"] for cat in CATEGORIAS.values()]
    if eh_arquiteta():
        titulos_tabs = titulos_tabs + ["Projetos Prontos"]

    tabs = st.tabs(titulos_tabs)
    tabs_categorias = tabs[: len(CATEGORIAS)]

    for tab, (cat_id, cat) in zip(tabs_categorias, CATEGORIAS.items()):
        with tab:
            if eh_arquiteta():
                with st.expander("✏️ Editar categoria"):
                    with st.form(f"form_editar_categoria_{cat_id}"):
                        novo_titulo = st.text_input("Título", value=cat["titulo"])
                        nova_descricao = st.text_area("Descrição", value=cat["descricao"])
                        if st.form_submit_button("Salvar"):
                            salvar_categoria_texto(cat_id, novo_titulo.strip(), nova_descricao.strip())
                            st.toast("Categoria atualizada!")
                            st.rerun()

            st.markdown(f"*{cat['descricao']}*")
            st.markdown("---")
            variantes = cat["variantes"]
            for i in range(0, len(variantes), 2):
                cols = st.columns(2, gap="large")
                for j, col in enumerate(cols):
                    idx = i + j
                    if idx < len(variantes):
                        with col:
                            card_preco(variantes[idx], cat, cat_id, idx)

    if eh_arquiteta():
        with tabs[-1]:
            conteudo_projetos_prontos()


def conteudo_projetos_prontos():
    st.markdown("*Projetos já concluídos pela RF Arquitetura & Interiores*")
    st.markdown("---")

    projetos = carregar_projetos_prontos()

    if eh_arquiteta():
        with st.form("form_add_projeto_pronto", clear_on_submit=True):
            st.markdown("**Adicionar novo projeto**")
            nome = st.text_input("Nome do projeto")
            descricao = st.text_area("Descrição", max_chars=500)
            imagem = st.file_uploader("Imagem / foto do projeto", type=["png", "jpg", "jpeg", "webp"])
            if st.form_submit_button("Salvar projeto"):
                if not nome or not descricao:
                    st.error("Preencha nome e descrição.")
                else:
                    imagem_path = None
                    if imagem is not None:
                        PROJETOS_PRONTOS_IMG_DIR.mkdir(parents=True, exist_ok=True)
                        extensao = Path(imagem.name).suffix.lower() or ".jpg"
                        nome_arquivo = f"{uuid.uuid4().hex}{extensao}"
                        destino = PROJETOS_PRONTOS_IMG_DIR / nome_arquivo
                        destino.write_bytes(imagem.getvalue())
                        imagem_path = f"static/projetos_prontos/{nome_arquivo}"

                    projetos.insert(
                        0,
                        {
                            "id": uuid.uuid4().hex,
                            "nome": nome.strip(),
                            "descricao": descricao.strip(),
                            "imagem": imagem_path,
                        },
                    )
                    salvar_projetos_prontos(projetos)
                    st.toast("Projeto adicionado!")
                    st.rerun()

    if not projetos:
        st.info("Nenhum projeto adicionado ainda.")
        return

    for i in range(0, len(projetos), 3):
        cols = st.columns(3, gap="large")
        for j, col in enumerate(cols):
            idx = i + j
            if idx >= len(projetos):
                continue
            projeto = projetos[idx]
            with col:
                imagem_html = (
                    f'<img src="{foto_src(projeto["imagem"], EMPRESA["logo"])}" alt="{projeto["nome"]}">'
                    if projeto.get("imagem")
                    else ""
                )
                st.markdown(
                    f"""
                    <div class="card-projeto-pronto">
                        {imagem_html}
                        <div class="corpo">
                            <h3>{projeto['nome']}</h3>
                            <p>{projeto['descricao']}</p>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if eh_arquiteta():
                    if st.button("Excluir", key=f"excluir_pronto_{projeto['id']}", use_container_width=True):
                        if projeto.get("imagem"):
                            caminho_img = _BASE_DIR_APP / projeto["imagem"]
                            if caminho_img.is_file():
                                caminho_img.unlink()
                        salvar_projetos_prontos(
                            [p for p in projetos if p["id"] != projeto["id"]]
                        )
                        st.rerun()


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

    st.markdown('<div class="secao-contratar">', unsafe_allow_html=True)
    st.markdown("### Resumo do Pedido")
    exibir_tabela(df_resumo_pedido(st.session_state.carrinho))

    if st.button("Editar carrinho", key="vendas_editar_carrinho"):
        st.session_state.nav_page = "Carrinho"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="secao-contratar bloco-dados-contratar">', unsafe_allow_html=True)
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
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="secao-contratar bloco-pagamento-contratar">', unsafe_allow_html=True)
    st.markdown("### Escolha como pagar")

    METODOS_INFO = [
        {"nome": "Pix", "descricao": "Aprovação imediata • 10% de desconto"},
        {"nome": "Boleto", "descricao": "Aprovação em 1 a 2 dias úteis"},
        {"nome": "Cartão de crédito ou débito", "descricao": "Parcele em até 12x no crédito"},
    ]

    cols_pag = st.columns(3)
    for i, metodo in enumerate(METODOS_INFO):
        with cols_pag[i]:
            st.markdown(
                f"""
                <div class="pagamento-card">
                    <h4 style="margin:0.5rem 0;">{metodo['nome']}</h4>
                    <p style="font-size:0.85rem; color:#6b5d4d;">{metodo['descricao']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    metodo_escolhido = st.radio(
        "Selecione como pagar:",
        [m["nome"] for m in METODOS_INFO],
        horizontal=True,
        key="metodo_pag_radio",
    )

    dados_cartao_ok = True
    parcelas_selecionadas = 1
    forma = None

    if metodo_escolhido == "Pix":
        forma = "PIX"
        st.markdown("#### Pagar com Pix")
        chave_pix = EMPRESA.get("chave_pix", "")
        if chave_pix:
            st.markdown(
                f"""
                <div class="pix-box">
                    <p>Chave Pix para pagamento:</p>
                    <p class="pix-chave">{chave_pix}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.caption(
                "Copie a chave acima no aplicativo do seu banco, realize o pagamento e "
                "depois clique em Confirmar Pagamento abaixo."
            )
        else:
            st.warning("Chave Pix ainda não configurada pela arquiteta. Escolha outra forma de pagamento.")

    elif metodo_escolhido == "Boleto":
        forma = "Boleto"
        st.markdown("#### Pagar com Boleto")
        if "boleto_codigo" not in st.session_state:
            st.session_state.boleto_codigo = None

        if st.button("Gerar Boleto", key="gerar_boleto"):
            st.session_state.boleto_codigo = " ".join(
                f"{random.randint(0, 99999):05d}" for _ in range(10)
            )

        if st.session_state.boleto_codigo:
            st.success("Boleto gerado com sucesso!")
            st.code(st.session_state.boleto_codigo)
            st.caption(
                "Pague em qualquer banco, app ou lotérica até o vencimento. "
                "O pedido é confirmado após a compensação (1 a 2 dias úteis)."
            )
        else:
            st.caption("Clique em \"Gerar Boleto\" para obter o código de pagamento.")

    else:
        forma = st.radio(
            "Tipo de cartão:",
            ["Cartão de Crédito", "Cartão de Débito"],
            horizontal=True,
            key="tipo_cartao_radio",
        )
        st.markdown("#### Dados do cartão")
        c1, c2 = st.columns([2, 1])
        with c1:
            numero_cartao = st.text_input(
                "Número do cartão",
                key="cartao_numero",
                placeholder="0000 0000 0000 0000",
                max_chars=19,
            )
        with c2:
            cvv = st.text_input(
                "CVV", key="cartao_cvv", placeholder="000", max_chars=4, type="password"
            )
        c3, c4 = st.columns(2)
        with c3:
            nome_cartao = st.text_input("Nome impresso no cartão", key="cartao_nome")
        with c4:
            validade = st.text_input(
                "Validade (MM/AA)", key="cartao_validade", placeholder="MM/AA", max_chars=5
            )

        if forma == "Cartão de Crédito":
            parcelas_selecionadas = st.selectbox(
                "Parcelas",
                options=list(range(1, 13)),
                format_func=lambda n: "À vista" if n == 1 else f"{n}x de {formatar_moeda(valor_total / n)} sem juros",
                key="cartao_parcelas",
            )

        numero_limpo = re.sub(r"\D", "", numero_cartao)
        cvv_limpo = re.sub(r"\D", "", cvv)
        validade_ok = bool(re.fullmatch(r"(0[1-9]|1[0-2])/\d{2}", validade))

        dados_cartao_ok = (
            13 <= len(numero_limpo) <= 19
            and nome_cartao.strip() != ""
            and validade_ok
            and 3 <= len(cvv_limpo) <= 4
        )
        if any([numero_cartao, nome_cartao, validade, cvv]) and not dados_cartao_ok:
            st.caption("Confira os dados do cartão: número, nome, validade (MM/AA) e CVV.")

    st.session_state.forma_pagamento = forma
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    desconto_pix = forma == "PIX"
    valor_final = valor_total * 0.9 if desconto_pix else valor_total

    if desconto_pix:
        st.caption(f"Valor original: {formatar_moeda(valor_total)}")
        st.markdown(f"### Total com 10% de desconto (PIX): {formatar_moeda(valor_final)}")
    else:
        st.markdown(f"### Total: {formatar_moeda(valor_final)}")

    if st.button(
        f"Confirmar Pagamento — {formatar_moeda(valor_final)}",
        use_container_width=True,
        key="vendas_confirmar_pagamento",
    ):
        st.session_state.pagamento_confirmado = True
        registrar_compra(
            {
                "id": uuid.uuid4().hex,
                "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "cliente_nome": st.session_state.cliente_nome,
                "cliente_email": st.session_state.cliente_email,
                "cliente_telefone": st.session_state.cliente_telefone,
                "itens": [
                    {
                        "categoria": p["categoria"],
                        "variante": p["variante"],
                        "tipo": label_tipo_projeto(p),
                        "valor": valor_item(p),
                    }
                    for p in st.session_state.carrinho
                ],
                "total": valor_final,
                "forma_pagamento": st.session_state.forma_pagamento,
                "parcelas": parcelas_selecionadas if forma == "Cartão de Crédito" else 1,
                "desconto_pix_aplicado": desconto_pix,
            }
        )
        st.balloons()
        st.rerun()

    if st.session_state.pagamento_confirmado:
        st.success("Pagamento confirmado com sucesso! Alguém do nosso time entrará em contato em breve.")


def pagina_dashboard():
    hero("Dashboard de Vendas", "Visão geral dos pacotes e valores")

    df = criar_df_precos()
    df_exibicao = formatar_colunas_moeda(
        df, ["Arquitetura Simples", "Arquitetura Completo", "Interiores"]
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total de Pacotes", len(df))
    with col2:
        st.metric("Ticket Médio (Arq. Simples)", formatar_moeda(df["Arquitetura Simples"].mean()))
    with col3:
        st.metric("Ticket Médio (Arq. Completo)", formatar_moeda(df["Arquitetura Completo"].mean()))
    with col4:
        st.metric("Ticket Médio (Interiores)", formatar_moeda(df["Interiores"].mean()))

    st.markdown("### Tabela de Preços Completa")
    exibir_tabela(df_exibicao)

    st.markdown("### Valores por Categoria")
    chart_data = df.groupby("Categoria")[["Arquitetura Simples", "Arquitetura Completo", "Interiores"]].mean()
    chart_data.columns = ["Arq. Simples (médio)", "Arq. Completo (médio)", "Interiores (médio)"]
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


def pagina_compras_realizadas():
    hero("Compras Realizadas", "Clientes que confirmaram pagamento pela plataforma")

    compras = carregar_compras()

    if not compras:
        st.info("Nenhuma compra registrada ainda.")
        return

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f'<div class="metric-box"><div class="valor">{len(compras)}</div><div class="label">Compras</div></div>',
            unsafe_allow_html=True,
        )
    with col2:
        receita_total = sum(c["total"] for c in compras)
        st.markdown(
            f'<div class="metric-box"><div class="valor">{formatar_moeda(receita_total)}</div><div class="label">Receita total</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    for compra in compras:
        titulo = f"{compra['cliente_nome'] or 'Cliente sem nome'} — {formatar_moeda(compra['total'])} — {compra['data_hora']}"
        with st.expander(titulo):
            st.markdown(f"**E-mail:** {compra['cliente_email'] or '—'}")
            st.markdown(f"**Telefone:** {compra['cliente_telefone'] or '—'}")
            forma_txt = compra["forma_pagamento"]
            if compra.get("parcelas", 1) > 1:
                forma_txt += f" em {compra['parcelas']}x"
            st.markdown(f"**Forma de pagamento:** {forma_txt}")
            st.markdown("**Itens:**")
            for item in compra["itens"]:
                st.markdown(
                    f"- {item['categoria']} — {item['variante']} ({item['tipo']}) — {formatar_moeda(item['valor'])}"
                )


def tela_selecao_papel():
    hero(EMPRESA["nome"], "Como você quer acessar o site?")

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown(
            """
            <div class="sobre-card">
                <h3>👤 Sou Cliente</h3>
                <p>Faça seu cadastro rápido e veja o catálogo, preços e contrate um projeto.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        with st.form("form_cadastro_cliente"):
            nome_cadastro = st.text_input("Nome completo", value=st.session_state.cliente_nome)
            email_cadastro = st.text_input("E-mail", value=st.session_state.cliente_email)
            telefone_cadastro = st.text_input(
                "Telefone / WhatsApp", value=st.session_state.cliente_telefone
            )
            if st.form_submit_button("Entrar como Cliente", use_container_width=True):
                st.session_state.cliente_nome = nome_cadastro.strip()
                st.session_state.cliente_email = email_cadastro.strip()
                st.session_state.cliente_telefone = telefone_cadastro.strip()
                st.session_state.papel = "cliente"
                st.session_state.nav_page = "Início"
                st.rerun()

    with col2:
        st.markdown(
            """
            <div class="sobre-card">
                <h3>🛠️ Sou Arquiteta</h3>
                <p>Acesse o painel para editar preços, textos e projetos do site.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        senha = st.text_input("Senha de acesso", type="password", key="senha_papel_arquiteta")
        if st.button("Entrar como Arquiteta", use_container_width=True, key="entrar_arquiteta"):
            if senha == senha_admin():
                st.session_state.papel = "arquiteta"
                st.session_state.nav_page = "Início"
                st.rerun()
            else:
                st.error("Senha incorreta.")


def main():
    init_session()

    if "papel" not in st.session_state:
        tela_selecao_papel()
        return

    with st.sidebar:
        st.markdown("## RF Arquitetura")
        st.markdown("*Interiores & Projetos*")

        if eh_arquiteta():
            st.markdown(
                '<div class="badge-papel badge-papel-arquiteta">🛠️ Modo Arquiteta</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="badge-papel badge-papel-cliente">👤 Modo Cliente</div>',
                unsafe_allow_html=True,
            )

        if st.button("Trocar de usuário", use_container_width=True, key="trocar_papel"):
            del st.session_state["papel"]
            st.session_state.nav_page = "Início"
            st.rerun()

        st.markdown("---")

        paginas = {
            "Início": pagina_inicio,
            "Catálogo": pagina_catalogo,
            "Carrinho": pagina_carrinho,
            "Contratar": pagina_vendas,
            "Dashboard": pagina_dashboard,
        }
        if eh_arquiteta():
            paginas["Compras Realizadas"] = pagina_compras_realizadas

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
        st.markdown(
            '<p class="dica-instalar-app">'
            "📱 <strong>Instalar no celular:</strong> "
            "Android → menu ⋮ → <em>Adicionar à tela inicial</em>. "
            "iPhone → compartilhar ⎋ → <em>Adicionar à Tela de Início</em>."
            "</p>",
            unsafe_allow_html=True,
        )
        st.caption(f"© 2026 {EMPRESA['nome']}")

    paginas[st.session_state.nav_page]()


if __name__ == "__main__":
    main()
