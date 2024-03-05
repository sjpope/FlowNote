# FlowNote
![Project Logo](notes/static/notes/css/images/logo.png)
> FlowNote is an innovative, AI-powered note-taking application that enhances user productivity by offering advanced features like real-time speech-to-text conversion and intelligent note summarization.

## Table of Contents
* [Team](#team)
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Screenshots](#screenshots)
* [Setup](#setup)
* [Usage](#usage)
* [Project Status](#project-status)
* [Room for Improvement](#room-for-improvement)
* [Acknowledgements](#acknowledgements)
* [Contact](#contact)

## Team
We are a team of Texas State University students developing this project as part of our Software Engineering course.

* Samuel Pope
* Israel Ibinayin
* John Yamamoto
* Matthew Ruiz

## General Information
- FlowNote is designed to address the challenges of traditional note-taking by integrating AI capabilities, making the process more intuitive and efficient.
- The aim is to provide a seamless platform for users to create, organize, and summarize notes with minimal effort, leveraging AI to enhance the overall experience.
- This project was initiated to explore the integration of AI in everyday productivity tools, pushing the boundaries of conventional note-taking solutions.

## Technologies Used
- Django - version 5.0.2
- MongoDB - version 4.4
- SQLite - version 3.33

## Features
- **Speech-to-Text**: Transform spoken words into written notes effortlessly, making note-taking more accessible and convenient.
- **AI Summarization**: Employ AI to condense long notes into brief, digestible summaries, saving time and enhancing information retention.
- **Dual Database Architecture**: Utilize SQLite for managing user data and authentication, while employing MongoDB for storing and handling dynamic, unstructured note content.

## Sprint 1 ##
* **Israel Ibinayin:**
    * `Jira Task SCRUM-4: Design AI Assistant Integration.`
        * [SCRUM-4](https://cs3398s24klingons.atlassian.net/browse/SCRUM-4), [Bitbucket]()
    * `Jira Task SCRUM-5: Implement AI Assistant Integration.`
        * [SCRUM-5](https://cs3398s24klingons.atlassian.net/browse/SCRUM-5), [Bitbucket]()
    * `Jira Task SCRUM-6: Unit Testing for AI Assistant Integration.`
        * [SCRUM-6](https://cs3398s24klingons.atlassian.net/browse/SCRUM-6), [Bitbucket]()
    * `Jira Task SCRUM-7: User Interface Design for AI Assistant.`
        * [SCRUM-7](https://cs3398s24klingons.atlassian.net/browse/SCRUM-7), [Bitbucket]()
    * `Jira Task SCRUM-8: Implement User Interface for AI Assistant.`
        * [SCRUM-8](https://cs3398s24klingons.atlassian.net/browse/SCRUM-8), [Bitbucket]()
    
* **Samuel Pope:**
    * `Jira Task SCRUM-14: Design Search Functionality.`
        * [SCRUM-14](https://cs3398s24klingons.atlassian.net/browse/SCRUM-14), [Bitbucket]()
    * `Jira Task SCRUM-15: Implement Search Backend.`
        * [SCRUM-15](https://cs3398s24klingons.atlassian.net/browse/SCRUM-15), [Bitbucket]()
    * `Jira Task SCRUM-17: User Interface Design for Search.`
        * [SCRUM-17](https://cs3398s24klingons.atlassian.net/browse/SCRUM-17), [Bitbucket]()
    * `Jira Task SCRUM-18: Implement User Interface for Search.`
        * [SCRUM-18](https://cs3398s24klingons.atlassian.net/browse/SCRUM-18), [Bitbucket]()
    * `Jira Task SCRUM-42: Design the Note Model.`
        * [SCRUM-42](https://cs3398s24klingons.atlassian.net/browse/SCRUM-42), [Bitbucket]()
    * `Jira Task SCRUM-43: Implement CRUD Views.`
        * [SCRUM-43](https://cs3398s24klingons.atlassian.net/browse/SCRUM-43), [Bitbucket]()
    * `Jira Task SCRUM-44: Create Note Templates`
        * [SCRUM-44](https://cs3398s24klingons.atlassian.net/browse/SCRUM-44), [Bitbucket]()
    * `Jira Task SCRUM-45: Implement URL Routing.`
        * [SCRUM-45](https://cs3398s24klingons.atlassian.net/browse/SCRUM-45), [Bitbucket]()
    * `Jira Task SCRUM-47: Design the User Registration Form.`
        * [SCRUM-47](https://cs3398s24klingons.atlassian.net/browse/SCRUM-47), [Bitbucket]()
    * `Jira Task SCRUM-48: Implement User Authentication Views.`
        * [SCRUM-48](https://cs3398s24klingons.atlassian.net/browse/SCRUM-48), [Bitbucket]()
    * `Jira Task SCRUM-49: Create Authentication Templates.`
        * [SCRUM-49](https://cs3398s24klingons.atlassian.net/browse/SCRUM-49), [Bitbucket]()
    * `Jira Task SCRUM-51: Unit Testing for Authentication.`
        * [SCRUM-51](https://cs3398s24klingons.atlassian.net/browse/SCRUM-51), [Bitbucket]()
    * `Jira Task SCRUM-58: Develop a Note Analysis Backend Service.`
        * [SCRUM-58](https://cs3398s24klingons.atlassian.net/browse/SCRUM-58), [Bitbucket]()
    * `Jira Task SCRUM-62: Integrate Djongo/MongoDB into Backend Operations.`
        * [SCRUM-62](https://cs3398s24klingons.atlassian.net/browse/SCRUM-62), [Bitbucket]()
    * `Jira Task SCRUM-63: Base Template Footer doesn't resize/scroll along with the other page contents.`
        * [SCRUM-63](https://cs3398s24klingons.atlassian.net/browse/SCRUM-63), [Bitbucket]()
    * `Jira Task SCRUM-65:User Auth: Notes should be private to the User/Login Credentials.`
        * [SCRUM-65](https://cs3398s24klingons.atlassian.net/browse/SCRUM-65), [Bitbucket]()
    * `Jira Task SCRUM-66: Develop Note Content Parsing and Analysis Module.`
        * [SCRUM-66](https://cs3398s24klingons.atlassian.net/browse/SCRUM-66), [Bitbucket]()
    * `Jira Task SCRUM-72: Create a Separate App for AI and Complex Data Operations.`
        * [SCRUM-72](https://cs3398s24klingons.atlassian.net/browse/SCRUM-72), [Bitbucket]()
    * `Jira Task SCRUM-73: Integrate ML models (Build AI Features).`
        * [SCRUM-73](https://cs3398s24klingons.atlassian.net/browse/SCRUM-73), [Bitbucket]()
    * `Jira Task SCRUM-74: Integrate External APIs for Complex Data Operations (Build/Test AI Features).`
        * [SCRUM-74](https://cs3398s24klingons.atlassian.net/browse/SCRUM-74), [Bitbucket]()
    * `Jira Task SCRUM-77: User Auth: Modify to use FlowNote Acct & Re-style Auth Options.`
        * [SCRUM-77](https://cs3398s24klingons.atlassian.net/browse/SCRUM-77), [Bitbucket]()
    * `Jira Task SCRUM-78: ModuleNotFoundError: 'flownote' not found.`
        * [SCRUM-78](https://cs3398s24klingons.atlassian.net/browse/SCRUM-78), [Bitbucket]()
    * `Jira Task SCRUM-79: Runtime Error: Model Class allauth.account.models.EmailAddress is defined in settings.py but throwing exception.`
        * [SCRUM-79](https://cs3398s24klingons.atlassian.net/browse/SCRUM-79), [Bitbucket]()
    * `Jira Task SCRUM-80: Migration from SQLite3 to SQL Server.`
        * [SCRUM-80](https://cs3398s24klingons.atlassian.net/browse/SCRUM-80), [Bitbucket]()

* **Matthew Ruiz:** "Email Verification, Test Summarization feature, and Integrate External APIs."
    * `Jira Task SCRUM-24: Test OpenAI Summarization Feature.`
        * [SCRUM-24](https://cs3398s24klingons.atlassian.net/browse/SCRUM-24), [Bitbucket]()
    * `Jira Task SCRUM-25: The user interface for submitting documents and receiving summaries must be intuitive, and easy to navigate.`
        * [SCRUM-25](https://cs3398s24klingons.atlassian.net/browse/SCRUM-25), [Bitbucket]()
    * `Jira Task SCRUM-50: Setup Email Verification.`
        * [SCRUM-50](https://cs3398s24klingons.atlassian.net/browse/SCRUM-50), [Bitbucket]()
    * `Jira Task SCRUM-74: Integrate External APIs for Complex Data Operations (Build/Test AI Features).`
        * [SCRUM-74](https://cs3398s24klingons.atlassian.net/browse/SCRUM-74), [Bitbucket]()

* **John Yamamoto:** "Implement AI generated Summaries, and Create CRUD tests for Notes."
    * `Jira Task SCRUM-22: Implement Generative AI API to summarize notes.`
        * [SCRUM-22](https://cs3398s24klingons.atlassian.net/browse/SCRUM-22), [Bitbucket](https://bitbucket.org/cs3398s24klingons/flownote/commits/0ecd11a18b9433d750b847b03a1456dc9cfaec43)
    * `Jira Task SCRUM-23: A Method to add Summary to notes.`
        * [SCRUM-23](https://cs3398s24klingons.atlassian.net/browse/SCRUM-23), [Bitbucket](https://bitbucket.org/cs3398s24klingons/flownote/commits/dab858cf2a54ddeee5aa8cd5bf978da1eaeae0cd)
    * `Jira Task SCRUM-46: Write Unit Tests for CRUD Operations.`
        * [SCRUM-46](https://cs3398s24klingons.atlassian.net/browse/SCRUM-46), [Bitbucket](https://bitbucket.org/cs3398s24klingons/flownote/commits/d6d734ec88323ca881b1df17ab634fb55052eb97)

## 1st Report ##
![Burnup1](notes/static/notes/css/images/Sprint1BurnupReport.png)

## Next Steps (Sprint 2) ##
* **Israel Ibinayin:**
    *
* **Samuel Pope:**
    *
* **Matthew Ruiz:**
    *
* **John Yamamoto:**
    * Look to potentially design user interface for the Analysis and Content Sugestion Features.

## Screenshots
![FlowNote Screenshot](./img/flow_note_screenshot.png)

## Setup
FlowNote requires Python 3.12.1, MongoDB, and an environment capable of running Django. 

To get started:
1. Clone the repository to your local machine.
2. Install the required Python packages: `pip install -r requirements.txt`.
3. Apply migrations to set up the database: `python manage.py migrate`.
4. Start the Django development server: `python manage.py runserver`.

## Usage
Once the server is running, access FlowNote through your web browser at `http://127.0.0.1:8000/`. Register for an account or log in to begin creating and managing your notes. Utilize the speech-to-text feature to dictate notes and leverage the AI summarization to review notes efficiently.

## Project Status
Project is: _in progress_. Future updates are planned to introduce more sophisticated AI models for improved feature performance and additional user functionalities.

## Room for Improvement
* Future enhancements include:
    * Expanding AI capabilities for greater accuracy in speech-to-text transcription.
    * Introducing more advanced algorithms for note summarization to cater to various content types.

* Planned features:
    * Implementing guest user functionality with session-based note storage.
    * Enhancing the user interface for a more engaging and intuitive user experience.

## Acknowledgements
- This project was inspired by a vision to revolutionize the way we take and manage notes.
- Special thanks to the Django community for their invaluable resources and support.

## Contact
Created by Samuel Pope and John Yamamoto - feel free to reach out at sjpope03@gmail.com.