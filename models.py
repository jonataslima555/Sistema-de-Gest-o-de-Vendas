import hashlib
from peewee import *
from os import getenv
from dotenv import load_dotenv

load_dotenv()

DB_NAME = getenv('DB_NAME')

db = SqliteDatabase(DB_NAME)


class BaseModel(Model):
    class Meta:
        database = db


def hash_password(password):
    """Hash a password usando SHA-256."""
    hashed = hashlib.sha256(password.encode()).hexdigest()
    return hashed


class Admin(BaseModel):
    user = CharField(unique=True)
    password = CharField()
    cpf = CharField(unique=True)
    type = DecimalField(default=1)

    @classmethod
    def create_account(cls, user, password, cpf):
        hashed_password = hash_password(password)

        try:
            with db.atomic():
                cls.create(
                    user=user,
                    password=hashed_password,  # Armazenando a senha com hash
                    cpf=cpf
                )
                print(f'Usuario: {user.capitalize()} criado com sucesso!')
        except IntegrityError:
            print('Erro ao criar usuario...')


class User(BaseModel):
    user = CharField(unique=True)
    password = CharField()
    cpf = CharField(unique=True)
    type = DecimalField(default=0)

    @classmethod
    def create_account(cls, user, password, cpf):
        hashed_password = hash_password(password)
        try:
            with db.atomic():
                cls.create(
                    user=user,
                    password=hashed_password,  # Armazenando a senha com hash
                    cpf=cpf
                )
                print(f'Usuario: {user.capitalize()} criado com sucesso!')
        except IntegrityError:
            print('Erro ao criar usuario...')


class Relatorio(BaseModel):
    user = ForeignKeyField(User, backref='relatorios')
    total_vendas = DecimalField(default=0)
    meta_vendas = DecimalField(default=10)
    data_cep = CharField()

    @classmethod
    def create_relatorio(cls, user, total_vendas, meta_vendas, data_cep):
        try:
            with db.atomic():
                cls.create(
                    user=user,
                    total_vendas=total_vendas,
                    meta_vendas=meta_vendas,
                    data_cep=data_cep
                )
                print(f'Relatorio para {user.user.capitalize()} criado com sucesso!')
        except IntegrityError:
            print('Erro ao criar relatorio...')


class Meta(BaseModel):
    user = ForeignKeyField(User, backref='metas')  # Relaciona a meta ao vendedor
    meta_vendas = DecimalField()  # Valor da meta de vendas
    mes = CharField()  # Mês da meta (pode ser string como 'Setembro' ou '2024-09')
    pontuacao = IntegerField(default=0)  # Pontuação quando a meta é batida
    meta_batida = BooleanField(default=False)  # Verifica se a meta foi batida
    valor = DecimalField(default=0)  # Valor atual de vendas atingidas pelo vendedor

    @classmethod
    def criar_meta(cls, user, meta_vendas, mes):
        """Cria uma meta de vendas para o vendedor"""
        try:
            with db.atomic():
                cls.create(
                    user=user,
                    meta_vendas=meta_vendas,
                    mes=mes
                )
                print(f"Meta criada para {user.user.capitalize()}!")
        except IntegrityError:
            print("Erro ao criar meta.")

    @classmethod
    def atualizar_meta(cls, user, vendas):
        """Atualiza o valor de vendas da meta e verifica se foi batida"""
        meta = cls.select().where((cls.user == user) & (cls.meta_batida == False)).first()
        if meta:
            meta.valor += vendas
            if meta.valor >= meta.meta_vendas:
                meta.meta_batida = True
                meta.pontuacao += 1
                print(f"Meta batida por {user.user.capitalize()}!")
            meta.save()
        else:
            print(f"Nenhuma meta em aberto encontrada para {user.user.capitalize()}.")

    @classmethod
    def exibir_progress_bar(cls, user):
        """Exibe a barra de progresso da meta do vendedor"""
        meta = cls.select().where((cls.user == user) & (cls.meta_batida == False)).first()
        if meta:
            progresso = (meta.valor / meta.meta_vendas) * 100
            print(f"Progresso da meta para {user.user.capitalize()}: {progresso:.2f}%")
        else:
            print(f"Nenhuma meta em aberto para {user.user.capitalize()}.")

# Criando as tabelas
try:
    with db.atomic():
        db.create_tables([Admin, User, Relatorio, Meta])
        #print('Tabelas criadas com sucesso!')
        Admin.create_account('admin','123','087')
except Exception as e:
    print(f'Erro ao criar tabelas: {e}')
