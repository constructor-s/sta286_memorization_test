@ echo off

set hour=%time:~0,2%
if "%hour:~0,1%" == " " set hour=0%hour:~1,1%
REM echo hour=%hour%
set min=%time:~3,2%
if "%min:~0,1%" == " " set min=0%min:~1,1%
REM echo min=%min%
set secs=%time:~6,2%
if "%secs:~0,1%" == " " set secs=0%secs:~1,1%
REM echo secs=%secs%

set datetimef=ecf_%hour%_%min%_%secs%

echo We will first start with a typing test. Press enter and you will be redirected to webpage. Please record your typing speed results.
pause
start "" "www.typingtest.com/test.html?minutes=1&textfile=enchanted.txt"
cls
set /p speed="Enter your typing speed result (WPM): "
echo %speed% > typingSpeed_%datetimef%.txt
cls

start noise-only.mp3
echo Running Part One of the test. Please listen to noise-only.mp3 for at least 60 seconds with headphones, KEEP NOISE PLAYING, and then we will repeat the test.
pause
echo true > noise.tmp
C:\Python27\ArcGIS10.3\python.exe memory_reaction_test.py noNoise
cls

echo ---------------------------------------------------------------

echo Now please stop white_noise.mp3 and stay in a quiet environment. Then we will repeat the test.
pause
echo false > noise.tmp
C:\Python27\ArcGIS10.3\python.exe memory_reaction_test.py noise
del noise.tmp
echo ---------------------------------------------------------------
echo Test complete! Please save all files in current directory.
pause