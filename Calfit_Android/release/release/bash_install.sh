echo "Auto App Installation Program"
echo "-------------------------------------------"
adb devices > devices.txt

# Current number of Devices connected
myNum=1

# Number of spaces to output
myCount=0
while read line
do

if [ -n ${line%List*} ]
then

myCount=`expr $myCount + 1`

# Two consequtive spaces means no devices are connected
if [ $myCount = 2 ]
then
echo "No devices connected"
fi

else
myCount=`expr $myCount - 1`
echo "====================== The ${myNum}-th Phone has started installing ======================"
for FILE in $(ls)
do
if [[ $FILE =~ ".apk" ]]
then
echo "App ${FILE} is installing"
adb -s ${line%de*} install -r $FILE
echo "App ${FILE} completed installation"
fi
done
myNum=`expr $myNum + 1`
echo "====================== App is successfully installed ======================"
fi


done < devices.txt
