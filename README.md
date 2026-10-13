# Smart Crop Management System

A Django web application for managing oil palm plantation records, reviewing tree health by zone, and supporting field decisions with AI image analysis and an agricultural chat assistant.

## Features

- **Employee accounts:** Session-based login, employee profiles, active-account controls, and Supervisor, Administrator, and Viewer permission levels.
- **Plantation monitoring:** Store zones and oil palm tree records, then review health, disease, and productivity summaries by zone and by individual tree.
- **AI image analysis:** Submit a tree image with its zone and row/column location. A Qwen2-VL vision model describes visible symptoms; an LLM classifies health, disease, and productivity, and the result is saved to the matching tree record.
- **Agricultural assistant:** Chat in Chinese or English about oil palm care. The assistant combines a local agricultural knowledge base with DuckDuckGo web search and an Ollama-compatible local LLM endpoint.
- **Login activity:** Review login records and IP/device details, including failed-attempt counts and IP blocking controls.
- **Weather data helper:** `utils/get_waether.py` can periodically retrieve current weather for its configured Open-Meteo location and save readings to the database.

## Main Components

- `account/`, `employee/` — login, employee accounts, profiles, and permission levels
- `monitoring/` — zones, oil palm tree records, and monitoring views
- `analyze/`, `ai_model/yolo/`, `utils/vlm.py` — image upload and AI analysis pipeline
- `ai_assistant/`, `utils/agricultural_knowledge.py`, `utils/rag.py`, `utils/llm.py` — chat, local knowledge retrieval, web search, and LLM calls
- `login_log/`, `middleware/` — login activity and IP verification
- `templates/`, `media/` — Django pages and uploaded images
- `utils/get_waether.py` — optional weather polling helper

## Environment Setup

Use Python 3.10 for the model artifacts included with this project. There is no dependency lockfile or `requirements.txt` in the repository, so install packages based on the features you plan to run. The Django application uses Django, Django REST Framework, and Pillow; AI image analysis also requires PyTorch, Transformers, and `qwen-vl-utils`. The chat and retrieval helpers use `requests`, `ddgs`, and `markdown-it-py`.

Install a PyTorch build compatible with your hardware and CUDA setup, then install the project dependencies. The Qwen2-VL model is loaded from Hugging Face when the analysis module is initialized, so the model files must be available locally or downloadable in the runtime environment.

The chat assistant calls an Ollama-compatible endpoint at `http://localhost:11434` and uses the `gpt-oss:120b-cloud` model name by default. Configure and start that service before using chat. RAG web search also requires network access.

## Run Locally

From the project directory, run database migrations and start Django:

```bash
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```

Open `http://127.0.0.1:8000/`. The root page redirects to the account login page. The database uses SQLite by default, and uploaded images are stored under `media/`.

## Application Routes

- `/account/login/` — sign in
- `/monitoring/get_crop_zone_data/` — plantation monitoring dashboard
- `/monitoring/zone/<zone_id>/` — zone details
- `/monitoring/tree/<tree_id>/` — individual tree details
- `/analyze/upload_oil_palm_tree_image/` — upload and analyze a tree image
- `/ai_assistant/get_chat/` — agricultural assistant
- `/employee/get_all_employee/` — employee list
- `/login_log/get_all_login_record/` — login records
- `/login_log/get_all_login_ip/` — IP and device records

Most application pages require an authenticated account. For local testing, use:

- Username: `test`
- Password: `(Test123)`

## Configuration and Deployment Notes

- Django settings are in `smart_crop_management_system/settings.py`; SQLite and media paths are configured there.
- The analysis pipeline requires the Qwen2-VL model and an available runtime compatible with the installed PyTorch build.
- The assistant requires the Ollama-compatible LLM service; its model name is set in `utils/llm.py`.
- Before deployment, move secrets out of source code, rotate any credentials that have been committed, disable `DEBUG`, configure `ALLOWED_HOSTS`, and review login-record handling. Do not use the development settings as production settings.



