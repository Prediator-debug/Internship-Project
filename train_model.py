import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

print("Loading dataset...")
# Load dataset
df = pd.read_csv(
    r"D:\Chrome Download\archive\spam.csv",
    encoding="latin-1"
)

# Preprocess dataset
# Assuming v1 is label and v2 is message based on preview
df = df.rename(columns={'v1': 'label', 'v2': 'message'})
df = df[['label', 'message']]

print("Mapping labels...")
df['label_num'] = df['label'].map({'ham': 0, 'spam': 1})
df = df.dropna(subset=['label_num', 'message'])

X = df['message']
y = df['label_num']

print("Splitting dataset...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Building pipeline...")
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english', max_features=3000)),
    ('model', LogisticRegression(max_iter=1000))
])

print("Training model...")
pipeline.fit(X_train, y_train)

# Evaluate
y_pred = pipeline.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"Model accuracy on test set: {acc:.4f}")

# Save the model
model_path = "spam_model.pkl"
print(f"Saving model to {model_path}...")
joblib.dump(pipeline, model_path)
print("Done!")
