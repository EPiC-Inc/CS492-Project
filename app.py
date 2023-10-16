try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

from app import app


app.run(host='0.0.0.0', port=81)
