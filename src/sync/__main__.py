def main():
    """Entry point for the sync UI.
    Executes the Flask application defined in pr_sync.ui.app.
    """
    # Import inside function to avoid heavy imports when the module is imported elsewhere.
    from pr_sync.ui.app import app
    # Run Flask development server
    app.run(host="127.0.0.1", port=5000, debug=True)

if __name__ == "__main__":
    main()
