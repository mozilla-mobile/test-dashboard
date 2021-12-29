import re


def abbreviate_test_suite_name(name_long):
    """ Given a long test suite name, sanitize it
    and return an abbreviated form """

    tmp = name_long.replace('&', ' and ')
    tmp = name_long.replace('(', ' ')
    tmp = name_long.replace(')', ' ')
    tmp = '_'.join(tmp.split()).lower()
    found = re.findall(r'_tests?_?suites?', tmp)
    if len(found) > 0:
        return tmp.split(found[0])[0]
    return tmp


if __name__ == '__main__':
    name_long = 'FxA&Sync'
    name_long = 'Full Functional  TestSuite'
    resp = abbreviate_test_suite_name(name_long)
    print(resp)
