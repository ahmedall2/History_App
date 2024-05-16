from flask import Flask, request, render_template
import os
import google.generativeai as genai

app = Flask(__name__)

# Configure Gemini API (replace with your API key)
genai.configure(api_key="AIzaSyC_Fvo_TzZoVS-Si-zyKOsHVBmyzajhftY")

# Model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]


def create_model():
  """Creates a new generative model instance."""
  return genai.GenerativeModel(
      model_name="gemini-1.5-flash-latest",
      safety_settings=safety_settings,
      generation_config=generation_config,
      system_instruction="Your main task is to collect patient medical data, like their name, age, demographic, initial presenting history, general history, families. social drug history and so on. And collect them in the end. you're going to. summarize, and I would put the data in a structured way as the doctor write each information you should. ask for the next. The doctor will always start with the patient name, and then you're going to ask the age and the rest of the demographics and so on. You don't need to confirm what the doctor is typing. Just ask the next question directly.",
      )


# Global variables
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

@app.route("/", methods=["GET", "POST"])
def index():
  global chat_history, model

  if request.method == "POST":
    # Get user input
    user_input = request.form["history"]

    # Create model if not already created
    if model is None:
      model = create_model()

    # Send user input to the model and update history
    response = model.send_message(user_input)
    chat_history.append(user_input)
    chat_history.append(response.text)

    return render_template("home.html", history=chat_history, response=response.text)

  # Render initial page
  return render_template("home.html", history=[], response="")

if __name__ == "__main__":
  app.run(host="0.0.0.0", debug=True)
