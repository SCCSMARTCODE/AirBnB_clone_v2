#!/usr/bin/python3
from fabric import task
from datetime import datetime
import os


@task
def do_pack(c):
    """Create a .tgz archive from the contents of web_static folder"""
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    archive_filename = "web_static_{}.tgz".format(timestamp)
    archive_folder = "versions"

    if not os.path.exists(archive_folder):
        os.makedirs(archive_folder)

    archive_path = os.path.join(archive_folder, archive_filename)
    command = "tar -czvf {} web_static".format(archive_path)
    result = c.local(command)

    if result.failed:
        return None

    return archive_path


@task
def deploy(c):
    """Deploy the web_static archive"""
    archive_path = do_pack(c)
    if not archive_path:
        print("Archive creation failed.")
        return

    # Your deployment logic goes here
    # For example, you can use fabric's put() function to upload the archive to a remote server
    # and extract it to the desired location on the server
    # You can also perform any necessary setup or configuration tasks

    print("Deployment completed successfully.")


# Entry point for running the task
def main(c):
    deploy(c)


# Task runner
if __name__ == "__main__":
    task_runner = task(main)
    task_runner()
