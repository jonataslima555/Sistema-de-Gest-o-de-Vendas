# Sistema de Gestão de Vendas

Este projeto é um sistema de gestão de vendas com funcionalidades voltadas tanto para **administradores** quanto para **vendedores**. Ele permite que administradores gerenciem vendedores, estabeleçam metas de vendas e acompanhem o progresso individual dos vendedores. Vendedores podem adicionar relatórios de vendas, acompanhar o seu progresso e visualizar as metas batidas.

## Funcionalidades Principais

### Para Administradores

- **Criação de Contas de Vendedores**: O administrador pode criar contas para novos vendedores.
- **Definição de Metas**: O administrador pode criar metas de vendas para os vendedores, atribuindo metas específicas para cada um.
- **Acompanhamento de Metas**: O administrador pode visualizar o progresso dos vendedores, incluindo uma barra de progresso mostrando o quanto falta para atingir a meta.
- **Visualização de Relatórios**: O administrador pode consultar os relatórios de vendas de cada vendedor, com dados sobre vendas totais e metas alcançadas.

### Para Vendedores

- **Login Seguro**: Vendedores podem acessar o sistema com um login seguro.
- **Relatórios de Vendas**: Vendedores podem adicionar seus relatórios de vendas, informando o total de vendas realizadas e outros detalhes.
- **Acompanhamento de Metas**: Vendedores podem visualizar suas metas e acompanhar o progresso por meio de uma barra de progresso, sabendo exatamente o quanto falta para bater a meta.
- **Feedback sobre Metas Batidas**: O vendedor pode ver quantas metas já foram atingidas, ganhando pontuação por metas concluídas.

## Tecnologias Utilizadas

- **Python**: Linguagem principal utilizada no desenvolvimento do sistema.
- **Peewee**: Utilizada como ORM (Object-Relational Mapping) para manipulação de banco de dados.
- **SQLite**: Banco de dados local utilizado para armazenar usuários, relatórios e metas de vendas.
- **Colorama**: Biblioteca usada para estilização de texto no terminal, proporcionando uma experiência visual mais rica.
- **Requests**: Usada para fazer requisições HTTP, por exemplo, para a verificação de CEP através de APIs externas.
- **Python-dotenv**: Utilizada para carregar variáveis de ambiente, como a chave da API utilizada para consultar CEPs.

## Bibliotecas Utilizadas

As seguintes bibliotecas foram usadas no projeto e estão listadas no arquivo `requirements.txt`: (pip install requirements.txt)

`certifi==2024.8.30`

`charset-normalizer==3.3.2`

`colorama==0.4.6`

`idna==3.10`

`peewee==3.17.6`

`python-dotenv==1.0.1`

`requests==2.32.3`

`urllib3==2.2.3`

## Diferenciais

- **Gestão de Metas de Vendas**: A possibilidade de atribuir metas personalizadas para cada vendedor e acompanhar seu desempenho em tempo real, tanto para administradores quanto para os vendedores.
- **Barra de Progresso**: Feedback visual tanto para administradores quanto para vendedores sobre o progresso das metas.
- **Sistema Seguro**: Login e armazenamento seguro de senhas utilizando hashing com SHA-256.
- **Integração com API Externa**: Verificação de CEPs em tempo real para garantir que os endereços sejam válidos.
- **Feedback Interativo**: Sistema de cores no terminal (via Colorama) para melhorar a experiência do usuário.

## Instruções para Configuração e Execução

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/seu_usuario/sistema-gestao-vendas.git
   cd sistema-gestao-vendas
   ```

`python -m venv venv `

Linux/Mac `source venv/bin/activate  `

Windows `venv\Scripts\activate`

**Configure as variáveis de ambiente** :
Crie um arquivo `.env` na raiz do projeto e adicione a variável `API_KEY` com a chave da API para consulta de CEP:

API_KEY=sua_chave_api_aqui (https://api.invertexto.com/api-consulta-cep)
DB_NAME=database.db

**Execute o sistema** :

python main.py

Acesse o admin: 

username = admin

password = 123
