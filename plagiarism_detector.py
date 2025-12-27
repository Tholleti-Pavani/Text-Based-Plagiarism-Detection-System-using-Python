import os
import string

FOLDER_PATH = "documents"
SIMILARITY_THRESHOLD = 50  # Percentage above which plagiarism is flagged

def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return set(text.split())

def similarity(doc1, doc2):
    intersection = doc1.intersection(doc2)
    union = doc1.union(doc2)
    if not union:
        return 0
    return round((len(intersection) / len(union)) * 100, 2)

def load_documents(folder):
    docs = {}
    for file in os.listdir(folder):
        if file.endswith(".txt"):
            with open(os.path.join(folder, file), "r", encoding="utf-8") as f:
                docs[file] = clean_text(f.read())
    return docs

def compare_documents(docs):
    results = []
    files = list(docs.keys())
    for i in range(len(files)):
        for j in range(i + 1, len(files)):
            sim = similarity(docs[files[i]], docs[files[j]])
            if sim >= SIMILARITY_THRESHOLD:
                conclusion = "Potential plagiarism detected"
            else:
                conclusion = "No significant plagiarism"
            results.append((files[i], files[j], sim, conclusion))
    return results

def main():
    docs = load_documents(FOLDER_PATH)
    results = compare_documents(docs)

    print("\nPLAGIARISM CHECK RESULTS\n")
    for f1, f2, sim, conclusion in results:
        print(f"{f1}  <->  {f2} : {sim}% similarity | {conclusion}")

if __name__ == "__main__":
    main()
