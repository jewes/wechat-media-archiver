export PYTHONPATH=`pwd`/src:$PYTHONPATH
nohup python3 app.py > stdout.log 2>&1 &
echo $$ > .pid
