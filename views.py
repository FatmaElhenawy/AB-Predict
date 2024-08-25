import json
import logging
from logging import exception
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.template import Context
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import joblib
import numpy as np
from django.http import JsonResponse
import os
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.utils import register_keras_serializable
from .models import *
from .encoding import precompute_encoding, encode_features
from django.db.models import Q

def index(response):
    
    return render(response, 'myApp/base.html' )

def home(response):
    return render(response, 'myApp/home.html')

def home_log(response):
    return render(response, 'myApp/home-log.html')


def sign(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created successfully!')       
    else:
        form = UserRegisterForm()
    
    context = {'form': form}
    return render(request, 'myApp/sign.html', context)

def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        context = {}

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return render(request,'myApp/home-log.html')
        else:
            messages.info(request, 'Username or password is incorrect')
            return render(request, 'myApp/login.html', context)
        
    context = {}

    return render(request,'myApp/login.html', context )

def logoutUser(request):
    logout(request)
    return redirect('myApp:Login')

logger = logging.getLogger(__name__)
@login_required(login_url='myApp:Login')
def history(request):
    query_input_data = request.GET.get('input_data', '')
    query_description = request.GET.get('description', '')
    query_prediction_date = request.GET.get('prediction_date', '')
    
    filters = Q(user=request.user)

    if query_input_data:
        filters &= Q(input_data__icontains=query_input_data)
    
    if query_description:
        filters &= Q(Description__icontains=query_description)
    
    if query_prediction_date:
        filters &= Q(prediction_date__date=query_prediction_date)
    
    user_history = PredictionHistory.objects.filter(filters).order_by('-prediction_date')
    
    for record in user_history:
        logger.debug(f"Raw input_data: {record.input_data}")
        try:
            record.input_data = json.loads(record.input_data) 
            logger.debug(f"Parsed input_data: {record.input_data}")
        except json.JSONDecodeError as e:
            logger.error(f"JSONDecodeError: {e}")
            record.input_data = {} 
    
    context = {
        'history': user_history,
        'query_input_data': query_input_data,
        'query_description': query_description,
        'query_prediction_date': query_prediction_date,
    }
    return render(request, 'myApp/history.html', context)

#to load the model's pkl files:
integer_encoder = joblib.load('myApp/integer_encoder.pkl')
one_hot_encoder = joblib.load('myApp/one_hot_encoder.pkl')
cnn_model = load_model('myApp/1CNNup90.h5')
parameters = joblib.load('myApp/parameters.pkl')

columns_of_interest = ['H_CDR1', 'H_CDR2', 'H_CDR3', 'L_CDR1', 'L_CDR2', 'L_CDR3', 'Epitope']
max_lens = parameters['max_lens']
num_features = parameters['num_features']

#encoding
def encode_sequence(sequence):
    integer_encoded = integer_encoder.transform(list(sequence))
    integer_encoded = np.array(integer_encoded).reshape(-1, 1)
    one_hot_encoded = one_hot_encoder.transform(integer_encoded)
    return one_hot_encoded

#padding
def custom_pad_sequences(sequences, maxlen, num_features):
    padded_sequences = np.zeros((len(sequences), maxlen, num_features), dtype='float32')
    for i, seq in enumerate(sequences):
        length = min(len(seq), maxlen)
        #pad the sequence to the maxlen and number of features
        padded_seq = np.zeros((maxlen, num_features), dtype='float32')
        padded_seq[:length, :seq.shape[1]] = seq[:length]
        padded_sequences[i] = padded_seq
    return padded_sequences

#preprocessing
def preprocess_input(input_data, columns_of_interest, global_max_len, num_features):
    encoded_features = []
    for col in columns_of_interest:
        maxlen_for_col = global_max_len[col]
        encoded_col = [encode_sequence(seq) for seq in input_data[col]]
        padded_col = custom_pad_sequences(encoded_col, maxlen=maxlen_for_col, num_features=num_features)
        encoded_features.append(padded_col)
    input_features = np.concatenate(encoded_features, axis=1)
    return input_features
    

def predict(request):
    if integer_encoder is None or one_hot_encoder is None or cnn_model is None or parameters is None:
        return JsonResponse({'error': 'model files not loaded correctly'}, status=500)
    if request.method == 'POST':
        form = userInputForm(request.POST)

        if form.is_valid():
            columns_of_interest = ["H_CDR1", "H_CDR2", "H_CDR3", "L_CDR1", "L_CDR2", "L_CDR3", "Epitope"]
            input_data = form.cleaned_data
            Description = input_data.pop('Description', '')

            new_data = {
                'H_CDR1': [input_data['H_CDR1']],
                'H_CDR2': [input_data['H_CDR2']],
                'H_CDR3': [input_data['H_CDR3']],
                'L_CDR1': [input_data['L_CDR1']],
                'L_CDR2': [input_data['L_CDR2']],
                'L_CDR3': [input_data['L_CDR3']],
                'Epitope': [input_data['Epitope']]
            }
            new_df = pd.DataFrame(new_data)
            columns_of_interest = ['H_CDR1', 'H_CDR2', 'H_CDR3', 'L_CDR1', 'L_CDR2', 'L_CDR3', 'Epitope']
            preprocessed_new_input = preprocess_input(new_df, columns_of_interest, max_lens, num_features)

            new_predictions = (cnn_model.predict(preprocessed_new_input) > 0.5).astype(int)
            prediction = 'Yes' if new_predictions[0][0] == 1 else 'No'

            if request.user.is_authenticated:
                PredictionHistory.objects.create(
                    user=request.user,
                    input_data=json.dumps(new_data), 
                    Description=Description,
                    prediction_result=str(prediction)
                )

            return render(request, 'myApp/model_one.html', {'form': form, 'prediction': prediction})
        else:
            return JsonResponse({'error': 'Form data is not valid'}, status=400)
    else:
        form = userInputForm()
    return render(request, 'myApp/model_one.html', {'form': form})



#custom metric definition
@register_keras_serializable(package='Custom', name='mse')
def mse(y_true, y_pred):
    return MeanSquaredError()(y_true, y_pred)

#custom objects for model loading
custom_objects = {'mse': mse}

#to load the model
model = load_model('myApp/my_modelBigDataNN.h5', custom_objects=custom_objects)


def predictBigData(request):
    if request.method == 'POST':
        form = userInputForm2(request.POST)

        if form.is_valid():
            input_data = {key: value for key, value in form.cleaned_data.items() if key != 'Description'}
            Description = form.cleaned_data.get('Description', '')
            try:
                df = pd.DataFrame({
                    'Type': [input_data['Type']],
                    'CDR': [int(input_data['CDR'])],
                    'BWindow': [input_data['BWindow']],
                    'AWindow': [input_data['AWindow']],
                    'BSol': [input_data['BSol']],
                    'ASol': [input_data['ASol']],
                    'BSec': [input_data['BSec']],
                    'ASec': [input_data['ASec']]
                })

                precompute_encoding(df, sides='AB', verbose=False)
                X_new = encode_features(df, verbose=False)
                y_new_pred = model.predict(X_new)

                y_pred_binary = (y_new_pred > 0.5).astype(int)
                prediction = int(y_pred_binary[0][0])
                prediction = 'Yes' if prediction == 1 else 'No'

                if request.user.is_authenticated:
                    PredictionHistory.objects.create(
                        user=request.user,
                        input_data=json.dumps(input_data),
                        Description=Description,
                        prediction_result=str(prediction)
                    )

                return render(request, 'myApp/model_two.html', {'form': form, 'prediction': prediction})

            except KeyError as e:
                return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)

        else:
            return JsonResponse({'error': 'Form data is not valid'}, status=400)

    else:
        form = userInputForm2()
        return render(request, 'myApp/model_two.html', {'form': form})
    
def mainPrediction(request):
    return render(request, 'myApp/predictionM.html')
