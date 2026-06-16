from fastapi_mail import ConnectionConfig, MessageSchema, FastMail
from dotenv import load_dotenv
import os

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),

    MAIL_PORT=int(os.getenv("MAIL_PORT")),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),

    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,

    USE_CREDENTIALS=True,

    MAIL_FROM_NAME=os.getenv("MAIL_FROM_NAME")
)

# メール送信関数
async def send_reservation_mail(
    email: str,
    name: str,
    start_at: str,
    people: int,
    kids: int
):

    message = MessageSchema(
        subject="予約完了",
        recipients=[email],

        body=f"""
{name} 様

ご予約ありがとうございます。

予約日時:
{start_at}

人数:
{people}名
子ども:
{kids}名
""",

        subtype="plain"
    )

    fm = FastMail(conf)

    await fm.send_message(message)