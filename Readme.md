# 🎇 CodeWaliDiwali  

**Personalized Festival Greetings, Coded with Joy 💻✨**

CodeWaliDiwali is a Django-based interactive web app that brings festivals to life — combining creativity, personalization, and code.  
It sends unique, custom greetings for **Diwali**, **New Year**, and **Bhai Dooj**, each with its own interactive experience and festive animations.  

---

## 🌟 Features  

- 🎁 **Personalized Links** — Each recipient gets a unique link generated from an Excel sheet using a unique ID.  
- 🪔 **Dynamic Greetings** — Displays custom messages like _“Happy Diwali, Pratham!”_ fetched dynamically from your data.  
- 💬 **WhatsApp Integration** — Share personalized greeting links directly via WhatsApp.  
- 🔥 **Interactive Festive Games** —  
  - **Diwali:** Light diyas, reveal messages with each flame.  
  - **New Year:** Burst confetti to unlock wishes.  
  - **Bhai Dooj:** Collect blessings in a mini-click game.  
- 🧩 **Modular Design** — Built for easy expansion — add more festivals or features without rewriting core logic.  
- 🌐 **Deployed with Django & Bootstrap** — Fast, responsive, and celebration-ready!  

---

## 🧠 Tech Stack  

| Component | Technology |
|------------|-------------|
| Backend | Django (Python) |
| Frontend | HTML, CSS, JS, Bootstrap |
| Database | SQLite |
| IDE | Visual Studio Code |
| Version Control | Git + GitHub |
| Data Source | Excel (CSV import for contacts) |

---

## ⚙️ Setup  

**1. Clone the Repository**
```bash
git clone https://github.com/Pratham1803/codewalidiwali.git
cd codewalidiwali
````

**2. Create Virtual Environment**

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

**3. Run Migrations**

```bash
python manage.py migrate
```

**4. Import Contacts**

```bash
python manage.py import_contacts static/contacts.csv
```

**5. Run Server**

```bash
python manage.py runserver
```

6. Visit → `http://127.0.0.1:8000/`

---

## 📸 Sneak Peek

🪔 **Diwali Mode** → Light diyas and watch each flame reveal a new wish.
🎉 **New Year Mode** → Confetti bursts bring joyful messages.
💞 **Bhai Dooj Mode** → Interactive click-based blessings exchange.

---

## 🔗 Future Enhancements

* Add more festival themes (Holi, Raksha Bandhan, Christmas, etc.)
* Add background music and real-time chat-style wishboard.
* Deploy live using Render / Vercel with custom domain.

---

## 💡 Inspiration

Every developer deserves a festival where **code meets creativity**.
CodeWaliDiwali started as an idea to make digital greetings more personal — where every click, diya, and sparkle is coded with heart.

---

## 👨‍💻 Author

**Pratham** — Android & Flutter Developer | Python + Django Enthusiast
📧 [Your Email or Portfolio Link]
🌐 [GitHub Profile](https://github.com/pratham1803)

---

## 🪄 Tagline

> “Lighting up hearts — one line of code at a time.”