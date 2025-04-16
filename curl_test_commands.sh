
PHONE_SUCCESS="09191111111"
PHONE_FAIL="09190000000"

# 1. تست درخواست OTP برای کاربر جدید (موفق)
echo "OTP request test for $PHONE_SUCCESS:"
RESPONSE=$(curl -s -X POST http://localhost:8000/api/otp/request/ \
-H "Content-Type: application/json" \
-d "{\"phone_number\": \"$PHONE_SUCCESS\"}")
echo "$RESPONSE"

# استخراج کد OTP از پاسخ (فرض می‌کنیم پاسخ JSON است)
OTP_CODE=$(echo "$RESPONSE" | grep -oE '[0-9]{6}')
if [ -z "$OTP_CODE" ]; then
    echo "error: OTP code not received!"
    exit 1
fi

echo "Extracted OTP code: $OTP_CODE"


# 2. تست تأیید OTP با کد درست برای شماره موفق
echo -e "\n\nOTP verifying test for $PHONE_SUCCESS:"
curl -X POST http://localhost:8000/api/otp/verify/ \
-H "Content-Type: application/json" \
-c cookies_success.txt \
-d "{\"phone_number\": \"$PHONE_SUCCESS\", \"code\": \"$OTP_CODE\"}"

# 3. تست درخواست OTP برای شماره دیگر (برای بلاک شدن)
echo -e "\n\nOTP request test for $PHONE_FAIL:"
curl -X POST http://localhost:8000/api/otp/request/ \
-H "Content-Type: application/json" \
-d "{\"phone_number\": \"$PHONE_FAIL\"}"

# 4. تست سه بار تلاش ناموفق برای تأیید OTP و بلاک شدن
#(otp verifying)
echo -e "\n\nthree failed attempt test for $PHONE_FAIL:" 
for i in {1..3}; do
    curl -X POST http://localhost:8000/api/otp/verify/ \
    -H "Content-Type: application/json" \
    -d "{\"phone_number\": \"$PHONE_FAIL\", \"code\": \"wrongcode\"}"
done

# 5. تست درخواست OTP در حالت بلاک برای شماره بلاک‌شده
echo -e "\n\nOTP request test when $PHONE_FAIL is blocked:"
curl -X POST http://localhost:8000/api/otp/request/ \
-H "Content-Type: application/json" \
-d "{\"phone_number\": \"$PHONE_FAIL\"}"

# 6. تست تکمیل پروفایل برای شماره موفق
echo -e "\n\nprofile completing test for $PHONE_SUCCESS:"
curl -X POST http://localhost:8000/api/profile/ \
-H "Content-Type: application/json" \
-b cookies_success.txt \
-d "{\"first_name\": \"علی\", \"last_name\": \"محمدی\", \"email\": \"ali@example.com\", \"password\": \"newpassword123\"}"

# 7. تست ورود با رمز عبور برای شماره موفق
echo -e "\n\nloggin in with password test for $PHONE_SUCCESS:"
curl -X POST http://localhost:8000/api/login/ \
-H "Content-Type: application/json" \
-c cookies_new.txt \
-d "{\"phone_number\": \"$PHONE_SUCCESS\", \"password\": \"newpassword123\"}"

# 8. تست سه بار تلاش ناموفق ورود با رمز اشتباه و بلاک شدن
# (logging in with password)
echo -e "\n\nthree failed attempt test for $PHONE_SUCCESS:" 
for i in {1..3}; do
    curl -X POST http://localhost:8000/api/login/ \
    -H "Content-Type: application/json" \
    -d "{\"phone_number\": \"$PHONE_SUCCESS\", \"password\": \"wrongpassword\"}"
done

# تمیز کردن فایل‌های کوکی
rm cookies_success.txt cookies_new.txt