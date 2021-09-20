import boto3
import os
import csv
from flask import Flask, request, jsonify, _request_ctx_stack, session, Response, send_file
from flask_restful import Api
from flask_cors import CORS
from datetime import datetime
from zipfile import ZipFile
import io
app = Flask(__name__)
CORS(app)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
api = Api(app)

@app.route("/ping", methods=['GET'])
def ping():
    return jsonify({"status": 'successful'}), 200

'''
Get list of all images from S3 bucket, send as json response
'''
@app.route("/api/public/getListOfImages", methods=['POST'])
def getListOfImages():
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('ceres-technical-challenge') 
    image_list = []
    for bucket_object in bucket.objects.all():
        if(bucket_object.key != "metadata.txt"):
            image_list.append(bucket_object.key)
    return jsonify({"status": 'successful', 'list': image_list}), 200   

'''
Download image by returning presigned url from s3 via boto3
'''
@app.route("/api/public/downloadImage", methods=['POST'])
def downloadImage():
    post_data = request.get_json();
    s3_client = boto3.client('s3')
    image_list = []
    response = s3_client.generate_presigned_url('get_object',Params={'Bucket': 'ceres-technical-challenge', 'Key': post_data['file_name']},ExpiresIn=None)
    return jsonify({"status": 'successful', 'img_url': response}), 200  

'''
Get the corresponding metadata by matching the image file name given with that in the metadata 
'''
@app.route("/api/public/getMetadataOfImage", methods=['POST'])
def getMetadataOfImage():
    post_data = request.get_json();
    image_file_name = post_data['file_name']    
    file_metadata = "None" #return none if not found for some reason
    s3_client = boto3.client('s3')
    s3_client.download_file('ceres-technical-challenge', "metadata.txt", "metadata.txt")    
    with open("metadata.txt") as tsv:
        csv_reader = csv.reader(tsv, delimiter="\t")
        header =  next(csv_reader) 
        for line in csv_reader: 
            if(line[0] == image_file_name):
                file_metadata = {}
                for i in range(len(header)):
                    file_metadata[header[i]] = line[i] 
    return jsonify({"status": 'successful', 'metadata': str(file_metadata)}), 200

'''
Get list of images within the begin time and end time given, which are two millisecond values.
The begin time and end time are added to the 2020-06-01 17:41:07.000000+00:00 value as a timestamp 
'''
@app.route("/api/public/getListOfImagesInTime", methods=['POST'])
def getListOfImagesInTime():
    post_data = request.get_json();
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('ceres-technical-challenge')
    s3_client = boto3.client('s3')
    s3_client.download_file('ceres-technical-challenge', "metadata.txt", "metadata.txt")      
    begin_time = post_data['begin_time']
    begin_str = str(begin_time)
    if(begin_str.isdigit() == False):
        begin_time = 0
    end_time = post_data['end_time']
    end_str = str(end_time)
    if(end_str.isdigit() == False):
        end_time = 0       
    base_time = datetime.fromisoformat("2020-06-01 17:41:07.000000+00:00")
    base_ticks = int(base_time.timestamp())
    begin_ticks = float(begin_time)/1000 + base_ticks
    end_ticks = float(end_time)/1000 + base_ticks
    image_list = []
    if(end_ticks < begin_ticks): #if input is invalid, return an empty list
        return jsonify({"status": 'successful', 'img_list': image_list}), 200
    else:    
        with open("metadata.txt") as tsv:
            csv_reader = csv.reader(tsv, delimiter="\t")
            next(csv_reader)
            for line in csv_reader:
                new_date = datetime.fromisoformat(line[13])
                date_ticks = int(new_date.timestamp())
                if((begin_ticks <= date_ticks) and (date_ticks <= end_ticks)):
                    image_list.append(line[0])
        return jsonify({"status": 'successful', 'img_list': image_list}), 200

'''
Gets the zip of all the images.
Downloads everything to the local disk from boto3, then writes it all to a zip file, and sends it down.
Deletes everything on the local disk afterwards.
'''
@app.route("/api/public/getZipOfAllImages", methods=['GET', 'POST'])
def getZipOfAllImages():
    if (os.path.exists('images.zip')):
        os.remove('images.zip')
    s3 = boto3.resource('s3')
    s3_client = boto3.client('s3')
    bucket = s3.Bucket('ceres-technical-challenge') 
    image_list = []
    for bucket_object in bucket.objects.all():
        s3_client.download_file('ceres-technical-challenge', bucket_object.key, bucket_object.key)
    path = os.getcwd()
    file_paths = []
    for file_name in os.listdir(path):
        if(file_name != 'image_api.py' and file_name != 'requirements.txt' and file_name != 'env'):
            file_paths.append(file_name)
    memory_file = io.BytesIO()       
    with ZipFile(memory_file,'w') as zip:
        # writing each file one by one
        for file in file_paths:
            zip.write(file)
    for file in file_paths:
        if os.path.exists(file):
            os.remove(file)
    memory_file.seek(0)        
    return Response(memory_file.getvalue(), mimetype='application/zip', headers={'Content-Disposition': 'attachment;filename=images.zip'})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=3334,debug=True)