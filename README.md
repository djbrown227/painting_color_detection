# Painting Color Detection Web Application

## Overview

This project provides a web application that allows users to upload an image and analyze the colors present within a grid overlay on the image. The application utilizes OpenCV for image processing and Flask for the web framework. The processed image, along with a detailed color analysis, is displayed to the user. Additionally, users can download the analysis results as a JSON file.

## Features

- **Image Upload and Analysis**: Supports JPEG, JPG, and PNG formats for uploading and analyzing images.
- **Grid Overlay Generation**: Automatically overlays a grid on the uploaded image and extracts color information from each grid cell.
- **Color Information Display**: Shows color details including RGB, Hex, and HSL values for each grid cell.
- **Processed Image Visualization**: Displays the original image and the processed image with contours highlighted.
- **Download Results**: Allows users to download the detailed color analysis results as a JSON file.

## Technologies Used

- **Flask**: Backend framework for handling HTTP requests and serving web pages.
- **OpenCV**: Library for image processing and grid overlay generation.
- **HTML/CSS**: Frontend development for creating the user interface.
- **Werkzeug**: Utility library for secure file handling and form data processing.

## How to Use

1. **Clone the repository:**

    ```sh
    git clone https://github.com/djbrown227/painting_color_detection.git
    cd painting_color_detection
    ```

2. **Create and activate a virtual environment:**

    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the required dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Run the Flask application:**

    ```sh
    python app.py
    ```

5. **Open your web browser and navigate to:**

    ```
    http://127.0.0.1:5000/
    ```

6. **Upload an image for analysis:**

    - Click the "Choose File" button and select a JPEG, JPG, or PNG image.
    - Click the "Upload" button to process the image.

7. **View the results:**

    - The original and processed images will be displayed.
    - The color legend and summary statistics will be shown.
    - Click the "Download JSON Data" link to download the analysis results.

## Project Structure

- `app.py`: The main Flask application file that handles image upload, processing, and result rendering.
- `uploads/`: Directory where uploaded and processed images are stored.
- `templates/`: HTML templates for rendering the upload and results pages.
- `static/`: Directory for static files such as CSS, JavaScript, and images.
- `requirements.txt`: List of Python packages required for the application.

## Future Improvements

- **Enhanced Image Processing**: Incorporate advanced color analysis techniques and more customizable grid settings.
- **User Interface Enhancements**: Improve the frontend design for a more interactive and visually appealing user experience.
- **Additional Export Options**: Support for exporting color data in various formats (e.g., CSV, Excel).
- **Performance Optimization**: Optimize image processing for faster performance with larger images and grids.
