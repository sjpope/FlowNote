# FlowNote

FlowNote is an innovative AI-powered note-taking application designed to streamline productivity through features such as:
- **GPT-2-based Autocompletion** and summarization
- **Dual-database architecture** (initially SQLite and MongoDB)

> **Status**: Actively maintained by [Samuel Pope](mailto:sjpope03@gmail.com). Previously a group project at Texas State University, now managed post-course completion and migrated from BitBucket to GitHub.

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [Setup and Installation](#setup-and-installation)
5. [Usage](#usage)
6. [Future Plans](#future-plans)
7. [License](#license)
8. [Contact](#contact)

---

## Overview

FlowNote started as a collaborative software engineering project. It leverages local GPT-2 Large (via Hugging Face Transformers) to help users generate, summarize, and analyze their notes. Over time, it has expanded to include:
- Summarization and content generation using Transformers
- Note Grouping based on TF-IDF and Cosine Similarity Matrix Scores
- Database flexibility (MongoDB + SQLite)

Currently, the repository is being restructured for clarity and future growth, with a stronger focus on MLOps best practices and modular AI components.

## Features

1. **Speech-to-Text**: Dictate your notes and have them automatically transcribed.  
2. **AI Summaries**: Summarize large blocks of text into concise overviews using GPT-2.  
3. **GPT-2 Autocomplete**: Predictive text generation that assists in writing.  
4. **Dual Database Support**: MongoDB for flexible note storage; SQLite for user auth and other relational data.

## Tech Stack

- **Python 3.12+**  
- **Django 5.0.2**  
- **MongoDB 4.4** and **SQLite 3.33**  
- **Hugging Face Transformers** (GPT-2 Large)  
- (Optional) **Docker** for containerization  
- (Optional) **MLflow** or **Weights & Biases** for model experiment tracking

## Setup and Installation

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/sjpope/flownote.git
   cd flownote
   ```

(To be continued...)