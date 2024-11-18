from flask import Flask,jsonify,request,render_template,redirect,url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, Column,String,Integer
import os
from flask_marshmallow import Marshmallow
import pandas as pd



app = Flask(__name__)
app.secret_key = os.urandom(18)


username='Balli'
server = 'localhost'
driver ='ODBC+Driver+17+for+SQL+Server'
password=''
database = 'TestDB'

Basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'mssql+pyodbc://{username}:{password}@{server}/{database}?Trusted_connection=Yes&driver={driver}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

dbo=SQLAlchemy(app)
ma=Marshmallow(app)


class patient(dbo.Model):
    __tablename__ = 'Patient'
    patient_id = Column(String(25),primary_key=True)
    Disease = Column(String(100),nullable=False)
    Fever = Column(String,nullable=False)
    Cough = Column(String,nullable=False)
    Fatigue	= Column(String,nullable=False)
    Difficulty_Breath = Column(String,nullable=False)
    Age = Column(Integer,nullable=False)
    Gender = Column(String(15),nullable=False)
    Blood_Pressure = Column(String(25),nullable=False)
    Cholesterol_Level = Column(String(25),nullable=False)
    Outcome_Variable = Column(String(25),nullable=False)

    __table_args__ = (
        CheckConstraint("Blood_pressure in ('High','Low','Normal')",name="Bloodcheck_input"),
        CheckConstraint("Cholesterol_Level in ('High','Low','Normal')",name="cholesterolcheck_input"),
        CheckConstraint("Outcome_Variable in ('Positive','Negative')",name="outcomecheck_inpcommand"))

def __repr__(self):
    return 'Patient profile with created'


@app.cli.command('createall')
def createall():
    dbo.create_all()
    print('database created/accessed and dbo object created successfully')


class patientschema(ma.Schema):
    class Meta:
        fields=('patient_id','Disease','Fever','Cough','Fatigue','Difficulty_Breath','Age','Gender','Blood_Pressure',
               'Cholesterol_Level','Outcome_Variable')


patient_schema=patientschema()
patients_Schema=patientschema(many=True)



@app.cli.command('upload')
def upload():
    file_location='C:/Users/Balli/Patient_Profile_Dataset.csv'
    if os.path.exists(file_location):
        try:
            df=pd.read_csv(file_location)
            if not df.empty:
                df.fillna({
                        'Patient Id': 'Unknown',
                        'Disease': 'Unknown',  
                        'Fever': False,
                        'Cough': False,
                        'Fatigue': False,
                        'Difficulty Breathing': False,
                        'Age': 0, 
                        'Gender': 'Unknown', 
                        'Blood Pressure': 'Normal',
                        'Cholesterol Level': 'Normal',
                        'Outcome Variable': 'Unknown' }, inplace=True)
                        
                df['Patient Id']=df['Patient Id'].astype(str)
                df['Disease']=df['Disease'].astype(str)
                df['Fever']= df['Fever'].astype(str)
                df['Cough']=df['Cough'].astype(str)
                df['Fatigue']= df['Fatigue'].astype(str)
                df['Difficulty Breathing']=df['Difficulty Breathing'].astype(str)
                df['Age']= df['Age'].astype(int)
                df['Gender']=df['Gender'].astype(str)
                df['Blood Pressure']= df['Blood Pressure'].astype(str)
                df['Cholesterol Level']= df['Cholesterol Level'].astype(str)
                df['Outcome Variable']=df['Outcome Variable'].astype(str)
                if df.empty:
                    print('Empty dataset') 
                else:
                        for _, row in df.iterrows():
                            patient_record= patient(patient_id=row['Patient Id'],Disease=row['Disease'],
                                            Fever= row['Fever'],
                                            Cough=row['Cough'],
                                            Fatigue=row['Fatigue'],
                                            Difficulty_Breath=row['Difficulty Breathing'],
                                            Age=row['Age'],Gender=row['Gender'],Blood_Pressure=row['Blood Pressure'],
                                            Cholesterol_Level=row['Cholesterol Level'],Outcome_Variable=row['Outcome Variable'])   
                            dbo.session.add(patient_record)
                        dbo.session.commit()
                        print(patient_record)
                        print('Database Object loaded successfully')
            else:
                print('No File found')
        except Exception as e:
            print(f'Erro processing file:{e}')



@app.route('/records',methods=['GET'])
def records():
    records = patient.query.all()
    if records:
                try:
                    return render_template('viewpatientrecord.html', records=records)
                        
                except Exception as e:
                    return jsonify(Error_message=f'Error processing patient record:{e}')
    else:
        return render_template('invalid.html')


@app.route('/ID',methods=['GET','POST'])
def ID():
    if request.method== "POST":
          pid = request.form.get('patient_ID')
          precord= patient.query.filter_by(patient_id=pid).first()
          if precord:
            return  redirect(url_for('patientdetails',patient_id=pid))
          else:
            return render_template('invalid1.html')
    return render_template('patient.html')
    
    

@app.route('/singlerecord/<string:patient_id>',methods=['Get'])
def patientdetails(patient_id:str):
    patientone = patient.query.filter_by(patient_id=patient_id).first()
    if patientone:
        return render_template('patientone.html', patient=patientone,patient_id=patient_id)




@app.route('/patientAdd', methods=['GET','POST'])
def Addpatient():
    if request.method == "POST": 
        patient_ID =request.form['patient_ID']
        test = patient.query.filter_by(patient_id=patient_ID).first()
        if test:
            return render_template('invalid.html')
        else:
            Disease=request.form['Disease']
            Fever=request.form['Fever']
            Cough=request.form['Cough']
            Fatigue=request.form['Fatigue']
            Difficulty_Breath=request.form['Difficulty_Breath']
            Age= int(request.form['Age'])
            Gender=request.form['Gender']
            Blood_Pressure=request.form['Blood_Pressure']
            Cholesterol_Level=request.form['Cholesterol_Level']
            Outcome_Variable=request.form['Output_Variable']

            new_patient =patient(patient_id =patient_ID,Disease=Disease,Fever=Fever,Cough=Cough,Fatigue=Fatigue,
                                Difficulty_Breath=Difficulty_Breath,Age=Age,Gender=Gender,Blood_Pressure=Blood_Pressure,
                                Cholesterol_Level=Cholesterol_Level,Outcome_Variable=Outcome_Variable)
            dbo.session.add(new_patient)
            dbo.session.commit()
            return render_template('successful.html')

    return render_template('Addpatient.html')


@app.route('/updatepage',methods=['GET','POST'])
def updatepage():
    if request.method== "POST":
          pid = request.form.get('patient_ID')
          precord= patient.query.filter_by(patient_id=pid).first()
          if precord:
            return  redirect(url_for('updatepatient',Pid=pid))
          else:
            return render_template('invalid.html')
    return render_template('update_patient.html')
               


@app.route('/updatepatient/<string:Pid>',methods=['GET','POST'])
def updatepatient(Pid:str):
    patient_record= patient.query.filter_by(patient_id=Pid).first()
    if request.method == "POST":
            if patient_record:
                patient_record.Disease = request.form.get('Disease')
                patient_record.Fever = request.form.get('Fever')
                patient_record.Cough = request.form.get('Cough')
                patient_record.Fatigue = request.form.get('Fatigue')
                patient_record.Difficulty_Breath = request.form.get('Difficulty_Breath')
                patient_record.Age = int(request.form.get('Age',0))
                patient_record.Gender = request.form.get('Gender')
                patient_record.Blood_Pressure = request.form.get('Blood_Pressure')
                patient_record.Cholesterol_Level = request.form.get('Cholesterol_Level')
                patient_record.Outcome_Variable = request.form.get('Output_Variable')
                dbo.session.commit()
                return render_template('successful.html')
            return redirect(url_for('updatepage'))
            
    return render_template('updateform.html', patient=patient_record, Pid=Pid)



@app.route('/deletepage',methods=['GET','POST'])
def deletepage():
    if request.method== "POST":
          pid = request.form.get('patient_ID')
          precord= patient.query.filter_by(patient_id=pid).first()
          if precord:
            return  redirect(url_for('deleterecord',ID=pid))
          else:
            return render_template('invalid2.html')
    return render_template('deletepage.html')
         


@app.route('/deleterecord/<string:ID>',methods=['GET','POST'])
def deleterecord(ID:str):
    patient_record = patient.query.filter_by(patient_id=ID).first()
    if request.method == "POST":
        if patient_record:
                dbo.session.delete(patient_record)
                dbo.session.commit()
                return jsonify(Confirmation_Message='Patient record deleted successfully'),201
        else:
                return redirect(url_for('deletepage'))
            
    return render_template('confirmdelete.html',ID=ID)
            

@app.route('/')
def default_display():
    return render_template('default_display.html')
 
if __name__ == "__main__":
    app.run(debug=True)






