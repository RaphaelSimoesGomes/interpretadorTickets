# -*- coding: utf-8 -*-
import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()
API = os.getenv("API")

def find_system_in_title(title, systems):
    """Verifica se algum nome de sistema da base de conhecimento está no título."""
    for system_name in systems.keys():
        if system_name.lower() in title.lower():
            return system_name
    return None


def check_generic_consistency(api_key, ticket_title, ticket_description):
    """Faz uma verificação genérica de consistência quando o sistema não é conhecido."""
    if not api_key:
        return "Erro: A chave da API não foi fornecida."

    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    prompt = f"""
    Analise o título e a descrição de um ticket de suporte. A tarefa é determinar se o título e a descrição são consistentes e parecem se referir ao mesmo problema ou solicitação.

    Título: "{ticket_title}"
    Descrição: "{ticket_description}"

    Responda em uma linha: O título é condizente com a descrição? (Responda com 'Sim' ou 'Não' e uma breve justificativa).
    """
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        result = response.json()
        if 'candidates' in result and result['candidates']:
            return result['candidates'][0]['content']['parts'][0]['text'].strip()
        return "Não foi possível realizar a verificação de consistência."
    except Exception:
        return "Erro ao contatar a API para verificação de consistência."


def interpret_ticket_with_gemini(api_key, ticket_title, ticket_description, system_definitions):
    """Interpreta um ticket usando a base de conhecimento de sistemas."""
    if not api_key:
        return "Erro: A chave da API não foi fornecida."

    definitions_text = "\n".join([f"- {name}: {desc}" for name, desc in system_definitions.items()])
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    prompt = f"""
    Você é um assistente de TI especialista. Sua tarefa é analisar um ticket de suporte com base em uma lista pré-definida de sistemas e suas funções.

    --- BASE DE CONHECIMENTO DE SISTEMAS ---
    {definitions_text}
    --- FIM DA BASE DE CONHECIMENTO ---

    Agora, analise o seguinte ticket:

    Título da Requisição: "{ticket_title}"
    Descrição do Ticket:
    \"\"\"
    {ticket_description}
    \"\"\"

    Com base na sua base de conhecimento, extraia as seguintes informações:

    --- ANÁLISE DO TICKET ---
    Análise de Consistência: (Responda "Condizente" se a descrição da tarefa corresponde à função do sistema mencionado. Responda "Incondizente" se não corresponder.)
    Justificativa e Correção: (Se for "Incondizente", explique por que e sugira qual sistema da base de conhecimento seria o correto. Se for "Condizente", apenas confirme que a solicitação está no sistema correto.)
    Tipo de Solicitação: (Ex: Alteração de Permissão, Criação de Usuário, Relatório)
    Usuários Envolvidos: (Liste os nomes, separados por vírgula. Se não houver, escreva "Não informado".)
    Sistema/Módulo Principal: (Identifique o sistema da sua base de conhecimento que foi mencionado no ticket.)
    Resumo da Ação Sugerida: (Descreva em uma frase o que precisa ser feito.)
    """

    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
    }
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()

        result = response.json()

        if 'candidates' in result and result['candidates']:
            generated_text = result['candidates'][0]['content']['parts'][0]['text']
            return generated_text.strip()
        else:
            return f"Erro: A resposta da API não continha o resultado esperado.\nResposta completa: {json.dumps(result, indent=2)}"

    except requests.exceptions.RequestException as e:
        return f"Erro de conexão com a API: {e}"
    except Exception as e:
        return f"Ocorreu um erro inesperado: {e}"


if __name__ == "__main__":
    definicoes_sistemas = {
        "SAP": "Sistema principal para gestão financeira, faturamento, notas fiscais e controle de estoque.",
        "VAPT Jornada": "Sistema focado na jornada do colaborador, banco de horas, apontamento"
    }

    print("--- Interpretador de Tickets de TI com IA (Python) ---")
    print("O sistema usará a base de conhecimento definida no código.")

    api_key = API

    while True:
        print("\n> Insira o Título da Requisição (ou deixe em branco e pressione Enter para sair):")
        title_input = input()

        if not title_input.strip():
            break

        print("\n> Cole a Descrição do Ticket (pressione Enter em uma linha vazia para enviar):")

        lines = []
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)

        description_input = "\n".join(lines)

        if not description_input.strip():
            print("Descrição não fornecida. Tente novamente.")
            continue

        print("\nAnalisando... Por favor, aguarde.")

        mentioned_system = find_system_in_title(title_input, definicoes_sistemas)

        if mentioned_system:
            analysis_result = interpret_ticket_with_gemini(api_key, title_input, description_input, definicoes_sistemas)
        else:
            error_message = f"AVISO: Não há uma pré-definição para o sistema mencionado no título ('{title_input}')."
            print(error_message)
            print("Realizando uma verificação de consistência básica...")
            analysis_result = check_generic_consistency(api_key, title_input, description_input)

        print("--- RESULTADO ---")
        print(analysis_result)
        print("----------------------------------------------------")

    print("\nPrograma encerrado.")