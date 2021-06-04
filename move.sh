mkdir ../Water

cp Water.service build.sh app.py gunicorn.conf.py to_Elsys_sensor_data.csv *.log ../Water
cp -r frontend/build ../Water

scp -i ../ChexyAIHost_key.pem -r ../Water azureuser@52.138.36.161:~
rm -rf ../Water
ssh -o ServerAliveInterval=100000000 -i ../ChexyAIHost_key.pem azureuser@52.138.36.161

# then on server: cd Water
# chmod +x build.sh app.py
# ./build.sh
# ./deploy.sh
# ./http_certification.sh
