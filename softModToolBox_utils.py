import maya.cmds as cmds



class CustomSoftMod():
    listSms     = []
    dictOrigs   = {}
    dictDeforms = {}
    dictSms     = (dictOrigs, dictDeforms)
    
    #
    def __init__(self):
        self.sms          = None #list
        
        self.attrBuild    = "softMod"
        self.attrType     = "string"
        self.step1        = "BPM"
        self.step2        = "DONE"
        
        self.falloff      = 3
        self.slideX       = 0
        self.slideY       = 0
        self.slideZ       = 0
        
        self._listSms     = CustomSoftMod.listSms
        self._dictOrigs   = CustomSoftMod.dictOrigs
        self._dictDeforms = CustomSoftMod.dictDeforms
        self._dictSms     = CustomSoftMod.dictSms
        
    #
    '''def selectedSoftMod(self):
        for sm in self.sms:
            if sm not in self._listSms:
                self._listSms.append(sm)
                self._dictOrigs[sm]   = ""
                self._dictDeforms[sm] = ""'''
                
    #
    def getDeformerHandle(self, sm):
        handle = cmds.listConnections((sm+".matrix"), s=1)
        return handle[0]
        
    #
    def deformerAttribute(self, sm):
        cmds.addAttr(sm, ln=self.attrBuild, dt=self.attrType, k=True)
        cmds.setAttr((sm + "." + self.attrBuild), self.step1, type=self.attrType)
        
    #
    def softModBpm(self, sm):
        if not cmds.attributeQuery(self.attrBuild, node=sm, exists=True):
            self.deformerAttribute(sm)
            
            # Orig
            smOrig = cmds.group(em=True, name=(sm + "_orig"))
            cmds.parent(smOrig, sm, r=True)
            cmds.parent(smOrig, w=True)
            cmds.parent(sm, smOrig, a=True)
            pivot = cmds.xform(sm, q=True, ws=True, rp=True)
            cmds.xform(smOrig, ws=True, piv=(pivot[0], pivot[1], pivot[2]))
            
            # BPM
            deform = cmds.listConnections((sm+".worldMatrix[0]"), s=0, d=1, c=0, p=0)
            cmds.connectAttr(sm+".parentInverseMatrix", deform[0]+".bindPreMatrix")
            
            # Fill dictionnaries
            self._dictOrigs[sm]   = smOrig
            self._dictDeforms[sm] = deform[0]
            
    #
    def softModCtrl(self, sm):
        step = cmds.getAttr(sm + "." + self.attrBuild)
        if step == self.step1:
            cmds.setAttr((sm + "." + self.attrBuild), self.step2, type=self.attrType)
            
            smOrig = self._dictSms[0][sm]
            deform = self._dictSms[1][sm]
            
            # Control
            ctrlOrig = cmds.createNode('transform', name=(sm + "_ctrl_orig_toCnst"))
            ctrl     = cmds.circle(ch=0, name=(sm + "_ctrl"))
            
            cmds.addAttr(ctrl, ln="EXTRA_ATTR", at='enum', en="#####:")
            cmds.setAttr(ctrl[0]+".EXTRA_ATTR", e=True, channelBox=True)
            
            cmds.addAttr(ctrl, ln="offsetX", at='double', dv=0, k=True)
            cmds.addAttr(ctrl, ln="offsetY", at='double', dv=0, k=True)
            cmds.addAttr(ctrl, ln="offsetZ", at='double', dv=0, k=True)
            
            cmds.addAttr(ctrl, ln="falloffRadius", at='double', min=0, dv=3, k=True)
            cmds.addAttr(ctrl, ln="slideX", at='double', min= 0, max=1, dv=0, k=True)
            cmds.addAttr(ctrl, ln="slideY", at='double', min= 0, max=1, dv=0, k=True)
            cmds.addAttr(ctrl, ln="slideZ", at='double', min= 0, max=1, dv=0, k=True)
            
            cmds.addAttr(ctrl, ln="slideAll", at='double', min= 0, max=1, dv=0, k=True)
            cmds.setAttr((ctrl[0]+".slideAll"), l=True)
            
            cmds.parent(ctrl, ctrlOrig, r=True)
            cmds.delete(cmds.parentConstraint(sm, ctrlOrig))
            
            # Offset locator
            locOrig = cmds.createNode('transform', name=(sm + "_loc_orig"))
            loc     = cmds.spaceLocator(p=(0 ,0 ,0), name=(sm + "_loc") )
            
            cmds.parent(loc, locOrig)
            cmds.delete(cmds.parentConstraint(sm, locOrig))
            
            # Clean hierarchy
            all = cmds.createNode('transform', name=(sm + "_ALL_grp"))
            cmds.parent(ctrlOrig, smOrig, locOrig, all)
            
            cmds.setAttr(smOrig+".v", 0, l=True)
            cmds.setAttr(locOrig+".v", 0, l=True)
            
            # Attributes connection
            cmds.connectAttr((ctrl[0]+".falloffRadius"), (deform+".falloffRadius"))
            cmds.connectAttr((loc[0]+"Shape.worldPosition[0]"), (deform+".falloffCenter"))
            
            attrs = [".rx", ".ry", ".rz", ".sx", ".sy", ".sz"]
            for attr in attrs:
                cmds.connectAttr(ctrl[0]+attr, sm+attr)
                
            # Expression
            exp = ""
            for axis in ("X", "Y", "Z"):
                exp += '\n// {4} axis\n'.format(sm, ctrl[0], loc[0], deform, axis)
                exp += '{0}.translate{4} = {1}.translate{4} * (1-{1}.slide{4});\n'.format(sm, ctrl[0], loc[0], deform, axis)
                exp += '{2}.translate{4} = ( {1}.translate{4} * clamp(0, 1, ({1}.slide{4} + {1}.slideAll)) ) + {1}.offset{4};\n'.format(sm, ctrl[0], loc[0], deform, axis)
                #exp += '{2}.translate{4} = {1}.translate{4} * (1-{1}.slide{4});\n'.format(sm, ctrl[0], loc[0], deform, axis)
            cmds.expression(ae=0, name=(deform+"_slideEXP"), s=exp)
            
            
            # TMP
            animSet = "RIG:ANIM_accessories_set"
            if cmds.objExists(animSet):
            	cmds.sets(ctrl[0], e=True, fe=animSet)
            # TMP
            
            
            
########## Trigger
csm = CustomSoftMod()

def do_softModBpm():
    sel = cmds.ls(sl=True)
    for obj in sel:
        smHandle = csm.getDeformerHandle(obj)
        csm.softModBpm(smHandle)
    cmds.select(sel, r=True)
        
def do_softModCtrl():
    sel = cmds.ls(sl=True)
    for obj in sel:
        smHandle = csm.getDeformerHandle(obj)
        csm.softModCtrl(smHandle)
    cmds.select(sel, r=True)
