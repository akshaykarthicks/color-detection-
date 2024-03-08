from flask import Flask, render_template, request
import cv2
import pandas as pd
import numpy as np

app = Flask(__name__)

# Reading CSV file with Pandas and giving names to each column
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv(r"C:\Users\aksha\Downloads\COLOR DETECTION\colors.csv", names=index, header=None)
print("CSV file loaded successfully.")

# Function to calculate minimum distance from all colors and get the most matching color
def get_color_name(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/color_detect', methods=['POST'])
def color_detect():
    if 'image' in request.files:
        file = request.files['image']
        img_bytes = file.read()
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        x = int(request.form['x'])
        y = int(request.form['y'])
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)
        color_info = get_color_name(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
        return color_info
    return "No image uploaded or click event not triggered."

if __name__ == '__main__':
    app.run(debug=True)
