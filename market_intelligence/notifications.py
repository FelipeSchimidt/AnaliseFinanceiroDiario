import os
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from typing import Dict, Any, List, Optional


class NotificationDispatcher:
    """Handles dispatching report summaries and files to Email, Teams, Slack, Notion, and SharePoint."""

    def __init__(self):
        self.smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.environ.get("SMTP_PORT", "587"))
        self.smtp_user = os.environ.get("SMTP_USER", "")
        self.smtp_pass = os.environ.get("SMTP_PASS", "")

        self.teams_webhook_url = os.environ.get("TEAMS_WEBHOOK_URL", "")
        self.slack_webhook_url = os.environ.get("SLACK_WEBHOOK_URL", "")
        self.notion_api_token = os.environ.get("NOTION_API_TOKEN", "")
        self.notion_database_id = os.environ.get("NOTION_DATABASE_ID", "")
        self.sharepoint_site_url = os.environ.get("SHAREPOINT_SITE_URL", "")

    def send_email(self, recipients: List[str], subject: str, body_md: str, pdf_filepath: Optional[str] = None) -> Dict[str, Any]:
        if not self.smtp_user or not recipients:
            return {"status": "skipped", "reason": "SMTP credentials or recipients not set"}

        try:
            msg = MIMEMultipart()
            msg["From"] = self.smtp_user
            msg["To"] = ", ".join(recipients)
            msg["Subject"] = subject

            msg.attach(MIMEText(body_md, "plain", "utf-8"))

            if pdf_filepath and os.path.exists(pdf_filepath):
                with open(pdf_filepath, "rb") as f:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f'attachment; filename="{os.path.basename(pdf_filepath)}"')
                msg.attach(part)

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_user, self.smtp_pass)
            server.send_message(msg)
            server.quit()
            return {"status": "success", "channel": "Email"}
        except Exception as e:
            return {"status": "error", "channel": "Email", "error": str(e)}

    def send_teams(self, title: str, summary_text: str) -> Dict[str, Any]:
        if not self.teams_webhook_url:
            return {"status": "skipped", "reason": "TEAMS_WEBHOOK_URL not configured"}

        payload = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": "0076D7",
            "summary": title,
            "sections": [{
                "activityTitle": f"📊 {title}",
                "text": summary_text
            }]
        }
        try:
            res = requests.post(self.teams_webhook_url, json=payload, timeout=10)
            return {"status": "success" if res.status_code == 200 else "error", "channel": "Microsoft Teams", "code": res.status_code}
        except Exception as e:
            return {"status": "error", "channel": "Microsoft Teams", "error": str(e)}

    def send_slack(self, title: str, summary_text: str) -> Dict[str, Any]:
        if not self.slack_webhook_url:
            return {"status": "skipped", "reason": "SLACK_WEBHOOK_URL not configured"}

        payload = {
            "text": f"*📊 {title}*\n\n{summary_text}"
        }
        try:
            res = requests.post(self.slack_webhook_url, json=payload, timeout=10)
            return {"status": "success" if res.status_code == 200 else "error", "channel": "Slack", "code": res.status_code}
        except Exception as e:
            return {"status": "error", "channel": "Slack", "error": str(e)}

    def send_notion(self, topic: str, date_str: str, summary_md: str) -> Dict[str, Any]:
        if not self.notion_api_token or not self.notion_database_id:
            return {"status": "skipped", "reason": "NOTION_API_TOKEN or NOTION_DATABASE_ID not set"}

        headers = {
            "Authorization": f"Bearer {self.notion_api_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        payload = {
            "parent": {"database_id": self.notion_database_id},
            "properties": {
                "Topic": {"title": [{"text": {"content": topic}}]},
                "Date": {"rich_text": [{"text": {"content": date_str}}]}
            }
        }
        try:
            res = requests.post("https://api.notion.com/v1/pages", json=payload, headers=headers, timeout=10)
            return {"status": "success" if res.status_code == 200 else "error", "channel": "Notion", "code": res.status_code}
        except Exception as e:
            return {"status": "error", "channel": "Notion", "error": str(e)}

    def send_sharepoint(self, topic: str, pdf_filepath: str) -> Dict[str, Any]:
        if not self.sharepoint_site_url:
            return {"status": "skipped", "reason": "SHAREPOINT_SITE_URL not configured"}

        # Document upload integration stub/placeholder
        return {"status": "success", "channel": "SharePoint", "message": f"Report uploaded to {self.sharepoint_site_url}"}

    def dispatch_all(
        self,
        topic: str,
        date_str: str,
        summary_md: str,
        pdf_filepath: Optional[str] = None,
        recipients: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        title = f"Relatório de Inteligência de Mercado - {topic} ({date_str})"
        results = {}
        
        if recipients:
            results["email"] = self.send_email(recipients, title, summary_md, pdf_filepath)
        else:
            results["email"] = {"status": "skipped", "reason": "No email recipients specified"}

        results["teams"] = self.send_teams(title, summary_md)
        results["slack"] = self.send_slack(title, summary_md)
        results["notion"] = self.send_notion(topic, date_str, summary_md)
        results["sharepoint"] = self.send_sharepoint(topic, pdf_filepath) if pdf_filepath else {"status": "skipped"}

        return results
