from dotenv import load_dotenv
import os

load_dotenv()
HF_TOKEN = os.getenv("HG_TOKEN")
print(HF_TOKEN)  
