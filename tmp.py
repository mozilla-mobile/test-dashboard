import os


version_cached = os.environ['VERSION_NUM']

def new_version_exists(version_cached, version_actual):

    if version_actual == version_cached:
        print('same')
        return False
    else:
        print('theres a new version!')
        return True


def github_version_actual():
    return "116.0"


if __name__ == '__main__':

    version_actual  = github_version_actual()

    result = new_version_exists(version_cached, version_actual)
    print(result)

