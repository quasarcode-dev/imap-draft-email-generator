import imaplib
import os
from dotenv import load_dotenv

load_dotenv()

imap = imaplib.IMAP4_SSL(os.getenv("IMAP_HOST"), 993)
imap.login(os.getenv("IMAP_USER"), os.getenv("IMAP_PASS"))

status, mailboxes = imap.list()

print("\n📂 CARPETAS IMAP DISPONIBLES:\n")
for m in mailboxes:
    print(m.decode())

imap.logout()
