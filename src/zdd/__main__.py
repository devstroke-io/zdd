import signal
import sys

import click
from colorama import Fore, Style

from .__about__ import __version__
from .services.deploy import Deploy
from .services.logger import Logger

logo = """
███████╗██████╗ ██████╗                                                    
╚══███╔╝██╔══██╗██╔══██╗                                                   
  ███╔╝ ██║  ██║██║  ██║                                                   
 ███╔╝  ██║  ██║██║  ██║                                                   
███████╗██████╔╝██████╔╝                                                   
╚══════╝╚═════╝ ╚═════╝                                                    
██████╗ ███████╗██╗   ██╗███████╗████████╗██████╗  ██████╗ ██╗  ██╗███████╗
██╔══██╗██╔════╝██║   ██║██╔════╝╚══██╔══╝██╔══██╗██╔═══██╗██║ ██╔╝██╔════╝
██║  ██║█████╗  ██║   ██║███████╗   ██║   ██████╔╝██║   ██║█████╔╝ █████╗  
██║  ██║██╔══╝  ╚██╗ ██╔╝╚════██║   ██║   ██╔══██╗██║   ██║██╔═██╗ ██╔══╝  
██████╔╝███████╗ ╚████╔╝ ███████║   ██║   ██║  ██║╚██████╔╝██║  ██╗███████╗
╚═════╝ ╚══════╝  ╚═══╝  ╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝
"""


def signal_handler(sig: int, frame: object) -> None:
    """Handler for signals captured
    :param sig: Signal identifier
    :type sig: int
    :param frame: Current stack frame
    :type frame: object
    :return: None
    :rtype: None
    """
    if sig == signal.SIGINT:
        sig_type = "SIGINT"
    elif sig == signal.SIGTERM:
        sig_type = "SIGTERM"
    else:
        sig_type = f"UNKNOWN ({sig})"
    Logger.get('main').critical(f"Process interrupted ({sig_type})")
    sys.exit(200)


@click.command(context_settings={'help_option_names': ['-h', '--help']})
@click.version_option(__version__, '-V', '--version')
@click.argument('project', type=click.STRING, required=True)
@click.argument('tag', type=click.STRING, required=False, default="latest")
@click.option('-q', '--quiet', is_flag=True, help="no output")
@click.option('-v', '--verbose', count=True, help="verbosity level")
def main(project, tag, quiet, verbose) -> None:
    """
    Deploy PROJECT with TAG (default 'latest')
    """
    print(Fore.MAGENTA + Style.BRIGHT + logo + Style.RESET_ALL)
    for sig_name in [signal.SIGINT, signal.SIGTERM]:
        signal.signal(sig_name, signal_handler)
    Logger.prepare('main', 1000 if quiet else 50 - verbose * 10)
    deploy = Deploy(project, tag)
    deploy.pull()
    deploy.reload()


if __name__ == '__main__':
    main()
