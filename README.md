# Jump

# 环境
Android设备：
Windows 11 预览体验版
Windows Subsystem for Android
（如果使用自己的手机，以上两项无需满足）

手机需在开发者模式中打开ADB调试选项，确保手机与电脑连接才可使用

ADB调试工具(adb.exe AdbWinApi.dll AdbWinUsbApi.dll)

python：
opencv_python
pyautogui（如果使用自己手机，无需满足）

# 调试
程序中 ratio 为按压时间比
ratio = 实际按压时间 / 图像中像素距离
该比例一般和屏幕比例成正比，需要根据自己手机屏幕比例修改

虚拟机在屏幕上大约为 336 * 599 像素
所以在使用本代码时，ratio应调整为
ratio = ratio / 336 * 手机宽边像素长度
或
ratio = ratio / 599 * 手机长边像素长度

ratio 这个值需要反复多次调节，以达到更高精度

# 运行
将ADB工具和本代码放在同一目录下，运行时切换到该目录运行，尽量避免中文路径

如果使用自己的安卓手机，
1.代码中所有
pyautogui.screenshot("img.png")
应替换为：
os.system("adb shell screencap -p /sdcard/img.png")
os.system("adb pull /sdcard/img.png")

2.代码中所有
pyautogui.click(X, Y)
应替换为：
os.system("adb shell input tap X Y")
且所有点击的位置需要根据自己手机的屏幕进行修改
位置为手机上的像素位置，可以截图后用电脑自带的画图工具查看

3.代码中所有
pyautogui.moveTo(screenWidth // 2, screenHeight // 2)
time.sleep(0.25)
pyautogui.mouseDown()
time.sleep(real_dis * 0.001)
pyautogui.mouseUp()
应修改为：
os.system(f"adb shell input swipe X Y X Y {real_dis}")
X，Y建议设置为手机屏幕像素长度的一半

# 其他
reborn_times 为可复活次数
有时可能为0， 有时可能为5
大多数情况为2
