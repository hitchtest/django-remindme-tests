from hitchserve import ServiceBundle, Interactive, HitchTraceback
from os import path, system, chdir
from subprocess import call, PIPE
import hitchenvironment
import hitchpostgres
import hitchselenium
import hitchdjango
import hitchcelery
import hitchredis
import hitchsmtp
import hitchcron
import unittest
import IPython
import sys

# Get directory above this file
PROJECT_DIRECTORY = path.abspath(path.join(path.dirname(__file__), '..'))

class DjangoReminderTestExecutionEngine(unittest.TestCase):
    """Engine for orchestating and interacting with the reminders app."""
    settings = {}
    preconditions = {}

    def setUp(self):
        """Ensure virtualenv present, then run all services."""
        chdir(PROJECT_DIRECTORY)
        if not path.exists(path.join(PROJECT_DIRECTORY, "venv")):
            call(["virtualenv", "venv", "--no-site-packages"])
            call(["./venv/bin/pip", "install", "-U", "pip",])
        call(["./venv/bin/pip", "install", "-r", "requirements.txt"])

        environment = hitchenvironment.Environment(
            self.settings["platform"],
            self.settings["systembits"],
            self.settings["requires_internet"]
        )

        self.services = ServiceBundle(
            project_directory=PROJECT_DIRECTORY,
            environment=environment,
            startup_timeout=float(self.settings["startup_timeout"]),
            shutdown_timeout=5.0,
            quiet=self.settings["quiet"],
        )

        # Postgres user called remindme with password 'password' required - see Django's settings.py
        postgres_user = hitchpostgres.PostgresUser("remindme", "password")

        self.services['Postgres'] = hitchpostgres.PostgresService(
            version=self.settings.get("postgres_version"),
            postgres_installation=hitchpostgres.PostgresInstallation(
                bin_directory = self.settings.get("postgres_folder")
            ),
            users=[postgres_user, ],
            databases=[hitchpostgres.PostgresDatabase("remindme", postgres_user), ]
        )

        self.services['HitchSMTP'] = hitchsmtp.HitchSMTPService()

        self.services['Redis'] = hitchredis.RedisService(
            version=self.settings.get("redis_version"),
            port=16379,
        )

        self.services['Django'] = hitchdjango.DjangoService(
            python="{}/venv/bin/python".format(PROJECT_DIRECTORY),
            version=str(self.settings.get("django_version")),
            settings="remindme.settings",
            needs=[self.services['Postgres'], ]
        )

        self.services['Celery'] = hitchcelery.CeleryService(
            python="{}/venv/bin/python".format(PROJECT_DIRECTORY),
            version=self.settings.get("celery_version"),
            app="remindme", loglevel="INFO",
            needs=[
                self.services['Redis'], self.services['Postgres'],
            ]
        )

        self.services['Firefox'] = hitchselenium.SeleniumService(xvfb=self.settings.get("xvfb", False))

        self.services['Cron'] = hitchcron.CronService(
            run=self.services['Django'].manage("trigger").command,
            every=1,
            needs=[ self.services['Django'], self.services['Celery'], ],
        )

        self.services.startup(interactive=False)

        # Configure selenium driver
        self.driver = self.services['Firefox'].driver
        self.driver.implicitly_wait(2.0)
        self.driver.accept_next_alert = True

    def pause(self):
        """Stop. IPython time."""
        if hasattr(self, 'services'):
            self.services.pause()
        else:
            IPython.embed()

    def load_website(self):
        """Navigate to website in Firefox."""
        self.driver.get(self.services['Django'].url())

    def click(self, on):
        """Click on HTML id."""
        self.driver.find_element_by_id(on).click()

    def fill_form(self, **kwargs):
        """Fill in a form with id=value."""
        for element, text in kwargs.items():
            self.driver.find_element_by_id(element).send_keys(text)

    def click_submit(self):
        """Click on a submit button if it exists."""
        self.driver.find_element_by_css_selector("button[type=\"submit\"]").click()

    def confirm_emails_sent(self, number):
        """Count number of emails sent by app."""
        self.assertEquals(len(self.services['HitchSMTP'].logs.json()), int(number))

    def wait_for_email(self, containing=None):
        """Wait for, and return email."""
        self.services['HitchSMTP'].logs.out.tail.until_json(
            lambda email: containing in email['payload'] or containing in email['subject'],
            timeout=15,
            lines_back=1,
        )

    def time_travel(self, days=""):
        """Get in the Delorean, Marty!"""
        self.services.time_travel(days=int(days))

    def on_failure(self, exception):
        """Stop and IPython."""
        if call(["which", "kaching"], stdout=PIPE) == 0:
            call(["kaching", "fail"])       # play a sad sound (sudo pip/pipsi install kaching first)
        if self.settings.get("pause_on_failure", False):
            self.pause()

    def on_success(self):
        """Ka-ching!"""
        if call(["which", "kaching"], stdout=PIPE) == 0:
            call(["kaching", "pass"])       # play a happy sound (sudo pip/pipsi install kaching first)

    def tearDown(self):
        """Commit genocide on the services required to run your test."""
        if hasattr(self, 'services'):
            self.services.shutdown()
