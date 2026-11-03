# Conecta Migrante

Chatbot de Telegram que orienta a personas guatemaltecas en proceso migratorio o de retorno sobre qué institución atiende cada necesidad (consulados, DPI, pasaporte, empleo, salud, derechos). Proyecto de Responsabilidad Social Universitaria del curso de Ética Aplicada, Universidad Rafael Landívar, Campus de Quetzaltenango. Equipo de 4 personas.

## Estructura

- `bot.py`: lógica del bot (python-telegram-bot, modo polling).
- `contenido.json`: todos los menús, respuestas y palabras clave. Es donde se hace la mayoría de cambios.
- `requirements.txt`: dependencias.
- `.env.example`: plantilla del token. El `.env` real es local y nunca se sube.
- `README.md`: documentación del proyecto.

## Reglas obligatorias

- **Nunca** leas, muestres, copies ni subas el contenido de `.env`, ni escribas el token del bot en ningún archivo, commit, log o mensaje.
- Antes de cada commit, revisa con `git status` que `.env` y `venv/` no estén incluidos.
- No trabajes directo en `main`: crea una rama y abre un pull request.
- No agregues inteligencia artificial generativa, APIs de pago ni servicios con costo. Es una decisión ética del proyecto: el bot solo responde con contenido escrito y verificado por el equipo.
- No agregues funciones que pidan o guarden datos personales (nombre, DPI, teléfono, conversaciones).
- No inventes información de instituciones. Todo dato nuevo debe salir de un sitio oficial (igm.gob.gt, minex.gob.gt, renap.gob.gt, etc.). Si no se puede verificar, pregunta antes de agregarlo.
- No incluyas números de teléfono de instituciones salvo que se hayan verificado en su sitio oficial; se prefiere el sitio web.

## Cómo editar `contenido.json`

Cada sección es un nodo dentro de `"nodos"`:

- `texto`: respuesta del bot. Usa Markdown de Telegram: `*negrita*` y `_cursiva_`. Los `*` y `_` deben ir **en pares**, o Telegram no puede mostrar el mensaje.
- `padre`: nodo al que regresa el botón "Volver".
- `opciones`: lista de botones `{"texto": "...", "ir_a": "id_del_nodo"}`.
- `palabras_clave`: palabras que activan la sección al escribir. Se comparan como palabras completas, sin tildes ni mayúsculas.

Reglas:
- Cada `ir_a` y cada `padre` debe apuntar a un nodo existente.
- El texto de un botón no puede repetirse en dos secciones distintas, porque el bot identifica las opciones por su texto.
- El orden de los nodos importa en la búsqueda por palabras clave: el primero que coincide gana. `ext_riesgo` (detención o riesgo) va primero a propósito.
- Mantén el tono claro, cercano y en español sencillo; dirígete a la persona de "tú".

## Cómo probar cambios

1. Activa el entorno: `venv\Scripts\activate` (Windows) o `source venv/bin/activate`.
2. Verifica que el JSON sea válido y que los enlaces entre nodos existan:
   ```bash
   python -c "import json; d=json.load(open('contenido.json',encoding='utf-8'))['nodos']; print([(k,o['ir_a']) for k,v in d.items() for o in v.get('opciones',[]) if o['ir_a'] not in d] or 'ok')"
   ```
3. Ejecuta `python bot.py` y prueba en Telegram con `/start`.
4. Cada integrante usa su propio bot de prueba (su propio token en su `.env`). Solo una instancia puede correr por token; si sale `Conflict: terminated by other getUpdates request`, alguien más lo tiene encendido.

## Git

- Ramas con nombres descriptivos: `contenido-salud`, `fix-palabras-clave`, `mejora-menu`.
- Commits cortos en español que digan qué cambió: `agrega seccion de albergues`, `corrige palabras clave de DPI`.
- Haz `git pull` antes de empezar a trabajar.

## Estilo de código

- Comentarios en español y en minúsculas.
- Mantén la lógica en `bot.py` simple; el contenido va en `contenido.json`, no en el código.
