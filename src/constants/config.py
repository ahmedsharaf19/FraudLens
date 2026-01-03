from src.constants import BOLD, CYAN, BLUE, YELLOW, MAGENTA, GREEN, RESET

DATA_PATH = "dataset"
OUTPUT_PATH = 'outputs'

COLUMNS = [
    'step',              
    'type',              
    'amount',            
    'nameOrig',          
    'oldbalanceOrg',     
    'newbalanceOrig',    
    'nameDest',          
    'oldbalanceDest',    
    'newbalanceDest'    
]


NUMERIC_COLUMNS = {
    'step': int,
    'amount': float,
    'oldbalanceOrg': float,
    'newbalanceOrig': float,
    'oldbalanceDest': float,
    'newbalanceDest': float
}

CATEGORICAL_COLUMNS = [
    'type',
    'nameOrig',
    'nameDest'
]

E = 1e-6


MENU = [
    "📂 Loading dataset(s)",
    "🧹 Cleaning data",
    "👤 Building customer featuress",
    "💳 Building transaction features",
    "🧐 Calculating customer risk score",
    "🚨 Flagging suspicious transactions",
    "📊 Display Summary",
    "🗃️ Export Reports",
    "💹 Export Dashboard",
    "👋 Exiting FRAUDLENS"
]


banner = f"""
{BOLD}{CYAN}🔍💳  FRAUDLENS  💳🔍{RESET}

{BLUE}
░██████████                                      ░██ ░██                                          
░██                                              ░██ ░██                                          
░██        ░██░████  ░██████   ░██    ░██  ░████████ ░██          ░███████  ░████████   ░███████  
░█████████ ░███           ░██  ░██    ░██ ░██    ░██ ░██         ░██    ░██ ░██    ░██ ░██        
░██        ░██       ░███████  ░██    ░██ ░██    ░██ ░██         ░█████████ ░██    ░██  ░███████  
░██        ░██      ░██   ░██  ░██   ░███ ░██   ░███ ░██         ░██        ░██    ░██        ░██ 
░██        ░██       ░█████░██  ░█████░██  ░█████░██ ░██████████  ░███████  ░██    ░██  ░███████  
{RESET}

{YELLOW}📊  Statistical Analysis Risk Scoring & Anomaly Detection{RESET}
{MAGENTA}🧠  Banking Transactions Intelligence System{RESET}

{GREEN}© Ahmed Sharaf – ITI-AI{RESET}
"""

SPACE_STEP = 5
SPACE = "\t"*SPACE_STEP