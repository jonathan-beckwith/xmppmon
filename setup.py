from setuptools import setup, find_packages

setup(
    name='XmppMonitor',
    version='2.0.0b33',
    entry_points={
    	'console_scripts': [
    		'xmpp_monitor=xmpp_monitor.command_line:main'
    	]
    },
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
    	"Flask==0.10.1",
		"Flask-RESTful==0.3.1",
        "flask-admin==1.4.0",
		"Jinja2==2.7.3",
		"MarkupSafe==0.23",
		"Werkzeug==0.10.1",
		"itsdangerous==0.24",
		"peewee==2.8.0",
		"pytz==2014.10",
		"six==1.9.0",
        "python-dateutil",
        "pytz",
        "wtf-peewee==0.2.6",
        "sleekxmpp==1.3.1"
    ],
)
