from peru_chef_app import app
from peru_chef_app.controllers import posts, users

if __name__=="__main__":
    app.run(debug=True)