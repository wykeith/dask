@echo off

echo $env:PASS_FIXED = 'password'

git config --global user.email 'wykeith@gmail.com'
git config --global user.name 'wykeith'

REM git config --global filter.openssl.smudge C:\\data\\notebooks\\notebooks\\tools\\smudge_filter_openssl.bat
REM git config --global filter.openssl.clean C:\\data\\notebooks\\notebooks\\tools\\clean_filter_openssl.bat
REM git config --global diff.openssl.textconv C:\\data\\notebooks\\notebooks\\tools\\diff_filter_openssl.bat
REM git config --global core.attributesfile C:\data\notebooks\notebooks\gitattributes

SET CWD=%~dp0
SET CURRENTDIR=%CWD:\=\\%
echo %CURRENTDIR%
git config --global filter.openssl.smudge %CURRENTDIR%tools\\smudge_filter_openssl.bat
git config --global filter.openssl.clean %CURRENTDIR%tools\\clean_filter_openssl.bat
git config --global diff.openssl.textconv %CURRENTDIR%tools\\diff_filter_openssl.bat
git config --global core.attributesfile %CURRENTDIR%\gitattributes

REM [Environment]::GetEnvironmentVariable("PASS_FIXED","Machine")
REM powershell -noprofile -command "$Input | openssl enc -d -base64 -pbkdf2 -aes-256-ecb -S %SALT_FIXED% -k %PASS_FIXED%"