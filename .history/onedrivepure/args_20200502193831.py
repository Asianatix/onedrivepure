import argparse
import os



# Arguments
def parse_args():

    parser = argparse.ArgumentParser()

    # Set the config file location
    parser.add_argument('-chunk',
                        default=10(*1024**2),
                        type=int,
                        help='Set the chunk size when uploading, use with -hack, must be times of 327680. Max is 62914560.')
    parser.add_argument('-workers',
                        default=10,
                        type=int,
                        help='Set the number of workers in multi-thread uploading')
    # parser.add_argument('-batchnum',
    #                     default=10,
    #                     type=int,
    #                     help='Set the number of batchnum in multi-thread uploading')
    parser.add_argument('-sharelink',
                        action='store_true',
                        default=False,
                        help='Switch the mode of upload, if is Ture the client will upload the file in sharelink'
                        '(arg\'s position used to be the local file) automatically')
    parser.add_argument('-step',
                        default=102400,
                        type=int,
                        help='Set the step size of progress bar')
    # Set the config file location
    parser.add_argument('-conf',
                        default=os.path.expanduser('~/.onedrive.json'),
                        help='Set the location of config file')

    # Whether Force hard delete or overwrite, default if False
    parser.add_argument('-force',
                        action='store_true',
                        default=False,
                        help='Force delete or overwrite when performing')

    # Whether Recursive listing folder, default if False
    parser.add_argument('-recursive',
                        action='store_true',
                        default=False,
                        help='Recursively listing folder')

    # TODO: asc when listing folder and searching. But by which field?
    parser.add_argument('-asc',
                        action='store_true',
                        default=False,
                        help='Recursively listing folder')

    # TODO: desc when listing folder and searching
    parser.add_argument('-desc',
                        action='store_true',
                        default=False,
                        help='Recursively listing folder')

    # Use downloader to download, or use multi-thread upload(highly exp)
    parser.add_argument('-hack',
                        action='store_true',
                        default=False,
                        help='')

    # Only output the download links
    parser.add_argument('-url',
                        action='store_true',
                        default=False,
                        help='Only display the download link(s), temp one')

    # Set the logging level
    parser.add_argument('-verbose',
                        action='store',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                        default='WARNING',
                        help='Set the logging level')

    # Show full path instead of short one while listing
    parser.add_argument('-fullpath',
                        action='store_true',
                        default=False,
                        help='Show full path instead of short one while listing')

    # Script actions
    # Set mutually exclusive actions
    parser.add_argument('mode',
                        choices=['init_business', 'init', 'get', 'list', 'put', 'delete', 'mkdir', 'move', 'remote',
                                 'quota', 'share', 'direct', 'search'],

    # Return the parsed content
    args, rest = parser.parse_known_args()
    args.rest = rest
    return args
