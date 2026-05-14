import streamlit as st
from langchain_community.tools import ArxivQueryRun,WikipediaQueryRun,DuckDuckGoSearchRun
from langchain_community.utilities import ArxivAPIWrapper,WikipediaAPIWrapper
from langchain_groq import ChatGroq
from langchain.agents import create_agent


st.title("Langchain chat with websearch")
st.write("This AI agent can search the web, Wikipedia, and Arxiv papers.")
st.sidebar.title("settings")
groq_api_key=st.sidebar.text_input("Enter your groq API key",type="password")

arxiv_api_wrapper= ArxivAPIWrapper(top_k_results=1,doc_content_chars_max=300)
wikipedia_api_wrapper = WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=300)

arxiv_tool=ArxivQueryRun(api_wrapper=arxiv_api_wrapper)
wikipedia_tool=WikipediaQueryRun(api_wrapper=wikipedia_api_wrapper)

search_tool=DuckDuckGoSearchRun()
tools=[arxiv_tool,wikipedia_tool,search_tool]


if "messages" not in st.session_state:
    st.session_state.messages =[
        {
            "role": "assistant",
            "content": "Hi! I can search the web and research papers. Ask me anything"
        }
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
    
prompt=st.chat_input(placeholder="Ask something...")

if prompt:
    
    st.session_state.messages.append(
       {
          "role": "user",
          "content": prompt  
       }
    )
    st.chat_message("user").write(prompt)
    
    llm=ChatGroq(groq_api_key=groq_api_key,model="openai/gpt-oss-120b")
    
    agent=create_agent(model=llm,tools=tools)    
    
       
    #agent invoke
      
    response = agent.invoke(
        {
            #invoke with chat histoy
            "messages": st.session_state.messages 
            #invoke with out chat history   
            # "messages": [ ("user",prompt) ]
        },
        
                
    )
  
        
    final_response= response["messages"][-1].content
    
    st.write(final_response)
    
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": final_response
        }
    )
    

    




