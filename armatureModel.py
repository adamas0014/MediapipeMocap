
import numpy as np
import math
import matplotlib.pyplot as plt
#import livelink

class Vec3():
    def __init__(self, x, y, z, scale =None):
        self._x = x
        self._y = y 
        self._z = z
        self._scale = scale
        
    def cross(self, other):
        crs = np.cross(self.getMatrix(), other.getMatrix())
        return(Vec3(crs[0], crs[1], crs[2]))

    def getMatrix(self):
        return[self._x, self._y, self._z]

    def getPosition(self):
        return Vec3(self._x, self._y, self._z)

    def __sub__(self, other):
        vec = other.getPosition()
        return Vec3(self._x - vec._x, self._y - vec._y, self._z - vec._z)
        
    def __add__(self, other):
        vec = other.getPosition()
        return Vec3(self._x + vec._x, self._y + vec._y, self._z + vec._z)

    def __str__(self):
        return f"( {self._x}, {self._y}, {self._z}, M {((self._x **2) + (self._y **2) + (self._z **2))**(1/2)} )"

    def __repr__(self): #debug, vebose
        return f"DEBUG [ {self._x}, {self._y}, {self._z}, M {((self._x **2) + (self._y **2) + (self._z **2))**(1/2)} ]"


class bone_base():
    #needs to take in a coordinate pair or something and replace it with a base point and a vector
    def __init__(self, name: str, boneOffset: Vec3, vector: Vec3, rot = None):
        self._bone = vector
        self._name = name
        self._boneOffset = boneOffset
        self._rot = rot
        
    
    def __str__(self):
        return(f" {self._name}: {self._bone} |")
        
    def link(self, parent, children:list):
        self._parent = parent
        self._children = children
        return self

    def setParent(self, p):
        self._parent = p
        return self._parent

    def getParent(self):
        return self._parent
    
    def getChildren(self):
        return self._children

    def getName(self):
        return self._name

    def getSpherical(self):
        r = ((self._bone._x ** 2) + (self._bone._y ** 2) + (self._bone._z ** 2))**(1/2)
        theta = math.atan(self._bone._y / self._bone._x)
        gamma = math.atan((((self._bone._x ** 2) + (self._bone._y ** 2))**(1/2)) / self._bone._z)
        return {"R": r, "T": theta, "G": gamma}

    def getOrientation(self):
        if(self._bone._rot == None): return None

        s = self.getSpherical()
        return map({"Roll": self._rot, "Pitch": s["T"], "Yaw": s["G"]}) #pretty sure this ain't right, revisit, return copy
    
    def getQuaternion(self):
        if(self._bone._rot == None): return None

        orientation = self.getOrientation()
        return quaternion(orientation["Roll"], orientation["Pitch"], orientation["Yaw"])

    def getBone(self):
        return self._bone
    def setBone(self, bone:Vec3):
        self._bone = bone
        return self._bone
    def getBoneOffset(self):
        return self._boneOffset
    
    def setGlobalOffset(self, globalOffset: Vec3):
        self._globalOffset = globalOffset
        return self._globalOffset

    def getGlobalOffset(self):
        return self._globalOffset

class bone_default(bone_base):
    pass






root = bone_default("ROOT", Vec3(0, 0, 0), Vec3(10, 10, 10))
spine = bone_default("SPINE", Vec3(0, 0, 0), Vec3(20, 50, 20))
hip = bone_default("HIP", Vec3(0, 0, 0), Vec3(20, 50, 20))
thigh = bone_default("THIGH", Vec3(0, 0, 0), Vec3(20, 50, 60))
neck = bone_default("NECK", Vec3(0, 0, 0), Vec3(30, 60, 40))


#double-linked tree
skeletonConfig = {
    root.getName(): root.link(None, [spine, hip]), 
    spine.getName(): spine.link(root, [neck]), 
    hip.getName(): hip.link(root, [thigh]),
    thigh.getName(): thigh.link(hip, [None]),
    neck.getName(): neck.link(spine, [None])
}

class quaternion():
    def __init__(self, roll, pitch, yaw):
        self._qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
        self._qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
        self._qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
        self._qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
        return [self._qx, self._qy, self._qz, self._qw]




class Armature():
    def __init__(self, name, skeletonConfig: list):
        self._name = name
        self._defaultConfig = skeletonConfig
        self._armatureConfig = skeletonConfig
        self._armature = None
    
    def getBoneByName(self, name):
        print(f"Retrieved: {str(self._armatureConfig[name])}")
        return self._armatureConfig[name]

    def orderArmature(self):
        #still need to figure out how to detect loops in the bone hierarchy
        self._armature = list()

        #find start point
        focus = [self.getBoneByName("ROOT")]

        while(focus != None and focus != [None] and focus != []):
            print(f"FocusList: {focus}")
            nextFocus = []
            for f in focus:
                print(str(f))
                #add to the iteration list
                self._armature.append(f)
                #set its children to focus
                for c in f.getChildren():
                    if(c != [None] and c != None):
                        nextFocus.append(c)
                        print(f"Appending: {str(c)}")

            #Next, iterate over the children of the previous bones in focus
            focus = nextFocus
       
        return True

    
    def findGlobalOffsets(self):
        if(self._armature == None):
            ret = self.orderArmature()
            if(ret == True):
                print("Regenerated armature list")

        

        for focus in self._armature:

            if(focus.getParent() == None):
                zero = Vec3(0, 0, 0)
                focus.setGlobalOffset(zero)
                #if we are focused on the ROOT bone, we know it's referenced to [0, 0, 0]
            
            else:
                try:
                    #if we are not focused on the ROOT bone, we'll need to add its parent global offset + length of parent bone + offset from end of parent bone
                    parentGlobalOffset = focus.getParent().getGlobalOffset()
                    focus.setGlobalOffset(parentGlobalOffset + focus.getParent().getBone() + focus.getBoneOffset())
                except:
                    return None, False

        return self._armature, True


    def findArmaturePose(self):
        points = list()
        for _, p in enumerate(self._armature):
            points.append( [p.getBone()._x, p.getBone()._y, p.getBone()._z] )

        return points

    def show(self):
        pts = self.findArmaturePose()
        print(pts)
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(projection='3d')
        for pt in pts:
            print(pt)
            self.ax.scatter3D(pt[0], pt[1], pt[2], s=40)

        plt.show()

    def __str__(self):
        try:
            ret = []
            ret.append(f"{self._name} =")
            for f in self._armature:
                ret.append(str(f))

            return ''.join(ret)

        except:
            return f"Failed to build string representation of {self._name}"
    

    def __repr__(self): #debug, verbose
        try:
            ret = []
            for f in self._armature:
                ret.append(str(f))

            return f"{self._name}: {ret}"

        except:
            return f"Failed to build string representation of {self._name}"
    



    










