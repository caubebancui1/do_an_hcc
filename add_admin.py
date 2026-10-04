<<<<<<< HEAD
from app import app, db
from sqlalchemy import text
from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()

    rows = db.session.execute(text('SHOW COLUMNS FROM accounts')).all()
    cols = [row[0] for row in rows]

    if 'pass' not in cols:
        db.session.execute(text('ALTER TABLE accounts ADD COLUMN pass VARCHAR(255) NOT NULL DEFAULT ""'))

    if 'password_hash' in cols:
        db.session.execute(text('UPDATE accounts SET pass = password_hash WHERE pass = "" OR pass IS NULL'))
        db.session.execute(text('ALTER TABLE accounts DROP COLUMN password_hash'))

    if 'role' in cols:
        db.session.execute(text('ALTER TABLE accounts DROP COLUMN role'))

    if 'created_at' in cols:
        db.session.execute(text('ALTER TABLE accounts DROP COLUMN created_at'))

    db.session.execute(
        text("INSERT INTO accounts (username, pass) VALUES (:u, :p) ON DUPLICATE KEY UPDATE pass = VALUES(pass)"),
        {'u': 'admin', 'p': generate_password_hash('123')},
    )
    db.session.commit()
    print('ADMIN_READY')
    print(db.session.execute(text('SHOW COLUMNS FROM accounts')).all())
=======
from app import app, db
from sqlalchemy import text
from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()

    rows = db.session.execute(text('SHOW COLUMNS FROM accounts')).all()
    cols = [row[0] for row in rows]

    if 'pass' not in cols:
        db.session.execute(text('ALTER TABLE accounts ADD COLUMN pass VARCHAR(255) NOT NULL DEFAULT ""'))

    if 'password_hash' in cols:
        db.session.execute(text('UPDATE accounts SET pass = password_hash WHERE pass = "" OR pass IS NULL'))
        db.session.execute(text('ALTER TABLE accounts DROP COLUMN password_hash'))

    if 'role' in cols:
        db.session.execute(text('ALTER TABLE accounts DROP COLUMN role'))

    if 'created_at' in cols:
        db.session.execute(text('ALTER TABLE accounts DROP COLUMN created_at'))

    db.session.execute(
        text("INSERT INTO accounts (username, pass) VALUES (:u, :p) ON DUPLICATE KEY UPDATE pass = VALUES(pass)"),
        {'u': 'admin', 'p': generate_password_hash('123')},
    )
    db.session.commit()
    print('ADMIN_READY')
    print(db.session.execute(text('SHOW COLUMNS FROM accounts')).all())
>>>>>>> 20e273270e4e56e8663036fc5b11e7151b128a20
