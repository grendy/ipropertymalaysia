# ipropertymalaysia
Crawling ipropertymalaysia using scrapy and send json to kafka
##Install scrapy on centos
sudo rpm -Uvh http://dl.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-5.noarch.rpm </br>
yum update -y </br>
yum install python-pip -y </br>
yum install python-devel -y </br>
yum install gcc gcc-devel -y </br>
yum install libxml2 libxml2-devel -y </br>
yum install libxslt libxslt-devel -y </br>
yum install openssl openssl-devel -y </br>
yum install libffi libffi-devel -y </br>
CFLAGS="-O0" pip install lxml </br>
pip install scrapy </br>

##Install selenium
pip install selenium
##Install xvfb and PyVirtualDisplay for running browser on background process
yum install xorg-x11-server-Xvfb </br>
pip install PyVirtualDisplay </br>
##Browser version
Firefox browser version must 45.xx 

##Running browser on background process
display = Display(visible=0, size=(800,600)) </br>
display.start() </br>
driver = webdriver.Firefox() </br>
