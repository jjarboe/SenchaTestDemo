import re
import sys
import os

ver_rec_re = re.compile('^ext\.version\.number=(\d+)\.(\d+)\.(\d+)\.(\d+)')
ver_re = re.compile('(\d+)\.(\d+)\.(\d+)\.(\d+)')

def get_opts():
    expected = None
    basedir = None
    errors = False
    try:
        expected = sys.argv[1]
        basedir = sys.argv[2]
    except IndexError:
        errors = True

    if not expected or not ver_re.match(expected):
        sys.stderr.write('Must specify minimum version (x.x.x.x)\n')
        errors = True
    if not basedir:
        sys.stderr.write('Must specify base workspace directory\n')
        errors = True
    if errors:
        sys.exit(1)

    return expected, basedir

def need_to_upgrade(expected_str, basedir):
    v = tuple(map(int, ver_re.match(expected_str).groups()))
    expected = '%04d%04d%04d%06d' % v

    try:
      with open(os.path.join(basedir,'version.properties'), 'r') as f:
        for l in f:
            m = ver_rec_re.match(l)
            if m:
               ver = '%04d%04d%04d%06d' % tuple(map(int, m.groups()))
    except (IOError,AttributeError):
      return True

    return ver < expected

def install_ext(expected, basedir):
    source = '/opt/ext'
    if need_to_upgrade(expected, source):
        source = '/opt/ext-'+expected
        if need_to_upgrade(expected, source):
            raise Exception("Couldn't find suitable Ext JS version")

    print 'Installing ExtJS from %s to %s' % (source, basedir)
    copy_cmd = '[ -e "%s" -o -h "%s" ] && mv "%s" "%s.old"' % (basedir, basedir, basedir, basedir)
    os.system(copy_cmd)
    copy_cmd = 'cp -rp "%s/" "%s"' % (source, basedir)
    os.system(copy_cmd)
    return True

if __name__ == '__main__':
    expected, basedir = get_opts()

    if need_to_upgrade(expected, basedir):
       install_ext(expected, basedir)
    else:
       print 'Appropriate version of Ext JS is installed'
