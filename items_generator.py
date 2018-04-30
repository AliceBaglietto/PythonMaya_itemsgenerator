################# ITEMS POPULATOR #################
################ by Alice Baglietto #################
################# 20.03.18 VERSION #################

import maya.cmds as cmds
import random as rand
from random import randint, uniform


########## Functions Definitions ##########     
def import_files():

    #pathOfFiles = "H:/Desktop/rocks/"
    #pathOfFiles = "/Users/Alice/Desktop/rocks/"
    pathOfFiles = "/run/media/i7436074/HD_Alice/Alice/BU/ThirdYear/Major Project/Scripts/rocks/"
    fileType = "ma"
    files = cmds.getFileList( folder=pathOfFiles, filespec='*.%s' % fileType )
    if len( files ) == 0:
        cmds.warning( "No files found" )
    else:
        cmds.namespace( add = 'rocks' )
        cmds.namespace( set = 'rocks')
        for f in files:
            cmds.file( pathOfFiles + f, i=True) 

def random_translation(tx_min, tx_max, tz_min, tz_max):
    i=1
    while (i<3):
        index = str(i)
        obj = 'rocks:rock' + index
        tx_rand = rand.randint(tx_min, tx_max)
        tz_rand = rand.randint(tz_min, tz_max)
        cmds.select(obj)
        cmds.duplicate(obj) 
        cmds.move(tx_rand, rand.uniform (-1, 0.6), tz_rand)
        i += 1

def u_scale(s_min, s_max):
    u_scale = rand.uniform(s_min, s_max) #for both scale functions
   
def random_scale(s_min, s_max):
    i=1
    while (i<3):
        index = str(i)
        obj = 'rocks:rock' + index
        u_scale = rand.uniform(s_min, s_max)
        cmds.select(obj)
        cmds.scale(u_scale)
        i += 1        
        
def uniform_scale(numOfRocks, s_min, s_max, *pArgs):
    rr = 1
    while (rr < (numOfRocks*2+2 )):
        indexR = str(rr)
        obj = 'rocks:rock' + indexR
        u_scale = rand.uniform(s_min, s_max)
        cmds.select(obj)
        cmds.xform(s= (u_scale/2, u_scale/2, u_scale/2) )
        rr += 1
        
def random_rotation(rot):
    i=1
    while (i<3):
        index = str(i)
        obj = 'rocks:rock' + index
        rx_rand = rand.randint(-rot,rot)
        ry_rand = rand.randint(-rot,rot)
        rz_rand = rand.randint(-rot,rot)
        cmds.select(obj)
        cmds.rotate(rx_rand, ry_rand, rz_rand)
        i += 1

def populate(numOfRocks, tx_min, tx_max, tz_min, tz_max, s_min, s_max, rot, *pArgs):
    r = 0
    while (r < numOfRocks):
        random_translation(tx_min, tx_max, tz_min, tz_max)
        random_scale(s_min, s_max)
        random_rotation(rot)
        r += 1
        
    
# delete overlapping objects? if needed? maybe just if overlapping? but is can simulate nice rocks tbh
# delete objects in water?

########## Main ##########

##### CLEAR the scene #####
def delete_old_population():
    cmds.namespace( removeNamespace = ":rocks", deleteNamespaceContent = True)

def select_namespace():
    cmds.select( "rocks:*")
    
# GUI STUFF BEGIN
def intSliderValue( elem ):
	return cmds.intSliderGrp( elem, query = True, value = True )

def cancelProc( *pArgs ):
	cmds.deleteUI( "Rocks Populator" )

def createUI( *pArgs):
	win = "rocksPopulator"
	
	if cmds.window( win, exists = True ):
		cmds.deleteUI( win )

	cmds.window( win, title = "Objects Populator", widthHeight = (60, 200) )
	cmds.columnLayout( adjustableColumn = True, rs = 5, cal = "center" )

	cmds.radioCollection()
	
	### INPUTS ###
	cmds.button(label = "Delete old items?", command = 'delete_old_population()' )
	cmds.button(label = "Select all items", command = 'select_namespace()' )
	
	##Population parameters##
	cmds.text(label = "ITEMS PARAMETERS", w = 250 )
	cmds.text(label = "Number of items", w = 150 )
	numOfRocks =  cmds.intSliderGrp( label = "Number of items" , minValue = -500, maxValue = 500, value = 200, field = True ) #cmds.intField( value = 200 )
	
	cmds.text(label = "Translation Range in the X", w = 150 )
	tx_min = cmds.intSliderGrp( label = "Min Value" , minValue = -500, maxValue = 500, value = -250, field = True )
	tx_max = cmds.intSliderGrp( label = "Max Value" , minValue = -500, maxValue = 500, value = 250, field = True )

        cmds.text(label = "Translation Range in the Z", w = 150 )
        tz_min = cmds.intSliderGrp( label = "Min Value" , minValue = -500, maxValue = 500, value = -250, field = True )
	tz_max = cmds.intSliderGrp( label = "Max Value" , minValue = -500, maxValue = 500, value = 250, field = True )
	
	cmds.text(label = "Scale Range", w = 150 )
	s_min= cmds.floatSliderGrp( label = "Min Value" , minValue = -180, maxValue = 180, value = 0.5, field = True )
        s_max = cmds.floatSliderGrp( label = "Min Value", minValue = -180, maxValue = 180, value = 4.0, field = True )
        cmds.button(label = "Make uniform scale", command = lambda *args: uniform_scale( cmds.intSliderGrp (numOfRocks, query=True, value=True), cmds.floatSliderGrp (s_min, query=True, value=True), cmds.floatSliderGrp (s_max, query=True, value=True) ) )
        
        cmds.text(label = "Rotation Max angle", w = 150 )
        rot = cmds.intField( value = 30 )
    
        cmds.button(label = "Import original files from path below:", command = 'import_files()' )
	cmds.button(label = "Populate!", command = lambda *args: populate( cmds.intSliderGrp (numOfRocks, query=True, value=True), cmds.intSliderGrp (tx_min, query=True, value=True), cmds.intSliderGrp (tx_max, query=True, value=True), cmds.intSliderGrp (tz_min, query=True, value=True), cmds.intSliderGrp (tz_max, query=True, value=True), cmds.floatSliderGrp (s_min, query=True, value=True), cmds.floatSliderGrp (s_max, query=True, value=True), cmds.intField(rot, query=True, value=True)) )
	
	cmds.showWindow()

##### CREATE and apply functions #####  
createUI( )