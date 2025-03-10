from flask import Flask, request, jsonify
from chat_manager import ChatManager
import os
from werkzeug.utils import secure_filename

# Create the Flask app
app = Flask(__name__)

# Global chat session manager instance
chat_session = ChatManager()

# Create the upload folder if it doesn't exist
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_document():
    # Check if file was included in request
    if 'file' not in request.files:
        return jsonify({"error": "No file part in request"}), 400
    # Get the file from the request
    file = request.files['file']
    # Check if a file was selected
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    # Try to process the file
    try:
        # Secure the filename
        filename = secure_filename(file.filename)
        # Create the full path
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        # Save file temporarily
        file.save(filepath)
        # Process the document
        result = chat_session.upload_document(filepath)
        # Clean up temporary file
        os.remove(filepath)
        # Return success message
        return jsonify({
            "message": f"File '{filename}' uploaded and processed successfully.",
            "result": result
        }) 
    except Exception as e:
        return jsonify({"error": f"Failed to save file: {str(e)}"}), 500

@app.route('/message', methods=['POST'])
def send_message():
    # Get the data from the request
    data = request.get_json()
    # Check if the message is provided
    if not data or 'message' not in data:
        return jsonify({"error": "No message provided"}), 400
    # Get the message from the request data
    user_message = data['message']
    # Try to send the message
    try:
        # Send the message to the chat session
        ai_response = chat_session.send_message(user_message)
    except Exception as e:
        # Return the error
        return jsonify({"error": str(e)}), 500
    # Return the AI response
    return jsonify({"response": ai_response})

@app.route('/reset', methods=['POST'])
def reset_chat():
    # Reset the chat session
    result = chat_session.reset_session()
    # Return the success message
    return jsonify({"message": "Chat session has been reset.", "result": result})

if __name__ == '__main__':
    # Run the app on port 3000
    app.run(debug=True, host='0.0.0.0', port=3000)