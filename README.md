# AssessorAI Client

Sistema de planejamento e gestão para mandatos parlamentares, desenvolvido em Django.

## Descrição

O AssessorAI Client é uma plataforma web que auxilia parlamentares na gestão e planejamento de seus mandatos, oferecendo ferramentas para:

- Cadastro e gerenciamento de informações do mandato
- Planejamento estratégico com análise de oportunidades e desafios
- Definição de objetivos e metas
- Gestão de equipe

## Tecnologias Utilizadas

- **Python 3.10+**
- **Django** - Framework web principal
- **django-crispy-forms** - Formulários estilizados
- **Tailwind CSS** - Framework CSS para estilização

## Estrutura do Projeto

```
assessorai-client/
├── core/                    # App principal
│   ├── models.py           # Modelos (Mandato, Planejamento, Objetivo)
│   ├── forms.py            # Formulários
│   ├── views.py            # Views
│   └── templates/          # Templates HTML
├── config/                 # Configurações do Django
├── theme/                  # App para temas e assets estáticos
└── static/                 # Arquivos estáticos
```

## Instalação e Execução

1. **Clone o repositório:**
```bash
git clone <url-do-repositorio>
cd assessorai-client
```

2. **Crie e ative um ambiente virtual:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Execute as migrações:**
```bash
python manage.py migrate
```

5. **Crie um superusuário (opcional):**
```bash
python manage.py createsuperuser
```

6. **Execute o servidor de desenvolvimento:**
```bash
python manage.py runserver
```

7. **Acesse o sistema:**
Abra seu navegador e vá para `http://localhost:8000`

## Funcionalidades

### Gestão de Mandato
- Cadastro de informações básicas do parlamentar
- Definição de casa legislativa, cargo e localização
- Configuração de perfil político

### Planejamento Estratégico
- Análise de oportunidades e ameaças
- Definição de temas prioritários
- Estabelecimento de objetivos anuais

### Objetivos e Metas
- Criação de objetivos específicos
- Acompanhamento de metas

## Desenvolvimento

### Estrutura de Temas
O projeto utiliza Tailwind CSS através do app `theme/`. Para compilar os estilos:

```bash
cd theme/static_src
npm install
npm run build
```

### Comandos Úteis

- `python manage.py populate_sample_data` - Popula dados de exemplo
- `python manage.py collectstatic` - Coleta arquivos estáticos
- `python manage.py shell` - Abre shell interativo do Django

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença [MIT](LICENSE).

## Contato

Para dúvidas ou sugestões, entre em contato através de [seu-email@exemplo.com].
