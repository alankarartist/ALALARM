import AlAlarm.AlTaskScheduler as ats
import os
import pyttsx3
import datefinder
import speech_recognition as sr 
import datetime
import subprocess

cwd = os.path.dirname(os.path.realpath(__file__))

def speak(audio):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    print(audio)
    engine.setProperty('voice', voices[0].id)
    engine.say(audio)
    engine.runAndWait()

def setAlarm(query):
    dateTimeAlarm = datefinder.find_dates(query)
    objAlarm = ''
    for match in dateTimeAlarm:
        objAlarm = match
    stringAlarm = str(objAlarm)
    timeAlarm = stringAlarm[11:]
    print(timeAlarm)
    splitTimeAlarm = timeAlarm.split(':')
    hourAlarm = (splitTimeAlarm[0])
    minuteAlarm = (splitTimeAlarm[1])
    return str(hourAlarm)+':'+str(minuteAlarm)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")    
        queryTask = r.recognize_google(audio, language='en-in')
        print(f"{queryTask}\n")
    except:
        print("Say that again please...")
        return "None"
    return queryTask

def AlSetAlarm(query):
    timeSet = setAlarm(query)
    pythonPath = subprocess.check_output('python -c "import sys; print(sys.executable)"').decode("utf-8").replace('\r\n','')
    pythonFilePath = os.path.join(cwd, 'AlAlarm.py')
    cmd = '"'+pythonPath+'" "'+pythonFilePath+'" "'+timeSet+'"'
    batFileName = "Alarm.bat"
    batFilePath = os.path.join(cwd+'\AlAlarm', batFileName)
    batFile = open(batFilePath, "w")
    batFile.write(cmd)
    batFile.close()
    vbsFileName = 'Alarm.vbs'
    vbsFilePath = os.path.join(cwd+'\AlAlarm', vbsFileName)
    vbsFileLines = ['Set WshShell = CreateObject("WScript.Shell")\n',f'WshShell.Run chr(34) & "{batFilePath}" & Chr(34), 0\n','Set WshShell = Nothing\n']
    vbsFile = open(vbsFilePath,'w')
    vbsFile.writelines(vbsFileLines)
    vbsFile.close()
    dateNow = datetime.datetime.now().strftime('%Y-%m-%d')
    alarmTime = dateNow+' '+timeSet
    alarmTimeObject = datetime.datetime.strptime(alarmTime, '%Y-%m-%d %H:%M')
    timeDiff = str(alarmTimeObject - datetime.datetime.now())
    if timeDiff.startswith('-'):
        alarmTimeObject = alarmTimeObject + datetime.timedelta(days=1)
    ats.scheduleTask('Alarm', vbsFilePath, alarmTimeObject)
    speak('alarm has been set at '+timeSet)

speak('At what time you want to set the alarm? Give time command in 12 hour format.')
query = takeCommand().lower()
query = 'set alarm at '+query
print(query)
AlSetAlarm(query)