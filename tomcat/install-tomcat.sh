sudo apt-get -qq install default-jdk
sudo apt-get -qq install unzip
sudo wget https://dlcdn.apache.org/tomcat/tomcat-8/v8.5.75/bin/apache-tomcat-8.5.75.zip
sudo unzip apache-tomcat-*.zip
sudo chmod 755 -R ./apache-tomcat-8.5.75/
sudo ./startup.sh
