@echo off
SET "SALT_FIXED=73616c7465646861"
openssl enc -d -base64 -pbkdf2 -aes-256-ecb -S %SALT_FIXED% -k %PASS_FIXED%