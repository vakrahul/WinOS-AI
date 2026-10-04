import subprocess
import urllib.parse
import time

to_email = "oxastra7@gmail.com"
subject = "Application for AI/ML Research Intern — Rahul Vakiti"

body = """Dear Hiring Team at OxAstra,

I came across your recent hiring post on LinkedIn for the AI/ML Research Intern position and wanted to express my strong interest in joining your team in Bengaluru.

I am a Computer Science undergraduate at CMRIT with hands-on experience building AI systems, agentic frameworks, and machine learning models. Key highlights from my background include:

• Model Optimization & Deep Learning: Published research in IRE Journals titled "Investigating Data Leakage–Induced Over-Confidence and Explanation Faithfulness in Transformer-Based Text and Audio Models".
• Production AI Projects: Built Nexus Agent (Autonomous AI Platform) and ResumeGuard AI (LLM Security & Prompt Injection Defense) featured on my portfolio.
• Engineering & Startup Experience: SDE Intern at xstratum.ai and Core Product Team member at Aden (YC-backed startup), developing scalable agentic workflows and model pipelines.
• Technical Stack: Proficient in Python, PyTorch, FastAPI, Vector Databases, Linux, and Git.

Portfolio: https://rahulvakiti.space
GitHub: https://github.com/vakrahul
LinkedIn: https://linkedin.com/in/vakiti-rahul

I would welcome the opportunity to contribute to OxAstra's real-time computer vision and edge AI models. My resume is attached for your review.

Thank you for your time and consideration.

Sincerely,
Rahul Vakiti
+91-7416754611
vakitirahul@gmail.com"""

encoded_to = urllib.parse.quote(to_email)
encoded_su = urllib.parse.quote(subject)
encoded_body = urllib.parse.quote(body)

gmail_compose_url = f"https://mail.google.com/mail/?view=cm&fs=1&to={encoded_to}&su={encoded_su}&body={encoded_body}"

print("Launching Gmail Compose in active Chrome window...")
# Use PowerShell Start-Process so & characters are preserved exactly
cmd = ["powershell", "-NoProfile", "-Command", f"Start-Process 'chrome.exe' -ArgumentList '{gmail_compose_url}'"]
subprocess.run(cmd)
print("[+] Gmail Compose window opened with pre-filled application draft.")
