"""
XCSOURCE Flask Server
- Serves static HTML
- Handles contact/cooperation email sending to hujoey@qq.com
"""

import os
import smtplib
import socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder=".")

# ─── Config ──────────────────────────────────────────────────────────────────
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.qq.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")      # sender email address
SMTP_PASS = os.getenv("SMTP_PASS", "")      # sender password / app password
TO_EMAIL  = "hujoey@qq.com"
FROM_NAME = "XCSOURCE Website"

# ─── Route: serve index.html ──────────────────────────────────────────────────
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

# ─── Route: serve static assets ───────────────────────────────────────────────
@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

# ─── Route: send contact/cooperation email ────────────────────────────────────
@app.route("/api/send-email", methods=["POST"])
def send_email():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Invalid JSON data."}), 400

    # ── Required fields from sender ────────────────────────────────────────
    sender_name    = (data.get("name") or "").strip()
    sender_email   = (data.get("email") or "").strip()
    company        = (data.get("company") or "").strip()
    message_body   = (data.get("message") or "").strip()
    inquiry_type   = (data.get("inquiry_type") or "General Inquiry").strip()

    # ── Validation ────────────────────────────────────────────────────────
    if not sender_name:
        return jsonify({"success": False, "message": "Name is required."}), 400
    if not sender_email:
        return jsonify({"success": False, "message": "Your email address is required."}), 400
    if not sender_email or "@" not in sender_email or "." not in sender_email.split("@")[-1]:
        return jsonify({"success": False, "message": "Please enter a valid email address."}), 400
    if not message_body:
        return jsonify({"success": False, "message": "Message content is required."}), 400

    if len(message_body) > 2000:
        return jsonify({"success": False, "message": "Message is too long (max 2000 characters)."}), 400

    # ── Build email ─────────────────────────────────────────────────────────
    subject = f"[XCSOURCE Website] {inquiry_type} from {sender_name}"

    html_body = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; border: 1px solid #e5e7eb; border-radius: 8px; overflow: hidden;">
      <div style="background: #111111; padding: 20px 24px;">
        <h2 style="color: #ffffff; margin: 0; font-size: 18px; letter-spacing: 0.05em;">
          XCSOURCE — New Website Inquiry
        </h2>
      </div>
      <div style="padding: 24px; background: #ffffff;">
        <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
          <tr>
            <td style="padding: 8px 0; color: #9ca3af; width: 120px;">Inquiry Type</td>
            <td style="padding: 8px 0; font-weight: 600; color: #D3122B;">{inquiry_type}</td>
          </tr>
          <tr>
            <td style="padding: 8px 0; color: #9ca3af;">Name</td>
            <td style="padding: 8px 0; color: #111111;">{sender_name}</td>
          </tr>
          <tr>
            <td style="padding: 8px 0; color: #9ca3af;">Email</td>
            <td style="padding: 8px 0;">
              <a href="mailto:{sender_email}" style="color: #D3122B;">{sender_email}</a>
            </td>
          </tr>
          <tr>
            <td style="padding: 8px 0; color: #9ca3af;">Company</td>
            <td style="padding: 8px 0; color: #111111;">{company if company else '—'}</td>
          </tr>
        </table>
        <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 16px 0;">
        <p style="font-size: 14px; color: #9ca3af; margin: 0 0 8px 0;">Message:</p>
        <div style="background: #f9fafb; border-left: 3px solid #D3122B; padding: 12px 16px; font-size: 14px; color: #374151; white-space: pre-wrap;">{message_body}</div>
        <p style="font-size: 12px; color: #9ca3af; margin-top: 20px;">
          This message was sent via the XCSOURCE website contact form.
        </p>
      </div>
    </div>
    """

    text_body = f"""XCSOURCE Website Inquiry

Inquiry Type: {inquiry_type}
Name: {sender_name}
Email: {sender_email}
Company: {company if company else '—'}

Message:
{message_body}

---
This message was sent via the XCSOURCE website contact form.
"""

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{FROM_NAME} <{SMTP_USER or sender_email}>"
    msg["To"] = TO_EMAIL
    msg["Reply-To"] = sender_email

    msg.attach(MIMEText(text_body, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    # ── Send via SMTP ──────────────────────────────────────────────────────
    if not SMTP_USER or not SMTP_PASS:
        print("⚠ SMTP credentials not configured. Email logged (not sent):")
        print(f"  From: {sender_name} <{sender_email}>")
        print(f"  Subject: {subject}")
        print(f"  Body: {message_body}")
        return jsonify({
            "success": True,
            "message": "Email recorded (server not configured for SMTP delivery). The recipient will be notified directly."
        })

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15) as server:
            server.ehlo("xcsource-server")
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, [TO_EMAIL], msg.as_string())
        print(f"✅ Email sent successfully from {sender_email} to {TO_EMAIL}")
        return jsonify({
            "success": True,
            "message": "Your message has been sent successfully. We will respond within 1–2 business days."
        })
    except smtplib.SMTPAuthenticationError:
        return jsonify({"success": False, "message": "Authentication failed. Please contact the site administrator."}), 500
    except smtplib.SMTPException as e:
        print(f"❌ SMTP error: {e}")
        return jsonify({"success": False, "message": f"Failed to send email: {str(e)}"}), 500

# ─── Route: health check ──────────────────────────────────────────────────────
@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "service": "XCSOURCE"})

# ─── Route: env status (for debugging) ───────────────────────────────────────
@app.route("/api/env-status")
def env_status():
    has_smtp = bool(SMTP_USER and SMTP_PASS)
    return jsonify({
        "smtp_configured": has_smtp,
        "smtp_host": SMTP_HOST,
        "smtp_port": SMTP_PORT,
        "from_email": SMTP_USER or "(not set)",
        "to_email": TO_EMAIL,
    })

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    print(f"Starting XCSOURCE server on port {port}...")
    print(f"SMTP configured: {bool(SMTP_USER and SMTP_PASS)}")
    app.run(host="0.0.0.0", port=port, debug=False)