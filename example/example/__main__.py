import uvicorn
from daedalus import initialize_daedalus

def main():
    app = initialize_daedalus()
    print("Daedalus application initialized successfully")
    print("Starting server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()