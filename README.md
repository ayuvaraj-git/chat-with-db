Database Assistant - Convert Natural Language to SQL Queries
This open-source repository houses the code for a web application built with Streamlit that acts as a database assistant, empowering users to translate natural language questions into executable SQL queries for a Microsoft SQL Server database.

Key Features:
Intuitive Interface: Interact with the database through a conversational chat interface, asking questions in plain English.
Generative AI Conversion: Powered by Google's Generative AI, the assistant accurately translates your questions into valid SQL queries.
Dynamic Data Retrieval: Query your database seamlessly. Retrieved data is presented directly within the chat interface.
Chat History Management: Keep track of past conversations and refer back to previous interactions easily. Rename past chats for personalized organization.
Performance Optimization: Caching mechanisms ensure swift responses, minimizing API calls and enhancing interaction speed.
Prerequisites:
Python 3.7+: Ensure you have Python installed on your system.
Google Cloud Project with Generative AI API: Set up a Google Cloud project and enable the Generative AI API. Store the API key as an environment variable named GOOGLE_API_KEY.
Microsoft SQL Server: Connect to a running Microsoft SQL Server instance. Configure the connection details (server, database, username, password) as environment variables named SERVER, DATABASE, USERNAME, and PASSWORD.
Streamlit: Install the Streamlit library using pip install streamlit.
Additional Libraries: The code also utilizes pandas, sqlvalidator, and joblib. Install them using pip install pandas sqlvalidator joblib.
Getting Started:
Clone the repository: Download the code to your local machine using Git.
Install dependencies: Make sure you have the required libraries installed as mentioned in the prerequisites.
Set environment variables: Configure the environment variables with your database connection details and Google API key.
Run the application: Execute the code using streamlit run app.py.
Using the Assistant:
Launch the application: The web app will open in your browser.
Ask your question: Enter your natural language question related to the database in the chat input field.
Submit your query: Click the "Enter" button or press "Ctrl+Enter".
See the response: The assistant will convert your question to an SQL query, execute it, and display the retrieved data or an appropriate message in the chat window.
Explore further: Continue asking questions and interacting with your database using natural language queries.
Additional Notes:
The generative AI model used might sometimes generate inaccurate or incomplete responses.
Verify that you have the necessary permissions to access and query the target database.
Feel free to customize the code to align with your specific needs and database schema.
Contributing:
We encourage contributions to this project! If you have any ideas, improvements, or bug fixes, please don't hesitate to create a pull request.

License:
This project is licensed under the MIT License. Please refer to the LICENSE file for details.
