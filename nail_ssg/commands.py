import sys
import click


@click.group(chain=True)
@click.pass_context
def cli1(ctx):
    print(ctx)


@cli1.command('prepare')
@click.argument('directory', default='pages', type=str)
def prepare(directory=None):
    """prepare"""
    print('prepare', directory)
    pass


@click.group(chain=True)
@click.pass_context
def cli2(ctx):
    print(ctx)


@cli1.command('build')
@click.argument('configfile', default='.config.yml', type=str)
def build(configfile=None):
    """build"""
    print('build', configfile)
    pass

cli = click.CommandCollection(sources=[cli1, cli2])


def run(argv=None):
    argv = argv or sys.argv[:]
    cli()
