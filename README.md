# Bike Sharing Data Analysis Dashboard

Project ini merupakan dashboard data analisis Bike Sharing Dataset untuk mengetahui lebih jauh tentang data yang ada menggunakan Streamlit sebagai dashboardnya. Project ini memberikan insight mengenai penyewaan sepeda berdasarkan musim, cuaca, dan hari.

## Project Structure
```
DATA-ANALYSIS/
│── dashboard/
│   ├── dashboard.py                        # Streamlit app
│   ├── data/
│   │   ├── day.csv                         # Dataset
│   │   ├── hour.csv
│── requirements.txt                        # Dependencies
│── README.md                               # Instructions
│── Submission_Data_Analysis_Haiqel.ipynb   # Notebook 
│── url.txt                                 # Link dashboard
```

## Instalasi dan Run secara Local

### 1. Clone Repository
```sh
git clone https://github.com/Haiqelhakeem/bike-sharing-analysis.git
cd /dashboard
```

### 2. Buat Virtual Environment (Optional)
```sh
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Run Streamlit App
```sh
streamlit run dashboard.py
```

Dashboard akan berjalan pada port:
```
http://localhost:8501/
```

## Author
Haiqel Azizul Hakeem

