1. get the Experiment into NRP: copy the entire folder "Experiment/project_traffic_signs" to nrp container Experiments
	
	- docker cp /local/path nrp:/home/bbpnrsoa/nrp/src/Experiments

2. get the Assets for the Experiment: copy the entire folder "Assets/traffic_signs" to nrp container Models

	- docker cp /local/path nrp:/home/bbpnrsoa/nrp/src/Models

3. get our version of the husky robot: copy the entire folder "Assets/traffic_husky_model" to nrp container Models. Attention, this will rewrite your husky robot model because of the same name
	
	- docker cp /local/path nrp:/home/bbpnrsoa/nrp/src/Models

4. copy "model_library.json" from "Assets" to nrp container Models/libraries
	
	- docker cp /local/path/model_library.json nrp:/home/bbpnrsoa/nrp/src/Models/libraries

5. copy "street.sdf" from "Environment" to nrp

	- docker cp /local/path/street.sdf nrp:/home/bbpnrsoa/nrp/src/Models

6. run ./create_symlinks.sh in the NRP home/bbpnrsoa/nrp/src/Models directory

6. get the neural network model: copy the frozen_inference_graph.pb and label_map.pbtxt  that are located in the "Training/trained model" in the following directory of NRP: "/home/bbpnrsoa/.opt/graph_def"

7. you need to have tensorflow object detection api installed in the container to run our experiment. Below are the instructions for installation of tensorflow

8. our experiment will appear as a template under name " Project traffic signs detection"


Installation of Tensorflow:

1.

=== Install TensorFlow in a VirtualEnv ===

TensorFlow must be installed in a separate VirtualEnv to avoid any version
conflicts with the NRP, follow the steps:

https://www.tensorflow.org/install/install_linux#installing_with_virtualenv

2. 

== Install TensorFlow Models for Object Detection ==

You will need some system level dependencies:

sudo apt-get install -y protobuf-compiler python-pil python-lxml python-pip python-dev git

If you are unable to write to /.opt, pick a different path and note it for below.

cd /.opt
git clone https://github.com/tensorflow/models
cd models/research

3.
=== now install protoc === 
=== download and extract https://github.com/protocolbuffers/protobuf/releases/download/v3.4.0/protoc-3.4.0-linux-x86_64.zip

<protoc dir>/bin/protoc object_detection/protos/*.proto --python_out=.
=== now we need to install the object_detection from the tensorflow/models/research directory into the tensorflow virtualenv:
source <path to tensorflow_venv>/bin/activate
cd /.opt/models/research
pip install -e .

4.
=== Ensure the Models Are Accessible By Your User ===

If you installed into /opt, you'll need to ensure your platform user can access/read the files.

chown -R <username> /opt/models /opt/graph_def

You may need to do this as root.
