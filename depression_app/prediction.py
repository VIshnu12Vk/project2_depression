import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import os



def text_predict(new_texts):
   
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    xml_file_path = os.path.join(base_dir, 'depression_app', 'dataset', 'depression_dataset_reddit_cleaned.csv')
    df = pd.read_csv(xml_file_path)
    X = df['clean_text']
    y = df['is_depression']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    vectorizer = TfidfVectorizer()
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    model = LogisticRegression()
    model.fit(X_train_vec, y_train)
    y_pred = model.predict(X_test_vec)
    new_texts_vec = vectorizer.transform(new_texts)
    new_predictions = model.predict(new_texts_vec)
    return new_predictions[0]

