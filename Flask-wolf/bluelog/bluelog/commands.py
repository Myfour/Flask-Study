import click
from bluelog.extensions import db
from bluelog.fakes import fake_admin, fake_categories, fake_comments, fake_posts


def register_commands(app):
    @app.cli.command()
    @click.option('--category',
                  default=10,
                  help='Quantity of categories, default is 10.')
    @click.option('--post',
                  default=50,
                  help='Quantity of posts, default is 50.')
    @click.option('--comment',
                  default=500,
                  help='Quantity of comments, default is 500.')
    def forge(category, post, comment):
        '''Generate the fake data'''

        db.drop_all()
        db.create_all()

        click.echo('Generating the administrator...')
        fake_admin()
        click.echo(f'Generating {category} categories...')
        fake_categories(category)
        click.echo(f'Generating {post} post...')
        fake_posts(post)
        click.echo(f'Generating {comment} comments...')
        fake_comments(comment)

        click.echo('Done...')