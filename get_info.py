import json
import os

ARQUIVO_JSON = "info.json"

class User:
    def __init__(self, nome):
        self.nome = nome
        self.email = ""
        self.linkedin = ""
        self.github = ""
        self.celular = ""
        self.estado = ""
        self.cidade = ""
        self.objetivo = ""
        self.formacao = []
        self.competencias = {}
        self.experiencias = []
        self.projetos = []
        self.certificacoes = []
        self.idiomas = []
        self.disponibilidade = ""
        self.informacoes_adicionais = ""

    def to_dict(self):
        return self.__dict__
    
    @classmethod
    def from_dict(cls, data):
        # Cria uma nova instância de User a partir de um dicionário (vindo do JSON)
        user = cls(data.get('nome', 'Desconhecido'))
        user.__dict__.update(data)
        return user

# Setters da classe User

def add_formacao(user):
    tipo_formacao = input("Digite o nome da sua formacao (Exemplo: 'Bacharelado em Engenharia de Computação'): ")
    local_formacao = input("Digite o nome da instituição de sua formação (Exemplo: 'PUC Minas - Pontifícia Universidade Católica de Minas Gerais'): ")
    concluido = input("Digite 1 se já foi concluída e 2 para previsão de conclusão: ")
    conclusao = ""
    if concluido == '1':
        concluir = "Concluído em "
    elif concluido == '2':
        concluir = "Previsão de conclusão: "
    else:
        print("Erro: Número inválido. Repetindo inserção de formação...")
        return False
    data = input("Insira a data de formacao no formato 'mes/ano': ")
    conclusao = conclusao + data 
    user.formacao.append({"tipo": tipo_formacao, "onde": local_formacao, "conclusao": conclusao})
    return True

def experiencias_lista(user):
    lista = []
    check = 's'
    while check.lower() == 's':
        titulo = input(f"Digite o título {len(lista)+1}° item da lista de experiencias: ")
        descricao = input(f"Digite a descrição de {titulo}: ")
        lista.append({titulo:descricao})
        check = input("Você quer adicionar mais itens na lista de experiências (S/N)? ")
        if check.lower() != 'n' and check.lower() != 's':
                print("Erro: Resposta inválida. Perguntando novamente...")
    return lista

def certificacoes_lista(user):
    lista = []
    check = 's'
    while check.lower() == 's':
        titulo = input(f"Digite o título {len(lista)+1}° item da lista de certificados: ")
        descricao = input(f"Digite a descrição de {titulo}: ")
        lista.append({titulo:descricao})
        check = input("Você quer adicionar mais itens na lista de certificados (S/N)? ")
        if check.lower() != 'n' and check.lower() != 's':
                print("Erro: Resposta inválida. Perguntando novamente...")
    return lista

def idiomas_lista(user):
    lista = []
    check = 's'
    while check.lower() == 's':
        lista.append(input("Digite um idioma para ser adicionado: "))
        check = input("Você quer adicionar mais idiomas (S/N)? ")
        if check.lower() != 'n' and check.lower() != 's':
                print("Erro: Resposta inválida. Perguntando novamente...")
    return lista

def projetos_lista(user):
    lista = []
    check = 's'
    while check.lower() == 's':
        titulo = input(f"Digite o título {len(lista)+1}° item da lista de projetos: ")
        descricao = input(f"Digite a descrição de {titulo}: ")
        lista.append({titulo:descricao})
        check = input("Você quer adicionar mais itens na lista de projetos (S/N)? ")
        if check.lower() != 'n' and check.lower() != 's':
                print("Erro: Resposta inválida. Perguntando novamente...")
    return lista

def competencias_lista(tipo):
    lista = []
    check = 's'
    while check.lower() == 's':
        lista.append(input(f"Digite o {len(lista)+1}° item da lista de {tipo}: "))
        check = input("Você quer adicionar mais itens na lista (S/N)? ")
        if check.lower() != 'n' and check.lower() != 's':
                print("Erro: Resposta inválida. Perguntando novamente...")
    return lista

def add_competencias(user):
    tipo_competencia = input("Digite o nome da categoria de competencias que voce quer adicionar: ")
    lista_ou_string = input("Digite 1 se quiser fazer uma lista ou 2 se quiser escrever uma linha descritiva: ")
    competencias = None
    if lista_ou_string == '1':
        competencias = competencias_lista(tipo_competencia)
    elif lista_ou_string == '2':
        competencias = input("Digite a linha descritiva da competencia: ")
    else:
        print("Erro: Número inválido. Repetindo inserção de competencias...")
        return False
    user.competencias[tipo_competencia] = competencias
    return True

# Constructor e Mostrar

def adicionar_user(dados): # retorna user
    nome = input("Digite seu nome: ")
    if nome in dados:
        print(f"Erro: Usuário {nome} já existe. Não foi possível adicionar.")
        return None
    dados[nome] = User(nome)
    email = input("Digite seu email: ")
    dados[nome].email = email
    linkedin = input("Digite o link do seu linkedin (ou 'none' se não tiver): ")
    if linkedin != "none":
        dados[nome].linkedin = linkedin
    github = input("Digite o link do seu github se houver (ou 'none' se não tiver): ")
    if github != "none":
        dados[nome].github = github
    celular = input("Digite seu numero de celular: ")
    dados[nome].celular = celular
    estado = input("Digite a sigla do seu estado: ")
    dados[nome].estado = estado
    cidade = input("Digite o nome da sua cidade: ")
    dados[nome].cidade = cidade
    objetivo = input("Digite uma frase como seu objetivo profissional: ")
    dados[nome].objetivo = objetivo
    # --- Adicionar Formações ---
    while True:
        if add_formacao(dados[nome]):
            check = input("Quer adicionar mais formações (S/N)? ")
            if check.lower() != 's':
                break
    # --- Adicionar Competências ---
    while True:
        if add_competencias(dados[nome]):
            check = input("Quer adicionar mais competências (S/N)? ")
            if check.lower() != 's':
                break
    experiencias = experiencias_lista(dados[nome])
    dados[nome].experiencias = experiencias
    projetos = projetos_lista(dados[nome])
    dados[nome].projetos = projetos
    certificacoes = certificacoes_lista(dados[nome])
    dados[nome].certificacoes = certificacoes
    idiomas = idiomas_lista(dados[nome])
    dados[nome].idiomas = idiomas
    disponibilidade = input("Digite o horario da sua disponibilidade (manha/tarde/noite): ")
    dados[nome].disponibilidade = "Período da " + disponibilidade
    informacoes_adicionais = input("Digite um paragrafo curto sobre você se quiser (ou 'none' se não): ")
    if informacoes_adicionais != "none":
        dados[nome].informacoes_adicionais = informacoes_adicionais
    print(f"Usuário '{nome}' adicionado!\n")
    return dados[nome]

def mostrar_nomes(dados):
    if not dados:
        print("Nenhum dado adicionado ainda.")
    else:
        print("Todos os dados:\n")
        for i, user in enumerate(dados.values()):
            print(f"{i+1}. {user.nome}")
    print()

# Ações com o Json

def carregar_dados():
    if os.path.exists(ARQUIVO_JSON):
        try:
            with open(ARQUIVO_JSON, 'r') as f:
                dados_lista = json.load(f)
                dados = {}
                for user_dict in dados_lista:
                    user_obj = User.from_dict(user_dict) # Converte para objeto User
                    dados[user_obj.nome] = user_obj # Adiciona ao dicionário com o nome como chave
                print("Dados carregados do arquivo!")
                return dados
        except Exception as e:
            print(f"Erro ao carregar o arquivo {ARQUIVO_JSON}: {e}")
            return {}
    return{}

def salvar_dados(dados):
    dados_para_salvar = [user.to_dict() for user in dados.values()]
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

# Seleçao de usuario

def selecionar_usuario(dados): # retorna user
    mostrar_nomes(dados)
    while True: # Loop para permitir múltiplas tentativas de seleção
        try:
            nome = input("Digite o nome do usuário a ser editado (ou '0' para adicionar um usuário/cancelar): ").strip()
            
            if nome == '0':
                # Se 0, chama adicionar e retorna o resultado (User ou None)
                return adicionar_user(dados) 
            
            check = 'n'
            
            # 1. Tenta acessar o usuário para confirmação (lança KeyError se não existir)
            if nome not in dados:
                 raise KeyError 

            # 2. Se existe, entra no loop de confirmação
            while check.lower() != 's':
                check = input(f"Você deseja editar o currículo de {dados[nome].nome} (S/N)? ")
                
                if check.lower() == 's':
                    return dados[nome] # Seleção bem-sucedida, sai da função
                else:
                    print("Seleção cancelada. Tente novamente com outro nome.")
                    break # Sai do loop de confirmação para recomeçar o loop principal (While True)
                    
        except KeyError:
            # Capturado se 'nome' não estiver em 'dados'
            print(f"Usuário '{nome}' não existe.\n")
            # O loop 'while True' continua, pedindo novo input.
            
        except (ValueError, IndexError):
            # Captura outros erros (embora menos prováveis)
            print("Entrada inválida.\n")
            # O loop 'while True' continua, pedindo novo input.

    return None # Nunca deve ser alcançado
            
# Editar atributos do usuario

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
    email = input("Digite seu email: ")
    user.email = email
def editar_linkedin(user):
    linkedin = input("Digite o link do seu linkedin (ou 'none' se não tiver): ")
    if linkedin != "none":
        user.linkedin = linkedin
def editar_github(user):
    github = input("Digite o link do seu github se houver (ou 'none' se não tiver): ")
    if github != "none":
        user.github = github
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
def editar_formacao(user):
    while True:
        if add_formacao(user):
            check = input("Quer adicionar mais formações (S/N)? ")
            if check.lower() != 's':
                break
def editar_competencias(user):
    while True:
        if add_competencias(user):
            check = input("Quer adicionar mais competências (S/N)? ")
            if check.lower() != 's':
                break
def editar_experiencias(user):
    experiencias = experiencias_lista(user)
    user.experiencias = experiencias
def editar_projetos(user):
    projetos = projetos_lista(user)
    user.projetos = projetos
def editar_certificacoes(user):
    certificacoes = certificacoes_lista(user)
    user.certificacoes = certificacoes
def editar_idiomas(user):
    idiomas = idiomas_lista(user)
    user.idiomas = idiomas
def editar_disponibilidade(user):
    disponibilidade = input("Digite o horario da sua disponibilidade (manha/tarde/noite): ")
    user.disponibilidade = "Período da " + disponibilidade
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
    
# Deletar usuário

def remover_usuario(dados, user):
    dados.pop(user.nome)

def remover_user(dados):
    user_a_remover = selecionar_usuario(dados)
    if user_a_remover:
        nome_escolhido = user_a_remover.nome
        check = input(f"Tem certeza que deseja remover **TODOS** os dados de '{nome_escolhido}' (S/N)? ")
        if check.lower() == 's':
            remover_usuario(dados, user_a_remover) 
            print(f"Usuário '{nome_escolhido}' removido com sucesso!\n")
        else:
            print(f"Remoção de '{nome_escolhido}' cancelada.\n")

# Visualização de curriculos

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
                print(f"  > {tipo}: {', '.join(comp)}")
            else:
                print(f"  > {tipo}: {comp}")
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
    exibir_lista_de_itens("Idiomas", user.idiomas)

    print(f"\n--- Informações Adicionais ---")
    print(user.informacoes_adicionais or 'N/A')
    print("--------------------------------------\n")

def ver_curriculo_alheio(dados):
    user = selecionar_usuario(dados)
    if user:
        print_curriculo_terminal(user)

# Login e Menu principal

def login(dados):
    nome = input("Digite seu nome para fazer login (ou '0' para cancelar): ")
    if nome == '0':
        return None
    user = dados.get(nome)
    if user:
        print(f"Login bem-sucedido! Bem-vindo(a), {user.nome}.\n")
        return user # Retorna o objeto User logado
    else:
        print(f"Usuário '{nome}' não encontrado. Você precisa cadastrar o usuário primeiro (Opção 2 do Menu Principal).\n")
        return None

def logout():
    """Limpa o status de usuário logado."""
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
    print("4. Remover Currículo (Qualquer Um)")
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
        remover_user(dados)
    elif opcao == "5":
        return "logout"
    elif opcao == "6":
        return "sair"
    else:
        print("Opção inválida. Tente novamente.")
    
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
