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


banner = r"""
🔍💳  FRAUDLENS  💳🔍

  ______   _____               _    _   _____    _        ______   _   _    _____ 
 |  ____| |  __ \      /\     | |  | | |  __ \  | |      |  ____| | \ | |  / ____|
 | |__    | |__) |    /  \    | |  | | | |  | | | |      | |__    |  \| | | (___  
 |  __|   |  _  /    / /\ \   | |  | | | |  | | | |      |  __|   | . ` |  \___ \ 
 | |      | | \ \   / ____ \  | |__| | | |__| | | |____  | |____  | |\  |  ____) |
 |_|      |_|  \_\ /_/    \_\  \____/  |_____/  |______| |______| |_| \_| |_____/ 

📊  Statistical Analysis Risk Scoring & Anomaly Detection
🧠  Banking Transactions Intelligence System

© Ahmed Sharaf – ITI-AI
"""

SPACE_STEP = 5
SPACE = "\t"*SPACE_STEP