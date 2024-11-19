from pydantic import BaseModel
from typing import Dict, List, Optional

class StatData(BaseModel):
    total_tools: int
    available_tools: int
    reserved_tools: int

    # List of tool name and ID pairs
    most_reserved_tools: List[Dict[str, str]]  
    least_reserved_tools: List[Dict[str, str]] 
