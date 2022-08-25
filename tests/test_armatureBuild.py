import armatureModel as AM
import matplotlib.pyplot as plt

def test():
    armature = AM.Armature("MyArmature", AM.skeletonConfig)

    print("hello")
    armature.findGlobalOffsets()
    print("hello2")
    print(str(armature))
    armature.show()
    
    return




if __name__ == "__main__":
    test()
