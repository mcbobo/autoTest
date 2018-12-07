@echo off
title auto_install
cd %~dp0

echo.
echo ************************************************************
echo *                   Install node                           *
echo ************************************************************
echo.
start /wait node-v6.11.3-x64.msi
echo.
echo === install NPM taobao image
cmd /c "npm install -g cnpm --registry=https://registry.npm.taobao.org"
echo.
echo ************************************************************
echo *                   Install appium1.8.2                    *
echo ************************************************************
echo.
cmd /c "cnpm install appium@1.8.2 -g"
cmd /c "appium -v"
echo.
echo ************************************************************
echo *                   Install python 3.5                     *
echo ************************************************************
echo.
start /wait python-3.5.0-amd64.exe
echo.
echo.
set /P EN=please already installed python,pip press enter to install Appium-Python-Client!
echo.
echo ************************************************************
echo *                   Install Appium-Python-Client           *
echo ************************************************************
echo.
cmd /c "pip install Appium-Python-Client"
echo.
echo ************************************************************
echo *                   Install JDK                            *
echo ************************************************************
echo.
start /wait jdk-8u5-windows-x64.exe
echo.
echo.
set /P EN=please downloaded Andriod sdk
echo.
set javahome=C:\Program Files\Java\jdk1.8.0_05
set androidhome=D:\Appium\SDK
set ENV_PATH=%PATH%
set androidpath=%%ANDROID_HOME%%\tools;%%ANDROID_HOME%%\platform-tools;%%ANDROID_HOME%%\build-tools\27.0.1;
set javapath=%%JAVA_HOME%%\bin;%%JAVA_HOME%%\jre\bin;
echo.
echo.
echo ************************************************************
echo *                   set environment                        *
echo ************************************************************
echo.
echo.
echo === set environment: JAVA_HOME=%javahome%
echo === Warning: if JAVA_HOME exist,will be cover with new value,pls check!! ===
echo.
echo === set environment(. in the end): classPath=%%JAVA_HOME%%\lib\tools.jar;%%JAVA_HOME%%\lib\dt.jar;.
echo === Warning: if classPath exist,will be cover with new value,pls check!! ===
echo.
echo === set environment: JAVA_PATH=%%JAVA_HOME%%\bin
echo.
echo.
echo === set environment: ANDROID_HOME=%androidhome%
echo === Warning: if ANDROID_HOME exist,will be cover with new value,pls check!! ===
echo.
echo === set environment: PATH=%androidpath%
echo.
set /P EN=yes/pls enter to set!
echo.
echo.
echo.
echo === new environment value JAVA_HOME=%javahome%
setx "JAVA_HOME" "%javahome%" -M
echo.
echo.
echo === new environment value classPath=%%JAVA_HOME%%\lib\tools.jar;%%JAVA_HOME%%%\lib\dt.jar;.
setx "classPath" "%%JAVA_HOME%%\lib\tools.jar;%%JAVA_HOME%%%\lib\dt.jar;." -m
echo.
echo.
echo.
echo.
echo === new environment value ANDROID_HOME=%androidhome%
setx "ANDROID_HOME" "%androidhome%" -M
echo.
echo.
echo === add PATH value ===
echo === add PATH value java_PATH=%%JAVA_HOME%%\bin == android_PATH=%androidpath% ===
set ENV_PATH=%PATH%
@echo ====current environment：
@echo %ENV_PATH%
echo.
set ENV_PATH=%PATH%%MY_PATH%%androidpath%
setx path "%ENV_PATH%" -m
echo.
cmd /c "java -version"
cmd /c "adb"
cmd /c "aapt"
echo.
cmd /c "cnpm install appium-doctor -g"
cmd /c "appium-doctor"
echo === please press any key to quit!
pause>null