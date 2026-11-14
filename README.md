# Calculadora de rescisão trabalhista

Aplicativo Streamlit em português para estimar as principais verbas de uma rescisão CLT urbana padrão. O resultado é bruto e informativo; não substitui o TRCT, o eSocial ou uma análise profissional.

## Como executar

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

## Escopo

Inclui saldo salarial, aviso indenizado nas modalidades aplicáveis, 13º proporcional, férias vencidas e proporcionais com 1/3, indenização estimada do FGTS e descontos informados manualmente. Não calcula INSS/IRRF nem valores devidos por rescisão antecipada de contrato a prazo. As verbas variáveis são representadas por uma média mensal fornecida pelo usuário.

Fontes legais usadas como orientação: [CLT compilada (Planalto)](https://www.planalto.gov.br/ccivil_03/decreto-lei/del5452compilado.htm), [Lei do FGTS (Planalto)](https://www.planalto.gov.br/ccivil_03/leis/l8036consol.htm) e [Perguntas frequentes do MTE](https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/acoes-e-programas/programas-projetos-acoes-obras-e-atividades/proteja/duvidas-frequentes).
