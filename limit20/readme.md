Adding assets to NRP:

* add the whole directory with model to ~/nrp/src/Models/   (see 1)
	* it can be placed to another wrapping directory for better structure, e.g. limit20 can be placed to ~/nrp/src/Models/traffic_signs/limit20
	* edit ~/nrp/src/Models/libraries/model_library.json (see 2)
		* add to one of the categories:
		{
            "modelPath": "limit20", //name of the directory with the model
            "modelTitle": "Limit 20", // any title
            "thumbnail": "img/esv/objects/pointlight.png" // path to thumbnail for the model if there is one. In this case it's just a thumbnail of another unrelated asset
        },
    * run ~/nrp/src/Models/create-symlinks.sh which will create links to the model into gazebo directories (details in create_symlinks.sh)
    * delete cache in browser and restart experiment to see the newly added model


1. 
copy files/ditectories from your computer to container
	docker cp /local/path container_name:/full/path

2.
to edit documents in container need first to connect to a running container and run the shell
	docker exec -it container_name /bin/bash

