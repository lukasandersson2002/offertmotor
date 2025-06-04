from flask import Flask, request, send_file, render_template
from fpdf import FPDF
from flask_mail import Mail, Message
import sqlite3
import os

app = Flask(__name__)

# Mail-konfiguration (fyll i med din info)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'lukasa020930@gmail.com'    
app.config['MAIL_PASSWORD'] = 'firn psbk mtve qoye'      
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

def rekommendera_laddbox(data):
    fastighet = data.get('property_type')
    laddpunkter = int(data.get('charging_points', 1))
    trefas = data.get('three_phase')

    if fastighet == 'Villa' and trefas == 'Ja':
        return 'Easee Home'
    elif fastighet == 'Bostadsrättsförening' and laddpunkter > 5:
        return 'Charge Amps Halo'
    elif fastighet == 'Företag':
        return 'Zaptec Pro'
    else:
        return 'Zaptec Go'

def spara_forfragan(data):
    conn = sqlite3.connect("offert.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS forfragningar
                      (namn TEXT, email TEXT, fastighet TEXT, laddpunkter INT, trefas TEXT, anteckningar TEXT)''')
    cursor.execute('''INSERT INTO forfragningar VALUES (?, ?, ?, ?, ?, ?)''', (
        data['name'], data['email'], data['property_type'], data['charging_points'], data['three_phase'], data['notes']
    ))
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return send_file("form.html")

@app.route('/generate-offer', methods=['POST'])
def generate_offer():
    data = request.form
    name = data['name']
    email = data['email']

    rekommendation = rekommendera_laddbox(data)
    spara_forfragan(data)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Offert - Laddbox", ln=True, align='C')
    pdf.ln(10)
    for key in data:
        pdf.cell(200, 10, txt=f"{key.capitalize()}: {data[key]}", ln=True)
    pdf.cell(200, 10, txt=f"Rekommenderad laddbox: {rekommendation}", ln=True)

    filename = f"offert_{name.replace(' ', '_')}.pdf"
    filepath = os.path.join(os.getcwd(), filename)
    pdf.output(filepath)

    msg = Message(
        subject="Din offert från LaddboxPro",
        sender=app.config['MAIL_USERNAME'],
        recipients=[email],
        body=f"Hej {name},\n\nHär kommer din offert som PDF.\n\nVänligen,\nLaddboxPro"
    )
    with app.open_resource(filepath) as fp:
        msg.attach(filename, "application/pdf", fp.read())
    mail.send(msg)

    return f"Offert skickad till {email}!"

@app.route('/admin')
def admin():
    conn = sqlite3.connect("offert.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM forfragningar")
    rows = cursor.fetchall()
    conn.close()
    return render_template('admin.html', data=rows)

if __name__ == '__main__':
    app.run(debug=True)
