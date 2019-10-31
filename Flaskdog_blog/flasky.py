from app import create_app
app = create_app()

# 不知为何无用目前
# @app.cli.command()
# def test():
#     import unittest
#     tests = unittest.TestLoader().discover('tests')
#     unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    app.run()
