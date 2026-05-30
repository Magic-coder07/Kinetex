from pydantic import BaseModel
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate

class ResearchResponse (BaseModel): # wt we need in research 
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

   # calling local model
llm = ChatOllama(
    model="gemma3:4b",
    base_url= "http://localhost:11434",
    temperature=0.7
)

  # covering into strs 
parser = PydanticOutputParser(pydantic_object=ResearchResponse)
format_instructions = parser.get_format_instructions()


 # Creating Prompt
# Build the system message as a plain string – no outer f‑string

system_message = (
    "You are a research assistant that helps generate research papers.\n"
    "Answer the user query and use necessary tools.\n"
    "Wrap the output in this format and provide no other text:\n\n"
    + format_instructions   # contains literal {topic}, {summary}, etc.
)

# Create the prompt template safely
prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content=system_message),                    # fixed, not a template
    HumanMessagePromptTemplate.from_template("{query}"),      # variable part
])
   # CREATING CHAIN to understand the flow 
chain = prompt | llm | parser

  #Main Loop
while True:

    query = input("\nHow can I help you today?(entre 'q' or 'exit' or 'quit')\n")

    if query.lower() in ["q", "exit", "quit"]:
        print("GoodBye See You later MOTHERFUCKER !")
        break
    
    if "research" in query.lower() or "paper" in query.lower():
        try:
            result = chain.invoke({"query": query})
            print("\n" + "="*50)
            print("Research Response :")
            print("="*50)
            print(f"Topic: {result.topic}")
            print(f"\nSummary: {result.summary}")
            print(f"\nSources: {', '.join(result.sources)}")
            print(f"\nTools Used: {', '.join(result.tools_used)}")
        
        except Exception as e:
            print("Error",e)

    else:
        # short answers 
        respones = llm.invoke(f"Answers in briefly: {query}")
        print("\n" + "="*50)
        print("ANSWER :")
        print("="*50)
        print(respones.content)
