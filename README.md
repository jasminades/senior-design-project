## neuroscan

neuroscan is a web-based application that allows users to upload MRI images and receive AI-based predictions on dementia stages.
the project combines deep learning models to analyze brain scans and provides visual expalanation using Grad-CAM heatmaps.

features
  - MRI upload and analysis - a dashboard for uploading MRI images for dementia classification
  - AI prediction - predicts one of four dementia stages: Non-Demented, Very-Mild Demented, Mild Demented and Moderate Demented
  - confidence scroes - each prediction includes a confidence score (0-100%)
  - Grad-CAM heatmaps - visual representation of detected patterns relevant to the analysis
  - history table - stores previous analyses on the user's profile page


technologies 
  - backend
      - Python
      - Flask (REST API)
      - TensorFlow / Keras
      - OpenCV
      - NumPy
      - MySQL
      - Flask-CORS
   
  - frontend
      - Vue.js 3
      - Vuetify 3
      - Axios
