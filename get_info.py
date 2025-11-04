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
        self.competencias = {"linguagens": []}
        self.experiencias = []
        self.projetos = []
        self.certificacoes = []
        self.idiomas = []
        self.disponibilidade = ""
        self.informacoes_adicionais = ""

def carregar_dados():
    if os.path.exists(ARQUIVO_JSON):
        try:
            with open(ARQUIVO_JSON, 'r') as f:
                dados = json.load(f)
                print("Dados carregados do arquivo!")
                return dados
        except Exception as e:
            print(f"Erro ao carregar o arquivo {ARQUIVO_JSON}: {e}")
            return []
    return[]

def salvar_dados(dados):
    try:
        with open(ARQUIVO_JSON, 'w') as f:
            json.dump(dados, f, indent=4)
        print("Dados salvos com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar dados: {e}")

def mostrar_nomes(dados):
    if not dados:
        print("Nenhum dado adicionado ainda.")
    else:
        print("Todos os dados:\n")
        for i in range(len(dados)):
            dado = dados[i]
            print(f"{i+1}. {dado["nome"]}")
    print()

# ------------------------------------------------------
def adicionar_user(dados):
    nome = input("Digite seu nome: ")
    dados.append({"nome": nome, })
    print(f"Tarefa '{titulo}' adicionada!\n")

def editar_dados(dados):
    mostrar_nomes(dados)
    if dados:
        try:
            num = int(input("Digite o numero da tarefa concluida: "))
            dados[num-1]["feita"] = True
            print("Tarefa marcada como feita!\n")
        except (ValueError, IndexError):
            print("Número inválido.\n")

def remover_tarefa(dados):
    mostrar_nomes(dados)
    if dados:
        try:
            num = int(input("Digite o numero da tarefa para remover: "))
            if 1 <= num <= len(dados):
                dado = dados.pop(num-1)
                print(f"Tarefa '{dado['titulo']}' removida!\n")
        except (ValueError, IndexError):
            print("Número inválido.\n")

def sair(dados):
    salvar_dados(dados)
    print("Saindo...")
    return "sair"

# def menu(tarefas):
#     print("=== To-do List ===")
#     print("1. Ver tarefas")
#     print("2. Adicionar tarefa")
#     print("3. Marcar como feita")
#     print("4. Remover tarefa")
#     print("5. Salvar e Sair")
#     opcao = input("Escolha uma opcao: ")
#     acoes = {
#         "1": lambda: mostrar_tarefas(tarefas),
#         "2": lambda: adicionar_tarefa(tarefas),
#         "3": lambda: marcar_como_feita(tarefas),
#         "4": lambda: remover_tarefa(tarefas),
#         "5": lambda: sair(tarefas)
#     }
#     acao = acoes.get(opcao, lambda: print("Opcao inválida\n"))
#     if acao() == "sair":
#         return 0
#     return 1

if __name__ == "__main__":
    running = 1
    dados = carregar_dados()

    # while running == 1:
    #     running = menu(dados)

