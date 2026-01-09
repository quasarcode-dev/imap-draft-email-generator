# ───────────────── IMPORTACIONES ─────────────────

# Permite acceder a variables de entorno y operaciones del sistema
import os

# Biblioteca estándar para comunicación con servidores IMAP (correo)
import imaplib

# Permite construir correos MIME con múltiples partes (HTML / texto)
from email.mime.multipart import MIMEMultipart

# Permite crear contenido MIME de tipo texto o HTML
from email.mime.text import MIMEText

# Carga variables de entorno desde un archivo .env
from dotenv import load_dotenv

# Cliente oficial de Groq para consumir modelos LLM
from groq import Groq


# ───────────────── CARGA DE VARIABLES DE ENTORNO ─────────────────

# Carga automáticamente las variables definidas en el archivo .env
load_dotenv()


# ───────────────── CONFIGURACIÓN GENERAL ─────────────────

# Host del servidor IMAP (ej: imap.gmail.com, mail.example.com)
IMAP_HOST = os.getenv("IMAP_HOST", "imap.example.com")

# Usuario del correo que guardará los borradores
IMAP_USER = os.getenv("IMAP_USER", "user@example.com")

# Contraseña del correo IMAP
IMAP_PASS = os.getenv("IMAP_PASS", "password")

# API Key para Groq (modelo de lenguaje)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "your_api_key_here")

# Modo de prueba:
# True  → no llama al LLM, usa texto genérico
# False → llama a Groq y genera correos reales
DRY_RUN = False

# Inicializa el cliente de Groq con la API Key
client = Groq(api_key=GROQ_API_KEY)

# Archivo que contiene los correos a procesar (uno por línea)
EMAILS_FILE = "emails.txt"

# Carpeta donde se guardan borradores en TXT si falla IMAP
OUTPUT_DIR = "drafts_txt"

# Crea la carpeta de salida si no existe
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ───────────────── FIRMA DEL CORREO (HTML) ─────────────────

# Firma profesional en formato HTML
HTML_SIGNATURE = """
<table cellpadding="0" cellspacing="0" style="font-family: Arial, Helvetica, sans-serif;">
  <tr>
    <td>
      <strong>John Doe</strong><br>
      Software Consultant<br>
      Example Company
    </td>
  </tr>
  <tr>
    <td>
      🌐 <a href="https://example.com">example.com</a><br>
      ✉️ <a href="mailto:contact@example.com">contact@example.com</a>
    </td>
  </tr>
</table>
"""


# ───────────────── FIRMA DEL CORREO (TEXTO PLANO) ─────────────────

# Firma alternativa en texto plano (fallback)
TEXT_SIGNATURE = """
--
John Doe
Software Consultant
Example Company
https://example.com
contact@example.com
""".strip()


# ───────────────── FUNCIONES AUXILIARES ─────────────────

def extractDomain(email: str) -> str:
    """
    Extrae el dominio de un correo electrónico.
    Ejemplo: contacto@empresa.com → empresa.com
    """
    return email.split("@")[-1].lower()


def sanitizeFilename(email: str) -> str:
    """
    Convierte un correo en un nombre de archivo válido.
    Ejemplo: contacto@empresa.com → contacto_empresa_com
    """
    return email.replace("@", "_").replace(".", "_")


def mockEmailBody(email: str) -> str:
    """
    Genera un cuerpo de correo genérico.
    Se usa cuando DRY_RUN = True para pruebas.
    """
    domain = extractDomain(email)
    company = domain.split(".")[0].capitalize()

    return f"""
Hello,

My name is John Doe and I represent Example Company.

I am reaching out to {company} to explore potential collaboration
opportunities in custom software development and automation.

I would be happy to schedule a short, no-obligation call.

Kind regards,
""".strip()


def buildPrompt(email: str) -> str:
    """
    Construye el prompt que se envía al modelo de lenguaje.
    Define contexto, objetivos y restricciones del correo.
    """
    domain = extractDomain(email)
    company = domain.split(".")[0].capitalize()

    return f"""
My name is John Doe.
I represent Example Company.

I am contacting the business {company} ({domain})
to explore collaboration opportunities in custom software development.

Write a professional B2B outreach email addressed to {company}.

Restrictions:
- Professional and friendly tone
- Do not mention AI
- Do not include subject
- Do not include signature
"""


def generateEmailBody(email: str) -> str:
    """
    Genera el cuerpo del correo.
    Usa DRY_RUN o llama al modelo de Groq.
    """
    prompt = buildPrompt(email)

    # Muestra el prompt generado para depuración
    print("\n🧠 PROMPT GENERADO")
    print(prompt)

    # Si está en modo prueba, devuelve texto genérico
    if DRY_RUN:
        return mockEmailBody(email)

    # Llamada al modelo LLM de Groq
    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )

    # Acumula la respuesta completa
    fullResponse = ""

    # Lee la respuesta en streaming
    for chunk in completion:
        delta = chunk.choices[0].delta.content
        if delta:
            print(delta, end="", flush=True)
            fullResponse += delta

    return fullResponse.strip()


# ───────────────── GUARDADO EN TXT (FALLBACK) ─────────────────

def saveDraftTxt(email: str, body: str):
    """
    Guarda el correo como archivo TXT si falla IMAP.
    """
    filename = f"{OUTPUT_DIR}/draft_{sanitizeFilename(email)}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"TO: {email}\n")
        f.write("SUBJECT: Business Process Optimization\n\n")
        f.write(body)
        f.write("\n\n")
        f.write(TEXT_SIGNATURE)


# ───────────────── GUARDADO EN IMAP ─────────────────

def saveDraftImap(email: str, body: str):
    """
    Guarda el correo como borrador en el servidor IMAP.
    """
    # Crea el mensaje MIME
    msg = MIMEMultipart("alternative")

    # Define encabezados del correo
    msg["From"] = IMAP_USER
    msg["To"] = email
    msg["Subject"] = "Business Process Optimization"

    # Construye el cuerpo HTML
    htmlBody = f"""
    <html>
      <body>
        {body.replace("\n", "<br>")}
        <br><br>
        {HTML_SIGNATURE}
      </body>
    </html>
    """

    # Adjunta el HTML al mensaje
    msg.attach(MIMEText(htmlBody, "html"))

    # Conexión al servidor IMAP
    imap = imaplib.IMAP4_SSL(IMAP_HOST)

    # Autenticación
    imap.login(IMAP_USER, IMAP_PASS)

    # Guarda el mensaje en la carpeta Drafts
    imap.append("Drafts", None, None, msg.as_bytes())

    # Cierra sesión
    imap.logout()


# ───────────────── PROGRAMA PRINCIPAL ─────────────────

def loadEmails():
    """
    Carga los correos desde el archivo emails.txt
    """
    with open(EMAILS_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


if __name__ == "__main__":
    # Carga la lista de correos
    emails = loadEmails()

    print(f"📨 Correos cargados: {len(emails)}")

    # Procesa cada correo
    for email in emails:
        try:
            # Genera el cuerpo del correo
            body = generateEmailBody(email)

            # Intenta guardarlo en IMAP
            saveDraftImap(email, body)

            print(f"✅ Draft guardado para {email}")

        except Exception as e:
            # Si IMAP falla, guarda en TXT
            print(f"⚠️ Error IMAP: {e}")
            saveDraftTxt(email, body)
