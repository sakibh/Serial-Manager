from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///serial.db'
db = SQLAlchemy(app)

class Serials(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	product_name = db.Column(db.String(200), nullable=False)
	product_image = db.Column(db.Text, nullable=False)
	serial_number = db.Column(db.Text, nullable=False)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)

	def __repr__(self):
		return '<Serial %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
	if request.method == 'POST':
		sdb_product_name = request.form['product_name']
		sdb_product_image = request.form['product_image']
		sdb_serial_number = request.form['serial_number']
		new_sdb = Serials(product_name=sdb_product_name, product_image=sdb_product_image, serial_number=sdb_serial_number)

		try:
			db.session.add(new_sdb)
			db.session.commit()
			return redirect('/')
		except:
			return 'Error, unable to add to database!'

	else:
		sdb_serials = Serials.query.order_by(Serials.date_created).all()
		return render_template('index.html', sdb_serials=sdb_serials)

@app.route('/delete/<int:id>')
def delete(id):
	serial_to_delete = Serials.query.get_or_404(id)

	try:
		db.session.delete(serial_to_delete)
		db.session.commit()
		return redirect('/')
	except:
		return 'Error deleting task!'

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
	serialsdb = Serials.query.get_or_404(id)

	if request.method == 'POST':
		serialsdb.product_name = request.form['product_name']
		serialsdb.product_image = request.form['product_image']
		serialsdb.serial_number = request.form['serial_number']

		try:
			db.session.commit()
			return redirect('/')
		except:
			return 'Error updating serial!'

	else:
		return render_template('edit.html', serialsdb=serialsdb)


if __name__ == "__main__":
	app.run(debug=True)