
!pip install watchdog

#cloning the folder
!git clone https://github.com/saadi-cz1/asad.git

import os
import time
import subprocess

#to observe the folder for any changes
from watchdog.observers import Observer

#decidng what to do next
from watchdog.events import FileSystemEventHandler


import google.generativeai as genai

#CONFIGURING GEMINI
api_key = "AIzaSyC_4vQF76i-gCwWQE3l8ILVnskb6eqfPXA"
model = genai.GenerativeModel(model_name="gemini-2.0-flash-exp")

genai.configure(api_key=api_key)

#GENERATING DOCUMENTATION
def generate_documentation_with_gemini(file_path):

    if not file_path.lower().endswith(".py"): #To pick only the python files
        return
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()

    except Exception as e:
        print(f"❌ Failed to read file: {e}")
        return

  #extracting the file name and requesting the query to gemini

    filename = os.path.basename(file_path)
    print(f"🧠 Sending {filename} to Gemini for documentation...")
    prompt = (
        f"You are a professional Python developer.\n"
        f"Generate documentation for this Python file including:\n"
        f"1. Overview/summary of the script\n"
        f"2. Line-by-line explanation\n\n"
        f"Respond in Markdown format.\n\n"
        f"```python\n{code}\n```"
    )

    #to send the prompt for for execution
    try:
        response = model.generate_content(prompt)
        doc_content = response.text.strip() if response and hasattr(response, "text") else None
    except Exception as e:
        print(f"❌ Gemini API Error: {e}")
        doc_content = None
    if not doc_content:
        doc_content = (
            f"⚠️ Gemini did not return a valid response.\n"
            f"Check your API key or model name.\n\n"
            f"File attempted: `{filename}`\n"
        )
        print(f"❗ No valid response received. Creating fallback doc for {filename}")

    # Save documentation
    doc_filename = filename.replace(".py", "_gemini_doc.txt")
    doc_path = os.path.join("asad", "docs")
    os.makedirs(doc_path, exist_ok=True)
    full_doc_path = os.path.join(doc_path, doc_filename)

    try:
        with open(full_doc_path, "w", encoding="utf-8") as f:
            f.write(f"# Gemini Documentation for `{filename}`\n\n")
            f.write(doc_content)
        print(f"✅ Documentation saved to: {full_doc_path}")
    except Exception as e:
        print(f"❌ Failed to write documentation file: {e}")


# ========== FILE EVENT HANDLER ==========
class ChangeHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print(f"🆕 New file created: {event.src_path}")
            generate_documentation_with_gemini(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            print(f"✏️ File modified: {event.src_path}")
            generate_documentation_with_gemini(event.src_path)


# ========== GIT AUTO-PULL ==========
def git_pull():
    print("🔁 Pulling latest changes from GitHub...")
    try:
        subprocess.run(["git", "-C", "asad", "clean", "-fd"], check=True)
        subprocess.run(["git", "-C", "asad", "fetch"], check=True)
        subprocess.run(["git", "-C", "asad", "reset", "--hard", "origin/main"], check=True)
        print("✅ Git repository updated.")
    except subprocess.CalledProcessError as e:
        print("❌ Git pull failed:", e)


# ========== MAIN WATCHER LOOP ==========
if __name__ == "__main__":
    folder_to_watch = "./asad"
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=folder_to_watch, recursive=True)
    observer.start()

    print("👀 Watching for changes in 'asad' folder...")

    try:
        while True:
            git_pull()
            time.sleep(30)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()



