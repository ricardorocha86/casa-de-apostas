"""Formatação de números no padrão brasileiro."""


def numero_br(valor, casas=2):
    texto = f"{valor:,.{casas}f}"
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


def brl(valor):
    """1234.5 → 'R$ 1.234,50' | -3 → '-R$ 3,00'"""
    valor = round(valor, 2)
    prefixo = "-R$ " if valor < 0 else "R$ "
    return prefixo + numero_br(abs(valor))


def brl_md(valor):
    """Versão de brl() segura para st.markdown/st.caption (o $ não vira LaTeX)."""
    return brl(valor).replace("$", "\\$")


def pct(valor, casas=1):
    """Recebe o valor já em pontos percentuais: 5.26 → '5,3%'"""
    return f"{numero_br(valor, casas)}%"


def formatar_brl(df, colunas):
    """Styler que exibe as colunas em R$ mantendo a ordenação numérica da tabela."""
    return df.style.format(brl, subset=colunas)
