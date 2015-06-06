from hitchserve import ServiceBundle, Interactive, HitchTraceback
from os import path, system, chdir
import hitchenvironment
import hitchpostgres
import hitchselenium
import hitchdjango
import hitchcelery
import hitchredis
import hitchsmtp
import hitchcron
import subprocess
import unittest
import datetime
import sys

# Get directory above this file
PROJECT_DIRECTORY = path.abspath(path.join(path.dirname(__file__), '..'))

class DjangoReminderTestExecutionEngine(unittest.TestCase):
    """Engine for orchestating and interacting with the reminders app."""
    test_vars = {}
    preconditions = {}

    def setUp(self):
        """Ensure virtualenv present, then run all services."""
        chdir(PROJECT_DIRECTORY)
        if not path.exists(path.join(PROJECT_DIRECTORY, "venv")):
            subprocess.call(["virtualenv", "venv", "--no-site-packages"])
            subprocess.call(["./venv/bin/pip", "install", "-U", "pip",])
        subprocess.call(["./venv/bin/pip", "install", "-r", "requirements.txt"])

        environment = hitchenvironment.Environment(
            self.test_vars["platform"],
            self.test_vars["systembits"],
            self.test_vars["requires_internet"]
        )

        self.services = ServiceBundle(
            project_directory=PROJECT_DIRECTORY,
            environment=environment,
            startup_timeout=float(self.test_vars["startup_timeout"]),
            shutdown_timeout=5.0,
        )

        # Postgres user called remindme with password 'password' required - see Django's settings.py
        postgres_user = hitchpostgres.PostgresUser("remindme", "password")

        self.services['Postgres'] = hitchpostgres.PostgresService(
            version=self.test_vars.get("postgres_version"),
            postgres_installation=hitchpostgres.PostgresInstallation(
                bin_directory = self.test_vars.get("postgres_folder")
            ),
            users=[postgres_user, ],
            databases=[hitchpostgres.PostgresDatabase("remindme", postgres_user), ]
        )

        self.services['HitchSMTP'] = hitchsmtp.HitchSMTPService()

        self.services['Redis'] = hitchredis.RedisService(
            version=self.test_vars.get("redis_version"),
            port=16379,
        )

        self.services['Django'] = hitchdjango.DjangoService(
            python="{}/venv/bin/python".format(PROJECT_DIRECTORY),
            version=str(self.test_vars.get("django_version")),
            settings="remindme.settings",
            needs=[self.services['Postgres'], ]
        )

        self.services['Celery'] = hitchcelery.CeleryService(
            python="{}/venv/bin/python".format(PROJECT_DIRECTORY),
            version=self.test_vars.get("celery_version"),
            app="remindme", loglevel="INFO",
            needs=[
                self.services['Redis'], self.services['Postgres'],
            ]
        )

        self.services['Firefox'] = hitchselenium.SeleniumService(xvfb=self.test_vars.get("xvfb", False))

        self.services['Cron'] = hitchcron.CronService(
            run=self.services['Django'].manage("trigger").command,
            every=1,
            needs=[ self.services['Django'], self.services['Celery'], ],
        )

        self.services.startup(interactive=False)

        # Convenience functions
        self.driver = self.services['Firefox'].driver
        self.driver.implicitly_wait(5.0)
        self.driver.accept_next_alert = True
        self.log = self.services.log
        self.warn = self.services.warn
        self.pause = self.services.pause

    def load_website(self):
        self.driver.get(self.services['Django'].url())

    def click(self, on):
        """Click on HTML id."""
        self.driver.find_element_by_id(on.replace(" ", "-").lower()).click()

    def fill_form(self, **kwargs):
        """Convert keyword args into HTML ids and type in them with the value."""
        for element, text in kwargs.items():
            self.driver.find_element_by_id("id_{}".format(element.lower())).send_keys(text)
        self.driver.find_element_by_css_selector("button[type=\"submit\"]").click()

    def create_reminder(self, description="", days_from_now=""):
        reminder_date_and_time = datetime.datetime.now() + datetime.timedelta(days=int(days_from_now))
        self.driver.find_element_by_id("id_description").send_keys(description)
        self.driver.find_element_by_id("id_date_and_time").send_keys(
            reminder_date_and_time.strftime("%m/%d/%Y %H:%M")
        )
        self.driver.find_element_by_css_selector("""input[type=\"submit\"]""").click()

    def confirm_emails_sent(self, number):
        self.assertEquals(len(self.services['HitchSMTP'].logs.json()), int(number))

    def wait_for_email(self, containing=None):
        self.services['HitchSMTP'].logs.out.tail.until_json(
            lambda email: containing in email['payload'] or containing in email['subject'],
            timeout=15,
            lines_back=1,
        )

    def time_travel(self, days=""):
        """Get in the Delorean, Marty!"""
        self.services.time_travel(days=int(days))

    def tearDown(self):
        """We're done here..."""
        if sys.exc_info() != (None, None, None):
            #system("notify-send -i 'notification-power-disconnected' {} FAILURE".format(sys.argv[0]))
            #system("kaching fail")                     # play a sad sound (sudo pip/pipsi install kaching first)
            if self.test_vars.get("pause_on_failure", False):
                self.pause()
        else:
            #system("notify-send -i 'notification-display-brightness-full' {} PASSED".format(sys.argv[0]))
            #subprocess.call(["kaching", "pass"])       # play a happy sound (sudo pip/pipsi install kaching first)
            if self.test_vars.get("pause_on_success", False):
                self.pause()

        # Commit genocide on the services required to run your test
        self.services.shutdown()
