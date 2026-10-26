# WhatsApp Prospect Dashboard

Painel web para organizar contatos, gerenciar campanhas de prospecção e preparar mensagens personalizadas para envio manual pelo WhatsApp Web.

O projeto utiliza **Python, Flask, SQLite e Playwright**, com foco em organização, rastreabilidade e simplicidade de uso.

> **Importante:** o sistema não utiliza a API oficial do WhatsApp. A automação abre o WhatsApp Web e prepara a mensagem para revisão e envio manual. Não há garantia de compatibilidade permanente com o WhatsApp Web.

## Funcionalidades

- **Dashboard:** visão geral dos contatos, campanhas e atividades.
- **Gestão de contatos:** cadastro, edição e organização de potenciais clientes.
- **Importação de planilhas:** importação de contatos por arquivos CSV e Excel, conforme os formatos suportados pelo projeto.
- **Campanhas:** organização dos contatos e mensagens por campanha.
- **Mensagens personalizadas:** utilização de modelos com variáveis, como nome do contato e empresa.
- **Envio manual:** preparação da conversa e da mensagem no WhatsApp Web, com revisão antes do envio.
- **Histórico:** registro das atividades realizadas pelo sistema.
- **Relatórios:** acompanhamento dos contatos e resultados registrados.
- **Banco de dados local:** armazenamento persistente em SQLite.
- **Controle de opt-out:** possibilidade de marcar contatos que não desejam receber novas mensagens.

## Tecnologias

| Tecnologia | Finalidade |
|---|---|
| Python | Lógica e processamento |
| Flask | Aplicação web e rotas |
| SQLite | Armazenamento de dados |
| Playwright | Automação do navegador |
| HTML, CSS e JavaScript | Interface do painel |
| CSV e Excel | Importação de contatos |

## Requisitos

Antes de começar, instale:

- Python 3.10 ou superior, conforme a compatibilidade das dependências.
- Google Chrome ou Chromium, quando necessário para o navegador automatizado.
- WhatsApp com uma conta ativa.
- Acesso à internet para utilizar o WhatsApp Web.

## Instalação

### 1. Baixe e extraia o projeto

Extraia os arquivos para uma pasta local. Abra o terminal nessa pasta.

### 2. Crie um ambiente virtual

No Windows, usando PowerShell:

```powershell
py -m venv .venv
```

Ative o ambiente:

```powershell
.\.venv\Scripts\Activate.ps1
```

Se o PowerShell bloquear a ativação, você pode executar os comandos usando o Python do ambiente virtual diretamente.

### 3. Instale as dependências

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Instale o navegador do Playwright

```powershell
python -m playwright install chromium
```

### 5. Inicie o sistema

```powershell
python app.py
```

Abra o endereço local indicado no terminal. Se a aplicação utilizar a porta padrão configurada, acesse:

http://127.0.0.1:5000

> Execute os comandos a partir da pasta do projeto e mantenha o terminal aberto enquanto estiver utilizando o painel.

## Banco de dados SQLite

O projeto utiliza SQLite, um banco de dados que funciona localmente, sem precisar instalar ou administrar um servidor separado.

O arquivo `.db` armazena os dados persistentes da aplicação, como contatos, campanhas, modelos de mensagens e registros de atividades, de acordo com as tabelas implementadas.

### Cuidados importantes

- Não exclua o arquivo do banco enquanto estiver utilizando o sistema.
- Faça cópias de segurança antes de atualizar o projeto.
- Evite abrir o mesmo banco simultaneamente por processos que possam causar conflitos.
- Se o banco for criado automaticamente pela aplicação, ele normalmente aparecerá no caminho configurado no código.
- O histórico anterior em JSON só será migrado se essa funcionalidade estiver implementada e o arquivo antigo estiver disponível no local esperado.

**Atenção:** o nome e o caminho exatos do arquivo do banco dependem da configuração da aplicação. Confira o código de inicialização antes de mover ou excluir arquivos.

## Importação de contatos

Prepare uma planilha com os campos aceitos pelo sistema. Um exemplo de CSV:

```csv
empresa,contato,telefone,autorizou
Empresa Exemplo,João,5547999999999,sim
Loja Modelo,Maria,5547988888888,sim
```

Recomendações:

- Utilize o código do país e o DDD no telefone.
- Verifique se os números estão corretos.
- Remova contatos duplicados antes de importar.
- Utilize o campo de autorização de acordo com as regras de consentimento implementadas no sistema.
- Não importe listas compradas ou contatos que não esperam receber suas mensagens.

O formato acima é um exemplo. Os nomes das colunas devem corresponder aos campos aceitos pela versão instalada.

## Modelos de mensagens

Utilize modelos para padronizar as abordagens e personalizar as mensagens de acordo com os dados disponíveis.

Exemplo ilustrativo:

```text
Olá, {contato}! Tudo bem?

Sou responsável pela {empresa}. Gostaria de apresentar
uma solução que pode ser interessante para o seu negócio.

Se tiver interesse, posso enviar mais informações.
Caso não queira receber novas mensagens, é só me avisar.
```

Os nomes das variáveis precisam corresponder aos identificadores suportados pela aplicação.

## Fluxo de uma campanha

1. Cadastre ou importe os contatos.
2. Revise os telefones e as autorizações.
3. Crie uma campanha.
4. Selecione ou prepare um modelo de mensagem.
5. Revise a mensagem personalizada antes de cada envio.
6. Abra a conversa no WhatsApp Web.
7. Confira o destinatário e envie manualmente.
8. Registre o resultado no painel, quando disponível.
9. Consulte o histórico e os relatórios para acompanhar a campanha.

O sistema deve distinguir entre uma mensagem apenas preparada, uma mensagem efetivamente enviada e uma resposta recebida. Abrir uma conversa não comprova que a mensagem foi enviada.

## Boas práticas

- Envie mensagens relevantes e personalizadas.
- Contate apenas pessoas que tenham autorizado ou que legitimamente esperem esse contato, respeitando a legislação aplicável.
- Identifique claramente quem está entrando em contato.
- Respeite imediatamente os pedidos para não receber novas mensagens.
- Evite abordagens repetitivas, listas indiscriminadas e práticas que possam ser consideradas spam.
- Faça testes com poucos contatos antes de executar uma campanha maior.
- Não compartilhe o perfil do navegador, cookies ou sessões autenticadas.

A automação não oficial pode parar de funcionar após mudanças no WhatsApp Web e pode resultar em restrições da conta. O uso do projeto é de responsabilidade do operador.

## Solução de problemas

### O painel não inicia

Confira se o ambiente virtual está ativo e se as dependências foram instaladas:

```powershell
pip install -r requirements.txt
python app.py
```

Verifique também se a porta configurada já está sendo utilizada.

### O navegador não abre

Instale novamente o navegador do Playwright:

```powershell
python -m playwright install chromium
```

### O WhatsApp solicita autenticação

Abra o WhatsApp Web e faça a leitura do QR Code com o celular. Se o projeto utilizar um perfil persistente, a sessão poderá ser reutilizada enquanto permanecer válida.

### Os contatos não são importados

Confira os cabeçalhos da planilha, o formato do arquivo e a presença dos campos obrigatórios. Verifique também as mensagens de erro exibidas pelo painel ou terminal.

### Os dados parecem ter desaparecido

Confira o caminho do banco SQLite configurado na aplicação. Executar o projeto a partir de outra pasta ou alterar a configuração do banco pode fazer com que outro arquivo seja utilizado.

## Segurança e privacidade

- Mantenha o banco de dados e os arquivos de sessão protegidos.
- Não publique arquivos `.db`, cookies ou dados pessoais em repositórios públicos.
- Não compartilhe credenciais nem sessões autenticadas.
- Realize backups periódicos.
- Utilize os dados dos contatos somente para finalidades legítimas e compatíveis com a autorização recebida.

## Estrutura do projeto

A estrutura exata depende dos arquivos incluídos na versão instalada. Uma organização típica pode conter:

```text
whatsapp-prospect-dashboard/
├── app.py
├── bot.py
├── requirements.txt
├── templates/
├── static/
├── prospect.db
└── README.md
```

O arquivo do banco pode não existir antes da primeira inicialização caso seja criado automaticamente pela aplicação. A presença de cada pasta ou arquivo depende da implementação real do projeto.

## Licença

Defina uma licença antes de distribuir publicamente o projeto. Na ausência de uma licença explícita, não presuma que terceiros têm permissão para redistribuir ou modificar o código.

---

**WhatsApp Prospect Dashboard**  
Organização de contatos e campanhas com revisão humana antes do envio.
