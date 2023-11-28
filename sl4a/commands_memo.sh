

# start emulator
emulator -avd droid

# start RPC server
adb shell am start \
	-a com.googlecode.android_scripting.action.LAUNCH_SERVER \
	-n com.googlecode.android_scripting/.activity.ScriptingLayerServiceLauncher

# forward port
export AP_PORT=9999
adb forward tcp:9999 tcp:XXXXX
# [XXXXX] check on emu


