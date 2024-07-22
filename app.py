from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import cv2
import colorsys
import webcolors
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def analyze_grid(original_image_path):
    image = cv2.imread(original_image_path)
    
    # Convert BGR to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Threshold the image to create a binary image
    _, thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)
    
    # Find contours in the binary image
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Draw contours on original image for visualization
    image_with_contours = image.copy()
    cv2.drawContours(image_with_contours, contours, -1, (0, 255, 0), 2)
    
    # Extract color information from contours
    grid_colors = []
    grid_size = 200  # Size of the grid
    height, width = gray.shape
    cell_height = height // grid_size
    cell_width = width // grid_size
    
    color_frequency = {}
    
    for i in range(grid_size):
        for j in range(grid_size):
            # Define coordinates for the current grid cell
            x1 = j * cell_width
            y1 = i * cell_height
            x2 = (j + 1) * cell_width
            y2 = (i + 1) * cell_height
            
            # Extract color of the grid cell
            cell_image = image[y1:y2, x1:x2]
            mean_color = cv2.mean(cell_image)[:3]
            mean_color = tuple([int(x) for x in mean_color])
            
            # Convert RGB to HSL using colorsys.rgb_to_hls
            r, g, b = mean_color
            h, l, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
            
            # Get hex color representation
            hex_color = webcolors.rgb_to_hex((r, g, b))
            
            # Update color frequency
            if hex_color in color_frequency:
                color_frequency[hex_color] += 1
            else:
                color_frequency[hex_color] = 1
            
            # Append color information to grid_colors list
            grid_colors.append({
                'position': (i, j),
                'rgb': mean_color,
                'hex': hex_color,
                'hsl': (int(h * 360), int(s * 100), int(l * 100))
            })
    
    # Save processed image with contours
    processed_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'processed_' + os.path.basename(original_image_path))
    cv2.imwrite(processed_image_path, cv2.cvtColor(image_with_contours, cv2.COLOR_RGB2BGR))
    
    # Summary statistics
    unique_colors = len(color_frequency)
    most_frequent_colors = sorted(color_frequency.items(), key=lambda item: item[1], reverse=True)
    
    summary = {
        'total_cells': grid_size * grid_size,
        'unique_colors': unique_colors,
        'most_frequent_colors': most_frequent_colors
    }
    
    # Combine grid color data and summary statistics
    result_data = {
        'grid_colors': grid_colors,
        'summary': summary
    }
    
    # Save result data to a JSON file
    json_path = os.path.join(app.config['UPLOAD_FOLDER'], 'result_data.json')
    with open(json_path, 'w') as json_file:
        json.dump(result_data, json_file, indent=4)
    
    return grid_colors, processed_image_path, json_path, result_data


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            grid_colors, processed_image_path, json_path, result_data = analyze_grid(file_path)
            return render_template('results.html', 
                                   original_image=file_path, 
                                   processed_image=processed_image_path, 
                                   grid_colors=grid_colors, 
                                   json_path=json_path, 
                                   summary=result_data['summary'],
                                   os=os)  # Pass os module to template context
    return render_template('upload.html')

@app.route('/uploads/<filename>')
def send_uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/download_json')
def download_json():
    json_path = request.args.get('json_path')
    if json_path and os.path.exists(json_path):
        return send_from_directory(app.config['UPLOAD_FOLDER'], os.path.basename(json_path), as_attachment=True)
    return "JSON file not found", 404

if __name__ == '__main__':
    app.run(debug=True)
