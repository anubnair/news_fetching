import subprocess
import shlex


def execute_shell(cmd):
    """
    Execute the given cmd in shell
    """
    try:
        cmd = shlex.split(cmd)
        print ("going to execute %s" % cmd)

        p = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        print out
        return (out, err)
    except Exception as e:
        print str(e)
        return None
