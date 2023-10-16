from app import app

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

app.run(host='0.0.0.0', port=81)
