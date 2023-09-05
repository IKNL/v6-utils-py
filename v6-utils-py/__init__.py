""" methods.py

This file contains all algorithm pieces that are executed on the nodes.
It is important to note that the master method is also triggered on a
node just the same as any other method.

When a return statement is reached the result is send to the central
server after encryption by the node.
"""
import os
import datetime

from pathlib import Path

from vantage6.tools.util import info, warn


def RPC_fetch_static_file(_, filename: str = None):
    """ Fetch a static file from the data station

    This method allows to fetch a static file from a data station. The node
    needs to be configured to set the environment variable STATIC_FILE within
    the node container. This can be done by adding the following keys to the
    configuration file of the node:

    ```yaml
    application:
        algorithm_env:
            STATIC_FOLDER: /mnt/data/some/other/folder
            STATIC_FILENAME: filename.txt
    ```

    Note that this file needs to be located in the _data folder from the node
    docker volume (on Linux this is accesable directly from the host system in
    `/var/lib/docker/volumes/vantage6-<NODE_NAME>-<SYSTEM_OR_USER>-vol/_data`).

    The node mounts this path at `/mnt/data`, so you *always* start with
    /mnt/data (!)

    The node can configure a filename, but the user can overwrite this by
    supplying the `filename` as an argument.

    For security reasons it is not possible to transfer database files using this
    algorithm.

    """

    info("Reading environment variable: STATIC_FOLDER")
    folder = os.environ.get('STATIC_FOLDER', '/mnt/data')
    info(f'Using {folder} to search for the file...')

    # check that the request is not a database file
    env_labels = dict(os.environ)
    db_filenames = [os.path.basename(value)
                for label, value in env_labels.items() 
                if '_DATABASE_URI' in label]

    if filename in db_filenames:
        info('Database file requested by user. This is not permitted!')
        return {'msg': 'It is not allowed to transfer a database file...'}

    # when the user did not provide a filename
    if not filename:
        info("No filename provided by the user. Looking for an environment "
             "variable!")
        filename = os.environ.get('STATIC_FILENAME')
        if not filename:
            warn('Filename is missing!')
            return {'msg': 'Either the node or you should specify a filename!'}

    # check that the file exists
    info(f"Locating static file: {filename}")
    file_ = Path(folder) / filename
    if not file_.exists():
        warn(f'Static file is not found in the expected location {file_}')
        return {'msg': f'Static file {file_} could not be found'}

    # read and return the file
    info('Reading static file')
    try:
        with open(file_, 'rb') as f:
            contents = f.read()
    except Exception as e:
        warn(f'Could not read static file {file_}!')
        return {'msg': f'failed to read static file {file_}! {e}'}

    info('Writing contents to output file')
    return contents


def RPC_list_static_files(_, extension: list = None):
    """ List all static files on the data station

    This method returns a dictionary with the filenames and modification 
    timestamps of all static files in the /mnt/data folder on the node.

    To only list files with a specific extension use the argument `extension`,
    e.g. extension = ['.txt'] or extension = ['.txt', '.pdf']

    """

    info("Reading environment variable: STATIC_FOLDER")
    folder = os.environ.get('STATIC_FOLDER', '/mnt/data')

    info(f"Listing static files in: {folder}")
    all_files = os.listdir(folder)

    if extension: all_files = [file for file in all_files if file.endswith(tuple(extension))]
        
    files = dict()
    for file in all_files:

        path = os.path.join(folder, file)

        # Cross-platform way to get file modification time in Python. 
        # Returns the Unix timestamp of when the file was last modified.
        c_time = os.path.getmtime(path) 
        dt_c = datetime.datetime.fromtimestamp(c_time)

        files[file] = dt_c.strftime("%Y-%m-%d, %H:%M:%S")
            
    info(f"Listed {len(files)} files")
    files = dict(sorted(files.items()))
    return files