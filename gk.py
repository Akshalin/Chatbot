from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# Configure OpenAI API
openai.api_key = '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'

@app.route('/webhook', methods=['POST'])
def webhook():
    user_input = request.form.get('user_input').lower()
    bot_response = generate_response(user_input)
    return jsonify({'response': bot_response})

def generate_response(user_input):
    # Use OpenAI GPT to generate a response
    gpt_response = openai.Completion.create(
        engine="davinci",
        prompt=user_input,
        max_tokens=50
    )

    return gpt_response.choices[0].text

if __name__ == '__main__':
    app.run(debug=True)