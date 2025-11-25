import csv
import sys
from datetime import datetime
from pathlib import Path

from ubersuggest_client import UbersuggestClient


INTENT_MAP = {
    1: "I",  # Informacional (suposição)
    2: "N",  # Navegacional (se aparecer)
    3: "C",  # Comercial
    4: "T",  # Transacional
}


def format_volume(v):
    if v is None:
        return ""
    try:
        v = int(v)
    except (TypeError, ValueError):
        return ""
    if v >= 1000:
        return f"{v/1000:.1f}k".replace(".", ",")
    return str(v)


def format_cpc_brl(cpc):
    if cpc is None:
        return ""
    try:
        val = float(cpc)
    except (TypeError, ValueError):
        return ""
    txt = f"{val:,.2f}"
    txt = txt.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R${txt}"


def format_intent(codes):
    if not codes:
        return ""
    seen = []
    for c in codes:
        letter = INTENT_MAP.get(c)
        if letter and letter not in seen:
            seen.append(letter)
    return " ".join(seen)


def humanize_timestamp(ts):
    if not ts:
        return ""
    try:
        dt = datetime.fromtimestamp(int(ts))
    except Exception:
        return ""
    now = datetime.now()
    diff = now - dt
    days = diff.days
    if days < 1:
        return "Hoje"
    if days == 1:
        return "Há 1 dia"
    if days < 7:
        return f"Há {days} dias"
    weeks = days // 7
    if weeks == 1:
        return "Há 1 semana"
    if weeks < 8:
        return f"Há {weeks} semanas"
    months = days // 30
    if months == 1:
        return "Há 1 mês"
    if months < 12:
        return f"Há {months} meses"
    return "Há mais de 1 ano"


def print_entry(e):
    keyword = e.get("keyword", "")
    volume = format_volume(e.get("volume"))
    cpc = format_cpc_brl(e.get("cpc"))
    pd = e.get("pd")
    sd = e.get("sd")
    intent = format_intent(e.get("searchIntent") or [])
    updated = humanize_timestamp(e.get("updated_at"))

    print(keyword)
    if intent:
        print(f"  Intenção: {intent}")
    if volume:
        print(f"  Volume: {volume}")
    if cpc:
        print(f"  CPC: {cpc}")
    if pd is not None:
        print(f"  PD: {pd}")
    if sd is not None:
        print(f"  SEO Difficulty: {sd}")
    if updated:
        print(f"  Atualizado: {updated}")
    print()


def salvar_csv(dados, keyword_base):
    suggestions = dados.get("suggestions", [])
    searched = dados.get("searched_keywords", [])

    safe_kw = keyword_base.replace(" ", "_")
    output_path = Path(f"keywords_{safe_kw}.csv")

    campos = [
        "origem",         # base ou ideia
        "keyword",
        "intent",
        "volume",
        "cpc_brl",
        "pd",
        "sd",
        "updated_human",
    ]

    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()

        # linha(s) da keyword base
        for b in searched:
            writer.writerow({
                "origem": "base",
                "keyword": b.get("keyword", ""),
                "intent": format_intent(b.get("searchIntent") or []),
                "volume": format_volume(b.get("volume")),
                "cpc_brl": format_cpc_brl(b.get("cpc")),
                "pd": b.get("pd", ""),
                "sd": b.get("sd", ""),
                "updated_human": humanize_timestamp(b.get("updated_at")),
            })

        # linhas das ideias
        for s in suggestions:
            writer.writerow({
                "origem": "ideia",
                "keyword": s.get("keyword", ""),
                "intent": format_intent(s.get("searchIntent") or []),
                "volume": format_volume(s.get("volume")),
                "cpc_brl": format_cpc_brl(s.get("cpc")),
                "pd": s.get("pd", ""),
                "sd": s.get("sd", ""),
                "updated_human": humanize_timestamp(s.get("updated_at")),
            })

    print(f"\n[SEOgenius] CSV salvo em: {output_path}")


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 run.py <palavra-chave>")
        sys.exit(1)

    keyword = sys.argv[1]
    client = UbersuggestClient()
    dados = client.match_keywords(keyword)

    searched = dados.get("searched_keywords", [])
    suggestions = dados.get("suggestions", [])

    print("\n===== SUAS PALAVRAS-CHAVE =====\n")
    if not searched:
        print("(Nenhuma keyword base encontrada)\n")
    else:
        for b in searched:
            print_entry(b)

    print("===== IDEIAS DE PALAVRAS-CHAVE =====\n")
    # Se quiser limitar, troque para suggestions[:50]
    for s in suggestions:
        print_entry(s)

    # Gera CSV com tudo
    salvar_csv(dados, keyword)


if __name__ == "__main__":
    main()
