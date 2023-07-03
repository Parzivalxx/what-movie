import os
import unittest
import coverage


def register_cli_commands(app, db):
    @app.cli.command("test")
    def test():
        """Runs the unit tests without test coverage."""
        tests = unittest.TestLoader().discover("../tests/", pattern="test*.py")
        # tests = unittest.TestLoader().loadTestsFromName(
        #     "tests.integration.test_favourites.TestFavouritesBlueprint.test_list_favourite_success_favourites_exist"
        # )
        result = unittest.TextTestRunner(verbosity=2).run(tests)
        if result.wasSuccessful():
            return 0
        return 1

    @app.cli.command("cov")
    def cov():
        """Runs the unit tests with coverage."""
        COV = coverage.coverage(
            branch=True,
            include="../what_movie_server/*",
            omit=[
                "../what_movie_server/config.py",
                "../what_movie_server/*/__init__.py",
            ],
        )
        COV.start()
        tests = unittest.TestLoader().discover("../tests")
        result = unittest.TextTestRunner(verbosity=2).run(tests)
        if result.wasSuccessful():
            COV.stop()
            COV.save()
            print("Coverage Summary:")
            COV.report()
            basedir = os.path.abspath(os.path.dirname(__file__))
            covdir = os.path.join(basedir, "tmp\\coverage")
            COV.html_report(directory=covdir)
            print(f"HTML version: {covdir}\\index.html")
            COV.erase()
            return 0
        return 1

    @app.cli.command("create_db")
    def create_db():
        """Creates the db tables."""
        db.create_all()

    @app.cli.command("drop_db")
    def drop_db():
        """Drops the db tables."""
        db.drop_all()
