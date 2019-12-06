# flask-dashboard
A realtime dashboard built on Creative Tim's dashboard template.
# flask-dashboard
A realtime dashboard built on Creative Tim's dashboard template.
## Build from sources

#Caveat: This application works primarily with python 3.6+. For python 3.8 systems, ensure you upgrade your dependencies, especially SQLAlchemy and Flask-SQLAlchemy to their latest versions. Older versions of these dependencies have a deprecated method `time.clock` which has been removed in python 3.8. Upgrading these dependencies will solve the problems you may encounter while running this app.

#To Run using python3.6+:
After cloning this app, see how to clone below:

On Windows:
```
  $env\Scripts\activate
  $python app.py
```

On Linux and MacOS:
```
  $source env/bin/activate
  $python app.py
```

For normal setting up,
#Optional


1. Clone the repo: All OS
  ```
  $ git clone https://github.com/Sirneij/flask-dashboard.git
  $ cd flask-dashboard
  ```

2. Initialize and activate a virtualenv:Linux and MacOS
  ```
  $ pip install virtualenv
  $ python3 -m venv venv
  $ . venv/bin/activate

  ```
  On Windows:
 ```
 >pip install virtualenv
 >py -3 -m venv venv
 >venv\Scripts\activate
 ```
3. Install the dependencies:
  ```
  $ pip install -r requirements.txt
  ```

5. Run the development server:
  ```
  $ python app.py
  ```

6. Navigate to [http://localhost:5000](http://localhost:5000) using any browser.
