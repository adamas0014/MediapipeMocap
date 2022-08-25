import sys, os
sys.path.append(os.path.join(sys.path[0],'../'))
import armatureModel as am

root = am.bone_default("ROOT", am.Vec3(0, 0, 0), am.Vec3(10, 10, 10))
arm = am.bone_default("ARM", am.Vec3(0, 0, 0), am.Vec3(30, 60, 40))
forearm = am.bone_default("FOREARM", am.Vec3(0, 0, 0), am.Vec3(10, 10, 10))

armConfig = {
    root.getName(): root.link(None, [arm]),
    arm.getName(): arm.link(root, [forearm]),
    forearm.getName(): forearm.link(arm, [None])
}

def test():



    
    return







if __name__ == "__main__":
    test()