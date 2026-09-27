import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Load cleaned dataset
df = pd.read_csv("data/cleaned_jobs.csv")


# Remove any remaining missing values
df = df.dropna(subset=["Job Title", "Key Skills"])


# Create TF-IDF vectorizer
vectorizer = TfidfVectorizer(
    stop_words="english",
    lowercase=True
)


# Convert job skills into TF-IDF vectors
job_vectors = vectorizer.fit_transform(df["Key Skills"])


def recommend_jobs(user_skills, top_n=3):

    # Convert list of skills to a single string
    user_text = " ".join(user_skills)

    # Convert user skills into same TF-IDF vector space
    user_vector = vectorizer.transform([user_text])

    # Calculate cosine similarity
    similarity_scores = cosine_similarity(
        user_vector,
        job_vectors
    ).flatten()

    # Make temporary copy
    results = df.copy()

    # Add similarity score
    results["Similarity Score"] = similarity_scores

    # Sort highest score first
    results = results.sort_values(
        by="Similarity Score",
        ascending=False
    )

    # Return top recommendations
    return results.head(top_n)


# Testing
if __name__ == "__main__":

    print("\nTECH STACK RECOMMENDER")
    print("----------------------")

    user_input = input(
        "Enter at least 3 skills separated by commas: "
    )

    skills = [
        skill.strip()
        for skill in user_input.split(",")
        if skill.strip()
    ]

    if len(skills) < 3:
        print("\nPlease enter at least 3 skills.")

    else:

        recommendations = recommend_jobs(
            skills,
            top_n=3
        )

        print("\nTop 3 Recommended Jobs:\n")

        for i, (_, row) in enumerate(
            recommendations.iterrows(),
            start=1
        ):

            score = row["Similarity Score"] * 100

            print(f"{i}. {row['Job Title']}")
            print(f"   Match Score: {score:.2f}%")
            print()