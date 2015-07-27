exe() { echo "\$ $@" ; "$@" ; }
check_service() {
exe ping $1 -c 10 -v
exe dig $1
exe mtr -rw $1
#exe nslookup $1
#exe tracepath $1
}

TODAY=$(date +"%Y%m%d_%H%M")

echo "\n DATE"
echo "================================================\n"
echo $TODAY
echo "\n NETWORK CONFIG"
echo "================================================\n"
exe nm-tool
exe ip route show
exe curl -s checkip.dyndns.org|sed -e 's/.*Current IP Address: //' -e 's/<.*$//'

echo "\n GOOGLE CONNECTIVITY"
echo "================================================"
check_service www.google.com

echo "\n ERP SERVER CONNECTIVITY"
echo "================================================"
# WARNING: Add ERP services settings

echo "\n HELPSCOUT CONNECTIVITY"
echo "================================================"
check_service www.helpscout.net


echo "\n FTP SERVICE"
echo "================================================"
exe timeout -s KILL 10 wget ftp://ftp.cesca.cat/ubuntu/release/10.04.4/ubuntu-10.04.4-server-amd64.iso 2>&1
exe timeout -s KILL 10 wget ftp://ftp.rediris.es/mirror/CentOS/7/os/x86_64/images/boot.iso 2>&1
exe timeout -s KILL 10 wget http://ftp.nz.debian.org/debian-cd/8.1.0-live/i386/iso-hybrid/debian-live-8.1.0-i386-cinnamon-desktop.iso 2>&1

echo "\n OVH SERVICE"
echo "================================================"
check_service rbx.proof.ovh.net
exe timeout -s KILL 10 wget rbx.proof.ovh.net/files/1Gb.dat 2>&1
rm boot*.iso
rm ubuntu*.iso
rm debian*.iso
rm 1Gb.dat 
