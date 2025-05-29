from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

senha_admin = 'admin123'
hash = bcrypt.generate_password_hash(senha_admin).decode('utf-8')
print(hash)