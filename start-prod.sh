export PYTHONPATH=`pwd`/src:$PYTHONPATH
python3 app.py > stdout.log 2>&1 &
echo $! > .pid
