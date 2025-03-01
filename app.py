from flask import Flask, render_template, request, flash, redirect, url_for, send_file
from werkzeug.utils import secure_filename
import os
from encryption import encrypt_image
from decryption import decrypt_image
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['GET', 'POST'])
def encrypt():
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('No image uploaded', 'error')
            return redirect(request.url)
            
        file = request.files['image']
        if file.filename == '':
            flash('No image selected', 'error')
            return redirect(request.url)
            
        message = request.form.get('message', '').strip()
        password = request.form.get('password', '').strip()
        
        if not message or not password:
            flash('Message and password are required', 'error')
            return redirect(request.url)
        
        try:
            # Save uploaded file
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Encrypt the image
            output_path = encrypt_image(filepath, message, password)
            
            # Return the encrypted file
            return send_file(output_path, as_attachment=True)
            
        except Exception as e:
            flash(f'Error during encryption: {str(e)}', 'error')
            return redirect(request.url)
            
    return render_template('encrypt.html')

@app.route('/decrypt', methods=['GET', 'POST'])
def decrypt():
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('No image uploaded', 'error')
            return redirect(request.url)
            
        file = request.files['image']
        if file.filename == '':
            flash('No image selected', 'error')
            return redirect(request.url)
            
        password = request.form.get('password', '').strip()
        if not password:
            flash('Password is required', 'error')
            return redirect(request.url)
        
        try:
            # Save uploaded file
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Decrypt the image
            message = decrypt_image(filepath, password)
            
            # Pass the decrypted message to template
            return render_template('decrypt.html', decrypted_message=message)
            
        except Exception as e:
            flash(f'Error during decryption: {str(e)}', 'error')
            return redirect(request.url)
            
    return render_template('decrypt.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
