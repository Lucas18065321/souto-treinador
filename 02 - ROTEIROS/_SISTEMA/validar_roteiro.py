"""Valida um roteiro falado (os 6 mecanismos do Briefing de roteiro) contra a Ficha de conteúdo do tema. Só biblioteca padrão.

Uso (de qualquer pasta):
  python validar_roteiro.py "<roteiro.md>"                   ERROS/AVISOS; sai com código 1 se houver erro
  python validar_roteiro.py "<roteiro.md>" --montar-fontes   valida e, se passar, escreve "## Texto para gravar",
                                                             "## Fontes" e "## Nível de certeza" a partir dos [#n]
                                                             (e tira a seção antiga "## Para gravar (TELA DIVIDIDA)")

FORMATO PADRÃO (o que o agente `roteirista` escreve; ver .claude/agents/02-roteiros/roteirista.md):
  ---
  ficha: "<Tema> - Ficha"        (ou  tema: <tema>; o nome antigo "Ficha - <tema>" também vale)
  formato: tela-dividida         (youtube: só confere duração se houver  duracao: "480-720")
  ---
  ## Roteiro
  1. RELEVÂNCIA EMOCIONAL — Fala, com [#n] logo depois de cada afirmação de evidência.
  2. CURIOSIDADE & EFEITO AHAA — Pode ter várias frases. [#8]
  ...
  ## Análise
  - CONTRASTE — por que foi usado (6 a 8 bullets)
  Sem corte de cena: só o texto falado. Rótulos: RELEVÂNCIA EMOCIONAL · CURIOSIDADE & EFEITO AHAA · CONTRASTE ·
  CONFLITO & MUDANÇA · TEMA & MORAL DA HISTÓRIA · LINGUAGEM FAMILIAR & IMAGENS MENTAIS (sem acento/maiúscula
  tanto faz; separador —, – ou -), em qualquer ordem. A chamada para ação fica dentro de uma parte.
  ERRO: rótulo que não é um dos 6 · numeração fora de sequência · placeholder entre colchetes ([GANCHO], [CTA]…) ·
        linha "> tela:" ou "gancho visual" · expressões proibidas (Briefing, seção 9) · e todas as checagens de
        evidência e de ética (id da ficha, verbo × certeza, número × linha, diretriz sem [#n], palavras proibidas,
        promessa de resultado, antes/depois, depoimento de aluno, preço, prescrição de dieta/suplemento/remédio).
  AVISO: frase com mais de 22 palavras · clichês · sigla/jargão no texto falado · menos de 4 ou mais de 10 partes ·
         sem TEMA & MORAL DA HISTÓRIA · "## Análise" ausente ou fora de 6 a 8 bullets · rótulo de bullet fora dos 6
         (aceita FORMATO e AIDA) · ordem de treino com número para quem assiste (parece prescrição individual).

ESTRUTURA VIRAL (vídeo animado com voz de IA; frontmatter  estrutura: viral). "## Roteiro" com as partes
  1. GANCHO — · 2. RETENÇÃO — · DESENVOLVIMENTO — · REENGAJAMENTO — (os dois se alternam e podem repetir:
  "DESENVOLVIMENTO 2 — ") · ENCERRAMENTO — · CHAMADA PRA AÇÃO — (a última). "## Ganchos": 3 opções em bullets, a
  escolhida marcada com "(recomendado)".
  ERRO: ordem fora da estrutura · rótulo fora das partes · relato em 1ª pessoa ("eu perdi", "meus alunos": a voz de
        IA não tem história) · e as mesmas checagens de evidência e de ética do formato padrão.
  AVISO: tamanho das partes (gancho, reengajamento e encerramento com 1 frase; retenção com 2 ou 3) · miolo com menos
         de 2 desenvolvimentos e 2 reengajamentos · CTA sem pedido de comentário ou sem a PALAVRA em maiúsculas ·
         duração fora de 30 a 60 s · "## Ganchos" ausente, sem 3 opções ou sem "(recomendado)".

Ética (Código de Ética do Profissional de Educação Física, Resolução CONFEF 307/2015, + regras da marca): promessa de
resultado com número no corpo de quem assiste ("7 kg em um mês", "ganhe 5 kg de músculo", "10 cm de cintura em 30
dias") é ERRO; o CTA pode prometer o que o produto entrega. Prescrever dieta, cardápio, calorias ou suplemento com dose
para quem assiste é ERRO (atividade do nutricionista, Lei 8.234/1991); mandar parar/trocar remédio ou usar hormônio
também é ERRO (assunto do médico).

FORMATO ANTIGO (só por compatibilidade): se "## Roteiro" não tiver nenhuma linha numerada, mas tiver linhas
"[GATILHO] Frase [#n]" (e "> tela: …"), vale o caminho antigo: 9 gatilhos, espinha GANCHO → tensão → EFEITO AHÁ →
MORAL → CTA.

Referências: [#n] = linha n da tabela "Afirmações prontas"; [#N2] = 2º item de "Números de impacto";
[#M2] = 2ª linha da tabela "Mitos e meias-verdades" (coluna "O que a evidência diz");
[#H1] = linha H1 da tabela "Histórias reais (verificáveis)" (pessoa/caso real com link; números conferidos na linha).
As fontes saem da própria ficha (nota-base + localizador) e da linha "Vancouver:"/campo "link:" da nota-base ou do JSON
do artigo no catálogo: nenhuma referência é escrita por IA. Este módulo também é usado por
03 - CARROSSÉIS E ARTE/Gerador/validar_carrossel.py e pelo hook .claude/hooks/validar_peca.py.

Fichas: "01 - BASE CIENTÍFICA/**/<Tema> - Ficha.md" (fora de _MÁQUINA) e, só para o teste do motor,
"02 - ROTEIROS/_SISTEMA/teste/" (Fichas fictícias com nome começando por TESTE). Caminhos relativos a este arquivo:
nada depende do usuário nem da pasta de onde o comando é rodado.
"""
import difflib
import json
import os
import re
import sys
import unicodedata
from pathlib import Path

AQUI = Path(__file__).resolve().parent                 # .../02 - ROTEIROS/_SISTEMA
RAIZ = AQUI.parents[1]                                 # raiz do repositório
BASE = RAIZ / "01 - BASE CIENTÍFICA"
# Fichas fictícias do teste do motor (nunca na base). Ver _SISTEMA/teste/LEIA-ME.md.
TESTE = AQUI / "teste"
# Fichas = BASE/<área>/<Tema> - Ficha.md (qualquer pasta, menos _MÁQUINA). Notas de fonte processadas: _MÁQUINA/fontes-processadas.
MAQUINA = BASE / "_MÁQUINA"
PROCESSADAS = MAQUINA / "fontes-processadas"
# Catálogo de artigos (biblioteca.py): se a Ficha cita um artigo do catálogo, a referência sai do JSON do artigo.
ARTIGOS_JSON = MAQUINA / "artigos"
PALAVRAS_POR_SEG = 2.5
DURACAO_PADRAO = (45, 75)

GATILHOS = ["GANCHO VISUAL", "CONFLITO UNIVERSAL", "RELEVÂNCIA EMOCIONAL", "CONTRASTE", "FAMILIARIDADE",
            "DEBATE MENTAL", "EFEITO AHÁ", "MORAL DA HISTÓRIA", "CTA"]
# Tensão: precisa aparecer (a 1ª vez) antes do último EFEITO AHÁ. Espinha do formato antigo:
# GANCHO abre · tensão (repete e mistura à vontade) · EFEITO AHÁ · MORAL DA HISTÓRIA · CTA fecha.
TENSAO = ["CONFLITO UNIVERSAL", "RELEVÂNCIA EMOCIONAL", "CONTRASTE", "FAMILIARIDADE", "DEBATE MENTAL"]
NIVEIS = ["muito baixa", "baixa", "moderada", "alta"]
CALIBRADOR = {0: '"não se sabe"', 1: '"pode"', 2: '"provavelmente"', 3: 'verbo direto ("reduz", "aumenta")'}

# Formato padrão (Briefing de roteiro): partes numeradas "N. MECANISMO — fala" + "## Análise".
MECANISMOS = ["RELEVÂNCIA EMOCIONAL", "CURIOSIDADE & EFEITO AHAA", "CONTRASTE", "CONFLITO & MUDANÇA",
              "TEMA & MORAL DA HISTÓRIA", "LINGUAGEM FAMILIAR & IMAGENS MENTAIS"]
ROTULOS_ANALISE = MECANISMOS + ["FORMATO", "DISTRIBUIÇÃO AIDA", "AIDA"]
MORAL = "TEMA & MORAL DA HISTÓRIA"
PARTES_MIN, PARTES_MAX = 4, 10
BULLETS_MIN, BULLETS_MAX = 6, 8
MAX_PALAVRAS_FRASE = 22
EXPRESSOES_PROIBIDAS = [  # (regex sobre texto sem acento e minúsculo, nome na mensagem) — Briefing, seção 9
    (r"\ba verdade que doi\b", "a verdade que dói"),
    (r"\bnao e sobre\b.{1,120}?\be sobre\b", "não é sobre … é sobre …"),
    (r"\bo resultado\s*\?", "o resultado?"),
    (r"\bpay[- ]?off\b", "pay-off"),
    (r"\bunderdog\b", "underdog"),
    (r"\bb[- ]?roll\b", "b-roll"),
    (r"\btakeaway\b", "takeaway"),
    (r"\bhooks?\b", "hook"),
    (r"\bchain[- ]of[- ]thought\b", "chain-of-thought"),
    (r"\bjailbreak\b", "jailbreak"),
]
CLICHES = [(r"\bvoce nao vai acreditar\b", "você não vai acreditar"), (r"\bisso vai mudar tudo\b", "isso vai mudar tudo"),
           (r"\bpouca gente sabe\b", "pouca gente sabe"), (r"\bsem desculpas\b", "sem desculpas"),
           (r"\bno pain,? no gain\b", "no pain no gain"), (r"\bfoco,? forca e fe\b", "foco, força e fé")]
# Promessa de resultado com número no corpo de quem assiste (ERRO). O CTA pode prometer o que o produto entrega
# ("o guia traz 3 treinos"), nunca "X kg em N dias", "ganhe 5 kg de músculo" ou "10 cm de cintura em 30 dias".
# Garantia já está em PROIBIDAS.
# Prazo curto de marketing (até 8 semanas ou 3 meses). Fato de estudo com "grupo", "participantes" etc. vira AVISO.
_PRAZO = (r"(?:(?:\d+|um|uma|dois|duas|tres|quatro|cinco|seis|sete|oito|nove|dez|quinze|vinte|trinta)\s+dias?|"
          r"(?:[1-8]|uma|duas|tres|quatro|cinco|seis|sete|oito)\s+semanas?|(?:[1-3]|um|dois|tres)\s+(?:mes|meses))")
_CONTEXTO_ESTUDO = r"\b(?:grupos?|participantes|voluntari\w+|estudos?|pesquisas?|ensaios?|em media|na media|revis\w+)\b"
_MEDIDA = r"(?:kg|kgs|quilos?|kilos?|cm|centimetros?)"
PROMESSA_NUM = [
    (r"\b\d+(?:[.,]\d+)?\s?" + _MEDIDA + r"\s+(?:a menos\s+|a mais\s+)?(?:de\s+\w+\s+)?(?:na\s+\w+\s+|no\s+\w+\s+)?em\s+"
     r"(?:(?:so|apenas|ate|menos de)\s+)?" + _PRAZO + r"\b", "medida × prazo"),
    (r"\b\d+(?:[.,]\d+)?\s?%\s+(?:a menos\s+)?de\s+gordura\s+em\s+(?:(?:so|apenas|ate|menos de)\s+)?" + _PRAZO + r"\b",
     "% de gordura × prazo"),
    (r"(?<!nao )(?<!nunca )\b(?:perder|eliminar|emagrecer|secar|derreter|ganhar)\s+ate\s+\d|"
     r"\b(?:perca|percam|elimine|eliminem|emagreca|emagrecam|seque|sequem|derreta|derretam|ganhe|ganhem|conquiste)\s+"
     r"(?:\w+\s+){0,2}?\d+(?:[.,]\d+)?\s?" + _MEDIDA + r"\b|"
     r"(?<!quem )(?<!que )\b(?:quer|vai|vamos)\s+(?:te\s+)?(?:fazer\s+)?(?:perder|emagrecer|eliminar|secar|ganhar)\b"
     r"[^.!?;]{0,25}?\d+(?:[.,]\d+)?\s?" + _MEDIDA + r"\b",
     "meta de quilos/medidas"),
]
# Ética do Profissional de Educação Física (Resolução CONFEF 307/2015) + limites legais das outras profissões.
# (regex sobre texto sem acento e minúsculo, mensagem). ERRO.
ETICA_ERRO = [
    (r"\b(?:fotos?|videos?|imagens?)\s+de\s+antes\s+e\s+depois\b|\bmeu\s+antes\s+e\s+depois\b"
     r"|\bantes\s+e\s+depois\s+d[aeo]s?\s+(?:meus?|minhas?|nossos?|nossas?)?\s*(?:alunos?|alunas?|clientes?|consultorias?)\b"
     r"|\bantes\s*/\s*depois\b",
     "antes/depois de aluno ou cliente não entra em conteúdo aberto (marca + sigilo e dignidade do aluno, CONFEF 307/2015)"),
    (r"\b(?:meus?|minhas?|nossos?|nossas?)\s+(?:alunos?|alunas?|clientes?)\b[^.!?]{0,50}?\b(?:perdeu|perderam|emagreceu|"
     r"emagreceram|ganhou|ganharam|secou|secaram|eliminou|eliminaram|conquistou|conquistaram|transformou|curou|"
     r"tirou|tiraram|largou|largaram)\b",
     "depoimento/resultado de aluno não entra em conteúdo aberto (sigilo e respeito ao aluno, CONFEF 307/2015)"),
    (r"r\$\s?\d|\b\d+(?:[.,]\d+)?\s?reais\b|\bpor apenas\b|\bcupom\b|\bdesconto de\b|\bpromocao (?:imperdivel|relampago)\b",
     "preço ou promoção em conteúdo aberto (regra da marca; CONFEF 307/2015 veda concorrência por preço aviltado)"),
    (r"\b(?:coma|comam|tome|tomem|ingira|ingiram|consuma|consumam|beba|bebam)\s+(?:\w+\s+){0,3}?\d+(?:[.,]\d+)?\s?"
     r"(?:g|gramas?|kcal|calorias|mg|ml|colheres?|scoops?|doses?|capsulas?|comprimidos?)\b"
     r"|\b(?:monte|montei|faca|segue|siga)\s+(?:a\s+)?(?:sua|minha|essa|esta)\s+dieta\b|\bdieta de \d+\s?(?:kcal|calorias)\b"
     r"|\bcardapio\s+(?:pra|para)\s+(?:voce|voces|secar|emagrecer|ganhar|definir)\b",
     "prescrição de dieta/suplemento para quem assiste: é atividade do nutricionista (Lei 8.234/1991) — eduque com a "
     "Ficha, sem ordem nem dose para a pessoa"),
    (r"\b(?:pare|parem|suspenda|suspendam|troque|troquem|largue|larguem)\s+(?:de\s+)?(?:tomar\s+)?(?:o\s+|a\s+|os\s+|as\s+|"
     r"seu\s+|sua\s+|seus\s+|suas\s+)?(?:remedios?|medicamentos?|medicacao|medicacoes|insulina|hormonios?|estatinas?)\b"
     r"|\b(?:use|usem|tome|tomem|aplique|apliquem|comece|comecem)\s+(?:a\s+)?(?:\w+\s+){0,2}?(?:anabolizantes?|"
     r"esteroides?|testosterona|hormonios?|ozempic|semaglutida|tirzepatida|mounjaro)\b",
     "ordem sobre remédio ou hormônio: é assunto do médico (fora da competência do profissional de Educação Física)"),
]
# AVISO: ordem de treino com número para quem assiste (prescrição individual em conteúdo aberto). Faixa da evidência
# ("de 10 a 20 séries por semana, segundo a revisão [#n]") é educação; "faça 4 séries de 12" é ordem.
ETICA_AVISO = [
    (r"\b(?:faca|facam|faz)\s+(?:\w+\s+){0,2}?\d+\s+(?:series|repeticoes|reps|minutos|treinos)\b",
     "ordem de treino com número para quem assiste: em conteúdo aberto, fale da faixa que a evidência mostra (com [#n]) "
     "e lembre que a dose é individual (avaliação com profissional)"),
]

# Estrutura viral (vídeo animado com voz de IA). Frontmatter "estrutura: viral".
VIRAIS = ["GANCHO", "RETENÇÃO", "DESENVOLVIMENTO", "REENGAJAMENTO", "ENCERRAMENTO", "CHAMADA PRA AÇÃO"]
_VIRAL_ALIAS = {"CHAMADA PARA AÇÃO": "CHAMADA PRA AÇÃO"}
DURACAO_VIRAL = (30, 60)
FRASES_VIRAIS = {"GANCHO": (1, 1), "RETENÇÃO": (2, 3), "REENGAJAMENTO": (1, 1), "ENCERRAMENTO": (1, 1)}
# A voz é de IA: nada de relato pessoal nem de aluno (seria história inventada e depoimento).
RELATO_1A_PESSOA = (r"\beu\s+(?:ja\s+|tambem\s+)?(?:perdi|emagreci|sequei|eliminei|ganhei|tirei|baixei|curei|venci|sai|"
                    r"treinei|levantei)\b"
                    r"|\bmeu resultado\b|\bmeus? (?:pacientes?|alunos?|clientes?)\b|\bminhas? (?:pacientes?|alunas?|clientes?)\b")
# Sigla/jargão no texto falado (AVISO): siglas de treino e de estatística. Sem diferenciar maiúscula: RIR, RPE, VO2,
# mTOR, mg/dL, %, "risco relativo", "tamanho de efeito", "meta-regressão". Só em maiúsculas (senão pegam palavras
# comuns): RM/1RM, IC, NNT, TG, HIIT.
JARGAO_CI = re.compile(r"\bRIR\b|\bRPE\b|\bVO\s?2(?:\s?m[aá]x)?\b|\bmTOR\b|\bmg\s?/\s?dL\b|\brisco relativo\b"
                       r"|\btamanho de efeito\b|\bmeta-?regress[aã]o\b|\bsarcopl[aá]sm\w*|\bmiofibril\w*|%", re.I)
JARGAO_CS = re.compile(r"\b\d*RM\b|\b(?:IC|NNT|TG|HIIT|DOMS)\b")

def sa(t):
    """Minúsculas sem acento (mesmo comprimento do texto em NFC)."""
    return "".join(c for c in unicodedata.normalize("NFD", t.lower()) if unicodedata.category(c) != "Mn")


def nfc(t):
    return unicodedata.normalize("NFC", t)


# ---------- calibração do verbo ----------
HEDGES = [  # (nível que o calibrador expressa, regex sobre texto sem acento)
    (0, r"nao se sabe|ninguem sabe|nao sabemos|ainda nao se sabe|\bincert[oa]s?\b|nao (?:esta|e|ficou) claro"
        r"|nao ha (?:evidencias?|provas?|dados)|faltam (?:estudos|dados|provas)|evidencias? (?:insuficientes?|fracas?)"
        r"|ninguem (?:mostrou|provou|demonstrou)"),
    (1, r"\bpode(?:m|ria|riam)?\b|\btalvez\b|\bsuger(?:e|em|iu|iram)\b|\bindicios\b|\bpossivelmente\b"
        r"|\be possivel que\b|\bha sinais\b"),
    (2, r"\bprovavelmente\b|\bprovavel\b|\btende(?:m)? a\b|\bparece(?:m)?\b|\btudo indica\b"),
]
_ALVO = (r"(?=\s+(?:o|a|os|as|um|uma|seu|sua|seus|suas|esse|essa|isso|em|ate|mais|menos|\d|forca|musculos?|massa"
         r"|hipertrofia|gordura|desempenho|rendimento|dor|dores|lesao|lesoes|quedas?|ossos?|pressao|glicose|peso|risco"
         r"|metabolismo|colesterol|infarto|equilibrio|postura)\b)")
VERBOS = {  # verbos de efeito "fortes" (afirmação sem calibrador); heurística sobre texto sem acento
    "reduzir": r"\breduz(?:em|ir|iu|iram|indo)?\b",
    "diminuir": r"\bdiminu(?:i|em|ir|iu|iram|indo)\b",
    "aumentar": r"\baument(?:a|am|ar|ou|aram|ando)\b",
    "elevar": r"\belev(?:a|am|ar|ou|aram|ando)\b",
    "baixar": r"\b(?:a)?baix(?:ar|ou|aram|ando)\b|\b(?:a)?baixam?\b" + _ALVO,
    "derrubar": r"\bderrub(?:a|am|ar|ou|aram)\b",
    "melhorar": r"\bmelhor(?:a|am|ar|ou|aram)\b" + _ALVO,
    "piorar": r"\bpior(?:a|am|ar|ou|aram)\b" + _ALVO,
    "prevenir": r"\bprevin(?:e|em)\b|\bpreven(?:ir|iu|iram)\b",
    "proteger": r"\bproteg(?:e|em|er|eu|eram)\b",
    "evitar": r"\bevit(?:a|am|ar|ou|aram)\b",
    "causar": r"\bcaus(?:am|ar|ou|aram)\b|\bcausa\b" + _ALVO,
    "provocar": r"\bprovoc(?:a|am|ar|ou|aram)\b",
    "controlar": r"\bcontrol(?:a|am|ar|ou|aram)\b",
    "tratar": r"\btrat(?:a|am|ar|ou|aram)\b" + _ALVO,
    "zerar": r"\bzer(?:a|am|ar|ou|aram)\b",
    "mudar": r"\bmud(?:a|am|ar|ou|aram)\b" + _ALVO,  # só com alvo: "a embalagem muda." não é afirmação clínica
    "funcionar": r"\bfuncion(?:a|am|ar|ou|aram)\b" + _ALVO,
    "resolver": r"\bresolv(?:e|em|er|eu|eram)\b",
    "ajudar": r"\bajud(?:a|am|ar|ou|aram)\s+a\b",
    "combater": r"\bcombat(?:e|em|er|eu)\b",
    "queimar": r"\bqueim(?:a|am|ar)\b",
    "dispensar": r"\bdispens(?:a|am|ar|ou)\b",
    "salvar": r"\bsalv(?:a|am|ar|ou)\s+(?:vidas|a vida|o coracao)",
    "fazer bem/mal": r"\bfaz(?:em)?\s+(?:bem|mal)\b",
    "comprovar": r"\bcomprovad[oa]s?\b|\bcomprova(?:m)?\b|\bprovad[oa]s?\b|\bprova que\b",
    "limpar artérias": r"\blimp(?:a|am|ar)\s+(?:as\s+)?arterias|\bdesent(?:op|up)\w*",
    # efeitos típicos das promessas de academia
    "acelerar": r"\bacelera(?:m|r|ou|ram)?\b",
    "emagrecer": r"\bemagrec(?:e|em)\b",
    "fortalecer": r"\bfortalec(?:e|em|er|eu|eram)\b",
    "definir": r"\bdefin(?:e|em)\b" + _ALVO,
    "fazer ganhar/perder": r"\bfaz(?:em)?\s+(?:ganhar|perder)\b",
}
PROIBIDAS = [
    (r"\bcur(?:a|as|ar|ado|ada|ados|adas|am|ou)\b", "cura"),
    (r"\bmilagr\w*", "milagre"),
    (r"\bgarant\w*", "garantido"),
    (r"\bsegredos?\b", "segredo"),
    (r"\bnunca mais\b", "nunca mais"),
    (r"\b100\s?%|\bcem por cento\b", "100%"),
    (r"\bsem esforco\b", "sem esforço"),
]
# Sem [#n]: posição de diretriz/órgão é ERRO; menção a diretriz/estudo é AVISO.
RECOMENDA = (r"\b(?:recomenda|admite|aprova|autoriza|contraindica|proibe|libera|condena|preconiza|endossa)m?\b"
             r"|\b(?:recomendad|contraindicad|aprovad|proibid)[oa]s?\b")
CITA_FONTE = (r"\bdiretriz(?:es)?\b|\bacsm\b|\bnsca\b|\bsbme\b|\boms\b|\bconfef\b|\banvisa\b|\bcochrane\b|\bensaios?\b"
              r"|\bposicionamentos?\b|\bposition stand\b"
              r"|\bmeta-?analises?\b|\brevis(?:ao|oes) sistematicas?\b|\bestudos?\b|\bpesquisas?\b")
NEGACAO = {"nao", "nenhum", "nenhuma", "sem", "nem", "mito", "mitos", "promete", "prometem", "prometer",
           "promessa", "promessas", "vende", "vendem", "vender"}
# Fala relatada (o mito enunciado para ser desmentido): o verbo de efeito depois destas marcas, na mesma oração, não é
# afirmação do Jorge e fica fora do verbo × certeza. Trecho entre aspas também fica fora (citação).
RELATO = (r"\bpromet\w*|\bpromessas?\b|\bvend(?:e|em|ia|iam|ido|ida|idos|idas)\b|\bmitos?\b|\bcrenca\b|\bboato\b"
          r"|\b(?:diz|dizem|dizia|diziam|jura|juram|repete|repetem|garantem?) que\b|\bcircula(?:m)?\b|\bsegundo (?:o|a) (?:rotulo|propaganda|anuncio)\b")
_ASPAS = re.compile(r'"[^"\n]*"|“[^”\n]*”|«[^»\n]*»|‘[^’\n]*’')
# Número arredondado em linguagem leiga ("quase 36 pontos" para 35,8): aceito até 10% do número da ficha, no sentido
# que a palavra diz. "1 em cada 3" também vale para 33% (mesma tolerância).
APROX = [  # (regex sobre texto sem acento, logo antes do número; sentido: -1 = real ≤ escrito, +1 = real ≥ escrito, 0 = tanto faz)
    (r"\b(?:quase|menos de|ate|abaixo de)\s*$", -1),
    (r"\b(?:mais de|acima de|pelo menos|no minimo|passa de|passou de)\s*$", 1),
    (r"\b(?:cerca de|perto de|em torno de|por volta de|aproximadamente|uns|umas|algo como|na casa d[oa]s?)\s*$", 0),
]
TOLERANCIA = 0.10


def sem_citacao(t):
    """Trecho entre aspas vira espaço (mesmo comprimento): citação não passa pelo verbo × certeza."""
    return _ASPAS.sub(lambda m: " " * len(m.group(0)), t)


def relatado(oracao, verbo):
    """True se o verbo de efeito vem depois de uma marca de fala relatada ("o pote promete baixar…")."""
    m = re.search(re.escape(verbo), oracao)
    return bool(m and re.search(RELATO, oracao[:m.start()]))


def _aproximado(valor, antes, permitidos):
    """Número arredondado com a palavra certa ("quase", "mais de", "cerca de") e até 10% de um número da ficha."""
    a = sa(antes)[-30:]
    for rx, sentido in APROX:
        if re.search(rx, a):
            return any(p > 0 and abs(valor - p) / p <= TOLERANCIA and (sentido == 0 or (p - valor) * sentido >= 0)
                       for p in permitidos)
    return False


def _fracoes_ok(texto, permitidos):
    """Posições dos números de "1 em cada 3" que equivalem a um percentual da ficha (33%) com a mesma tolerância."""
    ok = set()
    for m in re.finditer(r"(?<![\w.,])(\d+)\s+(?:em cada|a cada|de cada)\s+(\d+)\b", texto):
        k, n = int(m.group(1)), int(m.group(2))
        if n and any(p > 0 and abs(k / n * 100 - p) / p <= TOLERANCIA for p in permitidos):
            ok |= {m.start(1), m.start(2)}
    return ok

_SEP = re.compile(r"([.;:!?…]+)(?=\s|$)|\s[—–]\s|\b(?:mas|porem|entretanto|contudo)\b")


def oracoes(t):
    """Divide um texto (já sem acento) em orações: [(texto, é_pergunta)]."""
    res, ini = [], 0
    for m in _SEP.finditer(t):
        trecho = t[ini:m.start()].strip()
        if trecho:
            res.append((trecho, "?" in (m.group(1) or "")))
        ini = m.end()
    resto = t[ini:].strip()
    if resto:
        res.append((resto, False))
    return res


def hedge(t):
    """(nível, palavra) do calibrador mais cauteloso da oração, ou (None, None)."""
    achados = [(n, m.group(0)) for n, rx in HEDGES for m in [re.search(rx, t)] if m]
    return min(achados) if achados else (None, None)


def verbos_fortes(t):
    return {nome: m.group(0) for nome, rx in VERBOS.items() for m in [re.search(rx, t)] if m}


def nivel_da_certeza(texto):
    """Lê a coluna Certeza da ficha → 0..3 (muito baixa..alta). Em texto misto, fica com o nível mais baixo."""
    t = sa(texto).replace("“", '"').replace("”", '"')
    m = re.search(r'(?:usar|dizer)\s+"([^"]+)"', t)
    if m:
        n, _ = hedge(m.group(1))
        if n is not None:
            return n, True
    t = re.sub(r"\([^)]*\)", " ", t)
    achados = []
    if re.search(r"muito baixa|criticamente baixa", t):
        achados.append(0)
        t = re.sub(r"muito baixa|criticamente baixa", " ", t)
    if re.search(r"\bbaixa\b", t):
        achados.append(1)
    if re.search(r"nao graduad|sem grau", t):
        achados.append(1)
    if re.search(r"\bmoderada\b", t):
        achados.append(2)
    if re.search(r"\balta\b", t):
        achados.append(3)
    m = re.search(r"\bnivel\s+([abc])\b", t)
    if m:
        achados.append({"a": 3, "b": 2, "c": 1}[m.group(1)])
    if achados:
        return min(achados), True
    if re.search(r"\bforte\b", t):
        return 3, True
    return 1, False  # não reconhecida: trata como baixa (conservador)


# ---------- números ----------
_NUM = re.compile(r"(?<![\w.,])(\d+(?:[.,]\d+)*)(\s?%)?")


def numeros(texto, com_pos=False):
    """[(valor, como_escrito, é_percentual)] de todos os números em algarismos (com_pos: + posição no texto)."""
    out = []
    for m in _NUM.finditer(texto):
        i = m.start()
        if i >= 2 and texto[i - 1] == "-" and texto[i - 2].isalpha():  # ômega-3
            continue
        if re.search(r"CREF-?\s?\d{0,2}[\s/-]*$", texto[max(0, i - 8):i]):  # registro profissional (CREF 000000-G/UF): não é dado
            continue
        bruto = m.group(1)
        if re.fullmatch(r"\d{1,3}(?:\.\d{3})+", bruto):
            s = bruto.replace(".", "")
        elif "," in bruto:
            s = bruto.replace(".", "").replace(",", ".")
        else:
            s = bruto
        try:
            out.append((float(s), bruto + (m.group(2) or "").strip(), bool(m.group(2))) + ((i,) if com_pos else ()))
        except ValueError:
            pass
    return out


# ---------- ficha ----------
def frontmatter(texto):
    """(dict, corpo, nº da linha onde o corpo começa)."""
    fm = {}
    if not texto.startswith("---"):
        return fm, texto, 1
    linhas = texto.splitlines()
    for k in range(1, len(linhas)):
        if linhas[k].strip() == "---":
            for l in linhas[1:k]:
                m = re.match(r"^([\w\-]+)\s*:\s*(.*)$", l)
                if m:
                    fm[m.group(1)] = m.group(2).strip().strip('"').strip("'")
            return fm, "\n".join(linhas[k + 1:]), k + 2
    return fm, texto, 1


def secoes(corpo):
    out, atual = {}, None
    for l in corpo.splitlines():
        m = re.match(r"^##\s+(.+?)\s*$", l)
        if m:
            atual = m.group(1)
            out[atual] = []
        elif atual:
            out[atual].append(l)
    return {k: "\n".join(v) for k, v in out.items()}


def _celulas(l):
    return [c.strip() for c in l.strip().strip("|").split("|")]


def _analisar_afirmacao(texto):
    """Calibradores e verbos fortes ditos sem calibrador na própria redação da ficha."""
    hedges, livres = set(), set()
    for o, _ in oracoes(sa(texto)):
        n, _ = hedge(o)
        if n is not None:
            hedges.add(n)
        else:
            livres |= set(verbos_fortes(o))
    return hedges, livres


def _fonte_final(t):
    # "… (Wang 2023, Tab. 2; não graduada)." → "Wang 2023, Tab. 2" (só as partes com ano)
    p = re.search(r"\(([^()]*\d{4}[^()]*)\)\s*\.?\s*$", t)
    if p:
        partes = [x.strip() for x in p.group(1).split(";") if re.search(r"\d{4}", x)]
        if partes:
            return "; ".join(partes)
    m = re.search(r"((?:[A-ZÀ-Ý][\wÀ-ÿ/]*\s)+\d{4}(?:,\s*[^()]*?)?)\.?\s*$", t)
    return m.group(1).strip() if m else ""


def carregar_ficha(caminho):
    texto = Path(caminho).read_text(encoding="utf-8-sig")
    fm, corpo, _ = frontmatter(texto)
    sec = secoes(corpo)
    itens = {}
    for titulo, conteudo in sec.items():
        tt = sa(titulo)
        if tt.startswith("afirmacoes prontas"):
            linhas = [l for l in conteudo.splitlines() if l.strip().startswith("|")]
            if len(linhas) < 3:
                continue
            cab = [sa(c) for c in _celulas(linhas[0])]
            col = lambda chave: next((k for k, c in enumerate(cab) if chave in c), None)
            ci, ct, cc, cn, cf = col("#"), col("afirmac"), col("certeza"), col("numero"), col("fonte")
            for l in linhas[2:]:
                c = _celulas(l)
                if ci is None or ci >= len(c) or not re.fullmatch(r"\d+", c[ci]):
                    continue
                pega = lambda k: c[k] if k is not None and k < len(c) else ""
                nivel, reconhecido = nivel_da_certeza(pega(cc))
                hedges, livres = _analisar_afirmacao(pega(ct))
                itens[c[ci]] = {"id": c[ci], "texto": pega(ct), "certeza": pega(cc), "numero": pega(cn),
                                "fonte": pega(cf), "linha": " | ".join(c), "nivel": nivel,
                                "certeza_reconhecida": reconhecido, "hedges": hedges, "livres": livres}
        elif tt.startswith("mitos"):
            linhas = [l for l in conteudo.splitlines() if l.strip().startswith("|")]
            if len(linhas) < 3:
                continue
            cab = [sa(c) for c in _celulas(linhas[0])]
            col = lambda chave: next((k for k, c in enumerate(cab) if chave in c), None)
            cm, ce, cc, cf = col("mito"), col("evidencia"), col("certeza"), col("fonte")
            for k, l in enumerate(linhas[2:], 1):
                c = _celulas(l)
                pega = lambda j: c[j] if j is not None and j < len(c) else ""
                nivel, _ = nivel_da_certeza(pega(cc))
                hedges, livres = _analisar_afirmacao(pega(ce))
                itens[f"M{k}"] = {"id": f"M{k}", "texto": pega(ce), "certeza": pega(cc), "numero": "",
                                  "fonte": pega(cf), "linha": " | ".join(c), "nivel": nivel,
                                  "certeza_reconhecida": True, "hedges": hedges, "livres": livres,
                                  "mito": pega(cm)}
        elif tt.startswith("historias reais"):
            # | # | Fato (como pode ser contado) | Fonte (link) | → [#H1]… História real e verificável (pessoa/caso
            # conhecido) para o gancho e a narrativa; não é evidência clínica, então não passa pela calibração do verbo.
            linhas = [l for l in conteudo.splitlines() if l.strip().startswith("|")]
            if len(linhas) < 3:
                continue
            cab = [sa(c) for c in _celulas(linhas[0])]
            col = lambda chave: next((k for k, c in enumerate(cab) if chave in c), None)
            ci, ctx, cf = col("#"), col("fato"), col("fonte")
            for l in linhas[2:]:
                c = _celulas(l)
                pega = lambda j: c[j] if j is not None and j < len(c) else ""
                hid = pega(ci).upper()
                if not re.fullmatch(r"H\d+", hid):
                    continue
                itens[hid] = {"id": hid, "texto": pega(ctx), "certeza": "história real verificável (fonte jornalística)",
                              "numero": "", "fonte": pega(cf), "linha": " | ".join(c), "nivel": None,
                              "certeza_reconhecida": True, "hedges": set(), "livres": set(), "historia": True}
        elif tt.startswith("numeros de impacto"):
            k = 0
            for l in conteudo.splitlines():
                if re.match(r"^\s*[-*]\s+", l):
                    k += 1
                    t = re.sub(r"^\s*[-*]\s+", "", l).replace("**", "")
                    itens[f"N{k}"] = {"id": f"N{k}", "texto": t, "certeza": "dado descritivo (Números de impacto)",
                                      "numero": "", "fonte": _fonte_final(t), "linha": t, "nivel": None,
                                      "certeza_reconhecida": True, "hedges": set(), "livres": set()}
    for it in itens.values():
        it["numeros"] = {v for v, _, _ in numeros(it["linha"])}
    notas = re.findall(r"\[\[([^\]]+)\]\]", fm.get("notas_base", "")) or re.findall(r"\[\[([^\]|]+)", sec.get("Para aprofundar", ""))
    return {"nome": Path(caminho).stem, "caminho": str(caminho), "fm": fm, "itens": itens, "notas": notas}


def fichas_da_base():
    """Todas as Fichas: 01 - BASE CIENTÍFICA/**/<Tema> - Ficha.md (fora de _MÁQUINA), em ordem alfabética, + as Fichas
    fictícias de _SISTEMA/teste (nome começando por TESTE). Pasta ausente: simplesmente não entra (sem erro)."""
    out = []
    for d, dirs, arqs in os.walk(BASE):
        dirs[:] = [x for x in dirs if nfc(x) != nfc("_MÁQUINA") and not x.startswith(".")]
        out += [Path(d) / a for a in arqs if nfc(a).endswith(" - Ficha.md")]
    if TESTE.is_dir():
        out += [p for p in TESTE.glob("*.md") if nfc(p.name).endswith(" - Ficha.md") and sa(p.name).startswith("teste")]
    return sorted(out, key=lambda p: sa(nfc(p.stem)))


def _tema_da_ficha(stem):
    return nfc(stem)[:-len(" - Ficha")]


def achar_ficha(nome_ou_tema):
    """Aceita '<Tema> - Ficha' (nome novo), 'Ficha - <Tema>' (nome antigo), '<Tema>', '[[…]]' ou '….md'. Devolve (caminho, msg_erro).
    Se o nome antigo trouxer um qualificador entre parênteses ('… (anti-pseudociência)'), tenta também sem ele."""
    n = re.sub(r"^\[\[|\]\]$|\.md$", "", (nome_ou_tema or "").strip())
    if not n:
        return None, "frontmatter sem 'ficha:' (ou 'tema:') — diga de qual Ficha saem as afirmações"
    tema = n
    if sa(tema).startswith("ficha - "):
        tema = tema[len("ficha - "):]
    elif sa(tema).endswith(" - ficha"):
        tema = tema[:-len(" - ficha")]
    todas = fichas_da_base()
    alvos = [sa(nfc(tema))]
    sem_parenteses = re.sub(r"\s*\([^)]*\)\s*$", "", tema)
    if sem_parenteses != tema:
        alvos.append(sa(nfc(sem_parenteses)))
    for alvo in alvos:
        for p in todas:
            if sa(_tema_da_ficha(p.stem)) == alvo:
                return p, None
    return None, (f"ficha '{n}' não encontrada em 01 - BASE CIENTÍFICA (arquivo '<Tema> - Ficha.md' em qualquer área). "
                  f"Disponíveis: {', '.join(p.stem for p in todas) or '(nenhuma)'}")


def escolher_item(oracao, itens):
    if len(itens) == 1:
        return itens[0]
    pal = lambda t: {w for w in re.findall(r"[a-z0-9]+", sa(t)) if len(w) >= 4}
    po = pal(oracao)
    return max(itens, key=lambda it: (len(po & pal(it["texto"])), it["nivel"]))


def checar_trecho(texto, ids, ficha):
    """Confere um trecho falado/escrito contra os itens da ficha que ele cita. → (erros, avisos)."""
    E, A = [], []
    itens = []
    for i in ids:
        it = ficha["itens"].get(i)
        if not it:
            E.append(f"[#{i}] não existe na {ficha['nome']} (use o nº da tabela 'Afirmações prontas', N1… de 'Números de impacto', "
                     f"M1… de 'Mitos' ou H1… de 'Histórias reais')")
            continue
        if "(conferir)" in sa(it["linha"]):
            E.append(f"[#{i}] está marcado '(conferir)' na ficha: depende de diretriz sem íntegra — não use até conferir")
        if not it["certeza_reconhecida"]:
            A.append(f"[#{i}] certeza '{it['certeza']}' não reconhecida pelo script: tratei como baixa")
        itens.append(it)
    if not itens:
        return E, A
    refs = ", ".join("#" + it["id"] for it in itens)
    permitidos = set().union(*(it["numeros"] for it in itens))
    fracoes = _fracoes_ok(texto, permitidos)
    for valor, bruto, pct, pos in numeros(texto, com_pos=True):
        if valor not in permitidos and pos not in fracoes and not _aproximado(valor, texto[:pos], permitidos):
            msg = (f"número '{bruto}' não está na linha {refs} da ficha: copie o número da linha, arredonde com a palavra "
                   f"certa («quase 36», «mais de 35», «cerca de 36», até 10% de diferença) ou use «1 em cada 3» para 33%")
            (A if valor <= 10 and valor == int(valor) and not pct else E).append(msg)
    calibraveis = [it for it in itens if it["nivel"] is not None]
    if calibraveis:
        algum_calibrador = False
        for o, pergunta in oracoes(sa(sem_citacao(texto))):
            if pergunta:
                continue
            it = escolher_item(o, calibraveis)
            L = it["nivel"]
            n, palavra = hedge(o)
            fortes = {k: v for k, v in verbos_fortes(o).items() if not relatado(o, v)}
            if n is not None or fortes:
                algum_calibrador = True
            if n is not None:
                if n > L and n not in it["hedges"]:
                    E.append(f"[#{it['id']}] certeza {NIVEIS[L]}: '{palavra}' é forte demais. Use {CALIBRADOR[L]} "
                             f"ou a redação da ficha: «{it['texto']}»")
            elif fortes and L < 3:
                extra = [v for k, v in fortes.items() if k not in it["livres"]]
                if extra:
                    E.append(f"[#{it['id']}] certeza {NIVEIS[L]}: '{extra[0]}' sem calibrador é forte demais. "
                             f"Use {CALIBRADOR[L]} ou a redação da ficha: «{it['texto']}»")
        L = min(it["nivel"] for it in calibraveis)
        if not algum_calibrador and L < 3 and any(it["hedges"] for it in calibraveis):
            A.append(f"[{refs}] certeza {NIVEIS[L]}, mas o trecho não tem calibrador ({CALIBRADOR[L]}): confira se não ficou "
                     f"mais forte que a ficha")
    t = sa(texto)
    nums = numeros(texto)
    if any(p for _, _, p in nums) and not any(not p for _, _, p in nums) and re.search(r"\brisco|\bchance|eventos", t):
        A.append(f"[{refs}] efeito relativo (%) sem número absoluto no mesmo trecho")
    return E, A


def checar_proibidas(texto):
    """→ (erros, avisos). Em desmentido ('não existe milagre') vira aviso."""
    E, A = [], []
    t = sa(texto)
    for rx, nome in PROIBIDAS:
        for m in re.finditer(rx, t):
            antes = re.findall(r"[a-z]+", t[:m.start()])[-4:]
            if NEGACAO & set(antes):
                A.append(f"palavra proibida '{m.group(0)}' em contexto de desmentido: confira se não soa como promessa")
            else:
                E.append(f"palavra proibida '{m.group(0)}' (lista: cura, milagre, garantido, segredo, nunca mais, 100%, "
                         f"sem esforço)")
    return E, A


def checar_promessa(texto, avisos=None):
    """→ erros. Promessa de resultado com número no corpo de quem assiste ('7 kg em um mês', 'ganhe 5 kg de músculo',
    '10 cm de cintura em 30 dias'). Se a frase descreve um estudo ('o grupo ganhou…', 'os participantes…'), vira aviso
    (quando a lista `avisos` vem) ou é ignorada: é fato da Ficha, não promessa."""
    t = sa(texto)
    out = []
    for rx, nome in PROMESSA_NUM:
        for m in re.finditer(rx, t):
            ini = max(t.rfind(".", 0, m.start()), t.rfind("!", 0, m.start()), t.rfind("?", 0, m.start())) + 1
            fim = min([x for x in (t.find(".", m.end()), t.find("!", m.end()), t.find("?", m.end())) if x >= 0] or [len(t)])
            if re.search(_CONTEXTO_ESTUDO, t[ini:fim]):
                if avisos is not None:
                    avisos.append(f"«{m.group(0)}» parece resultado de estudo: deixe claro que é o resultado do grupo "
                                  f"estudado, não promessa para quem assiste")
                continue
            out.append(f"promessa de resultado ({nome}) «{m.group(0)}»: o CTA pode prometer o que o produto entrega, "
                       f"nunca quilos, medidas ou % de gordura no corpo de quem assiste (ética CONFEF + regra da marca)")
            break
    return out


def checar_etica(texto):
    """→ (erros, avisos). Ética do Profissional de Educação Física (CONFEF 307/2015) e limites das outras profissões:
    antes/depois, depoimento de aluno, preço, prescrição de dieta/suplemento (nutricionista, Lei 8.234/1991), ordem
    sobre remédio/hormônio (médico) = ERRO; ordem de treino com número para quem assiste = AVISO. Trecho entre aspas
    (o mito citado para ser desmentido) fica fora."""
    E, A = [], []
    t = sa(sem_citacao(texto))
    for rx, msg in ETICA_ERRO:
        m = re.search(rx, t)
        if m:
            E.append(f"«{m.group(0).strip()}»: {msg}")
    for rx, msg in ETICA_AVISO:
        m = re.search(rx, t)
        if m:
            A.append(f"«{m.group(0).strip()}»: {msg}")
    return E, A


def checar_sem_referencia(texto):
    """Trecho sem [#n]: números e verbos de efeito precisam de fonte."""
    E, A = [], []
    for valor, bruto, pct in numeros(texto):
        if pct or valor != int(valor) or valor > 10:
            E.append(f"número '{bruto}' sem [#n]: todo número precisa vir de uma linha da ficha (ponha o [#n] logo depois)")
    for o, pergunta in oracoes(sa(sem_citacao(texto))):
        if pergunta:
            continue
        f = {k: v for k, v in verbos_fortes(o).items() if not relatado(o, v)}
        if f:
            A.append(f"'{next(iter(f.values()))}' parece afirmação clínica sem [#n]")
        m = re.search(RECOMENDA, o)
        if m:
            E.append(f"'{m.group(0)}' é posição de diretriz/órgão sem [#n]: cite a linha da ficha (Afirmações, Números ou Mitos) ou tire")
        elif re.search(CITA_FONTE, o):
            A.append(f"cita diretriz/estudo sem [#n] («{o[:50]}»): se for afirmação, marque")
    return E, A


# ---------- fontes ----------
def _norm(t):
    return re.sub(r"\s+", " ", re.sub(r"[/–—\-_,.()]", " ", sa(t))).strip()


def nota_do_rotulo(rotulo, notas):
    r = _norm(rotulo)
    if not r:
        return None
    desc = {n: _norm(n.split(" - ", 1)[1]) if " - " in n else "" for n in notas}
    for teste in (lambda n: _norm(n) == r, lambda n: _norm(n).startswith(r + " "),
                  lambda n: desc[n].startswith(r), lambda n: f" {r} " in f" {_norm(n)} "):
        for n in notas:
            if teste(n):
                return n
    return None


def _indice_notas():
    """nome da nota (sem acento, minúsculo) → caminho. Primeiro _MÁQUINA/fontes-processadas, depois o resto da base
    (Protocolos, Fichas) e, por último, as notas fictícias de _SISTEMA/teste. Pasta ausente: pulada."""
    idx = {}
    podar_base = {nfc(x) for x in ("_MÁQUINA", "_anexos", "ENTRADA")}
    for raiz, podar in ((PROCESSADAS, set()), (BASE, podar_base), (TESTE, set())):
        for d, dirs, arqs in os.walk(raiz):
            dirs[:] = [x for x in dirs if nfc(x) not in podar and not x.startswith(".")]
            for a in arqs:
                if a.endswith(".md"):
                    idx.setdefault(sa(nfc(a[:-3])), os.path.join(d, a))
    return idx


def referencia_da_nota(caminho):
    t = Path(caminho).read_text(encoding="utf-8-sig")
    fm, _, _ = frontmatter(t)
    m = re.search(r"^[>\-*\s]*(?:\*\*)?Vancouver(?:\*\*)?\s*:\s*(?:\*\*)?\s*(.+?)\s*$", t, re.M)
    link = fm.get("link") or (f"https://doi.org/{fm['doi']}" if fm.get("doi") else "")
    return (m.group(1).strip() if m else ""), link


def artigo_da_biblioteca(nome):
    """Id de artigo do catálogo (_MÁQUINA/artigos) → (vancouver, link) tirados do JSON, ou None."""
    p = ARTIGOS_JSON / f"{nome}.json"
    if not p.exists():
        p = next((q for q in ARTIGOS_JSON.glob("*.json") if sa(nfc(q.stem)) == sa(nfc(nome))), None)
    if not p:
        return None
    r = json.loads(p.read_text(encoding="utf-8")).get("referencia", {})
    return r.get("vancouver", ""), r.get("link", "")


def montar_secoes(ficha, ids):
    """Gera as seções '## Fontes' e '## Nível de certeza' para os ids usados. → (markdown, [notas], avisos)."""
    avisos, grupos, ordem = [], {}, []
    for i in ids:
        it = ficha["itens"][i]
        if it.get("historia"):  # história real: a fonte é o(s) link(s) da própria linha
            chave = "H:" + it["fonte"]
            if chave not in grupos:
                grupos[chave] = {"nota": None, "rotulo": "História real — " + (it["fonte"] or "(sem link na ficha)"), "locs": []}
                ordem.append(chave)
            grupos[chave]["locs"].append(f"#{i}")
            continue
        anterior = None
        for parte in [p.strip() for p in it["fonte"].split(";") if p.strip()] or [""]:
            rotulo, _, loc = parte.partition(",")
            nota = nota_do_rotulo(rotulo, ficha["notas"])
            if not nota and anterior and re.match(r"(sec|tab|rec|result|sof|fig|§|p\.|\d)", sa(parte)):
                rotulo, loc, nota = anterior[0], parte, anterior[1]  # "Hooper 2020, SoF 1; Tab. 2": mesma fonte
            anterior = (rotulo, nota)
            chave = nota or rotulo.strip() or f"(sem fonte na ficha para #{i})"
            if not nota:
                avisos.append(f"#{i}: nota-base de '{rotulo.strip() or '?'}' não identificada; saiu como está na ficha")
            if chave not in grupos:
                grupos[chave] = {"nota": nota, "rotulo": rotulo.strip(), "locs": []}
                ordem.append(chave)
            grupos[chave]["locs"].append(f"{loc.strip() or 'sem localizador'} (#{i})")
    idx = _indice_notas()
    linhas = ["## Fontes", f"<!-- montado por validar_roteiro.py --montar-fontes a partir da {ficha['nome']}; ids: {','.join(ids)} -->"]
    for k, chave in enumerate(ordem, 1):
        g = grupos[chave]
        ref, link = "", ""
        da_biblioteca = False
        if g["nota"]:
            cam = idx.get(sa(nfc(g["nota"])))
            if cam:
                ref, link = referencia_da_nota(cam)
            elif artigo_da_biblioteca(g["nota"]):
                ref, link = artigo_da_biblioteca(g["nota"])
                da_biblioteca = True
            else:
                avisos.append(f"arquivo da nota [[{g['nota']}]] não encontrado na base nem no catálogo (_MÁQUINA/artigos)")
            if not ref:
                ref = f"{g['rotulo']} (nota do cofre, sem linha 'Vancouver')"
        else:
            ref = g["rotulo"] or chave
        origem = (f" · biblioteca `{g['nota']}`" if da_biblioteca else f" · nota [[{g['nota']}]]") if g["nota"] else ""
        linhas.append(f"{k}. {ref}" + (f" {link}" if link and link not in ref else "")
                      + origem + f" · {'; '.join(g['locs'])}")
    linhas += ["", "## Nível de certeza", "| Ref. | Afirmação (redação da ficha) | Certeza | Número absoluto |", "|---|---|---|---|"]
    for i in ids:
        it = ficha["itens"][i]
        cel = lambda t: (t or "—").replace("|", "/")
        linhas.append(f"| #{i} | {cel(it['texto'])} | {cel(it['certeza'])} | {cel(it['numero'])} |")
    notas = [grupos[c]["nota"] for c in ordem if grupos[c]["nota"]]
    return "\n".join(linhas) + "\n", notas, avisos


def falas_do_roteiro(md):
    """As falas de '## Roteiro', limpas (sem número, rótulo nem [#n]): uma por parte no formato novo, ou por linha
    '[GATILHO] frase' no antigo."""
    _, corpo, _ = frontmatter(md)
    falas, dentro = [], False
    for l in corpo.splitlines():
        if re.match(r"^##\s+Roteiro\b", l, re.I):
            dentro = True
            continue
        if dentro and re.match(r"^##\s+", l):
            break
        if not dentro:
            continue
        pm, tm = _PARTE.match(l), _TAG.match(l)
        if pm:
            resto = pm.group(2).strip()
            viral = rotulo_viral(resto)
            fala = viral[1] if viral[2] else separar_rotulo(resto, MECANISMOS)[1]
        elif tm:
            fala = tm.group(2)
        else:
            continue
        fala = re.sub(r"\s+([.,;:!?])", r"\1", re.sub(r"\s+", " ", _REF.sub("", fala))).strip()
        if fala:
            falas.append(fala)
    return falas


def montar_texto_para_gravar(md):
    """'## Texto para gravar': só as falas do roteiro, uma parte por parágrafo, sem número, rótulo nem referências."""
    return "## Texto para gravar\n\n" + "\n\n".join(falas_do_roteiro(md)) + "\n"


def _fim_da_analise(linhas):
    """Índice da linha onde termina a seção '## Análise' (o próximo '## ' ou o fim), ou None se não houver."""
    ini = next((k for k, l in enumerate(linhas) if re.match(r"^##\s+An[áa]lise\b", l, re.I)), None)
    if ini is None:
        return None
    return next((j for j in range(ini + 1, len(linhas)) if re.match(r"^##\s+", linhas[j])), len(linhas))


def substituir_secoes(md, novo, apos_analise=False):
    """Tira '## Para gravar' (a antiga, TELA DIVIDIDA), '## Texto para gravar', '## Fontes' e '## Nível de certeza'
    antigos (até o próximo '## ') e põe o bloco novo no lugar. Com apos_analise (roteiros), o bloco nunca fica antes
    da '## Análise': se as seções antigas estavam antes dela, o bloco vai para logo depois."""
    linhas, out, pulando, pos = md.rstrip("\n").splitlines(), [], False, None
    for l in linhas:
        if re.match(r"^##\s+(Para gravar|Texto para gravar|Fontes|N[íi]vel de certeza)\b", l):
            pulando = True
            if pos is None:
                pos = len(out)
            continue
        if pulando and re.match(r"^##\s+", l):
            pulando = False
        if not pulando:
            out.append(l)
    bloco = novo.rstrip("\n").splitlines()
    fim = _fim_da_analise(out) if apos_analise else None
    if pos is not None and fim is not None and pos < fim:
        j = fim
        while j > 0 and not out[j - 1].strip():
            j -= 1
        out[j:fim] = [""] + bloco + ([""] if fim < len(out) else [])
        return "\n".join(out).rstrip("\n") + "\n"
    if pos is None:
        out += [""] + bloco
    else:
        out[pos:pos] = bloco + [""]
    return "\n".join(out).rstrip("\n") + "\n"


def atualizar_fontes_fm(md, notas):
    if not md.startswith("---"):
        return md
    linhas = md.splitlines()
    fim = next((k for k in range(1, len(linhas)) if linhas[k].strip() == "---"), None)
    if fim is None:
        return md
    valor = "fontes: " + json.dumps([f"[[{n}]]" for n in notas], ensure_ascii=False)
    for k in range(1, fim):
        if re.match(r"^fontes\s*:", linhas[k]):
            linhas[k] = valor
            break
    else:
        linhas.insert(fim, valor)
    return "\n".join(linhas) + ("\n" if md.endswith("\n") else "")


# ---------- roteiro ----------
_TAG = re.compile(r"^\s*\[([^\]#][^\]]*)\]\s*(.*)$")  # formato antigo: [GATILHO] frase
_PARTE = re.compile(r"^\s*(\d+)\s*[.)](?!\d)\s*(.*)$")  # formato novo: 3. MECANISMO — fala
_REF = re.compile(r"\[#([^\]]*)\]")
_CANON = {sa(g).upper(): g for g in GATILHOS}
_SEP_ROTULO = re.compile(r"\s*[—–]\s*|\s+-\s+")
_BULLET = re.compile(r"^\s*[-*•]\s+(.*)$")
_TELA = re.compile(r"^\s*>\s*tela\s*:", re.I)
_COLCHETE = re.compile(r"\[([^\]]*)\]")
_PALAVRA = re.compile(r"[0-9A-Za-zÀ-ÿ]+(?:[-'’][0-9A-Za-zÀ-ÿ]+)*")
_GERADAS = ("texto para gravar", "para gravar", "fontes", "nivel de certeza")  # seções que o --montar-fontes escreve


def grupos_de_referencia(frase):
    """[(trecho, [ids])] — cada trecho vai até o [#n] que o fecha; [#3][#4] colados somam ids. + resto sem [#n]."""
    out, ini = [], 0
    for m in _REF.finditer(frase):
        trecho = frase[ini:m.start()]
        ids = [x.strip().lstrip("#").upper() for x in re.split(r"[,;\s]+", m.group(1)) if x.strip().lstrip("#")]
        if out and not re.search(r"\w", trecho):
            out[-1][1].extend(ids)
        else:
            out.append([trecho, ids])
        ini = m.end()
    return out, frase[ini:]


def separar_rotulo(resto, validos):
    """'MECANISMO — fala' → (rótulo, fala, canônico|None, separador_ok). Compara sem acento e sem maiúscula;
    o separador é —, – ou - (o hífen só com espaço dos dois lados)."""
    resto = nfc(resto)
    t = sa(resto)
    for canon in validos:
        c = sa(canon)
        if t.startswith(c) and not (len(t) > len(c) and t[len(c)].isalnum()):
            m = _SEP_ROTULO.match(resto, len(c))
            if m:
                return canon, resto[m.end():].strip(), canon, True
            return canon, resto[len(c):].lstrip(" :.,;").strip(), canon, False
    m = _SEP_ROTULO.search(resto)
    if m:
        return resto[:m.start()].strip(), resto[m.end():].strip(), None, True
    return resto.strip(), resto.strip(), None, False


def rotulo_viral(resto):
    """'DESENVOLVIMENTO 2 — fala' → (rótulo, fala, canônico|None, separador_ok), nas partes da estrutura viral.
    Aceita o número de repetição depois de DESENVOLVIMENTO/REENGAJAMENTO e a grafia 'CHAMADA PARA AÇÃO'."""
    resto = re.sub(r"^(\s*(?:desenvolvimento|reengajamento))\s+\d+\b", r"\1", nfc(resto), flags=re.I)
    rotulo, fala, canon, ok = separar_rotulo(resto, VIRAIS + list(_VIRAL_ALIAS))
    return rotulo, fala, _VIRAL_ALIAS.get(canon, canon), ok


def _frases(t):
    return [f for f in re.split(r"""(?<=[.!?…])["”’')]*\s+""", t.strip()) if _PALAVRA.search(f)]


def placeholders(texto):
    """Colchetes que não são referência [#…] (nem link markdown): [GANCHO], [CTA], [PAUSA], [INSIRA …]."""
    return [m.group(0) for m in _COLCHETE.finditer(texto)
            if not m.group(1).startswith("#") and texto[m.end():m.end() + 1] != "("]


def expressoes_proibidas(texto):
    """Nomes das expressões proibidas do Briefing de roteiro (seção 9) achadas no texto, sem repetir."""
    t = nfc(texto)
    s = sa(t)
    out = [nome for rx, nome in EXPRESSOES_PROIBIDAS if re.search(rx, s, re.S)]
    if re.search(r"\bDAN\b", t):  # só a sigla em maiúsculas (o nome "Dan" não é a expressão)
        out.append("DAN")
    return out


def jargoes(texto):
    """Siglas e termos técnicos achados no texto falado (que deve ser leigo), sem repetir."""
    achados, vistos = [], set()
    for rx in (JARGAO_CI, JARGAO_CS):
        for m in rx.finditer(texto):
            if m.group(0).lower() not in vistos:
                vistos.add(m.group(0).lower())
                achados.append(m.group(0))
    return achados


def _checar_fala(n, frase, ficha, usados, E, A):
    """Evidência de uma fala: id existe na ficha, verbo × certeza, número × linha, diretriz sem [#n] e palavras
    proibidas, promessa e ética (CONFEF). Acumula em E/A (com o nº da linha) e em `usados`. → o texto falado (sem os [#n])."""
    grupos, resto = grupos_de_referencia(frase)
    for trecho, ids in grupos:
        invalidos = [i for i in ids if not re.fullmatch(r"\d+|[NMH]\d+", i)]
        for i in invalidos:
            E.append(f"L{n}: referência inválida [#{i}] (use [#3], [#N1], [#M2] ou [#H1])")
        ids = [i for i in ids if i not in invalidos]
        if not ids:
            continue
        e, a = checar_trecho(trecho, ids, ficha)
        E += [f"L{n}: {x}" for x in e]
        A += [f"L{n}: {x}" for x in a]
        usados += [i for i in ids if i in ficha["itens"] and i not in usados]
    e, a = checar_sem_referencia(resto)
    E += [f"L{n}: {x}" for x in e]
    A += [f"L{n}: {x}" for x in a]
    falada = _REF.sub("", frase)
    e, a = checar_proibidas(falada)
    E += [f"L{n}: {x}" for x in e]
    A += [f"L{n}: {x}" for x in a]
    av = []
    E += [f"L{n}: {x}" for x in checar_promessa(falada, av)]
    A += [f"L{n}: {x}" for x in av]
    e, a = checar_etica(falada)
    E += [f"L{n}: {x}" for x in e]
    A += [f"L{n}: {x}" for x in a]
    return falada


def _checar_estilo(n, falada, E, A):
    """Estilo do texto falado (Briefing de roteiro): expressão proibida é ERRO; clichê, sigla/jargão e frase longa são AVISO."""
    for nome in expressoes_proibidas(falada):
        E.append(f"L{n}: expressão proibida «{nome}» (Briefing, seção 9): reescreva com palavras do dia a dia")
    s = sa(falada)
    for rx, nome in CLICHES:
        if re.search(rx, s):
            A.append(f"L{n}: clichê «{nome}»: prefira uma dúvida concreta que o próprio assunto cria")
    for termo in jargoes(falada):
        A.append(f"L{n}: «{termo}» no texto falado: linguagem leiga: explique com palavras do dia a dia ou analogia")
    for frase in re.split(r"""(?<=[.!?…])["”’')]*\s+""", falada.strip()):
        k = len(_PALAVRA.findall(frase))
        if k > MAX_PALAVRAS_FRASE:
            A.append(f"L{n}: frase com {k} palavras (o ideal é até {MAX_PALAVRAS_FRASE}): «{frase[:50].strip()}…»")


def _duracao(fm, falado, E, padrao=DURACAO_PADRAO):
    """Soma as palavras faladas (sem rótulo e sem [#n]) a 2,5 palavras/s e confere com a faixa do formato (a mensagem
    vai para a lista recebida: E no formato novo, A na estrutura viral). → (palavras, s)."""
    palavras = len(_PALAVRA.findall(" ".join(falado)))
    seg = palavras / PALAVRAS_POR_SEG
    faixa = None
    m = re.match(r"^\s*(\d+)\s*[-–a]\s*(\d+)", fm.get("duracao", ""))
    if m:
        faixa = (int(m.group(1)), int(m.group(2)))
    elif sa(fm.get("formato", "reels")) != "youtube":
        faixa = padrao
    if faixa and not (faixa[0] <= seg <= faixa[1]):
        alvo = f"{int(faixa[0] * PALAVRAS_POR_SEG)}–{int(faixa[1] * PALAVRAS_POR_SEG)} palavras"
        E.append(f"duração estimada {seg:.0f} s ({palavras} palavras a {PALAVRAS_POR_SEG} palavras/s); alvo {faixa[0]}–{faixa[1]} s = {alvo}")
    return palavras, seg


def _fontes_desatualizadas(texto, usados, A):
    """Fontes já montadas e desatualizadas?"""
    m = re.search(r"<!-- montado por validar_roteiro\.py.*?ids: ([^ ]*) -->", texto)
    if m and m.group(1).split(",") != usados:
        A.append("seção Fontes desatualizada: rode de novo com --montar-fontes")


def validar(caminho):
    """→ (erros, avisos, info). Mensagens já com o nº da linha do arquivo.
    Formato novo (partes numeradas '1. MECANISMO — fala'); o antigo ('[GATILHO] frase') só se '## Roteiro' não tiver
    nenhuma linha numerada."""
    E, A = [], []
    texto = Path(caminho).read_text(encoding="utf-8-sig")
    fm, corpo, l0 = frontmatter(texto)
    cam_ficha, msg = achar_ficha(fm.get("ficha") or fm.get("tema"))
    if not cam_ficha:
        return [msg], [], {}
    ficha = carregar_ficha(cam_ficha)
    if fm.get("ficha") is None:
        A.append(f"frontmatter sem 'ficha:'; usei a do tema ({ficha['nome']})")
    if ficha["fm"].get("status") not in (None, "pronta"):
        A.append(f"{ficha['nome']} está com status '{ficha['fm'].get('status')}'")

    linhas = corpo.splitlines()
    ini = next((k + 1 for k, l in enumerate(linhas) if re.match(r"^##\s+Roteiro\b", l, re.I)), None)
    achou_roteiro = ini is not None
    if ini is None:
        A.append("sem a seção '## Roteiro': li o corpo inteiro")
        ini = 0
    regiao = []  # linhas da seção Roteiro
    for l in linhas[ini:]:
        if re.match(r"^##\s+", l):
            break
        regiao.append(l)
    if sa(str(fm.get("estrutura") or "")).startswith("viral"):
        return _validar_viral(texto, fm, linhas, l0, achou_roteiro, ficha, E, A)
    if any(_TAG.match(l) for l in regiao) and not any(_PARTE.match(l) for l in regiao):
        return _validar_antigo(texto, fm, linhas, l0, ini, ficha, E, A)
    return _validar_novo(texto, fm, linhas, l0, achou_roteiro, ficha, E, A)


def _validar_novo(texto, fm, linhas, l0, achou_roteiro, ficha, E, A):
    """Formato novo: '## Roteiro' com partes '1. MECANISMO — fala [#n]' e '## Análise' com 6 a 8 bullets."""
    secao = None  # título (sem acento, minúsculo) da seção '## …' onde a linha está; None = antes da primeira
    partes, bullets = [], []  # partes: (nº da linha, mecanismo|None); bullets: nº da linha
    usados, falado = [], []
    esperado, tem_analise = 1, False
    for k, l in enumerate(linhas):
        n = l0 + k
        l = nfc(l)
        h = re.match(r"^##\s+(.+?)\s*$", l)
        if h:
            secao = sa(h.group(1))
            tem_analise = tem_analise or secao.startswith("analise")
            continue
        s = l.strip()
        if not s or s.startswith("<!--") or re.fullmatch(r"[-*_]{3,}", s):
            continue
        if secao and secao.startswith(_GERADAS):  # escritas pelo --montar-fontes: não se valida
            continue
        na_analise = bool(secao) and secao.startswith("analise")
        # corte de cena não entra mais (o visual da Tela Dividida só aparece num bullet da Análise)
        tela = bool(_TELA.match(l))
        if tela:
            E.append(f"L{n}: linha '> tela:' (corte de cena não entra mais no roteiro; o apoio visual vai só num bullet da Análise)")
        elif not na_analise and re.search(r"gancho\s+visual", sa(l)):
            E.append(f"L{n}: «gancho visual» (corte de cena não entra mais no roteiro; o apoio visual vai só num bullet da Análise)")
        if na_analise:
            bm = _BULLET.match(l)
            if not bm:
                continue
            bullets.append(n)
            rotulo, txt, canon, sep_ok = separar_rotulo(bm.group(1).strip(), ROTULOS_ANALISE)
            if not (canon and sep_ok):
                A.append(f"L{n}: rótulo de bullet «{rotulo[:40]}» não é um dos 6 mecanismos (nem FORMATO ou AIDA), "
                         f"ou falta o ' — ' depois dele")
            for nome in expressoes_proibidas(_REF.sub("", txt)):
                E.append(f"L{n}: expressão proibida «{nome}» na Análise (Briefing, seção 9)")
            continue
        em_roteiro = secao.startswith("roteiro") if secao is not None else not achou_roteiro
        if not em_roteiro or tela or (secao is None and s.startswith("#")):
            continue
        pm = _PARTE.match(l)
        if not pm:
            E.append(f"L{n}: linha fora do formato 'N. MECANISMO — fala' (cada parte é uma linha numerada): «{s[:60]}»")
            E += [f"L{n}: placeholder {p} proibido (só valem as referências [#n], [#N1], [#M2], [#H1])" for p in placeholders(s)]
            continue
        num, resto = int(pm.group(1)), pm.group(2).strip()
        if num != esperado:
            E.append(f"L{n}: numeração fora de sequência: veio {num}, esperava {esperado}")
        esperado = num + 1
        rotulo, fala, canon, sep_ok = separar_rotulo(resto, MECANISMOS)
        partes.append((n, canon if sep_ok else None))
        if canon and not sep_ok:
            E.append(f"L{n}: falta ' — ' depois do rótulo (escreva '{num}. {canon} — fala')")
        elif canon is None and sep_ok:
            sug = difflib.get_close_matches(sa(rotulo), [sa(m) for m in MECANISMOS], n=1, cutoff=0.75)
            dica = f" Você quis dizer «{next(m for m in MECANISMOS if sa(m) == sug[0])}»?" if sug else ""
            cta = " A chamada para ação não é uma parte: fica dentro de uma delas." if sa(rotulo) in ("cta", "aida", "gancho") else ""
            E.append(f"L{n}: rótulo «{rotulo[:40]}» não é um dos 6 mecanismos.{dica}{cta} Válidos: {' · '.join(MECANISMOS)}")
        elif canon is None:
            E.append(f"L{n}: parte {num} sem 'MECANISMO — fala': «{resto[:60]}»")
        E += [f"L{n}: placeholder {p} proibido (só valem as referências [#n], [#N1], [#M2], [#H1])" for p in placeholders(resto)]
        if not fala:
            E.append(f"L{n}: parte {num} sem texto falado")
            continue
        falada = _checar_fala(n, fala, ficha, usados, E, A)
        _checar_estilo(n, falada, E, A)
        falado.append(falada)

    if not partes:
        return E + ["nenhuma parte no formato 'N. MECANISMO — fala' encontrada na seção '## Roteiro'"], A, {}

    if not PARTES_MIN <= len(partes) <= PARTES_MAX:
        A.append(f"{len(partes)} partes no roteiro: o esperado é de {PARTES_MIN} a {PARTES_MAX}")
    if not any(c == MORAL for _, c in partes):
        A.append(f"nenhuma parte {MORAL}: a moral é a ideia que a pessoa leva embora")
    if not tem_analise:
        A.append(f"sem a seção '## Análise' (de {BULLETS_MIN} a {BULLETS_MAX} bullets, um por decisão)")
    elif not BULLETS_MIN <= len(bullets) <= BULLETS_MAX:
        A.append(f"'## Análise' com {len(bullets)} bullet(s): o esperado é de {BULLETS_MIN} a {BULLETS_MAX}")
    if not usados:
        A.append("nenhuma afirmação marcada com [#n]: o roteiro não cita a ficha")
    palavras, seg = _duracao(fm, falado, E)
    _fontes_desatualizadas(texto, usados, A)
    return E, A, {"ficha": ficha, "usados": usados, "palavras": palavras, "segundos": seg, "frases": len(partes),
                  "unidade": "partes"}


def _checar_narrador(n, falada, E):
    """Estrutura viral: a voz é de IA, então relato pessoal ou de aluno seria história inventada."""
    m = re.search(RELATO_1A_PESSOA, sa(falada))
    if m:
        E.append(f"L{n}: «{m.group(0)}»: a voz é de IA e não tem história nem aluno; conte o fato da Ficha "
                 f"(nada de relato inventado nem depoimento)")


def _checar_ordem_viral(partes, E, A):
    """Ordem e tamanho das partes da estrutura viral. partes = [(nº da linha, canônico, fala)]."""
    seq, lin = [c for _, c, _ in partes], [x for x, _, _ in partes]
    if None in seq:  # rótulo inválido já deu ERRO; a ordem só é conferida com todos os rótulos certos
        return
    def erro(i, msg):
        E.append(f"L{lin[i]}: {msg}")
    if len(seq) < 6:
        E.append(f"{len(seq)} partes: a estrutura viral tem no mínimo 6 (gancho, retenção, desenvolvimento, "
                 f"reengajamento, encerramento, chamada pra ação); o guia usa 8")
    if seq[0] != "GANCHO":
        erro(0, "a 1ª parte é o GANCHO (a frase que para o dedo)")
    if len(seq) > 1 and seq[1] != "RETENÇÃO":
        erro(1, "a 2ª parte é a RETENÇÃO (2 ou 3 frases que confirmam a promessa do gancho e dão motivo para ficar)")
    if seq[-1] != "CHAMADA PRA AÇÃO":
        erro(-1, "a última parte é a CHAMADA PRA AÇÃO (palavra no comentário + o material grátis)")
    if len(seq) > 3 and seq[-2] != "ENCERRAMENTO":
        erro(-2, "a penúltima parte é o ENCERRAMENTO (fecha a ideia em uma frase)")
    meio = list(range(2, len(seq) - 2))
    for i in meio:
        if seq[i] not in ("DESENVOLVIMENTO", "REENGAJAMENTO"):
            erro(i, f"«{seq[i]}» no miolo: entre a retenção e o encerramento só entram DESENVOLVIMENTO e REENGAJAMENTO")
    if meio and seq[meio[0]] != "DESENVOLVIMENTO":
        erro(meio[0], "depois da retenção vem um DESENVOLVIMENTO")
    for a, b in zip(meio, meio[1:]):
        if seq[a] == seq[b] == "REENGAJAMENTO":
            erro(b, "2 reengajamentos seguidos: entre eles vem um desenvolvimento")
    nd = sum(seq[i] == "DESENVOLVIMENTO" for i in meio)
    nr = sum(seq[i] == "REENGAJAMENTO" for i in meio)
    if nd < 1 or nr < 1:
        E.append("o miolo precisa de pelo menos 1 DESENVOLVIMENTO e 1 REENGAJAMENTO")
    elif nd < 2 or nr < 2:
        A.append(f"miolo com {nd} desenvolvimento(s) e {nr} reengajamento(s): o guia usa 2 de cada "
                 f"(repita quantas vezes o assunto pedir)")
    for x, c, fala in partes:
        if c in FRASES_VIRAIS:
            k, (lo, hi) = len(_frases(fala)), FRASES_VIRAIS[c]
            if not lo <= k <= hi:
                A.append(f"L{x}: {c} com {k} frase(s): o guia pede {lo if lo == hi else f'{lo} a {hi}'}")
        if c == "CHAMADA PRA AÇÃO":
            if not re.search(r"\b(?:comenta|comente|escreve|escreva|digita|digite|manda|mande)\b", sa(fala)):
                A.append(f"L{x}: a chamada pra ação pede o comentário com a palavra («Comenta TREINO que eu te mando…»)")
            if not re.search(r"(?<![\wÀ-ÿ])[A-ZÀ-Ý]{3,}(?![\wÀ-ÿ])", fala):
                A.append(f"L{x}: chamada pra ação sem a PALAVRA em maiúsculas (curta, fácil de digitar, a do eixo)")


def _validar_viral(texto, fm, linhas, l0, achou_roteiro, ficha, E, A):
    """Estrutura viral ('estrutura: viral'): '## Roteiro' com GANCHO · RETENÇÃO · DESENVOLVIMENTO/REENGAJAMENTO
    alternados · ENCERRAMENTO · CHAMADA PRA AÇÃO, e '## Ganchos' com 3 opções (a escolhida com '(recomendado)')."""
    secao = None
    partes, ganchos = [], []  # partes: (nº da linha, canônico|None, fala); ganchos: (nº da linha, texto)
    usados, falado = [], []
    esperado = 1
    validos = " · ".join(VIRAIS)
    for k, l in enumerate(linhas):
        n = l0 + k
        l = nfc(l)
        h = re.match(r"^##\s+(.+?)\s*$", l)
        if h:
            secao = sa(h.group(1))
            continue
        s = l.strip()
        if not s or s.startswith("<!--") or re.fullmatch(r"[-*_]{3,}", s):
            continue
        if secao and secao.startswith(_GERADAS):
            continue
        if _TELA.match(l):
            E.append(f"L{n}: linha '> tela:' (o roteiro é só o texto falado; as cenas saem no motor de vídeo)")
            continue
        if secao and secao.startswith("ganchos"):
            bm = _BULLET.match(l)
            if bm:
                ganchos.append((n, bm.group(1).strip()))
            continue
        em_roteiro = secao.startswith("roteiro") if secao is not None else not achou_roteiro
        if not em_roteiro or (secao is None and s.startswith("#")):
            continue
        pm = _PARTE.match(l)
        if not pm:
            E.append(f"L{n}: linha fora do formato 'N. PARTE — fala' (cada parte é uma linha numerada): «{s[:60]}»")
            continue
        num, resto = int(pm.group(1)), pm.group(2).strip()
        if num != esperado:
            E.append(f"L{n}: numeração fora de sequência: veio {num}, esperava {esperado}")
        esperado = num + 1
        rotulo, fala, canon, sep_ok = rotulo_viral(resto)
        if canon and not sep_ok:
            E.append(f"L{n}: falta ' — ' depois do rótulo (escreva '{num}. {canon} — fala')")
        elif canon is None:
            E.append(f"L{n}: rótulo «{rotulo[:40]}» não é uma parte da estrutura viral. Válidos: {validos}")
        E += [f"L{n}: placeholder {p} proibido (só valem as referências [#n], [#N1], [#M2], [#H1])" for p in placeholders(resto)]
        if not fala:
            E.append(f"L{n}: parte {num} sem texto falado")
            continue
        falada = _checar_fala(n, fala, ficha, usados, E, A)
        _checar_estilo(n, falada, E, A)
        _checar_narrador(n, falada, E)
        partes.append((n, canon if sep_ok else None, falada))
        falado.append(falada)

    if not partes:
        return E + ["nenhuma parte no formato 'N. PARTE — fala' encontrada na seção '## Roteiro'"], A, {}
    _checar_ordem_viral(partes, E, A)
    if not ganchos:
        A.append("sem a seção '## Ganchos' (3 opções de gancho, a escolhida marcada com '(recomendado)')")
    else:
        if len(ganchos) != 3:
            A.append(f"'## Ganchos' com {len(ganchos)} opção(ões): o esperado é 3")
        if not any(re.search(r"\(recomendado\)", g, re.I) for _, g in ganchos):
            A.append("'## Ganchos' sem a opção marcada com '(recomendado)'")
        for x, g in ganchos:
            falada = _checar_fala(x, re.sub(r"\s*\(recomendado\)\s*", " ", g, flags=re.I).strip(), ficha, [], E, A)
            _checar_estilo(x, falada, E, A)
            _checar_narrador(x, falada, E)
    if not usados:
        A.append("nenhuma afirmação marcada com [#n]: o roteiro não cita a ficha")
    palavras, seg = _duracao(fm, falado, A, DURACAO_VIRAL)
    _fontes_desatualizadas(texto, usados, A)
    return E, A, {"ficha": ficha, "usados": usados, "palavras": palavras, "segundos": seg, "frases": len(partes),
                  "unidade": "partes"}


def _validar_antigo(texto, fm, linhas, l0, ini, ficha, E, A):
    """Formato antigo, só por compatibilidade: 9 gatilhos '[GATILHO] frase [#n]' e a espinha GANCHO → tensão → AHÁ → MORAL → CTA."""
    frases = []  # (nº linha, [gatilhos], texto)
    for k in range(ini, len(linhas)):
        l = linhas[k]
        if re.match(r"^##\s+", l):
            break
        s = l.strip()
        if not s or s.startswith(">") or s.startswith("#") or s.startswith("<!--"):
            continue
        n = l0 + k
        m = _TAG.match(l)
        if not m:
            E.append(f"L{n}: linha sem [GATILHO] no início: «{s[:60]}» (direção de cena vai em linha começando com '>')")
            continue
        tags = []
        for t in re.split(r"\s*[+/]\s*", m.group(1)):
            c = _CANON.get(sa(t).upper().strip())
            if c:
                tags.append(c)
            else:
                E.append(f"L{n}: gatilho desconhecido [{t.strip()}]. Válidos: {', '.join(GATILHOS)}")
        if not m.group(2).strip():
            E.append(f"L{n}: [{m.group(1)}] sem frase")
        frases.append((n, tags, m.group(2)))

    if not frases:
        return E + ["nenhuma frase no formato '[GATILHO] frase' encontrada na seção '## Roteiro'"], A, {}

    # gatilhos: presença e espinha
    pos = {}
    for k, (_, tags, _) in enumerate(frases):
        for t in tags:
            pos.setdefault(t, []).append(k)
    faltam = [g for g in GATILHOS if g not in pos]
    if faltam:
        E.append(f"gatilhos ausentes: {', '.join(faltam)}")
    if "GANCHO VISUAL" not in frases[0][1]:
        E.append(f"L{frases[0][0]}: a 1ª frase tem de ser [GANCHO VISUAL]")
    if "CTA" not in frases[-1][1]:
        E.append(f"L{frases[-1][0]}: a última frase tem de ser [CTA]")
    if "CTA" in pos:
        for k in range(pos["CTA"][0], len(frases)):
            if "CTA" not in frases[k][1]:
                E.append(f"L{frases[k][0]}: frase depois do [CTA]: o CTA fecha o roteiro")
    if "EFEITO AHÁ" in pos:
        ultimo_aha = pos["EFEITO AHÁ"][-1]
        for g in TENSAO:
            if g in pos and pos[g][0] > ultimo_aha:
                E.append(f"L{frases[pos[g][0]][0]}: [{g}] aparece pela 1ª vez depois do último [EFEITO AHÁ] (a tensão vem antes da virada)")
        if "MORAL DA HISTÓRIA" in pos and pos["MORAL DA HISTÓRIA"][-1] < ultimo_aha:
            E.append(f"L{frases[ultimo_aha][0]}: o último [EFEITO AHÁ] vem depois da última [MORAL DA HISTÓRIA] (a moral fecha a virada)")

    # evidência, números e palavras proibidas, frase a frase
    usados, falado = [], []
    for n, tags, frase in frases:
        falado.append(_checar_fala(n, frase, ficha, usados, E, A))
    if not usados:
        A.append("nenhuma afirmação marcada com [#n]: o roteiro não cita a ficha")
    palavras, seg = _duracao(fm, falado, E)
    _fontes_desatualizadas(texto, usados, A)
    return E, A, {"ficha": ficha, "usados": usados, "palavras": palavras, "segundos": seg, "frases": len(frases)}


def relatorio(nome, E, A, info):
    linhas = [f"validar_roteiro · {nome}" + (f" · {info['ficha']['nome']}" if info.get("ficha") else "")]
    linhas += [f"ERRO  {x}" for x in E] + [f"AVISO {x}" for x in A]
    if info.get("frases"):
        linhas.append(f"{len(E)} erro(s), {len(A)} aviso(s) · {info['frases']} {info.get('unidade', 'frases')} · {info['palavras']} palavras ≈ "
                      f"{info['segundos']:.0f} s · refs: {', '.join('#' + i for i in info['usados']) or '—'}")
    else:
        linhas.append(f"{len(E)} erro(s), {len(A)} aviso(s)")
    return "\n".join(linhas)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        sys.exit(2)
    caminho = args[0]
    E, A, info = validar(caminho)
    print(relatorio(Path(caminho).name, E, A, info))
    if "--montar-fontes" in sys.argv:
        if E:
            print("\nFontes NÃO montadas: corrija os erros primeiro.")
        else:
            md = Path(caminho).read_text(encoding="utf-8-sig")
            bloco, notas, av = montar_secoes(info["ficha"], info["usados"])
            md = atualizar_fontes_fm(substituir_secoes(md, montar_texto_para_gravar(md) + "\n" + bloco, apos_analise=True), notas)
            Path(caminho).write_text(md, encoding="utf-8")
            for x in av:
                print(f"AVISO {x}")
            print(f"\nTexto para gravar, Fontes e Nível de certeza montados a partir da ficha ({len(notas)} nota(s)-base).")
    sys.exit(1 if E else 0)


if __name__ == "__main__":
    main()
