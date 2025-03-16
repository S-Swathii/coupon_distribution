from datetime import datetime, timedelta

# Dictionary to store IP addresses and their last claim time
ip_claims = {}

def is_ip_on_cooldown(user_ip):
    cooldown_period = timedelta(minutes=5)  # Set cooldown period to 5 minutes
    if user_ip in ip_claims:
        last_claim_time = ip_claims[user_ip]
        if datetime.now() - last_claim_time < cooldown_period:
            return True
    # Update the last claim time for the IP address
    ip_claims[user_ip] = datetime.now()
    return False
