from app import db

class Coupon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100), unique=True, nullable=False)
    claimed = db.Column(db.Boolean, default=False)

class Claim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coupon_id = db.Column(db.Integer, db.ForeignKey('coupon.id'), nullable=False)
    user_ip = db.Column(db.String(100), nullable=False)
    user_agent = db.Column(db.String(200), nullable=False)

    coupon = db.relationship('Coupon', backref='claims')
