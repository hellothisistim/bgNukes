

cmd = "nuke -ix testScene.nk"

cmd = " ".join([nuke.env['ExecutablePath'], flags, '-F', '"' + instRange + '"', nuke.value("root.name"), '&>', logFile])
print ">>> starting instance %d" % (i, )
print "command: " + cmd
subprocess.Popen(cmd, shell=True)
    
