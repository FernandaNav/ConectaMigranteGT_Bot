# Conecta Migrante 🇬🇹

Chatbot de Telegram que orienta a personas guatemaltecas en proceso migratorio o de retorno sobre **qué institución atiende cada necesidad y cómo contactarla**: consulados, documentos (DPI y pasaporte), empleo, salud y derechos.

Proyecto de Responsabilidad Social Universitaria del curso de **Ética Aplicada**, Facultad de Ingeniería, Universidad Rafael Landívar, Campus San Alberto Hurtado (Quetzaltenango).

**Equipo:** Luis Granados · María Inés Cardona López · Fernanda Abigail Navarro Martínez · Andy Emmanuel Maldonado López

---

## ¿Qué problema atiende?

Muchas personas migrantes y retornadas no saben a qué institución acudir, qué trámites existen o a quién pedir ayuda, y eso las expone a desinformación y a estafas de supuestos "gestores". Conecta Migrante reúne esa orientación en un solo lugar, gratis y desde una app de mensajería que ya usan.

## Funcionalidades

- Menú guiado con botones: retorno a Guatemala, personas en el extranjero, trámites, derechos y directorio.
- Respuestas a texto libre por palabras clave. Por ejemplo, "me deportaron", "necesito mi pasaporte" o "mi hermano está detenido" llevan a la sección correspondiente.
- Las consultas urgentes (detención o riesgo) tienen prioridad en la búsqueda.
- Navegación con **Volver** y **Menú principal**, dejando visible el historial de la conversación.
- Alertas contra estafas en trámites.
- Comandos: `/start`, `/directorio`, `/ayuda`.

## Flujo de conversación

```
/start → Menú principal
├── Acabo de regresar a Guatemala
│   ├── ¿Qué pasa al llegar?        (IGM, Plan Retorno al Hogar)
│   ├── Obtener o reponer mi DPI    (RENAP)
│   ├── Empleo y capacitación       (MINTRAB, INTECAP)
│   └── Salud y apoyo emocional     (MSPAS, emergencias)
├── Estoy en el extranjero
│   ├── Consulados y servicios      (MINEX)
│   ├── Estoy detenido/a o en riesgo
│   └── Documentos desde afuera
├── Trámites y documentos
│   ├── Pasaporte                   (IGM)
│   └── DPI                         (RENAP)
├── Derechos y denuncias            (PDH, CONAMIGUA)
├── Directorio de instituciones
└── Acerca del proyecto
```

## Tecnologías

| Componente | Herramienta |
|---|---|
| Canal | Telegram |
| Conexión | Telegram Bot API (bot registrado con @BotFather) |
| Lenguaje | Python 3.10+ |
| Librería | [python-telegram-bot](https://python-telegram-bot.org/) |
| Contenido | Archivo JSON editable |
| Tipo de chatbot | Basado en reglas (menús y palabras clave), sin inteligencia artificial |

## Cómo funciona

1. La persona escribe o toca un botón en Telegram.
2. Telegram entrega el mensaje al programa (`bot.py`).
3. El programa revisa, en este orden: si es un botón de navegación, si coincide con una opción del menú, o si contiene una palabra clave. Antes de comparar quita tildes y mayúsculas.
4. Responde con el texto de esa sección, tomado de `contenido.json`, y muestra los botones siguientes.
5. Si no encuentra coincidencia, ofrece el menú principal.

## Estructura del proyecto

```
conecta-migrante-bot/
├── bot.py            # lógica del bot
├── contenido.json    # menús, respuestas y palabras clave
├── requirements.txt  # dependencias
├── .env.example      # plantilla para el token
├── .gitignore
└── README.md
```

## Instalación y ejecución local

1. **Crear el bot en Telegram:** busca `@BotFather` (con la palomita de verificado), envía `/newbot` y guarda el token que te da.
2. **Clonar e instalar:**
   ```bash
   git clone https://github.com/<usuario>/<repositorio>.git
   cd <repositorio>
   python -m venv venv
   venv\Scripts\activate          # Windows
   # source venv/bin/activate     # Mac / Linux
   pip install -r requirements.txt
   ```
3. **Configurar el token:** copia `.env.example` como `.env` y escribe tu token:
   ```
   TELEGRAM_TOKEN=tu_token_aqui
   ```
4. **Ejecutar:**
   ```bash
   python bot.py
   ```
   Cuando aparezca `Application started`, abre el bot en Telegram y envía `/start`. El bot responde mientras el programa esté corriendo, y se detiene con `Ctrl + C`.

> ⚠️ Nunca subas el archivo `.env` ni compartas el token. Si se expone, genera uno nuevo en @BotFather con `/revoke`.

## Editar el contenido

Todo el texto está en `contenido.json`, sin necesidad de tocar el código. Cada sección es un **nodo** con estos campos:

| Campo | Descripción |
|---|---|
| `texto` | Respuesta del bot. Admite `*negrita*` y `_cursiva_`. |
| `padre` | Sección a la que regresa el botón Volver. |
| `opciones` | Botones que llevan a otros nodos (`texto` del botón e `ir_a` con el id del nodo). |
| `palabras_clave` | Palabras que activan la sección cuando el usuario escribe. |

Para agregar una sección, crea el nodo y añade un botón que apunte a él desde su nodo padre. Los textos de los botones no deben repetirse entre secciones.

## Consideraciones éticas

- **No usa IA generativa:** cada respuesta fue redactada y revisada por el equipo, así que el bot no inventa requisitos ni datos.
- **Transparencia:** todo lo que el bot puede decir está a la vista en `contenido.json`.
- **Privacidad:** no pide nombre, DPI ni teléfono, y no guarda conversaciones. Solo recuerda temporalmente en qué sección va cada usuario, para el botón Volver.
- **Orientación, no asesoría:** el bot remite siempre a los canales oficiales de cada institución y aclara que no sustituye asesoría legal.
- **Gratuito:** para las personas usuarias y para el proyecto.

## Limitaciones

- Solo entiende las palabras clave definidas. Las frases que no reconoce se envían al menú principal.
- La información de las instituciones puede cambiar y requiere revisión periódica.
- Ejecutado localmente, el bot funciona solo mientras el equipo que lo hospeda esté encendido.

## Trabajo futuro

- **Corto plazo:** desplegar en la nube (Render, modo webhook) y ampliar el contenido y las palabras clave con base en pruebas de usuarios.
- **Mediano plazo:** contenido en idiomas mayas (k'iche', mam, q'anjob'al), mensajes de audio, ubicaciones de oficinas y métricas de uso anónimas.
- **Largo plazo:** alianza con una institución u organización para mantener la información actualizada, y evaluar WhatsApp o IA restringida al contenido verificado.

## Aviso

Conecta Migrante brinda orientación general. No sustituye asesoría legal ni la información oficial de cada institución. Confirma siempre en sus canales oficiales.