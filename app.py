import streamlit as st
import os
from dotenv import load_dotenv
import pandas as pd
import google.generativeai as genai
import time
import random
from sqlalchemy.engine import URL
from sqlalchemy import (
    create_engine
)
import joblib
import sqlvalidator

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')
SERVER = os.getenv('SERVER')
DATABASE = os.getenv('DATABASE')
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'
connectionurl = URL.create(
    "mssql+pyodbc", query={"odbc_connect": connectionString})

new_chat_id = f'{time.time()}'

try:
    os.mkdir('data/')
except:
    # data/ folder already exists
    pass


def get_database_session(connectionurl):
    engine1 = create_engine(connectionurl, pool_pre_ping=True)
    conn = engine1.connect()
    return conn


# conn = get_database_session(connectionurl)


A_PROMPT = [""" You are an expert converting English to SQL query. You are working on Microsoft SQL server. Generate query without line breaks. Use only select queries. use the AS keyword to rename duplicate columns after selecting them. Choose clear and descriptive names to avoid confusion.
Sql code should not have the word sql in the generated output. Sql code should not have ``` in the beginning or the end. Remove the line breaks from the output, also remove line breaks from the output.
"""]

mssg = ["""Sorry, I couldn't get that correctly""",
        """Oops, Something is wrong..Come again please...""", """My bad, Come again...."""]


def search_list_of_dicts(data, search_value):
    result = []
    for item in data:
        if search_value in item.values():
            result.append(item)
            break
    return result


@st.cache_resource(show_spinner=False, ttl=300)
def getsqlquery(question):
    response = search_list_of_dicts(st.session_state.gemini_history, question)
    if response == []:
        response = model.generate_content([A_PROMPT[0], question])
        response = response.text
    else:
        response = response[0]['Query']
    # print (response)
    # response = model.generate_content([A_PROMPT[0], question])
    # print(response.text)
    return response


@st.cache_data(show_spinner=False, ttl=300)
def getsqldata(query):
    # print (query)
    try:
        # global conn
        try:
            if conn.closed:
                conn = get_database_session(connectionurl)
        except:
            conn = get_database_session(connectionurl)
        df = pd.read_sql_query(query, conn)
        df.index.names = ['S.No']
        df.index += 1
        df = df.T.drop_duplicates().T
    except Exception as error:
        print(error)
        random_mssg = random.choice(mssg)
        df = random_mssg
    # df = df.set_index(df.columns[0])
    # print(df)
    return df


def move_focus():
    # inspect the html to determine which control to specify to receive focus (e.g. text or textarea).
    st.components.v1.html(
        f"""
            <script>
                var textarea = window.parent.document.querySelectorAll("textarea[type=textarea]");
                for (var i = 0; i < textarea.length; ++i) {{
                    textarea[i].focus();
                }}
            </script>
        """,
    )


header = st.container()
header.title("Test Bot")
header.write("""<div class='fixed-header'/>""", unsafe_allow_html=True)

# Custom CSS for the sticky header
st.markdown(
    """
<style>
    div[data-testid="stVerticalBlock"] div:has(div.fixed-header) {
        position: sticky;
        top: 2.875rem;
        background-color: #0E1117;
        z-index: 999;
    }
    .fixed-header {
        border-bottom: 1px solid black;
    }
</style>
    """,
    unsafe_allow_html=True
)

# st.title("Meeting Services Bot")

try:
    past_chats: dict = joblib.load('data/past_chats_list')
except:
    past_chats = {}

selectlist = [new_chat_id] + list(past_chats.keys())
if st.session_state.get('chat_id') is None:
    selectlistindex = new_chat_id
else:
    if st.session_state.get('chat_id') not in past_chats.keys():
        selectlist = [st.session_state.get(
            'chat_id')] + list(past_chats.keys())
    selectlistindex = st.session_state.get('chat_id')
with st.sidebar:
    st.write('# Past Chats')
    st.session_state.chat_id = st.selectbox(
        label='Pick a past chat',
        options=selectlist,
        index=selectlist.index(selectlistindex),
        format_func=lambda x: past_chats.get(x, 'New Chat'),
        placeholder='_',
    )
    try:
        if len(past_chats) > 0:
            st.caption(
                'Below is the list of chat avilable in the history,You can rename the tiltle for easy reference. Use the above drop to view the chat history')
            past_chats_new = st.data_editor(past_chats, column_config={
                                            "value": st.column_config.Column("Chat Name")}, hide_index=True)
    except:
        pass
    try:
        if past_chats_new != past_chats:
            joblib.dump(past_chats_new, 'data/past_chats_list')
    except:
        pass


# print (st.session_state.get('chat_id'))
# print (selectlistindex)
st.session_state.chat_title = f'ChatSession-{st.session_state.chat_id}'


try:
    # st.session_state.messages = []
    # st.session_state.gemini_history = []
    st.session_state.messages = joblib.load(
        f'data/{st.session_state.chat_id}-st_messages'
    )

    # print('old cache')
except Exception as error:
    st.session_state.messages = []
    # print("An exception occurred:", error)
    # print('new_cache made')
# print (st.session_state.get('chat_id'))
# Sample Example

try:
    # st.session_state.messages = []
    # st.session_state.gemini_history = []

    st.session_state.gemini_history = joblib.load(
        f'data/aidata-gemini_messages'
    )
    # print('old cache')
except Exception as error:
    st.session_state.gemini_history = []

text = "Hi, I am your DB assistant, I am an expert in converting Natural Language to SQL queries.You can start asking your questions :)"
speed = 2


# Initialize chat history
if len(st.session_state.messages) == 0:
    # st.session_state.messages = []

    time.sleep(1)
    with st.chat_message(
        name="assistant"

    ):
        message_placeholder = st.empty()
        full_response = ''
        # assistant_response = response
        # Streams in a chunk at a time
        tokens = text.split()
        for index in range(len(tokens) + 1):
            curr_full_text = " ".join(tokens[:index])
            message_placeholder.markdown(curr_full_text)
            time.sleep(1 / (speed * (random.randrange(1, 10, 1))))


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if isinstance(message["content"], pd.DataFrame):
        st.chat_message(message["role"]).dataframe(
            message["content"], hide_index=True)
    else:
        st.chat_message(message["role"]).markdown(message["content"])
if len(st.session_state.messages) == 0:
    st.session_state.messages.append({"role": "assistant", "content": text})


# React to user input
if prompt := st.chat_input("Count of users"):
    if st.session_state.chat_id not in past_chats.keys():
        past_chats[st.session_state.chat_id] = st.session_state.chat_title
        joblib.dump(past_chats, 'data/past_chats_list')
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("Checking...") as status:
        # ai_response = pd.DataFrame(np.random.randn(50, 20), columns=("col %d" % i for i in range(20)))
        ai_sqlresponse = getsqlquery(prompt)
        sql_query = sqlvalidator.parse(ai_sqlresponse)
        if sql_query.is_valid():
            ai_response = getsqldata(ai_sqlresponse)
            print(ai_sqlresponse)
        else:
            ai_response = random.choice(mssg)
        if isinstance(ai_response, pd.DataFrame):
            try:
                st.chat_message("AI").dataframe(ai_response, hide_index=True)
                st.session_state.gemini_history.append(
                    {"Question": prompt, "Query": ai_sqlresponse})
                st.session_state.messages.append(
                    {"role": "AI", "content": ai_response})
            except:
                pass
        else:
            st.chat_message("AI").markdown(ai_response)

    move_focus()


joblib.dump(
    st.session_state.messages,
    f'data/{st.session_state.chat_id}-st_messages',
)
joblib.dump(
    st.session_state.gemini_history,
    f'data/aidata-gemini_messages',
)
