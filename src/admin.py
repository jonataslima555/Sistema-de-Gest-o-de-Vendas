import hashlib
import os
from colorama import init, Fore, Style
from models import Admin, User, Relatorio, Meta
from peewee import fn
# Inicializar o colorama
init(autoreset=True)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def clear_terminal():
    """Limpa o terminal para Windows ou Linux"""
    os.system('cls' if os.name == 'nt' else 'clear')

def home_login(user, password):
    clear_terminal()
    try:
        # Tenta buscar o administrador pelo nome de usuário
        admin = Admin.get(Admin.user == user)
        
        # Hash da senha fornecida para comparação
        hashed_password = hash_password(password)

        # Compara a senha hashada com a armazenada no banco de dados
        if admin.password == hashed_password:
            print(f"{Fore.GREEN}Login bem-sucedido! Bem-vindo, {user.capitalize()}!")
            return home()
        else:
            print(f"{Fore.RED}Senha incorreta. Tente novamente.")
    
    except Admin.DoesNotExist:
        print(f"{Fore.RED}Usuário não encontrado.")
    except Exception as e:
        print(f"{Fore.RED}Ocorreu um erro durante o login: {e}")

def see_vendedor():
    """Exibe a lista de vendedores e permite selecionar um vendedor pelo CPF"""
    clear_terminal()
    try:
        vendedores = User.select()
        
        # Listar todos os vendedores
        if vendedores:
            print(f"{Fore.YELLOW}Lista de vendedores:\n")
            for vendedor in vendedores:
                print(f"{Fore.CYAN}Nome: {vendedor.user} | CPF: {vendedor.cpf}")
            
            # Solicitar CPF do vendedor para ver os relatórios
            cpf = input(f"\n{Fore.YELLOW}Digite o CPF do vendedor para ver os relatórios: {Fore.RESET}")
            
            # Buscar o vendedor selecionado
            vendedor_selecionado = User.get(User.cpf == cpf)
            
            # Exibir os relatórios do vendedor selecionado
            see_relatorios(vendedor_selecionado)
        else:
            print(f"{Fore.RED}Nenhum vendedor encontrado.")
    except User.DoesNotExist:
        print(f"{Fore.RED}Vendedor não encontrado.")
    except Exception as e:
        print(f"{Fore.RED}Ocorreu um erro: {e}")

def see_relatorios(vendedor):
    """Exibe todos os relatórios de vendas de um vendedor específico"""
    clear_terminal()
    try:
        relatorios = Relatorio.select().where(Relatorio.user == vendedor)

        if relatorios:
            print(f"\n{Fore.YELLOW}Relatórios de vendas para o vendedor {Fore.CYAN}{vendedor.user}:\n")
            for relatorio in relatorios:
                print(f"{Fore.GREEN}Total Vendas: {relatorio.total_vendas} | "
                      f"Meta Vendas: {relatorio.meta_vendas} | "
                      f"Data CEP: {relatorio.data_cep}")
        else:
            print(f"{Fore.RED}\nNenhum relatório encontrado para o vendedor {vendedor.user}.")
    except Exception as e:
        print(f"{Fore.RED}Ocorreu um erro ao buscar os relatórios: {e}")

def home():
    """Menu principal do administrador"""
    clear_terminal()
    print(f"{Fore.YELLOW}{'='*40}")
    print(f"{Fore.BLUE}   Sistema de Gestão de Vendas - Admin")
    print(f"{Fore.YELLOW}{'='*40}\n")

    print(f'{Fore.CYAN}1. Criar conta para vendedor')
    print(f'{Fore.CYAN}2. Ver vendedores')
    print(f'{Fore.CYAN}3. Adicionar meta para vendedor')  # Nova opção para adicionar meta
    print(f'{Fore.CYAN}4. Ver progresso de vendedores')   # Nova opção para ver progresso
    print(f'{Fore.CYAN}5. Sair')

    escolha = input(f"\n{Fore.YELLOW}Escolha uma opção: {Fore.RESET}")
    
    if escolha == '1':
        clear_terminal()
        print(f"{Fore.BLUE}Criando uma nova conta de vendedor:\n")
        user = input(f'{Fore.CYAN}Nome do vendedor: ')
        password = input(f'{Fore.CYAN}Senha do vendedor: ')
        cpf = input(f'{Fore.CYAN}CPF do vendedor: ')
        User.create_account(user, password, cpf)
        input(f"{Fore.GREEN}\nVendedor criado com sucesso! Pressione Enter para continuar...")
        return home()
    elif escolha == '2':
        see_vendedor()  # Chama a função para ver e selecionar vendedores
        input(f"\n{Fore.YELLOW}Pressione Enter para voltar ao menu principal...")
        return home()
    elif escolha == '3':
        criar_meta_para_vendedor()  # Chama a função de criar meta
        input(f"\n{Fore.YELLOW}Pressione Enter para voltar ao menu principal...")
        return home()
    elif escolha == '4':
        ver_progresso_vendedor()  # Chama a função de ver progresso de vendedores
        input(f"\n{Fore.YELLOW}Pressione Enter para voltar ao menu principal...")
        return home()
    elif escolha == '5':
        print(f'{Fore.GREEN}Saindo...')
    else:
        print(f'{Fore.RED}Opção inválida. Tente novamente.')
        input(f"{Fore.YELLOW}Pressione Enter para tentar novamente...")
        return home()


def criar_meta_para_vendedor():
    """Permite ao administrador criar uma meta de vendas para um vendedor."""
    clear_terminal()
    
    # Listar todos os vendedores
    vendedores = User.select()
    if vendedores:
        print(f"{Fore.YELLOW}Lista de vendedores:\n")
        for vendedor in vendedores:
            print(f"{Fore.CYAN}Nome: {vendedor.user} | CPF: {vendedor.cpf}")
        
        cpf = input(f"\n{Fore.YELLOW}Digite o CPF do vendedor para criar uma meta: {Fore.RESET}")
        
        try:
            vendedor_selecionado = User.get(User.cpf == cpf)
            meta_vendas = input(f"\n{Fore.CYAN}Digite o valor da meta de vendas: ")
            mes = input(f"{Fore.CYAN}Digite o mês (Ex: Setembro ou 2024-09): ")

            Meta.criar_meta(vendedor_selecionado, meta_vendas, mes)
            input(f"{Fore.GREEN}\nMeta criada com sucesso! Pressione Enter para continuar...")
        
        except User.DoesNotExist:
            print(f"{Fore.RED}Vendedor não encontrado.")
    else:
        print(f"{Fore.RED}Nenhum vendedor encontrado.")

def ver_progresso_vendedor():
    """Permite ao administrador ver o progresso do vendedor em relação à meta."""
    clear_terminal()
    
    vendedores = User.select()
    if vendedores:
        print(f"{Fore.YELLOW}Lista de vendedores:\n")
        for vendedor in vendedores:
            print(f"{Fore.CYAN}Nome: {vendedor.user} | CPF: {vendedor.cpf}")
        
        cpf = input(f"\n{Fore.YELLOW}Digite o CPF do vendedor para ver o progresso da meta: {Fore.RESET}")
        
        try:
            vendedor_selecionado = User.get(User.cpf == cpf)
            meta_atual = Meta.get_or_none(Meta.user == vendedor_selecionado, Meta.mes == 'Setembro')
            
            if meta_atual:
                vendas_totais = Relatorio.select(fn.SUM(Relatorio.total_vendas)).where(Relatorio.user == vendedor_selecionado).scalar()
                progresso = (vendas_totais / meta_atual.meta_vendas) * 100
                
                print(f"{Fore.GREEN}Meta de {meta_atual.meta_vendas} para {meta_atual.mes}")
                print(f"Vendas atuais: {vendas_totais}")
                print(f"Progresso: {Fore.BLUE}[{'#' * int(progresso // 10)}{'-' * (10 - int(progresso // 10))}] {progresso:.2f}%")
            else:
                print(f"{Fore.RED}O vendedor não tem metas para este mês.")
        
        except User.DoesNotExist:
            print(f"{Fore.RED}Vendedor não encontrado.")
    else:
        print(f"{Fore.RED}Nenhum vendedor encontrado.")
