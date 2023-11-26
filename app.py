from genderTracker.setup import app

import genderTracker.views
import genderTracker.api

if __name__ == "__main__":
    import os
    port = os.environ.get("FLASK_PORT", 5000)
    app.run("0.0.0.0", int(port), debug=True)
