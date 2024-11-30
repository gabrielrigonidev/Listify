# Listify - Gerenciador de Tarefas  

**Bem-vindo ao Listify!**  
Este projeto é um gerenciador de tarefas desenvolvido como parte de um processo seletivo para a posição de desenvolvedor web. A aplicação permite criar, visualizar, editar, excluir e organizar tarefas, oferecendo funcionalidades personalizadas como contagem de tarefas urgentes e de alto custo, tudo com foco na usabilidade e uma interface intuitiva.  

<div align="center">
<br>
   <p>Tecnologias utilizadas:</p>
  <img align="center" src="https://skillicons.dev/icons?i=python,django,tailwind,sqlite">
</div>

## Funcionalidades  

### 🔧 **Gerenciamento de Tarefas**  
- **Adicionar Tarefa**: Criação de tarefas com nome, custo e data limite.  
- **Editar Tarefa**: Modificação de tarefas existentes, com validação para evitar nomes duplicados.  
- **Excluir Tarefa**: Remoção de tarefas com confirmação prévia.  

### 📋 **Organização e Navegação**  
- Reorganização de tarefas com botões para subir ou descer na ordem de exibição.  
- Exibição de tarefas de **alto custo** (≥ R$ 1.000,00) com destaque visual.  
- Contador dinâmico de tarefas **urgentes** (com prazo próximo) e de **alto custo** na barra de navegação.  

### 🔒 **Autenticação e Segurança**  
- Sistema de login com validação de credenciais e armazenamento seguro da senha (hashing).  
- Controle de sessão para garantir que apenas usuários autenticados acessem suas tarefas.  
- Logout com confirmação e mensagens de feedback para o usuário.  

### 💡 **Destaques Visuais e Usabilidade**  
- Interface estilizada com **Tailwind CSS**, garantindo um design moderno e responsivo.  
- Mensagens de sucesso, erro ou aviso para feedback imediato ao usuário.  

---

## Como Rodar o Projeto  

1. **Clone o Repositório**:  
   ```bash
   git clone https://github.com/seu-usuario/listify.git
   cd listify

2. **Crie e Ative um Ambiente Virtual e instale as dependências::**:  
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   pip install -r requirements.txt

3. **Aplique as Migrações:**:  
   ```bash
   python manage.py migrate

4. **Inicie o Servidor Local:**:  
   ```bash
   python manage.py runserver
   # Acesse em http://127.0.0.1:8000/

---

## Autor  

**[Gabriel Rigoni]**  
Desenvolvedor apaixonado por criar soluções eficientes e amigáveis para o usuário. Este projeto foi desenvolvido como parte de um processo seletivo, demonstrando habilidades em Python, Django, Tailwind CSS e banco de dados SQLite.  

- [LinkedIn](https://www.linkedin.com/in/gabriel-rigoni-martins/)  
- [Email](rigonigabriel12@gmail.com)  

Sinta-se à vontade para entrar em contato para discutir este projeto ou futuras oportunidades!

