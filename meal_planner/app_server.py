from flask import Flask, render_template, request, redirect, make_response, session

# import os
# import cloudinary
# import cloudinary.uploader

# cloudinary.config(
#     cloud_name='',
#     api_key='666411695648593',
#     api_secret='gLfAh3MdZ4VKslaBWdIleMtyEHw',
# )

app = Flask(__name__) 

@app.route('/')
def index():
    return render_template('login.html')



# Run the server
app.run(debug=True)
