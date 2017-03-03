# ipropertymalaysia
Crawling ipropertymalaysia using scrapy and send json to kafka
##Install scrapy on centos
```bash 
sudo rpm -Uvh http://dl.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-5.noarch.rpm </br>
yum update -y 
yum install python-pip -y 
yum install python-devel -y 
yum install gcc gcc-devel -y 
yum install libxml2 libxml2-devel -y 
yum install libxslt libxslt-devel -y 
yum install openssl openssl-devel -y 
yum install libffi libffi-devel -y 
CFLAGS="-O0" pip install lxml 
pip install scrapy 
```

##Install selenium
Selenium version must 2.53.6
```bash
pip install selenium
```
##Install xvfb and PyVirtualDisplay for running browser on background process
```bash
yum install xorg-x11-server-Xvfb 
pip install PyVirtualDisplay 
```
##Browser version
Browser used is Firefox browser
```bash
Firefox browser version must 45.0.2 or 45.xx.xx 
```
##Running browser on background process
To running browser on background process, install xvfb and pyVirtualDisplay
```bash
from pyvirtualdisplay import Display
display = Display(visible=0, size=(800,600)) </br>
display.start() </br>
driver = webdriver.Firefox() </br>
```
##Connect to mysql using MySQLdb library
Must insert mysql configuration into settings.py on scrapy </br>
```bash
conn=MySQLdb.connect(  
            host=crawler.settings['MYSQL_HOST'], 
            port=crawler.settings['MYSQL_PORT'], 
            user=crawler.settings['MYSQL_USER'],
            passwd=crawler.settings['MYSQL_PASS'],
            db=crawler.settings['MYSQL_DB'])
        return cls(conn)
```
