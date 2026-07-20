# Government Scheme Predictor

An intelligent Machine Learning-powered web application that helps citizens discover eligible government welfare schemes based on their demographic and socioeconomic profile.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green)
![ML](https://img.shields.io/badge/ML-Random%20Forest-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📋 Project Overview

The Government Scheme Predictor addresses the challenge of information asymmetry in government welfare programs. Many eligible citizens miss out on benefits due to lack of awareness about schemes they qualify for. This project uses Machine Learning (Random Forest classification) to analyze user profiles and predict the most suitable government schemes from a database of 15+ welfare programs.

### Key Features

- **ML-Powered Predictions**: Uses Random Forest algorithm for accurate scheme recommendations
- **Instant Results**: Get scheme predictions in seconds with confidence scores
- **User-Friendly Interface**: Professional Bootstrap 5 based responsive design
- **Comprehensive Coverage**: Supports 15+ government welfare schemes
- **Real-time Validation**: Client-side and server-side form validation
- **Error Handling**: Robust error handling with user-friendly messages
- **Mobile Responsive**: Fully responsive design for all devices

## 🏗️ Technology Stack

### Backend
- **Python 3.8+**: Core programming language
- **Flask 3.0.0**: Web framework
- **scikit-learn 1.3.2**: Machine learning library
- **pandas 2.1.4**: Data manipulation
- **numpy 1.26.2**: Numerical computing
- **joblib 1.3.2**: Model serialization

### Frontend
- **HTML5**: Markup language
- **CSS3**: Styling
- **Bootstrap 5.3.2**: UI framework
- **JavaScript**: Client-side scripting
- **Bootstrap Icons**: Icon library

## 📁 Folder Structure

```
GovernmentSchemePredictor/
│
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
│
├── scheme_model.pkl            # Trained ML model (to be added)
├── encoders.pkl                # Label encoders (to be added)
├── feature_columns.pkl        # Feature column names (to be added)
│
├── templates/                  # HTML templates
│   ├── base.html              # Base template with navbar/footer
│   ├── index.html             # Home page with prediction form
│   ├── result.html            # Results display page
│   ├── about.html             # About page
│   ├── contact.html           # Contact page
│   ├── error.html             # Generic error page
│   └── 404.html               # 404 not found page
│
├── static/                     # Static assets
│   ├── css/
│   │   └── style.css          # Custom CSS styling
│   ├── js/
│   │   └── script.js          # Client-side JavaScript
│   └── images/
│       ├── logo.png           # Application logo (to be added)
│       └── banner.jpg         # Banner image (to be added)
│
└── utils/                      # Utility modules
    └── preprocess.py          # Data preprocessing utilities
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step-by-Step Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/GovernmentSchemePredictor.git
   cd GovernmentSchemePredictor
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Unix/MacOS
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add model files**
   
   Before running the application, you need to add the trained model files:
   - `scheme_model.pkl` - Trained Random Forest model
   - `encoders.pkl` - Label encoders for categorical features
   - `feature_columns.pkl` - List of feature column names
   
   These files should be generated from your Jupyter Notebook training script using:
   ```python
   import joblib
   
   # Save the trained model
   joblib.dump(model, 'scheme_model.pkl')
   
   # Save label encoders
   joblib.dump(encoders, 'encoders.pkl')
   
   # Save feature columns
   joblib.dump(feature_columns, 'feature_columns.pkl')
   ```

## 🎯 How to Run

### Development Mode

1. **Activate the virtual environment** (if not already activated)

2. **Run the Flask application**
   ```bash
   python app.py
   ```

3. **Open your browser**
   Navigate to `http://localhost:5000`

### Production Mode

For production deployment, use a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📱 Usage Guide

1. **Home Page**: Fill in the prediction form with your details
   - Personal Information: Age, Gender
   - Economic Information: Income, BPL Status
   - Occupation Information: Occupation, District
   - Special Categories: Farmer, Student, Disability
   - Additional Information: Marital Status, Girl Child, Street Vendor
   - Work Categories: Artisan, Woman SHG, Rural Household

2. **Submit Form**: Click the "Predict Scheme" button

3. **View Results**: See the predicted government scheme with confidence score

4. **Learn More**: Visit the About page to understand the ML algorithm

5. **Contact**: Use the Contact page for any queries

## 🧠 Machine Learning Model

### Algorithm: Random Forest Classifier

**Why Random Forest?**
- High accuracy through ensemble learning
- Robust against overfitting
- Handles both numerical and categorical data
- Provides feature importance
- Offers prediction confidence scores

### Model Features

The model analyzes 15 demographic and economic factors:
- Age
- Gender
- Income
- Farmer status
- Student status
- Disability status
- BPL status
- Occupation
- District
- Marital Status
- Girl Child
- Street Vendor
- Artisan
- Woman SHG member
- Rural Household

### Training Process

1. **Data Loading**: Load government scheme dataset
2. **Data Cleaning**: Handle missing values
3. **Feature Encoding**: Label encode categorical features
4. **Model Training**: Train Random Forest classifier
5. **Model Evaluation**: Evaluate using accuracy, precision, recall
6. **Model Serialization**: Save using joblib

## 🖼️ Screenshots

### Home Page
![Home Page](screenshots/home.png)
*Prediction form with user-friendly interface*

### Results Page
![Results Page](screenshots/result.png)
*Displaying predicted scheme with confidence score*

### About Page
![About Page](screenshots/about.png)
*Project information and ML algorithm details*

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
FLASK_DEBUG=True
```

### Model Configuration

Edit model paths in `app.py` if needed:

```python
MODEL_PATH = os.path.join(BASE_DIR, 'scheme_model.pkl')
ENCODERS_PATH = os.path.join(BASE_DIR, 'encoders.pkl')
FEATURE_COLUMNS_PATH = os.path.join(BASE_DIR, 'feature_columns.pkl')
```

## 🚢 Deployment

### Deploy on Render

1. **Create a `Procfile`**
   ```
   web: gunicorn app:app
   ```

2. **Push to GitHub**

3. **Connect to Render**
   - Create new web service on Render
   - Connect your GitHub repository
   - Render will automatically deploy

### Deploy on PythonAnywhere

1. **Upload files** to PythonAnywhere

2. **Configure virtual environment**
   ```bash
   mkvirtualenv myenv
   pip install -r requirements.txt
   ```

3. **Configure WSGI file**
   ```python
   import sys
   path = '/home/yourusername/GovernmentSchemePredictor'
   if path not in sys.path:
       sys.path.append(path)
   
   from app import app as application
   ```

4. **Reload web app**

### Deploy on Heroku

1. **Create `Procfile`**
   ```
   web: gunicorn app:app
   ```

2. **Create `runtime.txt`**
   ```
   python-3.8.16
   ```

3. **Deploy**
   ```bash
   heroku create
   git push heroku main
   ```

## 🐛 Troubleshooting

### Common Issues

**Issue**: Model not loading
- **Solution**: Ensure `scheme_model.pkl`, `encoders.pkl`, and `feature_columns.pkl` exist in the project root

**Issue**: Port 5000 already in use
- **Solution**: Change port in `app.py` or kill the process using port 5000

**Issue**: Import errors
- **Solution**: Ensure all dependencies are installed: `pip install -r requirements.txt`

**Issue**: Template not found
- **Solution**: Ensure `templates` folder exists in the project root

## 🔮 Future Enhancements

- [ ] Add more government schemes to the database
- [ ] Implement user authentication and profile saving
- [ ] Add scheme application direct links
- [ ] Include multilingual support
- [ ] Add SMS/Email notifications for new schemes
- [ ] Implement admin dashboard for scheme management
- [ ] Add data visualization for scheme statistics
- [ ] Integrate with official government APIs
- [ ] Add mobile app version
- [ ] Implement recommendation system based on user history

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Developer

**B.Tech Computer Science Engineering Student**
- 7th Semester Mini Project
- Machine Learning & Web Development

## 🙏 Acknowledgments

- Government of India for scheme data
- scikit-learn team for ML library
- Flask community for web framework
- Bootstrap team for UI framework

## 📞 Contact

For queries and support:
- Email: contact@schemepredictor.com
- GitHub: [your-github-profile]
- LinkedIn: [your-linkedin-profile]

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## ⭐ Star the Project

If you find this project helpful, please consider giving it a star on GitHub!

---

**Note**: This is a mini project for academic purposes. For actual government scheme recommendations, please verify with official government sources.
