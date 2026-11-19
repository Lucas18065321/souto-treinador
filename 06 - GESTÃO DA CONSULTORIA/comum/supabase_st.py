"""Cliente do Supabase sem pacote externo (só a biblioteca padrão do Python): banco pela API REST (PostgREST)
e arquivos pelo Storage. Usado pelo Painel ST e pelo agente de dieta.

A chave service_role vem de %USERPROFILE%\\SoutoTreinador\\privado\\supabase.env (nunca do repositório) e nunca é
impressa. Ela passa por cima da segurança por linha (RLS): por isso só roda no PC do Jorge, nunca no navegador.

Também tem o banco de demonstração (Demo): os mesmos métodos, com os dados fictícios de Painel ST/demo/, na memória.
"""
import copy
import datetime
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config_st  # noqa: E402


class ErroSupabase(RuntimeError):
    pass


class Supabase:
    """Banco real. `select("alunos", {"status": "eq.ativo", "order": "nome.asc"})` = GET /rest/v1/alunos?..."""
    modo = "supabase"

    def __init__(self, env=None):
        env = env or config_st.ler_env()
        self.url = (env.get("SUPABASE_URL") or "").rstrip("/")
        self._chave = env.get("SUPABASE_SERVICE_ROLE_KEY") or ""
        self.bucket = env.get("SUPABASE_BUCKET") or "entregas"
        self.rt_pin_hash = env.get("RT_PIN_HASH") or ""
        if not self.url or not self._chave:
            raise ErroSupabase(f"Falta SUPABASE_URL ou SUPABASE_SERVICE_ROLE_KEY em {env.get('_arquivo')} "
                               "(veja docs/guias/05-dieta-e-painel-st.md, passo 4).")
        if not re.match(r"^https://[a-z0-9-]+\.supabase\.(co|in)$", self.url) and not self.url.startswith("http://127.0.0.1"):
            raise ErroSupabase("SUPABASE_URL deve ser o endereço do projeto, como https://abcdefgh.supabase.co")

    def __repr__(self):  # nunca mostra a chave
        return f"<Supabase {self.url}>"

    # ---------- HTTP ----------
    def _pedir(self, metodo, rota, corpo=None, cabecalhos=None, bruto=False, tipo="application/json"):
        dados = None
        if corpo is not None:
            dados = corpo if isinstance(corpo, (bytes, bytearray)) else json.dumps(corpo, ensure_ascii=False, default=str).encode("utf-8")
        req = urllib.request.Request(self.url + rota, data=dados, method=metodo)
        req.add_header("apikey", self._chave)
        if not self._chave.startswith("sb_secret_"):  # chave antiga (JWT) vai também no Authorization; a nova "secret key" vai só no apikey
            req.add_header("Authorization", "Bearer " + self._chave)
        req.add_header("Content-Type", tipo)
        req.add_header("User-Agent", "PainelST/1.0")
        for k, v in (cabecalhos or {}).items():
            req.add_header(k, v)
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                conteudo = r.read()
        except urllib.error.HTTPError as e:
            detalhe = e.read().decode("utf-8", "replace")[:400]
            raise ErroSupabase(f"Supabase {e.code} em {metodo} {rota.split('?')[0]}: {detalhe}") from None
        except urllib.error.URLError as e:
            raise ErroSupabase(f"sem conexão com o Supabase ({e.reason})") from None
        if bruto:
            return conteudo
        return json.loads(conteudo.decode("utf-8")) if conteudo else None

    @staticmethod
    def _q(params):
        return ("?" + urllib.parse.urlencode(params, safe=",.()*:-", quote_via=urllib.parse.quote)) if params else ""

    # ---------- banco ----------
    def select(self, tabela, params=None):
        params = dict(params or {})
        params.setdefault("select", "*")
        saida, inicio, passo = [], 0, 1000
        while True:  # o PostgREST devolve no máximo 1000 linhas por pedido
            lote = self._pedir("GET", f"/rest/v1/{tabela}{self._q(params)}", cabecalhos={"Range": f"{inicio}-{inicio + passo - 1}"})
            saida += lote or []
            if not lote or len(lote) < passo or "limit" in params:
                return saida
            inicio += passo

    def um(self, tabela, id_):
        r = self.select(tabela, {"id": f"eq.{id_}"})
        return r[0] if r else None

    def inserir(self, tabela, linhas):
        r = self._pedir("POST", f"/rest/v1/{tabela}", linhas, {"Prefer": "return=representation"})
        return r if isinstance(linhas, list) else (r[0] if r else None)

    def atualizar(self, tabela, id_, valores):
        r = self._pedir("PATCH", f"/rest/v1/{tabela}?id=eq.{urllib.parse.quote(str(id_))}", valores, {"Prefer": "return=representation"})
        if not r:
            raise ErroSupabase(f"nada atualizado em {tabela} (id não achado)")
        return r[0]

    def apagar(self, tabela, id_):
        self._pedir("DELETE", f"/rest/v1/{tabela}?id=eq.{urllib.parse.quote(str(id_))}")

    # ---------- arquivos (bucket privado) ----------
    def enviar_arquivo(self, caminho_local, destino, tipo="application/pdf"):
        with open(caminho_local, "rb") as f:
            corpo = f.read()
        self._pedir("POST", f"/storage/v1/object/{self.bucket}/{urllib.parse.quote(destino)}", corpo,
                    {"x-upsert": "true"}, tipo=tipo)
        return destino

    def url_assinada(self, destino, segundos=600):
        r = self._pedir("POST", f"/storage/v1/object/sign/{self.bucket}/{urllib.parse.quote(destino)}", {"expiresIn": segundos})
        return self.url + "/storage/v1" + r["signedURL"] if r and r.get("signedURL") else None

    def baixar(self, destino):
        return self._pedir("GET", f"/storage/v1/object/{self.bucket}/{urllib.parse.quote(destino)}", bruto=True)

    def saude(self):
        self.select("configuracoes", {"limit": "1"})
        return True


# ---------------------------------------------------------------------------
# Banco de demonstração (--demo): dados fictícios na memória, mesmo contrato do Supabase
# ---------------------------------------------------------------------------
_DATA_REL = re.compile(r"^@(hoje|semana)([+-]\d+)?(?:T(\d\d:\d\d))?$")


def _resolver_datas(v, hoje):
    """'@hoje-7' vira a data de 7 dias atrás; '@semana-7', a segunda-feira da semana passada; '@hoje+1T09:00' vira data e hora (fuso local). Assim a demo nunca envelhece."""
    if isinstance(v, dict):
        return {k: _resolver_datas(x, hoje) for k, x in v.items()}
    if isinstance(v, list):
        return [_resolver_datas(x, hoje) for x in v]
    if isinstance(v, str):
        m = _DATA_REL.match(v)
        if m:
            base = hoje if m.group(1) == "hoje" else hoje - datetime.timedelta(days=hoje.weekday())
            d = base + datetime.timedelta(days=int(m.group(2) or 0))
            if m.group(3):
                hh, mm = map(int, m.group(3).split(":"))
                return datetime.datetime(d.year, d.month, d.day, hh, mm).astimezone().isoformat(timespec="minutes")
            return d.isoformat()
    return v


class Demo:
    """Mesmos métodos do Supabase, sobre o JSON fictício. O que o painel grava fica só na memória (some ao fechar)."""
    modo = "demo"
    bucket = "entregas"
    rt_pin_hash = ""

    def __init__(self, arquivo):
        with open(arquivo, encoding="utf-8") as f:
            bruto = json.load(f)
        self.tabelas = _resolver_datas(bruto["tabelas"], datetime.date.today())
        self.url = "demo (dados fictícios)"

    def __repr__(self):
        return "<Demo>"

    @staticmethod
    def _cmp(valor, op, alvo):
        if op == "is":
            return {"null": valor is None, "true": valor is True, "false": valor is False}.get(alvo, False)
        if op == "in":
            return str(valor) in [x.strip().strip('"') for x in alvo.strip("()").split(",")]
        if valor is None:
            return False
        if op in ("ilike", "like"):
            padrao = "^" + ".*".join(re.escape(p) for p in alvo.split("*")) + "$"
            return re.match(padrao, str(valor), re.I if op == "ilike" else 0) is not None
        if isinstance(valor, bool):
            valor = "true" if valor else "false"
        a, b = str(valor), alvo
        try:
            a, b = float(valor), float(alvo)
        except (TypeError, ValueError):
            pass
        return {"eq": a == b, "neq": a != b, "gte": a >= b, "lte": a <= b, "gt": a > b, "lt": a < b}.get(op, True)

    def select(self, tabela, params=None):
        linhas = [copy.deepcopy(l) for l in self.tabelas.get(tabela, [])]
        params = dict(params or {})
        ordem, limite = params.pop("order", None), params.pop("limit", None)
        params.pop("select", None)
        for campo, expr in params.items():
            neg = expr.startswith("not.")
            op, _, alvo = (expr[4:] if neg else expr).partition(".")
            linhas = [l for l in linhas if self._cmp(l.get(campo), op, alvo) != neg]
        if ordem:
            for parte in reversed(ordem.split(",")):
                campo, _, dire = parte.partition(".")
                linhas.sort(key=lambda l: (l.get(campo) is None, str(l.get(campo) if not isinstance(l.get(campo), (int, float)) else f"{l.get(campo):020.4f}")),
                            reverse=dire.startswith("desc"))
        return linhas[: int(limite)] if limite else linhas

    def um(self, tabela, id_):
        r = self.select(tabela, {"id": f"eq.{id_}"})
        return r[0] if r else None

    def inserir(self, tabela, linhas):
        lista = linhas if isinstance(linhas, list) else [linhas]
        agora = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
        saida = []
        for l in lista:
            novo = {"id": str(uuid.uuid4()), "criado_em": agora, "atualizado_em": agora, **l}
            self.tabelas.setdefault(tabela, []).append(novo)
            saida.append(copy.deepcopy(novo))
        return saida if isinstance(linhas, list) else saida[0]

    def atualizar(self, tabela, id_, valores):
        for l in self.tabelas.get(tabela, []):
            if str(l.get("id")) == str(id_):
                l.update(valores)
                l["atualizado_em"] = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
                return copy.deepcopy(l)
        raise ErroSupabase(f"nada atualizado em {tabela} (id não achado)")

    def apagar(self, tabela, id_):
        self.tabelas[tabela] = [l for l in self.tabelas.get(tabela, []) if str(l.get("id")) != str(id_)]

    def enviar_arquivo(self, caminho_local, destino, tipo="application/pdf"):
        return destino

    def url_assinada(self, destino, segundos=600):
        return None

    def baixar(self, destino):
        raise ErroSupabase("na demonstração não há PDF guardado no Supabase")

    def saude(self):
        return True


def conectar(demo_arquivo=None):
    return Demo(demo_arquivo) if demo_arquivo else Supabase()
