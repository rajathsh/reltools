import os
import json
from flexObject import FlexObject
from flexConfigObject import FlexConfigObject
from flexStateObject import FlexStateObject

class apiGenie (object) :
    def __init__ (self, outputDir, objDescriptors, attrDescriptionsDir) :
        self.outputDir = outputDir
        self.objDescriptors = objDescriptors
        self.attrBase = attrDescriptionsDir
        self.objDict = {}
        self.buildObjects() 

    def buildObjects (self) :
        for desc  in self.objDescriptors:
            with open(desc) as fileHdl:
                objMembersData = json.load(fileHdl)                                                                        
                for objName, objInfo in objMembersData.iteritems():
                    if str(objInfo['access']) == 'w':
                        self.objDict[objName] = FlexConfigObject (objName, 
                                                                  objInfo['access'],
                                                                  objInfo['multiplicity'],
                                                                  self.attrBase + objName + "Members.json"
                                                                  )
                    elif str(objInfo['access']) == 'r':
                        self.objDict[objName] = FlexStateObject  (objName,
                                                                  objInfo['access'],
                                                                  objInfo['multiplicity'],
                                                                  self.attrBase + objName + "Members.json"
                                                                  )

    def writeApiCode(self) :
        outputFile = 'tmp.py'
        with open(outputFile, 'w+') as fileHdl:
            with open('baseCode.txt', 'r') as base:
                fileHdl.writelines(base.readlines())
            for objName, obj in self.objDict.iteritems():
                obj.writeAllMethods(fileHdl)
        

if __name__ == '__main__':
    baseDir = os.getenv('SR_CODE_BASE',None)
    if not baseDir:
        print 'Environment variable SR_CODE_BASE is not set'
    
    objDescriptors = [ baseDir + '/snaproute/src/models/' + 'genObjectConfig.json',
                       #baseDir + '/snaproute/src/models/' + 'handCodedObjInfo.json'
                     ]
    attrDescriptorsLocation = baseDir+'/reltools/codegentools/._genInfo/'
    outputDir = baseDir+'snaproute/src/flexSdk/py'
    gen = apiGenie( outputDir, objDescriptors, attrDescriptorsLocation)
    gen.writeApiCode()
