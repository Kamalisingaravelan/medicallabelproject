from flask import Flask, render_template, request, redirect, url_for, session, send_file, flash

import mysql.connector
import easyocr
import cv2 as cv
from gtts import gTTS
import os
import time
from googletrans import Translator

app = Flask(__name__)
app.secret_key = 'a'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/AdminLogin')
def AdminLogin():
    return render_template('AdminLogin.html')


@app.route('/UserLogin')
def UserLogin():
    return render_template('UserLogin.html')


@app.route('/NewUser')
def NewUser():
    return render_template('NewUser.html')


@app.route('/OCR')
def OCR():
    return render_template('OCR.html')


@app.route('/NewMedicine')
def NewMedicine():
    return render_template('NewMedicine.html')


@app.route("/serverlogin", methods=['GET', 'POST'])
def serverlogin():
    if request.method == 'POST':
        if request.form['uname'] == 'server' and request.form['password'] == 'server':

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1medicinelabltb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb ")
            data = cur.fetchall()
            return render_template('AdminHome.html', data=data)
        else:
            flash('Username or Password is wrong')
            return render_template('AdminLogin.html')


@app.route('/AdminHome')
def AdminHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1medicinelabltb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb ")
    data = cur.fetchall()
    return render_template('AdminHome.html', data=data)


@app.route('/MedicineInfo')
def MedicineInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1medicinelabltb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM meditb ")
    data = cur.fetchall()
    return render_template('MedicineInfo.html', data=data)


@app.route("/Remove")
def Remove():
    id = request.args.get('lid')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1medicinelabltb')
    cursor = conn.cursor()
    cursor.execute("Delete from meditb where id='" + id + "' ")
    conn.commit()
    conn.close()

    return MedicineInfo()


@app.route("/newmedicine", methods=['GET', 'POST'])
def newmedicine():
    if request.method == 'POST':
        mname = request.form['mname']
        info = request.form['info']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1medicinelabltb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from meditb where Medicine='" + mname + "'  ")
        data = cursor.fetchone()
        if data is None:
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1medicinelabltb')
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO meditb VALUES ('','" + mname + "','" + info + "')")
            conn.commit()
            conn.close()

            flash('Record Saved!')
            return render_template('NewMedicine.html')
        else:
            flash('Already Register This  Medicine!')
            return render_template('NewMedicine.html')


@app.route("/newuser", methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':
        uname = request.form['uname']
        mobile = request.form['mobile']
        email = request.form['email']
        address = request.form['address']
        username = request.form['username']
        password = request.form['password']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1medicinelabltb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + username + "'  ")
        data = cursor.fetchone()
        if data is None:
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1medicinelabltb')
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO regtb VALUES ('','" + uname + "','" + mobile + "','" + email + "','" + address + "','" +
                username + "','" + password + "')")
            conn.commit()
            conn.close()

            flash('Record Saved!')
            return render_template('NewUser.html')
        else:
            flash('Already Register This  UserName!')
            return render_template('NewUser.html')


@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':

        username = request.form['uname']
        password = request.form['password']
        session['uname'] = username
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1medicinelabltb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + username + "' and Password='" + password + "' ")
        data = cursor.fetchone()
        if data is None:

            flash('Username or Password is wrong')
            return render_template('UserLogin.html')

        else:

            conn = mysql.connector.connect(user='root', password='', host='localhost',
                                           database='1medicinelabltb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb where username='" + session['uname'] + "'")
            data1 = cur.fetchall()
            flash('Login Successfully')
            return render_template('UserHome.html', data=data1)


@app.route('/UserHome')
def UserHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost',
                                   database='1medicinelabltb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb where username='" + session['uname'] + "'")
    data1 = cur.fetchall()

    return render_template('UserHome.html', data=data1)


@app.route("/owfileupload", methods=['GET', 'POST'])
def owfileupload():
    if request.method == 'POST':
        from googletrans import Translator
        import easyocr
        import cv2 as cv
        reader = easyocr.Reader(['en'])

        file_path = "tamil_voice.mp3"

        # Try to close and wait before deleting
        try:
            os.remove(file_path)
        except PermissionError:
            print("File is in use, waiting...")
            time.sleep(5)  # Wait 5 seconds
            os.remove(file_path)  # Try again

        language = "ta"
        print(language)

        file = request.files['file']
        import random
        fnew = random.randint(111, 999)
        savename = str(fnew) + file.filename

        file.save("static/upload/" + savename)

        img = cv.imread("static/upload/" + savename)
        result = reader.readtext(img)
        final_text = " ".join([detection[1] for detection in result])

        translator = Translator()
        translated_text = translator.translate(final_text, src='en', dest=language)

        tamil_text = translated_text.text
        tts = gTTS(text=tamil_text, lang='ta')
        tts.save("tamil_voice.mp3")
        os.system("start tamil_voice.mp3")

        return render_template('OCR.html', v1=final_text, v2=translated_text.text)


@app.route("/Camera")
def Camera():
    import cv2 as cv

    import easyocr

    reader = easyocr.Reader(['en'])

    language = "ta"
    import re

    file_path = "tamil_voice.mp3"

    # Try to close and wait before deleting
    try:
        os.remove(file_path)
    except PermissionError:
        print("File is in use, waiting...")
        time.sleep(5)  # Wait 5 seconds
        os.remove(file_path)  # Try again

    cap = cv.VideoCapture(0)
    frame_count = 0
    while (cap.isOpened()):
        hasFrame, frame = cap.read()
        if hasFrame:
            frame_count += 1
            print(frame_count)
            if frame_count % 5 == 0:  # process every other frame to save time
                img = frame
                result = reader.readtext(img)
                for detection in result:
                    text = detection[1]

                    text = re.sub(r"[^a-zA-Z0-9]", "", detection[1])
                    # print(text)
                    print(text)
                    # speak.Speak(text)

                    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1medicinelabltb')
                    cur = conn.cursor()
                    cur.execute("SELECT * FROM meditb where Medicine like '%" + text + "%' ")
                    data = cur.fetchone()
                    if data:
                        mname = data[1]
                        info = data[2]

                        stext = "Medicine Name:" + mname + " Information:" + str(info)

                        translator = Translator()
                        translated_text = translator.translate(stext, src='en', dest=language)

                        tamil_text = translated_text.text
                        tts = gTTS(text=tamil_text, lang='ta')
                        tts.save("tamil_voice.mp3")
                        os.system("start tamil_voice.mp3")

                        cv.destroyAllWindows()
                        cap.release()
                        return render_template('OCR.html')

            if cv.waitKey(1) & 0xFF == ord('q'):
                break

            cv.imshow('frame', frame)
        else:
            break

    cv.destroyAllWindows()
    cap.release()
    return render_template('OCR.html')


if __name__ == '__main__':
    # app.run(host='0.0.0.0', debug=True, port=5000)
    app.run(debug=True, use_reloader=True)
