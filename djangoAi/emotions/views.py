from django.shortcuts import render



# Create your views here.

from django.http import HttpResponse
from keras.models import load_model
# from tensorflow.keras.preprocessing import image
import numpy as np
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.uploadhandler import TemporaryFileUploadHandler
from .models import ImageFromModel
from PIL import Image
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from django.conf import settings


def upload(request):
    if request.method == 'POST' and request.FILES['file']:
        # get the uploaded file
        uploaded_file = request.FILES['file']
        image_name = uploaded_file.name
        # create the path where the file will be saved
        file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
        
        file_path = file_path.replace('\\', '/')

        image_url = request.build_absolute_uri(file_path)
       
        # write the file to the media directory
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        print(file_path)

        model_path = 'C:/Users/Elie/djangoAi/savedModels'
        model = load_model(model_path)
        img = Image.open(file_path)
        img = img.resize((100, 100))
        img = img.convert('RGB')
        # Convert the image to a numpy array
        img_array = np.array(img)
        
        # Add a fourth dimension to the image array
        img_array = np.expand_dims(img_array, axis=0)
        print(img_array[0].shape)
        # Use the predict method to make predictions on the preprocessed image
        prediction = model.predict(img_array)[0]

        predicted_label_index = np.argmax(prediction)

        if predicted_label_index == 1:
            msg = "You look angry today!"
        elif predicted_label_index == 2:
            msg = "You look disgusted today."
        elif predicted_label_index == 3:
            msg = "You look fearful today."
        elif predicted_label_index == 4:
            msg = "You look happy today!"
        elif predicted_label_index == 5:
            msg = "You look neutral today."
        elif predicted_label_index == 6:
            msg = "You look sad today."
        elif predicted_label_index == 7:
            msg = "You look surprised today."
        else:
            msg = "Sorry, I'm not sure what emotion you're showing right now."
        # render a success message
        return render(request, 'upload.html', {'message': 'File uploaded successfully.','link':image_name,"predicted":msg})

    # render the upload form
    return render(request, 'upload.html')