import sys, os
sys.path.append(os.path.join(sys.path[0],'./tests'))
import test_dumpPoseData as dpd
import test_threadExecutionTiming as tet
import test_armatureBuild as ab
import test_mediapipeToArmature as m2a

def i_menu():
    return f"----MENU----\n0 - EXIT\n1 - Test: Dump Pose Data\n2 - Test: Thread Execution Timing\n3 - Test: Armature Build\n4 - Mediapipe2Armature\n\n----END----\n"

def interface():
    leave = False

    while(not leave):
        print(i_menu())
        menuInput = input()
        
        if   (menuInput == '0'):    leave = True
            
        elif (menuInput == '1'):    dpd.test()

        elif (menuInput == '2'):    tet.test() 
             
        elif (menuInput == '3'):    ab.test()
            
        elif (menuInput == '4'):    m2a.test()
            
        else: print(f"{menuInput} = Invalid Option")





if __name__ == "__main__":
    interface()