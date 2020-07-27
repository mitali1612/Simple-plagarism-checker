'''
Author: Mitali Unde
**SIMPLE PLAGARISM CHECKER**
The main function of this application is to upload two text files from the user
store it in folder and then compare them textually to find the similarity
between them using cosine similarity.
'''
import os, fnmatch
from app import app
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
import math
import re

ALLOWED_EXTENSIONS = set(['txt'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/index', methods=['POST'])
def upload_file():
    '''
    This method is used to upload the files given as user input into the local
    directory.

    '''
    if request.method == 'POST':
        delete()

        # check if the post request has the files part
        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)
        files = request.files.getlist('files[]')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


        return render_template('index.html')



@app.route('/output', methods=['POST'])
def cosineSimilarity():
    '''
    This method reads the uploaded text files, removes punctuation marks from
     it ,term frequencies are calculated and then cosine similarity between the
     two files is calculated to find similarity between them.
    :return: cosine similarity
    '''
    if request.method == 'POST':
        res = find('*.txt', './uploads')
        universalSetOfUniqueWords = []

        fd1 = open(res[0], "r")
        file1 = fd1.read().lower()

        file1WordList = re.sub("[^\w]", " ", file1).split()
        for word in file1WordList:
            if word not in universalSetOfUniqueWords:
                universalSetOfUniqueWords.append(word)


        fd2 = open(res[1], "r")
        file2 = fd2.read().lower()

        file2WordList = re.sub("[^\w]", " ", file2).split()

        for word in file2WordList:
            if word not in universalSetOfUniqueWords:
                universalSetOfUniqueWords.append(word)


        file1TF = []
        file2TF = []

        for word in universalSetOfUniqueWords:
            file1Counter = 0
            file2Counter = 0

            for word2 in file1WordList:
                if word == word2:
                    file1Counter += 1
            file1TF.append(file1Counter)

            for word2 in file2WordList:
                if word == word2:
                    file2Counter += 1
            file2TF.append(file2Counter)

        dotProduct = 0
        for i in range(len(file1TF)):
            dotProduct += file1TF[i] * file2TF[i]

        file1VectorMagnitude = 0
        for i in range(len(file1TF)):
            file1VectorMagnitude += file1TF[i] ** 2
        file1VectorMagnitude = math.sqrt(file1VectorMagnitude)

        file2VectorMagnitude = 0
        for i in range(len(file2TF)):
            file2VectorMagnitude += file2TF[i] ** 2
        file2VectorMagnitude = math.sqrt(file2VectorMagnitude)

        matchPercentage = (float)(dotProduct / (file1VectorMagnitude * file2VectorMagnitude)) * 100


        output = "The uploaded files have similarity of %0.02f%% " % matchPercentage

        return render_template('output.html', output=output)

def find(pattern, path):
    '''
    This method finds the text files uploaded by user at the given location
    :param pattern: regex pattern for finding file with particular extention
    :param path: path of the file

    '''
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))


    return result

def delete():
    '''
    This method is used to flush the already existing text files.

    '''
    mypath = "./uploads"
    for root, dirs, files in os.walk(mypath):
        for file in files:
            os.remove(os.path.join(root, file))


if __name__ == "__main__":
    app.run()