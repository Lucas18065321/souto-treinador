"""Regras editoriais do método BrandsDecoded (BD) para o texto do carrossel (carrossel.json). Só biblioteca padrão.

Chamado por validar_carrossel.py, que junta estes ERROS/AVISOS aos de evidência no mesmo relatório (e o hook roda tudo a
cada gravação). Também roda sozinho:
  python editorial.py "<pasta>/carrossel.json"      só as regras editoriais; código 1 se houver ERRO

Fonte das regras: o resumo operacional do método em Referências/Método BrandsDecoded/Método de texto - carrossel.md
(escrito com palavras próprias; o material original do curso não faz parte deste repositório).

ERRO (bloqueia): estrutura binária ("não é X, é Y", "não é sobre X, é sobre Y", "deixa de ser X para ser Y",
  "Menos X. Mais Y.", "Sem X. Sem Y.", "Antes: X. Agora: Y.") · cacoete de IA ("e isso muda tudo", "no fim das contas",
  "ao final do dia", "a pergunta que fica", "a questão é:", "o ponto é:", "o mecanismo funciona assim", "em um mundo
  onde", "vivemos em uma era", "cada vez mais", "simplesmente", "basicamente") · "de forma X" · dado vago ("estudos
  mostram", "especialistas dizem", "muitas empresas", "a maioria das pessoas", "recentemente") · anglicismo numérico
  ("5x", "10+", "2-3 anos"; em célula de tabela/stat vira AVISO) · abertura e fechamento de slide proibidos · CTA
  cordial · headline proibida na capa e no "headline" do topo ("descubra/saiba/conheça…", "quando X vira Y", "a ascensão
  de", "o impacto de", "tudo que você precisa saber", "o guia definitivo", "mudou para sempre", "revelamos…") ·
  ÉTICA DO PROFISSIONAL DE EDUCAÇÃO FÍSICA (Código de Ética do CONFEF + regras da marca): antes/depois de aluno,
  depoimento ou resultado de aluno, "meus alunos" com resultado, preço/promoção, promessa de resultado com número no
  corpo do leitor ("7 kg em um mês", "ganhe 5 kg de músculo", "10 cm de cintura em 30 dias") ou garantia ·
  NUTRIÇÃO FORA DA COMPETÊNCIA: prescrever dieta, cardápio, calorias ou suplemento com dose para o leitor ("monte sua
  dieta", "dieta de 1800 kcal", "tome 5 g de creatina") é atividade do nutricionista (Lei 8.234/1991) · ordem sobre
  remédio ou hormônio (assunto do médico). Promessa do que o PRODUTO entrega ("um treino montado para a sua rotina") é
  livre no CTA.
AVISO (conferir): ordem de comida ou suplemento sem dose ("coma mais proteína", "tome creatina") · slide que fala de
  dieta, proteína, caloria ou suplemento sem id da Ficha em "afirmacoes" (nutrição só como educação geral, com a fonte) ·
  "comida que emagrece", "exercício que seca a barriga" (queima localizada) · ordem de treino com número para o leitor
  ("faça 4 séries de 12": em conteúdo aberto, a faixa da evidência; a dose é individual) · 2ª pessoa (você, seu, sua,
  te…) fora dos slides com "funcao" aplicacao/cta (voz mista) · "virou" na headline · jargão · tom de coach ("é preciso",
  "devemos", "você precisa/deve", "sem desculpas") · contraste em fórmula ("X, não Y", "X. Não Y.") · dado vago leve
  ("a maioria dos…", "muita gente") · slide sem "funcao" · último slide antes do CTA que só resume · campos de topo do
  método BD ausentes ou fora da lista (tipo_carrossel, eixo, funil, cta, headline) · CTA "salvar"/"palavra" (o CTA é
  consultoria/treino individualizado, ou ebook se o Jorge tiver um material) · "cta" do topo diferente do "cta" do slide
  de CTA (no M5 vale o do slide, que vai para a arte) · consultoria sem o CREF no slide de CTA (M1–M4) · tipo "case" sem
  história real (id H) · mais de um CTA · linguagem leiga: sigla (RM, RIR, RPE, VO2, HIIT…, ou 2+ maiúsculas seguidas em
  campo que não é caixa-alta) e termo técnico (sarcoplasmática, síntese proteica, excêntrica, placebo, meta-análise,
  randomizado…, %) · M5: fundo escuro > 80 palavras ou claro > 100, 3 slides seguidos do mesmo fundo, tabela com menos
  de 3 linhas, CTA sem "ponte", tipo de slide ou componente fora da lista, setas/cards fora de 2–4/2–3 itens, mais de
  3 palavras em *destaque* no slide (a chamada da caixa do CTA conta), destaque fora do título no slide grad, título do
  grad fora de 2–4 palavras, card em slide que já tem título e corpo, slide interno só com tag + frase curta (menos de
  15 palavras, sem título nem componente).
Limites de caracteres (todos os modelos, inclusive o M5: por bloco, máx. 2 blocos, imagem_fundo só no dark) NÃO são
daqui: são do LIMITES/limites() do render_carrossel.py, conferidos pelo validar_carrossel.py (ERRO).

Como compara: o texto sai sem marcação (**, *, ==, _, <br>…), em minúsculas e sem acento, MENOS o verbo "é" isolado,
que fica com acento (para separar "é" de "e"). Só campos de texto (CAMPOS_TEXTO, menos FORA_DO_EDITORIAL).
Trecho entre aspas (“…”, "…", «…», ‘…’) = citação: ERRO vira AVISO e o que já era AVISO não conta. Desmentido ("não
existe dieta que…") com "não/nunca" logo antes não conta como ordem.
Cada mensagem diz o slide, o campo, o trecho e como reescrever.

PARA EDITAR AS REGRAS: mexa só nas listas de constantes logo abaixo. Cada regra é (padrão, nome, como reescrever).
O padrão é uma expressão regular escrita SEM ACENTO; o único acento que vale é o do verbo "é" isolado.
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

# ============================================================================================================
# CONSTANTES (edite aqui)
# ============================================================================================================

# Campos de texto que aparecem na arte, em todos os modelos. Os de M1–M4 são os de sempre; o M5 soma headline, ponte,
# setas, componente.* e cta.* (tag e titulo já existiam). O validar_carrossel.py usa esta mesma lista para a evidência.
CAMPOS_TEXTO = ("linha1", "linha2", "sub", "texto", "titulo", "itens", "antes", "palavra", "depois", "chamada", "fecho",
                "caixa", "topo", "base", "tag", "pre", "titulo_topo", "busca", "balao", "rodape", "cartoes", "nota",
                "janela", "barra", "script", "cursor",
                "headline", "ponte", "setas", "componente", "cta")
NAO_TEXTO = ("tipo",)  # dentro de componente/cta: é escolha de formato, não texto
FORA_DO_EDITORIAL = ("busca", "cursor", "cabecalho")  # layout (busca/cursor do M4, cabeçalho de tabela): sem regra editorial
CAMPOS_HEADLINE = ("headline", "pre", "titulo_topo", "topo", "linha1", "linha2", "base", "titulo")  # título da capa, na ordem
CAMPOS_TABELA = r"componente\.(?:linhas|valor|cabecalho)"  # número em tabela/stat: anglicismo numérico vira AVISO

FUNCOES = ("capa", "hook", "mecanismo", "prova", "expansao", "aplicacao", "direcao", "cta")
FUNCOES_2A_PESSOA = ("aplicacao", "cta")  # voz mista: só aqui pode "você"
FUNCAO_POR_TIPO = {"capa": "capa", "capa2": "capa", "cta": "cta", "pergunta": "cta"}  # quando o slide não tem "funcao"

TIPOS_CARROSSEL = ("tendencia", "tese", "tese-mito", "case", "previsao")

EIXOS = ("Mercado", "Cases", "Notícias", "Cultura", "Produto")  # os 5 do método (equivalente em treino: Método, seção 3)
FUNIS = ("topo", "meio", "fundo")
# CTA pelo conteúdo: consultoria = treino individualizado com o Jorge (padrão, link na bio, com nome e CREF);
# ebook = só se o Jorge tiver um material próprio (link na bio). "salvar" e "palavra" (ManyChat) continuam aceitos só
# com AVISO, para quando o Jorge decidir usar automação de comentário.
CTA_TIPOS = ("consultoria", "ebook")
CTA_ANTIGOS = ("salvar", "palavra")
REGISTRO = "CREF"  # o slide de CTA de consultoria (M1–M4) mostra o registro profissional (o valor fica no marca.json)

# ---- Modelo 5 (BrandsDecoded) ----
# Limites de caracteres, máximo de 2 blocos e "imagem_fundo" só no dark NÃO ficam aqui: são do LIMITES/limites() do
# render_carrossel.py (ERRO no validar_carrossel.py). Aqui ficam só as regras de densidade e de forma do método.
MODELO_M5 = "brandsdecoded"
FUNDO_M5 = {"capa": "foto", "dark": "escuro", "light": "claro", "grad": "degradê", "cta": "claro"}
PALAVRAS_MAX_M5 = {"escuro": 80, "degradê": 80, "claro": 100}
SEGUIDOS_MAX_M5 = 2  # 3 slides seguidos com o mesmo fundo = AVISO
TABELA_MIN_LINHAS = 3
SETAS_M5 = (2, 4)
CARDS_M5 = (2, 3)
COMPONENTES_M5 = ("card", "tabela", "stat", "setas", "cards")
DESTAQUE_MAX_M5 = 3  # palavras em *destaque* por slide (a chamada da caixa do CTA conta, porque também sai em degradê)
CHAMADA_CTA_M5 = {"salvar": "SALVA ESTE POST", "consultoria": "LINK NA BIO", "ebook": "LINK NA BIO"}  # texto padrão da caixa (modelo_brandsdecoded._cta)
TITULO_GRAD_M5 = (2, 4)  # frase de impacto do slide de direção: 2 a 4 palavras
PALAVRAS_MIN_INTERNO_M5 = 15  # slide interno sem título nem componente e com menos que isso = "tag + frase curta"

# ---- Regras: (padrão sem acento, nome, como reescrever) ----
_X = r"[^.!?;:,—–]{1,80}"  # o "X" de uma fórmula: um pedaço de frase sem pontuação no meio
_SER = r"(?:é|sao|era|eram|foi|foram)"

BINARIOS = [
    (r"\b(?:nao|nunca) " + _SER + r" sobre\b" + _X + r"\s*[,.;:!?—–]\s*(?:(?:mas|e) sim\b|" + _SER + r" sobre\b)",
     "«não é sobre X, é sobre Y»", "diga direto do que se trata, com o fato concreto, sem negar uma coisa para afirmar outra"),
    (r"\b(?:nao|nunca) " + _SER + r"\b" + _X + r"\s*[,.;:!?—–]\s*(?:(?:mas|e) sim\b|" + _SER + r"\b)",
     "«não é X, é Y»", "afirme só o que é, com o dado (ex.: «o que faz o músculo crescer é o volume da semana»)"),
    (r"\bnao\b[^.!?;]{1,80}?,\s*(?:mas|e) sim\b",
     "«não X, mas sim Y»", "afirme só o lado verdadeiro, com o fato que o sustenta"),
    (r"\bnao se trata de\b[^.!?]{1,80}?[,.;]\s*(?:(?:mas|e) sim\b|trata-se\b)",
     "«não se trata de X, mas de Y»", "diga direto do que se trata"),
    (r"\bdeix(?:a|am|ou|aram|ar|ando) de ser\b[^.!?]{1,80}?\b(?:(?:para|pra) (?:ser|virar|se tornar)|e (?:vira|virou|passa a ser|passou a ser))\b",
     "«deixa de ser X para ser Y»", "conte a mudança como fato: o que mudou, quando e por quê"),
    (r"(?:^|[.!?…]\s+)menos (?!de\b|do\b|da\b|que\b)[^.!?,;]{1,60}[.,;!]\s*mais (?!de\b|do\b|da\b|que\b)",
     "«Menos X. Mais Y.»", "escreva em prosa com conector («trocar X por Y ajuda porque…»)"),
    (r"(?:^|[.!?…]\s+)mais (?!de\b|do\b|da\b|que\b)[^.!?,;]{1,60}[.,;!]\s*menos (?!de\b|do\b|da\b|que\b)",
     "«Mais X. Menos Y.»", "escreva em prosa com conector («trocar X por Y ajuda porque…»)"),
    (r"(?:^|[.!?…]\s+)sem [^.!?]{1,60}[.!?…]\s+sem\b|(?:^|[.!?…]\s+)sem [^.!?,]{1,40},\s*sem\b",
     "«Sem X. Sem Y.»", "junte numa frase com sujeito e verbo, dizendo o que acontece de fato"),
    (r"\bantes\s*[:—–]\s*[^.!?]{1,80}[.!?;]?\s*(?:agora|hoje|depois)\s*[:—–]",
     "«Antes: X. Agora: Y.»", "conte a mudança em prosa, com data ou período («até 2017…; a revisão de 2024…»)"),
]

CACOETES = [
    (r"\bmuda(?:r|ria|ou|m)? tudo\b", "«e isso muda tudo»", "diga o que muda, para quem e quanto (com o dado da Ficha)"),
    (r"\bno fim das contas\b", "«no fim das contas»", "corte; a ideia fica de pé sem a transição"),
    (r"\bao final do dia\b", "«ao final do dia»", "corte (se é o horário de verdade, use «à noite»)"),
    (r"\ba (?:grande )?pergunta (?:que )?fica\b", "«a pergunta que fica»", "faça a pergunta direto, sem anunciá-la"),
    (r"\ba questao é(?:\s*:|\s+que\b)", "«a questão é:»", "corte o anúncio e diga a ideia"),
    (r"\bo ponto é(?:\s*:|\s+que\b)", "«o ponto é:»", "corte o anúncio e diga a ideia"),
    (r"\b(?:a logica|o mecanismo|a coisa|isso) funciona assim\b", "«o mecanismo funciona assim»",
     "explique o mecanismo direto, com a analogia"),
    (r"\b(?:em um|num) mundo (?:onde|em que)\b", "«em um mundo onde»", "comece direto no fato"),
    (r"\bvivemos (?:em )?(?:uma|numa) era\b", "«vivemos em uma era»", "comece direto no fato"),
    (r"\bcada vez mais\b", "«cada vez mais»", "use o dado real (quanto, desde quando) em vez da sensação"),
    (r"\bsimplesmente\b", "«simplesmente»", "corte"),
    (r"\bbasicamente\b", "«basicamente»", "corte"),
]

DE_FORMA = [
    (r"\bde (?:forma|maneira) (?!que\b|a\b|alguma\b|nenhuma\b|tal\b|como\b)[a-z]+",
     "«de forma X»", "diga como, com o fato concreto (ex.: «subiu toda semana», «em três meses»)"),
]

DADOS_VAGOS = [
    (r"\b(?:os |varios |muitos |alguns )?(?:estudos|pesquisas) (?:mostram|mostraram|dizem|apontam|indicam|comprovam|revelam|sugerem)\b|\ba ciencia (?:mostra|diz|comprova|aponta)\b",
     "«estudos mostram»", "diga qual estudo, em linguagem simples («uma revisão que juntou 15 estudos…»), com o id da Ficha"),
    (r"\b(?:os |muitos |varios )?especialistas (?:dizem|afirmam|apontam|alertam|recomendam|explicam)\b",
     "«especialistas dizem»", "diga quem («o posicionamento do Colégio Americano de Medicina do Esporte…»), com o id da Ficha"),
    (r"\bmuitas (?:empresas|marcas|academias)\b", "«muitas empresas/academias»", "dê o número ou o exemplo concreto"),
    (r"\ba maioria das pessoas\b", "«a maioria das pessoas»", "dê o número da Ficha («6 em cada 10…»)"),
    (r"\brecentemente\b", "«recentemente»", "dê a data ou o período («em 2025»)"),
]

ANGLICISMOS_NUM = [
    (r"(?<![\w.,])\d+(?:[.,]\d+)?\s?[x×](?!\w)", "«5x»", "escreva por extenso: «cinco vezes maior», «o dobro», «o triplo»"),
    (r"(?<![\w.,])\d+\+", "«10+»", "escreva «mais de 10»"),
    (r"(?<![\w/.,-])\d{1,3}(?:[.,]\d+)?\s?[-–]\s?\d{1,3}(?:[.,]\d+)?(?![\w/])", "«2-3 anos»",
     "escreva «duas ou três vezes» / «de 10 a 20 séries»"),
]

ABERTURAS = [
    (r"\bhoje (?:vamos|vou) falar\b|\bvamos falar (?:sobre|de)\b", "«hoje vamos falar»", "comece no fato, no dado ou na tensão"),
    (r"\b(?:neste|nesse|este|esse) carrossel\b", "«neste carrossel» (metalinguagem)", "fale do assunto, não do post"),
    (r"\bantes de comecar\b", "«antes de começar»", "comece no fato"),
    (r"\bcomo voce (?:provavelmente |ja )?sabe\b", "«como você provavelmente sabe»", "comece no fato"),
    (r"\bmuitas pessoas (?:me )?perguntam\b|\bmuita gente (?:me )?pergunta\b", "«muitas pessoas perguntam»",
     "comece na dúvida concreta, sem anunciá-la"),
    (r"\btodo mundo ja ouviu\b", "«todo mundo já ouviu»", "comece no fato"),
]

FECHOS = [
    (r"\bcontinu[ae] no proximo\b", "«continue no próximo»", "corte; a tensão do texto é que leva ao próximo slide"),
    (r"\b(?:arrast|desliz)(?:e|a|ar)\s+(?:para|pra|pro)\b", "«arraste para o lado»", "corte; o próximo slide vem pela tensão"),
    (r"\bswipe\b", "«swipe»", "corte; o próximo slide vem pela tensão"),
    (r"\bmas tem mais\b", "«mas tem mais»", "corte; deixe uma pergunta concreta em aberto"),
    (r"\bnao para por ai\b", "«não para por aí»", "corte; deixe uma pergunta concreta em aberto"),
]

CTA_CORDIAL = [
    (r"\bespero que (?:voce )?(?:tenha|tenham) gostado\b", "«espero que tenha gostado»",
     "CTA diretivo: «Treino individualizado: link na bio»"),
    (r"\bobrigad[oa] (?:por|pela|pelo)\b", "«obrigado por…»", "corte o agradecimento; só a ação"),
    (r"\bnao (?:se )?esquec(?:a|e)m? de (?:me )?seguir\b", "«não esqueça de seguir»", "um CTA só: consultoria (treino individualizado)"),
    (r"\bse (?:esse|este) (?:conteudo|post|carrossel) (?:te )?ajudou\b", "«se esse conteúdo te ajudou»",
     "CTA diretivo, sem condicional"),
    (r"\bse (?:voce )?tiver (?:alguma )?duvidas?\b", "«se tiver dúvidas»", "CTA diretivo: consultoria (treino individualizado)"),
]

HEADLINE_PROIBIDA = [  # na capa (campos CAMPOS_HEADLINE juntos) e no "headline" do topo
    (r"^(?:descubra|saiba|conheca)\b", "começa com «descubra/saiba/conheça»",
     "abra com o fato, o conflito ou a investigação («O fim do…:», «Investigando…»)"),
    (r"^quando\b[^.!?]{1,80}\bvir(?:a|am|ou|aram)\b", "«quando X vira Y»", "nomeie o fenômeno com o dado concreto"),
    (r"\ba ascensao d[aeo]s?\b", "«a ascensão de X»", "diga o que cresceu, quanto e onde"),
    (r"\bo impacto d[aeo]s?\b", "«o impacto de X»", "diga qual efeito, em quem"),
    (r"\b(?:tudo )?(?:o )?que voce precisa saber\b", "«tudo que você precisa saber»", "prometa a descoberta específica"),
    (r"\bo guia definitivo\b", "«o guia definitivo»", "prometa a descoberta específica"),
    (r"\bmud(?:ou|aram|a|am|ar) para sempre\b", "«mudou para sempre»", "diga o que mudou e desde quando"),
    (r"\b(?:revelamos|descobrimos|mostramos)\b", "«revelamos/descobrimos/mostramos»", "o assunto é o sujeito, não nós"),
    (r"\bpor que\b[^.!?]{1,60}\besta(?:o)? mudando\b", "«por que X está mudando Y»", "diga a mudança concreta"),
]
HEADLINE_AVISO = [
    (r"\bvir(?:ou|aram)\b", "«virou» como verbo", "troque por um verbo concreto (ex.: «passou a…», «ganhou…», «perdeu…»)"),
]

DADOS_VAGOS_AVISO = [
    (r"\ba maioria d(?:os|as)\b", "«a maioria dos…»", "se a Ficha tem o número, use («6 em cada 10…»)"),
    (r"\bmuita gente\b|\bmuitas pessoas\b", "«muita gente»", "se a Ficha tem o número, use"),
]
CONTRASTES_AVISO = [
    (r",\s*(?:e\s+)?nao (?!por acaso)(?:de|do|dos|das|com|por|pelo|pela|em|no|na|nos|nas|um|uma)\b[^.!?,;]{1,50}(?=[.!?]|$)",
     "«X, não Y»", "afirme o que é e mostre por quê; o contraste vem do fato, não da fórmula"),
    (r"(?:^|[.!?…]\s+)nao (?!por acaso)(?:quando|porque|pelo|pela|por|com|no|na|nos|nas|em|um|uma)\b",
     "«X. Não Y.»", "junte numa frase com conector, ou corte a negação"),
]
COACH = [
    (r"(?<!nao )\bé preciso\b", "«é preciso»", "descreva o que acontece ou o que a evidência mostra, sem dar ordem"),
    (r"\bdevemos\b", "«devemos»", "descreva o que acontece ou o que a evidência mostra, sem dar ordem"),
    (r"\bvoce (?:precisa|deve|tem que|tem de)\b", "«você precisa/deve»",
     "reportagem: «quem treina X costuma…»; ordem para o leitor só no CTA"),
    (r"\bsem desculpas\b|\bno pain,? no gain\b|\bfoco,? forca e fe\b|\bsai do sofa\b", "frase de coach motivacional",
     "troque pelo fato que motiva (o dado da Ficha), sem bordão"),
]
JARGOES = [
    (r"\becossistema", "«ecossistema»", "troque por «sistema», «ambiente»"),
    (r"\bsinergia", "«sinergia»", "troque por «integração», «junto»"),
    (r"\bdisruptiv", "«disruptivo»", "troque por «que quebra o padrão»"),
    (r"\bstakeholders?\b", "«stakeholders»", "troque por «os envolvidos»"),
    (r"\bmindset\b", "«mindset»", "troque por «mentalidade», «jeito de pensar»"),
    (r"\bcuradoria\b", "«curadoria»", "troque por «seleção», «escolha»"),
    (r"\bstorytelling\b", "«storytelling»", "troque por «história», «narrativa»"),
    (r"\boverview\b", "«overview»", "troque por «panorama», «visão geral»"),
    (r"\bbenchmark", "«benchmark»", "troque por «comparação», «referência»"),
    (r"\bshape\b", "«shape»", "troque por «corpo», «forma física»"),
]
OUTROS_AVISO = [
    (r"^na pratica\b", "abertura «na prática»", "vá direto para a prática"),
    (r"\bé claro que\b", "«é claro que»", "corte"),
]
# Ética do Profissional de Educação Física (Código de Ética do CONFEF) + regras da marca + limites legais das outras
# profissões (ERRO). Desmentido ("não existe dieta que…", "nunca pare o remédio por conta") não conta.
_PRAZO = (r"(?:(?:\d+|um|uma|dois|duas|tres|quatro|cinco|seis|sete|oito|nove|dez|quinze|vinte|trinta)\s+dias?|"
          r"(?:[1-8]|uma|duas|tres|quatro|cinco|seis|sete|oito)\s+semanas?|(?:[1-3]|um|dois|tres)\s+(?:mes|meses))")
_MEDIDA_CORPO = r"(?:kg|kgs|quilos?|kilos?|cm|centimetros?)"
ETICA = [
    (r"\bantes e depois\b(?!\s+(?:d[aeo]s?|em|n[ao]s?)\s+(?!alunos?\b|alunas?\b|clientes?\b|pacientes?\b))|\bantes\s*/\s*depois\b",
     "«antes e depois»", "sem antes/depois (ética do CONFEF e regra da marca): mostre o mecanismo e o número da Ficha, "
     "nunca o resultado de uma pessoa"),
    (r"\bdepoimentos? d[aeo]s? (?:\w+ )?(?:alunos?|alunas?|clientes?|pacientes?)\b", "«depoimento de aluno»",
     "sem depoimento de aluno (sigilo e respeito ao aluno, CONFEF): use o fato da Ficha ou uma história real pública e "
     "verificável (id H)"),
    (r"\b(?:meus|minhas|meu|minha|nossos|nossas) (?:alunos?|alunas?|clientes?|pacientes?)\b[^.!?]{0,50}?\b(?:perdeu|perderam|"
     r"emagreceu|emagreceram|ganhou|ganharam|secou|secaram|eliminou|eliminaram|conquistou|conquistaram|transformou|"
     r"curou|largou|largaram)\b",
     "«meus alunos» com resultado", "sem caso de aluno (CONFEF): o case é só história pública verificável (id H)"),
    (r"r\$\s?\d|\b\d+(?:[.,]\d+)?\s?reais\b|\bpor apenas\b|\bcupom\b|\bdesconto de\b|\bpromocao (?:imperdivel|relampago)\b",
     "preço/promoção", "sem preço nem promoção no conteúdo aberto (regra da marca; o CONFEF veda disputa por preço)"),
    # promessa de resultado com número no corpo do leitor; prazo de estudo («2 kg de músculo em 6 meses no grupo…») passa
    (r"(?<!grupo )\b\d+(?:[.,]\d+)?\s?" + _MEDIDA_CORPO + r"\s+(?:a menos\s+|a mais\s+)?(?:de\s+\w+\s+)?em\s+"
     r"(?:(?:so|apenas|ate|menos de)\s+)?" + _PRAZO + r"\b",
     "promessa de resultado (medida × prazo)", "sem promessa de resultado (CONFEF): nada de «X kg em N dias»; fale do "
     "processo, da rotina e do que a evidência mostra para grupos"),
    (r"(?<!nao )(?<!nunca )\b(?:perder|eliminar|emagrecer|secar|derreter|ganhar)\s+ate\s+\d|"
     r"\b(?:perca|percam|elimine|eliminem|emagreca|emagrecam|seque|sequem|derreta|derretam|ganhe|ganhem|conquiste)\s+"
     r"(?:\w+\s+){0,2}?\d+(?:[.,]\d+)?\s?" + _MEDIDA_CORPO + r"\b|"
     r"(?<!quem )(?<!que )\b(?:quer|vai|vamos)\s+(?:te\s+)?(?:fazer\s+)?(?:perder|emagrecer|eliminar|secar|ganhar)\b"
     r"[^.!?;]{0,25}?\d+(?:[.,]\d+)?\s?" + _MEDIDA_CORPO + r"\b",
     "promessa de resultado (meta de quilos/medidas)", "sem meta de quilos ou centímetros para o leitor (CONFEF); fale "
     "do processo e da rotina"),
    (r"(?<!existe )(?<!nenhum )(?<!sem )(?<!ha )\b(?:resultados?|emagrecimento|perda de peso|hipertrofia|ganho de massa)\s+"
     r"garantid[oa]s?\b|(?<!nao )(?<!ninguem )\bgarant(?:o|imos|ido|ida)\s+(?:o\s+|a\s+|seu\s+|sua\s+)?(?:resultado|"
     r"emagrecimento|perda|hipertrofia|ganho)",
     "resultado garantido", "sem promessa de resultado (CONFEF): nenhum resultado é garantido"),
    # NUTRIÇÃO: prescrever dieta, cardápio, calorias ou suplemento com dose é do nutricionista (Lei 8.234/1991).
    (r"(?<!nao )(?<!nunca )\b(?:tome|tomem|tomar|use|usem|consuma|consumam|coma|comam|beba|bebam|ingira|ingiram|inclua|"
     r"incluam|suplemente|suplementem)\b[^.!?;]{0,40}?\b\d+(?:[.,]\d+)?\s?(?:g|mg|mcg|ml|l|ui|gramas?|miligramas?|kcal|"
     r"calorias|capsulas?|comprimidos?|colher(?:es)?|xicaras?|copos?|doses?|scoops?|saches?)\b",
     "prescrição com dose (comida/suplemento)", "prescrever comida ou suplemento com dose é do nutricionista (Lei "
     "8.234/1991): eduque com o que a Ficha diz para grupos («a revisão cita…»), sem ordem com dose"),
    (r"(?<!nao )(?<!nunca )\b(?:monte|montem|siga|sigam|faca|facam|segue)\s+(?:a\s+|essa\s+|esta\s+)?(?:sua|minha|essa|esta)\s+"
     r"(?:dieta|cardapio|plano alimentar)\b|\b(?:dieta|cardapio|plano alimentar)\s+(?:de\s+)?\d+\s?(?:kcal|calorias)\b|"
     r"\b(?:cardapio|dieta|plano alimentar)\s+(?:pra|para)\s+(?:voce|voces|secar|emagrecer|ganhar|definir|crescer)\b|"
     r"\b(?:sua|seu)\s+(?:dieta|cardapio|plano alimentar)\s+(?:deve|precisa|tem que)\b",
     "prescrição de dieta", "dieta é atividade do nutricionista (Lei 8.234/1991): no conteúdo do Jorge, nutrição só como "
     "educação geral, com a fonte da Ficha («a revisão de 2024 encontrou…»), e encaminhe para um nutricionista"),
    (r"(?<!nao )(?<!nunca )\b(?:pare|parem|suspenda|suspendam|interrompa|interrompam|troque|troquem|largue|larguem|abandone|"
     r"abandonem)\b[^.!?;]{0,25}?\b(?:remedios?|medicacao|medicamentos?|tratamento|insulina|hormonios?|comprimidos?)\b|"
     r"(?<!nao )(?<!nunca )\b(?:use|usem|tome|tomem|aplique|apliquem|comece|comecem)\s+(?:a\s+)?(?:\w+\s+){0,2}?"
     r"(?:anabolizantes?|esteroides?|testosterona|hormonios?|ozempic|semaglutida|tirzepatida|mounjaro)\b",
     "ordem sobre remédio ou hormônio", "remédio e hormônio são assunto do médico (fora da competência do profissional "
     "de Educação Física): «a decisão é com o médico que acompanha»"),
]
# AVISO de ética: ordem sem número ou fora da competência que pede atenção (não bloqueia).
ETICA_AVISO = [
    (r"(?<!nao )(?<!nunca )\b(?:coma|comam|tome|tomem|beba|bebam|corte|cortem|evite|evitem|aumente|aumentem|reduza|reduzam|"
     r"inclua|incluam)\s+(?:\w+\s+){0,2}?(?:proteinas?|carboidratos?|carbos?|acucar(?:es)?|gorduras?|calorias|whey|creatina|"
     r"suplementos?|cafeina|pre-?treino|termogenicos?|jejum|gluten|lactose)\b",
     "ordem de comida/suplemento", "ordem de comida ou suplemento para o leitor soa como prescrição (nutricionista): "
     "troque pelo que a evidência mostra para grupos, com o id da Ficha, e encaminhe para o nutricionista"),
    (r"\b(?:faca|facam|faz)\s+(?:\w+\s+){0,2}?\d+\s+(?:series|repeticoes|reps|minutos|treinos)\b",
     "ordem de treino com número", "em conteúdo aberto, fale da faixa que a evidência mostra (com o id da Ficha) e "
     "lembre que a dose é individual (avaliação com profissional)"),
]
PROMESSA_AVISO = [
    (r"\b(?:alimentos?|lanches?|receitas?|comidas?|doces?|chas?|bebidas?|sucos?)\s+que\s+(?:emagrece|emagrecem|vai te emagrecer|"
     r"vao te emagrecer|secam?|derretem?)\b",
     "«comida que emagrece»", "nenhum alimento emagrece sozinho (e dieta é do nutricionista): fale do treino e da rotina"),
    (r"\b(?:exercicios?|treinos?|abdominais?|movimentos?)\s+(?:\w+\s+){0,2}?(?:que|pra|para)\s+(?:seca|secam|secar|queima|"
     r"queimam|queimar|derrete|derretem|derreter|perder|eliminar)\s+(?:a\s+)?(?:barriga|gordura localizada|culote|pochete|"
     r"gordura da barriga)\b",
     "«exercício que seca a barriga»", "a evidência não mostra queima localizada: fale do gasto total e da constância"),
]
# Linguagem leiga (AVISO): termo técnico que tem troca leiga (tabela de linguagem leiga do Método).
TERMOS_TECNICOS = [
    (r"\bplacebos?\b", "«placebo»", "troque por «um grupo que achava que estava recebendo X, mas não estava»"),
    (r"\bmeta[- ]?analises?\b|\brevis(?:ao|oes) sistematicas?\b", "«meta-análise / revisão sistemática»",
     "troque por «um estudo que juntou X estudos» / «uma revisão com N pessoas»"),
    (r"\bensaios?(?: clinicos?)?\b|\brandomizad", "«ensaio / randomizado»", "troque por «um teste em que metade fez X e metade não»"),
    (r"\bcoortes?\b|\bdesfechos?\b|\bmeta-?regress", "«coorte / desfecho / meta-regressão»", "troque pela palavra do dia a dia"),
    (r"\bsarcoplasmatic|\bmiofibril", "«sarcoplasmática / miofibrilar»", "troque por «o músculo cresce por dentro» e explique com analogia"),
    (r"\bsintese (?:de )?proteic|\bsintese de proteina", "«síntese proteica»", "troque por «a construção de músculo»"),
    (r"\bexcentric|\bconcentric", "«excêntrica / concêntrica»", "troque por «a fase de descida / de subida do movimento»"),
    (r"\bisometri", "«isometria»", "troque por «segurar parado na posição»"),
    (r"\bsarcopenia\b", "«sarcopenia»", "troque por «a perda de músculo com a idade»"),
    (r"\bperiodizacao\b", "«periodização»", "troque por «o plano que muda o treino ao longo das semanas»"),
    (r"\bfalha (?:muscular|concentrica)\b", "«falha muscular»", "troque por «até não conseguir mais nenhuma repetição»"),
    (r"(?<![\d.,])\d+(?:[.,]\d+)?\s?%|\bpor cento\b", "porcentagem",
     "prefira o número simples e comparativo («1 em cada 4», «o dobro», «de 10 para 20 séries»)"),
]
# Siglas (AVISO): as conhecidas do treino e da estatística, em qualquer campo; e, em campo que não é caixa-alta,
# qualquer sequência de 2+ maiúsculas. SIGLAS_OK são de uso leigo (ou da própria marca e do Instagram).
SIGLAS = (r"(?<![A-Za-zÀ-ÿ])(?:\d*RM|RIR|RPE|VO2(?:\s?m[aá]x)?|HIIT|LISS|DOMS|EPOC|TMB|NEAT|mTOR|NNT|RR|IC|ECR|RCT|LDL|HDL|"
          r"ACSM|NSCA)(?![a-zà-ÿ])")
SIGLAS_OK = ("CREF", "CONFEF", "SUS", "OMS", "AVC", "IMC", "OK", "TV", "PDF", "NA", "ANVISA", "BIO", "LINK")
ROTULOS = ("tag", "rotulo")  # rótulo de seção ("NA PRÁTICA", "COMO FUNCIONA"): não é frase
SO_TEXTO_CORRIDO = ("abertura «na prática»",)  # regras (pelo nome) que não valem em rótulo
# Assunto de nutrição: slide que fala disso sem id da Ficha em "afirmacoes" = AVISO (nutrição só como educação geral,
# com a fonte da Ficha; o validar_carrossel.py confere o id).
NUTRICAO = (r"\b(?:dietas?|cardapios?|plano alimentar|proteinas?|carboidratos?|calorias?|kcal|deficit calorico|"
            r"superavit|whey|creatina|suplementos?|suplementacao|jejum|macronutrientes?|comida|alimentacao)\b")

SEGUNDA_PESSOA = r"\b(?:voce|voces|vc|vcs|seu|sua|seus|suas|te|teu|tua|teus|tuas|contigo)\b"
RESUMO = r"^(?:em resumo|resumindo|em suma|recapitulando|enfim)\b"  # último slide antes do CTA que só resume

# ============================================================================================================
# Normalização
# ============================================================================================================
_PALAVRA = re.compile(r"[0-9A-Za-zÀ-ÿ]+(?:[-'’][0-9A-Za-zÀ-ÿ]+)*")
_ASPAS = re.compile(r"“[^”]*”|\"[^\"]*\"|«[^»]*»|‘[^’]*’")


def _sem_acento(t, manter_e=True):
    """Tira acentos; com manter_e, o 'é' (já marcado com \\x01) volta acentuado."""
    t = "".join(c for c in unicodedata.normalize("NFD", t) if unicodedata.category(c) != "Mn")
    return t.replace("\x01", "é") if manter_e else t


def norm(t):
    """Minúsculas sem acento, menos o verbo 'é' isolado. Mesmo comprimento do texto em NFC (posições batem)."""
    t = unicodedata.normalize("NFC", t).lower()
    return _sem_acento(re.sub(r"(?<!\w)é(?!\w)", "\x01", t))


def _rx(padrao):
    """Compila um padrão das listas: tira acentos, menos o 'é' (que no padrão é sempre o verbo)."""
    return re.compile(_sem_acento(unicodedata.normalize("NFC", padrao).replace("é", "\x01")))


def _compilar(lista):
    return [(_rx(p), nome, dica) for p, nome, dica in lista]


def limpar(t):
    """Texto como aparece na arte: sem marcação (**, *, ==, !!, ~~, {{ }}, _, <br>, |, '> ' do M1), espaços simples."""
    t = unicodedata.normalize("NFC", str(t))
    t = re.sub(r"<[^>]+>", " ", t).replace("|", " ").replace("\n", " ")
    t = re.sub(r"^\s*>\s*", "", t)
    t = re.sub(r"\*\*|\*|==|!!|~~|\{\{|\}\}", "", t)
    t = re.sub(r"(?<![\w/])_|_(?!\w)", "", t)
    return re.sub(r"\s+", " ", t).strip()


def palavras(t):
    return len(_PALAVRA.findall(limpar(t)))


# Grupos na ordem em que rodam (o primeiro que achar um trecho fica com ele; os seguintes não repetem o mesmo trecho).
REGRAS = [
    ("estrutura binária", "ERRO", _compilar(BINARIOS)),
    ("cacoete de IA", "ERRO", _compilar(CACOETES)),
    ("construção vaga", "ERRO", _compilar(DE_FORMA)),
    ("dado vago", "ERRO", _compilar(DADOS_VAGOS)),
    ("anglicismo numérico", "ERRO", _compilar(ANGLICISMOS_NUM)),
    ("abertura proibida", "ERRO", _compilar(ABERTURAS)),
    ("fechamento proibido", "ERRO", _compilar(FECHOS)),
    ("CTA cordial", "ERRO", _compilar(CTA_CORDIAL)),
    ("ética", "ERRO", _compilar(ETICA)),
    ("ética", "AVISO", _compilar(ETICA_AVISO)),
    ("promessa sem número", "AVISO", _compilar(PROMESSA_AVISO)),
    ("dado vago", "AVISO", _compilar(DADOS_VAGOS_AVISO)),
    ("possível estrutura binária", "AVISO", _compilar(CONTRASTES_AVISO)),
    ("tom de coach", "AVISO", _compilar(COACH)),
    ("jargão", "AVISO", _compilar(JARGOES)),
    ("estilo", "AVISO", _compilar(OUTROS_AVISO)),
    ("linguagem leiga: termo técnico", "AVISO", _compilar(TERMOS_TECNICOS)),
]
_SIGLAS = re.compile(SIGLAS)
_MAIUSCULAS = re.compile(r"(?<![\wÀ-ÿ])[A-ZÀ-Ý]{2,}\d*(?![\wÀ-ÿ])")
_HEADLINE_E = _compilar(HEADLINE_PROIBIDA)
_HEADLINE_A = _compilar(HEADLINE_AVISO)
_2A_PESSOA = _rx(SEGUNDA_PESSOA)
_RESUMO = _rx(RESUMO)
_TABELA = re.compile(CAMPOS_TABELA)
_NUTRICAO = _rx(NUTRICAO)


# ============================================================================================================
# Leitura do JSON
# ============================================================================================================
def campos_de_texto(s, editorial=False):
    """[(campo, texto)] do slide: CAMPOS_TEXTO, descendo em listas e dicionários (componente.linhas[2][1], cta.palavra…).
    editorial=True tira os campos de layout (FORA_DO_EDITORIAL)."""
    out = []
    pular = FORA_DO_EDITORIAL if editorial else ()

    def rec(caminho, v):
        if isinstance(v, str):
            if v.strip():
                out.append((caminho, v))
        elif isinstance(v, list):
            for k, x in enumerate(v, 1):
                rec(f"{caminho}[{k}]", x)
        elif isinstance(v, dict):
            for k, x in v.items():
                if k not in NAO_TEXTO and k not in pular:
                    rec(f"{caminho}.{k}", x)

    for k in CAMPOS_TEXTO:
        if k not in pular and k in s:
            rec(k, s[k])
    return out


def funcao(s):
    """'funcao' do slide (sem acento), ou a inferida pelo tipo (capa, cta) quando falta."""
    f = norm(str(s.get("funcao") or "")).strip()
    return f or FUNCAO_POR_TIPO.get(s.get("tipo"))


def prefixo(n, s):
    f = norm(str(s.get("funcao") or "")).strip()
    return f"slide-{n:02d} ({s.get('tipo', '?')}" + (f" · {f}" if f else "") + ")"


def _trecho(texto, m, maximo=70):
    """O trecho achado, esticado até o fim da frase (no máximo `maximo` caracteres)."""
    a, b = m.span()
    fim = re.search(r"[.!?…;](?=\s|$)", texto[b:])
    t = texto[a:b + fim.start() if fim else len(texto)].strip(" .,;:!?—–")
    return t if len(t) <= maximo else t[:maximo - 1].rstrip() + "…"


def _aspas(texto):
    return [m.span() for m in _ASPAS.finditer(texto)]


def _dentro(span, aspas):
    return any(a <= span[0] and span[1] <= b for a, b in aspas)


def _sobrepoe(span, ocupados):
    return any(span[0] < b and a < span[1] for a, b in ocupados)


# ============================================================================================================
# Checagens
# ============================================================================================================
def _checar_campo(pre, campo, valor, func, E, A):
    texto = limpar(valor)
    if not texto:
        return
    t = norm(texto)
    aspas = _aspas(texto)
    ocupados = []
    rotulo = re.match(r"[a-z_]*", campo).group(0) in ROTULOS
    for grupo, nivel, regras in REGRAS:
        if nivel == "ERRO" and grupo == "anglicismo numérico" and _TABELA.match(campo):
            nivel = "AVISO"
        for rx, nome, dica in regras:
            if rotulo and nome in SO_TEXTO_CORRIDO:
                continue
            m = next((m for m in rx.finditer(t) if not _sobrepoe(m.span(), ocupados)), None)
            if not m:
                continue
            ocupados.append(m.span())
            citacao = _dentro(m.span(), aspas)
            if citacao and nivel == "AVISO":
                continue
            msg = f"{pre} · {campo}: {grupo} {nome} em «{_trecho(texto, m)}»"
            if citacao:
                A.append(f"{msg} está entre aspas: se é citação literal de alguém, pode ficar; se não → {dica}")
            else:
                (E if nivel == "ERRO" else A).append(f"{msg} → {dica}")
    if func not in FUNCOES_2A_PESSOA:
        achados = []
        for m in _2A_PESSOA.finditer(t):
            p = texto[m.start():m.end()].lower()
            if not _dentro(m.span(), aspas) and not _sobrepoe(m.span(), ocupados) and p not in achados:
                achados.append(p)
        if achados:
            A.append(f"{pre} · {campo}: 2ª pessoa ({', '.join('«' + p + '»' for p in achados)}) fora da aplicação/CTA → "
                     f"reescreva em 3ª pessoa, tom de reportagem («quem treina…», «a pessoa…»); se «seu/sua» é de "
                     f"outra pessoa («o aluno e seu treinador»), ignore")


def _checar_siglas(pre, campo, valor, A, ok=()):
    """Linguagem leiga: siglas do treino e da estatística em qualquer campo; em campo que não é caixa-alta, qualquer 2+ maiúsculas seguidas."""
    texto = re.sub(r"\bCREF\s*\d+(?:\s*-\s*[A-Z])?(?:\s*/\s*[A-Z]{2})?", " ", limpar(valor))  # registro (CREF 000000-G/UF)
    letras = [c for c in texto if c.isalpha()]
    caixa_alta = letras and sum(c.isupper() for c in letras) / len(letras) > 0.6
    achados = [m.group(0) for m in _SIGLAS.finditer(texto)]
    if not caixa_alta:
        achados += [m.group(0) for m in _MAIUSCULAS.finditer(texto) if m.group(0) not in SIGLAS_OK and m.group(0) not in ok]
    achados = list(dict.fromkeys(achados))
    if achados:
        A.append(f"{pre} · {campo}: linguagem leiga: sigla ou caixa-alta {', '.join('«' + x + '»' for x in achados)} → troque "
                 f"pelo nome leigo (tabela de linguagem leiga do Método: «repetições que ainda sobravam», «treino "
                 f"intervalado», «o colégio americano de medicina do esporte»); se for palavra em caixa-alta para dar ênfase, use **negrito**")


def _checar_headline(pre, campo, texto, E, A):
    t = norm(limpar(texto))
    for rx, nome, dica in _HEADLINE_E:
        m = rx.search(t)
        if m:
            E.append(f"{pre} · {campo}: headline proibida {nome} em «{_trecho(limpar(texto), m)}» → {dica}")
    for rx, nome, dica in _HEADLINE_A:
        m = rx.search(t)
        if m:
            A.append(f"{pre} · {campo}: headline com {nome} → {dica}")


def _titulo_da_capa(s):
    """(nome dos campos, texto junto) do título da capa, ou None."""
    campos = [(k, s[k]) for k in CAMPOS_HEADLINE if isinstance(s.get(k), str) and limpar(s[k])]
    if not campos:
        return None
    return "+".join(k for k, _ in campos), " ".join(limpar(v) for _, v in campos)


def _ctas_dos_slides(slides):
    return [s["cta"] for s in slides if funcao(s) == "cta" and isinstance(s.get("cta"), dict)]


def _cta_do_carrossel(C, slides):
    """O CTA que vale: o do slide de CTA (é o que vai para a arte, no M5); sem ele, o do topo."""
    nos_slides = _ctas_dos_slides(slides)
    if nos_slides:
        return nos_slides[-1]
    return C["cta"] if isinstance(C.get("cta"), dict) else None


def _checar_topo(C, slides, A):
    faltam = [k for k in ("tipo_carrossel", "eixo", "funil") if not str(C.get(k) or "").strip()]
    cta = _cta_do_carrossel(C, slides)
    topo = C.get("cta") if isinstance(C.get("cta"), dict) else None
    if topo is not None and _ctas_dos_slides(slides) and cta is not topo:
        tt, ts = norm(str(topo.get("tipo") or "")).strip(), norm(str(cta.get("tipo") or "")).strip()
        pt, ps = norm(str(topo.get("palavra") or "")).strip(), norm(str(cta.get("palavra") or "")).strip()
        if tt != ts or (ts == "palavra" and pt != ps):
            A.append(f"cta: o «cta» do topo ({topo.get('tipo')}{' ' + str(topo.get('palavra')) if topo.get('palavra') else ''}) "
                     f"é diferente do «cta» do slide de CTA ({cta.get('tipo')}{' ' + str(cta.get('palavra')) if cta.get('palavra') else ''}) "
                     f"→ deixe os dois iguais: a arte usa o do slide; o funil, a legenda e o legendista leem o mesmo CTA")
    eixo = str(C.get("eixo") or "").strip()
    if eixo and norm(eixo) not in {norm(x) for x in EIXOS}:
        A.append(f"topo: eixo «{eixo}» fora da lista → use {', '.join(EIXOS)} (equivalente em treino: Método, seção 3)")
    if cta is None:
        faltam.append("cta")
    if not str(C.get("headline") or "").strip():
        faltam.append("headline")
    if faltam:
        A.append(f"topo: faltam os campos do método BD {', '.join('«' + k + '»' for k in faltam)} → no topo do JSON: "
                 f"\"tipo_carrossel\": \"{'|'.join(TIPOS_CARROSSEL)}\", \"eixo\": \"{'|'.join(EIXOS)}\", \"funil\": \"topo|meio|fundo\", "
                 f"\"headline\": \"<headline escolhida>\", \"cta\": {{\"tipo\": \"{'|'.join(CTA_TIPOS)}\"}} "
                 f"(carrossel antigo pode ficar sem)")
    tipo = norm(str(C.get("tipo_carrossel") or "")).strip()
    if tipo and tipo not in TIPOS_CARROSSEL:
        A.append(f"topo: tipo_carrossel «{C.get('tipo_carrossel')}» não existe → use {', '.join(TIPOS_CARROSSEL)}")
    funil = norm(str(C.get("funil") or "")).strip()
    if funil and funil not in FUNIS:
        A.append(f"topo: funil «{C.get('funil')}» não existe → use topo, meio ou fundo")
    if cta is not None:
        ct = norm(str(cta.get("tipo") or "")).strip()
        if ct in CTA_ANTIGOS:
            A.append(f"cta: «{ct}» não é o CTA padrão → CTA pelo conteúdo: \"consultoria\" (treino individualizado com o "
                     f"Jorge, link na bio) ou \"ebook\" (só se o Jorge tiver um material próprio)")
        elif ct not in CTA_TIPOS:
            A.append(f"cta: tipo «{cta.get('tipo') or ''}» inválido → use {', '.join(CTA_TIPOS)}")
        if ct == "palavra" and not str(cta.get("palavra") or "").strip():
            A.append("cta: tipo «palavra» sem a «palavra» → diga a palavra que a pessoa comenta (ex.: \"TREINO\")")
        if ct == "consultoria" and C.get("modelo", "manga-dark") != MODELO_M5:
            textos_cta = " ".join(limpar(v) for s in slides if funcao(s) == "cta" for _, v in campos_de_texto(s))
            if textos_cta and REGISTRO not in textos_cta.upper():
                A.append("cta: consultoria sem o CREF no slide de CTA → apresente o Jorge com nome e registro "
                         "(«Jorge Souto, treinador, CREF …», o número certo está no Gerador/marca.json); no M4, "
                         "«Consultoria no link da bio · Jorge Souto, CREF …» com uma ponte curta")
    if tipo == "case":
        ids = [str(x).strip().lstrip("#").upper() for s in slides
               for x in (s.get("afirmacoes") if isinstance(s.get("afirmacoes"), list) else [s.get("afirmacoes")]) if x]
        if not any(re.fullmatch(r"H\d+", i) for i in ids):
            A.append("topo: tipo «case» sem nenhuma história real citada → o case precisa de um id H (Histórias reais "
                     "verificáveis da Ficha) em \"afirmacoes\"")
    n_cta = [n for n, s in enumerate(slides, 1) if funcao(s) == "cta"]
    if len(n_cta) > 1:
        A.append(f"slides {', '.join(str(n) for n in n_cta)} são todos CTA → um CTA só (consultoria/treino individualizado)")


def _checar_nutricao(pre, s, A):
    """Nutrição só como educação geral, com a fonte: slide que fala de dieta, proteína, caloria ou suplemento sem id da
    Ficha em "afirmacoes" = AVISO (a prescrição em si já é ERRO na lista ETICA)."""
    if s.get("afirmacoes"):
        return
    for campo, valor in campos_de_texto(s, editorial=True):
        texto = limpar(valor)
        m = _NUTRICAO.search(norm(texto))
        if m and not _dentro(m.span(), _aspas(texto)):
            A.append(f"{pre} · {campo}: assunto de nutrição («{texto[m.start():m.end()]}») sem id da Ficha em \"afirmacoes\" "
                     f"→ no conteúdo do Jorge, nutrição só como educação geral, com a fonte da Ficha (prescrever dieta é do "
                     f"nutricionista); cite o id ou tire")
            return


def _checar_resumo_antes_do_cta(slides, A):
    i = next((k for k, s in enumerate(slides) if funcao(s) == "cta"), None)
    if not i:
        return
    s = slides[i - 1]
    for campo, valor in campos_de_texto(s, editorial=True):
        texto = limpar(valor)
        if _RESUMO.search(norm(texto)):
            A.append(f"{prefixo(i, s)} · {campo}: o último slide antes do CTA começa resumindo («{texto[:40]}…») → "
                     f"feche com uma virada (consequência, direção), não com um resumo")
            return


_DESTAQUE = re.compile(r"(?<!\*)\*(?![\s*])(.+?)(?<![\s*])\*(?!\*)")


def _destaques(v):
    """Palavras dentro de *destaque* (o **negrito** não conta)."""
    t = re.sub(r"\*\*(.+?)\*\*", r"\1", str(v))
    return [w for m in _DESTAQUE.finditer(t) for w in _PALAVRA.findall(m.group(1))]


def _checar_forma_m5(pre, s, tipo, A):
    """Regras de forma do design BD que só existiam no texto: destaque, título do grad, card, slide incompleto."""
    campos = campos_de_texto(s)
    marcadas = sum(len(_destaques(v)) for _, v in campos)
    if tipo == "cta":
        c = s.get("cta") if isinstance(s.get("cta"), dict) else {}
        ct = norm(str(c.get("tipo") or "palavra")).strip()
        chamada = c.get("palavra") or CHAMADA_CTA_M5.get(ct, "")
        marcadas += len(_PALAVRA.findall(limpar(chamada)))
    if marcadas > DESTAQUE_MAX_M5:
        extra = (" (a chamada da caixa do CTA já sai em degradê: em salvar e consultoria, tire o destaque do título)"
                 if tipo == "cta" else "")
        A.append(f"{pre}: {marcadas} palavras em destaque (máx. {DESTAQUE_MAX_M5} por slide) → destaque só a palavra-chave"
                 f"{extra}")
    if tipo == "grad":
        fora = [c for c, v in campos if not c.startswith("titulo") and _destaques(v)]
        if fora:
            A.append(f"{pre} · {fora[0]}: destaque fora do título no slide grad (sai branco, sem degradê) → no grad, "
                     f"*destaque* só no título")
        k = palavras(s.get("titulo") or "") if isinstance(s.get("titulo"), str) else 0
        if s.get("titulo") and not TITULO_GRAD_M5[0] <= k <= TITULO_GRAD_M5[1]:
            A.append(f"{pre} · titulo: {k} palavras no título do slide de direção → frase de impacto de "
                     f"{TITULO_GRAD_M5[0]} a {TITULO_GRAD_M5[1]} palavras (provocação, dado ou nome; nunca conselho)")
    comp = s.get("componente") if isinstance(s.get("componente"), dict) else {}
    if comp.get("tipo") == "card" and s.get("titulo") and s.get("texto"):
        A.append(f"{pre} · componente: card num slide que já tem título e corpo vira ruído (BD) → tire o título ou leve o "
                 f"texto do card para o corpo")
    if tipo in ("dark", "light", "grad") and not s.get("titulo") and not comp and not s.get("setas"):
        k = sum(palavras(v) for c, v in campos if not c.startswith("tag"))
        if k < PALAVRAS_MIN_INTERNO_M5:
            A.append(f"{pre}: só tag e {k} palavras → slide com tag + 1 frase curta parece incompleto (BD): expanda com o "
                     f"dado da Ficha ou funda com o vizinho")


def _checar_m5(slides, A):
    seguidos, ultimo = 0, None
    for n, s in enumerate(slides, 1):
        pre = prefixo(n, s)
        tipo = s.get("tipo")
        fundo = FUNDO_M5.get(tipo)
        _checar_forma_m5(pre, s, tipo, A)
        if fundo is None:
            A.append(f"{pre}: tipo «{tipo}» não existe no M5 → use {', '.join(FUNDO_M5)}")
        if fundo in PALAVRAS_MAX_M5:
            k = sum(palavras(v) for _, v in campos_de_texto(s))
            if k > PALAVRAS_MAX_M5[fundo]:
                A.append(f"{pre}: {k} palavras num slide de fundo {fundo} (meta do M5: até {PALAVRAS_MAX_M5[fundo]}) → "
                         f"corte o que repete e fique com o dado e a consequência")
        comp = s.get("componente")
        if comp is not None:
            ct = comp.get("tipo") if isinstance(comp, dict) else None
            if ct not in COMPONENTES_M5:
                A.append(f"{pre} · componente: tipo «{ct}» não existe → use {', '.join(COMPONENTES_M5)}")
            elif ct == "tabela":
                linhas = comp.get("linhas") if isinstance(comp.get("linhas"), list) else []
                if len(linhas) < TABELA_MIN_LINHAS:
                    A.append(f"{pre} · componente.linhas: tabela com {len(linhas)} linha(s) (mínimo {TABELA_MIN_LINHAS}) → "
                             f"complete com dados da Ficha ou troque por «stat» ou «card»")
            elif ct in ("setas", "cards"):
                itens = comp.get("itens", comp.get(ct))
                k = len(itens) if isinstance(itens, list) else 0
                lo, hi = SETAS_M5 if ct == "setas" else CARDS_M5
                if not lo <= k <= hi:
                    A.append(f"{pre} · componente: «{ct}» com {k} item(ns) (use de {lo} a {hi}) → ajuste a lista em \"itens\"")
        if isinstance(s.get("setas"), list) and not SETAS_M5[0] <= len(s["setas"]) <= SETAS_M5[1]:
            A.append(f"{pre} · setas: {len(s['setas'])} item(ns) (use de {SETAS_M5[0]} a {SETAS_M5[1]})")
        if tipo == "cta" and not limpar(s.get("ponte") or ""):
            A.append(f"{pre} · ponte: CTA sem frase-ponte → abra o slide com a frase que fecha o raciocínio "
                     f"(com **negrito**) antes de pedir a ação")
        if fundo and fundo == ultimo:
            seguidos += 1
            if seguidos == SEGUIDOS_MAX_M5 + 1 and fundo != "foto":
                A.append(f"{pre}: {seguidos} slides seguidos com fundo {fundo} → alterne dark e light (anatomia BD)")
        else:
            seguidos, ultimo = (1, fundo) if fundo else (0, None)


def validar(C):
    """Regras editoriais BD do carrossel (dicionário do carrossel.json) → (erros, avisos)."""
    E, A = [], []
    slides = [s for s in (C.get("slides") or []) if isinstance(s, dict)]
    _checar_topo(C, slides, A)
    capas = {}
    for n, s in enumerate(slides, 1):
        if funcao(s) == "capa":
            tc = _titulo_da_capa(s)
            if tc:
                capas[n] = tc
    head = limpar(C.get("headline") or "") if isinstance(C.get("headline"), str) else ""
    if head and norm(head) not in {norm(t) for _, t in capas.values()}:
        _checar_headline("topo", "headline", head, E, A)
        _checar_campo("topo", "headline", head, "capa", E, A)
    if head:
        _checar_siglas("topo", "headline", head, A)
    ok = tuple(str(c.get("palavra") or "").strip().upper() for c in [C.get("cta")] + _ctas_dos_slides(slides)
               if isinstance(c, dict) and c.get("palavra"))
    sem_funcao = []
    for n, s in enumerate(slides, 1):
        pre = prefixo(n, s)
        f = funcao(s)
        for campo, valor in campos_de_texto(s):
            _checar_siglas(pre, campo, valor, A, ok)
        if not str(s.get("funcao") or "").strip():
            sem_funcao.append(n)
        elif f not in FUNCOES:
            A.append(f"{pre}: funcao «{s.get('funcao')}» não existe → use {', '.join(FUNCOES)}")
        if n in capas:
            _checar_headline(pre, capas[n][0], capas[n][1], E, A)
        for campo, valor in campos_de_texto(s, editorial=True):
            _checar_campo(pre, campo, valor, f, E, A)
        _checar_nutricao(pre, s, A)
    if sem_funcao:
        A.append(f"slide(s) {', '.join(str(n) for n in sem_funcao)} sem \"funcao\" → marque o papel de cada slide "
                 f"({', '.join(FUNCOES)}); sem ela, o validador só libera a 2ª pessoa no slide de CTA")
    _checar_resumo_antes_do_cta(slides, A)
    if C.get("modelo") == MODELO_M5:
        _checar_m5(slides, A)
    return E, A


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    caminho = Path(sys.argv[1])
    C = json.loads(caminho.read_text(encoding="utf-8-sig"))
    E, A = validar(C)
    print("\n".join([f"editorial · {caminho.parent.name}/{caminho.name}"] + [f"ERRO  {x}" for x in E]
                    + [f"AVISO {x}" for x in A] + [f"{len(E)} erro(s), {len(A)} aviso(s)"]))
    sys.exit(1 if E else 0)


if __name__ == "__main__":
    main()
