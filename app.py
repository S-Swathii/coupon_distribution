from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from ip_tracker import is_ip_on_cooldown

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///coupons.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Initialize the database
with app.app_context():
    db.create_all()

@app.route('/coupons', methods=['GET'])
def get_coupons():
    coupons = Coupon.query.all()
    return jsonify([{'id': coupon.id, 'code': coupon.code, 'claimed': coupon.claimed} for coupon in coupons])

@app.route('/admin/coupons', methods=['GET'])
def admin_get_coupons():
    coupons = Coupon.query.all()
    return jsonify([{'id': coupon.id, 'code': coupon.code, 'claimed': coupon.claimed} for coupon in coupons])

@app.route('/admin/add_coupon', methods=['POST'])
def admin_add_coupon():
    data = request.json
    new_coupon = Coupon(code=data['code'])
    db.session.add(new_coupon)
    db.session.commit()
    return jsonify({'message': 'Coupon added successfully!'}), 201

@app.route('/admin/update_coupon/<int:coupon_id>', methods=['PUT'])
def admin_update_coupon(coupon_id):
    data = request.json
    coupon = Coupon.query.get(coupon_id)
    if coupon:
        coupon.code = data['code']
        db.session.commit()
        return jsonify({'message': 'Coupon updated successfully!'}), 200
    return jsonify({'message': 'Coupon not found.'}), 404

@app.route('/admin/toggle_coupon/<int:coupon_id>', methods=['PATCH'])
@app.route('/coupon/<int:coupon_id>', methods=['GET'])
def get_coupon(coupon_id):
    coupon = Coupon.query.get(coupon_id)
    if coupon:
        return jsonify({'id': coupon.id, 'code': coupon.code, 'claimed': coupon.claimed}), 200
    return jsonify({'message': 'Coupon not found.'}), 404

def admin_toggle_coupon(coupon_id):
    coupon = Coupon.query.get(coupon_id)
    if coupon:
        coupon.claimed = not coupon.claimed
        db.session.commit()
        return jsonify({'message': 'Coupon availability toggled successfully!'}), 200
    return jsonify({'message': 'Coupon not found.'}), 404

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to the Coupon Distribution API!'}), 200

@app.route('/claim_coupon', methods=['POST'])

def claim_coupon():

    data = request.json
    user_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')

    # Logic for claiming a coupon with IP and cookie tracking
    cookie_id = request.cookies.get('coupon_claimed')
    if cookie_id:
        return jsonify({'message': 'You have already claimed a coupon in this session.'}), 429

    if is_ip_on_cooldown(user_ip):
        return jsonify({'message': 'You have recently claimed a coupon. Please wait before claiming again.'}), 429

    coupon = Coupon.query.filter_by(claimed=False).first()

    if coupon:
        coupon.claimed = True
        new_claim = Claim(coupon_id=coupon.id, user_ip=user_ip, user_agent=user_agent)
        response = jsonify({'message': 'Coupon claimed successfully!', 'coupon_code': coupon.code})
        response.set_cookie('coupon_claimed', 'true', max_age=300)  # Set cookie for 5 minutes

        db.session.add(new_claim)
        db.session.commit()
        return jsonify({'message': 'Coupon claimed successfully!', 'coupon_code': coupon.code}), 200
    else:
        return jsonify({'message': 'No coupons available or all claimed.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
