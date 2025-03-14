# AnonymChat Bot

AnonymChat is a Telegram bot that allows users to chat anonymously with others. The bot provides various chat modes, in-service games, and a token system for in-app purchases.

## Features
- Anonymous chat with random users
- Multiple chat modes
- In-service games
- Token system for rewards and purchases
- Admin panel for managing users

## Installation

### Prerequisites
Before installing, make sure you have the following installed on your system:
- Python 3.10+
- `pip` (Python package manager)
- Git

### Clone the Repository
```bash
git clone https://github.com/Kinetic58/AnonymChat.git
cd AnonymChat
```

### Install Dependencies
Install all this library:
```bash
aiofiles==23.2.1
aiogram==2.23.1
aiohttp==3.8.6
aiohttp-retry==2.8.3
aiosignal==1.3.1
annotated-types==0.6.0
anyio==4.8.0
asgiref==3.8.1
async-timeout==4.0.3
attrs==23.2.0
Babel==2.9.1
beautifulsoup4==4.12.3
blinker==1.9.0
certifi==2024.8.30
chardet==5.2.0
charset-normalizer==3.3.2
click==8.1.8
colorama==0.4.6
deep-translator==1.11.4
Django==5.0.4
et-xmlfile==1.1.0
Flask==3.1.0
frozenlist==1.4.1
gigachat==0.1.38
greenlet==3.0.3
h11==0.14.0
httpcore==1.0.7
httpx==0.27.2
idna==3.10
itsdangerous==2.2.0
Jinja2==3.1.5
magic-filter==1.0.12
MarkupSafe==3.0.2
multidict==6.1.0
numpy==2.2.1
openpyxl==3.1.2
packaging==24.0
pandas==2.2.3
phonenumbers==8.13.47
playwright==1.44.0
pydantic==2.5.3
pydantic_core==2.14.6
pyee==11.1.0
PyJWT==2.9.0
python-dateutil==2.9.0.post0
python-dotenv==1.0.1
pytz==2024.2
requests==2.32.3
six==1.17.0
sniffio==1.3.1
soupsieve==2.5
sqlparse==0.5.0
tbomb==2.1.2
twilio==9.3.1
typing_extensions==4.9.0
tzdata==2024.1
urllib3==2.2.3
webdriver-manager==4.0.1
Werkzeug==3.1.3
yarl==1.11.1
YooMoney==0.1.0
```

## Configuration

1. add bot token and admin id in ../config/config.py:
```
ADMIN_ID = 'adm'
API_TOKEN = 'token'
```
2. Modify `config/config.py` to adjust settings as needed.

## Running the Bot
To start the bot, run:
```bash
python main.py
```

---

This is not a finish version of this project. U can add something to achieve working business bot.

## License
This project is licensed under the MIT License.
