<h1 align="center">Odin Assignment Management System(Odin AMS)</h1>

➔ With Odin AMS teachers will be able to leave behind the old
paper homework diaries and instead use a more intuitive online
homework and assignment system which will make it easier for students
to keep track of what they have been set

### ➔ Technical Details
**Languages:**
```Python3, HTML5, CSS3, JavaScript```

**Frameworks:**
```Flask, Bootstrap, DataTable.net```

**Database:**
```MySQL, SQLite```

### ➔ Project Setup
Install all requirements by running command below -
```
pip install -r requirements.txt
```

#### ➔ Database Setup
1. By default, a local database is configured. We recommend using it since 
it's more agile and stable.
   
    Initialise the database using below command in python console
    ```
    from models import init_db
    init_db()
    ```
2. An external database is also provided. 

    If you want to use it, comment out the local database configuration and 
    using the external database config we provided in the `app.py`

    **NOTE**: We assume that you can provide 
   related `UniUsername` and `UniPassword` credentials to establish
   ssh tunnel.

    Install `mysqlclient` for external database connection
    ```
    pip install mysqlclient
    ```

Run app.py using below command to start Flask 
```
python app.py
```
Once link has been clicked you should be taken to our login page

### ➔ Functionality
- **Students** - Students are able to view their profile,
view the courses which they are enrolled in and view
assignments that they have been set.
- **Teachers** - Teachers are able to view their profile,
view courses they teach as well as create new ones and
add students to a course. They are also able to create
and update assignments and view student information.
- **Admins** - Admins are able to create and view schools
create, update, delete and add people to a course. Able to
update and delete assignments. Approve users. View
security log
