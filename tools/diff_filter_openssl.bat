@echo off
SET "SALT_FIXED=73616c7465646861"
openssl enc -d -base64 -pbkdf2 -aes-256-ecb -k $PASS_FIXED -in %~1