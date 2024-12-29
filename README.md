# 📧 Email Checker
*Enhance and optimize your emails with AI-driven recommendations.*

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Streamlit](https://img.shields.io/badge/Powered_by-Streamlit-green.svg)
![OpenAI](https://img.shields.io/badge/Powered_by-OpenAI-blue.svg)

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Contact](#contact)
- [Acknowledgements](#acknowledgements)

## Description

Cuesta Email Mentor is a Streamlit application that leverages OpenAI's chat-based language models to evaluate and enhance your emails. By providing AI-driven recommendations based on predefined instructions, it ensures your emails are professional, clear, and effective.

## Features

- **AI-Driven Email Evaluation**: Analyze and improve your emails with AI-generated feedback.
- **Customizable Instructions**: Customize the instructions within the app, or use the provided template.
- **User-Friendly Interface**: Intuitive Streamlit interface for seamless interactions.
- **Detailed Recommendations**: Receive comprehensive feedback on email structure, tone, clarity, and more.

## Instructions
 - install requirements.txt
 - set up a config.yaml

## Configuration

config.yaml config:
```yaml
openai:
  temperature: 0.7
  max_tokens: 2000
  top_p: 1.0
  frequency_penalty: 0.0
  presence_penalty: 0.0
  model_name: "gpt-4o-mini" ## insert model choice
  api_key: "INSERT OPENAI API KEY"
```

## Contact
 - [LinkedIn](https://www.linkedin.com/in/wongmarcus/)

## Acknowledgements

Thank you to [Hilary Gridley](https://hils.substack.com/) for the idea, from [Lenny's Newsletter](https://www.lennysnewsletter.com/p/how-to-become-a-supermanager-with).  Much of the inspiration comes from her custom GPT, as well as the instructions use her template. 

Props to [@okld](https://github.com/okld/streamlit-quill) for writing streamlit_quill.  The library was a lifesaver in this project, for allowing rich text AND for converting it into HTML for which I could feed it to OpenAI.  The application would be significantly less useful had it not been for this library. 
