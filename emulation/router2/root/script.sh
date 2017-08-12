rm -rf igmp/
cp -rf /hosthome/Desktop/igmp/ .
cd igmp
pip-3.2 install -r requirements.txt

python3 Run.py -stop
python3 Run.py -start
python3 Run.py -ai eth0
