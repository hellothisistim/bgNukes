#
# bgNukes.py
#
# v1.4
#
# Tim BOWMAN [puffy@netherlogic.com]
#
# A script for launching single-core command-line Nuke renderers 
# in the background from inside the Nuke UI.
# 
# Saves log files of each render instance's output to the same folder
# where the Nuke script lives. 
#
# Thanks go to Nathan Dunsworth. His localRender.py was (and continues 
# to be) an excellent reference.
#
# Edited by Ryan O'Phelan for Windows compatability
#
# Refactor by Thomas Mansencal.

# From Python
import os
import platform
import subprocess

# From Nuke
import nuke

class UserInputError( Exception ):
    '''
    This Class Is Used For User Input Errors.
    '''

    def __init__( self, value ) :
        '''
        This Method Initializes The Class.

        @param value: Error Value Or Message. ( String )
        '''

        self.value = value

    def __str__( self ) :
        '''
        This Method Returns The Exception Representation.
        
        @return: Exception Representation. ( String )
        '''

        return self.value

def launch_nukes_panel_ui( settings = { "nodes" : "", "start" : 1, "end" : 10, "instances" : 1 } ):
    '''
    Launch Nukes Ui panel definition.
    
    @param settings: Panel UI Settings. ( Dictionary )
    '''

    panel = nuke.Panel( "BG Render - Launch Process" )
    panel.addSingleLineInput( "Frames to execute :", "%s-%s" % ( str( settings["start"] ), str( settings["end"] ) ) )
    panel.addSingleLineInput( "Node(s) to execute :", settings["nodes"] )
    panel.addSingleLineInput( "Number of background process :", settings["instances"] )
    panel.addButton( "Cancel" )
    panel.addButton( "OK" )

    return panel, panel.show()

def process_launch_nukes_panel_values( panel ):
    '''
    Process Launch Nukes Ui panel values.
	
	@param panel: Panel. ( Panel )
    '''

    framerange = panel.value( "Frames to execute :" )
    nodes = panel.value( "Node(s) to execute :" ).replace( " ", "" )
    instances = panel.value( "Number of background process :" )

    if not framerange :
        nuke.message( "%s : No Frames Range defined, aborting !" % __name__ )
        raise UserInputError, "Input Error : 'framerange' Value : '%s'." % framerange

    if not instances :
        nuke.message( "%s : No Process count defined, aborting !" % __name__ )
        raise UserInputError, "Input Error : 'instances' Value : '%s'." % instances

    nodes = nodes.replace( " ", "" )
    instances = int( instances )

    return framerange, nodes, instances

def launch_nukes( nodes = None ):
    '''
    Launch single-core command-line Nuke renderers from inside the Nuke UI.
	
	@param nodes: Nodes. ( List )
    '''

    if not nuke.root().knob( "name" ).value():
        nuke.message( "%s : Script is not saved, aborting !" % __name__ )
        return

    nodes = nodes and ",".join( [node.name() for node in nodes if node.Class() == "Write"] ) or ""

    ui_settings = {}
    ui_settings["nodes"] = nodes
    ui_settings["start"] = int( nuke.knob( "first_frame" ) )
    ui_settings["end"] = int( nuke.knob( "last_frame" ) )
    ui_settings["instances"] = nuke.env["numCPUs"]

    panel, value = launch_nukes_panel_ui( ui_settings )

    if not value :
        return

    framerange, nodes, instances = process_launch_nukes_panel_values( panel )

    nkRange = nuke.FrameRanges()
    nkRange.add( framerange )
    nkRange.compact()
    frames = nkRange.toFrameList()

    instancesframes = [[] for i in range( instances )]
    count = 0
    for frame in frames:
        instancesframes[count].append( str( frame ) )
        count += 1
        if count == instances : count = 0

    print( "%s : Launching : '%s' Nuke instances !" % ( __name__, instances ) )

    scriptpath, scriptname = os.path.split( nuke.value( "root.name" ) )
    flags = "-ixm 1"
    if nodes : flags += " -X %s" % nodes

    logFiles = []
    for i in range( instances ):
        instancerange = " ".join( instancesframes[i] )

        print( "%s : Frames for Nuke instance '%s' : '%s'." % ( __name__, i, instancerange ) )

        logFile = os.path.join( scriptpath, "%s_logging_%02d.log" % ( scriptname, i ) )
        logFiles.append( logFile )
        if platform.system() == "Windows" or platform.system() == "Microsoft":
            redirection = ">"
        else :
            redirection = "&>"
        command = " ".join( [nuke.env["ExecutablePath"], flags, "-F", "\"%s\"" % instancerange, nuke.value( "root.name" ), redirection, logFile] )
        print( "%s : Starting Nuke instance : '%d'." % ( __name__, i ) )
        print( "%s : Launch command : '%s'." % ( __name__, command ) )
        subprocess.Popen( command, shell = True )

    nuke.message( "%s : '%s' Nuke renderers launched in the background.\nLogging files : '%s'" % ( __name__, instances, ",".join( logFiles ) ) )

# Add BG Render to the Render menu.
nkmenu = nuke.menu( "Nuke" )
rendermenu = nkmenu.findItem( "Render" )
if not rendermenu.findItem( "BG Render" ):
    rendermenu.addCommand( "-", "" )
    rendermenu.addCommand( "BG Render", "bgNukes.launch_nukes(nuke.selectedNodes())" )
