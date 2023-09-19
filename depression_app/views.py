from django.shortcuts import render
from django.http import JsonResponse
from .utils import question
from django.http import HttpResponse
from django.shortcuts import render
import os
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import numpy as np
import cv2
import os
from keras.models import load_model
from keras.utils import img_to_array
import numpy as np
import time
emotion_score = 0
from .import prediction
# from .models import model, haarcascade_frontalface_default

normal_symptoms=['hopeless','frustration','weight','insomnia']
critical_symptom=['suicide','lost_interest']
other_symptoms=['Past','Family']

def first_page(request):
    return render(request,'depression_app/firstpage.html')

def secondpage(request):
    if request.method == 'POST':
        textarea_value = request.POST.get('my_textarea') 
        pure_text =[textarea_value]
        rslt=prediction.text_predict(pure_text)
        if (rslt == 1):
            request.session['situation_result']= 20
    return render(request,'depression_app/secondpage_test.html')

def about(request):  
    return render(request,'depression_app/about.html')

def game(request): 
    global emotion_score 
    print("value of emotion = ",emotion_score)
    return render(request,'depression_app/game.html')

def my_view(request):
    data = question()
    return HttpResponse(data)

def result_view(request):
    global emotion_score

    a = request.session.get('game_result')
    b = emotion_score
    c = request.session.get('clinical_result')
    d = request.session.get('situation_result')

    a = a or 0
    b = b or 0
    c = c or 0
    d = d or 0

    result = a + b + c + d
    no_symptom = result / 20
    symptom_percentage = int((no_symptom /11)*100)
    print("total score =", result)
    result = int((result / 180) * 100)
    if (result > 50):
        mssg ="You Have High Symptoms Of Depression."
    elif (result < 50):
        mssg ="You Have Low Symptoms Of Depression."
    elif (result == 0):
        mssg ="You Dont Have Any Symptoms Of Depression."

    context = {
        'my_session_variable': result,
        'answered_percentage': symptom_percentage,
        'depression_message': mssg,
    }

    return render(request, 'depression_app/result.html', context)




    # s=request.session.get('dep_score')
    # print('total score is  ',s) 
    # return render(request,'depression_app/result.html')


# def initialize_score(request):
#     request.session['dep_score'] = 0


    

def question_page(request):
    score=0
    if request.method == 'POST':
        for i in normal_symptoms:
            selected_option = request.POST.get(i)
            if (selected_option == 'Everytime'):
                score += 10
            elif (selected_option == 'Sometimes'):
                score+=5
        for i in critical_symptom:
            selected_option = request.POST.get(i)
            if (selected_option == 'Everytime'):
                score +=20
            elif (selected_option == 'Sometimes'):
                score+=10

        for i in other_symptoms:
            selected_option = request.POST.get(i)
            if (selected_option == 'Yes'):
                score += 20
        request.session['clinical_result']=score
        # s=request.session.get('dep_score')
        # print('score after is  ',s)
        
           
    return render(request,'depression_app/questions_page.html')



base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


xml_file_path = os.path.join(base_dir, 'depression_app', 'mlmodel', 'haarcascade_frontalface_default.xml')
h5_file_path = os.path.join(base_dir, 'depression_app', 'mlmodel', 'model.h5')


face_classifier = cv2.CascadeClassifier(xml_file_path)

classifier = load_model(h5_file_path)


# face_classifier = cv2.CascadeClassifier('./mlmodel/haarcascade_frontalface_default.xml')
# classifier = load_model('./mlmodel/model.h5')
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

# Function to perform emotion detection
import time

def detect_emotion():
    cap = cv2.VideoCapture(0)
    start_time = time.time()
    show_camera = False  # Flag to control camera view visibility
    
    while True:
        _, frame = cap.read()
        labels = []
        
        if show_camera:
            cv2.imshow('Camera', frame)
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray)
        
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)
            
            if np.sum([roi_gray]) != 0:
                roi = roi_gray.astype('float') / 255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi, axis=0)
                
                prediction = classifier.predict(roi)[0]
                label = emotion_labels[prediction.argmax()]
                label_position = (x, y)
                cv2.putText(frame, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                if label == "Sad" or label == "Angry":
                    global emotion_score
                    emotion_score = 20
                    # print('sadness is ',emotion_score)
                    break
            else:
                cv2.putText(frame, 'No Faces', (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        _, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        
        if time.time() - start_time >= 5:
            break
    
    cap.release()
    cv2.destroyAllWindows()


    cap.release()

        
def emotion_detection_page(request):
    # if (emotion_score == True):
    #     request.session['dep_score']+=20
    # a=request.session.get('dep_score')
    # print('second page value is ',a)
    return render(request, 'depression_app/emotion.html')


# Decorator to enable video streaming
@gzip.gzip_page
def live_emotion_detection(request):
    try:
        return StreamingHttpResponse(detect_emotion(), content_type='multipart/x-mixed-replace; boundary=frame')
    except Exception as e:
        print("An error occurred: " + str(e))

@csrf_exempt
def update_session_variable(request):
    request.session['game_result'] =0
    if request.method == 'POST' and request.is_ajax():
        variable_value = request.POST.get('flips')
        request.session['game_result'] = variable_value
        request.session.modified = True
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})
    



