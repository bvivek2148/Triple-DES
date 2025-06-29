from flask import Flask, render_template, request, send_file, flash, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import os
import sqlite3
from datetime import datetime
from triple_des_example import TripleDESCipher

# Get the project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Configure Flask app with proper template and static folders
app = Flask(__name__,
           template_folder=os.path.join(PROJECT_ROOT, 'templates'),
           static_folder=os.path.join(PROJECT_ROOT, 'static'))
app.secret_key = os.urandom(24)

# Configure folders using relative paths
UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, 'uploads')
KEYS_FOLDER = os.path.join(PROJECT_ROOT, 'secure_keys')
DB_PATH = os.path.join(PROJECT_ROOT, 'database', 'encryption_history.db')

for folder in [UPLOAD_FOLDER, KEYS_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['KEYS_FOLDER'] = KEYS_FOLDER

cipher = TripleDESCipher()
cipher.key_file = os.path.join(KEYS_FOLDER, 'secure_keys.json')

def add_to_history(filename, key_id, operation_type):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO encryption_history (filename, key_id, operation_type)
        VALUES (?, ?, ?)
    ''', (filename, key_id, operation_type))
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM encryption_history ORDER BY timestamp DESC LIMIT 10')
    history = c.fetchall()
    conn.close()
    return history

@app.route('/')
def index():
    history = get_history()
    return render_template('index.html', history=history)

@app.route('/encryption-tool')
def encryption_tool():
    history = get_history()
    back_url = request.referrer or url_for('index')  # Get previous page or default to index
    return render_template('encryption_tool.html', history=history, back_url=back_url)

@app.route('/history')
def history():
    history = get_history()
    back_url = request.referrer or url_for('index')
    return render_template('history.html', history=history, back_url=back_url)

@app.route('/about')
def about():
    back_url = request.referrer or url_for('index')
    return render_template('about.html', back_url=back_url)

@app.route('/decrypt', methods=['POST'])
def decrypt():
    if 'file' not in request.files or 'key_id' not in request.form:
        flash('Both file and key ID are required', 'danger')
        return redirect(url_for('encryption_tool'))
    
    file = request.files['file']
    key_id = request.form['key_id']
    
    if file.filename == '' or not key_id:
        flash('Both file and key ID are required', 'danger')
        return redirect(url_for('index'))

    if file:
        filename = secure_filename(file.filename)

        # Extract original filename from encrypted file
        if filename.startswith('encrypted_') and filename.endswith('.bin'):
            # Remove 'encrypted_' prefix and '.bin' suffix to get original name
            original_filename = filename[10:-4]  # Remove 'encrypted_' (10 chars) and '.bin' (4 chars)
        elif filename.endswith('.bin'):
            # Just remove .bin extension
            original_filename = filename[:-4]
        else:
            # Use filename as is
            original_filename = filename

        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        decrypted_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
        
        file.save(input_path)
        
        try:
            if not cipher.load_key(key_id):
                flash('Invalid or expired key ID', 'danger')
                return redirect(url_for('index'))
            
            cipher.decrypt_file(input_path, decrypted_path)
            add_to_history(original_filename, key_id, 'Decryption')

            os.remove(input_path)

            # Store key ID in session for display after download
            from flask import session
            session['last_key_id'] = key_id
            session['last_operation'] = 'decryption'
            session['last_filename'] = original_filename

            return send_file(decrypted_path, as_attachment=True)
        except Exception as e:
            flash(f'Decryption error: {str(e)}', 'danger')
            return redirect(url_for('encryption_tool'))

@app.route('/encrypt', methods=['POST'])
def encrypt():
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file selected'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No file selected'})

    if file:
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        encrypted_path = os.path.join(app.config['UPLOAD_FOLDER'], f'encrypted_{filename}.bin')

        file.save(input_path)

        try:
            cipher.generate_key()
            key_id = os.urandom(8).hex()
            cipher.save_key(key_id)

            cipher.encrypt_file(input_path, encrypted_path)
            add_to_history(filename, key_id, 'Encryption')

            os.remove(input_path)

            # Store download data in session for the download route
            from flask import session
            session['download_file'] = encrypted_path
            session['download_filename'] = f'encrypted_{filename}.bin'

            return jsonify({
                'success': True,
                'key_id': key_id,
                'download_url': url_for('download_encrypted'),
                'filename': f'encrypted_{filename}.bin'
            })
        except Exception as e:
            return jsonify({'success': False, 'message': f'Encryption error: {str(e)}'})

@app.route('/delete-history/<int:record_id>', methods=['POST'])
def delete_history_record(record_id):
    """Delete a specific history record"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        # Check if record exists
        c.execute('SELECT filename FROM encryption_history WHERE id = ?', (record_id,))
        record = c.fetchone()

        if record:
            # Delete the record
            c.execute('DELETE FROM encryption_history WHERE id = ?', (record_id,))
            conn.commit()
            flash(f'✅ History record for "{record[0]}" deleted successfully!', 'success')
        else:
            flash('❌ Record not found!', 'danger')

        conn.close()
    except Exception as e:
        flash(f'❌ Error deleting record: {str(e)}', 'danger')

    return redirect(url_for('history'))

@app.route('/download-encrypted')
def download_encrypted():
    from flask import session

    # Get download data from session
    download_file = session.pop('download_file', None)
    download_filename = session.pop('download_filename', None)

    if download_file and os.path.exists(download_file):
        return send_file(download_file, as_attachment=True, download_name=download_filename)
    else:
        return jsonify({'success': False, 'message': 'Download file not found'})

@app.route('/clear-history', methods=['POST'])
def clear_all_history():
    """Clear all history records"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        # Get count before deletion
        c.execute('SELECT COUNT(*) FROM encryption_history')
        count = c.fetchone()[0]

        if count > 0:
            # Delete all records
            c.execute('DELETE FROM encryption_history')
            conn.commit()
            flash(f'✅ All {count} history records cleared successfully!', 'success')
        else:
            flash('ℹ️ No history records to clear.', 'info')

        conn.close()
    except Exception as e:
        flash(f'❌ Error clearing history: {str(e)}', 'danger')

    return redirect(url_for('history'))

if __name__ == '__main__':
    app.run(debug=True)