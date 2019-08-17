# -*- coding: utf-8 -*-
###################################################################################
#
#  InitGui.py
#  
#  Copyright 2018 Mark Ganson <TheMarkster> mwganson at gmail
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
###################################################################################

import asm4wb_locator
global asm4wb_icons_path, asm4wb_ex_path
asm4wbPath = os.path.dirname( asm4wb_locator.__file__ )
asm4wb_icons_path = os.path.join( asm4wbPath, 'icons')
asm4wb_ex_path = asm4wbPath #os.path.join( asm4wbPath, 'Examples')

global main_Assembly4WB_Icon
main_Assembly4WB_Icon = os.path.join( asm4wb_icons_path , 'Assembly4.svg' )
global submenu, submenu1

submenu = ['Asm4_Examples']
submenu1 = ['asm_Bielle.fcstd','asm_Cylinders.FCStd','asm_Hypnotic.fcstd','asm4-test.FCStd','README.pdf']


#def myFunc(string):
#    print (string)
#    global act
#    act.setVisible(True)

#mw=Gui.getMainWindow()
#bar=mw.menuBar()
#act=bar.addAction("MyCmd")
#mw.workbenchActivated.connect(myFunc)



"""
    +-----------------------------------------------+
    |            Initialize the workbench           |
    +-----------------------------------------------+
"""
class Assembly4_WorkBench(Workbench):
 
    global main_Assembly4WB_Icon

    MenuText = "Assembly 4"
    ToolTip = "Assembly 4 workbench"
    Icon = main_Assembly4WB_Icon

    
    def __init__(self):
        "This function is executed when FreeCAD starts"
        pass


    def Initialize(self):
        global submenu
        import newModelCmd     # creates a new App::Part container called 'Model'
        import newSketchCmd    # creates a new Sketch in 'Model'
        import newLCSCmd       # creates a new LCS in 'Model'
        import newPointCmd     # creates a new LCS in 'Model'
        import newBodyCmd      # creates a new Body in 'Model
        import insertLinkCmd   # inserts an App::Link to a 'Model' in another file
        import placeLinkCmd    # places a linked part by snapping LCS (in the Part and in the Assembly)
        import placeDatumCmd   # places an LCS relative to an external file (creates a local attached copy)
        import importDatumCmd  # creates an LCS in assembly and attaches it to an LCS relative to an external file
        self.listCmd =           [ "newModelCmd", "insertLinkCmd", "placeLinkCmd", "newLCSCmd", "importDatumCmd", "placeDatumCmd", "newSketchCmd", "newPointCmd", "newBodyCmd" ] # A list of command names created in the line above
        self.itemsMenu =         [ "newModelCmd", "insertLinkCmd", "placeLinkCmd", "newLCSCmd", "importDatumCmd", "placeDatumCmd", "newSketchCmd", "newPointCmd", "newBodyCmd" ] # A list of command names created in the line above
        self.itemsToolbar =      [ "newModelCmd", "insertLinkCmd", "placeLinkCmd", "newLCSCmd", "importDatumCmd", "placeDatumCmd", "newSketchCmd", "newPointCmd", "newBodyCmd" ] # A list of command names created in the line above
        self.itemsContextMenu =  [ "placeLinkCmd", "placeDatumCmd" ] # A list of command names created in the line above
        self.appendToolbar("Assembly 4",self.itemsToolbar) # leave settings off toolbar
        self.appendMenu("&Assembly",self.itemsMenu) # creates a new menu
        #self.appendMenu(["&Edit","DynamicData"],self.list) # appends a submenu to an existing menu
        #submenu = ['Asm4_Examples']
        #submenu1 = ['asm_Bielle.fcstd','asm_Cylinders.FCStd','asm_Hypnotic.fcstd','asm4-test.FCStd','README.pdf']
        self.appendMenu(["&Assembly", submenu[0]],submenu1)
        #for m in submenu[1]:
        #    self.appendMenu(submenu[0], [m])
        

    """
    +-----------------------------------------------+
    |          Standard necessary functions         |
    +-----------------------------------------------+
    """
    def Activated(self):
        "This function is executed when the workbench is activated"
        return


    def Deactivated(self):
        "This function is executed when the workbench is deactivated"
        return 


    def ContextMenu(self, recipient):
        "This is executed whenever the user right-clicks on screen"
        # "recipient" will be either "view" or "tree"
        self.appendContextMenu( "Assembly", self.itemsContextMenu ) # add commands to the context menu
 
 
    def GetClassName(self): 
        # this function is mandatory if this is a full python workbench
        return "Gui::PythonWorkbench"



"""
    +-----------------------------------------------+
    |          actually make the workbench          |
    +-----------------------------------------------+
"""
class a4Exc:
    exFile = None

    def __init__(self, exFile):
        self.exFile = str(exFile)
        self.ext    = self.exFile[self.exFile.rfind('.'):].lower()
        #print self.ext
    
    # 'hierarchy_nav.svg' for Demo
    #'Pixmap'  : os.path.join( ksuWB_icons_path , 'hierarchy_nav.svg') ,

    def GetResources(self):
        import os
        if 'fcstd' in self.ext:
            return {'Pixmap'  : os.path.join( asm4wb_icons_path , 'FreeCad.svg') ,
                    'MenuText': str(self.exFile),
                    'ToolTip' : "Asm4 Demo files"}        
        elif 'pdf' in self.ext:
            return {'Pixmap'  : os.path.join( asm4wb_icons_path , 'datasheet.svg') ,
                    'MenuText': str(self.exFile),
                    'ToolTip' : "Help file"}
        
    def Activated(self):
        global submenu
        FreeCAD.Console.PrintWarning('opening ' + self.exFile + "\r\n")
        import os, sys
        # So we can open the "Open File" dialog
        mw = FreeCADGui.getMainWindow()

        # Start off defaulting to the Examples directory
        # ksu_base_path = ksu_locator.module_path()
        # exs_dir_path = os.path.join(ksu_base_path, 'demo')
        # abs_ksu_path = ksu_locator.abs_module_path()
        # # Append this script's directory to sys.path
        # sys.path.append(os.path.dirname(exs_dir_path))

        # We've created a library that FreeCAD can use as well to open CQ files
        fnameDemo=(os.path.join(asm4wb_ex_path, submenu[0], self.exFile))
        ext = os.path.splitext(os.path.basename(fnameDemo))[1]
        nme = os.path.splitext(os.path.basename(fnameDemo))[0]
        if ext.lower()==".fcstd":
            FreeCAD.open(fnameDemo)
        elif ext.lower()==".pdf":
            import subprocess, sys, os
            if sys.platform == "linux" or sys.platform == "linux2":
                # linux
                if 'LD_LIBRARY_PATH' in os.environ: # workaround for AppImage
                    my_env = os.environ
                    ldlp = os.environ['LD_LIBRARY_PATH']
                    del my_env['LD_LIBRARY_PATH']
                    #print("xdg-open", fnameDemo)
                    subprocess.Popen(["xdg-open", fnameDemo], env=my_env)
                else:
                    subprocess.call(["xdg-open", fnameDemo])
                #if 'LD_LIBRARY_PATH' in os.environ:
                #    os.environ['LD_LIBRARY_PATH'] = ldlp
                #os.execve(sys.executable, ["xdg-open", fnameDemo], os.environ)
                #os.execv(sys.executable, ["xdg-open", fnameDemo])
            if sys.platform == "darwin":
                # osx
                cmd_open = 'open '+fnameDemo
                os.system(cmd_open) #win, osx
            else:
                # win
                subprocess.Popen([fnameDemo],shell=True)
##

        
for curFile in submenu1:
    FreeCADGui.addCommand(curFile, a4Exc(curFile))

wb = Assembly4_WorkBench()
Gui.addWorkbench(wb)





