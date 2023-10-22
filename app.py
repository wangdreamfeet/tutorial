from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  
from flask_cors import CORS 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calculator.db'  # 使用SQLite数据库
app.config['TEMPLATES_AUTO_RELOAD'] = True  # 自动重新加载模板
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)

class Calculation(db.Model):
    __tablename__ = 'calculator'
    id = db.Column(db.Integer, primary_key=True)
    expression = db.Column(db.String(100))
    result = db.Column(db.Float)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('history.html')

@app.route('/save_result', methods=['POST'])
def save_result():
    data = request.get_json()
    expression = data.get('expression')
    result = data.get('result')

    calculation = Calculation(expression=expression, result=result)
    db.session.add(calculation)
    db.session.commit()

    return jsonify({'success': True})

@app.route('/get_history')
def get_history():
    calculations = Calculation.query.all()
    history = [f'{calculation.expression} = {calculation.result}' for calculation in calculations]
    return jsonify({'success': True, 'history': history})

@app.route('/history')
def history():
    calculations = Calculation.query.all()
    return render_template('history.html', calculations=calculations)


@app.route('/clear_history', methods=['GET', 'POST'])
def clear_history():
    Calculation.query.delete()
    db.session.commit()
    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)