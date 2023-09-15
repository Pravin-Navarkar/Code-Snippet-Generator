from flask import Flask, render_template, request
from jinja2 import Environment, FileSystemLoader
import openai
import CodeSnippetConstants

# Set up your OpenAI API key
api_key = CodeSnippetConstants.API_KEY
openai.api_key = api_key

app = Flask(__name__)
#app = Flask(__name__, template_folder="templates")

template_dir = "templates"
jinja_env = Environment(loader=FileSystemLoader(template_dir))

@app.route("/", methods=["GET", "POST"])
def index():
    user_input = ""
    code_snippet = ""
    selected_language = "python"  # Default to Python

    if request.method == "POST":
        user_input = request.form["user_input"]
        target_language = request.form["target_language"]

        if user_input and target_language:
            try:
                # Define prompts for different target languages
                prompts = {
                    "python": f"Generate Python code snippet: {user_input}\n",
                    "java": f"Generate Java code snippet: {user_input}\n",
                    "cpp": f"Generate C++ code snippet: {user_input}\n",
                    "dotnet": f"Generate .NET code snippet: {user_input}\n",
                    "php": f"Generate PHP code snippet: {user_input}\n",
                    "javascript": f"Generate JavaScript code snippet: {user_input}\n",
                    "sql": f"Generate SQL code snippet: {user_input}\n",
                }

                # Use the appropriate prompt based on the selected target language
                prompt = prompts.get(target_language.lower(), "")

                if prompt:
                    response = openai.Completion.create(
                        engine=CodeSnippetConstants.ENGINE,
                        prompt=prompt,
                        max_tokens=1200
                    )
                    code_snippet = response.choices[0].text.strip()
                    selected_language = target_language  # Update the selected language
                else:
                    code_snippet = "Invalid target language selected."
            except Exception as e:
                code_snippet = f"Error: {str(e)}"

    return render_template("index.html", user_input=user_input, code_snippet=code_snippet, selected_language=selected_language)

if __name__ == "__main__":
    app.run(debug=True)
