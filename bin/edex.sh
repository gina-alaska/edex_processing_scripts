#!/bin/bash
#-----------------------------------------------------------------------#
# Options                                                               #
#                                                                       #
# edex [status]                                                         #
#       'edex' defaults to 'edex status', notifying the user whether    #
#       edex services are on, and which ones.                      #
#                                                                       #
# edex start/stop                                                       #
#       Controls stopping / starting all edex standalone services:      #
#               edex_postgres                                           #
#               edex_camel                                              #
#               httpd_pypies                                            #
#               qpid                                                    #
#                                                                       #
# edex log [ingest|request|gribingest|datingest]                        #
#       Monitors the current day's requested log. Defaults to ingest.   #
#                                                                       #
#									#
# edex setup								#
#	Adds server IP and hostname to EDEX config files if they don't  #
#	contain the correct setting already (requires user prompt)	#
#									#
#-----------------------------------------------------------------------#
# ChangeLog                                                             #
# 07/2011 M.James/Unidata       Created                                 #
#-----------------------------------------------------------------------#

# directories definitions
AWIPS_HOME="/awips2/"
EDEX_PATH=$AWIPS_HOME'edex/'
DATA_PATH=$AWIPS_HOME'data/'
LOG_PATH=$EDEX_PATH'logs/'


# files
PG_FILE=$DATA_PATH'pg_hba.conf'
EDEX_ENV_FILE=$EDEX_PATH'bin/setup.env'
LDMD_CONF=/usr/local/ldm/etc/ldmd.conf

# valid options
options=( 'status' 'start' 'stop' 'log' 'setup' 'test' )
nopts=${options[@]}

# main program
#

# Construct IP subnet
#
# OS X
#IP=`ifconfig  | grep -E 'inet.[0-9]' | grep -v '127.0.0.1' | awk '{ print $2}'`
# Linux
IP=`/sbin/ifconfig | grep "inet addr" | grep -v 127.0.0 | grep -v 192.168 | awk '{ print $2 }' | cut -d: -f2`

# truncate
IP_CIDR="${IP%.*}"
editFiles=($PG_FILE $EDEX_ENV_FILE $LDMD_CONF)
boolFiles=(true true true)
editFuncs=(edit_pg edit_edex edit_ldm)

YMD=`date '+%Y%m%d'`

args=("$@")

# functions
edex_status() { # report back edex server on/off status
	echo ''
	echo '[edex status]'
	# CHECK POSTGRES
	postgres_prc=`ps aux | grep postgresql | grep -v grep | awk '{ print $11 }'`
        postgres_prc=`echo $postgres_prc | cut -f1 -d' '`
	if [ -z $postgres_prc ]; then
	#if [ -z $postgres_chk ]; then
		echo ' postgres    :: not running'
	else
		postgresPid=`ps aux | grep postgresql\/bin\/postmaster | grep -v grep | awk '{ print $2 }'`
		echo ' postgres    :: running :: pid '$postgresPid''
	fi

	# CHECK PYPIES
    	pypies_prc=`ps aux | grep httpd_pypies | grep -v grep | head -1 | awk '{ print $11 }'`
    	if [ -z $pypies_prc ]; then
    		echo ' pypies      :: not running'
    	else
    		pypiesPid=`ps aux | grep awips2\/httpd_pypies\/usr\/sbin\/httpd | grep -v grep | head -1 | awk '{ print $2 }'`
    		echo ' pypies      :: running :: pid '$pypiesPid''
    	fi

	# CHECK QPID
	qpid_prc=`ps aux | grep qpid- | grep -v grep | head -1 | awk '{ print $11 }'`
	if [ -z $qpid_prc ]; then
		echo ' qpid        :: not running'
	else
		qpidPid=`ps aux | grep qpid- | grep -v grep | head -1 | awk '{ print $2 }'`
		echo ' qpid        :: running :: pid '$qpidPid''
	fi

	# CHECK EDEX
	edex_ingest_ps=`ps aux | grep ingest | grep -v ingestGrib | grep -v ingestDat | awk '{ print $15 }'`
	if [ -z $edex_ingest_ps ]; then
		echo ' EDEXingest  :: not running'
	else
		edex_ingest_pid=`ps aux | grep ingest | grep -v ingestGrib | grep -v ingestDat | awk '{ print $2 }'`
		echo ' EDEXingest  :: running :: pid '$edex_ingest_pid''
	fi
	
	edex_ingestGrib_ps=`ps aux | grep ingestGrib | awk '{ print $15 }'`
	if [ -z $edex_ingestGrib_ps ]; then
		echo ' EDEXgrib    :: not running'
	else
		edex_ingestGrib_pid=`ps aux | grep ingestGrib | awk '{ print $2 }'`
		echo ' EDEXgrib    :: running :: pid '$edex_ingestGrib_pid''
	fi
	
	edex_request_ps=`ps aux | grep request | awk '{ print $15 }'`
	if [ -z $edex_request_ps ]; then
		echo ' EDEXrequest :: not running'	
	else
		edex_request_pid=`ps aux | grep request | awk '{ print $2 }'`
		echo ' EDEXrequest :: running :: pid '$edex_request_pid''
	fi

	echo ''
}

tail_log() {
	if [ -e $LOG_FILE ]; then
		echo ' :: Viewing '${LOG_FILE}'. Press CTRL+C to exit'
		echo ''
		su -c "tail --follow=name ${LOG_FILE} | grep INFO | grep Ingest | sed 's/INFO  //g' | sed 's/\[genericThreadPool-[0-9][0-9]\] //g' | sed 's/2012-07-12 //g' | sed 's/,[0-9][0-9][0-9] / /g' | sed 's/Ingest\: EDEX\: Ingest - //g'"	
	else 
		echo ' :: '$LOG_FILE' not found'
		echo ' :: Check '$LOG_PATH
		echo ''
	fi
}

edex_log() { # display todays log, default to ingest
	echo '[edex] EDEX Log Viewer'
	echo ''
	# EDEX request log
	if [ "${args[1]}" == 'request' ]; then	
		LOG_FILE=${LOG_PATH}edex-request-${YMD}.log
		tail_log
		exit;
	fi

	# EDEX ingestGrib log
	if [ "${args[1]}" == 'grib' ]; then
                LOG_FILE=${LOG_PATH}edex-ingestGrib-${YMD}.log
		tail_log
		exit;
        fi

	# EDEX ingest log (default)
	LOG_FILE=${LOG_PATH}edex-ingest-${YMD}.log
	if [ "${args[1]}" == 'ingest' ]; then
		tail_log
		exit;
	fi	
	if [ -z ${args[1]} ]; then
		echo ' :: No log specified - Defaulting to ingest log'
		tail_log
		exit;
	else
		echo 'Unknown argument' ${args[1]}' -  Viewing ingest log'
		tail_log
		exit;
	fi
}

edit_pg() { # edex pg_hba.conf
	schStr=`grep "\/24" $PG_FILE | head -1 | awk '{ print $4 }' | cut -d/ -f1`
	subStr=$IP_CIDR'.0'
	sed -i.setup_$YMD 's/'$schStr'/'$subStr'/g' $PG_FILE
	echo '[edit] '$subStr' added to '$iPG_FILE
	echo '       File backed up to '$PG_FILE'.setup_'$YMD
}

edit_ldm() { # edex pg_hba.conf
	sed -i.setup_$YMD 's/EDEX_HOSTNAME/'$HOSTNAME'/g' $LDMD_CONF
	echo '[edit] Hostname '$HOSTNAME' added to '$LDMD_CONF
}


edit_edex() { # setup.env automatic edit
	sed -i.setup_$YMD 's/localhost/'$HOSTNAME'/g' $EDEX_ENV_FILE
	#echo '[edit] '$HOSTNAME' added to '$EDEX_ENV_FILE
	echo '       File backed up to '$EDEX_ENV_FILE'.setup_'$YMD
}

edex_edits() {
	for index in ${!editFiles[*]}; do
		if ${boolFiles[$index]}; then
			${editFuncs[$index]}
		fi
	done
	echo '[done]'
	exit;
}

edex_ipexit() { # abandon ip editing, post msg to guide manual edits
	for index in ${!editFiles[*]}; do
                if ${boolFiles[$index]}; then
                        editCom+='\t'${editFiles[$index]}'\n'
                fi
        done
	echo -e '[edex] Exiting EDEX IP Setup'
	echo -e ''
	echo -e ' You may need to MANUALLY EDIT the following files'
	echo -e '\n'$editCom
	echo -e ' for EDEX to work properly. \n'
	#echo -e ' All instances of "localhost" should be replaced with the'
	#echo -e ' fully-qualified hostname of your machine.\n'
	echo -e ' Special notes:'
	echo -e ' '$PG_FILE' *must* contain your subdomain.'
	echo -e ' '$PY_FILE' *must* contain "Group fxalpha", not "Group awips"'
	echo ''
}

edex_setup() { # setup IP subnet and domains for EDEX, prompt user for confirm
	echo ''
	# run services on system startup
	chkconfig edex_postgres --add
	chkconfig httpd-pypies --add
	chkconfig qpidd --add
	chkconfig edex_camel --add
	chkconfig edex_postgres on --level 235
	chkconfig httpd-pypies on --level 235
	chkconfig qpidd on --level 235
	chkconfig edex_camel on --level 235
	echo '[edex] EDEX IP and Hostname Setup'
	# check files exist
	continue=true
	for index in ${!editFiles[*]}; do
                echo "Checking files: ${editFiles[$index]}"
		if [[ ! -f ${editFiles[$index]} ]]; then
			echo '[Error] ** '${editFiles[$index]}' not found.'
			continue=false
		fi
	done
	if ! $continue; then
		echo 'Exiting'
		exit;
	fi
	continue=false

	# pg_hba.conf

	pgGrep=`grep $IP_CIDR $PG_FILE | head -1`
	echo -n ' Checking '$PG_FILE
	if [[ ! -z ${pgGrep} ]]; then
		echo ' [OK]'
		boolFiles[0]=false
	else
		echo -e '\n      ** Missing '$IP_CIDR
		continue=true
	fi

	# EDEX env

	envGrep=`grep $HOSTNAME $EDEX_ENV_FILE | head -1`
	echo -n ' Checking '$EDEX_ENV_FILE
	if [[ ! -z ${envGrep} ]]; then
		echo ' [OK]'
		boolFiles[1]=false
	else 
		echo '      ** Missing '$HOSTNAME
		continue=true
	fi

	# LDM
	ldmGrep=`grep EDEX_HOSTNAME $LDMD_CONF | head -1`
	echo -n ' Checking '$LDMD_CONF
	if [[ ! -z ${ldmGrep} ]]; then
		echo -e '\n      ** Missing '$HOSTNAME
		continue=true
	else
		echo ' [OK]'
		boolFiles[2]=false
	fi

	echo ''
	edex_edits
	if [ $continue=true ]; then
		echo ' EDEX correctly configured'
	fi
	echo ''
}


edex_conf_check() { # check that IP and hostname are set correctly. if not, call setup
	if [[ -z `grep $IP_CIDR $PG_FILE` ]]; then
		echo '[WARN] *** File ['$PG_FILE'] contains incorrect IP addresses'
		while true; do
                	echo ''
                	read -p "Run setup now? [y/n]" eyn
                	case $eyn in
                                [Yy]* ) edex_setup; break;;
                                [Nn]* ) echo 'exiting'; exit;;
                                * ) echo "Please answer yes or no.";;
                        esac
                	echo ''
                done
		echo '        Run "edex setup" to configure'
		exit
	fi
	#if [[ -z `grep $HOSTNAME $EDEX_ENV_FILE` ]]; then
	#	echo '[WARN] *** File ['$EDEX_ENV_FILE'] contains localhost'
	#	echo '       *** Run "edex setup" to configure'
	#	exit
	#fi
}

edex_start() { # start all edex services
	#edex_conf_check
        echo "finished config check"
	sudo service edex_postgres start
	sudo service httpd-pypies start
        echo "postgre started"
	sudo service qpidd start
        echo "qpidd started"
	sudo service edex_camel start
        echo "edex_camel started"
}

edex_stop() { # stop all edex services
	sudo service edex_camel stop
	sudo service qpidd stop
	sudo service httpd-pypies stop
	sudo service edex_postgres stop
	edex_status;
}

edex_options() { # print out options for this programs
	echo ''
	echo '     edex.sh (status|start|stop|setup|log)'
	echo ''
}

edex_invalid() {
	echo ''
	echo "     Invalid option: '"${args[0]}"' not understood"
	edex_options
}

check_input() { # check input against accepted options
	found=false
	for i in "${options[@]}"
	do
		if [[ "${args[0]}" == $i ]]; then
			edexcmd='edex_'${args[0]}
			found=true
		fi
	done
	if [[ "$found" == 'false' ]]; then
		if [[ -z ${args[0]} ]]; then
			# if no input specified, default to status
			edex_status
			edex_options
		else
			# if bad command
			edex_invalid
		fi
	else
		$edexcmd
	fi
}

# check input - first/only program run
#
check_input

echo "done?"
read ans
exit;



