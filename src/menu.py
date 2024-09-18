from src.admin import home_login
from src.sale import vendedor_login
def menu():
    user = input('Admin [1]\nVendedor [2]\n: ')
    if user == '1':
        admin_user = input('Digite o nome de usuário: ')
        admin_password = input('Digite a senha: ')
        return home_login(admin_user, admin_password)
    elif user == '2':
        sale_user = input('Digite o nome de usuário: ')
        sale_password = input('Digite a senha: ')
        return vendedor_login(sale_user, sale_password)
    else:
        print('Digite 1 ou 2...')
        return menu()
