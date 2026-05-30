from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import Tool 
from datetime import datetime
import uuid 

search = DuckDuckGoSearchRun()


def search_tool (query : str ) -> str:
    """Search the web for information"""
    try: 
       return search.run(query)
    
    except Exception as e:
       return f"Search Eorro : {str(e)}"


    
    