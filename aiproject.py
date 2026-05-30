import dotenv
from pydantic import BaseModel
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_agent
#from tools import search_tool 
import uuid

dotenv.load_dotenv()

class ResearchResponse(BaseModel): # Creates a blueprint for ai agent
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

llm = ChatOllama(model="gemma3:4b")
parser = PydanticOutputParser(pydantic_object=ResearchResponse) # LLM text output into ResearchResponse instances
format_instructions = parser.get_format_instructions() # this instructions tells the LLM how to format its output

# Create RESEARCH agent for structured research papers
research_system_prompt = f"""You are a research assistant that helps generate research papers.
Answer the user query and use necessary tools.
Wrap the output in this format and provide no other text:

{format_instructions}"""

#tools = [search_tool] #from wikipidia search 

research_agent = create_agent(
    model=llm,
    system_prompt=research_system_prompt,
    tools=[]
)

# Create DIRECT ANSWER agent for simple questions
direct_system_prompt = """You are a helpful assistant. Answer the user's question directly and concisely.
Do NOT generate a research paper. Just give a simple, direct answer."""

direct_agent = create_agent(
    model=llm,
    system_prompt=direct_system_prompt,
    tools=[]
)

# Choose which agent to use based on the query

#query = "Tell me about St. Joseph father of Lord Jesus life give me the research paper"

while(True):

  query = input("How can I help you ?\n")

  if "research" in query.lower() or "paper" in query.lower():
    response = research_agent.invoke({"messages": [{"role": "user", "content": query}]}) #  role: "user" - Message from user ,content: query - question
 
    
    try:
        # Handle different response structures
        if isinstance(response, dict):
            if "output" in response:
                output_respose = response["output"][0]["text"] if isinstance(response["output"], list) else response["output"]
            elif "messages" in response:
                output_respose = response["messages"][-1].content
            else:
                output_respose = str(response)
        else:
            output_respose = str(response)
        
        # makes output structured format
        structured_output = parser.parse(output_respose)
        print("\n" + "="*50)
        print("RESEARCH RESPONSE:")
        print("="*50)
        print(f"Topic: {structured_output.topic}")
        print(f"\nSummary: {structured_output.summary}")
        print(f"\nSources: {', '.join(structured_output.sources)}")
        print(f"\nTools Used: {', '.join(structured_output.tools_used)}")
        
    except Exception as e:
        print(f"\nError parsing response: {e}")
        print("Raw response:", response)
  else:
    response = direct_agent.invoke({"messages": [{"role": "user", "content": query}]})
    
    # Extract and display direct answer
    if isinstance(response, dict):
        if "messages" in response:
            direct_answer = response["messages"][-1].content
        elif "output" in response:
            direct_answer = response["output"][0]["text"] if isinstance(response["output"], list) else response["output"]
        else:
            direct_answer = str(response)
    else:
        direct_answer = str(response)
    
    print("\n" + "="*50)
    print("DIRECT ANSWER:")
    print("="*50)
    print(direct_answer)

    if(query== "q" or "Q"):
        break;
