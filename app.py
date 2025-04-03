from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
from pathlib import Path

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return 'MeshNode backend is running.'

@app.route('/save-journal', methods=['POST'])
def save_journal():
    content = request.form.get('entry', '')
    if not content.strip():
        return 'Empty journal entry.', 400

    timestamp = datetime.now().isoformat(timespec='minutes').replace(':', '-')
    save_path = Path.home() / 'pi' / 'meshnode' / 'data' / 'journal'
    save_path.mkdir(parents=True, exist_ok=True)
    filename = save_path / f"{timestamp}-log.md"
    filename.write_text(content.strip())

    return 'Journal entry saved.', 200

@app.route('/get-journal', methods=['GET'])
def get_journal():
    journal_path = Path.home() / 'pi' / 'meshnode' / 'data' / 'journal'
    entries = []

    if not journal_path.exists():
        return jsonify(entries)

    for entry_file in sorted(journal_path.glob("*.md")):
        try:
            entries.append({
                'filename': entry_file.name,
                'content': entry_file.read_text(encoding='utf-8')  # ensures proper character handling
            })
        except Exception as e:
            entries.append({
                'filename': entry_file.name,
                'error': str(e)
            })

    return jsonify(entries)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

