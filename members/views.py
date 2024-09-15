from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from requests import request
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm,SetPasswordForm
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_protect
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
import random

import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
# Create your views here.

#success_user = User.objects.create_user(account['user'],account['password'],account['email'],account['mobile'])
#Credential Accounts

account={}
otp_number = str(random.randint(100000, 999999))
detection ={}



from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def main(request):
    return render(request,"main.html")


def index(request):
    # If the login was unsuccessful or it's not a POST request, render the login page
    return render(request, 'index.html')


@csrf_protect   
def welcome(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
            
        user=authenticate(username=username,password=password)
        print(username,password)
        if user is not None:
           login(request,user)
           messages.success(request,"Welcome,You are Successfully Logged in!!!")
           return render(request,"dashboard.html")
        else:
            messages.error(request,"Username or Password is incorrect.Please try again..")
            return render(request,"error.html")
    
    return render(request,"index.html")

# Creating a Account
def register(request):
            
 return render(request,"signup.html")
        
        # Now Adding Some Conditions



real_news_samples = [
    "Study finds evidence of water on Mars.",
    "Stock market experiences record gains in the past quarter.",
    "President signs new bill into law to improve healthcare access.",
    "Researchers discover new species in the Amazon rainforest.",
    "Local community comes together to clean up the park.",
]

def train_classifier(fake_samples, real_samples):
    corpus = fake_samples + real_samples
    labels = ['fake'] * len(fake_samples) + ['real'] * len(real_samples)

    # Check if there are at least two unique classes in the training data
    unique_classes = set(labels)
    if len(unique_classes) < 2:
        print("Error: Need at least two classes in the training data.")
        return None, None

    vectorizer = TfidfVectorizer(max_features=1000)
    X = vectorizer.fit_transform(corpus)

    X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.2, random_state=42)

    classifier = LogisticRegression()
    classifier.fit(X_train, y_train)

    y_pred = classifier.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    detection['accuracy'] = accuracy
    print("Classifier Accuracy:", accuracy)

    return vectorizer, classifier

def get_article_text(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        article_text = ' '.join([p.get_text() for p in soup.find_all('div', class_='_1W5s')])
        return article_text
    except Exception as e:
        print("Error retrieving article text:", str(e))
        return None

def classify_news_article(article_text, vectorizer, classifier):
    try:
        X_article = vectorizer.transform([article_text])
        prediction = classifier.predict(X_article)
        return prediction[0]
    except Exception as e:
        print("Error classifying news article:", str(e))
        return 'fake'




def detect(request):

 if request.method=="POST":
    


    detection['values'] = request.POST.get('textarea')
    fake_samples_input = request.POST.get('textarea')
    fake_samples = [headline.strip() for headline in fake_samples_input.split(',')]

    vectorizer, classifier = train_classifier(fake_samples, real_news_samples)

    if vectorizer is not None and classifier is not None:
        news_url = "https://www.timesnownews.com/latest-news"
        article_text = get_article_text(news_url)

        if article_text:
            detection['article'] = article_text
            print("\nArticle Text:\n", article_text)

            classification = classify_news_article(article_text, vectorizer, classifier)

            detection['Classification'] = classification
            print("\nClassification: ", classification)
        else:
            print("Failed to retrieve article text. Please check the URL and try again.")

    return render(request,"success.html",detection)




def send_otp(request):
    if request.method == 'POST':

        account['user'] = request.POST.get("username")
        account['email']  = request.POST.get("email")
        account['mobile'] = request.POST.get("mobile")
        account['password'] = request.POST.get("password")
        account['repassword'] = request.POST.get("confirmPassword")
        account['method'] = request.POST.get('Verification')

        credential = {'name':account['user'],'email':account['email'],'mobile':account['mobile'],'password':account['password'],'repassword':account['repassword'],'method':account['method']}
        # Open the file in write mode
        with open('credential.txt', 'w') as file:
        # Write the content to the file
            file.write(str(credential))
        
        if account['method'] == 'email':
            # Your email credentials
            fromaddr = "anakeerth00@gmail.com"
            toaddr = request.POST.get("email")
            smtp_password = "ynjy hqya srqz vthz"

            # Create a MIMEMultipart object
            msg = MIMEMultipart()

            # Set the sender and recipient email addresses
            msg['From'] = fromaddr
            msg['To'] = toaddr
            
            # Set the subject
            msg['Subject'] = "Fake New Otp Verification"

            # Set the email body
            body = f"Your OTP is: {otp_number}"
            msg.attach(MIMEText(body, 'plain'))

            try:
                # Connect to the SMTP server
                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    # Start TLS for security
                    server.starttls()

                    # Log in to the email account
                    server.login(fromaddr, smtp_password)

                    # Send the email
                    server.sendmail(fromaddr, toaddr, msg.as_string())

                # Email sent successfully, render a template
                return render(request, 'verification_otp.html')

            except Exception as e:
                # An error occurred while sending email, redirect with an error message
                messages.error(request, f"Error sending OTP email: {e}")
                return render(request,'signup.html')  # You need to replace 'verify_it' with the appropriate URL name
        else:
            # Invalid method, redirect with an error message
            messages.error(request, "Invalid verification method")
            return render(request,'signup.html')  # You need to replace 'verify_it' with the appropriate URL name

    # If the request method is not POST, redirect with an error message
    messages.error(request, "Invalid request method")
    return render(request,'signup.html') # You need to replace 'verify_it' with the appropriate URL name


def verify_it(request):
    
    if request.method=="POST":


       

        verifi_otp1 = request.POST.get("otp1")
        verifi_otp2 = request.POST.get("otp2")
        verifi_otp3 = request.POST.get("otp3")
        verifi_otp4 = request.POST.get("otp4")
        verifi_otp5 = request.POST.get("otp5")
        verifi_otp6 = request.POST.get("otp6")

        six_digits=f"{verifi_otp1}{verifi_otp2}{verifi_otp3}{verifi_otp4}{verifi_otp5}{verifi_otp6}"
        if six_digits==otp_number:

         my_user=User.objects.create_user(account['user'],account['email'],account['password'])
         my_user.save() 
         messages.success(request,"Your account has been Created Successfully!!!")
         redirect(index)


        # else:
        #     messages.success(request,"Registration Failed!!")
        #     return render(request, 'success.html',six_digits)
        
    return render(request,"index.html")  



""" "Scientists confirm that aliens have landed on Earth!",
    "Breaking: New study claims that eating chocolate can make you lose weight!",
    "Government officials caught in massive corruption scandal!",
    "Famous celebrity spotted with a unicorn in their backyard!",
    "Breaking: Giant asteroid on collision course with Earth!",
    """


