import os
from dotenv import load_dotenv
from flask import Flask, render_template, request
from google import genai

app = Flask(__name__)

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("ERROR: GEMINI_API_KEY is not set.")
    client = None
else:
    client = genai.Client(api_key=api_key)

MODEL = "gemini-3.6-flash"


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    error = None

    if request.method == "POST":
        notice = request.form.get("notice", "").strip()

        if not notice:
            error = "Please paste a notice first."

        else:
            try:
                prompt = f"""
You are Notice2Simple, an AI assistant that helps students understand complicated notices.

Analyze the notice below and return ONLY the following sections:

WHAT IS THIS?
Explain what the notice is about in simple language.

WHO CAN APPLY?
Explain eligibility. If the notice does not say, write:
"Not specified in the notice."

IMPORTANT DATE
Find deadlines or other important dates. If none are found,
write:
"No specific date mentioned."

DOCUMENTS REQUIRED
List required documents. If none are mentioned, say:
"No documents mentioned."

WHAT YOU NEED TO DO
Give the student a simple numbered action plan.

IMPORTANT INFORMATION
Mention important warnings, conditions, fees, restrictions,
or other things the student should know.

IMPORTANT:
- Do not invent information.
- Use only information contained in the notice.
- Use simple language.
- If something is missing, clearly say it is not mentioned.

NOTICE:
{notice}
"""

                response = client.models.generate_content(
                    model=MODEL,
                    contents=prompt
                )

                result = response.text

            except Exception as e:

                print("GEMINI ERROR:", repr(e))
                error = f"Gemini error: {str(e)}"

    return render_template(
        "index.html",
        result=result,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)