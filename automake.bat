call "D:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"
set MSYS=D:\Env_pkg\mingw64\bin        // 相当于在环境变量窗口新建一个MSYS的变量
PATH=%MSYS%;%path%;D:\Windows Kits\10\Lib\10.0.22000.0\um\x64  // 解决编译过程找不到USER32.Lib的问题
set INCLUDE=%INCLUDE%
set LIB=%LIB%
bash -c "mingw32-make ARCH=x86_64 OS=msvc"
pause
