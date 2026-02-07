@echo off
echo Starting Restaurant Analytics Backend...
set PATH=%PATH%;C:\Program Files\Eclipse Adoptium\jdk-17.0.17.10-hotspot\bin;%USERPROFILE%\Tools\apache-maven-3.9.6\bin
cd backend
mvn spring-boot:run