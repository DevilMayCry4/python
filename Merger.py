import os
dir1 = '/Users/virgil/Desktop/build2'
dir2 = '/Users/virgil/Desktop/build1'
output = '/Users/virgil/Desktop/build3'
if __name__ == '__main__':
    for obj in os.listdir(dir1):
    	if os.path.exists(os.path.join(dir2,obj)) and '.a' in obj:
    		os.system('lipo -create %s %s -output %s'%(os.path.join(dir1,obj),os.path.join(dir2,obj),os.path.join(output,obj)))
    	  