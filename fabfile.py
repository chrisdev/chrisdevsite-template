from fabric.api import *
from fabric.contrib.files import *
import yaml
from fabric.contrib.console import confirm
from fabric.contrib.files import exists
from fabric.contrib import django
from datetime import date
import datetime
import os
import sys
import random
import cuisine
from os.path import abspath, dirname, join, split
from site import addsitedir
PROJECT_PATH = split(os.path.abspath(os.path.dirname(__file__)))[1]


@task
def production():
    """
    The production servers
    """
    CFG = yaml.load(open('_deploy.cfg'))
    env.hosts = CFG['prod_hosts']
    env.sites = CFG['sites']
    env.project = PROJECT_PATH
    env.virtualenvs = CFG['virtualenvs']
    env.directory = join(env.sites, PROJECT_PATH)
    env.python = join(env.virtualenvs, "%s-env/bin/python" % PROJECT_PATH)
    env.nginx_root = CFG['nginx_root']
    env.gunicorn = CFG['gunicorn']
    env.user = CFG['user']
    env.memcache = CFG['memcache']
    env.db_user = CFG["db_user"]
    env.db_passwd = CFG["db_passwd"]
    env.db_host = CFG["db_host"]
    env.db_name = CFG["db_name"]
    env.email_from = CFG["email_from"]
    env.email_user = CFG["email_user"]
    env.email_host = CFG["email_host"]
    env.email_password = CFG["email_password"]
    env.is_production = True
    env.site_name = CFG['production_site_name']
    env.secret_key = CFG['secret_key']
    env.akismet_api_key = CFG['akismet_api_key']


@task
def testing():
    """
    The test server
    """
    CFG = yaml.load(open('_deploy.cfg'))
    env.hosts = CFG['test_hosts']
    env.sites = CFG['sites']
    env.project = PROJECT_PATH
    env.virtualenvs = CFG['virtualenvs']
    env.directory = join(env.sites, PROJECT_PATH)
    env.python = join(env.virtualenvs, "%s-env/bin/python" % PROJECT_PATH)
    env.nginx_root = CFG['nginx_root']
    env.gunicorn = CFG['gunicorn']
    env.user = CFG['user']
    env.memcache = CFG['memcache']
    env.db_user = CFG["db_user"]
    env.db_passwd = CFG["db_passwd"]
    env.db_host = CFG["db_host"]
    env.db_name = CFG["db_name_test"]
    env.email_from = CFG["email_from"]
    env.email_user = CFG["email_user"]
    env.email_host = CFG["email_host"]
    env.email_password = CFG["email_password"]
    env.is_production = False
    env.site_name = CFG['testing_site_name']
    env.secret_key = CFG['secret_key']
    env.akismet_api_key = CFG['akismet_api_key']

####################### Utilities & Settings ###########################
@task
def utils_encrypt_cfg():
    """
    Encrypt the file that stores your secerets
    Do not check this into scouce control
    """

    cfg = prompt('cfg file', default='_deploy.cfg')
    local(
        "openssl cast5-cbc -e -in {f} -out {f}.cast5 && chmod 600 {f}".format(
            f=cfg
        )
    )

@task
def utils_decrypt_cfg():
    """
    Decrypt the file that stores your secerets
    You can check this into source control
    """
    puts("Contact cclarke@chrisdev.com for the password.")
    cfg = prompt('cfg file', default='_deploy.cfg')
    local(
        "openssl cast5-cbc -d -in {f}.cast5 -out {f} && chmod 600 {f}".format(
            f=cfg
        )
    )

@task
def utils_fix_hook():
    """
    Fix permissions on the hook.log
    """
    with cd(env.directory):
        with cuisine.mode_sudo():
            cuisine.file_attribs('{}/hook.log'.format(env.virtualenvs),
                                 owner=env.user,
                                 group=env.user)

@task
def utils_generate_key():
    """
    Generate the key
    """
    chars = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPURSTUV"
    print("".join([random.choice(chars) for i in xrange(41)]))

@task
def utils_ssl_cert_install():
    """
    Create the ssl directory, upload the certs and create a combined cert
    """
    source_dir =  prompt('ssl key file directory')
    dest_dir = '/svr/ssl'
    source_file_list = local('ls {}'.format(source_dir), capture=True).split('\n')

    cmd_crt_comb = 'cat {}/hiv.opm.gov.tt.crt {}/geo_trust_intermediate.crt > {}/hiv.opm.gov.tt.comb.crt'
    with cuisine.mode_sudo():

        cuisine.dir_ensure('/svr/ssl/', recursive=True)
        cuisine.dir_attribs(dest_dir, mode="0400")
        for fl in source_file_list:
            cuisine.file_upload(dest_dir, '{}/{}'.format(source_dir, fl))
            cuisine.file_attribs('{}/{}'.format(dest_dir, fl), mode="0400")

        sudo(cmd_crt_comb.format(dest_dir, dest_dir, dest_dir))


@task
def utils_media_sync_local():
    """
    Rsync the media from the remote to local project dir
    """
    source = prompt('Server name', default=env.host)
    remote_dir = "{}/{}/site_media".format(env.sites, env.project)
    local("cd site_media && rsync -avp -e ssh {}@{}:{}/media .".format(
            env.user,
            source,
            remote_dir)
     )

@task
def utils_media_sync(source):
    """
    Rsync the media from source to target
    """
    source = prompt('Server name', default=env.host)
    media_dir = "{}/{}/site_media".format(env.sites, env.project)
    with settings(warn_only=True):
        with cd(media_dir):
            run(
                'rsync -avp -e ssh {}@{}:{}/media .'.format(env.user,
                                                            source,
                                                            media_dir)
            )


@task
def utils_hosting_dirs():
    """
    Adds the sites dir require for hosting
    """
    with cuisine.mode_sudo():
        cuisine.dir_ensure(
            '/usr/local/sites/',
            owner='django',
            group='django'
    )
###################### Operations dealing with the Database ##########
@task
def db_dump():
    """
    Perform a backup of the database to the ~user_name/dump_db directory
    """
    location =join("/home",env.user, "dump_db")
    cuisine.dir_ensure(location)
    ts = datetime.datetime.now().strftime('%s')
    dump_path = "{}/{}-{}.bak".format(location, env.db_name, ts)
    with shell_env(PGPASSWORD=env.db_passwd):
        run("pg_dump -U {user} -h {host} -Ox -Fc -Z 9 -f {dump_path} {db_name}".format(
                  user=env.db_user,
                  host=env.db_host,
                  dump_path=dump_path,
                  db_name=env.db_name
             )
         )


@task
def db_get_latest_dump():
    """
    Download the tatest dump form ~user_name/dump_db  to local machine
    """
    location =join("/home",env.user, "dump_db")
    out = run('ls -t {}/{}-*.bak'.format(location,env.db_name))
    latest_dump = out.split()[0]

    get(join(location,latest_dump), "db_dumps")


@task
def db_create():
    with shell_env(PGPASSWORD=env.db_passwd):
        run("createdb -U {user} -h {host} {db_name}".format(
                  user=env.db_user,
                  host=env.db_host,
                  db_name=env.db_name
             )
        )

@task
def db_drop():
    with shell_env(PGPASSWORD=env.db_passwd):
        run("dropdb -U {user} -h {host} {db_name}".format(
                  user=env.db_user,
                  host=env.db_host,
                  db_name=env.db_name
             )
        )

############## Virtual Enviromnent Operations ##########################
@task
def virtualenv_create():
    """
    Create the virtualenv_cmd for the project
    """
    with settings(warn_only=True):
        if run("test -d %s%s-env" % (env.virtualenvs, env.project)).failed:
            run('mkvirtualenv {}-env '.format(
                    env.project
                )
            )
@task
def virtualenv_add2():
    """
    Adds the project directory project dir to the sys.path
    """
    virtualenv_cmd('add2virtualenv {}'.format(
            join(env.sites,env.project)
        )
    )
@task
def virtualenv_cmd(command):
    """
    Enable the virtualenv_cmd and a run command
    """
    with cd(env.directory):
        run('source %s%s-env/bin/activate && %s' % (env.virtualenvs,
            env.project, command))


###################### Deployment Operations  ##########################

@task
def deploy_supervisor():
    """
    Upload and configure the supervisord template
    Store the ngix settings in _deploy.cfg
    """
    destination = "/etc/supervisor/conf.d/%s.conf" % env.project
    upload_template('deploy/supervisor.conf', destination, context=env,
        use_sudo=True)
    sudo('{cmd} reread && {cmd} add {site} && {cmd} start {site}'.format(
            cmd="supervisorctl", site=PROJECT_PATH)
    )

@task
def deploy_gunicorn():
    """
     Upload and configure the gunicorn template
     Store the gunicorn ip_address:port in _deploy.cfg
    """
    destination = join(env.directory, "gunicorn.conf")
    upload_template('deploy/gunicorn.conf', destination, context=env)


@task
def deploy_scripts():
    """
    Upload update_index and setup a cron job
    """
    script_dir= join(env.directory,"scripts")
    cuisine.dir_ensure(script_dir)
    upload_template('deploy/update_index.sh', script_dir, context=env)


@task
def deploy_nginx():
    """
    Upload and configure the  nginx template
    Store the nginx settings in _deploy.cfg
    """

    if not env.is_production:

        upload_template('deploy/nginx.conf',
                        join(env.nginx_root, env.project),
                        context=env, use_sudo=True)
    else:
        upload_template('deploy/nginx_prod.conf',
                        join(env.nginx_root, env.project),
                        context=env, use_sudo=True)





@task
def deploy_conf_files():
    """
    Upload and configure config templates for local_settings,
    nginx.conf,supervisord.conf and gunicorn.py
    """
    deploy_gunicorn()
    deploy_supervisor()
    deploy_enable_nginx()

#######################################################################
################### Requirement management ###############



@task
def requirements_install():
    """
    Install new requirements if any
    """
    virtualenv_cmd('pip install -r {}/requirements/production.txt'.format(
             join(env.sites,env.project)
            )
        )


@task
def requirements_uninstall_package():
    """
    Uninstall a package
    """
    source = prompt('package_name')
    virtualenv_cmd('pip uninstall {}'.format(package))



##########################Source Control################################
@task
def src_clone_project():

    with settings(warn_only=True):
        with cd(env.sites):
            if run("test -d %s/%s" % (env.sites, env.project)).failed:
                run('hg clone ssh://hg@bitbucket.org/chrisdev/%s' % env.project)



@task
def src_pull_update():
    """
    Hg pull and update
    """
    with cd(env.directory):
        run('hg pull')
        run('hg update')


#######################################################################
####################Nginx, Gunicorn & Supervisor#######################


@task
def site_nginx_enable():
    """
    Create the symbolic link in the nginx sites-enabled directory to the
    nginx config for the site
    """
    with cd('/etc/nginx/sites-enabled/'):
        with settings(warn_only=True):
            sudo('ln -s /etc/nginx/sites-available/%s %s' % (env.project,
                env.project))
    sudo('/etc/init.d/nginx configtest')


@task
def site_nginx_reload():
    """
    Reload the nginx server.
    Once the site is up and running you should not have  to use this
    """
    sudo("/etc/init.d/nginx reload")


@task
def site_gunicorn_reload():
    """
    Reload the gunicorn.
    """
    with settings(warn_only=True):
        sudo("sudo supervisorctl restart %s" % PROJECT_PATH)


@task
def site_maint_mode():
    """
    Put the site in maintenence mode
    """
    with settings(warn_only=True):
        with cd('%s/site_media/static' % env.directory):
            run('touch maint.html')

@task
def site_debug():
    """
    Put the site in debug mode
    """
    with cd(join(env.directory, env.project, 'settings')):
        sed("production.py", "^DEBUG = False$", "DEBUG = True")
    site_gunicorn_reload()


@task
def site_nodebug():
    """
    Put the site in non mode. DRBUG = False
    """
    with cd(join(env.directory, env.project, 'settings')):
        sed("production.py", "^DEBUG = True$", "DEBUG = False")
    site_gunicorn_reload()


@task
def site_production_mode():
    """
    Puts the site into production mode
    """
    gunicorn_reload()
    # with cd('%s/site_media/static' % env.directory):
    #     run('rm maint.html')

@task
def site_nginx_enable():
    """
    Create the symbolic link in the nginx sites-enabled directory to the
    nginx config for the site
    """
    with cd('/etc/nginx/sites-enabled/'):
        with settings(warn_only=True):
            sudo('ln -s /etc/nginx/sites-available/%s %s' % (env.project,
                 env.project))

    sudo('/etc/init.d/nginx configtest')

    ans = prompt('Do you wish to restart nginx [yes/no]',
                 validate=r'^(yes|no|YES|NO|y|n|Y|N)$')
    if ans.lower() == 'yes' or ans.lower() == 'y':
        sudo('/etc/init.d/nginx restart')

##############################################################################

########################### Django Mananagment ################################

@task
def manage_createsuperuser():
    """
    Create superuser.
    """
    super_user = prompt('enter superuser name')
    with shell_env(
                DJANGO_SETTINGS_MODULE='cuba_site.settings.production',
                SECRET_KEY=env.secret_key,
                DB_NAME=env.db_name,
                DB_USER=env.db_user,
                DB_PASSWD=env.db_passwd,
                DB_HOST=env.db_host,
                AKISMET_API_KEY=env.akismet_api_key,
                EMAIL_USER = env.email_user,
                EMAIL_PASSWORD = env.email_password,
                MEMCACHE_PORT=env.memcache):
        with prefix('workon cuba_site-env'):
            #run( "django-admin.py migrate filer")
            run("django-admin.py createsuperuser --username={}".format(
            super_user))

@task
def manage_migrate():
    """
    Run the south  migrate.
    """
    with shell_env(
                DJANGO_SETTINGS_MODULE='cuba_site.settings.production',
                SECRET_KEY=env.secret_key,
                DB_NAME=env.db_name,
                DB_USER=env.db_user,
                DB_PASSWD=env.db_passwd,
                DB_HOST=env.db_host,
                AKISMET_API_KEY=env.akismet_api_key,
                EMAIL_USER = env.email_user,
                EMAIL_PASSWORD = env.email_password,
                MEMCACHE_PORT=env.memcache):
        with prefix('workon cuba_site-env'):
            #run( "django-admin.py migrate filer")
            run("django-admin.py migrate --all")

@task
def manage_show_settings():
    """
    Run the south  migrate.
    """
    with shell_env(
                DJANGO_SETTINGS_MODULE='cuba_site.settings.production',
                SECRET_KEY=env.secret_key,
                DB_NAME=env.db_name,
                DB_USER=env.db_user,
                DB_PASSWD=env.db_passwd,
                DB_HOST=env.db_host,
                AKISMET_API_KEY=env.akismet_api_key,
                EMAIL_USER = env.email_user,
                EMAIL_PASSWORD = env.email_password,
                MEMCACHE_PORT=env.memcache):
        with prefix('workon cuba_site-env'):
            run( "django-admin.py diffsettings")

@task
def manage_syncdb():
    """
    Run the syncdb
    """
    with shell_env(
                DJANGO_SETTINGS_MODULE='cuba_site.settings.production',
                SECRET_KEY=env.secret_key,
                DB_NAME=env.db_name,
                DB_USER=env.db_user,
                DB_PASSWD=env.db_passwd,
                DB_HOST=env.db_host,
                AKISMET_API_KEY=env.akismet_api_key,
                EMAIL_USER=env.email_user,
                EMAIL_PASSWORD=env.email_password,
                MEMCACHE_PORT=env.memcache):
        with prefix('workon cuba_site-env'):
            run("django-admin.py syncdb")


@task
def manage_migrate_syncdb():
    #manage_migrate()
    manage_syncdb()


@task
def manage_build_static():
    """
    Copy the static files (images,css,js) to site_media
    """
    with shell_env(
                DJANGO_SETTINGS_MODULE='cuba_site.settings.production',
                SECRET_KEY=env.secret_key,
                DB_NAME=env.db_name,
                DB_USER=env.db_user,
                DB_PASSWD=env.db_passwd,
                DB_HOST=env.db_host,
                AKISMET_API_KEY=env.akismet_api_key,
                EMAIL_USER=env.email_user,
                EMAIL_PASSWORD=env.email_password,
                MEMCACHE_PORT=env.memcache):
        with prefix('workon cuba_site-env'):
            run("django-admin.py  collectstatic --noinput")


@task
def manage_update_index():
    """
    Update the haystack index
    """
    with shell_env(
                DJANGO_SETTINGS_MODULE='cuba_site.settings.production',
                SECRET_KEY=env.secret_key,
                DB_NAME=env.db_name,
                DB_USER=env.db_user,
                DB_PASSWD=env.db_passwd,
                DB_HOST=env.db_host,
                AKISMET_API_KEY=env.akismet_api_key,
                EMAIL_USER=env.email_user,
                EMAIL_PASSWORD=env.email_password,
                MEMCACHE_PORT=env.memcache):
        with prefix('workon cuba_site-env'):
            run("django-admin.py  manage.py  update_index")

task
def manage_update_index():
    """
    Update the haystack index
    """
    with shell_env(
                DJANGO_SETTINGS_MODULE='cuba_site.settings.production',
                SECRET_KEY=env.secret_key,
                DB_NAME=env.db_name,
                DB_USER=env.db_user,
                DB_PASSWD=env.db_passwd,
                DB_HOST=env.db_host,
                AKISMET_API_KEY=env.akismet_api_key,
                EMAIL_HOST_USER=env.email_user,
                EMAIL_HOST_PASSWORD=env.email_password,
                MEMCACHE_PORT=env.memcache):
        with prefix('workon cuba_site-env'):
            run("django-admin.py  manage.py  update_index")


######################## Task Collections #################################
@task
def bootstrap():
    """
    Everything need to get project running on this server
    """
    virtualenv_create()
    utils_hosting_dirs()
    src_clone_project()
    requirements_install()
    deploy_conf_files()
    migrate_syncdb()
    with settings(warn_only=True):
        with cd(env.directory):
            run('mkdir logs')
    #sudo supervisorctl reread
    #sudo supervisorctl add foundation_theme_site


@task
def update_site():
    """
    Pull and update, build static and reload gunicorn
    """
    #maint_mode()
    src_pull_update()
    requirements_install()
    manage_migrate_syncdb()
    manage_build_static()
    #production_mode()
