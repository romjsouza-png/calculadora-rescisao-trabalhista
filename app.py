import calendar
from datetime import date

import streamlit as st


st.set_page_config(page_title="Calculadora de Rescisão", page_icon="🧾", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #f5f7fa; color: #182638; }
.block-container { max-width: 1120px; padding-top: 2.2rem; padding-bottom: 4rem; }
h1,h2,h3 { font-family: 'Manrope', sans-serif !important; letter-spacing: -0.035em; }
.hero { background: linear-gradient(120deg,#102c3b,#145c58); padding: 2.2rem 2.5rem; border-radius: 20px; color:white; margin-bottom:1.4rem; }
.hero h1 { color:white; font-size:2.25rem; margin:0.3rem 0; }
.hero p { color:#d4e6e4; margin:0; }
.eyebrow { color:#8fe0c1; font-size:.76rem; font-weight:700; letter-spacing:.13em; text-transform:uppercase; }
.card { background:white; padding:1.3rem 1.5rem; border:1px solid #e3e9ee; border-radius:16px; }
.metric { background:white; border:1px solid #e3e9ee; border-radius:16px; padding:1.1rem 1.3rem; min-height:110px; }
.metric-label { color:#667788; font-size:.82rem; }
.metric-value { color:#123e3b; font-family:'Manrope'; font-size:1.65rem; font-weight:800; margin-top:.35rem; }
.muted { color:#667788; font-size:.9rem; }
div[data-testid="stDataFrame"] { border-radius:12px; overflow:hidden; }
</style>
<section class="hero"><div class="eyebrow">RH · Simulação trabalhista</div><h1>Calculadora de rescisão</h1><p>Uma estimativa transparente das principais verbas do encerramento do contrato CLT.</p></section>
""", unsafe_allow_html=True)

st.info("Simulação bruta para contratos CLT urbanos padrão. Convenção coletiva, médias variáveis, afastamentos, estabilidade, descontos legais e particularidades do contrato podem alterar o resultado. Não substitui TRCT, eSocial ou orientação profissional.", icon="ℹ️")

def money(x):
    return f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

with st.container(border=True):
    st.subheader("Dados do contrato")
    a, b, c = st.columns(3)
    with a:
        salario = st.number_input("Salário mensal bruto (R$)", min_value=0.0, value=3500.0, step=100.0)
        admissao = st.date_input("Data de admissão", value=date(2022, 5, 1), max_value=date.today())
    with b:
        desligamento = st.date_input("Último dia do contrato", value=date.today())
        modalidade = st.selectbox("Motivo do desligamento", ["Dispensa sem justa causa", "Pedido de demissão", "Acordo entre as partes (art. 484-A)", "Justa causa", "Término normal de contrato a prazo"])
    with c:
        aviso = st.selectbox("Aviso prévio", ["Indenizado pelo empregador", "Trabalhado", "Descontado / não cumprido pelo empregado", "Dispensado / não aplicável"])
        saldo_fgts = st.number_input("Saldo estimado do FGTS (R$)", min_value=0.0, value=0.0, step=500.0, help="Use o saldo para fins rescisórios do extrato da Caixa, se disponível.")
    d, e, f = st.columns(3)
    with d:
        dias_mes = st.number_input("Dias trabalhados no mês da saída", min_value=0, max_value=31, value=min(desligamento.day, 31))
    with e:
        ferias_vencidas = st.number_input("Períodos completos de férias ainda não gozados", min_value=0, max_value=10, value=0)
    with f:
        descontos = st.number_input("Outros descontos informados (R$)", min_value=0.0, value=0.0, step=50.0, help="Informe apenas descontos conhecidos. INSS e IRRF não são calculados nesta versão.")

with st.container(border=True):
    st.subheader("Parcelas variáveis e adiantamentos")
    x, y = st.columns(2)
    with x:
        media = st.number_input("Média mensal de adicionais/comissões (R$)", min_value=0.0, value=0.0, step=100.0, help="Inclua médias salariais habituais para compor a remuneração de referência.")
    with y:
        adiantamento_13 = st.number_input("Adiantamento de 13º já recebido neste ano (R$)", min_value=0.0, value=0.0, step=100.0)

col_action, col_hint = st.columns([1, 2])
with col_action:
    gerar = st.button("Gerar verbas rescisórias", type="primary", use_container_width=True)
if gerar:
    st.session_state["resultado_rescisao_visivel"] = True
with col_hint:
    st.caption("Preencha os dados acima e clique no botão para gerar o demonstrativo.")

if not st.session_state.get("resultado_rescisao_visivel", False):
    st.markdown("""
    <div class="card"><strong>Pronto para simular?</strong><br>
    <span class="muted">Informe as datas, o motivo da saída e os valores conhecidos. O demonstrativo aparecerá aqui após o cálculo.</span></div>
    """, unsafe_allow_html=True)
    st.stop()

if desligamento < admissao:
    st.error("A data de desligamento não pode ser anterior à admissão.")
    st.stop()

remuneracao = salario + media
anos = max(0, desligamento.year - admissao.year - ((desligamento.month, desligamento.day) < (admissao.month, admissao.day)))
aplica_aviso = modalidade in ("Dispensa sem justa causa", "Acordo entre as partes (art. 484-A)")
dias_aviso = min(90, 30 + 3 * anos) if aplica_aviso else 30
aviso_pago = 0.0
aviso_desconto = 0.0
if modalidade == "Dispensa sem justa causa" and aviso == "Indenizado pelo empregador":
    aviso_pago = remuneracao * dias_aviso / 30
elif modalidade == "Acordo entre as partes (art. 484-A)" and aviso == "Indenizado pelo empregador":
    aviso_pago = remuneracao * dias_aviso / 60
elif modalidade == "Pedido de demissão" and aviso == "Descontado / não cumprido pelo empregado":
    aviso_desconto = remuneracao

# A projeção do aviso indenizado pode alterar as frações de 13º e férias.
proj = dias_aviso if aviso_pago else 0
try:
    data_proj = date.fromordinal(desligamento.toordinal() + proj)
except Exception:
    data_proj = desligamento

saldo_salario = remuneracao * min(dias_mes, 30) / 30
def avos_13(inicio, fim, ano):
    total = 0
    for mes in range(1, 13):
        primeiro = date(ano, mes, 1)
        ultimo = date(ano, mes, calendar.monthrange(ano, mes)[1])
        dias_no_vinculo = (min(ultimo, fim) - max(primeiro, inicio)).days + 1
        if dias_no_vinculo >= 15:
            total += 1
    return total

meses_13 = avos_13(admissao, data_proj, desligamento.year)
meses_13_proj = avos_13(admissao, data_proj, data_proj.year) if data_proj.year > desligamento.year else 0
decimo = remuneracao * meses_13 / 12
decimo_proj = remuneracao * meses_13_proj / 12
if modalidade == "Justa causa":
    decimo = 0.0
    decimo_proj = 0.0

# Conta meses do período aquisitivo desde a admissão ou a última data de aniversário contratual.
inicio_periodo = date(data_proj.year, admissao.month, min(admissao.day, calendar.monthrange(data_proj.year, admissao.month)[1]))
if data_proj < inicio_periodo:
    inicio_periodo = date(data_proj.year - 1, admissao.month, min(admissao.day, calendar.monthrange(data_proj.year - 1, admissao.month)[1]))
meses_ferias = (data_proj.year - inicio_periodo.year) * 12 + data_proj.month - inicio_periodo.month
if data_proj.day >= inicio_periodo.day:
    meses_ferias += 1
meses_ferias = max(0, min(12, meses_ferias))
ferias_prop = 0.0 if modalidade == "Justa causa" else remuneracao * meses_ferias / 12
terco_prop = ferias_prop / 3
ferias_cheias = remuneracao * ferias_vencidas
terco_cheias = ferias_cheias / 3

if modalidade == "Acordo entre as partes (art. 484-A)":
    multa_fgts = saldo_fgts * 0.20
elif modalidade == "Dispensa sem justa causa":
    multa_fgts = saldo_fgts * 0.40
else:
    multa_fgts = 0.0

itens = [
    ("Saldo de salário", saldo_salario),
    (f"Aviso prévio indenizado ({dias_aviso} dias, quando aplicável)", aviso_pago),
    (f"13º proporcional ({meses_13}/12 avos)", decimo),
    (f"13º proporcional sobre projeção em {data_proj.year} ({meses_13_proj}/12 avos)", decimo_proj),
    ("Desconto de adiantamento de 13º", -adiantamento_13),
    (f"Férias proporcionais ({meses_ferias}/12 avos)", ferias_prop),
    ("1/3 sobre férias proporcionais", terco_prop),
    ("Férias vencidas informadas", ferias_cheias),
    ("1/3 sobre férias vencidas", terco_cheias),
    ("Multa estimada do FGTS", multa_fgts),
    ("Desconto de aviso não cumprido", -aviso_desconto),
    ("Outros descontos informados", -descontos),
]
total = sum(v for _, v in itens)

st.markdown("### Resultado estimado")
m1, m2, m3 = st.columns(3)
with m1: st.markdown(f'<div class="metric"><div class="metric-label">Total bruto de verbas</div><div class="metric-value">{money(sum(max(0,v) for _,v in itens))}</div></div>', unsafe_allow_html=True)
with m2: st.markdown(f'<div class="metric"><div class="metric-label">Descontos considerados</div><div class="metric-value">{money(aviso_desconto + descontos + adiantamento_13)}</div></div>', unsafe_allow_html=True)
with m3: st.markdown(f'<div class="metric"><div class="metric-label">Estimativa após descontos informados</div><div class="metric-value">{money(total)}</div></div>', unsafe_allow_html=True)

st.markdown("#### Memória de cálculo")
st.dataframe({"Verba": [n for n, _ in itens], "Valor estimado": [money(v) for _, v in itens]}, hide_index=True, use_container_width=True)

with st.expander("Como interpretar este resultado"):
    st.markdown("""
- O saldo do FGTS foi usado somente para estimar a indenização de 40% (dispensa sem justa causa) ou 20% (acordo). O saldo sacável não está somado às verbas pagas diretamente na rescisão.
- No acordo do art. 484-A, o aviso indenizado e a indenização do FGTS são calculados pela metade; o saque do FGTS pode ser limitado a 80%, conforme as regras aplicáveis.
- Férias vencidas são informadas manualmente. Férias proporcionais e 13º usam contagem simplificada por avos e podem variar com projeção de aviso, afastamentos e datas específicas.
- Não calculamos INSS, IRRF, faltas, banco de horas, adicionais variáveis detalhados, estabilidade, indenização de contrato a prazo interrompido, multa do art. 477, seguro-desemprego nem saque do FGTS.
- Em pedido de demissão com aviso trabalhado, os dias efetivamente trabalhados entram no saldo do mês. Término antecipado de contrato a prazo requer cálculo próprio.
""")
st.caption("Referências: [CLT, arts. 477, 487 e 484-A](https://www.planalto.gov.br/ccivil_03/decreto-lei/del5452compilado.htm) · [Perguntas frequentes do Ministério do Trabalho e Emprego](https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/acoes-e-programas/programas-projetos-acoes-obras-e-atividades/proteja/duvidas-frequentes)")
