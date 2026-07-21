"""SMTP service for sending summaries to configured recipients."""

import html
import logging
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

try:
    import markdown
except ImportError:
    markdown = None

from ..ai.markdown_utils import clean_app_summary_markdown
from ..models import EmailConfig

logger = logging.getLogger(__name__)


class EmailManager:
    """Send daily summaries over SMTP."""

    def __init__(self, config: EmailConfig, console=None):
        self.config = config
        self.pwd = os.getenv(self.config.password_env)
        if console is None:
            try:
                from rich.console import Console

                self.console = Console()
            except ImportError:

                class DummyConsole:
                    def print(self, *args, **kwargs):
                        print(*args, **kwargs)

                self.console = DummyConsole()
        else:
            self.console = console

        if not self.pwd and self.config.enabled:
            logger.warning(
                f"Environment variable {self.config.password_env} not set. Email features may fail."
            )
            self.console.print(
                f"[yellow]Warning: Environment variable {self.config.password_env} not set. Email features may fail.[/yellow]"
            )

    def send_daily_summary(self, summary_md: str, subject: str):
        """Send the daily summary to the configured recipients."""
        if not self.config.enabled or not self.config.recipients:
            return

        cleaned_summary = clean_app_summary_markdown(summary_md)
        safe_summary = html.escape(cleaned_summary)
        html_content = (
            markdown.markdown(safe_summary)
            if markdown
            else f"<pre>{safe_summary}</pre>"
        )

        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }}
                h1, h2, h3 {{ color: #2c3e50; }}
                code {{ background-color: #f4f4f4; padding: 2px 5px; border-radius: 3px; font-family: monospace; }}
                pre {{ background-color: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }}
                blockquote {{ border-left: 4px solid #ddd; padding-left: 15px; color: #777; }}
                .footer {{ margin-top: 40px; font-size: 12px; color: #888; text-align: center; border-top: 1px solid #eee; padding-top: 20px; }}
            </style>
        </head>
        <body>
            {html_content}
            <div class="footer">
                <p>Sent by {self.config.sender_name}</p>
            </div>
        </body>
        </html>
        """

        try:
            with smtplib.SMTP_SSL(
                self.config.smtp_server, self.config.smtp_port
            ) as server:
                server.login(
                    self.config.smtp_username or self.config.email_address, self.pwd
                )

                for recipient in self.config.recipients:
                    msg = MIMEMultipart("alternative")
                    msg["Subject"] = subject
                    msg["From"] = (
                        f"{self.config.sender_name} <{self.config.email_address}>"
                    )
                    msg["To"] = recipient

                    text_part = MIMEText(cleaned_summary, "plain")
                    html_part = MIMEText(html_body, "html")

                    msg.attach(text_part)
                    msg.attach(html_part)

                    try:
                        server.send_message(msg)
                        logger.info(f"Sent summary to {recipient}")
                    except Exception as e:
                        logger.error(f"Failed to send to {recipient}: {e}")

        except Exception as e:
            logger.error(f"SMTP Error: {e}")
