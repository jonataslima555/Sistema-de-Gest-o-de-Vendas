from decimal import Decimal
import hashlib
import os
from models import User, Relatorio, Meta
from apis import get_cep
from colorama import init, Fore
from peewee import fn

# Inicializa colorama
init(autoreset=True)

def hash_password(password):
    """Hash de senha usando SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def clear_terminal():
    """Limpa o terminal para Windows ou Linux."""
    os.system('cls' if os.name == 'nt' else 'clear')

def ver_progresso_vendedor(vendedor):
    """Exibe o progresso do vendedor em relação à meta"""
    clear_terminal()
    print(f"{Fore.YELLOW}=== Progresso da Meta ===\n")

    try:
        # Busca a meta mais recente para o vendedor
        meta = Meta.select().where(Meta.user == vendedor).order_by(Meta.id.desc()).get()

        # Busca o total de vendas realizadas pelo vendedor
        total_vendas = Relatorio.select(fn.SUM(Relatorio.total_vendas)).where(Relatorio.user == vendedor).scalar() or 0

        # Calcula o progresso
        progresso = (total_vendas / meta.valor) * 100

        # Exibe a barra de progresso
        barra = int(progresso // 5)  # Para exibir uma barra de 20 caracteres
        print(f"Meta: {meta.valor} vendas")
        print(f"Total de Vendas: {total_vendas}")
        print(f"Progresso: [{Fore.GREEN}{'█' * barra}{' ' * (20 - barra)}{Fore.RESET}] {progresso:.2f}%")
        
        # Exibe se a meta foi batida ou quanto falta
        if progresso >= 100:
            print(f"{Fore.GREEN}Parabéns! Você atingiu ou ultrapassou a meta!")
        else:
            restante = meta.valor - total_vendas
            print(f"{Fore.YELLOW}Faltam {restante} vendas para bater a meta.")

    except Meta.DoesNotExist:
        print(f"{Fore.RED}Nenhuma meta encontrada para o vendedor {vendedor.user}.")
    
    input(f"\n{Fore.YELLOW}Pressione Enter para voltar ao menu...")



def vendedor_login(user, password):
    """Função de login para vendedores."""
    clear_terminal()
    try:
        # Tenta buscar o vendedor pelo nome de usuário
        vendedor = User.get(User.user == user)
        
        # Hash da senha fornecida para comparação
        hashed_password = hash_password(password)

        # Compara a senha hashada com a armazenada no banco de dados
        if vendedor.password == hashed_password:
            print(f"{Fore.GREEN}Login bem-sucedido! Bem-vindo, {user.capitalize()}!")
            vendedor_menu(vendedor)
        else:
            print(f"{Fore.RED}Senha incorreta. Tente novamente.")
    
    except User.DoesNotExist:
        print(f"{Fore.RED}Usuário não encontrado.")
    except Exception as e:
        print(f"{Fore.RED}Ocorreu um erro durante o login: {e}")

def vendedor_menu(vendedor):
    """Menu principal para o vendedor após login."""
    while True:
        clear_terminal()
        print(f"{Fore.YELLOW}=== Menu do Vendedor ===")
        print(f"Vendedor: {vendedor.user}")
        print(f"{Fore.CYAN}1. Adicionar Relatório de Vendas")
        print(f"{Fore.CYAN}2. Ver Progresso da Meta")
        print(f"{Fore.CYAN}3. Sair\n")
        
        escolha = input(f"{Fore.RESET}Escolha uma opção: ")

        if escolha == '1':
            add_relatorio(vendedor)
        elif escolha == '2':
            ver_progresso_vendedor(vendedor)  # Chama a função para ver o progresso do vendedor
        elif escolha == '3':
            print(f"{Fore.GREEN}Saindo...")
            break
        else:
            print(f"{Fore.RED}Escolha inválida. Tente novamente.")


def add_relatorio(vendedor):
    """Adiciona um relatório de vendas para o vendedor logado e atualiza a meta."""
    clear_terminal()
    print(f"{Fore.YELLOW}=== Adicionar Relatório de Vendas ===")
    
    total_vendas = Decimal(input(f"{Fore.CYAN}Digite o total de vendas: "))
    meta_vendas = Decimal(input(f"{Fore.CYAN}Digite a meta de vendas: "))
    cep = input(f"{Fore.CYAN}Digite o CEP para verificação: ")

    print(f"{Fore.YELLOW}Verificando CEP...")
    if get_cep(cep):
        try:
            # Adiciona o relatório de vendas
            Relatorio.create_relatorio(
                user=vendedor,
                total_vendas=total_vendas,
                meta_vendas=meta_vendas,
                data_cep=cep
            )

            # Atualiza o progresso da meta do mês
            meta_atual = Meta.get_or_none(Meta.user == vendedor, Meta.mes == 'Setembro')
            if meta_atual and not meta_atual.meta_batida:
                vendas_totais = Relatorio.select(fn.SUM(Relatorio.total_vendas)).where(Relatorio.user == vendedor).scalar()
                
                if vendas_totais >= meta_atual.meta_vendas:
                    meta_atual.meta_batida = True
                    meta_atual.pontuacao += 1
                    meta_atual.save()
                    print(f"{Fore.GREEN}Meta batida! Parabéns!")
                else:
                    progresso = (vendas_totais / meta_atual.meta_vendas) * 100
                    print(f"Progresso da meta: {Fore.BLUE}[{'#' * int(progresso // 10)}{'-' * (10 - int(progresso // 10))}] {progresso:.2f}%")
            
            input(f"{Fore.GREEN}Relatório adicionado com sucesso!")
        
        except Exception as e:
            print(f"{Fore.RED}Erro ao adicionar relatório: {e}")
    else:
        print(f"{Fore.RED}CEP inválido. Relatório não adicionado.")
    
    input(f"{Fore.YELLOW}Pressione Enter para voltar ao menu...")

