# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]
 - delete getGINAsat.py.nodups
 - delete getGINAsatProd.py
 - delete getLatestASCAT_SBN.sh
 - delete getLatestMetar_SBN.sh
 - rewrite getLatestSat_GINA.sh (77%)
 - rewrite getLatestSat_GINA_nolog.sh (80%)
 - delete getLatestSat_SBN.sh
 - create getLatestSat_SCD.sh
 - delete getLatestSndg_SBN.sh
 - delete getLatest_SBN.sh
 - delete getMetarSBN_auto.sh
 - rename hetSnowCloudDes.py} (50%)
 - delete get_data_store.sh

## [1.0.2] - 2018-01-04
- modified the SPoRT LDM processing script to change an attribute on some incoming
  netcdf files. Needed to prevent conflicts with a few GINA files.
## [1.0.1] - 2017-10-19
### Added
- add `bin/getSST.sh` and `bin/getSST.py` - scripts to get SST 
- added a CHANGELOG.md file
### Fixed
- `bin/getMIRS.py` - bug fix for MIRS BTs
- `bin/makeMosaic.py` - bug fix for composititing NOAA POES
- `bin/processLDM_SSEC.py` - fix for river script problem
- `bin/makeMosiac.py` - bug fixes for latest version 2 of awips

## [1.0.0] - 2017-06-20
- initial 1.0.0 version to capture what was being done on EDEX

