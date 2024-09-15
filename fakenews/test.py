from googlesearch import search
from bs4 import BeautifulSoup
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# Function to perform Google search and get snippets
def google_search(query):
    snippets = []

    try:
        search_results = search(query, num=5, stop=5, pause=2)
        
        for result in search_results:
            try:
                response = requests.get(result)
                soup = BeautifulSoup(response.text, 'html.parser')
                snippet = soup.find('meta', {'name': 'description'})
                if snippet:
                    snippets.append(snippet.get('content', ''))
            except Exception as e:
                print(f"Error processing result: {result} - {e}")
    except Exception as e:
        print(f"Error during Google search: {e}")

    return snippets

# User Input
user_paragraph = input("Enter the news paragraph: ")

# Step 2: Google Search
search_query = f"Is the following news true or fake? {user_paragraph}"
search_results = google_search(search_query)

# Step 3: Display Search Results
print("\nSearch Results:")
for i, snippet in enumerate(search_results, start=1):
    print(f"{i}. {snippet}")

# Step 4: Fake News Detection using Machine Learning
def detect_fake_news(news_paragraph):
    # Example: Using a simple Multinomial Naive Bayes classifier
    model = make_pipeline(TfidfVectorizer(), MultinomialNB())
    
    # Example training data (you should replace this with a larger, labeled dataset)
    training_data = ["fake news example", "real news example", ...]
    labels = ["fake", "real", ...]
    
    # Training the model
    model.fit(training_data, labels)
    
    # Predicting the label for the user's input
    prediction = model.predict([news_paragraph])

    return prediction[0]

# Example result (replace with your actual detection):
fake_news_result = detect_fake_news(user_paragraph)

# Step 5: Print the final result
if fake_news_result.lower() == "fake":
    print("\nThe news is likely fake.")
else:
    print("\nThe news is likely real.")
