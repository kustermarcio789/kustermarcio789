"""Gera os SVGs animados do README do perfil.

Edite as constantes abaixo e rode:  python scripts/gerar_svgs.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

NOME = "Kuster"
USUARIO = "kuster"
HOST = "oficina"
TAGLINE = "// do código à peça física"

PROJETOS = [  # (arquivo, título, [linha1, linha2], tags)
    ("card-3dkprint", "3dkprint.com.br",
     ["Loja e orçamento online de impressão 3D,", "com painel administrativo próprio."],
     ["React", "TypeScript", "Supabase"]),
    ("card-agrale", "motopecasagrale.com.br",
     ["E-commerce de peças para motos Agrale com", "pagamento e frete integrados."],
     ["React", "Mercado Pago", "Melhor Envio"]),
    ("card-ecoferro", "ecoferro.com.br",
     ["Site B2B com portal do atacadista e", "acompanhamento da produção."],
     ["React", "Supabase", "PostgreSQL"]),
    ("card-vendas", "vendas.ecoferro.com.br",
     ["Gestão das vendas do Mercado Livre com", "emissão de NF-e integrada."],
     ["React", "Express", "SQLite"]),
    ("card-epi360", "epi360.ecoferro.com.br",
     ["SaaS de controle de EPIs: fichas com", "assinatura digital, estoque e alertas."],
     ["JavaScript", "Supabase", "Node.js"]),
    ("card-drive", "google-drive-disco-local",
     ["Google Drive como disco local no Windows", "e no Linux, com rclone. Guia + scripts."],
     ["PowerShell", "rclone", "Linux"]),
]

OUT = Path(__file__).resolve().parent.parent / "assets"
FS = 17
CW = FS * 0.6  # largura aproximada de um caractere monoespaçado
BG, BARRA, BORDA = "#0d1117", "#161b22", "#30363d"
VERDE, AZUL, CINZA, TEXTO = "#39d353", "#58a6ff", "#8b949e", "#c9d1d9"
LARANJA, LARANJA2, ROXO, CIANO = "#ffa657", "#f0883e", "#d2a8ff", "#79c0ff"
FONTE = "Consolas,'SF Mono',Menlo,'DejaVu Sans Mono','Courier New',monospace"
PROMPT = f"{USUARIO}@{HOST}:~$ "


def prompt(cmd=""):
    return (f'<tspan fill="{VERDE}">{USUARIO}@{HOST}</tspan><tspan fill="{CINZA}">:</tspan>'
            f'<tspan fill="{AZUL}">~</tspan><tspan fill="{CINZA}">$ </tspan>'
            f'<tspan fill="{TEXTO}">{escape(cmd)}</tspan>')


def comando(els, y, cmd, t):
    """Mostra o prompt no instante t e 'digita' o comando. Devolve quando a digitação acaba."""
    els.append(f'<text x="30" y="{y}" class="o" style="animation-delay:{t:.2f}s">{prompt(cmd)}</text>')
    dur = 0.07 * len(cmd)
    els.append(f'<rect x="{30 + len(PROMPT) * CW:.1f}" y="{y - 16}" width="{len(cmd) * CW + 8:.1f}" height="22" '
               f'fill="{BG}" class="tp" style="animation:tp {dur:.2f}s steps({len(cmd)}) {t + 0.3:.2f}s forwards"/>')
    return t + 0.3 + dur + 0.25


def saida(els, y, conteudo, t, attrs=""):
    els.append(f'<text x="30" y="{y}" class="o" style="animation-delay:{t:.2f}s"{attrs}>{conteudo}</text>')


def impressora(t0, dt):
    """Impressora 3D à direita: o bico percorre cada camada enquanto ela é depositada."""
    cx, mesa, h = 830, 340, 12
    larguras = [90, 110, 124, 132, 136, 134, 128, 118, 104, 88, 74, 64, 60, 62, 72, 84]
    n = len(larguras)
    dur = n * dt + 0.6
    pct = lambda s: f"{s / dur * 100:.3f}%"
    camadas, kf_bico, kf_eixo = [], [], []
    for k, w in enumerate(larguras):
        y = mesa - (k + 1) * h
        esq, dir_ = cx - w / 2, cx + w / 2
        ini, fim, origem = (esq, dir_, "left") if k % 2 == 0 else (dir_, esq, "right")
        cor = LARANJA2 if k % 2 == 0 else LARANJA
        camadas.append(f'<rect x="{esq}" y="{y}" width="{w}" height="{h - 1}" rx="2" fill="{cor}" class="cam" '
                       f'style="transform-origin:{origem};animation:cresce {dt}s linear {t0 + k * dt:.2f}s forwards"/>')
        a, b = k * dt, (k + 1) * dt - 0.01
        kf_bico += [f"{pct(a)}{{transform:translate({ini}px,{y}px)}}", f"{pct(b)}{{transform:translate({fim}px,{y}px)}}"]
        kf_eixo += [f"{pct(a)}{{transform:translateY({y}px)}}", f"{pct(b)}{{transform:translateY({y}px)}}"]
    kf_bico.append("100%{transform:translate(935px,120px)}")
    kf_eixo.append("100%{transform:translateY(120px)}")
    css = f"@keyframes bico{{{''.join(kf_bico)}}}\n@keyframes eixo{{{''.join(kf_eixo)}}}"
    svg = f"""<g fill="#484f58">
<rect x="696" y="66" width="10" height="290" rx="2"/><rect x="954" y="66" width="10" height="290" rx="2"/>
<rect x="696" y="66" width="268" height="10" rx="2"/><rect x="686" y="352" width="288" height="10" rx="3"/>
</g>
<rect x="730" y="340" width="200" height="8" rx="2" fill="#6e7681"/>
{''.join(camadas)}
<g style="animation:eixo {dur:.2f}s linear {t0:.2f}s both"><rect x="706" y="-25" width="248" height="6" rx="2" fill="#6e7681"/></g>
<g style="animation:bico {dur:.2f}s linear {t0:.2f}s both">
<rect x="-14" y="-32" width="28" height="20" rx="4" fill="#484f58" stroke="#6e7681"/>
<rect x="-6" y="-12" width="12" height="6" fill="#8b949e"/><path d="M-4 -6H4L0 0Z" fill="{LARANJA}"/>
<circle cx="8" cy="-22" r="2.5" fill="{VERDE}" class="led"/>
</g>
<text x="{cx}" y="388" text-anchor="middle" fill="{CINZA}" style="font-size:13px">{escape(TAGLINE)}</text>"""
    return svg, css, n * dt


def terminal():
    els, t = [], 0.4
    t = comando(els, 96, "whoami", t)
    saida(els, 134, f'<tspan fill="{TEXTO}" font-size="30" font-weight="700">{escape(NOME)}</tspan>', t)
    t = comando(els, 174, "cat foco.txt", t + 0.3)
    saida(els, 202, f'<tspan fill="{ROXO}">Full Stack</tspan><tspan fill="{CINZA}">  &amp;&amp;  </tspan>'
                    f'<tspan fill="{LARANJA}">CAD 3D</tspan><tspan fill="{CINZA}">  &amp;&amp;  </tspan>'
                    f'<tspan fill="{CIANO}">Impressão 3D</tspan>', t)
    t = comando(els, 240, "ls ~/projetos", t + 0.3)
    saida(els, 268, "".join(f'<tspan fill="{AZUL}" font-weight="700">{d}/</tspan><tspan>  </tspan>'
                            for d in ["sistemas", "lojas-online", "pecas-3d", "automacoes-ia"]), t)
    t = comando(els, 306, "./fatiar peca.step && ./imprimir", t + 0.3)
    maquina, css_maquina, tempo = impressora(t, 0.35)
    saida(els, 334, f'<tspan fill="{CINZA}">[</tspan>', t)
    els.append(f'<rect x="44" y="321" width="300" height="14" rx="2" fill="{BARRA}" class="o" style="animation-delay:{t:.2f}s"/>')
    els.append(f'<rect x="44" y="321" width="300" height="14" rx="2" fill="{LARANJA}" class="bar" '
               f'style="animation:bar {tempo:.2f}s steps(16) {t:.2f}s forwards"/>')
    els.append(f'<text x="350" y="334" class="o" style="animation-delay:{t:.2f}s" fill="{CINZA}">]</text>')
    t += tempo + 0.3
    els.append(f'<text x="370" y="334" class="o" style="animation-delay:{t:.2f}s" fill="{VERDE}">✔ peça impressa</text>')
    t += 0.4
    saida(els, 372, prompt(), t)
    els.append(f'<rect x="{30 + len(PROMPT) * CW:.1f}" y="357" width="10" height="19" fill="{TEXTO}" class="cur" '
               f'style="animation-delay:{t:.2f}s"/>')
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="400" viewBox="0 0 1000 400">
<style>
text{{font-family:{FONTE};font-size:{FS}px;white-space:pre}}
.o{{opacity:0;animation:o .01s linear forwards}}
@keyframes o{{to{{opacity:1}}}}
.tp{{transform-box:fill-box;transform-origin:right}}
@keyframes tp{{to{{transform:scaleX(0)}}}}
.bar{{transform-box:fill-box;transform-origin:left;transform:scaleX(0)}}
@keyframes bar{{to{{transform:scaleX(1)}}}}
.cam{{transform-box:fill-box;transform:scaleX(0)}}
@keyframes cresce{{to{{transform:scaleX(1)}}}}
.cur{{opacity:0;animation:o .01s linear forwards,pisca 1s steps(1) infinite}}
@keyframes pisca{{50%{{fill:transparent}}}}
.led{{animation:pisca 1.2s steps(1) infinite}}
{css_maquina}
</style>
<rect x="1" y="1" width="998" height="398" rx="14" fill="{BG}" stroke="{BORDA}" stroke-width="2"/>
<path d="M1 15a14 14 0 0 1 14-14H985a14 14 0 0 1 14 14V46H1Z" fill="{BARRA}"/>
<rect x="1" y="46" width="998" height="1" fill="{BORDA}"/>
<circle cx="28" cy="24" r="7" fill="#ff5f57"/><circle cx="50" cy="24" r="7" fill="#febc2e"/><circle cx="72" cy="24" r="7" fill="#28c840"/>
<text x="500" y="29" text-anchor="middle" fill="{CINZA}" style="font-size:14px">{USUARIO}@{HOST}: ~ — bash</text>
{maquina}
{chr(10).join(els)}
</svg>"""


def cabecalho(num, nome):
    texto = f"// {num}  > {nome}()"
    fim_texto = 24 + len(texto) * 12 + 18
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="54" viewBox="0 0 1000 54">
<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{LARANJA}"/><stop offset="1" stop-color="{LARANJA}" stop-opacity="0"/></linearGradient></defs>
<rect x="1" y="1" width="998" height="52" rx="10" fill="{BG}" stroke="{BORDA}" stroke-width="2"/>
<text x="24" y="34" font-family="{FONTE}" font-size="20" style="white-space:pre"><tspan fill="{CINZA}">// {num}  </tspan><tspan fill="{LARANJA}">&gt; </tspan><tspan fill="{VERDE}" font-weight="700">{nome}</tspan><tspan fill="{TEXTO}">()</tspan></text>
<rect x="{fim_texto:.0f}" y="26" width="{976 - fim_texto:.0f}" height="2" fill="url(#g)"/>
</svg>"""


def cartao(titulo, linhas, tags):
    cores = [LARANJA, AZUL, VERDE]
    desc = "".join(f'<text x="24" y="{74 + i * 22}" fill="{TEXTO}" font-size="15">{escape(l)}</text>'
                   for i, l in enumerate(linhas))
    x, chips = 24, []
    for tag, cor in zip(tags, cores):
        chips.append(f'<circle cx="{x + 5}" cy="{127}" r="5" fill="{cor}"/>'
                     f'<text x="{x + 15}" y="132" fill="{CINZA}" font-size="13">{escape(tag)}</text>')
        x += 15 + len(tag) * 7.8 + 18
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="490" height="156" viewBox="0 0 490 156">
<style>text{{font-family:{FONTE}}}</style>
<rect x="1" y="1" width="488" height="154" rx="12" fill="{BG}" stroke="{BORDA}" stroke-width="2"/>
<text x="24" y="40" fill="{AZUL}" font-size="19" font-weight="700">{escape(titulo)}</text>
{desc}
{''.join(chips)}
<text x="466" y="40" text-anchor="end" fill="{VERDE}" font-size="20">↗</text>
</svg>"""


def rodape():
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="60" viewBox="0 0 1000 60">
<style>text{{font-family:{FONTE};font-size:18px;white-space:pre}}</style>
<rect x="1" y="1" width="998" height="58" rx="10" fill="{BG}" stroke="{BORDA}" stroke-width="2"/>
<text x="500" y="36" text-anchor="middle">{prompt("exit")}<tspan fill="{CINZA}">   # valeu pela visita! volte sempre</tspan></text>
</svg>"""


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    arquivos = {"terminal": terminal(), "rodape": rodape()}
    for num, nome in [("01", "sobre_mim"), ("02", "stack"), ("03", "projetos"), ("04", "atividade")]:
        arquivos[f"h-{nome}"] = cabecalho(num, nome)
    for arq, titulo, linhas, tags in PROJETOS:
        assert len(linhas) <= 2 and all(len(l) <= 46 for l in linhas), f"descrição longa demais: {arq}"
        arquivos[arq] = cartao(titulo, linhas, tags)
    for nome, svg in arquivos.items():
        (OUT / f"{nome}.svg").write_text(svg, encoding="utf-8")
    print(f"{len(arquivos)} SVGs gerados em {OUT}")
