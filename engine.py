from hitchserve import ServiceBundle
from os import path, system, chdir
from subprocess import call, check_call, PIPE
import hitchpostgres
import hitchselenium
import hitchpython
import hitchredis
import hitchtest
import hitchsmtp
import hitchcron
import hitchnode
import IPython
import sys
import os
import copy

## Get directory above this file
PROJECT_DIRECTORY = path.abspath(path.join(path.dirname(__file__), '..'))


class ExecutionEngine(hitchtest.ExecutionEngine):
    """Engine for orchestating and interacting with the reminders app."""
    def set_up(self):
        """Ensure virtualenv present, then run all services."""
        chdir(PROJECT_DIRECTORY)
        
        python_package = hitchpython.PythonPackage(
            python_version=self.preconditions['python_version']
        )
        python_package.build()

        check_call([
            python_package.pip, "install", "-r",
            path.join(PROJECT_DIRECTORY, "requirements.txt")
        ])

        postgres_package = hitchpostgres.PostgresPackage(
            version=self.settings["postgres_version"],
        )
        postgres_package.build()
        redis_package = hitchredis.RedisPackage(
            version=self.settings.get("redis_version")
        )
        redis_package.build()

        node_package = hitchnode.NodePackage()
        node_package.build()

        if not path.exists(path.join(
            hitchtest.utils.get_hitch_directory(),
            "node_modules", "less", "bin", "lessc"
        )):
            chdir(hitchtest.utils.get_hitch_directory())
            check_call([node_package.npm, "install", "less"])
            chdir(PROJECT_DIRECTORY)

        self.services = ServiceBundle(
            project_directory=PROJECT_DIRECTORY,
            startup_timeout=float(self.settings["startup_timeout"]),
            shutdown_timeout=5.0,
        )

        # Postgres user called remindme with password 'password' required - see Django's settings.py
        postgres_user = hitchpostgres.PostgresUser("remindme", "password")

        self.services['Postgres'] = hitchpostgres.PostgresService(
            postgres_package=postgres_package,
            users=[postgres_user, ],
            databases=[hitchpostgres.PostgresDatabase("remindme", postgres_user), ]
        )

        self.services['HitchSMTP'] = hitchsmtp.HitchSMTPService()

        self.services['Redis'] = hitchredis.RedisService(
            redis_package=redis_package,
            port=16379,
        )

        dj_env_vars = copy.copy(os.environ)
        dj_env_vars['PATH'] = "{}:{}:{}".format(
            dj_env_vars['PATH'],
            node_package.bin_directory,
            path.join(hitchtest.utils.get_hitch_directory(), "node_modules", "less", "bin")
        )

        self.services['Django'] = hitchpython.DjangoService(
            python=python_package.python,
            settings="remindme.settings",
            needs=[self.services['Postgres'], ],
            env_vars=dj_env_vars
        )

        self.services['Celery'] = hitchpython.CeleryService(
            python=python_package.python,
            app="remindme", loglevel="INFO",
            needs=[
                self.services['Redis'], self.services['Postgres'],
            ]
        )

        self.services['Firefox'] = hitchselenium.SeleniumService(
            xvfb=self.settings.get("xvfb", False) or self.settings.get("quiet", False),
            no_libfaketime=True,
        )

        self.services['Cron'] = hitchcron.CronService(
            run=self.services['Django'].manage("trigger").command,
            every=1,
            needs=[ self.services['Django'], self.services['Celery'], ],
        )

        self.services.startup(interactive=False)

        # Configure selenium driver
        self.driver = self.services['Firefox'].driver
        #self.driver.set_window_size(450, 350)
        #self.driver.set_window_position(0, 0)
        self.driver.implicitly_wait(2.0)
        self.driver.accept_next_alert = True

    def pause(self, message=None):
        """Stop. IPython time."""
        if hasattr(self, 'services'):
            self.services.start_interactive_mode()
        self.ipython(message)
        if hasattr(self, 'services'):
            self.services.stop_interactive_mode()

    def load_website(self):
        """Navigate to website in Firefox."""
        self.driver.get(self.services['Django'].url())

    def click(self, on):
        """Click on HTML id."""
        self.driver.execute_script("document.getElementById('{}').click();".format(on))

    def fill_form(self, **kwargs):
        """Fill in a form with id=value."""
        for element, text in kwargs.items():
            self.driver.find_element_by_id(element).send_keys(text)

    def click_submit(self):
        """Click on a submit button if it exists."""
        self.driver.find_element_by_css_selector("button[type=\"submit\"]").click()

    def confirm_emails_sent(self, number):
        """Count number of emails sent by app."""
        assert len(self.services['HitchSMTP'].logs.json()) == int(number)

    def wait_for_email(self, containing=None):
        """Wait for, and return email."""
        self.services['HitchSMTP'].logs.out.tail.until_json(
            lambda email: containing in email['payload'] or containing in email['subject'],
            timeout=45,
            lines_back=1,
        )

    def time_travel(self, days=""):
        """Get in the Delorean, Marty!"""
        self.services.time_travel(days=int(days))

    def connect_to_kernel(self, service_name):
        self.services.connect_to_ipykernel(service_name)

    def on_failure(self):
        """Stop and IPython."""
        if call(["which", "kaching"], stdout=PIPE) == 0:
            call(["kaching", "fail"])  # sudo pip install kaching for sad sound
        if self.settings.get("pause_on_failure", False):
            self.pause(message=self.stacktrace.to_template())

    def on_success(self):
        """Ka-ching!"""
        if call(["which", "kaching"], stdout=PIPE) == 0:
            call(["kaching", "pass"])  # sudo pip install kaching for happy sound
        if self.settings.get("pause_on_success", False):
            self.pause(message="SUCCESS")

    def tear_down(self):
        """Commit genocide on the services required to run your test."""
        if hasattr(self, 'services'):
            self.services.shutdown()
