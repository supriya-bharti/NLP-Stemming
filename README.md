# NLP-Stemming

# NLP Mini Project - Porter Stemming Algorithm

## 1. Introduction

Natural Language Processing (NLP) is a branch of Artificial Intelligence that enables computers to process and understand human language.

This project implements the Porter Stemming Algorithm from scratch using Python.

The main objective of the project is to reduce words to their root-like forms by removing common morphological suffixes.

For example:

    playing → play
    played → play
    studies → studi
    relational → relat

The resulting stem does not necessarily have to be a valid English word.

---

## 2. Objectives

The objectives of this project are:

- Understand the concept of stemming in NLP.
- Implement the Porter Stemming Algorithm from scratch.
- Implement preprocessing techniques.
- Perform tokenization.
- Remove stopwords.
- Compare the custom implementation with NLTK's Porter Stemmer.
- Evaluate the implementation using accuracy.
- Provide an interactive text processing interface.

---

## 3. Technologies Used

- Python
- Natural Language Processing
- NLTK
- CSV
- VS Code

---

## 4. Project Structure

```text
NLP-STEMMING/
│
├── dataset/
│   └── sample.txt
│
├── results/
│   └── stemming_results.csv
│
├── main.py
├── stemmer.py
├── tokenizer.py
├── stopwords.py
├── preprocessing.py
├── evaluation.py
└── README.md