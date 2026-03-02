def generate_otp():
    # Default static OTP for now
    return "1234"


def verify_otp(user_otp, real_otp):
    return user_otp == real_otp
