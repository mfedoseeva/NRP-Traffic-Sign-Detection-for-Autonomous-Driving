* copy the entire foler "project_traffic_signs" to nrp container Experiments
``` docker cp /local/path nrp:/home/bbpnrsoa/nrp/src/Experiments
```
* copy the entire folder "traffic_signs" from "Assets" to nrp container Models
``` docker cp /local/path nrp:/home/bbpnrsoa/nrp/src/Models
```
* copy "model_library.json" from "Assets" to nrp container Models/libraries
``` docker cp /local/path/model_library.json nrp:/home/bbpnrsoa/nrp/src/Models/libraries
```
* copy "street.sdf" from "Environment" to nro container Models
``` docker cp /local/path/street.sdf nrp:/home/bbpnrsoa/nrp/src/Models
```
* clear cache in browser. if needed run ./nrp_installer.sh restart
* our experiment will appear as a template under the name "project traffic signs"