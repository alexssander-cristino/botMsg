import csv
import json
import re
import time
from datetime import datetime
from pathlib import Path

import pywhatkit
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "clientes.csv"
HISTORY_PATH = BASE_DIR / "historico.json"
PROFILE_PATH = BASE_DIR / "perfil_whatsapp"
DELAY_SECONDS = 20  # ajuste com prudência; não garante evitar bloqueios


def phone_digits(value):
    return re.sub(r"\D", "", value or "")


def load_history():
    if not HISTORY_PATH.exists():
        return {}
    try:
        return json.loads(HISTORY_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def save_history(history):
    HISTORY_PATH.write_text(
        json.dumps(history, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def build_message(company, contact):
    greeting = f"Olá, {contact}, tudo bem?" if contact else "Olá, tudo bem?"
    company_part = f" para a {company}" if company else " para sua empresa"
    return (
        f"{greeting}\n\n"
        "Meu nome é Alex e trabalho com desenvolvimento de sites e sistemas "
        "personalizados para empresas, criando soluções digitais de acordo "
        "com as necessidades de cada negócio, com foco em organização, "
        "eficiência e otimização de processos.\n\n"
        f"Gostaria de me colocar à disposição para conversar e entender se "
        f"alguma solução digital pode agregar valor{company_part}.\n\n"
        "Fico à disposição!\n\n"
        "Atenciosamente,\n"
        "Alex\n\n"
        "Se não quiser receber novas mensagens, é só me avisar."
    )


def read_contacts():
    if not CSV_PATH.exists():
        raise SystemExit(f"Não encontrei o arquivo: {CSV_PATH}")
    with CSV_PATH.open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        expected = {"empresa", "contato", "telefone", "autorizou"}
        if not reader.fieldnames or not expected.issubset(reader.fieldnames):
            raise SystemExit(
                "O clientes.csv precisa ter as colunas: "
                "empresa,contato,telefone,autorizou"
            )
        return list(reader)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Automatiza o WhatsApp Web com uma sessão local do navegador."
    )
    parser.add_argument(
        "--enviar",
        action="store_true",
        help="Confirma o envio real. Sem esta opção, apenas lista os contatos.",
    )
    parser.add_argument(
        "--campanha",
        default="prospeccao-01",
        help="Nome da campanha usado para evitar duplicação.",
    )
    parser.add_argument(
        "--limite",
        type=int,
        default=0,
        help="Limite de envios (0 = todos os elegíveis).",
    )
    args = parser.parse_args()

    history = load_history()
    contacts = read_contacts()
    eligible = []

    for row in contacts:
        company = (row.get("empresa") or "").strip()
        contact = (row.get("contato") or "").strip()
        phone = phone_digits(row.get("telefone"))
        consent = (row.get("autorizou") or "").strip().lower()

        if consent not in {"sim", "s", "yes", "true", "1"}:
            print(f"[IGNORADO] {company or phone}: autorização não marcada.")
            continue
        if not company or len(phone) < 12 or len(phone) > 15:
            print(f"[IGNORADO] Dados inválidos: {company} / {phone}")
            continue

        key = f"{args.campanha}:{phone}"
        if history.get(key, {}).get("status") in {"aberto_whatsapp", "enviado_manual"}:
            print(f"[DUPLICADO] {company} já foi processada nesta campanha.")
            continue

        eligible.append({
            "empresa": company,
            "contato": contact,
            "telefone": phone,
            "key": key,
            "mensagem": build_message(company, contact),
        })

    if not eligible:
        print("Nenhum contato elegível. Confira clientes.csv e a coluna autorizou.")
        return

    print(f"\nContatos elegíveis: {len(eligible)}")
    for item in eligible:
        print(f"- {item['empresa']} | {item['telefone']}")

    if not args.enviar:
        print("\nSIMULAÇÃO: nada foi aberto nem enviado.")
        print("Revise os contatos e execute novamente com --enviar.")
        return

    print(
        "\nO navegador será aberto. Na primeira execução, leia o QR Code "
        "do WhatsApp Web com seu celular."
    )
    print(
        "O bot abre a conversa e preenche a mensagem; confira e pressione "
        "ENVIAR manualmente em cada conversa."
    )
    print("Não é um disparador autônomo: o envio manual ajuda a revisar cada mensagem.")

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_PATH),
            headless=False,
            viewport={"width": 1280, "height": 900},
            args=["--start-maximized"],
        )
        page = context.pages[0] if context.pages else context.new_page()
        page.goto("https://web.whatsapp.com/", wait_until="domcontentloaded")

        try:
            page.get_by_role("textbox", name=re.compile("Pesquisar|Search", re.I)).wait_for(
                timeout=120_000
            )
        except PlaywrightTimeoutError:
            print("Não consegui confirmar o login no WhatsApp Web. Verifique o navegador.")
            context.close()
            return

        count = 0
        for item in eligible:
            if args.limite and count >= args.limite:
                break

            phone = item["telefone"]
            company = item["empresa"]
            message = item["mensagem"]

            print(f"\nAbrindo conversa: {company} ({phone})")
            url = f"https://web.whatsapp.com/send?phone={phone}"
            page.goto(url, wait_until="domcontentloaded")

            try:
                # Wait for the message composer; WhatsApp Web UI can change.
                composer = page.locator(
                    'footer [contenteditable="true"][role="textbox"]'
                ).last
                composer.wait_for(timeout=45_000)
                composer.fill(message)
                print("Mensagem preenchida. Revise e pressione Enter/Enviar no navegador.")
                history[item["key"]] = {
                    "status": "aberto_whatsapp",
                    "empresa": company,
                    "telefone": phone,
                    "data": datetime.now().isoformat(timespec="seconds"),
                }
                save_history(history)
                input("Depois de enviar manualmente (ou cancelar), pressione Enter aqui para continuar...")
                count += 1
                time.sleep(DELAY_SECONDS)
            except PlaywrightTimeoutError:
                print(
                    "Não encontrei o campo de mensagem. O WhatsApp Web pode ter mudado "
                    "ou o número pode não estar disponível."
                )
                history[item["key"]] = {
                    "status": "falha_abrir",
                    "empresa": company,
                    "telefone": phone,
                    "data": datetime.now().isoformat(timespec="seconds"),
                }
                save_history(history)

        context.close()
    print("\nFinalizado. Consulte historico.json e revise os envios manualmente.")


if __name__ == "__main__":
    main()
