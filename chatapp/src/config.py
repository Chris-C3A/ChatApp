import json

with open("config.json") as config_file:
    config = json.load(config_file)

class Config:
    SECRET_KEY = config.get("SECRET_KEY")
    GMAIL_USERNAME = config.get("GMAIL_USERNAME")

    SQLALCHEMY_DATABASE_URI = config.get("DB_DEV_URI")

    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = config.get("GMAIL_USERNAME")
    MAIL_PASSWORD = config.get("GMAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = config.get("GMAIL_USERNAME")