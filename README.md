# Setup do Projeto Livraria Django

Este arquivo contém todas as instruções necessárias para instalar, configurar e rodar o projeto em um único lugar.

## Requisitos

- Python 3.9+
- pip
- npm (instale o Node.js que já inclui o npm)
- Django 3.2+
- Node >= v18.13.0

## Passo a Passo de Instalação

### 1. Clonar o Repositório

Clone o repositório do projeto em sua máquina local:

```bash
git clone https://github.com/viniciusfelippetti/livraria.git
cd livraria
```

### 2. Criar Ambiente Virtual
Crie um ambiente virtual para isolar as dependências do projeto:
```bash
mkvirtualenv livraria
workon livraria
```

### 3. Instalar Dependências Python
Instale todas as dependências Python listadas no arquivo requirements.txt:
```bash
pip install -r requirements.txt
```

### 4. Instalar Template Gov.br
Certifique-se de que você tem o npm instalado. Então, instale o template:
```bash
npm install @govbr-ds/core
```

### 5. Configurar o Banco de Dados
Aplique as migrações para configurar o banco de dados:
```bash
python manage.py migrate
```

### 6. Importar Livros
Agora, importe os dados dos livros para o banco de dados com o seguinte comando:
```bash
python manage.py importar_livros
```

### 7. Rodar o Servidor
Após configurar o banco de dados e importar os livros, inicie o servidor de desenvolvimento Django:
```bash
python manage.py runserver
```
