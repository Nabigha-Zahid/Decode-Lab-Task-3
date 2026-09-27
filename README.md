# Decode Lab Task 3 - Tech Stack Recommender

**Live App:**  
https://decode-lab-task-3-r72hwkokvfs6ettxjp7bqe.streamlit.app/

## Project Overview

This project is a content-based recommendation system developed for DecodeLabs Artificial Intelligence Project 3.

The system recommends the top three job roles based on the technical skills entered by the user.

## How It Works

1. The user enters at least three technical skills.
2. Job roles and their key skills are loaded from a cleaned dataset.
3. TF-IDF converts the skill text into numerical vectors.
4. Cosine Similarity compares the user's skills with each job role.
5. Similarity scores are sorted in descending order.
6. The top three matching job roles are displayed.

## Features

- Minimum 3 skill inputs
- Content-Based Recommendation
- TF-IDF Vectorization
- Cosine Similarity
- Top 3 job recommendations
- Match percentage
- Interactive Streamlit interface
- Dataset cleaning and preprocessing

## Technologies Used

- Python
- Pandas
- Scikit-learn
- Streamlit

## Project Structure

```text
Decode-Lab-Task-3/
│
├── data/
│   ├── jobs.csv
│   └── cleaned_jobs.csv
│
├── app.py
├── clean_data.py
├── recommender.py
├── requirements.txt
├── README.md
└── .gitignore
## Live Demo

The application is deployed on Streamlit Community Cloud.

[Open the live application](https://decode-lab-task-3-r72hwkokvfs6ettxjp7bqe.streamlit.app/)