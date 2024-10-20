from flask import Flask, render_template, request, jsonify
import subprocess
import os

app = Flask(__name__)

# Define the path to the ollama executable
ollama_path = r'C:\Users\prady\AppData\Local\Programs\Ollama\ollama.exe'

def get_question_from_ollama(topic):
    prompt = f"Generate a question about {topic}."
    # Run the subprocess and capture output and error
    result = subprocess.run([ollama_path, 'run', 'gemma2:2b', prompt], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Check if the command was successful
    if result.returncode != 0:
        raise RuntimeError(f"Error generating question: {result.stderr.strip()}")
    
    return result.stdout.strip()

def evaluate_answer_with_ollama(question, answer):
    prompt = f"Is this answer correct for the question '{question}'? Answer: '{answer}'."
    # Run the subprocess and capture output and error
    result = subprocess.run([ollama_path, 'run', 'gemma2:2b', prompt], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Check if the command was successful
    if result.returncode != 0:
        raise RuntimeError(f"Error evaluating answer: {result.stderr.strip()}")
    
    return result.stdout.strip()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_question', methods=['POST'])
def generate_question():
    topic = request.json.get('topic')  # Get the topic from JSON request
    print(f"Topic received: {topic}")  # Debugging output
    question = get_question_from_ollama(topic)
    return jsonify({'question': question})

@app.route('/evaluate_answer', methods=['POST'])
def evaluate_answer():
    data = request.get_json()
    question = data['question']
    answer = data['answer']
    evaluation = evaluate_answer_with_ollama(question, answer)
    return jsonify({'evaluation': evaluation})

if __name__ == '__main__':
    app.run(debug=True)

