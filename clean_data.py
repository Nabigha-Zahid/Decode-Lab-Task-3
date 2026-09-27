import pandas as pd
import re


# Load dataset
df = pd.read_csv("data/jobs.csv")

print("Original shape:", df.shape)


# Keep useful columns
columns_to_keep = [
    "Job Title",
    "Key Skills",
    "Role Category",
    "Functional Area",
    "Industry"
]

df = df[columns_to_keep]


# Remove missing important values
df = df.dropna(subset=["Job Title", "Key Skills"])


# Clean spaces
for column in columns_to_keep:
    df[column] = df[column].astype(str).str.strip()


# Remove empty values
df = df[
    (df["Job Title"] != "") &
    (df["Key Skills"] != "")
]


# Remove obviously invalid job titles
def valid_job_title(title):

    title = str(title).strip()

    if len(title) > 60:
        return False

    if len(title.split()) > 8:
        return False

    if title.startswith(
        ("*", "-", ".", "\"", "'", "1.", "2.", "3.")
    ):
        return False

    if not re.search(r"[A-Za-z]", title):
        return False

    return True


df = df[df["Job Title"].apply(valid_job_title)]


# Tech-related keywords
tech_keywords = [
    "software",
    "developer",
    "engineer",
    "programmer",
    "data",
    "analyst",
    "scientist",
    "machine learning",
    "artificial intelligence",
    "ai ",
    "ml ",
    "python",
    "java",
    "web",
    "frontend",
    "front end",
    "backend",
    "back end",
    "full stack",
    "fullstack",
    "devops",
    "cloud",
    "network",
    "security",
    "cyber",
    "database",
    "dba",
    "architect",
    "testing",
    "test",
    "qa",
    "quality assurance",
    "android",
    "ios",
    "mobile",
    "ui",
    "ux",
    "system administrator",
    "technical",
    "technology",
    "it "
]


def is_tech_job(row):

    searchable_text = (
        str(row["Job Title"]) + " " +
        str(row["Role Category"]) + " " +
        str(row["Functional Area"]) + " " +
        str(row["Industry"])
    ).lower()

    return any(
        keyword in searchable_text
        for keyword in tech_keywords
    )


# Keep only tech-related jobs
df = df[df.apply(is_tech_job, axis=1)]


# Remove duplicates
df = df.drop_duplicates()


print("\nRows after tech filtering:", df.shape)


# Combine repeated job titles
clean_df = (
    df.groupby("Job Title")
    .agg({
        "Key Skills": lambda x: " ".join(x.astype(str)),
        "Role Category": "first",
        "Functional Area": "first",
        "Industry": "first"
    })
    .reset_index()
)


# Clean skill text
clean_df["Key Skills"] = (
    clean_df["Key Skills"]
    .str.replace(",", " ", regex=False)
    .str.replace("|", " ", regex=False)
    .str.replace("/", " ", regex=False)
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)


# Sort alphabetically
clean_df = clean_df.sort_values("Job Title")


print("\nFinal cleaned shape:", clean_df.shape)

print("\nSample tech jobs:")

print(
    clean_df[
        ["Job Title", "Key Skills"]
    ].head(30).to_string(index=False)
)


# Save cleaned dataset
clean_df.to_csv(
    "data/cleaned_jobs.csv",
    index=False
)

print("\nSaved:")
print("data/cleaned_jobs.csv")