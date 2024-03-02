from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect



# Initialize Flask application
app = Flask('__name__')

#  Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:pass%40word@localhost/test'

# Initialize SQLAlchemy with Flask application:
db = SQLAlchemy(app)


# Routing
@app.route('/')
def test():
    return render_template('test.html', user=user, all_users=all_users)


class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200), unique=True, nullable=True)
    password = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(255), unique=True, nullable=True)
    
    def __repr__(self):
        return '<User %r>' % self.username
    
    

def create_tables_if_not_exist():
    with app.app_context():
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        if not tables:
            db.create_all()


# Create the database tables
with app.app_context():
    create_tables_if_not_exist()
    action = 'read'

    # CREATE
    if action == 'create':
        new_user = User(username='moha', password= 'mohapass', email='moha@example.com')
        db.session.add(new_user)
        db.session.commit()

    # READ
    if action == 'read':
        all_users = db.session.query(User).all()
        user = db.session.get(User, 13)

        print(user.username)
    
    # UPDATE
    if action == 'update':
        user = db.session.get(User, 1)
        user.password = 'fuckingpassword'
        db.session.commit()

    # DELETE
    if action == 'delete':
        user = User.query.get(9)
        db.session.delete(user)
        db.session.commit()

    # Close Session
    db.session.close()






# App Running
if __name__ == '__main__':
    app.run(debug=True)