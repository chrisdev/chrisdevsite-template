WORKON_HOME='%(virtualenvs)s'
PROJECT_ROOT='%(sites)s/%(project)s'

# activate virtual environment
. $WORKON_HOME/%(project)s/bin/activate

cd $PROJECT_ROOT
python manage.py update_index >> $PROJECT_ROOT/logs/cron_notices.log 2>&1
