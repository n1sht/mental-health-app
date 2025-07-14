import sys
import os
sys.path.insert(0, os.path.abspath('app'))

from app import app

if __name__ == '__main__':
    os.makedirs('data/submissions', exist_ok=True)
    os.makedirs('app/models', exist_ok=True)
    
    app.run(host='0.0.0.0', port=5000, debug=True)