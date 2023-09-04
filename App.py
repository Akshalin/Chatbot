from flask import Flask, render_template, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from transformers import pipeline
import openai
from twilio.rest import Client

app = Flask(__name__)

# Configure OpenAI API
openai.api_key = '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'

# Configure Twilio
twilio_account_sid = 'AC316f5a4d0780059305549566ea5f3a5f'
twilio_auth_token = '212c1107b551279b5a835d54dfedded5'
twilio_client = Client(twilio_account_sid, twilio_auth_token)

# Create a sentiment analysis pipeline
nlp_sentiment = pipeline("sentiment-analysis")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    user_input = request.form.get('user_input').lower()
    bot_response = generate_response(user_input)
    send_message(bot_response)

    return jsonify({'response': bot_response})

def generate_response(user_input):
    # Use OpenAI GPT to generate a response
    gpt_response = openai.Completion.create(
        engine="davinci",
        prompt=user_input,
        max_tokens=50
    )

    # Perform sentiment analysis
    sentiment = nlp_sentiment(user_input)[0]['label']
    if sentiment == 'NEGATIVE':
        empathy_response = "I'm here to support you. Please feel free to share more."
        return f"{gpt_response.choices[0].text}\n\n{empathy_response}"

    return gpt_response.choices[0].text

def send_message(message):
    twilio_client.messages.create(
        body=message,
        from_='+16562230823',
        to='user_number'
    )

if __name__ == '__main__':
    app.run(debug=True)

