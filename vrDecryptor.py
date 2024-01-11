import os
import subprocess
from tqdm import tqdm
from time import sleep
import signal

def isVr(file):
	if file.endswith(".wsdcf"):
		return True
	else:
		return False

def main():
	errorCounter = 0
	dmmVideoPlayer = "C:\\Users\\feder\\AppData\\Local\\DMMVRPlayer\\DMMVRPlayer_Windows.exe"
	with open("vrDecryptionLog.txt", "w") as f:
		print("created log file")
	scanPath = input("Insert path containing the vr videos to decrypt: ")
	javItPath = ".\\jav-it.exe"
	fileList = []
	for file in os.listdir(scanPath):
		if isVr(file=file):
			print(f"Found the following file: {file}")
			process = subprocess.Popen([dmmVideoPlayer, file])
			sleep(20)
			process.kill()
			sleep(5)
			fileList.append(file)
	print(f"Found a total of {len(fileList)} vr files to decrypt\nNow decrypting")

	for vrFile in tqdm(fileList):
		outFile = vrFile.split(".")[0] + ".mp4"
		commandLine = " ".join([javItPath, "decrypt", "-i", vrFile, "-o", outFile, "-t", "dmm-vr"])
		print (commandLine)
		result = subprocess.run(commandLine)
		if result.returncode != 0:
			with open("vrDecryptionLog.txt", "a") as f:
				f.write("Couldn't decrypt the following file: " + vrFile + "\n\n")
				errorCounter += 1
		else:
			os.remove(vrFile)
	
	print(f"Process terminated. Decryptions failed: {errorCounter}, Check the file logs to see the files that failed decryption")

main()
