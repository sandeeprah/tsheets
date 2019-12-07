from application import app, db
# app.run(debug=True, threaded=True, host='0.0.0.0', port=5000)

from application.models import User, Post

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}

#app.run(debug=True, threaded=True, host='0.0.0.0', port=5000)
