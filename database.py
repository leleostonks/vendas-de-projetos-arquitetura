"""Dados de projetos, preços e informações da RF Arquitetura."""

import base64
from pathlib import Path

_BASE_DIR = Path(__file__).parent

EMPRESA = {
    "nome": "RF Arquitetura & Interiores",
    "arquiteta": "Rachel Fernandes",
    "gestor": "Igor Henrique",
    "whatsapp": "5511968988548",
    "site": "https://rfinteriores.wixsite.com/rfarquitetura",
    "portfolio": "https://www.canva.com/design/DAGisRykX5E/ZcMpMjV8gAvqCc8nZzailA/view",
    "portfolio_embed": "https://www.canva.com/design/DAGisRykX5E/ZcMpMjV8gAvqCc8nZzailA/view?embed",
    "logo": "https://static.wixstatic.com/media/b828b7_1fa3272fbe8246db97934eb79c7e0949~mv2.png/v1/fill/w_199,h_199,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/a-removebg-preview.png",
    "foto_arquiteta": "https://static.wixstatic.com/media/b828b7_574b980973514a9a8cec80d6fb975dbd~mv2.jpeg/v1/crop/x_29,y_0,w_299,h_481/fill/w_419,h_668,al_c,lg_1,q_80,enc_avif,quality_auto/b828b7_574b980973514a9a8cec80d6fb975dbd~mv2.jpeg",
    "foto_gestor": "https://static.wixstatic.com/media/b828b7_7b862c5225e8485cb13849a8de09ffe3~mv2.jpg/v1/crop/x_0,y_32,w_478,h_757/fill/w_478,h_713,al_c,q_80,enc_avif,quality_auto/Imagem%20do%20WhatsApp%20de%202025-06-18%20%C3%A0(s)%2012_25_21_1ce60db6.jpg",
    "rita_cassia": "Rita de Cássia",
    "foto_rita_cassia": "static/foto_rita_cassia.png",
}

FRASE_INSPIRACIONAL = (
    "Transforme seus sonhos em realidade, porque cada espaço que você habita "
    "tem o poder de refletir a melhor versão de você."
)

SOBRE_ARQUITETA = """
Rachel Fernandes é arquiteta e urbanista, graduada pela Universidade FMU, com pós-graduação em 
Design de Interiores e MBA em Design de Interiores, Conforto Ambiental e Luminotécnica. 
Com mais de 13 anos de experiência, sua criatividade reflete um vasto conhecimento e habilidade 
em harmonizar cores, texturas e elementos, criando ambientes únicos e personalizados. 
Desde projetos residenciais até comerciais, cada detalhe é cuidadosamente planejado para 
atender às necessidades e desejos de seus clientes.
"""

SOBRE_GESTOR = """
Igor Henrique profissional responsável pela gestão administrativa e pelo acompanhamento de obras, 
com atuação versátil e integrada. Experiência em controle financeiro, emissão de documentos, 
contratos, apoio aos setores de compras, além da supervisão de cronogramas, equipes e materiais 
em campo. Organizado, comprometido e com visão ampla de processos, assegura a execução eficiente 
dos projetos, dentro dos prazos e padrões de qualidade da empresa.
"""

SOBRE_RITA = """
Graduada em Arquitetura e Urbanismo pela Universidade Nove de Julho, adquiri experiência 
atuando em diversos escritórios de arquitetura, com vivência em diferentes segmentos, 
como projetos institucionais e residenciais, além da gestão e acompanhamento de obras. 
Essas experiências contribuíram para o desenvolvimento da minha autonomia profissional 
e ampliaram minha capacidade de atuar em diferentes áreas. Em parceria com outros 
profissionais do setor, tive a oportunidade de planejar e executar projetos de forma 
independente, desenvolvendo soluções alinhadas às necessidades de cada cliente.
"""

ITENS_PROJETO_SIMPLES = [
    "Planta de arquitetura",
    "Planta de layout",
    "Planta de iluminação",
    "Planta de forro",
    "Pontos de elétrica",
    "Pontos hidráulica",
    "3D fachada",
]

ITENS_PROJETO_COMPLETO_EXTRA = [
    "Planta de Demolir e construir",
    "Planta de piso",
    "Detalhamentos",
    "Mapa de Esquadrias",
    "Planta de Revestimento",
]

ITENS_PROJETO_INTERIORES = [
    "Briefing",
    "Mood board",
    "Apresentação com valores dos produtos usados e similares e indicação de onde comprar",
    "Projeto luminotécnico diferenciado",
    "Imagens 3D de todos os ambientes",
]

ITENS_3D_AMBIENTE = "3D — 1 ambiente escolhido por você"

ITENS_BASE_CASA = ITENS_PROJETO_SIMPLES

ITENS_BASE_STUDIO_APT_COM = ITENS_PROJETO_SIMPLES[:-1] + [ITENS_3D_AMBIENTE]

FORMAS_PAGAMENTO = [
    {"nome": "PIX", "descricao": "Pagamento instantâneo com desconto"},
    {"nome": "Cartão de Crédito", "descricao": "Parcelamento em até 12x sem juros"},
    {"nome": "Cartão de Débito", "descricao": "Débito à vista"},
]

CATEGORIAS = {
    "casas": {
        "titulo": "Casas",
        "descricao": "Projetos residenciais completos com 3D de fachada",
        "itens": ITENS_BASE_CASA,
        "variantes": [
            {
                "nome": "Até 50 m²",
                "area": "até 50 m²",
                "valor": 1500.00,
                "completo_extra": 1500.00,
                "valor_interiores": 3000.00,
            },
            {
                "nome": "60 a 80 m²",
                "area": "60 a 80 m²",
                "valor": 2500.00,
                "completo_extra": 1500.00,
                "valor_interiores": 5000.00,
            },
            {
                "nome": "90 a 120 m²",
                "area": "90 a 120 m²",
                "valor": 3500.00,
                "completo_extra": 2000.00,
                "valor_interiores": 7000.00,
            },
            {
                "nome": "Acima de 120 m²",
                "area": "acima de 120 m²",
                "valor": 6500.00,
                "completo_extra": 2000.00,
                "valor_interiores": 9000.00,
                "personalizado": True,
            },
        ],
    },
    "studios": {
        "titulo": "Studios",
        "descricao": "Projetos compactos com 3D de 1 ambiente à sua escolha",
        "itens": ITENS_BASE_STUDIO_APT_COM,
        "variantes": [
            {
                "nome": "Até 24 m²",
                "area": "até 24 m²",
                "valor": 1000.00,
                "completo_extra": 1500.00,
                "valor_interiores": 2500.00,
            },
            {
                "nome": "25 a 38 m²",
                "area": "25 a 38 m²",
                "valor": 1500.00,
                "completo_extra": 1500.00,
                "valor_interiores": 3000.00,
            },
            {
                "nome": "38 a 48 m²",
                "area": "38 a 48 m²",
                "valor": 2000.00,
                "completo_extra": 2000.00,
                "valor_interiores": 3500.00,
            },
        ],
    },
    "apartamentos": {
        "titulo": "Apartamentos",
        "descricao": "Projetos para apartamentos com 3D de 1 ambiente à sua escolha",
        "itens": ITENS_BASE_STUDIO_APT_COM,
        "variantes": [
            {
                "nome": "50 a 70 m²",
                "area": "50 a 70 m²",
                "valor": 2000.00,
                "completo_extra": 1500.00,
                "valor_interiores": 3000.00,
            },
            {
                "nome": "70 a 90 m²",
                "area": "70 a 90 m²",
                "valor": 2500.00,
                "completo_extra": 1500.00,
                "valor_interiores": 5000.00,
            },
            {
                "nome": "90 a 120 m²",
                "area": "90 a 120 m²",
                "valor": 3000.00,
                "completo_extra": 2000.00,
                "valor_interiores": 7000.00,
            },
            {
                "nome": "Acima de 120 m²",
                "area": "acima de 120 m²",
                "valor": 6500.00,
                "completo_extra": 2000.00,
                "valor_interiores": 9000.00,
                "personalizado": True,
            },
        ],
    },
    "comercial": {
        "titulo": "Comercial",
        "descricao": "Projetos comerciais com 3D de 1 ambiente à sua escolha",
        "itens": ITENS_BASE_STUDIO_APT_COM,
        "variantes": [
            {
                "nome": "Até 50 m²",
                "area": "até 50 m²",
                "valor": 1500.00,
                "completo_extra": 1500.00,
                "valor_interiores": 2500.00,
            },
            {
                "nome": "50 a 70 m²",
                "area": "50 a 70 m²",
                "valor": 2500.00,
                "completo_extra": 1500.00,
                "valor_interiores": 3500.00,
            },
            {
                "nome": "70 a 90 m²",
                "area": "70 a 90 m²",
                "valor": 3000.00,
                "completo_extra": 2000.00,
                "valor_interiores": 4500.00,
            },
        ],
    },
}


def url_portfolio_embed() -> str:
    return EMPRESA.get(
        "portfolio_embed",
        f"{EMPRESA['portfolio']}?embed",
    )


def itens_projeto_simples(cat_id: str = "casas") -> list[str]:
    if cat_id == "casas":
        return list(ITENS_PROJETO_SIMPLES)
    return ITENS_PROJETO_SIMPLES[:-1] + [ITENS_3D_AMBIENTE]


def itens_projeto_completo(cat_id: str = "casas") -> list[str]:
    return itens_projeto_simples(cat_id) + ITENS_PROJETO_COMPLETO_EXTRA


def itens_projeto_interiores() -> list[str]:
    return list(ITENS_PROJETO_INTERIORES)


def formatar_moeda(valor: float) -> str:
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def foto_src(caminho: str, fallback: str | None = None) -> str:
    if caminho.startswith(("http://", "https://", "data:")):
        return caminho
    path = _BASE_DIR / caminho
    if path.is_file():
        mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
        encoded = base64.b64encode(path.read_bytes()).decode("ascii")
        return f"data:{mime};base64,{encoded}"
    return fallback or caminho


def listar_todas_variantes() -> list[dict]:
    resultado = []
    for cat_id, cat in CATEGORIAS.items():
        for var in cat["variantes"]:
            resultado.append(
                {
                    "categoria_id": cat_id,
                    "categoria": cat["titulo"],
                    **var,
                }
            )
    return resultado
