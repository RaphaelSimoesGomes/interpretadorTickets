<img width=100% src="https://capsule-render.vercel.app/api?type=waving&color=00494c&height=120&section=header"/>

# Interpretador de Tickets de TI com IA
Este projeto utiliza a API do Google Gemini para analisar e interpretar tickets de suporte de TI. O script extrai informações estruturadas de um título e uma descrição, valida a solicitação com base em uma base de conhecimento de sistemas pré-definida e fornece um resumo claro da ação necessária.

# Funcionalidades Principais
- Análise Inteligente: Utiliza um modelo de linguagem de IA (Google Gemini) para compreender o contexto de um ticket de suporte.

- Base de Conhecimento: Valida se a solicitação do usuário é consistente com as funções de um sistema pré-definido por si.

- Verificação de Consistência: Se um sistema mencionado no ticket não for conhecido, a IA realiza uma verificação básica para ver se o título e a descrição são coerentes entre si.

- Extração de Dados: Identifica e extrai automaticamente informações chave como tipo de solicitação, usuários envolvidos e sistema principal.

- Fluxo Interativo: Permite que o utilizador insira títulos e descrições diretamente no terminal para análise em tempo real.

# Como Usar
Pré-requisitos
- Python 3.6 ou superior

- A biblioteca requests

Instalação
Clone o repositório ou guarde o ficheiro interpretador_ticket.py no seu computador.

Instale as dependências necessárias:
```bash
pip install requests
```
# Configuração

Obtenha uma Chave de API do Google Gemini:

- Vá ao [Google AI Studio](https://aistudio.google.com/app/apikey).

- Crie uma nova chave de API gratuitamente.

Configure a Chave de API no Script:

- Abra o ficheiro ```interpretador_ticket.py```.

- Encontre a linha: ```api_key = "SUA_CHAVE_DE_API_AQUI"```

- Substitua ```"SUA_CHAVE_DE_API_AQUI"``` pela chave que acabou de gerar.

Personalize a Base de Conhecimento:

- No mesmo ficheiro, localize o dicionário ```definicoes_sistemas```.

- Adicione, edite ou remova os sistemas e as suas respetivas descrições para corresponder ao seu ambiente de trabalho.
```bash
definicoes_sistemas = {
    "SAP": "Sistema principal para gestão financeira, faturamento, notas fiscais e controle de estoque.",
    "VAPT Jornada": "Sistema focado na jornada do colaborador, banco de horas, apontamento",
    "Salesforce": "Plataforma de CRM para gestão de clientes e vendas."
}
```
# Execução
Execute o script a partir do seu terminal:
```bash
python interpretador_ticket.py
```
Siga as instruções no terminal:

- Insira o título da requisição e pressione ```Enter```.

- Cole a descrição do ticket. Pode usar múltiplas linhas.

- Pressione ```Enter``` numa linha vazia para submeter o texto para análise.

Para sair do programa, não insira um título e pressione ```Enter```.

# Exemplo de Uso
### Cenário 1: Sistema Conhecido e Condizente
Input do Utilizador:

- Título: ```Reset de senha no SAP para o utilizador João Silva```

- Descrição: ```O colaborador João Silva da contabilidade esqueceu a sua senha do SAP e precisa de um reset para aceder aos relatórios financeiros.```

Output Esperado da IA:
```bash
--- RESULTADO ---
--- ANÁLISE DO TICKET ---
Análise de Consistência: Condizente
Justificativa e Correção: A solicitação está no sistema correto, pois o SAP é utilizado para gestão financeira.
Tipo de Solicitação: Reset de Senha
Usuários Envolvidos: João Silva
Sistema/Módulo Principal: SAP
Resumo da Ação Sugerida: Realizar o reset da senha do utilizador João Silva no sistema SAP.
----------------------------------------------------
```
### Cenário 2: Sistema Conhecido e Incondizente
Input do Utilizador:

- Título: ```Criar novo apontamento de horas no SAP```

- Descrição: ```Preciso registar as minhas horas extras da semana passada.```

Output Esperado da IA:
```bash
--- RESULTADO ---
--- ANÁLISE DO TICKET ---
Análise de Consistência: Incondizente
Justificativa e Correção: A solicitação de apontamento de horas não corresponde à função do SAP (gestão financeira). O sistema correto para esta tarefa é o VAPT Jornada.
Tipo de Solicitação: Apontamento de Horas
Usuários Envolvidos: Não informado
Sistema/Módulo Principal: SAP
Resumo da Ação Sugerida: Orientar o utilizador a fazer o registo de horas no sistema VAPT Jornada.
----------------------------------------------------
```
### Cenário 3: Sistema Desconhecido
Input do Utilizador:

- Título: ```Problema ao aceder ao Portal de Fornecedores```

- Descrição: ```Não consigo fazer login na plataforma de fornecedores para submeter uma nova fatura.```

Output Esperado do Script:
```bash
--- RESULTADO ---
AVISO: Não há uma pré-definição para o sistema mencionado no título ('Problema ao aceder ao Portal de Fornecedores').
Realizando uma verificação de consistência básica...
Sim, o título é condizente com a descrição, pois ambos se referem a um problema de acesso a uma plataforma de fornecedores.
----------------------------------------------------
```
<img width=100% src="https://capsule-render.vercel.app/api?type=waving&color=00494c&height=120&section=footer"/>
