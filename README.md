# Bot de WhatsApp Web (sem API oficial)

Este projeto usa Python + Playwright para abrir conversas no WhatsApp Web e preencher a mensagem personalizada. **Por segurança e para reduzir envios acidentais, o usuário revisa e envia manualmente cada mensagem.** Não usa a API oficial.

> Atenção: automação não oficial pode falhar quando o WhatsApp Web muda e pode gerar restrições na conta. Não existe intervalo garantido que evite bloqueios. Use somente para contatos que autorizaram receber mensagens; não use listas compradas nem faça spam.

## Requisitos

- Windows 10/11
- Python 3.10+
- WhatsApp instalado no celular e conta ativa

## Instalação (PowerShell)

```powershell
cd bot_whatsapp_web
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m playwright install chromium
```

## Preparar a lista

Edite `clientes.csv`:

```csv
empresa,contato,telefone,autorizou
Empresa Exemplo,Maria,5547999991111,sim
```

Telefone com código do país + DDD + número. Marque `sim` apenas se a pessoa autorizou receber esse tipo de mensagem. O exemplo vem com `nao` para evitar envio acidental.

## Simular

```powershell
python bot.py --campanha prospeccao-01
```

Não abre o WhatsApp nem envia nada.

## Executar com revisão manual

```powershell
python bot.py --enviar --campanha prospeccao-01 --limite 1
```

Na primeira execução, abre o Chromium. Escaneie o QR Code com WhatsApp > Dispositivos conectados. O bot abre cada conversa e preenche a mensagem. Confira o destinatário e pressione enviar no WhatsApp Web; depois volte ao terminal e pressione Enter para continuar.

## Mensagem usada

Olá, [contato], tudo bem?

Meu nome é Alex e trabalho com desenvolvimento de sites e sistemas personalizados para empresas, criando soluções digitais de acordo com as necessidades de cada negócio, com foco em organização, eficiência e otimização de processos.

Gostaria de me colocar à disposição para conversar e entender se alguma solução digital pode agregar valor à [empresa].

Fico à disposição!

Atenciosamente,
Alex

Se não quiser receber novas mensagens, é só me avisar.

## Limitações importantes

- Não é integração oficial, então pode quebrar quando a interface mudar.
- O envio não é totalmente autônomo: a confirmação manual é intencional.
- O histórico registra conversas abertas, não confirma que a mensagem foi realmente enviada.
- Para marcar o envio como concluído, revise o histórico e não reutilize o mesmo identificador de campanha para contornar pedidos de descadastro.
- Se a pessoa pedir para não ser contatada, remova-a da lista e mantenha um registro de supressão.
