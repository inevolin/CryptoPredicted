if [ $# -eq 0 ]
then
	#mongo -u "root" -p "1561_AEI_qzef26_GRZ_ez65" --authenticationDatabase "admin"
	mongo "159.69.94.65/crypto" -u "cryptopredicted" -p "1561_AEI_qzef26_GRZ_ez65_fezo_fze6"
elif [ "$1" == "backup" ]
then
	mongodump --username "root" --password "tester" --authenticationDatabase "admin" --out mongo_backup_dump
	tar -czvf mongo_backup_dump.tar.gz mongo_backup_dump/
	rm -dfr mongo_backup_dump/
fi
