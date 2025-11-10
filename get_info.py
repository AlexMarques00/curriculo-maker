# To do:
# refazer imprimir para ficar em ordem
# implementar traduçao do codigo para html e pdf
# fazer interface grafica - app de desktop e de celular
# pdf do html com separaçao de paginas 

import json
import os
from pydantic import BaseModel, EmailStr, HttpUrl, ValidationError
from typing import List, Dict, Any, Optional
from dataclasses import field

ARQUIVO_JSON = "info.json"

class User(BaseModel):
    nome: str
    email: Optional[EmailStr] = ""
    linkedin: Optional[HttpUrl] = ""
    github: Optional[HttpUrl] = ""
    celular: str = ""
    estado: str = ""
    cidade: str = ""
    objetivo: str = ""
    formacao: List[Dict[str, Any]] = field(default_factory=list)
    competencias: Dict[str, Any] = field(default_factory=dict)
    experiencias: List[Dict[str, Any]] = field(default_factory=list)
    projetos: List[Dict[str, Any]] = field(default_factory=list)
    certificacoes: List[Dict[str, Any]] = field(default_factory=list)
    idiomas: Dict[str, Any] = field(default_factory=dict)
    disponibilidade: str = ""
    informacoes_adicionais: str = ""

# --- Setters da classe User ---

def add_formacao(user):
    """Adiciona uma formação com validação de 1/2."""
    tipo_formacao = input("Digite o nome da sua formacao (Exemplo: 'Bacharelado em Engenharia de Computação'): ")
    local_formacao = input("Digite o nome da instituição de sua formação (Exemplo: 'PUC Minas'): ")
    
    while True:
        concluido = input("Digite 1 se já foi concluída e 2 para previsão de conclusão: ")
        if concluido == '1':
            concluir = "Concluído em "
            break
        elif concluido == '2':
            concluir = "Previsão de conclusão: "
            break
        else:
            print("Erro: Número inválido. Por favor, digite '1' ou '2'.")
            
    data = input("Insira a data de formacao no formato 'mes/ano': ")
    conclusao = concluir + data 
    user.formacao.append({"tipo": tipo_formacao, "onde": local_formacao, "conclusao": conclusao})
    return True

def lista_de_dicionarios(tipo_lista):
    """Função genérica para adicionar itens (título/descrição) a uma lista (experiencias, projetos, certificacoes)."""
    lista = []
    
    while True:
        titulo = input(f"Digite o título do {len(lista)+1}° item ({tipo_lista}): ")
        descricao = input(f"Digite a descrição de {titulo}: ")
        lista.append({titulo: descricao})
        
        while True:
            check = input(f"Você quer adicionar mais itens na lista de {tipo_lista} (S/N)? ").lower()
            if check in ['s', 'n']:
                break 
            print("Erro: Resposta inválida. Por favor, digite 'S' ou 'N'.")
            
        if check == 'n':
            break 
            
    return lista

def experiencias_lista(user):
    return lista_de_dicionarios("experiencias profissionais")

def certificacoes_lista(user):
    return lista_de_dicionarios("certificados")

def projetos_lista(user):
    return lista_de_dicionarios("projetos")

def idiomas_lista_dict(user):
    """Adiciona idiomas no formato {lingua: nivel}."""
    idiomas_dict = {}
    
    while True:
        lingua = input("Digite o nome do idioma: ")
        nivel = input(f"Digite o nível de fluência para {lingua} (Ex: 'Avançado', 'Fluente', 'B2'): ")
        idiomas_dict[lingua] = nivel
        
        while True:
            check = input("Você quer adicionar mais idiomas (S/N)? ").lower()
            if check in ['s', 'n']:
                break 
            print("Erro: Resposta inválida. Por favor, digite 'S' ou 'N'.")
            
        if check == 'n':
            break 
            
    return idiomas_dict

def competencias_lista(tipo):
    """Cria a lista de sub-competências."""
    lista = []
    while True:
        lista.append(input(f"Digite o {len(lista)+1}° item da lista de {tipo}: "))
        
        while True: 
            check = input("Você quer adicionar mais itens na lista (S/N)? ").lower()
            if check in ['s', 'n']:
                break 
            print("Erro: Resposta inválida. Por favor, digite 'S' ou 'N'.")
            
        if check == 'n':
            break 
    return lista

def add_competencias(user):
    """Adiciona uma categoria de competências com validação de 1/2."""
    tipo_competencia = input("Digite o nome da categoria de competencias que voce quer adicionar (Exemplo: 'Linguagens de Programação', 'Pacote Office', 'Ferramentas'): ")
    competencias = None
    
    while True:
        lista_ou_string = input("Digite 1 se quiser fazer uma lista ou 2 se quiser escrever uma linha descritiva: ")
        if lista_ou_string == '1':
            competencias = competencias_lista(tipo_competencia)
            break
        elif lista_ou_string == '2':
            competencias = input("Digite a linha descritiva da competencia: ")
            break
        else:
            print("Erro: Número inválido. Por favor, digite '1' ou '2'.")
            
    user.competencias[tipo_competencia] = competencias
    return True

# --- Constructor e Mostrar ---

def adicionar_user(dados): # retorna user
    nome = input("Digite seu nome: ")
    if nome in dados:
        print(f"Erro: Usuário {nome} já existe. Não foi possível adicionar.")
        return None
    user_data = {"nome": nome}
    def obter_input_validado(campo, prompt, is_optional=True):
        while True:
            valor = input(prompt)
            if valor.lower() == 'none' and is_optional:
                return ""
            temp_data = user_data.copy()
            temp_data[campo] = valor
            try:
                User(**temp_data)
                return valor
            except ValidationError as e:
                print(f"Erro de validacao para {campo.capitalize()}: {e.errors()[0]['msg']}")
                if input("Tentar novamente (S/N)? ").lower() != "s":
                    return ""
    user_data["email"] = obter_input_validado("email", "Digite seu email: ")
    user_data["linkedin"] = obter_input_validado("linkedin", "Digite o link do seu linkedin (ou 'none' se não tiver): ")
    user_data["github"] = obter_input_validado("github", "Digite o link do seu github se houver (ou 'none' se não tiver): ")
    user_data["celular"] = input("Digite seu numero de celular: ")
    user_data["estado"] = input("Digite a sigla do seu estado: ")
    user_data["cidade"] = input("Digite o nome da sua cidade: ")
    user_data["objetivo"] = input("Digite uma frase como seu objetivo profissional: ")
    try:
        novo_user = User(**user_data)
    except ValidationError as e:
        print(f"Erro inesperado na criação de usuário: {e}")
        return None
    
    dados[nome] = novo_user
    
    # --- Adicionar Formações ---
    while True:
        if add_formacao(novo_user):
            while True: 
                check = input("Quer adicionar mais formações (S/N)? ").lower()
                if check in ['s', 'n']:
                    break
                print("Erro: Resposta inválida. Por favor, digite 'S' ou 'N'.")
            if check == 'n':
                break
            
    # --- Adicionar Competências ---
    while True:
        if add_competencias(novo_user):
            while True: 
                check = input("Quer adicionar mais competências (S/N)? ").lower()
                if check in ['s', 'n']:
                    break
                print("Erro: Resposta inválida. Por favor, digite 'S' ou 'N'.")
            if check == 'n':
                break
                
    novo_user.experiencias = experiencias_lista(novo_user)
    novo_user.projetos = projetos_lista(novo_user)
    novo_user.certificacoes = certificacoes_lista(novo_user)
    novo_user.idiomas = idiomas_lista_dict(novo_user) 
    
    disponibilidade = input("Digite sua(s) disponibilidade(s) separada(s) por VÍRGULAS (Ex: 'Integral, Finais de Semana'):")
    novo_user.disponibilidade = disponibilidade.strip()

    informacoes_adicionais = input("Digite um paragrafo curto sobre você se quiser (ou 'none' se não): ")
    if informacoes_adicionais != "none":
        novo_user.informacoes_adicionais = informacoes_adicionais
    print(f"Usuário '{nome}' adicionado!\n")
    return novo_user

# --- Funções de Edição ---

def editar_lista_de_dicionarios(user, nome_campo, nome_exibicao):
    lista = getattr(user, nome_campo)
    while True:
        print(f"\n--- Editando lista de {nome_exibicao} ---")
        if not lista:
            print(f"Nenhum item em {nome_exibicao} cadastrado.")
        else:
            print(f"Itens Atuais:")
            for i, item_dict in enumerate(lista):
                titulo = list(item_dict.keys())[0]
                descricao = item_dict[titulo]
                print(f"{i+1}. {titulo}: {descricao[:40]}...")
        print("\nOpções")
        print("A. Adicionar Novo Item")
        if lista:
            print("E. Editar Item Existente")
            print("R. Remover Item Existente")
        print("V. Voltar ao menu de Edição")
        escolha = input("Escolha uma opção (A/E/R/V): ").upper()
        if escolha == "V":
            break
        elif escolha == "A":
            titulo = input("Digite o TÍTULO do novo item: ")
            descricao = input(f"Digite a DESCRIÇÃO para {titulo}: ")
            lista.append({titulo: descricao})
            print(f"Item '{titulo}' adicionado.")
        elif escolha == "E" and lista:
            try:
                indice = int(input("Digite o número do item para editar: ")) - 1
                if 0 <= indice < len(lista):
                    item_dict = lista[indice]
                    titulo_antigo = list(item_dict.keys())[0]
                    novo_titulo = input(f"Novo título (Atual: {titulo_antigo}): ")
                    nova_descricao = input(f"Nova descrição (Atual: {item_dict[titulo_antigo][:40]}): ")
                    lista.pop(indice)
                    lista.insert(indice, {novo_titulo: nova_descricao})
                    print(f"Item {titulo_antigo} atualizado para {novo_titulo}")
                else:
                    print("Número inválido")
            except ValueError:
                print("Entrada inválida. Digite um número.")
        elif escolha == "R" and lista:
            try:
                indice = int(input("Digite o NÚMERO do item para remover: ")) - 1
                if 0 <= indice < len(lista):
                    titulo_removido = list(lista[indice].keys())[0]
                    lista.pop(indice)
                    print(f"Item '{titulo_removido}' removido com sucesso.")
                else:
                    print("Número inválido.")
            except ValueError:
                print("Entrada inválida. Digite um número.")
        else:
            print("Opção inválida")

# BUG: só faz adição, falta edição e remocao de formacao e competencias

def editar_formacao(user):
    lista = user.formacao
    while True:
        print("\n--- Editando Formação ---")
        if not lista:
            print("Nenhuma formação cadastrada.")
        else:
            print("Formações Atuais:")
            for i, f in enumerate(lista):
                print(f"{i+1}. {f['tipo']} em {f['onde']} ({f['conclusao']})")
        print("\nOpções:")
        print("A. Adicionar Nova Formação")
        if lista:
            print("E. Editar Formação Existente")
            print("R. Remover Formação Existente")
        print("V. Voltar ao menu de Edição")
        escolha = input("Escolha uma opção (A/E/R/V): ").upper()
        if escolha == "V":
            break
        elif escolha == "A":
            add_formacao(user)
        elif escolha == "E" and lista:
            try:
                indice = int(input("Digite o NÚMERO da formação para EDITAR: ")) - 1
                if 0 <= indice < len(lista):
                    formacao_selecionada = lista[indice]
                    print(f"\nEditando {formacao_selecionada['tipo']} (Para deixar o campo sem alterações, apenas aperte ENTER sem escrever nada)")
                    formacao_selecionada['tipo'] = input(f"Novo nome da formação (Atual: {formacao_selecionada['tipo']})") or formacao_selecionada['tipo']
                    formacao_selecionada['onde'] = input(f"Nova instituição (Atual: {formacao_selecionada['onde']})") or formacao_selecionada["onde"]
                    print(f"Status Atual: {formacao_selecionada["conclusao"]}")
                    if input("Deseja alterar o status e data (S/N)? ").lower() == "s":
                        concluir = ""
                        while True:
                            concluido = input("Novo status: Digite 1 (Concluida) ou 2 (Previsão): ")
                            if concluido == "1":
                                concluir = "Concluido em "
                                break
                            elif concluido == "2":
                                concluir = "Previsão de conclusão: "
                                break
                            else:
                                print("Erro: Número inválido. Digite '1' ou 2'.")
                        data = input("Insira a Nova data de conclusão no formato 'mes/ano': ")
                        formacao_selecionada['conclusao'] = concluir + data
                    print(f"Formação '{formacao_selecionada['tipo']}' atualizada.")
                else:
                    print("Número inválido.")
            except ValueError:
                print("Entrada inválida. Digite um número.")
        elif escolha == "R" and lista:
            try:
                indice = int(input("Digite o NÚMERO da formação para REMOVER: ")) - 1
                if 0 <= indice < len(lista):
                    nome_removido = lista[indice]['tipo']
                    lista.pop(indice)
                    print(f"Formação '{nome_removido}' removida com sucesso.")
                else:
                    print("Número inválido.")
            except ValueError:
                print("Entrada inválida. Digite um número.")
        else:
            print("Opção inválida.")
    
def editar_competencias(user):
    competencias_dict = user.competencias
    while True:
        print("\n--- Editando Competências ---")
        if not competencias_dict:
            print("Nenhuma competência cadastrada.")
        else:
            print("Competencias Atuais:")
            comp_lista = list(competencias_dict.items())
            for i, (tipo, comp) in enumerate(comp_lista):
                if isinstance(comp, list):
                    valor = ", ".join(comp)
                    tipo_valor = "(Lista)"
                else:
                    valor = comp
                    tipo_valor = "(Linha Descritiva)"
                print(f"{i+1}. {tipo} {tipo_valor}: {valor[:50]}...")
        print("\nOpções:")
        print("A. Adicionar Nova Categoria")
        if competencias_dict:
            print("E. Editar Categoria Existente (Título e/ou Conteúdo)")
            print("R. Remover Categoria")
        print("V. Voltar ao menu de Edição")
        escolha = input("Escolha uma opção (A/E/R/V): ").upper()
        if escolha == "V":
            break
        elif escolha == "A":
            add_competencias()
        elif escolha == "E" and competencias_dict:
            try:
                indice = int(input("Digite o NÚMERO da categoria para EDITAR: ")) - 1
                comp_lista = list(competencias_dict.items())
                if 0 <= indice < len(comp_lista):
                    tipo_antigo = comp_lista[indice][0]
                    competencias_obj = competencias_dict[tipo_antigo]
                    novo_tipo = input(f"Novo nome da Categoria (Atual: {tipo_antigo}, ou Enter para manter): ") or tipo_antigo
                    while True:
                        print(f"\nValor atual para {tipo_antigo}: {competencias_obj}")
                        if isinstance(competencias_obj, list):
                            print("\n[Edição de LISTA de Conteúdo] Opções:")
                            print("1. Adicionar item à Lista")
                            print("2. Editar item existente na Lista")
                            print("3. Remover item da Lista")
                            print("4. Substituir por nova Linha Descritiva")
                            print("V. Voltar ao Menu Principal de Competências")
                            sub_escolha = input("Escolha (1/2/3/4/V): ").upper()
                            if sub_escolha == "V":
                                break
                            elif sub_escolha == '1': # Adicionar item
                                novo_item = input("Digite o novo item da lista de {novo_tipo}: ")
                                competencias_obj.append(novo_item)
                                print(f"Item '{novo_item}' adicionado.")
                            elif sub_escolha == '2': # Editar item
                                print("Itens da Lista:")
                                for i, item in enumerate(competencias_obj):
                                    print(f"{i+1}. {item}")
                                try:
                                    item_indice = int(input("Número do item para editar: ")) - 1
                                    if 0 <= item_indice < len(competencias_obj):
                                        novo_valor = input(f"Novo valor (Atual: {competencias_obj[item_indice]} ou ENTER para não alterar): ") or competencias_obj[item_indice]
                                        competencias_obj[item_indice] = novo_valor
                                        print("Item atualizado.")
                                    else:
                                        print("Número inválido")
                                except ValueError:
                                    print("Entrada inválida.")
                            elif sub_escolha == '3': # Remover item
                                print("Itens da Lista:")
                                for i, item in enumerate(competencias_obj):
                                    print(f"{i+1}. {item}")
                                try: 
                                    item_indice = int(input("Numero do item para remover: ")) - 1
                                    if 0 <= item_indice < len(competencias_obj):
                                        item_removido = competencias_obj.pop(item_indice)
                                        print(f"Item '{item_removido}' removido.")
                                    else:
                                        print("Número inválido.")
                                except ValueError:
                                    print("Entrada inválida.")
                            elif sub_escolha == '4': # Substituir por String
                                competencias_obj = input("Digite a nova LINHA DESCRITIVA (será substituída): ")
                                print("Conteúdo alterado para Linha Descritiva.")
                                break # Sai do sub-menu
                        else: # É uma string (Linha Descritiva)
                            print("\n[Edição de LINHA DESCRITIVA] Opções:")
                            print("1. Editar Linha Descritiva")
                            print("2. Converter para nova Lista")
                            print("V. Voltar ao Menu Principal de Competências")
                            sub_escolha = input("Escolha (1/2/V): ").upper()
                            
                            if sub_escolha == 'V':
                                break
                            elif sub_escolha == '1': # Editar String
                                competencias_obj = input(f"Nova linha descritiva (Atual: {competencias_obj}, ou Enter para manter): ") or competencias_obj
                                print("Linha descritiva atualizada.")
                                break # Sai do sub-menu
                            elif sub_escolha == '2': # Converter para Lista
                                competencias_obj = competencias_lista(novo_tipo)
                                print("Conteúdo alterado para Lista.")
                                break # Sai do sub-menu
                    # 2. Atualização do Dicionário (Fora do Sub-menu - sai do while True)
                    if novo_tipo != tipo_antigo:
                        competencias_dict.pop(tipo_antigo) # Remove chave antiga
                        competencias_dict[novo_tipo] = competencias_obj # Insere nova chave/valor
                    else:
                        competencias_dict[tipo_antigo] = competencias_obj # Mantém a chave, atualiza o valor
                        
                    print(f"Categoria '{tipo_antigo}' atualizada para '{novo_tipo}'.")
                else:
                    print("Número inválido.")
            except ValueError:
                print("Entrada inválida. Digite um número.")
                
        elif escolha == 'R' and competencias_dict:
            try:
                indice = int(input("Digite o NÚMERO da categoria para REMOVER: ")) - 1
                comp_lista = list(competencias_dict.keys())
                
                if 0 <= indice < len(comp_lista):
                    tipo_removido = comp_lista[indice]
                    competencias_dict.pop(tipo_removido)
                    print(f"Categoria '{tipo_removido}' removida com sucesso.")
                else:
                    print("Número inválido.")
            except ValueError:
                print("Entrada inválida. Digite um número.")
        
        else:
            print("Opção inválida.")


def editar_experiencias(user):
    editar_lista_de_dicionarios(user, "experiencias", "Experiências")

def editar_projetos(user):
    editar_lista_de_dicionarios(user, "projetos", "Projetos")

def editar_certificacoes(user):
    editar_lista_de_dicionarios(user, "certificacoes", "Certificações")

def editar_idiomas(user):
    idiomas_dict = user.idiomas
    while True:
        print("\n--- Editando Idiomas ---")
        if not idiomas_dict:
            print("Nenhum idioma cadastrado.")
        else:
            print("Idiomas Atuais:")
            idiomas_lista = list(idiomas_dict.items())
            for i, (lingua, nivel) in enumerate(idiomas_lista):
                print(f"{i+1}. {lingua}: {nivel}")
        print("\nOpções:")
        print("A. Adicionar Novo Idioma")
        if idiomas_dict:
            print("E. Editar Nivel de um Idioma Existente")
            print("R. Remover Idioma")
        print("V. Voltar ao menu de Edição")
        escolha = input("Escolha uma opção (A/E/R/V): ").upper()
        if escolha == "V":
            break
        elif escolha == "A":
            lingua_nova = input("Digite o nome do NOVO idioma: ")
            if lingua_nova in idiomas_dict:
                print(f"Idioma '{lingua_nova}' já existe. Use a opção 'E' para editar o nível.")
                continue
            nivel_novo = input(f"Digite o nível de fluência para {lingua_nova}: ")
            idiomas_dict[lingua_nova] = nivel_novo
            print(f"Idioma '{lingua_nova}' adicionado.")
        elif escolha == "E" and idiomas_dict:
            try:
                indice = int(input("Digite o NÚMERO do idioma para EDITAR o nível: ")) - 1
                idiomas_lista = list(idiomas_dict.items())
                if 0 <= indice < len(idiomas_lista):
                    lingua_selecionada = idiomas_lista[indice][0]
                    nivel_antigo = idiomas_dict[lingua_selecionada]
                    novo_nivel = input(f"Novo nível de fluência (Atual: {nivel_antigo}): ")
                    idiomas_dict[lingua_selecionada] = novo_nivel
                    print(f"Nivel de '{lingua_selecionada}' atualizado para {novo_nivel}")
                else:
                    print("Número inválido.")
            except ValueError:
                print("Entrada inválida. Digite um número.")
        elif escolha == "R" and idiomas_dict:
            try:
                indice = int(input("Digite o NÚMERO do idioma para REMOVER: ")) - 1
                idiomas_lista = list(idiomas_dict.keys())
                if 0 <= indice < len(idiomas_lista):
                    lingua_removida = idiomas_lista[indice]
                    idiomas_dict.pop(lingua_removida)
                    print(f"Idioma '{lingua_removida}' removido com sucesso.")
                else:
                    print("Número inválido.")
            except ValueError:
                print("Entrada inválida. Digite um número.")
        else:
            print("Opção inválida.")


def editar_nome(user, dados):
    nome_antigo = user.nome
    novo_nome = input(f"Nome atual ({nome_antigo}). Digite o novo nome: ")
    if novo_nome and novo_nome != nome_antigo:
        if novo_nome in dados:
            print("Erro: Novo nome já está em uso.")
            return
        dados[novo_nome] = dados.pop(nome_antigo)
        dados[novo_nome].nome = novo_nome
        print(f"Nome atualizado para {novo_nome}")

def editar_email(user):
    while True:
        email = input("Email atual ({user.email}). Digite o novo email: ")
        try:
            User(nome = user.nome, email=email)
            user.email = email
            print("Email atualizado e validado com sucesso!")
            break
        except ValidationError as e:
            print("Erro de validação: O formato do email é inválido.")
            if input("Tentar novamente (S/N)? ").lower() != "s":
                break

def editar_linkedin(user):
    while True:
        linkedin = input(f"LinkedIn atual ({user.linkedin or 'N/A'}). Digite o novo link (ou 'none'): ")
        if linkedin.lower() == "none":
            user.linkedin = "" # Limpa o campo
            print("LinkedIn removido.")
            break
        try:
            # Pydantic valida o formato da URL aqui (HttpUrl)
            User(nome=user.nome, linkedin=linkedin) 
            user.linkedin = linkedin
            print("LinkedIn atualizado e validado com sucesso!")
            break
        except ValidationError:
            print("Erro de Validação: A URL do LinkedIn é inválida (deve começar com http:// ou https://).")
            if input("Tentar novamente (S/N)? ").lower() != 's':
                break

def editar_github(user):
    while True:
        github = input(f"GitHub atual ({user.github or 'N/A'}). Digite o novo link (ou 'none'): ")
        if github.lower() == "none":
            user.github = ""
            print("GitHub removido.")
            break
        try:
            # Pydantic valida o formato da URL aqui (HttpUrl)
            User(nome=user.nome, github=github) 
            user.github = github
            print("GitHub atualizado e validado com sucesso!")
            break
        except ValidationError:
            print("❌ Erro de Validação: A URL do GitHub é inválida (deve começar com http:// ou https://).")
            if input("Tentar novamente (S/N)? ").lower() != 's':
                break

def editar_celular(user):
    celular = input("Digite seu numero de celular: ")
    user.celular = celular

def editar_estado(user):
    estado = input("Digite a sigla do seu estado: ")
    user.estado = estado

def editar_cidade(user):
    cidade = input("Digite o nome da sua cidade: ")
    user.cidade = cidade

def editar_objetivo(user):
    objetivo = input("Digite uma frase como seu objetivo profissional: ")
    user.objetivo = objetivo

def editar_disponibilidade(user):
    print("\n--- Editando Disponibilidade ---")
    print("Opções sugeridas: 1. Integral, 2. Manhã, 3. Tarde, 4. Noite, 5. Finais de Semana")
    
    nova_disponibilidade = input("Digite sua(s) disponibilidade(s) separada(s) por VÍRGULAS (Ex: 'Integral, Finais de Semana'): ")
    
    # Se a entrada não for vazia, atualiza.
    if nova_disponibilidade.strip():
        user.disponibilidade = nova_disponibilidade.strip()
        print(f"Disponibilidade atualizada para: {user.disponibilidade}")
    else:
        print("Disponibilidade não alterada.")

def editar_informacoes_adicionais(user):
    informacoes_adicionais = input("Digite o link do seu github se houver (ou 'none' se não tiver): ")
    if informacoes_adicionais != "none":
        user.informacoes_adicionais = informacoes_adicionais

def editar_usuario(dados, user):
    atributos = {
        "1": lambda: editar_nome(user, dados),
        "2": lambda: editar_email(user),
        "3": lambda: editar_linkedin(user),
        "4": lambda: editar_github(user),
        "5": lambda: editar_celular(user),
        "6": lambda: editar_estado(user),
        "7": lambda: editar_cidade(user),
        "8": lambda: editar_objetivo(user),
        "9": lambda: editar_formacao(user),    
        "10": lambda: editar_competencias(user), 
        "11": lambda: editar_experiencias(user), 
        "12": lambda: editar_projetos(user),    
        "13": lambda: editar_certificacoes(user),
        "14": lambda: editar_idiomas(user),
        "15": lambda: editar_disponibilidade(user),
        "16": lambda: editar_informacoes_adicionais(user)
    }
    while True:
        print(f"\n--- Editando Currículo de {user.nome} ---")
        print("1. Nome")
        print("2. Email")
        print("3. LinkedIn")
        print("4. GitHub")
        print("5. Celular")
        print("6. Estado")
        print("7. Cidade")
        print("8. Objetivo")
        print("9. Formação")
        print("10. Competências")
        print("11. Experiências")
        print("12. Projetos")
        print("13. Certificações")
        print("14. Idiomas")
        print("15. Disponibilidade")
        print("16. Informações Adicionais")
        print("0. Voltar ao Menu Principal")
        try:
            escolha = input("Digite o número do atributo que você quer editar: ")
            if escolha == '0':
                return
            acao = atributos.get(escolha)
            if acao:
                acao()
                print("Atributo editado com sucesso!")
            else:
                print("Opção inválida.")
        except Exception as e:
            print(f"Ocorreu um erro durante a edição: {e}")

def print_curriculo_terminal(user):
    """Exibe os dados completos de um único usuário."""
    if not user:
        return
        
    print(f"\n--- 📄 Currículo de {user.nome} ---")
    print(f"Objetivo Profissional: {user.objetivo}")
    print("\n--- Contato ---")
    print(f"Email: {user.email}")
    print(f"Celular: {user.celular}")
    print(f"Localização: {user.cidade} - {user.estado}")
    print(f"LinkedIn: {user.linkedin or 'N/A'}")
    print(f"GitHub: {user.github or 'N/A'}")
    print(f"Disponibilidade: {user.disponibilidade}")
    
    print("\n--- Formação ---")
    if user.formacao:
        for f in user.formacao:
            print(f"* {f['tipo']} em {f['onde']} ({f['conclusao']})")
    else:
        print("Nenhuma formação cadastrada.")

    print("\n--- Competências ---")
    if user.competencias:
        for tipo, comp in user.competencias.items():
            if isinstance(comp, list):
                print(f"  > {tipo}: {', '.join(comp)}")
            else:
                print(f"  > {tipo}: {comp}")
    else:
        print("Nenhuma competência cadastrada.")
        
    def exibir_lista_de_itens(titulo, lista):
        print(f"\n--- {titulo} ---")
        if lista:
            for item in lista:
                if isinstance(item, dict):
                    for k, v in item.items():
                         print(f"* {k}: {v}")
                elif isinstance(item, str):
                    print(f"* {item}")
        else:
            print(f"Nenhum(a) {titulo.lower()} cadastrado(a).")

    exibir_lista_de_itens("Experiências", user.experiencias)
    exibir_lista_de_itens("Projetos", user.projetos)
    exibir_lista_de_itens("Certificações", user.certificacoes)
    
    print("\n--- Idiomas ---") 
    if user.idiomas:
        for lingua, nivel in user.idiomas.items():
            print(f"* {lingua}: {nivel}")
    else:
        print("Nenhum idioma cadastrado.")

    print(f"\n--- Informações Adicionais ---")
    print(user.informacoes_adicionais or 'N/A')
    print("--------------------------------------\n")
    
def ver_curriculo_alheio(dados):
    user = selecionar_usuario(dados)
    if user:
        print_curriculo_terminal(user)

def remover_usuario(dados, user):
    check = input(f"Tem certeza que deseja remover **TODOS** os dados de '{user.nome}' (S/N)? ")
    if check.lower() == 's':
        nome = user.nome
        dados.pop(nome)        
        print(f"Usuário '{nome}' removido com sucesso!\n")
    elif check.lower() == 'n':
        print(f"Remoção de '{user.nome}' cancelada.\n")
    else:
        print("Entrada não aceita. Favor digitar 'S' ou 'N'.")
        remover_usuario(dados, user)

def remover_user(dados):
    user_a_remover = selecionar_usuario(dados)
    if user_a_remover:
        remover_usuario(dados, user_a_remover) 

def login(dados):
    nome = input("Digite seu nome para fazer login (ou '0' para cancelar): ")
    if nome == '0':
        return None
    user = dados.get(nome)
    if user:
        print(f"Login bem-sucedido! Bem-vindo(a), {user.nome}.\n")
        return user 
    else:
        print(f"Usuário '{nome}' não encontrado. Você precisa cadastrar o usuário primeiro (Opção 2 do Menu Principal).\n")
        return None

def logout():
    print("Sessão encerrada. Voltando ao menu inicial.")
    return None

def menu_login(dados):
    print("\n=== Acesso ao Gerenciador de Currículos ===")
    print("1. Fazer Login")
    print("2. Cadastrar Novo Usuário")
    print("3. Ver Lista de Usuários (Apenas Nomes)")
    print("4. Salvar e Sair")
    
    opcao = input("Escolha uma opção: ")
    print()
    
    if opcao == "1":
        return login(dados)
    elif opcao == "2":
        return adicionar_user(dados)
    elif opcao == "3":
        mostrar_nomes(dados)
        return None
    elif opcao == "4":
        return "sair"
    else:
        print("Opção inválida. Tente novamente.")
        return None

def menu_principal(dados, user):
    print(f"\n=== Logado como {user.nome} ===")
    print("1. Visualizar MEU Currículo Completo")
    print("2. Editar MEU Currículo")
    print("3. Visualizar Outro Currículo")
    print("4. Deletar minha Conta")
    print("5. Fazer Logout")
    print("6. Salvar e Sair")
    
    opcao = input("Escolha uma opção: ")
    print()
    
    if opcao == "1":
        print_curriculo_terminal(user)
    elif opcao == "2":
        editar_usuario(dados, user)
    elif opcao == "3":
        ver_curriculo_alheio(dados)
    elif opcao == "4":
        remover_usuario(dados, user)
        return "logout"
    elif opcao == "5":
        return "logout"
    elif opcao == "6":
        return "sair"
    else:
        print("Opção inválida. Tente novamente.")
    return None

def mostrar_nomes(dados):
    if not dados:
        print("Nenhum dado adicionado ainda.")
    else:
        print("Todos os usuários cadastrados:\n")
        for i, user in enumerate(dados.values()):
            print(f"{i+1}. {user.nome}")
    print()

def carregar_dados():
    if os.path.exists(ARQUIVO_JSON):
        try:
            with open(ARQUIVO_JSON, 'r') as f:
                dados_lista = json.load(f)
                dados = {}
                for user_dict in dados_lista:
                    try:
                        user_obj = User.model_validate(user_dict) 
                        dados[user_obj.nome] = user_obj
                    except ValidationError as e:
                        print(f"Aviso: Dados de usuário inválidos encontrados e ignorados: {e}")
                if dados:
                    print("Dados carregados do arquivo!")
                return dados
        except Exception as e:
            print(f"Erro ao carregar o arquivo {ARQUIVO_JSON}: {e}")
            return {}
    return{}

def salvar_dados(dados):
    dados_para_salvar = [user.model_dump() for user in dados.values()]
    try:
        with open(ARQUIVO_JSON, 'w') as f:
            json.dump(dados_para_salvar, f, indent=4, ensure_ascii=False)
        print("Dados salvos com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar dados: {e}")

def salvar_e_sair(dados):
    salvar_dados(dados)
    print("Saindo...")
    return "sair"
    
def selecionar_usuario(dados): # retorna user
    mostrar_nomes(dados)
    while True: 
        try:
            nome = input("Digite o nome do usuário a ser selecionado (ou '0' para adicionar um usuário/cancelar): ").strip()
            if nome == '0':
                return None 
            check = 'n'
            if nome not in dados:
                raise KeyError
            while check.lower() != 's':
                check = input(f"Você deseja selecionar o currículo de {dados[nome].nome} (S/N)? ")
                if check.lower() == 's':
                    return dados[nome]
                else:
                    print("Seleção cancelada. Tente novamente com outro nome.")
                    break 
        except KeyError:
            print(f"Usuário '{nome}' não existe.\n")
        except (ValueError, IndexError):
            print("Entrada inválida.\n")
    return None

# __main__ 

if __name__ == "__main__":
    running = 1
    dados = carregar_dados() 
    usuario_logado = None
    
    while running == 1:
        if usuario_logado:
            status = menu_principal(dados, usuario_logado)
            
            if status == "sair":
                running = 0
            elif status == "logout":
                usuario_logado = logout()
        else:
            status = menu_login(dados)
            
            if status == "sair":
                running = 0
            elif isinstance(status, User):
                usuario_logado = status
                
    salvar_e_sair(dados)
