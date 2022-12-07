A “design document” for your project in the form of a Markdown file called DESIGN.md that discusses, technically, how you implemented your project and why you made the design decisions you did. Your design document should be at least several paragraphs in length. Whereas your documentation is meant to be a user’s manual, consider your design document your opportunity to give the staff a technical tour of your project underneath its hood.

FOMO is a Python-Flask application that makes use of SQLAlchemy as a database for the backend processing. This design document will walk through some of the technical specifications used in the project.

1. models.py
models.py defines what are called "Models" in SQLAlchemy, which is the equivalent of tables, but act as Python classes. Its attributes are converted to table columns, and the "relationship" function defines unilateral relationships between parent and child tables.

For this project, we have four tables: User (user authentication data), Org (organization information, linked to a user), Party (party information, linked to an organization), and Review (data containg ratings and comments, linked to a user and a party)

2. forms.py
forms.py makes use of the Flask-WTForm module to easily generate beautiful forms and manage form validation in a way that is cleaner than traditional HTML forms.

The HostPartyForm is for hosting events - note the CKEditorField which is essentially a longer text field, and validate function which uses the FlaskForm.validate method to create a custom validation form, in this case to ensure that the datetime selected is after the present moment.

The UserRegisterForm, OrgRegisterForm and LoginForm are fairly straightforward and manage user authentication, linked to their respective databases when imported through app.py.

Finally, the ReviewForm is for users to review a specific party; here the SelectField is used to get numerical input from users.

3. config.py
As this application is hosted locally and not on a public server (as it might be eventually), for now config.py serves to configure the secret key that Flask requires for running. More on its use in README.md.

4. app.py (General)
Before going into the specific routes, some general features of app.py are that it uses Flask-Login, which requires certain initializations (e.g. the LoginManager object at line 33), as well as using wraps from functools to create two custom decorator functions: one to lock routes to users, and another to lock users to organizations.

5. base.html
base.html is a custom Jinja template that all of our pages inherit from; importantly, it itself inherits from the bootstrap base, with the additional features of the page title (displayed in the browser tab), as well as the navigation bar, finally creating a block for content to be added when inherited. This makes use of Flask-Bootstrap functionality, so certain blocks like {% block head %} and the {{ super() }} that follows, are inbuilt to the package.

5. app.py (register) and register.html
Both register and register.html dynamically manage two possible registration outcomes: one for users and one for organizations. This is using Flask's dynamic URL creation via <string:user_type> in the path, which is then passed as an argument into the register function. This allows us to check which form should be rendered. Afterwards, when the form is validated, we use SQLAlchemy to add it into the database. The user is then logged in and redirected to the homepage. As the page contains some hyperlinks, register.html makes use of {{ url_for('login') }}, for example, as a means of rerouting users. Also, the {{ wtf.quick_form }} is a means of easily displaying the form without HTML hassle.

6. app.py (login, logout) and login.html
In a similar way to register and register.html, the form functionality relies on WTForms and Flask-Bootstrap, while the login/logout functionality relies on the Flask-Login package. Simply put, it queries the database and compares it to the input from the user, authenticating accordingly.

7. app.py (host) and host.html
This is one of the simpler routes, which is yet another implementation of WTForms; key here is the addition of a new Party into the database using the data from the form.

8. app.py (organizations, parties) and orgs.html, parties.html
These two routes are analogous to each other in that they take a result of a query into the database, then list it out in table form using Jinja for loops. The most complex aspect is that SQLAlchemy's JOIN queries are a little complicated when data is spread out over multiple tables (involving Tuples), so we use list comprehension to make it look clean within the Jinja template.

9. app.py (organization, party) and org.html, party.html
These two routes are analogous in that they are hyperlinked through the previous page, when the user clicks to view a singular organization/party's data. This involves once again dynamic URL creation. For the possibility that multiple parties might have the same name, the URL is written to include the index of the party within the list of parties with this same name.

Most unique about the party route in particular is that it contains yet another form: the Review form. It then queries the database for the reviews and displays them within the same page. Again, list comprehension is used here to make it look better in the templates themselves. Notably, party.html makes use of multiple Jinja for loops and if statements to ensure that all comments are displayed.

