from flask import Flask,render_template,request
import os
import sys

app = Flask(__name__)
index=0
image_list=None
base_directory=None
image_name=None
current_index=0
coordinates_dict={}
filename="path_coordinates.csv"

@app.route("/")
def index():
    global current_index
    current_index=0
    return render_template("index.html")


@app.route("/view", methods=["POST"])
def view():
    global current_index,image_list,image_name
    base_directory="static"
    image_list = os.listdir(base_directory)
    print(image_list)
    image_name=image_list[current_index]
    return render_template("render_image.html",image_path=image_name)


@app.route("/next", methods=["POST"])
def next():
    global current_index,image_name,image_list
    coordinates_dict[image_name] = (request.form['normalized_x'], request.form['normalized_y'])
    current_index += 1
    if current_index==len(image_list):
        write_values(coordinates_dict)
        return "Results successfully written to file"
    image_name = image_list[current_index]
    return render_template("render_image.html",image_path=image_name)

def write_values(coordinates_dict):
    target_file=open(filename,'w')
    target_file.write("image_name,normalized_x,normalized_y\n")
    for key,value in coordinates_dict.items():
        target_file.write("{0},{1},{2}\n".format(key,value[0],value[1]))
    target_file.close()

if __name__ == '__main__':
    app.run()