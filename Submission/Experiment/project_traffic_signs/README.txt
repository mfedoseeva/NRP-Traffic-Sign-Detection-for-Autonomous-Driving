To run this tutorial experiment, you'll need to perform a few prerequisite tasks:


=== Install TensorFlow in a VirtualEnv ===

TensorFlow must be installed in a separate VirtualEnv to avoid any version
conflicts with the NRP, follow the steps:

https://www.tensorflow.org/install/install_linux#installing_with_virtualenv


== Install TensorFlow Models for Object Detction ==

Install the models from the official tensorflow/models repository.

You will need some system level dependencies:

sudo apt-get install -y protobuf-compiler python-pil python-lxml python-pip python-dev git

If you are unable to write to /opt, pick a different path and note it for below.

cd /opt
git clone https://github.com/tensorflow/models
cd models/research

=== now install protoc === 
=== download and extract https://github.com/protocolbuffers/protobuf/releases/download/v3.4.0/protoc-3.4.0-linux-x86_64.zip

<protoc dir>/bin/protoc object_detection/protos/*.proto --python_out=.
=== now we need to install the object_detection from the tensorflow/models/research directory into the tensorflow virtualenv:
source <path to tensorflow_venv>/bin/activate
cd /opt/models/research
pip install -e .

=== Ensure the Models Are Accessible By Your User ===

If you installed into /opt, you'll need to ensure your platform user can access/read the files.

chown -R <username> /opt/models /opt/graph_def

You may need to do this as root.


=== Update the TensorFlow Transfer Function With Local Paths ===

You'll need to edit and update tensorflow_object_detector.py in this directory
to use the proper paths for your local install.

Update the following variables:

# based on your TensorFlow installation path above
- <path to tensorflow venv>

# if you were unable to install the models to /opt, also update:
- MODEL_BASE
- PATH_TO_CKPT
- PATH_TO_LABELS
