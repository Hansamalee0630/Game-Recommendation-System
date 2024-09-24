# Game-Recommendation-System
Game Recommendation System made with Flask, Python, Pandas, Numpy, Scikit-learn, jQuery, HTML and CSS.


Game-Recommendation-System/
├── data/
│   └── Video_Games_Sales_as_at_22_Dec_2016.csv
├── model/
│   ├── recommendation_engine.py
│   └── Video_Games.ipynb
├── static/
│   └── styles.css
├── templates/
│   └── index.html
├── app.py
├── README.md
├── requirements.txt
└── .gitignore

# 🎮 Game Recommendation System

A Flask-based **Game Recommendation System** powered by **Machine Learning** algorithms, built using **Python**, **Pandas**, **Numpy**, and **Scikit-learn**. This system recommends video games based on historical sales data.

## 🚀 Features:
- **Game Recommendation Engine**: Using similarity metrics and recommendation logic.
- **Interactive Web Interface**: Built using Flask, HTML, CSS, and jQuery.
- **Data-Driven**: Recommends games based on real-world sales data.

## 🛠 Technologies Used:
- **Python** (Flask, Pandas, Numpy, Scikit-learn)
- **Flask** (Backend Framework)
- **jQuery, HTML, CSS** (Frontend)

## 📂 Folder Structure:
- `data/`: Contains the dataset (`Video_Games_Sales_as_at_22_Dec_2016.csv`).
- `model/`: Houses the recommendation logic (`recommendation_engine.py`) and the Jupyter notebook (`Video_Games.ipynb`) for data analysis and model building.
- `static/`: Contains static files like CSS (`styles.css`).
- `templates/`: HTML templates for the Flask app (`index.html`).
- `app.py`: Main Flask application file to run the web app.

## 📊 Dataset:
The dataset used in this project is **Video Games Sales as of Dec 2016**, which includes information about video game sales, genre, publisher, and more.

## 🚀 How to Run:
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/Game-Recommendation-System.git
   cd Game-Recommendation-System
   ```
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Flask app:
   ```bash
   python app.py
   ```
4. Open your browser and navigate to `http://127.0.0.1:5000/`.

## 🔮 Future Improvements:
- Enhance recommendation algorithms.
- Add more interactive features to the web app.
- Implement user login and personalized recommendations.

## 💻 Contribution:
Feel free to contribute by opening issues or creating pull requests.

## License:
[MIT License](LICENSE)
