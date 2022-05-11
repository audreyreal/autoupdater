# python-autoupdater

simple-ish python project to check github for new releases of a project

## rough documentation on intended usage pattern

1. Call ``get_latest_release(author, repo)`` to grab and parse the latest release json endpoint from the github API
1. Call ``check_for_update(data, current_version)`` (data being the object returned from get_latest_release, current_version being the version of the software you're running) which will return a bool, True if there's an update available, False if there isn't
1. If ``check_for_update`` returns False, carry on with the rest of your code as normal.
1. If ``check_for_update`` returns True, call ``get_release_urls(data)``, which will return a dictionary of the version releases corresponding to their respective OS's, ("windows", "mac", "linux")
1. If user approves, run ``download_release(releases)``, releases being the dict you got from the previous function, which will download the latest release corresponding to the user's operating system.
