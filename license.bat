@echo off
setlocal EnableDelayedExpansion
color 0A
title License Key Protected Script

set "VALID_KEYS=00x12u2838u89djwc778dcnmcdc 00xsuhd798he87ghewyhdhasbds 00xy9q23d98qyus798yduashdau 00xsdh98u3whe97wqehriuyfhwu 00xujhnd78asyd7qhqdy7u2yhdu 00xndsaudhsuad893dwqdwqdqwd 00x09saujf803ujf82uh38f9732 00x3xhynd378hsxrn783trcn3rc 00xynd378hsxrn783trcn3rcbzf 00x92xnqhe83cn28dhq7fh3nqzs 00xdn28xmcq29qdhz62mcxhejsv 00x83nch72mcxhd8273nsjdhqzd 00x28xnwq7cnc93ndh28ehxqwst 00xs72mcxn28qcnw73dhq2mshqh 00x3hdn29xmc28wqdhsh37euiqy 00xxcnw83dhqmc7sh28xn3qpsdh 00xndhcq72wqmxzns93he8dnszb 00x9283ndhe8nsq92mxchqwns9n 00x73nchd9283xns92mcwheh3sc 00x82ncmq9dhdnwq72cn38dnxwc 00xhs9x83ndqshc93nqwe7cnxss 00xdxh378dmcq2nshe93nxqwdza 00xq92mcnxh83nsh28cnsqmx87x 00x9cnxw93nd8xqhe72nsxcm2hd 00x83hcwqdm9zdh28nsqcmxhe93 00xdnsh28nsq9xwcm3hsdne92c2 00xcx823dshnmw7c8xhe29shqwd 00x8nxq92mcnhs83zqdnwmx82e5 00xq82xcnw3hd9zshcnq82mxdwv 00x93ndxh28mcqshe72ncxdsh31 00xxmcnsq7dhdnwz9mxchseu39k 00xsx92hdwqzndxh37cnq92ejsc 00x2qndwmc93ne82zshxcmnsd3z 00xd83qmcw2xnsd93heuxncm381 00xcnshd92mxzqwnc8dhesu3296 00xe29mcnsq83nchd7w9squ32nn 00xxzqcnwd3hehs29mxqnsue937 00x28ndqh29shxnqwm3esudnx7l"

set "USED_KEYS_FILE=used_keys.txt"
set "HARDWARE_FILE=hardware.txt"

for /f "tokens=2 delims==" %%A in ('wmic csproduct get UUID /value') do set "HARDWARE_ID=%%A"

:RETRY
cls
echo.
echo --------------------------------------
echo         LICENSED ACCESS REQUIRED
echo --------------------------------------
echo.
set /p "LICENSE=Enter your license key: "

set "KEY_VALID=0"
for %%k in (%VALID_KEYS%) do (
    if /I "!LICENSE!"=="%%k" set "KEY_VALID=1"
)

if !KEY_VALID!==0 (
    echo.
    echo ERROR: Invalid license key.
    timeout /t 2 /nobreak >nul
    goto RETRY
)

findstr /I "!LICENSE!" %USED_KEYS_FILE% >nul
if !errorlevel! == 0 (
    findstr /I "!LICENSE! - !HARDWARE_ID!" %HARDWARE_FILE% >nul
    if !errorlevel! == 0 (
        echo.
        echo Access granted. Welcome back!
    ) else (
        echo.
        echo ERROR: This key is associated with a different machine.
        timeout /t 2 /nobreak >nul
        goto RETRY
    )
) else (
    echo !LICENSE! - !HARDWARE_ID!>>%USED_KEYS_FILE%
    echo !LICENSE! - !HARDWARE_ID!>>%HARDWARE_FILE%
    echo.
    echo Access granted. Welcome!
)

:: Send Webhook
curl -s -X POST !FULL_WEBHOOK! ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"License Logger\", \"content\":\"LICENSE USED: !LICENSE! - Hardware ID: !HARDWARE_ID! - %%USERNAME%%\"}" >nul

cls
echo Protected script running...
pause
