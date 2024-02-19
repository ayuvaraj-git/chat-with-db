# chat-with-db

Database Assistant - Convert Natural Language to SQL Queries
This repository contains the code for a Streamlit web application that functions as a database assistant. It allows users to ask natural language questions about a Microsoft SQL Server database and receive corresponding SQL queries as responses.

Features
Natural Language to SQL Conversion: Utilizes Google's Generative AI model to translate user queries into valid SQL code.
Interactive Chat Interface: Enables users to enter natural language prompts and view responses in a chat-like format.
Database Connectivity: Connects to a Microsoft SQL Server database using provided credentials.
SQL Query Execution: Executes generated SQL queries and displays the retrieved data (if any).
Chat History Management: Stores past conversation history for future reference and allows renaming of past chats.
Caching and Performance: Uses caching mechanisms to improve response times and avoid unnecessary API calls.
Prerequisites
Python 3.7+: Make sure you have Python installed on your system.
Google Cloud Project with Generative AI API: Create a Google Cloud project and enable the Generative AI API. Set the API key as an environment variable named GOOGLE_API_KEY.
Microsoft SQL Server: You need a running Microsoft SQL Server database to connect to. Configure the connection details (server, database, username, password) as environment variables named SERVER, DATABASE, USERNAME, and PASSWORD.
Streamlit: Install the Streamlit library using pip install streamlit.
Additional Libraries: The code also uses pandas, sqlvalidator, and joblib. Install them using pip install pandas sqlvalidator joblib.
Setup
Clone this repository to your local machine.
Install the required libraries as mentioned in the prerequisites.
Set the necessary environment variables with your database connection details and Google API key.
Run the application using streamlit run app.py.
Usage
The application will launch in your web browser.
Enter your natural language question related to the database in the chat input box.
Click the "Enter" button or press "Ctrl+Enter" to submit your query.
The assistant will convert your question to an SQL query and execute it on the database.
If the query is successful, the retrieved data will be displayed in the chat window.
If the query is invalid or there's an error, an appropriate message will be shown.
You can continue asking questions and explore the data in the database through natural language queries.
Additional Notes
The application leverages a generative AI model, which may sometimes generate inaccurate or incomplete responses.
Ensure you have the necessary permissions to access and query the target database.
Feel free to explore and modify the code to suit your specific needs and database schema.
Contributing
We welcome contributions to this project! If you have any suggestions, improvements, or bug fixes, please create a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for details.

I hope this detailed README file provides a comprehensive overview of the project!