# WhatsApp Prospect Bot

**Automação de prospecção comercial com Python + WhatsApp Web**

Uma ferramenta para organizar contatos comerciais, personalizar mensagens e facilitar o processo de prospecção pelo WhatsApp Web, utilizando Python e Playwright — sem necessidade de integrar a API oficial do WhatsApp.

---

## Sobre o projeto

O WhatsApp Prospect Bot automatiza etapas repetitivas da prospecção comercial, permitindo trabalhar com uma lista de empresas e contatos através de um arquivo CSV.

O sistema abre as conversas pelo número de telefone, prepara mensagens personalizadas e mantém um histórico por campanha para ajudar a evitar o reprocessamento de contatos.

### Principais recursos

- **Importação de contatos:** carregamento de empresas e telefones através de CSV.
- **Mensagens personalizadas:** utiliza o nome do contato e da empresa no texto.
- **WhatsApp Web:** acessa conversas pela interface web, sem exigir que o contato esteja salvo na agenda.
- **Modo de simulação:** permite conferir a lista antes de iniciar a automação.
- **Controle de campanhas:** identifica a campanha executada pelo usuário.
- **Histórico local:** registra contatos processados para ajudar a evitar duplicidades dentro da mesma campanha.
- **Filtro de autorização:** processa somente contatos marcados como autorizados.
- **Limite de execução:** permite restringir a quantidade de contatos processados em uma execução.
- **Perfil persistente do navegador:** facilita manter a sessão do WhatsApp Web entre execuções.

---

## Tecnologias utilizadas

| Tecnologia | Finalidade |
|---|---|
| Python | Lógica principal da aplicação |
| Playwright | Automação do navegador |
| Chromium | Navegador utilizado na automação |
| CSV | Armazenamento da lista de contatos |
| JSON | Registro local do histórico |

---

## Estrutura do projeto

```text
bot-whatsapp/
├── bot.py
├── clientes.csv
├── requirements.txt
├── .gitignore
├── README.md
├── historico.json
└── perfil_whatsapp/
```

Os nomes dos arquivos de histórico e da pasta de perfil podem variar conforme a implementação atual do código.

---

## Requisitos

Antes de começar, você precisa ter:

- Python instalado no Windows.
- pip disponível no terminal.
- Conexão com a internet.
- Uma conta do WhatsApp com acesso ao WhatsApp Web.
- Os arquivos do projeto extraídos em uma pasta local.

---

## Instalação

### 1. Abra o terminal na pasta do projeto

No PowerShell, navegue até a pasta em que está o arquivo `bot.py`.

### 2. Crie o ambiente virtual

```powershell
py -m venv .venv
```

### 3. Ative o ambiente virtual

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Instale as dependências

```powershell
pip install -r requirements.txt
```

### 5. Instale o Chromium para o Playwright

```powershell
python -m playwright install chromium
```

Pronto! O ambiente está preparado para executar o projeto.

---

## Configuração dos contatos

Os contatos são cadastrados no arquivo `clientes.csv`.

### Exemplo

```csv
empresa,contato,telefone,autorizou
Empresa Exemplo,João,5547999990001,sim
Comércio Modelo,Maria,5547999990002,sim
Negócio Demonstrativo,Pedro,5547999990003,nao
```

### Campos disponíveis

| Campo | Descrição |
|---|---|
| `empresa` | Nome da empresa |
| `contato` | Nome da pessoa que receberá a mensagem |
| `telefone` | Número com código do país, DDD e telefone |
| `autorizou` | Define se o contato pode ser processado |

**Formato recomendado para telefones:** `55 + DDD + número`, utilizando somente dígitos.

O campo `autorizou` deve conter `sim` para que o contato seja elegível. Contatos sem autorização devem permanecer fora da prospecção.

Os números do exemplo são fictícios e devem ser substituídos por contatos reais que tenham autorizado o recebimento.

---

## Como executar

### Modo de simulação

Antes de abrir o WhatsApp, confira os contatos elegíveis:

```powershell
python bot.py --campanha prospeccao-01
```

Esse comando executa o modo de simulação, sem iniciar o envio de mensagens.

### Iniciar a automação

Para começar a processar os contatos pelo WhatsApp Web:

```powershell
python bot.py --enviar --campanha prospeccao-01
```

Para testar com apenas um contato:

```powershell
python bot.py --enviar --campanha prospeccao-01 --limite 1
```

### Primeiro acesso ao WhatsApp Web

1. Execute o comando de automação.
2. Aguarde o Chromium abrir.
3. Se necessário, escaneie o QR Code com o WhatsApp do celular.
4. Aguarde a conversa do contato ser aberta.
5. Confira o destinatário e o conteúdo da mensagem.
6. Envie a mensagem manualmente pelo WhatsApp Web.
7. Confirme no terminal para continuar o processamento.

**Importante:** a versão atual prepara as mensagens, mas não clica automaticamente no botão de envio. A confirmação no terminal permite avançar para o próximo contato.

---

## Personalização das mensagens

O bot monta a mensagem utilizando os dados de cada contato.

Exemplo ilustrativo:

```text
Olá, João, tudo bem?

Meu nome é Alex e trabalho com desenvolvimento de sites e
sistemas personalizados para empresas, criando soluções
digitais de acordo com as necessidades de cada negócio,
com foco em organização, eficiência e otimização de processos.

Gostaria de me colocar à disposição para conversar e entender
se alguma solução digital pode agregar valor à Empresa Exemplo.

Fico à disposição!

Atenciosamente,
Alex

Se não quiser receber novas mensagens, é só me avisar.
```

A mensagem pode ser adaptada para diferentes segmentos, mantendo uma abordagem profissional, transparente e respeitosa.

---

## Como funcionam as campanhas

Cada execução pode receber um identificador de campanha.

Exemplo:

```powershell
python bot.py --enviar --campanha prospeccao-01
```

Outra campanha:

```powershell
python bot.py --enviar --campanha prospeccao-02
```

O histórico é utilizado para ajudar a impedir que os mesmos contatos sejam processados novamente na mesma campanha.

**Atenção:** o histórico registra o processamento realizado pelo bot, não necessariamente a confirmação de que a mensagem foi entregue. Como o envio é manual, confirme que a mensagem foi realmente enviada antes de considerar o contato concluído.

Criar uma campanha com outro nome pode fazer com que contatos antigos sejam processados novamente. Confira a lista antes de iniciar uma nova campanha.

---

## Boas práticas

- Revise os números e os nomes antes de iniciar.
- Utilize mensagens relevantes para cada empresa.
- Faça uma simulação antes da execução real.
- Comece com poucos contatos para validar o funcionamento.
- Não reutilize campanhas sem conferir o histórico.
- Respeite pedidos para não receber novas mensagens.
- Entre em contato somente com pessoas que autorizaram a prospecção.
- Não utilize listas compradas, spam ou práticas que violem as regras do WhatsApp.

A automação via navegador não é uma integração oficial com o WhatsApp e pode parar de funcionar caso a interface seja alterada. O uso também pode estar sujeito a restrições da plataforma.

---

## Solução de problemas

### O Chromium não abre

Execute novamente a instalação do navegador:

```powershell
python -m playwright install chromium
```

### O WhatsApp solicita autenticação

Escaneie o QR Code com o celular e aguarde o carregamento completo das conversas.

### O contato não é encontrado

Verifique se o número está correto, possui código do país e DDD e está registrado no WhatsApp.

### O contato é ignorado

Confira o valor de `autorizou` no CSV e verifique o histórico da campanha.

### O bot não inicia

Certifique-se de estar na pasta correta, com o ambiente virtual ativado e as dependências instaladas.

---

## Segurança e privacidade

- Mantenha a sessão do navegador protegida.
- Não compartilhe a pasta de perfil do WhatsApp.
- Não publique arquivos com dados pessoais de clientes.
- Não envie credenciais, tokens ou informações privadas para repositórios públicos.
- Utilize os dados dos contatos somente para a finalidade autorizada.

---

## Roadmap

Possíveis melhorias para versões futuras:

- [ ] Interface gráfica para gerenciar campanhas.
- [ ] Editor de mensagens com variáveis personalizadas.
- [ ] Relatórios de contatos processados.
- [ ] Histórico com status de envio confirmado.
- [ ] Importação de planilhas Excel.
- [ ] Validação de números antes da execução.
- [ ] Agendamento de campanhas com limites configuráveis.
- [ ] Painel de acompanhamento de resultados.

*Os itens acima são ideias para futuras versões, não funcionalidades garantidas na versão atual.*

---

## Licença

Projeto de automação local para uso comercial responsável. Defina uma licença específica antes de redistribuir ou publicar o código como software de código aberto.

---

**Desenvolvido por Alex**  
*Python · Playwright · WhatsApp Web*
