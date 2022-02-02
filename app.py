import os
from PIL import Image
from flask import Flask, render_template, request, redirect, send_file
from ocr_core import ocr_core

UPLOAD_FOLDER = '/static/uploads/' # https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
# The UPLOAD_FOLDER is where we will store the uploaded files
# ALLOWED_EXTENSIONS is the set of allowed file extensions.

list = [] #blank list which is used later in the code

app = Flask(__name__) # it is a flask constructor used to instantiating the object ie app

def allowed_file(filename): # https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
    #if filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS # rsplit splits the filename by '.' only once since maxsplit parameter = 1
    """else:
        print("anmaya")
        return redirect("http://localhost:5000/reset")"""

@app.route('/reset', methods=['GET']) # this method is used to clear the list and the txt file
def test():
    if request.method == 'GET':
        f = open("extracted_text.txt", "r+") #opening the file for reading and writing using the os library r+ signifies that we can update the file
        f.seek(0)
        f.truncate()
        list.clear()
        return redirect("http://localhost:5000/") # redirecting the browser to app route /


@app.route('/return-files')
def return_files_tut():
		return send_file('F:\College\Semester 4\Programming Language\Project\extracted_text.txt', attachment_filename='extracted_text.txt', cache_timeout = -1) #we are returning the extracted_text text file that is in our project folder and which has all the current data the cache timeout is set to -1 so that the page doesn't cache

@app.route('/', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':

        if 'file' not in request.files: # check if the post request has the file part
            return render_template('upload.html', msg='No file selected')

        file = request.files['file']

        if file.filename == '': # if user does not select file, browser also submit a empty part without filename
            return render_template('upload.html', msg='No file selected')

        if file and allowed_file(file.filename):
            file.save(os.path.join(os.getcwd() + UPLOAD_FOLDER, file.filename)) #saving the file chosen by the user in the upload folder

            """test = (os.path.join(os.getcwd() + UPLOAD_FOLDER, file.filename))
            print("test address - ",test )
            extracted_text = ocr_core(test)"""

            extracted_text = ocr_core(file) # call the OCR function on it
            print(type(file))

            list.append(extracted_text) # appending the recognized test in the blank list that we created earlier
            listToStr = ' '.join(map(str, list)) # converting that list into a string using the join funcion

            f = open("extracted_text.txt", "r+") #delete previous data in the text file
            f.seek(0)
            f.truncate()

            #insert data in the file
            f = open("extracted_text.txt","a+") # open the text file in append mode so that we can append the string in it
            f.write(listToStr) # append the string in the text file
            # extract the text and display it
            return render_template('upload.html',
                                   msg='Successfully processed',
                                   extracted_text=listToStr,
                                   img_src=UPLOAD_FOLDER + file.filename) #return the render template with all the necessary info
        else:
            return render_template('upload.html', msg='Please select an Image File (.jpg)(.png)(.jpeg)')
            
    elif request.method == 'GET':
        return render_template('upload.html')

if __name__ == '__main__': # It checks whether the module is being run by itself not being imported by some other module
    app.run() # The run() method runs the application on the local development server.
    #https://medium.com/python-features/understanding-if-name-main-in-python-a37a3d4ab0c3
