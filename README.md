# IMAP Draft Email Generator

Generador de **borradores de correos B2B personalizados** que utiliza modelos de lenguaje (LLM) para redactar mensajes de prospección profesional y los guarda directamente en la carpeta **Drafts** de un servidor **IMAP** (por ejemplo Poste.io, Roundcube, Gmail IMAP, etc.).

El proyecto **NO envía correos automáticamente**. Su objetivo es mantener control humano total sobre el envío final.

---

## 🚀 Características

* Generación de correos B2B personalizados por dominio
* Integración con **IMAP** para guardar borradores reales
* Modo de prueba (*dry-run*) sin consumo de API
* Fallback automático a archivos `.txt`
* Compatible con servidores IMAP estándar
* Enfoque ético: prospección responsable, no spam

---

## 🧩 Requisitos

### Python

El proyecto es compatible con:

* **Python 3.9**
* **Python 3.10**
* **Python 3.11** (recomendado)

> No se garantiza compatibilidad con versiones anteriores a Python 3.9.

### Dependencias principales

* `imaplib` (stdlib)
* `email` (stdlib)
* `requests`
* `python-dotenv`

Instalación:

```bash
pip install -r requirements.txt
```

---

## 🔐 Variables de entorno

Crea un archivo `.env` basado en `.env.example`:

```env
IMAP_HOST=mail.tudominio.com
IMAP_USER=usuario@tudominio.com
IMAP_PASS=tu_password
IMAP_DRAFTS_FOLDER=Drafts #Verifica el listado de tus carpetas dependiende el mail server.

GROQ_API_KEY=tu_api_key
```

---

## 🧠 Modelos LLM (Groq)

Actualmente el proyecto trabaja con **Groq API** utilizando un modelo incluido en su **plan gratuito**.

* El modelo puede estar sujeto a cambios según las políticas de Groq
* No se garantiza disponibilidad permanente del mismo modelo

Para más información sobre planes, modelos y límites, visita:

👉 [https://groq.com](https://groq.com)

---

## 🧪 Modo de prueba (Dry-Run)

Antes de enviar el prompt a la API, el sistema puede operar en **modo prueba**, generando una respuesta genérica para validar:

* Flujo del sistema
* Conexión IMAP
* Guardado de borradores

Ejemplo de salida:

```text
🧠 PROMPT GENERADO (NO ENVIADO A LLM)
🧪 MODO PRUEBA ACTIVO
```

Este modo **no consume créditos** de la API.

---

## ✉️ Guardado de borradores IMAP

Los correos se guardan directamente en la carpeta:

```text
Drafts
```

Compatible con servidores que exponen carpetas como:

* Drafts
* Sent
* Trash
* INBOX

> El nombre de la carpeta puede ajustarse según el servidor.

---

## 🗂️ Fallback a archivos `.txt`

Si la conexión IMAP falla, el sistema puede guardar automáticamente el correo como:

```text
NombreDelCorreo.txt
```

Esto garantiza que **ningún contenido generado se pierda**.

---

## 🧱 Flujo general

1. Se analiza el dominio objetivo
2. Se genera un prompt estructurado
3. (Opcional) Se ejecuta modo prueba
4. Se consulta la API de Groq
5. Se construye el correo
6. Se guarda como borrador IMAP

---

## ⚠️ Consideraciones éticas

Este proyecto:

* No envía correos automáticamente
* No incluye scraping masivo
* No está diseñado para spam

Está pensado para **consultorías, agencias y equipos técnicos** que buscan escalar prospección personalizada de forma responsable.

---

## 📄 Licencia

MIT License

---

## ✨ Autor

**Héctor Daniel Ramírez Rodríguez**
**Quasar Code**
🌐 Sitio web: https://quasarcode.com
