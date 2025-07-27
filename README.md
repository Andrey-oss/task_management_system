# Task management system

Task management system is a personal task-tracking web application built with Django. It allows users to create, view, update, and delete tasks with additional functionality such as encryption, image upload, deadline management, and user authentication

## 🔧 Features

- 📝 Create, edit, and delete tasks
- 🔐 Optional encryption for task content with a password
- 🖼️ Image upload support (e.g., task-related screenshots)
- 🗓️ Deadlines with calendar input
- ✅ Status and category selection
- 🔎 Filtering and sorting options
- 👤 User registration, login, and protected routes
- 🧩 Admin interface for profile access
- ⚙️ Some permission features (superuser can edit or read tasks from any user directly from website page, not from admin panel)
- 🌐 DRF / REST API
- 📄 Swagger support (but raw)

## ⚙️ Technologies Used

- Django (CBV-based views)
- Bootstrap 5/Animate.css for responsive UI
- Custom templates with animations
- SQLite support
- Python Cryptography library for encryption (currently AES)
- Hashing password support (currently SHA256)
- Django Rest Framework with Swagger

## 🚫 Not Included (WIP)

This project does **not yet include**:
- Django Signals
- Custom context processors
- matplotlib or statistical dashboards
- Advanced permissions system
- JWT/TokenAuth (soon it will be possible)

## ▶️ Getting Started

1. Clone the repo:
```bash
git clone https://github.com/Andrey-oss/task_management_system.git
cd task_management_system
```

2. Create a virtual environment and install requirements:
```bash
bash init_venv.sh
```

3. Apply migrations and run server:
```bash
python manage.py migrate
python manage.py runserver
```

4. Visit [http://localhost:8000](http://localhost:8000)

## 🐳 Launch by Docker

1. Start the service:
```bash
systemctl start docker
```

2. Initialize container:
```bash
docker build -t tms-app .
```

3. Run the app:
```bash
docker run -p 8000:8000 tms-app
```

## 📁 Folder Structure

- `index/` - index pages (about, index)
- `accounts/` – user authentication and profile views
- `tms/` – main app logic (models, views, templates)
- `templates/` – custom templates (Bootstrap 5)
- `static/` – static files (CSS, JS, images)
- `media/` - media files (userspace dir)
- `crypter/` - crypter module (for enc/decryption tasks)
- `api/` - API section

## 🔒 Encryption

Task content can be encrypted with a custom password. AES (CBC) with PKCS7 padding and base64 encoding is used under the hood via the `cryptography` library
Also this app suports password hashing for better security. Uses SHA256 + PBKDF2 and base64 encoding/decoding with salt randomization, like a task encrypter 

## 💡 Future Plans

- Statistical dashboard with matplotlib
- Task sharing between users
- Signals and better permission logic
- Tests
- Add JWT/TokenAuth

---

## Contributing
Feel free to fork this repository and submit pull requests for improvements

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details
