from backend import app

if __name__ == "__main__":
    print("songs application.")
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )